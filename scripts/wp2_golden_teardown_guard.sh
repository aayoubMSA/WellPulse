#!/usr/bin/env bash
set -euo pipefail

PERSIST_DIR="${WP_PERSIST_EVIDENCE_DIR:?WP_PERSIST_EVIDENCE_DIR is required}"
OFF_DIR="${WP_OFF_POWDER_EVIDENCE_DIR:?WP_OFF_POWDER_EVIDENCE_DIR is required}"
RUN_ID="${WP_RUN_ID:?WP_RUN_ID is required}"

check_copy(){
  local root="$1" label="$2"
  [[ -d "$root" ]] || { echo "TEARDOWN_GUARD=FAIL_${label}_MISSING"; return 1; }
  [[ -s "$root/escrow/SOURCE_SHA256SUMS.txt" ]] || { echo "TEARDOWN_GUARD=FAIL_${label}_SOURCE_MANIFEST"; return 1; }
  [[ -s "$root/escrow/EVIDENCE_ESCROW_GATE.PASS" ]] || { echo "TEARDOWN_GUARD=FAIL_${label}_PASS_MARKER"; return 1; }
  grep -q "run_id=$RUN_ID" "$root/escrow/EVIDENCE_ESCROW_GATE.PASS" || { echo "TEARDOWN_GUARD=FAIL_${label}_RUN_ID"; return 1; }
  (
    cd "$root"
    sha256sum -c escrow/SOURCE_SHA256SUMS.txt >/dev/null
  ) || { echo "TEARDOWN_GUARD=FAIL_${label}_HASH_VERIFY"; return 1; }
}

echo '=== WP2 Golden teardown guard ==='
check_copy "$PERSIST_DIR" PERSISTENT
check_copy "$OFF_DIR" OFF_POWDER

PERSIST_HASH=$(sha256sum "$PERSIST_DIR/escrow/SOURCE_SHA256SUMS.txt" | awk '{print $1}')
OFF_HASH=$(sha256sum "$OFF_DIR/escrow/SOURCE_SHA256SUMS.txt" | awk '{print $1}')
[[ "$PERSIST_HASH" == "$OFF_HASH" ]] || { echo 'TEARDOWN_GUARD=FAIL_MANIFEST_MISMATCH'; exit 51; }

printf 'RUN_ID=%s\n' "$RUN_ID"
printf 'MANIFEST_SHA256=%s\n' "$PERSIST_HASH"
printf 'EVIDENCE_ESCROW_GATE=PASS\n'
printf 'TEARDOWN_AUTHORIZED=YES\n'
