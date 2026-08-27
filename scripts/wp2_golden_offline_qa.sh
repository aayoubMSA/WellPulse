#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-$(mktemp -d)}"
SRC="$ROOT/source"
PERSIST="$ROOT/persist"
CONTROLLER="$ROOT/controller"
ROUNDTRIP="$ROOT/independent-roundtrip"
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
bar 3 'Checking static Golden/controller/HCI contracts'; echo
PYTHONPATH=src python3 - <<'PY'
from pathlib import Path
from wellpulse.transport import make_run_topic
run_id='wp2-golden-offline-qa'
expected=make_run_topic(run_id,'GOLDEN')
assert expected.startswith('wellpulse/wp-pwd01/gold/'), expected
orch=Path('scripts/wp2_golden_orchestrator.sh').read_text()
assert 'MQTT_TOPIC="wellpulse/wp-pwd01/gold/${RUN_DIGEST}/records"' in orch
assert "--topic '$MQTT_TOPIC'" in orch
unsafe='local p="$1" m="$2" n=$((p/5))'
for name in (
    'scripts/wp2_golden_orchestrator.sh',
    'scripts/wp2_golden_evidence_escrow.sh',
    'scripts/wp2_golden_service_restore.sh',
    'scripts/wp2_golden_service_ready_probe.sh',
):
    text=Path(name).read_text()
    assert unsafe not in text, f'unsafe set -u progress helper remains in {name}'
escrow=Path('scripts/wp2_golden_evidence_escrow.sh').read_text()
assert 'CONTROLLER_OFFPOWDER_REQUIRED' in escrow
assert 'TEARDOWN_AUTHORIZED=NO' in escrow
verifier=Path('scripts/wp2_controller_verify_artifact_roundtrip.sh').read_text()
for marker in ('CONTROLLER_OFFPOWDER_GATE=PASS','EVIDENCE_ESCROW_GATE=PASS','TEARDOWN_AUTHORIZED=YES'):
    assert marker in verifier, marker

# HCI is a passive observer, not a second control plane.
assert 'HCI_CONTROL_ACTIONS_ENABLED=false' in orch
assert 'HCI_OBSERVER=DEGRADED_NON_AUTHORITATIVE' in orch
assert 'hci_emit G10 PENDING' in orch
hci=Path('scripts/wp2_golden_hci_emit.py').read_text()
for forbidden in ('subprocess', 'paramiko', 'requests', 'socket'):
    assert forbidden not in hci, f'forbidden HCI control/probe dependency: {forbidden}'
assert 'hci_control_actions_enabled' in hci
assert 'independent_probes' in hci
assert 'teardown_authorized' in hci
inventory=Path('experiments/WP-PWD01/evidence_inventory_golden_v1.txt').read_text()
assert 'CONDITIONAL|orchestration/hci_events.jsonl|yes|' in inventory
assert 'REQUIRED|orchestration/hci_events.jsonl|' not in inventory
print('STATIC_GOLDEN_CONTROLLER_HCI_CONTRACTS=PASS')
PY

bar 7 'Creating synthetic evidence tree'; echo
mkdir -p "$SRC"/{sender,receiver,substrate,runtime,orchestration,analysis} "$CONTROLLER" "$ROUNDTRIP"

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

bar 14 'Generating and validating passive HCI event'; echo
python3 scripts/wp2_golden_hci_emit.py \
  --output "$SRC/orchestration/hci_events.jsonl" \
  --run-id "$RUN_ID" --experiment-id "$EXP_ID" \
  --gate G6 --phase SERVICE_READY --status PASS --progress-pct 58 \
  --code-commit offline-qa \
  --evidence-state NOT_STARTED --persistent-copy-state NOT_STARTED \
  --off-powder-copy-state NOT_STARTED --teardown-authorized NO \
  | tee "$ROOT/hci-stdout.txt"
grep -q '^HCI_EVENT=' "$ROOT/hci-stdout.txt"
python3 - "$SRC/orchestration/hci_events.jsonl" <<'PY'
import json,sys
p=sys.argv[1]
rows=[json.loads(line) for line in open(p, encoding='utf-8') if line.strip()]
assert len(rows)==1
x=rows[0]
assert x['schema_version']=='wp2-hci-v1'
assert x['gate']=='G6' and x['phase']=='SERVICE_READY' and x['progress_pct']==58
assert x['scored_run'] is False
assert x['hci_control_actions_enabled'] is False
assert x['independent_probes']=='DISABLED'
assert x['teardown_authorized']=='NO'
assert 'detail' not in x
print('PASSIVE_HCI_EVENT_QA=PASS')
PY

bar 20 'Running Golden reconstruction from raw files'; echo
python3 scripts/reconstruct_wp2_golden.py --root "$SRC"
grep -q '"primary_cohort_count": 3' "$SRC/analysis/golden_reconstruction.json"
grep -q '"received_valid_by_horizon": 3' "$SRC/analysis/golden_reconstruction.json"
grep -q '"completeness_300": 1.0' "$SRC/analysis/golden_reconstruction.json"

bar 40 'Running persistent escrow simulation'; echo
WP_EVIDENCE_SRC="$SRC" WP_RUN_ID="$RUN_ID" WP_EXPERIMENT_ID="$EXP_ID" \
WP_PERSIST_ROOT="$PERSIST" \
WP_EVIDENCE_INVENTORY="experiments/WP-PWD01/evidence_inventory_golden_v1.txt" \
bash scripts/wp2_golden_evidence_escrow.sh | tee "$ROOT/persistent-escrow.txt"

