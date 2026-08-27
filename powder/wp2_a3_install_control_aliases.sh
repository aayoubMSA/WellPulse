#!/usr/bin/env bash
set -euo pipefail

CORE_EXT="${WP_A3_CORE_EXT:-nuc1.emulab.net}"
UE_EXT="${WP_A3_UE_EXT:-nuc2.emulab.net}"
REMOTE_USER="${POWDER_USERNAME:-aayoub}"
POWDER_SSH_PRIVATE_KEY="${POWDER_SSH_PRIVATE_KEY:-}"
POWDER_SSH_KEY_PASSPHRASE="${POWDER_SSH_KEY_PASSPHRASE:-}"
TMP="/tmp/wp2-a3-aliases"
SSH_AGENT_STARTED=0

bar(){ local p="$1" m="$2" n; n=$((p/5)); printf '\r['; printf '%*s' "$n" ''|tr ' ' '#'; printf '%*s' "$((20-n))" ''|tr ' ' '-'; printf '] %3d%%  %-56s' "$p" "$m"; }
fail(){ echo; echo "WP2_A3_CONTROL_ALIASES=FAIL:$1" >&2; exit "${2:-90}"; }
cleanup(){ set +e; [[ "$SSH_AGENT_STARTED" -eq 1 ]] && ssh-agent -k >/dev/null 2>&1 || true; rm -rf "$TMP"; }
trap cleanup EXIT

[[ -n "$POWDER_SSH_PRIVATE_KEY" ]] || fail SSH_KEY_MISSING 2
rm -rf "$TMP"; mkdir -p "$TMP" "$HOME/.ssh"; chmod 700 "$TMP" "$HOME/.ssh"; umask 077

bar 10 'Preparing SSH identity'; echo
python3 - <<'PY'
import os
from pathlib import Path
raw=os.environ['POWDER_SSH_PRIVATE_KEY'].replace('\\r\\n','\n').replace('\\r','\n').lstrip('\ufeff').strip()+"\n"
Path('/tmp/wp2-a3-aliases/key').write_text(raw,encoding='utf-8',newline='\n')
PY
chmod 600 "$TMP/key"
cat > "$TMP/askpass" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' "$POWDER_SSH_KEY_PASSPHRASE"
EOF
chmod 700 "$TMP/askpass"
export SSH_ASKPASS="$TMP/askpass" SSH_ASKPASS_REQUIRE=force DISPLAY=:0
setsid -w ssh-keygen -y -f "$TMP/key" >/dev/null </dev/null || fail SSH_KEY_INVALID 3
eval "$(ssh-agent -s)" >/dev/null; SSH_AGENT_STARTED=1
setsid -w ssh-add "$TMP/key" </dev/null >/dev/null || fail SSH_KEY_LOAD 3

bar 35 'Installing idempotent A3 control aliases on UE'; echo
ssh -A -o BatchMode=yes -o ConnectTimeout=15 -o StrictHostKeyChecking=accept-new "$REMOTE_USER@$UE_EXT" "CORE_EXT='$CORE_EXT' UE_EXT='$UE_EXT' bash -s" <<'REMOTE'
set -euo pipefail
core_ip="$(getent ahostsv4 "$CORE_EXT" | awk 'NR==1{print $1}')"
ue_ip="$(getent ahostsv4 "$UE_EXT" | awk 'NR==1{print $1}')"
python3 - "$core_ip" "$ue_ip" <<'PY'
import ipaddress,sys
for x in sys.argv[1:]: ipaddress.ip_address(x)
PY
sudo sed -i '/# WP2_A3_CONTROL_ALIAS$/d' /etc/hosts
printf '%s enb1 # WP2_A3_CONTROL_ALIAS\n%s rue1 # WP2_A3_CONTROL_ALIAS\n' "$core_ip" "$ue_ip" | sudo tee -a /etc/hosts >/dev/null
actual_core="$(getent ahostsv4 enb1 | awk 'NR==1{print $1}')"
actual_ue="$(getent ahostsv4 rue1 | awk 'NR==1{print $1}')"
[[ "$actual_core" == "$core_ip" ]]
[[ "$actual_ue" == "$ue_ip" ]]
printf 'ENB1_ALIAS_IP=%s\nRUE1_ALIAS_IP=%s\n' "$actual_core" "$actual_ue"
REMOTE

bar 70 'Verifying nested SSH over installed aliases'; echo
ssh -A -o BatchMode=yes -o ConnectTimeout=15 -o StrictHostKeyChecking=accept-new "$REMOTE_USER@$UE_EXT" "REMOTE_USER='$REMOTE_USER' bash -s" <<'REMOTE'
set -euo pipefail
ssh -o BatchMode=yes -o ConnectTimeout=12 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "$REMOTE_USER@enb1" 'test "$(hostname)" = nuc1'
ssh -o BatchMode=yes -o ConnectTimeout=12 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null "$REMOTE_USER@rue1" 'test "$(hostname)" = nuc2'
REMOTE

bar 100 'A3 control alias topology PASS'; echo
printf 'WP2_A3_CONTROL_ALIASES=PASS\n'
printf 'GOLDEN_EXECUTED=NO\n'
printf 'RF_ATTENUATION_CHANGED=NO\n'
printf 'SCORED_RUN_EXECUTED=NO\n'
