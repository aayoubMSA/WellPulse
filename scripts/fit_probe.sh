#!/bin/sh
set -eu

OUT="${1:-fit_probe_$(date -u +%Y%m%dT%H%M%SZ).log}"
NETEM_ERR="/tmp/wellpulse_netem_probe.err"
IPT_CHAIN="WELLPULSE_PROBE_$$"

cleanup_probe() {
  if command -v tc >/dev/null 2>&1; then
    tc qdisc del dev lo root >/dev/null 2>&1 || true
  fi
  if command -v iptables >/dev/null 2>&1; then
    iptables -F "$IPT_CHAIN" >/dev/null 2>&1 || true
    iptables -X "$IPT_CHAIN" >/dev/null 2>&1 || true
  fi
  rm -f "$NETEM_ERR"
}
trap cleanup_probe EXIT INT TERM

{
  echo "evidence_class=CAPABILITY_SMOKE_NOT_FINAL_EXPERIMENT"
  echo "probe_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "hostname=$(hostname)"

  echo "--- uname ---"
  uname -a || true

  echo "--- clock ---"
  date -u +%Y-%m-%dT%H:%M:%SZ || true
  cat /proc/uptime 2>/dev/null || true

  echo "--- runtime/tools ---"
  python3 --version 2>&1 || python --version 2>&1 || true
  command -v python3 || true
  command -v sqlite3 || true
  command -v git || true
  command -v openssl || true
  command -v mosquitto_pub || true
  command -v mosquitto_sub || true
  command -v iptables || true
  command -v nft || true

  echo "--- disk ---"
  df -h || true

  echo "--- persistent/shared path ---"
  ls -ld "$HOME/shared" "$HOME/shared/.iotlabsshcli" 2>/dev/null || true
  PERSIST_TEST="$HOME/shared/.wellpulse_write_test_$$"
  if : > "$PERSIST_TEST" 2>/dev/null; then
    echo "shared_write_test=PASS"
    rm -f "$PERSIST_TEST"
  else
    echo "shared_write_test=FAIL"
  fi

  echo "--- mounts of interest ---"
  mount | grep -Ei 'shared|nfs|sshfs' || true

  echo "--- network ---"
  ip addr 2>/dev/null || ifconfig 2>/dev/null || true

  echo "--- route ---"
  ip route 2>/dev/null || route -n 2>/dev/null || true

  echo "--- tc/netem capability ---"
  if command -v tc >/dev/null 2>&1; then
    tc -V 2>&1 || true
    tc qdisc show dev lo 2>&1 || true
    if tc qdisc add dev lo root netem delay 5ms 2>"$NETEM_ERR"; then
      echo "netem_loopback_add=PASS"
      tc qdisc show dev lo 2>&1 || true
      tc qdisc del dev lo root 2>&1 || true
    else
      echo "netem_loopback_add=FAIL"
      cat "$NETEM_ERR" 2>/dev/null || true
    fi
  else
    echo "tc_present=NO"
    echo "netem_loopback_add=NOT_TESTED"
  fi

  echo "--- iptables deterministic-outage capability ---"
  if command -v iptables >/dev/null 2>&1; then
    if iptables -N "$IPT_CHAIN" 2>/dev/null; then
      echo "iptables_chain_create=PASS"
      iptables -X "$IPT_CHAIN" 2>/dev/null || true
    else
      echo "iptables_chain_create=FAIL"
    fi
  else
    echo "iptables_present=NO"
    echo "iptables_chain_create=NOT_TESTED"
  fi

  echo "--- MQTT broker DNS ---"
  getent hosts mqtt4.iot-lab.info 2>/dev/null || nslookup mqtt4.iot-lab.info 2>/dev/null || true

  echo "--- TLS 8883 handshake probe ---"
  CA_FILE=""
  if [ -f "$HOME/shared/.iotlabsshcli/iot-lab-ca.pem" ]; then
    CA_FILE="$HOME/shared/.iotlabsshcli/iot-lab-ca.pem"
  elif [ -f /opt/iot-lab-ca.pem ]; then
    CA_FILE=/opt/iot-lab-ca.pem
  fi
  if command -v openssl >/dev/null 2>&1 && [ -n "$CA_FILE" ]; then
    echo "iotlab_ca_present=YES"
    echo "iotlab_ca_source=$(basename "$CA_FILE")"
    echo | openssl s_client \
      -connect mqtt4.iot-lab.info:8883 \
      -servername mqtt4.iot-lab.info \
      -CAfile "$CA_FILE" \
      2>&1 | grep -E 'Protocol|Cipher|Verify return code|Verification' || true
  elif [ -z "$CA_FILE" ]; then
    echo "iotlab_ca_present=NO"
  else
    echo "openssl_present=NO"
  fi

  echo "NOTE: authenticated MQTT publish/receive is a separate smoke step; no credentials are written to this log."
} > "$OUT" 2>&1

if command -v sha256sum >/dev/null 2>&1; then
  sha256sum "$OUT" > "$OUT.sha256"
fi
printf '%s\n' "$OUT"
