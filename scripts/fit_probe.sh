#!/bin/sh
set -eu

OUT="${1:-fit_probe_$(date -u +%Y%m%dT%H%M%SZ).log}"
{
  echo "probe_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "hostname=$(hostname)"
  echo "--- uname ---"
  uname -a || true
  echo "--- python ---"
  python3 --version 2>&1 || python --version 2>&1 || true
  echo "--- disk ---"
  df -h || true
  echo "--- mounts of interest ---"
  mount | grep -Ei 'A8|shared|nfs|sshfs' || true
  echo "--- network ---"
  ip addr 2>/dev/null || ifconfig 2>/dev/null || true
  echo "--- route ---"
  ip route 2>/dev/null || route -n 2>/dev/null || true
  echo "--- tc/netem capability ---"
  command -v tc || true
  tc -V 2>&1 || true
  tc qdisc show 2>&1 || true
  echo "--- MQTT broker DNS ---"
  getent hosts mqtt4.iot-lab.info 2>/dev/null || nslookup mqtt4.iot-lab.info 2>/dev/null || true
  echo "--- TCP 8883 probe ---"
  (command -v nc >/dev/null 2>&1 && nc -vz -w 5 mqtt4.iot-lab.info 8883) 2>&1 || true
  echo "NOTE: authenticated MQTT/TLS publish/receive is a separate step; do not place credentials in this log."
} > "$OUT" 2>&1

if command -v sha256sum >/dev/null 2>&1; then
  sha256sum "$OUT" > "$OUT.sha256"
fi
printf '%s\n' "$OUT"
