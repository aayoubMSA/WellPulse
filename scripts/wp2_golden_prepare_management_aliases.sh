#!/usr/bin/env bash
set -euo pipefail

# Run on the UE/application node before Golden G0.
# The controller must supply the exact management endpoints parsed from the
# authoritative Portal manifest. This helper binds the frozen logical aliases
# to those exact endpoints and proves SSH reachability before science.

CORE_MANAGEMENT_HOST="${WP_CORE_MANAGEMENT_HOST:?WP_CORE_MANAGEMENT_HOST is required}"
UE_MANAGEMENT_HOST="${WP_UE_MANAGEMENT_HOST:?WP_UE_MANAGEMENT_HOST is required}"
CORE_ALIAS="${WP_CORE_ALIAS:-enb1}"
UE_ALIAS="${WP_UE_ALIAS:-rue1}"
REMOTE_USER="${WP_REMOTE_USER:-aayoub}"

resolve_ipv4(){
  local host="$1" ip
  ip="$(getent ahostsv4 "$host" | awk 'NR==1{print $1}')"
  [[ "$ip" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]] || {
    echo "WP2_GOLDEN_MANAGEMENT_ALIAS_GATE=FAIL:RESOLVE_$host" >&2
    return 1
  }
  printf '%s\n' "$ip"
}

CORE_IP="$(resolve_ipv4 "$CORE_MANAGEMENT_HOST")"
UE_IP="$(resolve_ipv4 "$UE_MANAGEMENT_HOST")"

sudo sed -i -E "/[[:space:]]${CORE_ALIAS}([[:space:]]|$)/d; /[[:space:]]${UE_ALIAS}([[:space:]]|$)/d" /etc/hosts
printf '%s %s\n%s %s\n' "$CORE_IP" "$CORE_ALIAS" "$UE_IP" "$UE_ALIAS" | sudo tee -a /etc/hosts >/dev/null

[[ "$(getent ahostsv4 "$CORE_ALIAS" | awk 'NR==1{print $1}')" == "$CORE_IP" ]]
[[ "$(getent ahostsv4 "$UE_ALIAS" | awk 'NR==1{print $1}')" == "$UE_IP" ]]

SSH_OPTS=(-o BatchMode=yes -o ConnectTimeout=10 -o StrictHostKeyChecking=accept-new)
ssh "${SSH_OPTS[@]}" "$REMOTE_USER@$CORE_ALIAS" 'true'
ssh "${SSH_OPTS[@]}" "$REMOTE_USER@$UE_ALIAS" 'true'

printf 'WP2_GOLDEN_CORE_MANAGEMENT_HOST=%s\n' "$CORE_MANAGEMENT_HOST"
printf 'WP2_GOLDEN_UE_MANAGEMENT_HOST=%s\n' "$UE_MANAGEMENT_HOST"
printf 'WP2_GOLDEN_CORE_ALIAS=%s\n' "$CORE_ALIAS"
printf 'WP2_GOLDEN_UE_ALIAS=%s\n' "$UE_ALIAS"
printf 'WP2_GOLDEN_MANAGEMENT_ALIAS_GATE=PASS\n'
