#!/usr/bin/env bash
set -euo pipefail

REPO="${WP_REPO_ROOT:-$HOME/WellPulse}"
VENV="${WP_A3_VENV:-$HOME/.wp2-golden-venv}"
PYTHON_VERSION="${WP_A3_PYTHON_VERSION:-3.11.13}"
RCLONE_URL="${WP_A3_RCLONE_URL:-https://downloads.rclone.org/rclone-current-linux-amd64.zip}"

bar(){ local p="$1" m="$2" n; n=$((p/5)); printf '\r['; printf '%*s' "$n" ''|tr ' ' '#'; printf '%*s' "$((20-n))" ''|tr ' ' '-'; printf '] %3d%%  %-52s' "$p" "$m"; }
fail(){ echo; echo "A3_RUNTIME_BOOTSTRAP=FAIL:$1" >&2; exit 80; }

[[ -f "$REPO/pyproject.toml" ]] || fail REPO_NOT_PRESENT
command -v curl >/dev/null 2>&1 || fail CURL_MISSING

bar 10 'Installing uv in user space'; echo
export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
if ! command -v uv >/dev/null 2>&1; then
  curl -LsSf https://astral.sh/uv/install.sh | sh >/tmp/wp2-a3-uv-install.log 2>&1 || fail UV_INSTALL
  export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
fi
UV="$(command -v uv || true)"
[[ -x "$UV" ]] || fail UV_NOT_FOUND

bar 30 "Installing isolated Python $PYTHON_VERSION"; echo
"$UV" python install "$PYTHON_VERSION" >/tmp/wp2-a3-uv-python.log 2>&1 || fail PYTHON_INSTALL
rm -rf "$VENV"
"$UV" venv --python "$PYTHON_VERSION" --seed "$VENV" >/tmp/wp2-a3-uv-venv.log 2>&1 || fail VENV_CREATE
PY="$VENV/bin/python"
[[ -x "$PY" ]] || fail VENV_PYTHON_MISSING

bar 52 'Installing exact WellPulse MQTT dependency set'; echo
(
  cd "$REPO"
  "$UV" pip install --python "$PY" -e '.[mqtt]'
) >/tmp/wp2-a3-uv-pip.log 2>&1 || { tail -n 80 /tmp/wp2-a3-uv-pip.log >&2 || true; fail PACKAGE_INSTALL; }

bar 70 'Verifying Python and paho-mqtt contract'; echo
"$PY" - <<'PY' || fail PYTHON_CONTRACT
import sys, importlib.metadata
import wellpulse
assert sys.version_info >= (3,10), sys.version
v=importlib.metadata.version('paho-mqtt')
assert v == '2.1.0', v
print('PYTHON_RUNTIME='+sys.version.split()[0])
print('PAHO_MQTT='+v)
print('WELLPULSE_IMPORT=PASS')
PY

bar 82 'Installing rclone binary in user space if needed'; echo
if ! command -v rclone >/dev/null 2>&1 && [[ ! -x "$HOME/.local/bin/rclone" ]]; then
  rm -rf /tmp/wp2-a3-rclone /tmp/wp2-a3-rclone.zip
  mkdir -p /tmp/wp2-a3-rclone "$HOME/.local/bin"
  curl -fsSLo /tmp/wp2-a3-rclone.zip "$RCLONE_URL" || fail RCLONE_DOWNLOAD
  python3 -m zipfile -e /tmp/wp2-a3-rclone.zip /tmp/wp2-a3-rclone || fail RCLONE_EXTRACT
  RBIN="$(find /tmp/wp2-a3-rclone -type f -name rclone | head -1)"
  [[ -n "$RBIN" ]] || fail RCLONE_BINARY_NOT_FOUND
  install -m 755 "$RBIN" "$HOME/.local/bin/rclone" || fail RCLONE_INSTALL
fi
export PATH="$HOME/.local/bin:$PATH"
command -v rclone >/dev/null 2>&1 || fail RCLONE_NOT_FOUND

bar 94 'Recording exact runtime versions'; echo
{
  printf 'utc=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%S.%NZ)"
  printf 'host=%s\n' "$(hostname)"
  printf 'uv=%s\n' "$(uv --version 2>/dev/null || true)"
  printf 'python=%s\n' "$("$PY" --version 2>&1)"
  printf 'paho_mqtt=%s\n' "$("$PY" -c 'import importlib.metadata; print(importlib.metadata.version("paho-mqtt"))')"
  printf 'rclone=%s\n' "$(rclone version | head -1)"
  printf 'repo=%s\n' "$REPO"
  printf 'venv=%s\n' "$VENV"
} > "$HOME/wp2-a3-runtime-bootstrap.txt"

bar 100 'A3 isolated runtime PASS'; echo
printf 'WP_A3_PYTHON=%s\n' "$PY"
printf 'A3_RUNTIME_BOOTSTRAP=PASS\n'
