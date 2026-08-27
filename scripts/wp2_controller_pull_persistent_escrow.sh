#!/usr/bin/env bash
set -euo pipefail

HOST="${WP_PERSIST_HOST:?WP_PERSIST_HOST is required}"
USER="${WP_REMOTE_USER:-aayoub}"
PORT="${WP_SSH_PORT:-22}"
REMOTE_DIR="${WP_PERSIST_REMOTE_DIR:?WP_PERSIST_REMOTE_DIR is required}"
LOCAL_DIR="${WP_CONTROLLER_LOCAL_DIR:?WP_CONTROLLER_LOCAL_DIR is required}"
BUNDLE_OUT="${WP_CONTROLLER_BUNDLE_OUT:-${LOCAL_DIR%/}.tar}"
KNOWN_HOSTS="${WP_KNOWN_HOSTS_FILE:-$HOME/.ssh/known_hosts}"

fail(){ echo "CONTROLLER_PULL_GATE=FAIL:$1" >&2; exit 51; }

rm -rf "$LOCAL_DIR"
mkdir -p "$LOCAL_DIR" "$(dirname "$KNOWN_HOSTS")"

scp -r -P "$PORT" \
  -o BatchMode=yes \
  -o ConnectTimeout=15 \
  -o StrictHostKeyChecking=accept-new \
  -o UserKnownHostsFile="$KNOWN_HOSTS" \
  "$USER@$HOST:$REMOTE_DIR/." "$LOCAL_DIR/" || fail SCP_PULL

MANIFEST="$LOCAL_DIR/escrow/SOURCE_SHA256SUMS.txt"
[[ -s "$MANIFEST" ]] || fail SOURCE_MANIFEST_MISSING
[[ -s "$LOCAL_DIR/escrow/PERSISTENT_ESCROW_GATE.PASS" ]] || fail PERSISTENT_GATE_MARKER_MISSING

(
  cd "$LOCAL_DIR"
  sha256sum -c escrow/SOURCE_SHA256SUMS.txt >/dev/null
) || fail PULLED_CONTENT_HASH_MISMATCH

rm -f "$BUNDLE_OUT"
tar --sort=name --mtime='UTC 1970-01-01' --owner=0 --group=0 --numeric-owner \
  -C "$LOCAL_DIR" -cf "$BUNDLE_OUT" . || fail TAR_CREATE
[[ -s "$BUNDLE_OUT" ]] || fail TAR_EMPTY
BUNDLE_SHA="$(sha256sum "$BUNDLE_OUT" | awk '{print $1}')"

printf 'CONTROLLER_PULL_GATE=PASS\n'
printf 'PERSIST_REMOTE_DIR=%s\n' "$REMOTE_DIR"
printf 'CONTROLLER_LOCAL_DIR=%s\n' "$LOCAL_DIR"
printf 'CONTROLLER_BUNDLE=%s\n' "$BUNDLE_OUT"
printf 'CONTROLLER_BUNDLE_SHA256=%s\n' "$BUNDLE_SHA"
