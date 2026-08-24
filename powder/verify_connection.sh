#!/usr/bin/env bash
set -euo pipefail

HOST="${1:-}"
OUT="${2:-evidence/powder/latest.md}"
USER_NAME="${POWDER_USERNAME:-}"

if [[ -z "$HOST" ]]; then
  echo "POWDER_HOST is empty" >&2
  exit 2
fi
if [[ -z "$USER_NAME" ]]; then
  echo "POWDER_USERNAME is empty" >&2
  exit 2
fi

mkdir -p "$(dirname "$OUT")"
TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT

SSH_OPTS=(
  -o BatchMode=yes
  -o ConnectTimeout=20
  -o ServerAliveInterval=10
  -o ServerAliveCountMax=2
  -o StrictHostKeyChecking=accept-new
  -o UserKnownHostsFile="$HOME/.ssh/known_hosts"
)

set +e
ssh "${SSH_OPTS[@]}" "${USER_NAME}@${HOST}" \
  'printf "REMOTE_HOST="; hostname; printf "REMOTE_USER="; whoami; printf "UTC="; date -u +%Y-%m-%dT%H:%M:%SZ; printf "KERNEL="; uname -srmo; if [ -r /etc/os-release ]; then . /etc/os-release; printf "OS=%s %s\n" "${NAME:-unknown}" "${VERSION_ID:-unknown}"; fi' \
  >"$TMP" 2>&1
RC=$?
set -e

{
  echo "# POWDER plumbing — latest"
  echo
  echo "- Checked UTC: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "- GitHub SHA: ${GITHUB_SHA:-unknown}"
  echo "- Target host: \`$HOST\`"
  echo "- POWDER user: \`$USER_NAME\`"
  if [[ "$RC" -eq 0 ]]; then
    echo "- Gate: **POWDER_PLUMBING_PASS**"
    echo "- Scope: SSH/read-only metadata only; not scientific evidence"
    echo
    echo '```text'
    cat "$TMP"
    echo '```'
  else
    echo "- Gate: **POWDER_PLUMBING_FAIL**"
    echo "- SSH exit code: \`$RC\`"
    echo "- Scope: infrastructure failure; no experiment action attempted"
    echo
    echo '```text'
    # Keep only a short diagnostic and avoid dumping excessive runner output.
    tail -n 20 "$TMP"
    echo '```'
  fi
} > "$OUT"

exit "$RC"
