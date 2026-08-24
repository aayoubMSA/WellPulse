#!/usr/bin/env bash
set -uo pipefail

RUN_TAG="${1:-manual}"
OUTDIR="/tmp/wellpulse-g3-${RUN_TAG}"
TX_BIN="/usr/local/srsLTE/build/lib/examples/pdsch_enodeb"
RX_BIN="/usr/local/srsLTE/build/lib/examples/pdsch_ue"
IQ_FILE="$OUTDIR/pdsch.bin"

rm -rf "$OUTDIR"
mkdir -p "$OUTDIR"

{
  echo "RUN_TAG=$RUN_TAG"
  echo "UTC_START=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "HOSTNAME=$(hostname)"
  echo "USER=$(whoami)"
  echo "KERNEL=$(uname -a)"
  if [[ -f /etc/os-release ]]; then
    . /etc/os-release
    echo "OS_PRETTY_NAME=${PRETTY_NAME:-unknown}"
  fi
  echo "TX_BIN=$TX_BIN"
  echo "RX_BIN=$RX_BIN"
} > "$OUTDIR/remote-meta.txt"

TX_RC=127
RX_RC=127
IQ_BYTES=0
IQ_SHA256=""

if [[ -x "$TX_BIN" ]]; then
  "$TX_BIN" -o "$IQ_FILE" -n 5 -m 9 -v > "$OUTDIR/tx.log" 2>&1
  TX_RC=$?
else
  echo "Missing executable: $TX_BIN" > "$OUTDIR/tx.log"
fi

if [[ -f "$IQ_FILE" ]]; then
  IQ_BYTES="$(stat -c '%s' "$IQ_FILE" 2>/dev/null || echo 0)"
  IQ_SHA256="$(sha256sum "$IQ_FILE" 2>/dev/null | awk '{print $1}')"
fi

if [[ "$TX_RC" -eq 0 && "$IQ_BYTES" -gt 0 && -x "$RX_BIN" ]]; then
  "$RX_BIN" -i "$IQ_FILE" -n 5 -r 1234 -v -d > "$OUTDIR/rx.log" 2>&1
  RX_RC=$?
else
  if [[ ! -x "$RX_BIN" ]]; then
    echo "Missing executable: $RX_BIN" > "$OUTDIR/rx.log"
  else
    echo "Receiver not run because transmitter/output precondition failed." > "$OUTDIR/rx.log"
  fi
fi

UTC_END="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

{
  echo "TX_RC=$TX_RC"
  echo "RX_RC=$RX_RC"
  echo "IQ_BYTES=$IQ_BYTES"
  echo "IQ_SHA256=$IQ_SHA256"
  echo "UTC_END=$UTC_END"
  if [[ "$TX_RC" -eq 0 && "$RX_RC" -eq 0 && "$IQ_BYTES" -gt 0 ]]; then
    echo "PROCESS_GATE=PASS"
  else
    echo "PROCESS_GATE=FAIL"
  fi
} > "$OUTDIR/result.env"

# The binary waveform is not retained; reproducibility evidence keeps only size/hash.
rm -f "$IQ_FILE"

cat "$OUTDIR/result.env"
echo "RESULT_DIR=$OUTDIR"
