#!/usr/bin/env bash
set -euo pipefail

REPO="${WP_REPO_ROOT:-$HOME/WellPulse}"
VENV="${WP_A3_VENV:-$HOME/.wp2-golden-venv}"
PYTHON_VERSION="${WP_A3_PYTHON_VERSION:-3.11.13}"
UV_VERSION="${WP_A3_UV_VERSION:-0.12.1}"
UV_URL="${WP_A3_UV_URL:-https://github.com/astral-sh/uv/releases/download/${UV_VERSION}/uv-x86_64-unknown-linux-gnu.tar.gz}"
UV_SHA256="${WP_A3_UV_SHA256:-90b2f223fb69d19db49e117da601f64978593417988530aa733d456141b4bcbb}"
RCLONE_VERSION="${WP_A3_RCLONE_VERSION:-1.75.0}"
RCLONE_URL="${WP_A3_RCLONE_URL:-https://downloads.rclone.org/v${RCLONE_VERSION}/rclone-v${RCLONE_VERSION}-linux-amd64.zip}"
RCLONE_SHA256="${WP_A3_RCLONE_SHA256:-aa2804e08f48250e71009c727124b6341cd0288465804a9a09d14663cabafbaa}"

bar(){ local p="$1" m="$2" n; n=$((p/5)); printf '\r['; printf '%*s' "$n" ''|tr ' ' '#'; printf '%*s' "$((20-n))" ''|tr ' ' '-'; printf '] %3d%%  %-52s' "$p" "$m"; }
fail(){ echo; echo "A3_RUNTIME_BOOTSTRAP=FAIL:$1" >&2; exit 80; }

[[ -f "$REPO/pyproject.toml" ]] || fail REPO_NOT_PRESENT
command -v curl >/dev/null 2>&1 || fail CURL_MISSING
command -v sha256sum >/dev/null 2>&1 || fail SHA256SUM_MISSING
command -v tar >/dev/null 2>&1 || fail TAR_MISSING

bar 10 "Installing verified uv v$UV_VERSION"; echo
mkdir -p "$HOME/.local/bin"
export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
LOCAL_UV="$HOME/.local/bin/uv"
NEED_UV=1
if [[ -x "$LOCAL_UV" ]]; then
  INSTALLED_UV="$($LOCAL_UV --version 2>/dev/null | awk '{print $2; exit}')"
  [[ "$INSTALLED_UV" == "$UV_VERSION" ]] && NEED_UV=0
fi
if [[ "$NEED_UV" -eq 1 ]]; then
  rm -rf /tmp/wp2-a3-uv /tmp/wp2-a3-uv.tar.gz
  mkdir -p /tmp/wp2-a3-uv
  curl -fsSLo /tmp/wp2-a3-uv.tar.gz "$UV_URL" || fail UV_DOWNLOAD
  printf '%s  %s\n' "$UV_SHA256" /tmp/wp2-a3-uv.tar.gz | sha256sum -c - >/tmp/wp2-a3-uv-sha256.txt 2>&1 || {
    cat /tmp/wp2-a3-uv-sha256.txt >&2 || true
    fail UV_SHA256
  }
  tar -xzf /tmp/wp2-a3-uv.tar.gz -C /tmp/wp2-a3-uv || fail UV_EXTRACT
  UBIN="$(find /tmp/wp2-a3-uv -type f -name uv | head -1)"
  [[ -n "$UBIN" ]] || fail UV_BINARY_NOT_FOUND
  install -m 755 "$UBIN" "$LOCAL_UV" || fail UV_INSTALL
fi
[[ -x "$LOCAL_UV" ]] || fail UV_NOT_FOUND
INSTALLED_UV="$($LOCAL_UV --version 2>/dev/null | awk '{print $2; exit}')"
[[ "$INSTALLED_UV" == "$UV_VERSION" ]] || fail "UV_VERSION_$INSTALLED_UV"
printf 'UV_RUNTIME=%s\n' "$INSTALLED_UV"
UV="$LOCAL_UV"

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

bar 82 "Installing verified rclone v$RCLONE_VERSION"; echo
mkdir -p "$HOME/.local/bin"
export PATH="$HOME/.local/bin:$PATH"
LOCAL_RCLONE="$HOME/.local/bin/rclone"
NEED_RCLONE=1
if [[ -x "$LOCAL_RCLONE" ]]; then
  INSTALLED_RCLONE="$($LOCAL_RCLONE version 2>/dev/null | awk 'NR==1{gsub(/^rclone v/,""); print; exit}')"
  [[ "$INSTALLED_RCLONE" == "$RCLONE_VERSION" ]] && NEED_RCLONE=0
fi
if [[ "$NEED_RCLONE" -eq 1 ]]; then
  rm -rf /tmp/wp2-a3-rclone /tmp/wp2-a3-rclone.zip
  mkdir -p /tmp/wp2-a3-rclone
  curl -fsSLo /tmp/wp2-a3-rclone.zip "$RCLONE_URL" || fail RCLONE_DOWNLOAD
  printf '%s  %s\n' "$RCLONE_SHA256" /tmp/wp2-a3-rclone.zip | sha256sum -c - >/tmp/wp2-a3-rclone-sha256.txt 2>&1 || {
    cat /tmp/wp2-a3-rclone-sha256.txt >&2 || true
    fail RCLONE_SHA256
  }
  python3 -m zipfile -e /tmp/wp2-a3-rclone.zip /tmp/wp2-a3-rclone || fail RCLONE_EXTRACT
  RBIN="$(find /tmp/wp2-a3-rclone -type f -name rclone | head -1)"
  [[ -n "$RBIN" ]] || fail RCLONE_BINARY_NOT_FOUND
  install -m 755 "$RBIN" "$LOCAL_RCLONE" || fail RCLONE_INSTALL
fi
[[ -x "$LOCAL_RCLONE" ]] || fail RCLONE_NOT_FOUND
INSTALLED_RCLONE="$($LOCAL_RCLONE version 2>/dev/null | awk 'NR==1{gsub(/^rclone v/,""); print; exit}')"
[[ "$INSTALLED_RCLONE" == "$RCLONE_VERSION" ]] || fail "RCLONE_VERSION_$INSTALLED_RCLONE"
printf 'RCLONE_RUNTIME=%s\n' "$INSTALLED_RCLONE"

bar 94 'Recording exact runtime versions'; echo
{
  printf 'utc=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%S.%NZ)"
  printf 'host=%s\n' "$(hostname)"
  printf 'uv=%s\n' "$($UV --version 2>/dev/null || true)"
  printf 'uv_archive_sha256=%s\n' "$UV_SHA256"
  printf 'python=%s\n' "$("$PY" --version 2>&1)"
  printf 'paho_mqtt=%s\n' "$("$PY" -c 'import importlib.metadata; print(importlib.metadata.version("paho-mqtt"))')"
  printf 'rclone=%s\n' "$($LOCAL_RCLONE version | head -1)"
  printf 'rclone_archive_sha256=%s\n' "$RCLONE_SHA256"
  printf 'repo=%s\n' "$REPO"
  printf 'venv=%s\n' "$VENV"
} > "$HOME/wp2-a3-runtime-bootstrap.txt"

bar 100 'A3 isolated runtime PASS'; echo
printf 'WP_A3_PYTHON=%s\n' "$PY"
printf 'WP_A3_UV=%s\n' "$UV"
printf 'WP_A3_RCLONE=%s\n' "$LOCAL_RCLONE"
printf 'A3_RUNTIME_BOOTSTRAP=PASS\n'
