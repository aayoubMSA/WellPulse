#!/usr/bin/env bash
set -euo pipefail

# Run on the UE/application node after the profile instance is ready.
# Fail-closed: this node-side phase may preserve verified raw evidence in /proj,
# but it can NEVER authorize experiment teardown. Final off-POWDER verification
# belongs to the GitHub controller.

RUN_ID="${WP_RUN_ID:?WP_RUN_ID is required}"
EXPERIMENT_ID="${WP_EXPERIMENT_ID:?WP_EXPERIMENT_ID is required}"
CORE_HOST="${WP_CORE_HOST:?WP_CORE_HOST is required}"
UE_HOST="${WP_UE_HOST:-$(hostname)}"
REMOTE_USER="${WP_REMOTE_USER:-aayoub}"
REPO="${WP_REPO_ROOT:-$HOME/WellPulse}"
PY="${WP_PYTHON:-python3}"
EVDIR="${WP_EVIDENCE_ROOT:-$HOME/wellpulse-powder-evidence/golden/$RUN_ID}"
CORE_EVDIR="${WP_CORE_EVIDENCE_ROOT:-$HOME/wellpulse-powder-evidence/golden/$RUN_ID-core}"
PERSIST_ROOT="${WP_PERSIST_ROOT:-/proj/WellPulse/evidence-escrow}"
RECEIVER_LAUNCH_TIMEOUT_S="${WP_RECEIVER_LAUNCH_TIMEOUT_S:-15}"
HARD_EXPIRY_UTC="${WP_HARD_EXPIRY_UTC:-}"
SSH_OPTS=(-o BatchMode=yes -o ConnectTimeout=10 -o StrictHostKeyChecking=accept-new)
RUN_DIGEST="$(printf '%s' "$RUN_ID" | sha256sum | awk '{print substr($1,1,16)}')"
MQTT_TOPIC="wellpulse/wp-pwd01/gold/${RUN_DIGEST}/records"
SENDER_PID=""
RECEIVER_STARTED=0
GIT_SHA=""

mkdir -p "$EVDIR"/{sender,receiver,substrate,runtime,orchestration,analysis,escrow}
CONSOLE="$EVDIR/orchestration/golden_console.txt"
GATES="$EVDIR/orchestration/gate_events.jsonl"
HCI_EVENTS="$EVDIR/orchestration/hci_events.jsonl"
exec > >(tee -a "$CONSOLE") 2>&1

utc(){ date -u +%Y-%m-%dT%H:%M:%S.%NZ; }
bar(){ local p="$1" m="$2" n; n=$((p/5)); printf '\r['; printf '%*s' "$n" ''|tr ' ' '#'; printf '%*s' "$((20-n))" ''|tr ' ' '-'; printf '] %3d%%  %-52s' "$p" "$m"; }

# Non-authoritative observer only. It consumes orchestrator-owned state already
# available locally and NEVER issues SSH/API/tmcc/probe/control operations.
# Any HCI emission failure is explicitly degraded-but-non-fatal and must not
# alter scientific execution, evidence validity, or teardown interlocks.
hci_emit(){
  local g="$1" s="$2" p phase evidence persistent off teardown
  evidence=NOT_STARTED
  persistent=NOT_STARTED
  off=NOT_STARTED
  teardown=NO
  case "$g" in
    G0)  p=5;  phase=PREP ;;
    G1)  p=10; phase=PREP ;;
    G2)  p=22; phase=BASELINE ;;
    G3)  p=28; phase=RF_OUTAGE ;;
    G4)  p=38; phase=RESTORE ;;
    G5)  p=48; phase=RESTORE ;;
    G6)  p=58; phase=SERVICE_READY ;;
    G7)  p=66; phase=APPLICATION_HORIZON ;;
    G8)  p=82; phase=RECONSTRUCTION ; evidence=RAW_RECONSTRUCTED ;;
    G9)  p=92; phase=ESCROW; evidence=PERSISTENT_VERIFIED_CONTROLLER_REQUIRED; persistent=VERIFIED; off=PENDING ;;
    G10) p=96; phase=ESCROW; evidence=PENDING_CONTROLLER_FINALIZATION; persistent=VERIFIED; off=PENDING ;;
    *)   p=0; phase=PREP ;;
  esac
  if ! "$PY" "$REPO/scripts/wp2_golden_hci_emit.py" \
      --output "$HCI_EVENTS" \
      --run-id "$RUN_ID" \
      --experiment-id "$EXPERIMENT_ID" \
      --gate "$g" \
      --phase "$phase" \
      --status "$s" \
      --progress-pct "$p" \
      --code-commit "$GIT_SHA" \
      --hard-expiry-utc "$HARD_EXPIRY_UTC" \
      --evidence-state "$evidence" \
      --persistent-copy-state "$persistent" \
      --off-powder-copy-state "$off" \
      --teardown-authorized "$teardown"; then
    printf 'HCI_OBSERVER=DEGRADED_NON_AUTHORITATIVE gate=%s\n' "$g" >&2
  fi
  return 0
}

