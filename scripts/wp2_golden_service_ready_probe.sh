#!/usr/bin/env bash
set -euo pipefail

HOST="${WP_BROKER_HOST:-172.16.0.1}"
PORT="${WP_BROKER_PORT:-8883}"
CA_FILE="${WP_CA_FILE:?WP_CA_FILE is required}"
BOUND_S="${WP_SERVICE_BOUND_S:-120}"
START_EPOCH="${WP_RESTORE_START_EPOCH:-$(date +%s)}"
OUT="${WP_SERVICE_PROBE_OUT:-/tmp/wp2-golden-service-ready.txt}"

mkdir -p "$(dirname "$OUT")"
exec > >(tee -a "$OUT") 2>&1

utc(){ date -u +%Y-%m-%dT%H:%M:%S.%NZ; }
bar(){
  local p="$1" msg="$2" n=$((p/5))
  printf '\r['
  printf '%*s' "$n" '' | tr ' ' '#'
  printf '%*s' "$((20-n))" '' | tr ' ' '-'
  printf '] %3d%%  %-48s' "$p" "$msg"
}
remaining(){
  local now elapsed
  now=$(date +%s); elapsed=$((now-START_EPOCH)); echo $((BOUND_S-elapsed))
}
within_bound(){ [[ $(remaining) -gt 0 ]]; }

printf '=== WP2 Golden architecture-blind service-ready probe ===\n'
printf 'PROBE_START_UTC=%s\n' "$(utc)"
printf 'RESTORE_START_EPOCH=%s\nBOUND_S=%s\n' "$START_EPOCH" "$BOUND_S"

bar 10 'Waiting for tun_srsue'
echo
while within_bound; do
  if ip -4 addr show dev tun_srsue 2>/dev/null | grep -q 'inet '; then break; fi
  sleep 1
done
ip -4 addr show dev tun_srsue >/dev/null 2>&1 || { echo 'SERVICE_READY=FAIL_NO_TUNNEL'; exit 20; }
printf 'TUNNEL_READY_UTC=%s\n' "$(utc)"

bar 25 'Verifying broker route via tun_srsue'
echo
ROUTE=$(ip route get "$HOST" 2>&1 || true)
echo "$ROUTE"
grep -q 'dev tun_srsue' <<<"$ROUTE" || { echo 'SERVICE_READY=FAIL_ROUTE'; exit 21; }
printf 'ROUTE_READY_UTC=%s\n' "$(utc)"

bar 45 'Requiring 5/5 ICMP over LTE tunnel'
echo
PING_OUT=$(ping -I tun_srsue -c 5 -W 2 "$HOST" 2>&1 || true)
echo "$PING_OUT"
grep -Eq '5 packets transmitted, 5 received|5 packets transmitted, 5 packets received' <<<"$PING_OUT" || { echo 'SERVICE_READY=FAIL_ICMP'; exit 22; }
grep -q '0% packet loss' <<<"$PING_OUT" || { echo 'SERVICE_READY=FAIL_ICMP_LOSS'; exit 23; }
printf 'ICMP_READY_UTC=%s\n' "$(utc)"

bar 70 'Verifying TLS broker identity and CA'
echo
LEFT=$(remaining)
[[ "$LEFT" -gt 0 ]] || { echo 'SERVICE_READY=FAIL_TIMEOUT_BEFORE_TLS'; exit 24; }
TLS_OUT=$(timeout "${LEFT}s" openssl s_client -connect "${HOST}:${PORT}" -CAfile "$CA_FILE" -verify_return_error -verify_ip "$HOST" </dev/null 2>&1 || true)
echo "$TLS_OUT"
grep -q 'Verification: OK' <<<"$TLS_OUT" || grep -q 'Verify return code: 0 (ok)' <<<"$TLS_OUT" || { echo 'SERVICE_READY=FAIL_TLS_VERIFY'; exit 25; }

NOW=$(date +%s)
ELAPSED=$((NOW-START_EPOCH))
[[ "$ELAPSED" -le "$BOUND_S" ]] || { echo "SERVICE_READY=FAIL_BOUND_EXCEEDED ELAPSED_S=$ELAPSED"; exit 26; }

bar 100 'Architecture-blind service ready PASS'
echo
printf 'T_SERVICE_READY=%s\n' "$(utc)"
printf 'SERVICE_RESTORE_ELAPSED_S=%s\n' "$ELAPSED"
printf 'WP2_GOLDEN_SERVICE_READY=PASS\n'
