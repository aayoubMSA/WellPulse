#!/usr/bin/env bash
set -euo pipefail

LOCAL_ROOT="${WP_LOCAL_VERIFIED_ROOT:?WP_LOCAL_VERIFIED_ROOT is required}"
REMOTE_ROOT="${WP_RCLONE_REMOTE_ROOT:?WP_RCLONE_REMOTE_ROOT is required, e.g. gdrive:WellPulse/evidence}"
RUN_ID="${WP_RUN_ID:?WP_RUN_ID is required}"
EXPERIMENT_ID="${WP_EXPERIMENT_ID:?WP_EXPERIMENT_ID is required}"
PY="${WP_PYTHON:-python3}"
REMOTE_DIR="${REMOTE_ROOT%/}/$EXPERIMENT_ID/$RUN_ID"
MANIFEST="$LOCAL_ROOT/escrow/SOURCE_SHA256SUMS.txt"

bar(){
  local p="$1" m="$2" n
  n=$((p/5))
  printf '\r['
  printf '%*s' "$n" ''|tr ' ' '#'
  printf '%*s' "$((20-n))" ''|tr ' ' '-'
  printf '] %3d%%  %-48s' "$p" "$m"
}
fail(){ echo; echo "RCLONE_OFF_POWDER_GATE=FAIL:$1" >&2; exit 60; }

command -v rclone >/dev/null 2>&1 || fail RCLONE_MISSING
[[ -d "$LOCAL_ROOT" ]] || fail LOCAL_ROOT_MISSING
[[ -s "$MANIFEST" ]] || fail SOURCE_MANIFEST_MISSING

bar 10 'Checking rclone remote connectivity'; echo
rclone lsf "${REMOTE_ROOT%/}" >/dev/null 2>&1 || fail REMOTE_UNREACHABLE

bar 30 'Copying verified persistent evidence remotely'; echo
rclone copy "$LOCAL_ROOT" "$REMOTE_DIR" --create-empty-src-dirs || fail REMOTE_COPY

bar 65 'Read-back SHA-256 verification via rclone cat'; echo
"$PY" scripts/wp2_golden_rclone_verify.py --manifest "$MANIFEST" --remote-root "$REMOTE_DIR" || fail REMOTE_SHA256_VERIFY

bar 85 'Writing remote PASS marker'; echo
MARKER=$(printf 'run_id=%s\nexperiment_id=%s\nmanifest_sha256=%s\n' "$RUN_ID" "$EXPERIMENT_ID" "$(sha256sum "$MANIFEST"|awk '{print $1}')")
printf '%s' "$MARKER" | rclone rcat "$REMOTE_DIR/escrow/OFF_POWDER_RCLONE.PASS" || fail MARKER_WRITE
REMOTE_MARKER=$(rclone cat "$REMOTE_DIR/escrow/OFF_POWDER_RCLONE.PASS") || fail MARKER_READBACK
grep -q "run_id=$RUN_ID" <<<"$REMOTE_MARKER" || fail MARKER_RUN_ID

bar 100 'Verified rclone off-POWDER copy PASS'; echo
printf 'OFF_POWDER_REMOTE=%s\n' "$REMOTE_DIR"
printf 'RCLONE_OFF_POWDER_GATE=PASS\n'