gate(){
  "$PY" - "$1" "$2" "$3" <<'PY' >> "$GATES"
import json,sys,datetime
print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'gate':sys.argv[1],'status':sys.argv[2],'detail':sys.argv[3]},sort_keys=True,separators=(',',':')))
PY
  hci_emit "$1" "$2"
}
fail(){ echo; gate "$1" FAIL "$2"; echo "GOLDEN_E2E=FAIL_$1:$2"; [[ "$1" == G9 ]] && echo 'STOP_DO_NOT_TERMINATE=1'; exit 70; }
ssh_core(){ ssh "${SSH_OPTS[@]}" "${REMOTE_USER}@$CORE_HOST" "$@"; }
ssh_ue(){ ssh "${SSH_OPTS[@]}" "${REMOTE_USER}@$UE_HOST" "$@"; }
scp_core(){ scp "${SSH_OPTS[@]}" "${REMOTE_USER}@$CORE_HOST:$1" "$2"; }
scp_ue(){ scp "${SSH_OPTS[@]}" "${REMOTE_USER}@$UE_HOST:$1" "$2"; }
cleanup_rf(){ for id in 1 33 2 34; do /usr/local/etc/emulab/tmcc attenuator "$id" 0 >/dev/null 2>&1 || true; done; }
cleanup_runtime(){
  set +e
  cleanup_rf
  if [[ -n "$SENDER_PID" ]] && kill -0 "$SENDER_PID" 2>/dev/null; then
    kill -TERM "$SENDER_PID" 2>/dev/null || true
    sleep 1
    kill -KILL "$SENDER_PID" 2>/dev/null || true
  fi
  if [[ "$RECEIVER_STARTED" -eq 1 ]]; then
    ssh_core "test -f '$CORE_EVDIR/receiver/receiver.pid' && kill -TERM \$(cat '$CORE_EVDIR/receiver/receiver.pid') 2>/dev/null || true" >/dev/null 2>&1 || true
  fi
}
trap cleanup_runtime EXIT

echo '=== WellPulse WP2 Golden E2E node phase ==='
echo "RUN_ID=$RUN_ID"
echo "EXPERIMENT_ID=$EXPERIMENT_ID"
echo "CORE_HOST=$CORE_HOST"
echo "UE_HOST=$UE_HOST"
echo "MQTT_TOPIC=$MQTT_TOPIC"
echo "PERSIST_ROOT=$PERSIST_ROOT"
echo "HCI_CONTROL_ACTIONS_ENABLED=false"
echo "START_UTC=$(utc)"

