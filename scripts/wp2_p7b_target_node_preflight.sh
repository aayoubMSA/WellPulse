#!/usr/bin/env bash
set -euo pipefail

ROLE=${1:?usage: wp2_p7b_target_node_preflight.sh ue|core}
case "$ROLE" in ue|core) ;; *) echo "TARGET_NODE_PREFLIGHT=BLOCKED:BAD_ROLE"; exit 2;; esac

REPO=${WP_REPO_ROOT:-$HOME/WellPulse}
PY=${WP_PYTHON:-$HOME/.wp2-golden-venv/bin/python}
fail(){ echo "WP2_P7B_TARGET_NODE_PREFLIGHT=BLOCKED:$1" >&2; exit "${2:-20}"; }

[[ -d "$REPO" ]] || fail REPO_MISSING
[[ -x "$PY" ]] || fail PINNED_PYTHON_MISSING

os_id="unknown"; os_version="unknown"
if [[ -r /etc/os-release ]]; then
  # shellcheck disable=SC1091
  . /etc/os-release
  os_id=${ID:-unknown}; os_version=${VERSION_ID:-unknown}
fi
[[ "$os_id" == ubuntu && "$os_version" == 18.04 ]] || fail "TARGET_IMAGE_OS_${os_id}_${os_version}"

actual_system_py="$(python3 -c 'import sys; print(".".join(map(str,sys.version_info[:3])))' 2>/dev/null || true)"
[[ "$actual_system_py" == 3.6.9 ]] || fail "EFCC_SYSTEM_PYTHON_CHANGED_$actual_system_py"
actual_py="$($PY -c 'import sys; print(".".join(map(str,sys.version_info[:3])))')"
[[ "$actual_py" == 3.11.13 ]] || fail "PINNED_PYTHON_VERSION_$actual_py"
actual_paho="$($PY -c 'import importlib.metadata as m; print(m.version("paho-mqtt"))' 2>/dev/null || true)"
[[ "$actual_paho" == 2.1.0 ]] || fail "PAHO_MQTT_VERSION_$actual_paho"

printf 'ROLE=%s\nOS=%s:%s\nSYSTEM_PYTHON=%s\nPINNED_PYTHON=%s\nPAHO_MQTT=%s\n' "$ROLE" "$os_id" "$os_version" "$actual_system_py" "$actual_py" "$actual_paho"

for cmd in bash openssl tar sha256sum find sort xargs rsync tmux ss pgrep curl mosquitto_pub; do
  command -v "$cmd" >/dev/null || fail "COMMAND_MISSING_$cmd"
done

bash_version="$(bash -c 'printf "%s" "$BASH_VERSION"')"
[[ "$bash_version" == 4.4.19* ]] || fail "EFCC_BASH_CHANGED_$bash_version"

if [[ "$ROLE" == ue ]]; then
  command -v java >/dev/null || fail JAVA_MISSING_UE
  java_major="$(java -version 2>&1 | sed -n '1s/.*version "\([0-9][0-9]*\).*/\1/p')"
  [[ "$java_major" == 11 ]] || fail "JAVA_MAJOR_$java_major"
  [[ -n "${WP_B2_JAR_PATH:-}" ]] || fail B2_JAR_PATH_NOT_SUPPLIED
  [[ -s "$WP_B2_JAR_PATH" ]] || fail B2_JAR_MISSING
  jar_sha="$(sha256sum "$WP_B2_JAR_PATH" | awk '{print $1}')"
  [[ "$jar_sha" == 59914287adac506a28d5e8172eed262a22605f3df4d426b9d92f41dae2448185 ]] || fail "B2_JAR_SHA_$jar_sha"
else
  command -v mosquitto >/dev/null || fail MOSQUITTO_DAEMON_MISSING_CORE
  mosq_version="$(mosquitto -h 2>&1 | sed -n '1s/.*version \([^ ]*\).*/\1/p')"
  [[ "$mosq_version" == 1.4.15 ]] || fail "EFCC_MOSQUITTO_CHANGED_$mosq_version"
fi

test -d /proj/WellPulse || fail PROJ_WELLPULSE_MISSING
test -w /proj/WellPulse || fail PROJ_WELLPULSE_NOT_WRITABLE

# Syntax-compile exact runtime sources with the execution interpreter; never system Python.
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

# Runtime gate must not depend on pkg_resources, which EFCC observed absent.
for rel in scripts/wp2_p7b_c_node_r2.py scripts/wp2_p7b_validate_readiness_v2.py scripts/reconstruct_wp2_p7b_v2.py src/wellpulse/p7b_contract_v2.py src/wellpulse/p7b_runtime_compat.py; do
  if grep -Eq '(^|[^A-Za-z0-9_])pkg_resources([^A-Za-z0-9_]|$)' "$REPO/$rel"; then
    fail "PKG_RESOURCES_RUNTIME_DEPENDENCY_$rel"
  fi
done

# Preservation is shell/coreutils-only and must not require system Python or jq.
helper="$REPO/scripts/wp2_p7b_preservation_helpers_v2.sh"
test -s "$helper" || fail PRESERVATION_HELPER_V2_MISSING
bash -n "$helper" || fail PRESERVATION_HELPER_V2_SYNTAX
exec_helper="$(grep -Ev '^[[:space:]]*(#|$)' "$helper" || true)"
if grep -Eq '(^|[;&|()[:space:]])python3([;&|()[:space:]]|$)' <<<"$exec_helper"; then fail PRESERVATION_HELPER_DEPENDS_ON_SYSTEM_PYTHON; fi
if grep -Eq '(^|[;&|()[:space:]])jq([;&|()[:space:]]|$)' <<<"$exec_helper"; then fail PRESERVATION_HELPER_DEPENDS_ON_REMOTE_JQ; fi

# No live tmcc readback probe: observed interface has no machine-parseable physical readback.
printf 'ATTENUATOR_PREFLIGHT=FIXTURE_ONLY_NO_LIVE_TMCC_READBACK\n'
printf 'PROJECT_CODE_SYSTEM_PYTHON=PROHIBITED\n'
printf 'PYTHON_METADATA_INTERFACE=importlib.metadata\n'
printf 'REMOTE_JQ_DEPENDENCY=PROHIBITED\n'
printf 'PRESERVATION_REMOTE_PYTHON=PROHIBITED\n'
printf 'EFCC_RUNTIME_BINDING=PASS\n'
printf 'WP2_P7B_TARGET_NODE_PREFLIGHT=PASS\n'
