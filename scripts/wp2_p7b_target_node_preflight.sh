#!/usr/bin/env bash
set -euo pipefail

ROLE=${1:?usage: wp2_p7b_target_node_preflight.sh ue|core}
case "$ROLE" in ue|core) ;; *) echo "TARGET_NODE_PREFLIGHT=BLOCKED:BAD_ROLE"; exit 2;; esac

REPO=${WP_REPO_ROOT:-$HOME/WellPulse}
PY=${WP_PYTHON:-$HOME/.wp2-golden-venv/bin/python}
fail(){ echo "WP2_P7B_TARGET_NODE_PREFLIGHT=BLOCKED:$1" >&2; exit "${2:-20}"; }

[[ -d "$REPO" ]] || fail REPO_MISSING
[[ -x "$PY" ]] || fail PINNED_PYTHON_MISSING
actual_py="$($PY -c 'import sys; print(".".join(map(str,sys.version_info[:3])))')"
[[ "$actual_py" == 3.11.13 ]] || fail "PINNED_PYTHON_VERSION_$actual_py"

# System Python is observed for provenance only. It is never used for repo code.
system_py="$(python3 --version 2>&1 || true)"
printf 'ROLE=%s\nSYSTEM_PYTHON=%s\nPINNED_PYTHON=%s\n' "$ROLE" "$system_py" "$actual_py"

for cmd in bash openssl tar sha256sum find sort xargs rsync tmux ss pgrep curl mosquitto_pub; do
  command -v "$cmd" >/dev/null || fail "COMMAND_MISSING_$cmd"
done
if [[ "$ROLE" == ue ]]; then
  command -v java >/dev/null || fail JAVA_MISSING_UE
  java_major="$(java -version 2>&1 | sed -n '1s/.*version "\([0-9][0-9]*\).*/\1/p')"
  [[ "$java_major" == 11 ]] || fail "JAVA_MAJOR_$java_major"
else
  command -v mosquitto >/dev/null || fail MOSQUITTO_DAEMON_MISSING_CORE
fi

test -d /proj/WellPulse || fail PROJ_WELLPULSE_MISSING
test -w /proj/WellPulse || fail PROJ_WELLPULSE_NOT_WRITABLE

# Syntax-compile with the exact execution interpreter without creating pyc files.
SOURCES=(
  scripts/wp2_p7b_c_node.py
  scripts/wp2_p7b_c_node_r1.py
  scripts/wp2_p7b_c_node_r2.py
  scripts/wp2_p7b_python_gateway.py
  scripts/wp2_p7b_generator.py
  scripts/wp_pwd01_h_receiver.py
  scripts/wp2_p7b_b2_manifest.py
  scripts/wp2_p7b_validate_readiness_v2.py
  scripts/reconstruct_wp2_p7b_v2.py
  src/wellpulse/p7b.py
  src/wellpulse/p7b_contract_v2.py
  src/wellpulse/p7b_runtime_compat.py
)
for rel in "${SOURCES[@]}"; do
  test -s "$REPO/$rel" || fail "SOURCE_MISSING_$rel"
  "$PY" - "$REPO/$rel" <<'PY' || fail "TARGET_PYTHON_SYNTAX_$rel"
import pathlib,sys
p=pathlib.Path(sys.argv[1])
compile(p.read_text(encoding='utf-8'), str(p), 'exec')
PY
done

# Preservation is intentionally shell-only on POWDER nodes.
helper="$REPO/scripts/wp2_p7b_preservation_helpers_v2.sh"
test -s "$helper" || fail PRESERVATION_HELPER_V2_MISSING
bash -n "$helper" || fail PRESERVATION_HELPER_V2_SYNTAX
if grep -q 'python3' "$helper"; then fail PRESERVATION_HELPER_DEPENDS_ON_SYSTEM_PYTHON; fi

# The observed tmcc interface is not called here: no documented readback exists.
printf 'ATTENUATOR_PREFLIGHT=FIXTURE_ONLY_NO_LIVE_TMCC_READBACK\n'
printf 'PROJECT_CODE_SYSTEM_PYTHON=PROHIBITED\n'
printf 'PRESERVATION_REMOTE_PYTHON=PROHIBITED\n'
printf 'WP2_P7B_TARGET_NODE_PREFLIGHT=PASS\n'