PDIR="$PERSIST/$EXP_ID/$RUN_ID"
[[ -s "$PDIR/escrow/PERSISTENT_ESCROW_GATE.PASS" ]]
[[ -s "$PDIR/escrow/CONTROLLER_OFFPOWDER_REQUIRED" ]]
[[ -s "$PDIR/orchestration/hci_events.jsonl" ]]
grep -q '^TEARDOWN_AUTHORIZED=NO$' "$PDIR/escrow/CONTROLLER_OFFPOWDER_REQUIRED"
grep -q '^PERSISTENT_ESCROW_GATE=PASS$' "$ROOT/persistent-escrow.txt"
grep -q '^CONTROLLER_OFFPOWDER_GATE=PENDING$' "$ROOT/persistent-escrow.txt"
! grep -q '^TEARDOWN_AUTHORIZED=YES$' "$ROOT/persistent-escrow.txt"

bar 60 'Building deterministic controller bundle'; echo
BUNDLE="$CONTROLLER/wp2-offpowder-qa.tar"
tar --sort=name --mtime='UTC 1970-01-01' --owner=0 --group=0 --numeric-owner \
  -C "$PDIR" -cf "$BUNDLE" .
[[ -s "$BUNDLE" ]]
BUNDLE_SHA="$(sha256sum "$BUNDLE" | awk '{print $1}')"
[[ "$BUNDLE_SHA" =~ ^[0-9a-f]{64}$ ]]
printf 'CONTROLLER_PULL_GATE=PASS\nCONTROLLER_BUNDLE_SHA256=%s\n' "$BUNDLE_SHA" > "$ROOT/controller-pull-simulated.txt"

bar 75 'Testing independent controller round-trip verification'; echo
ROUNDTRIP_TAR="$ROUNDTRIP/wp2-offpowder-qa.tar"
cp "$BUNDLE" "$ROUNDTRIP_TAR"
WP_ROUNDTRIP_TAR="$ROUNDTRIP_TAR" WP_EXPECTED_BUNDLE_SHA256="$BUNDLE_SHA" \
WP_VERIFY_DIR="$ROOT/verified" \
bash scripts/wp2_controller_verify_artifact_roundtrip.sh | tee "$ROOT/controller-roundtrip.txt"
grep -q '^CONTROLLER_OFFPOWDER_GATE=PASS$' "$ROOT/controller-roundtrip.txt"
grep -q "^ROUNDTRIP_BUNDLE_SHA256=$BUNDLE_SHA$" "$ROOT/controller-roundtrip.txt"
grep -q '^EVIDENCE_ESCROW_GATE=PASS$' "$ROOT/controller-roundtrip.txt"
grep -q '^TEARDOWN_AUTHORIZED=YES$' "$ROOT/controller-roundtrip.txt"

bar 88 'Testing fail-closed outer-hash corruption'; echo
cp "$BUNDLE" "$ROOT/corrupt-outer.tar"
printf 'corruption\n' >> "$ROOT/corrupt-outer.tar"
set +e
WP_ROUNDTRIP_TAR="$ROOT/corrupt-outer.tar" WP_EXPECTED_BUNDLE_SHA256="$BUNDLE_SHA" \
bash scripts/wp2_controller_verify_artifact_roundtrip.sh > "$ROOT/corrupt-outer.txt" 2>&1
RC=$?
set -e
[[ "$RC" -ne 0 ]]
grep -q '^CONTROLLER_OFFPOWDER_GATE=FAIL:BUNDLE_SHA_MISMATCH$' "$ROOT/corrupt-outer.txt"
grep -q '^TEARDOWN_AUTHORIZED=NO$' "$ROOT/corrupt-outer.txt"
! grep -q '^TEARDOWN_AUTHORIZED=YES$' "$ROOT/corrupt-outer.txt"

bar 95 'Testing fail-closed internal raw-hash corruption'; echo
mkdir -p "$ROOT/internal-corrupt"
tar -xf "$BUNDLE" -C "$ROOT/internal-corrupt"
printf 'corruption\n' >> "$ROOT/internal-corrupt/sender/telemetry_generated.csv"
INTERNAL_BAD="$ROOT/internal-corrupt.tar"
tar --sort=name --mtime='UTC 1970-01-01' --owner=0 --group=0 --numeric-owner \
  -C "$ROOT/internal-corrupt" -cf "$INTERNAL_BAD" .
INTERNAL_BAD_SHA="$(sha256sum "$INTERNAL_BAD" | awk '{print $1}')"
set +e
WP_ROUNDTRIP_TAR="$INTERNAL_BAD" WP_EXPECTED_BUNDLE_SHA256="$INTERNAL_BAD_SHA" \
bash scripts/wp2_controller_verify_artifact_roundtrip.sh > "$ROOT/corrupt-internal.txt" 2>&1
RC=$?
set -e
[[ "$RC" -ne 0 ]]
grep -q '^CONTROLLER_OFFPOWDER_GATE=FAIL:INTERNAL_RAW_HASH_MISMATCH$' "$ROOT/corrupt-internal.txt"
grep -q '^TEARDOWN_AUTHORIZED=NO$' "$ROOT/corrupt-internal.txt"
! grep -q '^TEARDOWN_AUTHORIZED=YES$' "$ROOT/corrupt-internal.txt"

bar 100 'Offline HCI/reconstruction/controller escrow/interlock QA PASS'; echo
printf 'QA_ROOT=%s\n' "$ROOT"
printf 'PASSIVE_HCI_EVENT_QA=PASS\n'
printf 'HCI_CONTROL_ACTIONS_ENABLED=false\n'
printf 'WP2_GOLDEN_OFFLINE_QA=PASS\n'
printf 'POWDER_CONTACT=NO\n'
printf 'DRIVE_CONTACT=NO\n'
printf 'SCIENTIFIC_RUN=NO\n'