bar 5 'G0 environment identity'; echo
cd "$REPO" || fail G0 REPO_NOT_FOUND
GIT_SHA=$(git rev-parse HEAD)
PY_VERSION="$("$PY" --version 2>&1)" || fail G0 PYTHON_RUNTIME
PAHO_VERSION="$("$PY" -c 'import importlib.metadata; print(importlib.metadata.version("paho-mqtt"))')" || fail G0 PAHO_RUNTIME
[[ "$PAHO_VERSION" == 2.1.0 ]] || fail G0 "PAHO_VERSION_$PAHO_VERSION"
OPENSSL_VERSION="$(openssl version 2>/dev/null || true)"
{
  printf 'run_id=%s\nexperiment_id=%s\nue_host=%s\ncore_host=%s\nmqtt_topic=%s\ngit_sha=%s\n' "$RUN_ID" "$EXPERIMENT_ID" "$UE_HOST" "$CORE_HOST" "$MQTT_TOPIC" "$GIT_SHA"
  printf 'python=%s\npaho_mqtt=%s\nopenssl=%s\nutc=%s\n' "$PY_VERSION" "$PAHO_VERSION" "$OPENSSL_VERSION" "$(utc)"
} > "$EVDIR/runtime/ue_runtime_fingerprint.txt"
ssh_core "cd '$REPO' && echo host=\$(hostname) && echo git_sha=\$(git rev-parse HEAD) && '$PY' --version 2>&1 && '$PY' -c 'import importlib.metadata; print(\"paho_mqtt=\"+importlib.metadata.version(\"paho-mqtt\"))' && openssl version 2>&1 | sed 's/^/openssl=/' && mosquitto -h 2>&1 | head -1 | sed 's/^/mosquitto=/' && echo utc=\$(date -u +%Y-%m-%dT%H:%M:%S.%NZ)" > "$EVDIR/runtime/core_runtime_fingerprint.txt" || fail G0 CORE_IDENTITY
[[ -s "$EVDIR/runtime/ue_runtime_fingerprint.txt" && -s "$EVDIR/runtime/core_runtime_fingerprint.txt" ]] || fail G0 EMPTY_FINGERPRINT
grep -q '^paho_mqtt=2.1.0$' "$EVDIR/runtime/core_runtime_fingerprint.txt" || fail G0 CORE_PAHO_VERSION
gate G0 PASS "$GIT_SHA"

bar 10 'G1 clean run identity and paths'; echo
[[ ! -e "$EVDIR/sender/sender_summary.json" ]] || fail G1 RUN_DIR_NOT_CLEAN
ssh_core "rm -rf '$CORE_EVDIR'; mkdir -p '$CORE_EVDIR/receiver' '$CORE_EVDIR/substrate'" || fail G1 CORE_DIR_INIT
gate G1 PASS CLEAN

bar 16 'G2 starting TLS broker and retrieving CA'; echo
ssh_core "cd '$REPO' && bash powder/wp2_h_epc_broker.sh /tmp/wellpulse-wp2-golden-broker" > "$EVDIR/substrate/broker_start.txt" || fail G2 BROKER_START
scp_core "/tmp/wellpulse-wp2-golden-broker/ca.crt" "$EVDIR/substrate/ca.crt" || fail G2 CA_COPY
[[ -s "$EVDIR/substrate/ca.crt" ]] || fail G2 CA_EMPTY
ping -I tun_srsue -c 5 -W 2 172.16.0.1 | tee "$EVDIR/substrate/q0_pre_ping.txt" || fail G2 Q0_PING
# -brief preserves verification evidence without persisting TLS session secrets.
openssl s_client -brief -connect 172.16.0.1:8883 -CAfile "$EVDIR/substrate/ca.crt" -verify_return_error -verify_ip 172.16.0.1 </dev/null > "$EVDIR/substrate/q0_pre_tls.txt" 2>&1 || fail G2 Q0_TLS
grep -q 'Verification: OK' "$EVDIR/substrate/q0_pre_tls.txt" || fail G2 Q0_TLS_VERIFY
gate G2 PASS READY

bar 22 'G2 launching detached receiver on core node'; echo
command -v timeout >/dev/null 2>&1 || fail G2 TIMEOUT_COMMAND_MISSING
RECEIVER_LAUNCH_T0=$(date +%s)
if ! timeout "${RECEIVER_LAUNCH_TIMEOUT_S}s" ssh -n "${SSH_OPTS[@]}" "${REMOTE_USER}@$CORE_HOST" "set -eu; cd '$REPO'; nohup '$PY' scripts/wp_pwd01_h_receiver.py --run-id '$RUN_ID' --host 172.16.0.1 --port 8883 --topic '$MQTT_TOPIC' --ca-file /tmp/wellpulse-wp2-golden-broker/ca.crt --output-dir '$CORE_EVDIR/receiver' </dev/null > '$CORE_EVDIR/receiver/receiver_console.txt' 2>&1 & pid=\$!; echo \$pid > '$CORE_EVDIR/receiver/receiver.pid'; printf 'receiver_pid=%s\\n' \"\$pid\""; then
  fail G2 RECEIVER_START_TIMEOUT
