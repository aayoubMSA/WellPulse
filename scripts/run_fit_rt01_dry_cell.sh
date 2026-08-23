#!/usr/bin/env bash
set -euo pipefail

ARCH="${1:?architecture required}"
RUN_ID="${2:?run id required}"
OUT_ROOT="${3:?local output root required}"

: "${FIT_LOGIN:?}"
: "${FIT_PASSWORD:?}"
: "${SITE:?}"
: "${LOC:?}"
: "${EXP_ID:?}"
: "${SSH_KEY:?}"

case "$ARCH" in
  B0_publish_only) GATE="baseline" ;;
  W1_offline_first) GATE="complete" ;;
  *) echo "unsupported architecture: $ARCH" >&2; exit 2 ;;
esac

SSH_OPTS=(-i "$SSH_KEY" -o StrictHostKeyChecking=accept-new -o ConnectTimeout=20)
FRONTEND="${FIT_LOGIN}@${SITE}.iot-lab.info"
REL_BASE="shared/.iotlabsshcli/wp-rt01-dry/${RUN_ID}"
COMMON_REL="shared/.iotlabsshcli/wp-rt01-dry/common"
TOPIC="iotlab/${FIT_LOGIN}/wellpulse/wp-rt01/${RUN_ID}/records"
PROBE_TOPIC="iotlab/${FIT_LOGIN}/wellpulse/wp-rt01/${RUN_ID}/probe"
LOCAL_DIR="${OUT_ROOT}/${RUN_ID}"
mkdir -p "$LOCAL_DIR"

run_node() {
  local label="$1"
  local cmd="$2"
  local out="$LOCAL_DIR/${label}.json"
  iotlab-ssh -i "$EXP_ID" run-cmd "$cmd" -l "$LOC" > "$out"
  cat "$out"
  python - "$out" <<'PY'
import json, sys
p=sys.argv[1]
data=json.load(open(p))
ok=data.get('run-cmd',{}).get('0',[])
if not ok:
    raise SystemExit('remote command failed: '+p)
PY
}

stop_subscriber() {
  ssh "${SSH_OPTS[@]}" "$FRONTEND" "set +e; if [ -f '$REL_BASE/subscriber.pid' ]; then pid=\$(cat '$REL_BASE/subscriber.pid'); kill \"\$pid\" >/dev/null 2>&1 || true; sleep 1; pkill -f '$TOPIC' >/dev/null 2>&1 || true; fi" >/dev/null 2>&1 || true
}
trap stop_subscriber EXIT

ssh "${SSH_OPTS[@]}" "$FRONTEND" "rm -rf '$REL_BASE'; mkdir -p '$REL_BASE/edge' '$REL_BASE/receiver'; mkdir -p ~/.config; cp '$COMMON_REL/mqtt_auth.conf' ~/.config/mosquitto_sub; chmod 600 ~/.config/mosquitto_sub"

ssh "${SSH_OPTS[@]}" "$FRONTEND" "set -eu; nohup sh -c 'mosquitto_sub --cafile \"\$HOME/$COMMON_REL/iot-lab-ca.pem\" -h mqtt4.iot-lab.info -p 8883 -q 1 -t \"$TOPIC\" | python3 \"\$HOME/$COMMON_REL/fit_rt01_stamp_stream.py\" > \"\$HOME/$REL_BASE/receiver/receiver_raw.tsv\"' > '$REL_BASE/receiver/subscriber.log' 2>&1 & echo \$! > '$REL_BASE/subscriber.pid'"
sleep 2
ssh "${SSH_OPTS[@]}" "$FRONTEND" "set -eu; pid=\$(cat '$REL_BASE/subscriber.pid'); kill -0 \"\$pid\"; test ! -s '$REL_BASE/receiver/subscriber.log' || { cat '$REL_BASE/receiver/subscriber.log'; exit 1; }"

run_node setup_edge "set -eu; mkdir -p \"\$HOME/.config\" \"\$HOME/$REL_BASE/edge\"; cp \"\$HOME/$COMMON_REL/mqtt_auth.conf\" \"\$HOME/.config/mosquitto_pub\"; chmod 600 \"\$HOME/.config/mosquitto_pub\"; python3 -m py_compile \"\$HOME/$COMMON_REL/fit_rt01_edge.py\""

CMD1="python3 \"\$HOME/$COMMON_REL/fit_rt01_edge.py\" --run-id '$RUN_ID' --architecture '$ARCH' --condition C2_outage_restart --start-seq 1 --end-seq 4000 --workdir \"\$HOME/$REL_BASE/edge\" --topic '$TOPIC' --probe-topic '$PROBE_TOPIC' --ca \"\$HOME/$COMMON_REL/iot-lab-ca.pem\" --batch-size 50 --leave-outage-active"
run_node segment_1 "$CMD1"

CMD2="python3 \"\$HOME/$COMMON_REL/fit_rt01_edge.py\" --run-id '$RUN_ID' --architecture '$ARCH' --condition C2_outage_restart --start-seq 4001 --end-seq 10000 --workdir \"\$HOME/$REL_BASE/edge\" --topic '$TOPIC' --probe-topic '$PROBE_TOPIC' --ca \"\$HOME/$COMMON_REL/iot-lab-ca.pem\" --batch-size 50"
run_node segment_2 "$CMD2"

sleep 5
stop_subscriber
trap - EXIT
ssh "${SSH_OPTS[@]}" "$FRONTEND" "rm -f ~/.config/mosquitto_sub; test -s '$REL_BASE/receiver/receiver_raw.tsv'"

scp "${SSH_OPTS[@]}" -r "$FRONTEND:$REL_BASE/edge" "$LOCAL_DIR/"
scp "${SSH_OPTS[@]}" "$FRONTEND:$REL_BASE/receiver/receiver_raw.tsv" "$LOCAL_DIR/receiver_raw.tsv"
scp "${SSH_OPTS[@]}" "$FRONTEND:$REL_BASE/receiver/subscriber.log" "$LOCAL_DIR/subscriber.log" || true

ANALYZE=(python scripts/analyze_fit_rt01.py --run-id "$RUN_ID" --architecture "$ARCH" --condition C2_outage_restart --generated "$LOCAL_DIR/edge/generated.jsonl" --receiver-raw "$LOCAL_DIR/receiver_raw.tsv" --events "$LOCAL_DIR/edge/edge_events.jsonl" --outdir "$LOCAL_DIR/analysis")
if [ "$ARCH" = "W1_offline_first" ]; then
  ANALYZE+=(--queue-db "$LOCAL_DIR/edge/queue.sqlite" --require-complete)
else
  ANALYZE+=(--require-baseline-loss)
fi
"${ANALYZE[@]}" | tee "$LOCAL_DIR/analysis_stdout.txt"

sha256sum "$LOCAL_DIR/edge/generated.jsonl" "$LOCAL_DIR/edge/edge_events.jsonl" "$LOCAL_DIR/receiver_raw.tsv" "$LOCAL_DIR/analysis/metrics.json" "$LOCAL_DIR/analysis/reconciliation.csv" > "$LOCAL_DIR/SHA256SUMS.txt"
echo "dry_cell_gate=PASS architecture=$ARCH run_id=$RUN_ID gate=$GATE"
