#!/usr/bin/env bash
set -euo pipefail

LOCAL_ROOT="${WP_LOCAL_VERIFIED_ROOT:?WP_LOCAL_VERIFIED_ROOT is required}"
REMOTE_ROOT="${WP_RCLONE_REMOTE_ROOT:?WP_RCLONE_REMOTE_ROOT is required}"
RUN_ID="${WP_RUN_ID:?WP_RUN_ID is required}"
EXPERIMENT_ID="${WP_EXPERIMENT_ID:?WP_EXPERIMENT_ID is required}"
PY="${WP_PYTHON:-python3}"
MAX_ATTEMPTS="${WP_RCLONE_MAX_ATTEMPTS:-5}"
RETRY_SLEEP="${WP_RCLONE_RETRY_SLEEP_S:-15}"
REMOTE_DIR="${REMOTE_ROOT%/}/$EXPERIMENT_ID/$RUN_ID"
MANIFEST="$LOCAL_ROOT/escrow/SOURCE_SHA256SUMS.txt"

bar(){ local p="$1" m="$2" n; n=$((p/5)); printf '\r['; printf '%*s' "$n" ''|tr ' ' '#'; printf '%*s' "$((20-n))" ''|tr ' ' '-'; printf '] %3d%%  %-48s' "$p" "$m"; }
fail(){ echo; echo "RCLONE_OFF_POWDER_GATE=FAIL:$1" >&2; echo 'STOP_DO_NOT_TERMINATE=1'; exit 60; }

command -v rclone >/dev/null 2>&1 || fail RCLONE_MISSING
[[ -d "$LOCAL_ROOT" ]] || fail LOCAL_ROOT_MISSING
[[ -s "$MANIFEST" ]] || fail SOURCE_MANIFEST_MISSING

attempt=1
while (( attempt <= MAX_ATTEMPTS )); do
  echo "=== Drive escrow attempt $attempt/$MAX_ATTEMPTS ==="
  bar 10 'Checking authenticated Drive access'; echo
  if ! rclone lsf "${REMOTE_ROOT%/}" >/dev/null 2>&1; then
    echo "ATTEMPT_${attempt}=REMOTE_UNREACHABLE"
  else
    bar 35 'Copying verified evidence to Drive'; echo
    if rclone copy "$LOCAL_ROOT" "$REMOTE_DIR" --create-empty-src-dirs; then
      bar 65 'Read-back SHA-256 verification'; echo
      if "$PY" scripts/wp2_golden_rclone_verify.py --manifest "$MANIFEST" --remote-root "$REMOTE_DIR"; then
        bar 85 'Writing verified remote PASS marker'; echo
        MARKER=$(printf 'run_id=%s\nexperiment_id=%s\nmanifest_sha256=%s\n' "$RUN_ID" "$EXPERIMENT_ID" "$(sha256sum "$MANIFEST"|awk '{print $1}')")
        if printf '%s' "$MARKER" | rclone rcat "$REMOTE_DIR/escrow/OFF_POWDER_RCLONE.PASS" && \
           rclone cat "$REMOTE_DIR/escrow/OFF_POWDER_RCLONE.PASS" | grep -q "run_id=$RUN_ID"; then
          bar 100 'Verified Drive escrow PASS'; echo
          printf 'OFF_POWDER_REMOTE=%s\n' "$REMOTE_DIR"
          printf 'RCLONE_ESCROW_ATTEMPTS=%s\n' "$attempt"
          printf 'RCLONE_OFF_POWDER_GATE=PASS\n'
          exit 0
        fi
        echo "ATTEMPT_${attempt}=MARKER_VERIFY_FAILED"
      else
        echo "ATTEMPT_${attempt}=REMOTE_SHA256_VERIFY_FAILED"
      fi
    else
      echo "ATTEMPT_${attempt}=REMOTE_COPY_FAILED"
    fi
  fi
  if (( attempt < MAX_ATTEMPTS )); then
    echo "RETRYING_IN_S=${RETRY_SLEEP}"
    sleep "$RETRY_SLEEP"
  fi
  attempt=$((attempt+1))
done

fail "DRIVE_ESCROW_NOT_VERIFIED_AFTER_${MAX_ATTEMPTS}_ATTEMPTS"
