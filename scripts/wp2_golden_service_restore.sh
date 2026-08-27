#!/usr/bin/env bash
set -euo pipefail

CORE_HOST="${WP_CORE_HOST:?WP_CORE_HOST is required}"
UE_HOST="${WP_UE_HOST:?WP_UE_HOST is required}"
REMOTE_USER="${WP_REMOTE_USER:-aayoub}"
SSH_OPTS=(-o BatchMode=yes -o ConnectTimeout=10 -o StrictHostKeyChecking=accept-new)
OUT="${WP_RESTORE_OUT:-/tmp/wp2-golden-service-restore.txt}"

mkdir -p "$(dirname "$OUT")"
exec > >(tee -a "$OUT") 2>&1

utc(){ date -u +%Y-%m-%dT%H:%M:%S.%NZ; }
bar(){
  local p="$1" msg="$2" n
  n=$((p/5))
  printf '\r['
  printf '%*s' "$n" '' | tr ' ' '#'
  printf '%*s' "$((20-n))" '' | tr ' ' '-'
  printf '] %3d%%  %-48s' "$p" "$msg"
}
ssh_do(){ ssh "${SSH_OPTS[@]}" "${REMOTE_USER}@$1" "${@:2}"; }

RESTORE_START_EPOCH=$(date +%s)
printf '=== WP2 Golden deterministic LTE restoration ===\n'
printf 'T_RESTORE_START=%s\nRESTORE_START_EPOCH=%s\n' "$(utc)" "$RESTORE_START_EPOCH"
printf 'CORE_HOST=%s\nUE_HOST=%s\n' "$CORE_HOST" "$UE_HOST"

bar 10 'Stopping UE and clearing tunnel/session'; echo
ssh_do "$UE_HOST" "tmux kill-session -t ue >/dev/null 2>&1 || true; sudo pkill -TERM -x srsue 2>/dev/null || true; for i in \$(seq 1 20); do pgrep -x srsue >/dev/null || break; sleep 0.5; done; sudo pkill -KILL -x srsue 2>/dev/null || true; ip link show tun_srsue >/dev/null 2>&1 && sudo ip link delete tun_srsue 2>/dev/null || true; ! pgrep -x srsue >/dev/null"
printf 'T_UE_STOPPED=%s\n' "$(utc)"

bar 25 'Stopping EPC/eNB cleanly'; echo
ssh_do "$CORE_HOST" "tmux kill-session -t enb >/dev/null 2>&1 || true; sudo pkill -TERM -x srsenb 2>/dev/null || true; sudo pkill -TERM -x srsepc 2>/dev/null || true; sleep 2; sudo pkill -KILL -x srsenb 2>/dev/null || true; sudo pkill -KILL -x srsepc 2>/dev/null || true; ! pgrep -x srsenb >/dev/null && ! pgrep -x srsepc >/dev/null"
printf 'T_CORE_RAN_STOPPED=%s\n' "$(utc)"

bar 40 'Starting profile-authoritative EPC/eNB path'; echo
ssh_do "$CORE_HOST" "set +e; /local/repository/bin/start.sh >/tmp/wp2-golden-core-start.console 2>&1; rc=\$?; printf '%s\\n' \"\$rc\" >/tmp/wp2-golden-core-start.rc; exit 0"
printf 'T_CORE_START_COMMAND_DONE=%s\n' "$(utc)"

bar 55 'Requiring stable EPC/eNB processes for 10 s'; echo
ssh_do "$CORE_HOST" "deadline=\$((\$(date +%s)+40)); stable=0; while [ \$(date +%s) -lt \$deadline ]; do if tmux has-session -t enb 2>/dev/null && pgrep -x srsepc >/dev/null && pgrep -x srsenb >/dev/null; then stable=\$((stable+1)); [ \$stable -ge 10 ] && exit 0; else stable=0; fi; sleep 1; done; echo 'CORE_RAN_READY=FAIL' >&2; exit 31"
CORE_START_RC="$(ssh_do "$CORE_HOST" "cat /tmp/wp2-golden-core-start.rc 2>/dev/null || echo unknown")"
printf 'CORE_PROFILE_START_RC=%s\n' "$CORE_START_RC"
printf 'T_CORE_RAN_READY=%s\n' "$(utc)"

bar 70 'Starting fresh UE only after core/RAN readiness'; echo
ssh_do "$UE_HOST" "set +e; /local/repository/bin/start.sh >/tmp/wp2-golden-ue-start.console 2>&1; rc=\$?; printf '%s\\n' \"\$rc\" >/tmp/wp2-golden-ue-start.rc; exit 0"
printf 'T_UE_START_COMMAND_DONE=%s\n' "$(utc)"

bar 85 'Verifying fresh UE/tunnel state'; echo
ssh_do "$UE_HOST" "deadline=\$((\$(date +%s)+40)); while [ \$(date +%s) -lt \$deadline ]; do if tmux has-session -t ue 2>/dev/null && pgrep -x srsue >/dev/null && ip link show tun_srsue >/dev/null 2>&1 && ip -4 addr show dev tun_srsue | grep -q 'inet '; then exit 0; fi; sleep 1; done; echo 'UE_PROCESS_TUN_READY=FAIL' >&2; exit 32"
UE_START_RC="$(ssh_do "$UE_HOST" "cat /tmp/wp2-golden-ue-start.rc 2>/dev/null || echo unknown")"
printf 'UE_PROFILE_START_RC=%s\n' "$UE_START_RC"
printf 'T_UE_PROCESS_READY=%s\n' "$(utc)"

bar 100 'Clean-order LTE restoration command sequence complete'; echo
printf 'WP_RESTORE_START_EPOCH=%s\n' "$RESTORE_START_EPOCH"
printf 'WP2_GOLDEN_SERVICE_RESTORE_SEQUENCE=PASS\n'
