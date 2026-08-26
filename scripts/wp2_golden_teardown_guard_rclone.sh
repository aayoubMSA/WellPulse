#!/usr/bin/env bash
set -euo pipefail

PERSIST_DIR="${WP_PERSIST_EVIDENCE_DIR:?WP_PERSIST_EVIDENCE_DIR is required}"
REMOTE_DIR="${WP_RCLONE_EVIDENCE_DIR:?WP_RCLONE_EVIDENCE_DIR is required}"
RUN_ID="${WP_RUN_ID:?WP_RUN_ID is required}"
PY="${WP_PYTHON:-python3}"
MANIFEST="$PERSIST_DIR/escrow/SOURCE_SHA256SUMS.txt"

fail(){ echo "TEARDOWN_GUARD=FAIL_RCLONE:$1"; exit 71; }
command -v rclone >/dev/null 2>&1 || fail RCLONE_MISSING
[[ -s "$MANIFEST" ]] || fail SOURCE_MANIFEST_MISSING
[[ -s "$PERSIST_DIR/escrow/EVIDENCE_ESCROW_GATE.PASS" ]] || fail PERSISTENT_PASS_MISSING
grep -q "run_id=$RUN_ID" "$PERSIST_DIR/escrow/EVIDENCE_ESCROW_GATE.PASS" || fail PERSISTENT_RUN_ID
(
  cd "$PERSIST_DIR"
  sha256sum -c escrow/SOURCE_SHA256SUMS.txt >/dev/null
) || fail PERSISTENT_HASH

"$PY" scripts/wp2_golden_rclone_verify.py --manifest "$MANIFEST" --remote-root "$REMOTE_DIR" >/tmp/wp2-rclone-guard-verify.txt || fail REMOTE_HASH
MARKER=$(rclone cat "$REMOTE_DIR/escrow/OFF_POWDER_RCLONE.PASS" 2>/dev/null) || fail REMOTE_MARKER_MISSING
grep -q "run_id=$RUN_ID" <<<"$MARKER" || fail REMOTE_MARKER_RUN_ID
LOCAL_MANIFEST_HASH=$(sha256sum "$MANIFEST"|awk '{print $1}')
grep -q "manifest_sha256=$LOCAL_MANIFEST_HASH" <<<"$MARKER" || fail REMOTE_MANIFEST_HASH

echo '=== WP2 Golden rclone teardown guard ==='
printf 'RUN_ID=%s\n' "$RUN_ID"
printf 'MANIFEST_SHA256=%s\n' "$LOCAL_MANIFEST_HASH"
printf 'EVIDENCE_ESCROW_GATE=PASS\n'
printf 'TEARDOWN_AUTHORIZED=YES\n'
