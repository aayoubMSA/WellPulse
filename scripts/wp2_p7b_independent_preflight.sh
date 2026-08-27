#!/usr/bin/env bash
set -euo pipefail

# Orthogonal target preflight for an already-existing POWDER reservation.
# This script deliberately does NOT use:
# - powder/wp2_p7b_r3_execute.sh
# - scripts/wp2_p7b_target_node_preflight.sh
# - scripts/wp2_portal_client_bootstrap.sh
# - project readiness/manifest parsers
# It performs no reservation creation/termination, no RF mutation, and no B1/W1/B2 action.

: "${CORE_HOST:?CORE_HOST required}"
: "${CORE_USER:?CORE_USER required}"
: "${CORE_PORT:?CORE_PORT required}"
: "${UE_HOST:?UE_HOST required}"
: "${UE_USER:?UE_USER required}"
: "${UE_PORT:?UE_PORT required}"
: "${POWDER_SSH_PRIVATE_KEY:?POWDER_SSH_PRIVATE_KEY required}"
: "${POWDER_SSH_KEY_PASSPHRASE:=}"

EXPECTED_PINNED_PYTHON="${EXPECTED_PINNED_PYTHON:-3.11.13}"
EXPECTED_JAVA_MAJOR="${EXPECTED_JAVA_MAJOR:-11}"
REMOTE_REPO="${REMOTE_REPO:-$HOME/WellPulse}"
REMOTE_PINNED_PYTHON="${REMOTE_PINNED_PYTHON:-$HOME/.wp2-golden-venv/bin/python}"
TMP="${TMPDIR:-/tmp}/wp2-p7b-independent-preflight"
rm -rf "$TMP"
mkdir -p "$TMP"
umask 077

fail(){ echo "WP2_P7B_INDEPENDENT_PREFLIGHT=BLOCKED:$1" >&2; exit "${2:-20}"; }
pass(){ echo "WP2_P7B_INDEPENDENT_PREFLIGHT=PASS"; }

# Keep SSH material and agent lifetime in this single process. No cross-step state.
printf '%s\n' "$POWDER_SSH_PRIVATE_KEY" | tr -d '\r' > "$TMP/private.key"
chmod 600 "$TMP/private.key"
cat > "$TMP/askpass" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' "$POWDER_SSH_KEY_PASSPHRASE"
EOF
chmod 700 "$TMP/askpass"
export SSH_ASKPASS="$TMP/askpass" SSH_ASKPASS_REQUIRE=force DISPLAY=:0
setsid -w ssh-keygen -y -f "$TMP/private.key" > "$TMP/public.key" </dev/null || fail SSH_KEY_DERIVATION 4
eval "$(ssh-agent -s)" >/dev/null
trap 'ssh-agent -k >/dev/null 2>&1 || true; rm -rf "$TMP"' EXIT
setsid -w ssh-add "$TMP/private.key" </dev/null >/dev/null || fail SSH_KEY_LOAD 4
: > "$TMP/known_hosts"; chmod 600 "$TMP/known_hosts"
SSH_OPTS=(-A -o BatchMode=yes -o IdentitiesOnly=no -o ConnectTimeout=12 -o ServerAliveInterval=5 -o ServerAliveCountMax=2 -o StrictHostKeyChecking=accept-new -o UserKnownHostsFile="$TMP/known_hosts")

probe_node(){
  local role=$1 user=$2 host=$3 port=$4
  ssh "${SSH_OPTS[@]}" -p "$port" "$user@$host" \
    "ROLE='$role' EXPECTED_PINNED_PYTHON='$EXPECTED_PINNED_PYTHON' EXPECTED_JAVA_MAJOR='$EXPECTED_JAVA_MAJOR' REMOTE_REPO='$REMOTE_REPO' REMOTE_PINNED_PYTHON='$REMOTE_PINNED_PYTHON' bash -s" <<'REMOTE'
set -euo pipefail
rfail(){ echo "NODE_PREFLIGHT=BLOCKED:${ROLE}:$1" >&2; exit "${2:-30}"; }

echo "NODE_ROLE=$ROLE"
echo "NODE_HOST=$(hostname)"
echo "KERNEL=$(uname -srmo 2>/dev/null || uname -a)"
echo "BASH_VERSION=$BASH_VERSION"
echo "SYSTEM_PYTHON=$(python3 --version 2>&1 || true)"

test -x "$REMOTE_PINNED_PYTHON" || rfail PINNED_PYTHON_MISSING
PINNED_VERSION="$($REMOTE_PINNED_PYTHON -c 'import sys; print(".".join(map(str,sys.version_info[:3])))')"
echo "PINNED_PYTHON=$PINNED_VERSION"
test "$PINNED_VERSION" = "$EXPECTED_PINNED_PYTHON" || rfail "PINNED_PYTHON_VERSION_${PINNED_VERSION}"

for cmd in bash openssl tar sha256sum find sort xargs rsync ss pgrep curl; do
  command -v "$cmd" >/dev/null 2>&1 || rfail "COMMAND_MISSING_${cmd}"
done

test -d "$REMOTE_REPO" || rfail REMOTE_REPO_MISSING
test -d /proj/WellPulse || rfail PROJ_WELLPULSE_MISSING
test -w /proj/WellPulse || rfail PROJ_WELLPULSE_NOT_WRITABLE

# Prove the exact application interpreter can import the runtime MQTT library.
PAHO_VERSION="$($REMOTE_PINNED_PYTHON - <<'PY'
import importlib.metadata
print(importlib.metadata.version('paho-mqtt'))
PY
)" || rfail PAHO_IMPORT
printf 'PAHO_MQTT=%s\n' "$PAHO_VERSION"

