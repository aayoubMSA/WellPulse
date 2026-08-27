#!/usr/bin/env bash
set -euo pipefail

# WellPulse WP2 Portal API client bootstrap.
# This is the only accepted future-integration bootstrap contract for portal-cli.
# It intentionally fails closed if the authoritative revision cannot be fetched
# or if the checked-out commit differs from the frozen revision.

PORTAL_API_REPO="https://gitlab.flux.utah.edu/emulab/portal-api.git"
PORTAL_API_REVISION="01be03b2f60c067815a7654437320dd981ca3617"
PORTAL_API_CAPTURE_ARCHIVE_SHA256="3e9f0073b2df6840801baa38333f1f04debd02a2eaa57997939b6f7ee678d4c8"
PORTAL_API_CAPTURE_ARCHIVE_BYTES="1003520"
DEST="${1:-/tmp/portal-api}"

rm -rf "$DEST"
mkdir -p "$DEST"
git -C "$DEST" init -q
git -C "$DEST" remote add origin "$PORTAL_API_REPO"
git -C "$DEST" fetch -q --depth 1 origin "$PORTAL_API_REVISION"
git -C "$DEST" checkout -q --detach FETCH_HEAD

ACTUAL="$(git -C "$DEST" rev-parse HEAD)"
[[ "$ACTUAL" == "$PORTAL_API_REVISION" ]] || {
  echo "PORTAL_API_PIN_GATE=FAIL:REVISION_MISMATCH:$ACTUAL" >&2
  exit 41
}

python3 -m pip install --quiet "$DEST[cli]"
command -v portal-cli >/dev/null 2>&1 || {
  echo "PORTAL_API_PIN_GATE=FAIL:PORTAL_CLI_NOT_INSTALLED" >&2
  exit 42
}

printf 'PORTAL_API_PIN_GATE=PASS\n'
printf 'PORTAL_API_REPO=%s\n' "$PORTAL_API_REPO"
printf 'PORTAL_API_REVISION=%s\n' "$PORTAL_API_REVISION"
printf 'PORTAL_API_CAPTURE_ARCHIVE_SHA256=%s\n' "$PORTAL_API_CAPTURE_ARCHIVE_SHA256"
printf 'PORTAL_API_CAPTURE_ARCHIVE_BYTES=%s\n' "$PORTAL_API_CAPTURE_ARCHIVE_BYTES"
