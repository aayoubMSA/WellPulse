#!/usr/bin/env bash
set -euo pipefail

REMOTE_ROOT="${WP_RCLONE_REMOTE_ROOT:?WP_RCLONE_REMOTE_ROOT is required}"
PROBE_NAME="wp2-golden-preflight-$(date -u +%Y%m%dT%H%M%SZ)-$$.txt"
LOCAL_TMP="$(mktemp)"
trap 'rm -f "$LOCAL_TMP"' EXIT

bar(){ local p="$1" m="$2" n=$((p/5)); printf '\r['; printf '%*s' "$n" ''|tr ' ' '#'; printf '%*s' "$((20-n))" ''|tr ' ' '-'; printf '] %3d%%  %-48s' "$p" "$m"; }
fail(){ echo; echo "RCLONE_PREFLIGHT=FAIL:$1" >&2; exit 61; }

command -v rclone >/dev/null 2>&1 || fail RCLONE_MISSING

bar 10 'Checking authenticated remote listing'; echo
rclone lsf "${REMOTE_ROOT%/}" >/dev/null 2>&1 || fail REMOTE_LIST

bar 30 'Creating non-sensitive probe payload'; echo
printf 'wellpulse_wp2_golden_preflight\nutc=%s\nnonce=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$RANDOM-$RANDOM-$$" > "$LOCAL_TMP"
LOCAL_SHA="$(sha256sum "$LOCAL_TMP" | awk '{print $1}')"

bar 50 'Writing probe to external remote'; echo
rclone copyto "$LOCAL_TMP" "${REMOTE_ROOT%/}/$PROBE_NAME" || fail REMOTE_WRITE

bar 70 'Read-back SHA-256 verification'; echo
REMOTE_SHA="$(rclone cat "${REMOTE_ROOT%/}/$PROBE_NAME" | sha256sum | awk '{print $1}')" || fail REMOTE_READ
[[ "$LOCAL_SHA" == "$REMOTE_SHA" ]] || fail SHA_MISMATCH

bar 88 'Removing transient preflight probe'; echo
rclone deletefile "${REMOTE_ROOT%/}/$PROBE_NAME" || fail REMOTE_DELETE
if rclone lsf "${REMOTE_ROOT%/}" --include "$PROBE_NAME" | grep -q .; then fail DELETE_VERIFY; fi

bar 100 'Real off-POWDER destination preflight PASS'; echo
printf 'REMOTE_ROOT=%s\n' "$REMOTE_ROOT"
printf 'PROBE_SHA256=%s\n' "$LOCAL_SHA"
printf 'SECRET_MATERIAL_RECORDED=false\n'
printf 'RCLONE_PREFLIGHT=PASS\n'