fi
RECEIVER_LAUNCH_ELAPSED=$(( $(date +%s) - RECEIVER_LAUNCH_T0 ))
[[ "$RECEIVER_LAUNCH_ELAPSED" -le "$RECEIVER_LAUNCH_TIMEOUT_S" ]] || fail G2 RECEIVER_START_BOUND
RECEIVER_STARTED=1
sleep 3
ssh_core "pid=\$(cat '$CORE_EVDIR/receiver/receiver.pid'); kill -0 \"\$pid\"; test -s '$CORE_EVDIR/receiver/receiver_events.jsonl'" || fail G2 RECEIVER_NOT_READY
echo "RECEIVER_LAUNCH_ELAPSED_S=$RECEIVER_LAUNCH_ELAPSED"
gate G2 PASS "RECEIVER_READY launch_s=$RECEIVER_LAUNCH_ELAPSED"

bar 28 'G3 launching fixed Golden workload/RF runner'; echo
SERVICE_MARKER="$EVDIR/substrate/service_ready.marker"
nohup "$PY" scripts/wp_pwd01_golden_sender.py --run-id "$RUN_ID" --host 172.16.0.1 --port 8883 --ca-file "$EVDIR/substrate/ca.crt" --output-dir "$EVDIR/sender" --service-ready-file "$SERVICE_MARKER" > "$EVDIR/sender/sender_console.txt" 2>&1 &
SENDER_PID=$!
echo "$SENDER_PID" > "$EVDIR/sender/sender.pid"
gate G3 PASS "sender_pid=$SENDER_PID"

bar 38 'G4 waiting for physical Q3->Q0 restoration'; echo
DEADLINE=$(( $(date +%s) + 240 ))
while [[ ! -s "$EVDIR/sender/rf_restore.ready" && $(date +%s) -lt $DEADLINE ]]; do kill -0 "$SENDER_PID" 2>/dev/null || fail G4 SENDER_EXITED_EARLY; sleep 1; done
[[ -s "$EVDIR/sender/rf_restore.ready" ]] || fail G4 RF_RESTORE_TIMEOUT
T_RF_RESTORE=$(cat "$EVDIR/sender/rf_restore.ready")
gate G4 PASS "$T_RF_RESTORE"

bar 48 'G5 deterministic clean-order LTE restoration'; echo
WP_CORE_HOST="$CORE_HOST" WP_UE_HOST="$UE_HOST" WP_REMOTE_USER="$REMOTE_USER" WP_RESTORE_OUT="$EVDIR/substrate/service_restore.txt" bash scripts/wp2_golden_service_restore.sh || fail G5 RESTORE_SEQUENCE
RESTORE_START_EPOCH=$(awk -F= '/^RESTORE_START_EPOCH=/{print $2}' "$EVDIR/substrate/service_restore.txt" | tail -1)
[[ -n "$RESTORE_START_EPOCH" ]] || fail G5 RESTORE_START_MISSING
scp_core "/tmp/wp2-golden-core-start.console" "$EVDIR/substrate/core_start.console" || fail G5 CORE_CONSOLE_COPY
scp_ue "/tmp/wp2-golden-ue-start.console" "$EVDIR/substrate/ue_start.console" || fail G5 UE_CONSOLE_COPY
gate G5 PASS COMPLETE

bar 58 'G6 architecture-blind 120 s service-ready gate'; echo
WP_CA_FILE="$EVDIR/substrate/ca.crt" WP_RESTORE_START_EPOCH="$RESTORE_START_EPOCH" WP_SERVICE_PROBE_OUT="$EVDIR/substrate/service_ready_probe.txt" bash scripts/wp2_golden_service_ready_probe.sh || fail G6 SERVICE_RESTORE
T_SERVICE_READY=$(awk -F= '/^T_SERVICE_READY=/{print $2}' "$EVDIR/substrate/service_ready_probe.txt" | tail -1)
[[ -n "$T_SERVICE_READY" ]] || fail G6 READY_TIMESTAMP_MISSING
printf '%s\n' "$T_SERVICE_READY" > "$SERVICE_MARKER"
gate G6 PASS "$T_SERVICE_READY"

bar 66 'G7 fixed 300 s application observation'; echo
wait "$SENDER_PID" || fail G7 SENDER_FIXED_HORIZON
SENDER_PID=""
[[ $("$PY" -c "import json;print(json.load(open('$EVDIR/sender/sender_summary.json'))['status'])") == GOLDEN_FIXED_HORIZON_COMPLETE ]] || fail G7 BAD_SENDER_STATUS
gate G7 PASS 300S_COMPLETE

