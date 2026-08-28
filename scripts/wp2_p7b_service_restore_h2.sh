#!/usr/bin/env bash
set -euo pipefail

CORE_HOST="${WP_CORE_HOST:?WP_CORE_HOST is required}"
UE_HOST="${WP_UE_HOST:?WP_UE_HOST is required}"
REMOTE_USER="${WP_REMOTE_USER:-aayoub}"
CONTROLLER_PID="${WP_CONTROLLER_PID:?WP_CONTROLLER_PID is required}"
CONTROLLER_SESSION="${WP_CONTROLLER_SESSION:?WP_CONTROLLER_SESSION is required}"
CONTROLLER_HOST_ROLE="${WP_CONTROLLER_HOST_ROLE:?WP_CONTROLLER_HOST_ROLE is required}"
OUT="${WP_RESTORE_OUT:-/tmp/wp2-p7b-h2-service-restore.txt}"
FRONTIER="${WP_RESTORE_FRONTIER:?WP_RESTORE_FRONTIER is required}"
SSH_OPTS=(-o BatchMode=yes -o ConnectTimeout=10 -o StrictHostKeyChecking=accept-new)

mkdir -p "$(dirname "$OUT")" "$(dirname "$FRONTIER")"
exec > >(tee -a "$OUT") 2>&1

utc(){ date -u +%Y-%m-%dT%H:%M:%S.%NZ; }
mono(){ awk '{print $1}' /proc/uptime; }
ssh_do(){ ssh "${SSH_OPTS[@]}" "${REMOTE_USER}@$1" "${@:2}"; }
frontier(){
  local phase="$1" status="$2" line
  line=$(printf '{"phase":"%s","utc":"%s","monotonic":"%s","status":"%s"}' "$phase" "$(utc)" "$(mono)" "$status")
  printf '%s\n' "$line" >> "$FRONTIER"
  sync "$FRONTIER" 2>/dev/null || sync
}

case "$CONTROLLER_PID" in
  ''|*[!0-9]*) echo "H2_OWNERSHIP=BLOCKED:INVALID_CONTROLLER_PID"; exit 61;;
esac
if [ "$CONTROLLER_PID" -le 1 ]; then
  echo "H2_OWNERSHIP=BLOCKED:INVALID_CONTROLLER_PID"; exit 61
fi
case "$CONTROLLER_HOST_ROLE" in
  UE|EXTERNAL) ;;
  *) echo "H2_OWNERSHIP=BLOCKED:INVALID_CONTROLLER_HOST_ROLE"; exit 62;;
esac
case "$CONTROLLER_SESSION" in
  ue|srs-ue|enb|srs-enb|srs-epc)
    echo "H2_OWNERSHIP=BLOCKED:CONTROLLER_IN_SERVICE_SESSION:$CONTROLLER_SESSION"
    exit 63
    ;;
  '') echo "H2_OWNERSHIP=BLOCKED:CONTROLLER_SESSION_UNKNOWN"; exit 64;;
esac

printf 'CONTROLLER_SERVICE_SESSION_DISJOINTNESS=PASS\n'
printf 'CONTROLLER_RESTORE_FAILURE_DOMAIN_SEPARATION=PASS\n'
printf 'DESTRUCTIVE_TMUX_SESSION_KILL_AUTHORIZED=NO\n'
printf 'CONTROLLER_PID=%s\nCONTROLLER_SESSION=%s\nCONTROLLER_HOST_ROLE=%s\n' \
  "$CONTROLLER_PID" "$CONTROLLER_SESSION" "$CONTROLLER_HOST_ROLE"

stop_exact_processes(){
  local host="$1" role="$2"; shift 2
  local names=("$@")
  local cpid=0
  if [ "$CONTROLLER_HOST_ROLE" = "$role" ]; then cpid="$CONTROLLER_PID"; fi
  local joined=""
  local n
  for n in "${names[@]}"; do
    case "$n" in srsue|srsenb|srsepc) ;; *) echo "UNAPPROVED_SERVICE_PROCESS_TARGET=$n"; exit 65;; esac
    joined+=" $n"
  done

  ssh_do "$host" "set -eu
