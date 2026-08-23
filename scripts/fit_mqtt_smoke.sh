#!/bin/sh
set -u

TOPIC="${1:?topic required}"
PAYLOAD="${2:?payload required}"
BASE="$HOME/shared/.iotlabsshcli"
CA_FILE="$BASE/iot-lab-ca.pem"
AUTH_FILE="$BASE/mqtt_auth.conf"
LOG_FILE="$BASE/mqtt_smoke.log"
MSG_FILE="/tmp/wellpulse_mqtt_msg_$$"
SUB_PID=""

cleanup() {
  if [ -n "$SUB_PID" ] && kill -0 "$SUB_PID" 2>/dev/null; then
    kill "$SUB_PID" >/dev/null 2>&1 || true
    wait "$SUB_PID" >/dev/null 2>&1 || true
  fi
  rm -f "$MSG_FILE" "$HOME/.config/mosquitto_pub" "$HOME/.config/mosquitto_sub"
}
trap cleanup EXIT INT TERM

mkdir -p "$HOME/.config"
cp "$AUTH_FILE" "$HOME/.config/mosquitto_pub"
cp "$AUTH_FILE" "$HOME/.config/mosquitto_sub"
chmod 600 "$HOME/.config/mosquitto_pub" "$HOME/.config/mosquitto_sub"

set +e
{
  echo "evidence_class=CAPABILITY_SMOKE_NOT_FINAL_EXPERIMENT"
  echo "mqtt_smoke_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "topic_scope=wellpulse_smoke"
  echo "ca_file_present=$([ -f "$CA_FILE" ] && echo YES || echo NO)"
  echo "mosquitto_pub=$(command -v mosquitto_pub 2>/dev/null || echo MISSING)"
  echo "mosquitto_sub=$(command -v mosquitto_sub 2>/dev/null || echo MISSING)"
  mosquitto_pub --help 2>&1 | head -n 2 || true

  if [ ! -f "$CA_FILE" ] || ! command -v mosquitto_pub >/dev/null 2>&1 || ! command -v mosquitto_sub >/dev/null 2>&1; then
    echo "mqtt_authenticated=PREREQUISITE_MISSING"
    exit 4
  fi

  : > "$MSG_FILE"
  mosquitto_sub --cafile "$CA_FILE" -h mqtt4.iot-lab.info -p 8883 -C 1 -t "$TOPIC" > "$MSG_FILE" 2>&1 &
  SUB_PID=$!
  sleep 2

  mosquitto_pub --cafile "$CA_FILE" -h mqtt4.iot-lab.info -p 8883 -t "$TOPIC" -m "$PAYLOAD"
  PUB_RC=$?
  echo "publish_rc=$PUB_RC"

  I=0
  while kill -0 "$SUB_PID" 2>/dev/null && [ "$I" -lt 12 ]; do
    sleep 1
    I=$((I + 1))
  done

  if kill -0 "$SUB_PID" 2>/dev/null; then
    echo "subscriber_timeout=YES"
    kill "$SUB_PID" >/dev/null 2>&1 || true
    wait "$SUB_PID" >/dev/null 2>&1 || true
  else
    wait "$SUB_PID"
    SUB_RC=$?
    echo "subscribe_rc=$SUB_RC"
  fi
  SUB_PID=""

  echo "--- subscriber output ---"
  cat "$MSG_FILE" 2>/dev/null || true

  if [ "$PUB_RC" -eq 0 ] && grep -Fx "$PAYLOAD" "$MSG_FILE" >/dev/null 2>&1; then
    echo "mqtt_authenticated=PASS"
    exit 0
  fi

  echo "mqtt_authenticated=FAIL"
  exit 5
} > "$LOG_FILE" 2>&1
RC=$?
set -e
cat "$LOG_FILE"
exit "$RC"