bar 74 'Collecting receiver and substrate evidence'; echo
ssh_core "test -f '$CORE_EVDIR/receiver/receiver.pid' && kill -TERM \$(cat '$CORE_EVDIR/receiver/receiver.pid') 2>/dev/null || true; sleep 2" || true
RECEIVER_STARTED=0
scp -r "${SSH_OPTS[@]}" "${REMOTE_USER}@$CORE_HOST:$CORE_EVDIR/receiver/." "$EVDIR/receiver/" || fail G8 RECEIVER_COPY
ssh_core "tmux list-panes -a -F '#S:#I.#P' 2>/dev/null | while read p; do echo '=== PANE ' \"\$p\" ' ==='; tmux capture-pane -p -S -3000 -t \"\$p\" 2>/dev/null || true; done" > "$EVDIR/substrate/core_tmux_capture.txt" || fail G8 CORE_TMUX_CAPTURE
ssh_ue "tmux list-panes -a -F '#S:#I.#P' 2>/dev/null | while read p; do echo '=== PANE ' \"\$p\" ' ==='; tmux capture-pane -p -S -3000 -t \"\$p\" 2>/dev/null || true; done" > "$EVDIR/substrate/ue_tmux_capture.txt" || fail G8 UE_TMUX_CAPTURE
[[ -s "$EVDIR/substrate/core_tmux_capture.txt" && -s "$EVDIR/substrate/ue_tmux_capture.txt" ]] || fail G8 EMPTY_TMUX_CAPTURE
scp_core "/tmp/epc.log" "$EVDIR/substrate/epc.log" 2>/dev/null || scp_core "/tmp/srsepc.log" "$EVDIR/substrate/epc.log" 2>/dev/null || true
scp_core "/tmp/enb.log" "$EVDIR/substrate/enb.log" 2>/dev/null || scp_core "/tmp/srsenb.log" "$EVDIR/substrate/enb.log" 2>/dev/null || true
scp_ue "/tmp/ue.log" "$EVDIR/substrate/ue.log" 2>/dev/null || scp_ue "/tmp/wp2-srsue.log" "$EVDIR/substrate/ue.log" 2>/dev/null || true

bar 82 'G8 reconstructing endpoint from raw evidence'; echo
"$PY" scripts/reconstruct_wp2_golden.py --root "$EVDIR" || fail G8 RECONSTRUCTION
gate G8 PASS RECONSTRUCTABLE

bar 92 'G9 copying and verifying persistent /proj escrow'; echo
WP_EVIDENCE_SRC="$EVDIR" WP_RUN_ID="$RUN_ID" WP_EXPERIMENT_ID="$EXPERIMENT_ID" WP_PERSIST_ROOT="$PERSIST_ROOT" WP_EVIDENCE_INVENTORY="$REPO/experiments/WP-PWD01/evidence_inventory_golden_v1.txt" bash scripts/wp2_golden_evidence_escrow.sh || fail G9 PERSISTENT_ESCROW
PDIR="$PERSIST_ROOT/$EXPERIMENT_ID/$RUN_ID"
[[ -s "$PDIR/escrow/PERSISTENT_ESCROW_GATE.PASS" ]] || fail G9 PERSISTENT_MARKER_MISSING
printf 'run_id=%s\nexperiment_id=%s\npersistent_dir=%s\nutc=%s\n' \
  "$RUN_ID" "$EXPERIMENT_ID" "$PDIR" "$(utc)" > "$PDIR/escrow/CONTROLLER_OFFPOWDER_REQUIRED"
gate G9 PASS PERSISTENT_VERIFIED_CONTROLLER_COPY_REQUIRED
hci_emit G10 PENDING

bar 100 'Node phase safely complete; controller escrow required'; echo
printf 'GOLDEN_NODE_PHASE=PASS_PERSISTENT_ESCROW\n'
printf 'PERSISTENT_EVIDENCE=%s\n' "$PDIR"
printf 'RAW_EVIDENCE_COMPLETE=PASS\n'
printf 'CONTROLLER_OFFPOWDER_GATE=PENDING\n'
printf 'EVIDENCE_ESCROW_GATE=PENDING_CONTROLLER_COPY\n'
printf 'GOLDEN_E2E=PENDING_CONTROLLER_FINALIZATION\n'
printf 'TEARDOWN_AUTHORIZED=NO\n'