CPID='$cpid'
NAMES='$joined'
for n in \$NAMES; do
  PIDS=\$(pgrep -x \"\$n\" || true)
  for p in \$PIDS; do
    if [ \"\$CPID\" != 0 ] && [ \"\$p\" = \"\$CPID\" ]; then
      echo \"SERVICE_PID_OWNERSHIP_PROOF=BLOCKED process=\$n controller_pid=\$CPID\" >&2
      exit 71
    fi
  done
  echo \"SERVICE_PID_OWNERSHIP_PROOF=PASS role=$role process=\$n pids=\${PIDS:-NONE}\"
  for p in \$PIDS; do sudo kill -TERM \"\$p\"; done
  for i in \$(seq 1 20); do
    alive=0
    for p in \$PIDS; do sudo kill -0 \"\$p\" 2>/dev/null && alive=1 || true; done
    [ \"\$alive\" -eq 0 ] && break
    sleep 0.5
  done
  for p in \$PIDS; do sudo kill -0 \"\$p\" 2>/dev/null && sudo kill -KILL \"\$p\" || true; done
  ! pgrep -x \"\$n\" >/dev/null
done"
}

assert_no_stale_service_tmux(){
  local host="$1"; shift
  local s
  for s in "$@"; do
    if ssh_do "$host" "tmux has-session -t '$s' >/dev/null 2>&1"; then
      echo "H2_OWNERSHIP=BLOCKED:STALE_SERVICE_TMUX_SESSION:$s" >&2
      exit 72
    fi
  done
}

RESTORE_START_EPOCH=$(date +%s)
printf '=== WP2 P7B H2 ownership-safe LTE restoration ===\n'
printf 'T_RESTORE_START=%s\nRESTORE_START_EPOCH=%s\n' "$(utc)" "$RESTORE_START_EPOCH"
printf 'CORE_HOST=%s\nUE_HOST=%s\n' "$CORE_HOST" "$UE_HOST"
frontier RESTORE_REQUESTED BEGIN

printf 'PHASE=UE_PID_SCOPED_CLEANUP_BEGIN\n'
frontier UE_CLEANUP_BEGIN BEGIN
stop_exact_processes "$UE_HOST" UE srsue
ssh_do "$UE_HOST" "ip link show tun_srsue >/dev/null 2>&1 && sudo ip link delete tun_srsue 2>/dev/null || true"
assert_no_stale_service_tmux "$UE_HOST" ue srs-ue
printf 'T_UE_STOPPED=%s\n' "$(utc)"
frontier UE_CLEANUP_END PASS
printf 'PHASE=UE_PID_SCOPED_CLEANUP_END\n'

printf 'PHASE=CORE_PID_SCOPED_CLEANUP_BEGIN\n'
frontier CORE_CLEANUP_BEGIN BEGIN
stop_exact_processes "$CORE_HOST" CORE srsenb srsepc
assert_no_stale_service_tmux "$CORE_HOST" enb srs-enb srs-epc
printf 'T_CORE_RAN_STOPPED=%s\n' "$(utc)"
frontier CORE_CLEANUP_END PASS
printf 'PHASE=CORE_PID_SCOPED_CLEANUP_END\n'

printf 'PHASE=CORE_START\n'
frontier CORE_START_BEGIN BEGIN
ssh_do "$CORE_HOST" "set +e; /local/repository/bin/start.sh >/tmp/wp2-p7b-h2-core-start.console 2>&1; rc=\$?; printf '%s\\n' \"\$rc\" >/tmp/wp2-p7b-h2-core-start.rc; exit 0"
printf 'T_CORE_START_COMMAND_DONE=%s\n' "$(utc)"
frontier CORE_START_END PASS

ssh_do "$CORE_HOST" "deadline=\$((\$(date +%s)+40)); stable=0; while [ \$(date +%s) -lt \$deadline ]; do if pgrep -x srsepc >/dev/null && pgrep -x srsenb >/dev/null; then stable=\$((stable+1)); [ \$stable -ge 10 ] && exit 0; else stable=0; fi; sleep 1; done; echo 'CORE_RAN_READY=FAIL' >&2; exit 31"
printf 'T_CORE_RAN_READY=%s\n' "$(utc)"
frontier CORE_STABLE_READY PASS

printf 'PHASE=UE_START\n'
frontier UE_START_BEGIN BEGIN
ssh_do "$UE_HOST" "set +e; /local/repository/bin/start.sh >/tmp/wp2-p7b-h2-ue-start.console 2>&1; rc=\$?; printf '%s\\n' \"\$rc\" >/tmp/wp2-p7b-h2-ue-start.rc; exit 0"
printf 'T_UE_START_COMMAND_DONE=%s\n' "$(utc)"
frontier UE_START_END PASS

ssh_do "$UE_HOST" "deadline=\$((\$(date +%s)+30)); while [ \$(date +%s) -lt \$deadline ]; do pgrep -x srsue >/dev/null && exit 0; sleep 1; done; echo 'UE_PROCESS_READY=FAIL' >&2; exit 32"
printf 'T_UE_PROCESS_READY=%s\n' "$(utc)"
frontier UE_PROCESS_READY PASS
printf 'WP_RESTORE_START_EPOCH=%s\n' "$RESTORE_START_EPOCH"
printf 'H2_SAFE_RESTORE_SEQUENCE=PASS\n'
