#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$(mktemp -d)}"
SRC="$ROOT/source"
PERSIST="$ROOT/persist"
OFF="$ROOT/offtestbed"
RCLONE_LOCAL="$ROOT/rclone-remote"
RUN_ID="wp2-golden-offline-qa"
EXP_ID="OFFLINE-QA"

bar(){
  local p="$1" m="$2" n
  n=$((p/5))
  printf '\r['
  printf '%*s' "$n" ''|tr ' ' '#'
  printf '%*s' "$((20-n))" ''|tr ' ' '-'
  printf '] %3d%%  %-48s' "$p" "$m"
}

echo '=== WP2 Golden offline QA ==='
bar 5 'Creating synthetic evidence tree'; echo
mkdir -p "$SRC"/{sender,receiver,substrate,runtime,orchestration,analysis} "$RCLONE_LOCAL"

cat > "$SRC/sender/attenuation_timeline.csv" <<'EOF'
command_start_utc,command_end_utc,programmed_attenuation_db,attenuator_ids
2026-08-26T18:00:00+00:00,2026-08-26T18:00:01+00:00,0,1 33 2 34
2026-08-26T18:01:00+00:00,2026-08-26T18:01:01+00:00,55,1 33 2 34
2026-08-26T18:03:01+00:00,2026-08-26T18:03:02+00:00,0,1 33 2 34
EOF
cat > "$SRC/sender/telemetry_generated.csv" <<'EOF'
record_id,generated_ts_utc,payload_sha256,payload_json
r1,2026-08-26T18:02:58+00:00,a,{}
r2,2026-08-26T18:03:01+00:00,b,{}
r3,2026-08-26T18:03:02+00:00,c,{}
r4,2026-08-26T18:03:03+00:00,d,{}
EOF
cat > "$SRC/receiver/telemetry_received.csv" <<'EOF'
record_id,received_ts_utc,payload_sha256,payload_json,mqtt_qos,mqtt_retain
r1,2026-08-26T18:03:20+00:00,a,{},1,false
r2,2026-08-26T18:03:22+00:00,b,{},1,false
r3,2026-08-26T18:03:25+00:00,c,{},1,false
EOF
cat > "$SRC/substrate/service_ready_probe.txt" <<'EOF'
T_SERVICE_READY=2026-08-26T18:03:15+00:00
WP2_GOLDEN_SERVICE_READY=PASS
EOF

printf '{"run_id":"%s","status":"GOLDEN_FIXED_HORIZON_COMPLETE"}\n' "$RUN_ID" > "$SRC/sender/sender_summary.json"
printf '{"run_id":"%s","scored":false}\n' "$RUN_ID" > "$SRC/sender/golden_manifest.json"
printf 'utc,connected,pending_count,app_inflight_count,published_calls,puback_callbacks\n2026-08-26T18:03:15+00:00,true,3,1,3,2\n' > "$SRC/sender/queue_timeline.csv"
printf '{"event":"connect"}\n' > "$SRC/sender/mqtt_events.jsonl"
printf 'sqlite-placeholder\n' > "$SRC/sender/w1_queue.sqlite"
printf '{"event":"receiver_connect"}\n' > "$SRC/receiver/receiver_events.jsonl"
printf 'restore\n' > "$SRC/substrate/service_restore.txt"
printf 'core start\n' > "$SRC/substrate/core_start.console"
printf 'ue start\n' > "$SRC/substrate/ue_start.console"
printf 'core tmux capture\n' > "$SRC/substrate/core_tmux_capture.txt"
printf 'ue tmux capture\n' > "$SRC/substrate/ue_tmux_capture.txt"
printf 'epc\n' > "$SRC/substrate/epc.log"
printf 'enb\n' > "$SRC/substrate/enb.log"
printf 'ue\n' > "$SRC/substrate/ue.log"
printf 'core runtime\n' > "$SRC/runtime/core_runtime_fingerprint.txt"
printf 'ue runtime\n' > "$SRC/runtime/ue_runtime_fingerprint.txt"
printf 'golden console\n' > "$SRC/orchestration/golden_console.txt"
printf '{"gate":"offline_qa"}\n' > "$SRC/orchestration/gate_events.jsonl"

bar 20 'Running Golden reconstruction from raw files'; echo
python3 scripts/reconstruct_wp2_golden.py --root "$SRC"
grep -q '"primary_cohort_count": 3' "$SRC/analysis/golden_reconstruction.json"
grep -q '"received_valid_by_horizon": 3' "$SRC/analysis/golden_reconstruction.json"
grep -q '"completeness_300": 1.0' "$SRC/analysis/golden_reconstruction.json"

bar 40 'Running dual-filesystem escrow simulation'; echo
WP_EVIDENCE_SRC="$SRC" WP_RUN_ID="$RUN_ID" WP_EXPERIMENT_ID="$EXP_ID" \
WP_PERSIST_ROOT="$PERSIST" WP_OFF_POWDER_ROOT="$OFF" \
WP_EVIDENCE_INVENTORY="experiments/WP-PWD01/evidence_inventory_golden_v1.txt" \
bash scripts/wp2_golden_evidence_escrow.sh

PDIR="$PERSIST/$EXP_ID/$RUN_ID"
ODIR="$OFF/$EXP_ID/$RUN_ID"
bar 58 'Running filesystem teardown interlock'; echo
WP_PERSIST_EVIDENCE_DIR="$PDIR" WP_OFF_POWDER_EVIDENCE_DIR="$ODIR" WP_RUN_ID="$RUN_ID" \
bash scripts/wp2_golden_teardown_guard.sh | tee "$ROOT/teardown.txt"
grep -q '^TEARDOWN_AUTHORIZED=YES$' "$ROOT/teardown.txt"

bar 70 'Testing rclone remote copy/read-back SHA verification'; echo
RROOT=":local:$RCLONE_LOCAL"
WP_LOCAL_VERIFIED_ROOT="$PDIR" WP_RCLONE_REMOTE_ROOT="$RROOT" WP_RUN_ID="$RUN_ID" WP_EXPERIMENT_ID="$EXP_ID" \
bash scripts/wp2_golden_offpowder_rclone.sh | tee "$ROOT/rclone-copy.txt"
REMOTE_DIR="$RROOT/$EXP_ID/$RUN_ID"
WP_PERSIST_EVIDENCE_DIR="$PDIR" WP_RCLONE_EVIDENCE_DIR="$REMOTE_DIR" WP_RUN_ID="$RUN_ID" \
bash scripts/wp2_golden_teardown_guard_rclone.sh | tee "$ROOT/rclone-guard.txt"
grep -q '^TEARDOWN_AUTHORIZED=YES$' "$ROOT/rclone-guard.txt"

bar 85 'Testing fail-closed corruption behavior'; echo
printf 'corruption\n' >> "$ODIR/sender/telemetry_generated.csv"
set +e
WP_PERSIST_EVIDENCE_DIR="$PDIR" WP_OFF_POWDER_EVIDENCE_DIR="$ODIR" WP_RUN_ID="$RUN_ID" \
bash scripts/wp2_golden_teardown_guard.sh > "$ROOT/corrupt-guard.txt" 2>&1
RC=$?
set -e
[[ "$RC" -ne 0 ]]
! grep -q '^TEARDOWN_AUTHORIZED=YES$' "$ROOT/corrupt-guard.txt"

bar 100 'Offline reconstruction/escrow/interlock QA PASS'; echo
printf 'QA_ROOT=%s\n' "$ROOT"
printf 'WP2_GOLDEN_OFFLINE_QA=PASS\n'
