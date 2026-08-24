#!/bin/sh
set -eu

OUT="${1:-fit_probe_$(date -u +%Y%m%dT%H%M%SZ).log}"
EAS_COMMIT="75e90de8d6ba72b834f84b0f2b58414550140672"
FW="$HOME/shared/.iotlabsshcli/tutorial_a8_m3.elf"
UART="/dev/ttyA8_M3"

{
  echo "evidence_class=EAS_A8M3_PLUMBING_NON_SCORED"
  echo "eas_repo=aayoubMSA/empirical-architecture-synthesis"
  echo "eas_commit=$EAS_COMMIT"
  echo "probe_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "hostname=$(hostname)"
  echo "kernel=$(uname -a)"
  echo "uptime=$(cat /proc/uptime 2>/dev/null || true)"

  echo "--- required paths/tools ---"
  command -v flash_a8_m3 || true
  command -v wget || true
  command -v stty || true
  command -v timeout || true
  ls -l "$UART" 2>&1 || true

  echo "--- fetch official tutorial firmware ---"
  mkdir -p "$(dirname "$FW")"
  rm -f "$FW"
  if command -v wget >/dev/null 2>&1; then
    wget -q -O "$FW" https://raw.githubusercontent.com/wiki/iot-lab/iot-lab/firmwares/tutorial_a8_m3.elf || \
    wget -q -O "$FW" https://iot-lab.github.io/assets/firmwares/tutorial_a8_m3.elf || true
  fi
  if [ ! -s "$FW" ]; then
    echo "firmware_fetch=FAIL"
    exit 21
  fi
  echo "firmware_fetch=PASS"
  sha256sum "$FW" 2>/dev/null || true

  echo "--- flash M3 subsystem ---"
  if flash_a8_m3 "$FW"; then
    echo "m3_flash=PASS"
  else
    echo "m3_flash=FAIL"
    exit 22
  fi
  sleep 2

  echo "--- UART configure ---"
  if [ ! -c "$UART" ]; then
    echo "uart_device=FAIL"
    exit 23
  fi
  echo "uart_device=PASS"
  stty -F "$UART" 500000 raw -echo 2>&1 || true

  echo "--- capture startup ---"
  timeout 3 cat "$UART" > /tmp/eas_uart_startup.txt 2>/dev/null || true
  cat /tmp/eas_uart_startup.txt || true

  echo "--- deterministic request 1: h ---"
  (timeout 3 cat "$UART" > /tmp/eas_uart_r1.txt 2>/dev/null || true) &
  R1PID=$!
  sleep 0.3
  printf 'h\n' > "$UART"
  wait "$R1PID" || true
  cat /tmp/eas_uart_r1.txt || true

  echo "--- deterministic request 2: h ---"
  (timeout 3 cat "$UART" > /tmp/eas_uart_r2.txt 2>/dev/null || true) &
  R2PID=$!
  sleep 0.3
  printf 'h\n' > "$UART"
  wait "$R2PID" || true
  cat /tmp/eas_uart_r2.txt || true

  if grep -qi 'Type command\|print this help\|cmd' /tmp/eas_uart_r1.txt && grep -qi 'Type command\|print this help\|cmd' /tmp/eas_uart_r2.txt; then
    echo "m3_a8_request_response=PASS"
  else
    echo "m3_a8_request_response=REVIEW"
  fi

  echo "--- hashes ---"
  sha256sum /tmp/eas_uart_startup.txt /tmp/eas_uart_r1.txt /tmp/eas_uart_r2.txt 2>/dev/null || true

  rm -f /tmp/eas_uart_startup.txt /tmp/eas_uart_r1.txt /tmp/eas_uart_r2.txt
} > "$OUT" 2>&1

sha256sum "$OUT" > "$OUT.sha256" 2>/dev/null || true
printf '%s\n' "$OUT"
