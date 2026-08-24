#!/bin/sh
set -u

OUT="${1:-fit_probe_$(date -u +%Y%m%dT%H%M%SZ).log}"
EAS_COMMIT="75e90de8d6ba72b834f84b0f2b58414550140672"
FW="$HOME/shared/.iotlabsshcli/tutorial_a8_m3.elf"
UART="/dev/ttyA8_M3"
STATUS="PASS"
FAIL_CODE=""

mark_fail() {
  code="$1"
  STATUS="FAIL"
  if [ -z "$FAIL_CODE" ]; then FAIL_CODE="$code"; else FAIL_CODE="${FAIL_CODE},${code}"; fi
}

mkdir -p "$(dirname "$OUT")" 2>/dev/null || true
{
  echo "evidence_class=EAS_A8M3_PLUMBING_NON_SCORED"
  echo "eas_repo=aayoubMSA/empirical-architecture-synthesis"
  echo "eas_commit=$EAS_COMMIT"
  echo "probe_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "hostname=$(hostname)"
  echo "kernel=$(uname -a 2>/dev/null || true)"

  echo "--- required paths/tools ---"
  [ -x /usr/bin/iotlab_flash ] && echo "iotlab_flash_present=YES" || echo "iotlab_flash_present=NO"
  command -v stty || true
  command -v timeout || true
  ls -l "$UART" 2>&1 || true

  echo "--- firmware ---"
  if [ -s "$FW" ]; then
    echo "firmware_source=PRESTAGED_SHARED"
  else
    echo "firmware_source=NODE_DOWNLOAD_FALLBACK"
    mkdir -p "$(dirname "$FW")" 2>/dev/null || true
    if command -v wget >/dev/null 2>&1; then
      wget -q -O "$FW" https://iot-lab.github.io/assets/firmwares/tutorial_a8_m3.elf || true
    fi
  fi
  if [ -s "$FW" ]; then
    echo "firmware_fetch=PASS"
    sha256sum "$FW" 2>/dev/null || true
  else
    echo "firmware_fetch=FAIL"
    mark_fail FIRMWARE_FETCH
  fi

  echo "--- flash M3 subsystem ---"
  if [ -s "$FW" ] && [ -x /usr/bin/iotlab_flash ]; then
    if /usr/bin/iotlab_flash "$FW"; then echo "m3_flash=PASS"; else echo "m3_flash=FAIL"; mark_fail M3_FLASH; fi
  else
    echo "m3_flash=SKIPPED_OR_NO_TOOL"
    mark_fail NO_FLASH_TOOL
  fi
  sleep 2

  echo "--- UART configure ---"
  if [ -c "$UART" ]; then
    echo "uart_device=PASS"
    if command -v stty >/dev/null 2>&1 && stty -F "$UART" 500000 raw -echo 2>&1; then
      echo "uart_config=PASS"
    else
      echo "uart_config=FAIL"
      mark_fail UART_CONFIG
    fi
  else
    echo "uart_device=FAIL"
    mark_fail UART_DEVICE
  fi

  : > /tmp/eas_uart_startup.txt
  : > /tmp/eas_uart_r1.txt
  : > /tmp/eas_uart_r2.txt
  if [ -c "$UART" ] && command -v timeout >/dev/null 2>&1; then
    timeout 2 cat "$UART" > /tmp/eas_uart_startup.txt 2>/dev/null || true
    echo "--- deterministic request 1: h ---"
    (timeout 3 cat "$UART" > /tmp/eas_uart_r1.txt 2>/dev/null || true) & R1PID=$!
    sleep 0.3; printf 'h\n' > "$UART" 2>/dev/null || true; wait "$R1PID" || true
    cat /tmp/eas_uart_r1.txt || true
    echo "--- deterministic request 2: h ---"
    (timeout 3 cat "$UART" > /tmp/eas_uart_r2.txt 2>/dev/null || true) & R2PID=$!
    sleep 0.3; printf 'h\n' > "$UART" 2>/dev/null || true; wait "$R2PID" || true
    cat /tmp/eas_uart_r2.txt || true
    if [ -s /tmp/eas_uart_r1.txt ] && [ -s /tmp/eas_uart_r2.txt ]; then echo "uart_response_nonempty=PASS"; else echo "uart_response_nonempty=FAIL"; mark_fail EMPTY_UART_RESPONSE; fi
    if grep -Eqi 'Type command|print this help|cmd>' /tmp/eas_uart_r1.txt 2>/dev/null && grep -Eqi 'Type command|print this help|cmd>' /tmp/eas_uart_r2.txt 2>/dev/null; then
      echo "m3_a8_request_response=PASS"
    else
      echo "m3_a8_request_response=REVIEW"
      mark_fail REQUEST_RESPONSE
    fi
  else
    echo "uart_capture=SKIPPED"
    mark_fail UART_CAPTURE
  fi

  echo "--- hashes ---"
  sha256sum /tmp/eas_uart_startup.txt /tmp/eas_uart_r1.txt /tmp/eas_uart_r2.txt 2>/dev/null || true
  if [ "$STATUS" = "PASS" ]; then echo "plumbing_status=PASS"; else echo "plumbing_status=FAIL"; echo "plumbing_fail_code=$FAIL_CODE"; fi
  rm -f /tmp/eas_uart_startup.txt /tmp/eas_uart_r1.txt /tmp/eas_uart_r2.txt
} > "$OUT" 2>&1
sha256sum "$OUT" > "$OUT.sha256" 2>/dev/null || true
printf '%s\n' "$OUT"
exit 0