# Syntax-check representative project code with the exact target interpreter.
for rel in \
  scripts/wp2_p7b_c_node_r1.py \
  scripts/wp2_p7b_python_gateway.py \
  scripts/wp2_p7b_generator.py \
  scripts/wp_pwd01_h_receiver.py \
  src/wellpulse/p7b.py; do
  test -s "$REMOTE_REPO/$rel" || rfail "SOURCE_MISSING_${rel}"
  "$REMOTE_PINNED_PYTHON" - "$REMOTE_REPO/$rel" <<'PY' || exit 41
import pathlib,sys
p=pathlib.Path(sys.argv[1])
compile(p.read_text(encoding='utf-8'), str(p), 'exec')
PY
  test $? -eq 0 || rfail "TARGET_PYTHON_SYNTAX_${rel}" 41
done

if [ "$ROLE" = ue ]; then
  command -v java >/dev/null 2>&1 || rfail JAVA_MISSING
  JAVA_LINE="$(java -version 2>&1 | head -1)"
  echo "JAVA_VERSION_LINE=$JAVA_LINE"
  JAVA_MAJOR="$(printf '%s\n' "$JAVA_LINE" | sed -n 's/.*version "\([0-9][0-9]*\).*/\1/p')"
  test "$JAVA_MAJOR" = "$EXPECTED_JAVA_MAJOR" || rfail "JAVA_MAJOR_${JAVA_MAJOR:-UNKNOWN}"
else
  command -v mosquitto >/dev/null 2>&1 || rfail MOSQUITTO_DAEMON_MISSING
fi

# Directly observe route/interface state without project parsers.
ip route 2>/dev/null | sed -n '1,40p' || true
ip link 2>/dev/null | sed -n '1,80p' || true

# Preservation primitives must work independently of Python.
PTEST="/proj/WellPulse/.p7b-preflight-${ROLE}-$$"
mkdir -p "$PTEST/src" "$PTEST/dst"
printf 'preflight-%s\n' "$ROLE" > "$PTEST/src/payload.txt"
( cd "$PTEST/src" && sha256sum payload.txt > SHA256SUMS )
tar -C "$PTEST/src" -cf "$PTEST/archive.tar" .
mkdir -p "$PTEST/extract"
tar -C "$PTEST/extract" -xf "$PTEST/archive.tar"
( cd "$PTEST/extract" && sha256sum -c SHA256SUMS >/dev/null ) || rfail SHELL_PRESERVATION_ROUNDTRIP
rm -rf "$PTEST"

echo "NODE_PREFLIGHT=PASS:$ROLE"
REMOTE
}

probe_node core "$CORE_USER" "$CORE_HOST" "$CORE_PORT" | tee "$TMP/core.log"
probe_node ue "$UE_USER" "$UE_HOST" "$UE_PORT" | tee "$TMP/ue.log"

grep -q '^NODE_PREFLIGHT=PASS:core$' "$TMP/core.log" || fail CORE_PREFLIGHT
cat "$TMP/ue.log" >/dev/null
grep -q '^NODE_PREFLIGHT=PASS:ue$' "$TMP/ue.log" || fail UE_PREFLIGHT

# Explicit static self-audit: this probe must remain orthogonal and read-only.
SELF="$0"
for banned in \
  'wp2_p7b_r3_execute.sh' \
  'wp2_p7b_target_node_preflight.sh' \
  'wp2_portal_client_bootstrap.sh' \
  'portal-cli experiment create' \
  'portal-cli experiment terminate' \
  'tmcc attenuator' \
  'P7B-B1-S3' \
  'P7B-W1-S3' \
  'P7B-B2-S3'; do
  if grep -F "$banned" "$SELF" | grep -v "'$banned'" >/dev/null 2>&1; then
    fail "SELF_AUDIT_BANNED_REFERENCE_${banned// /_}" 50
  fi
done

pass
