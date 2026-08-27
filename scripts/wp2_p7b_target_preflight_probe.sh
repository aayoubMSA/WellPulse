#!/usr/bin/env bash
set -euo pipefail

ROLE="${1:-unknown}"
REPO_ROOT="${2:-$PWD}"
APP_PY="${WP2_APP_PYTHON:-$HOME/wellpulse-runtime-p311/bin/python}"

emit() { printf '%s=%s\n' "$1" "$2"; }
have() { command -v "$1" >/dev/null 2>&1; }
version_line() { "$@" 2>&1 | head -n 1 | tr '\n' ' '; }

emit PREFLIGHT_SCHEMA wp2-p7b-target-preflight-v1
emit ROLE "$ROLE"
emit HOSTNAME "$(hostname)"
emit UTC "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
emit KERNEL "$(uname -srmo 2>/dev/null || uname -a)"
if [[ -r /etc/os-release ]]; then
  . /etc/os-release
  emit OS_ID "${ID:-unknown}"
  emit OS_VERSION "${VERSION_ID:-unknown}"
fi

for tool in bash python python3 java javac mosquitto mosquitto_pub mosquitto_sub openssl tmcc tar sha256sum find ssh scp; do
  if have "$tool"; then emit "TOOL_${tool^^}" "$(command -v "$tool")"; else emit "TOOL_${tool^^}" MISSING; fi
done

if have bash; then emit BASH_VERSION "${BASH_VERSION:-unknown}"; fi
if have python; then emit SYSTEM_PYTHON_VERSION "$(version_line python --version)"; else emit SYSTEM_PYTHON_VERSION MISSING; fi
if have python3; then emit SYSTEM_PYTHON3_VERSION "$(version_line python3 --version)"; else emit SYSTEM_PYTHON3_VERSION MISSING; fi
if [[ -x "$APP_PY" ]]; then
  emit APP_PYTHON "$APP_PY"
  emit APP_PYTHON_VERSION "$(version_line "$APP_PY" --version)"
else
  emit APP_PYTHON MISSING
  emit APP_PYTHON_VERSION MISSING
fi
if have java; then emit JAVA_VERSION "$(version_line java -version)"; fi
if have javac; then emit JAVAC_VERSION "$(version_line javac -version)"; fi
if have openssl; then emit OPENSSL_VERSION "$(version_line openssl version)"; fi

for tool in find tar sha256sum; do
  if have "$tool"; then emit "PRESERVE_${tool^^}" PASS; else emit "PRESERVE_${tool^^}" FAIL; fi
done
if [[ -d /proj/WellPulse ]]; then emit PROJECT_ESCROW_DIR PRESENT; else emit PROJECT_ESCROW_DIR MISSING; fi
if [[ -w /proj/WellPulse ]]; then emit PROJECT_ESCROW_WRITABLE YES; else emit PROJECT_ESCROW_WRITABLE NO; fi

if have tmcc; then
  set +e
  TMCC_RAW="$(tmcc attenuator 2>&1)"
  TMCC_RC=$?
  set -e
  emit TMCC_ATTENUATOR_RC "$TMCC_RC"
  printf '%s\n' '--- TMCC_ATTENUATOR_RAW_BEGIN ---'
  printf '%s\n' "$TMCC_RAW"
  printf '%s\n' '--- TMCC_ATTENUATOR_RAW_END ---'
else
  emit TMCC_ATTENUATOR_RC MISSING
fi

# Target-path lint is static and read-only.
PATH_FAIL=0
for f in \
  experiments/WP-PWD01/p7b-qualification-contract.json \
  experiments/WP-PWD01/p7b-executable-contract-v2.json; do
  [[ -r "$REPO_ROOT/$f" ]] || continue
  if grep -nE '\$HOME|\$\{|(^|[[:space:]"'\''=])~/' "$REPO_ROOT/$f"; then PATH_FAIL=1; fi
done
emit UNRESOLVED_PATH_TOKEN_GATE "$([[ "$PATH_FAIL" -eq 0 ]] && echo PASS || echo FAIL)"

# Syntax-check application Python sources only with the pinned application interpreter.
APP_SYNTAX=PASS
if [[ -x "$APP_PY" ]]; then
  for f in \
    scripts/wp2_p7b_c_node_r1.py \
    scripts/wp2_p7b_c_node_r2.py \
    scripts/wp2_p7b_generator.py \
    scripts/wp2_p7b_python_gateway.py \
    scripts/wp_pwd01_h_receiver.py; do
    [[ -r "$REPO_ROOT/$f" ]] || { emit "APP_SOURCE_${f//\//_}" MISSING; APP_SYNTAX=FAIL; continue; }
    if "$APP_PY" -c 'import sys; p=sys.argv[1]; compile(open(p,"rb").read(),p,"exec")' "$REPO_ROOT/$f" >/dev/null 2>&1; then
      emit "APP_SOURCE_${f//\//_}" PASS
    else
      emit "APP_SOURCE_${f//\//_}" FAIL
      APP_SYNTAX=FAIL
    fi
  done
else
  APP_SYNTAX=FAIL
fi
emit APP_SOURCE_COMPATIBILITY_GATE "$APP_SYNTAX"

# Preservation deliberately has no Python dependency.
PRESERVE=PASS
for tool in find tar sha256sum; do have "$tool" || PRESERVE=FAIL; done
[[ -d /proj/WellPulse ]] || PRESERVE=FAIL
emit SHELL_ONLY_PRESERVATION_GATE "$PRESERVE"

# This probe never changes RF or starts application processes.
emit RF_MUTATION NO
emit CELL_EXECUTION NO
emit TEARDOWN NO
emit SCORED NO
