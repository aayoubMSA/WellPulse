#!/usr/bin/env bash
set -euo pipefail

A3_ID="357f3275-403d-491a-906f-99677bdf454f"
PORTAL_HTTP="${PORTAL_HTTP:-https://boss.emulab.net:43794}"
PORTAL_TOKEN="${PORTAL_TOKEN:-}"
POWDER_SSH_PRIVATE_KEY="${POWDER_SSH_PRIVATE_KEY:-}"
POWDER_SSH_KEY_PASSPHRASE="${POWDER_SSH_KEY_PASSPHRASE:-}"
POWDER_USERNAME="${POWDER_USERNAME:-aayoub}"
TMP="/tmp/wp2-a3-q0-prepare"
SSH_AGENT_STARTED=0

export PORTAL_HTTP PORTAL_TOKEN POWDER_SSH_PRIVATE_KEY POWDER_SSH_KEY_PASSPHRASE

bar(){ local p="$1" m="$2" n; n=$((p/5)); printf '\r['; printf '%*s' "$n" ''|tr ' ' '#'; printf '%*s' "$((20-n))" ''|tr ' ' '-'; printf '] %3d%%  %-58s' "$p" "$m"; }
fail(){ echo; echo "WP2_A3_Q0_PREPARE=FAIL:$1" >&2; exit "${2:-90}"; }
cleanup(){ set +e; [[ "$SSH_AGENT_STARTED" -eq 1 ]] && ssh-agent -k >/dev/null 2>&1 || true; rm -f "$TMP/private.key" "$TMP/askpass"; }
trap cleanup EXIT

[[ -n "$PORTAL_TOKEN" ]] || fail POWDER_API_TOKEN_MISSING 2
[[ -n "$POWDER_SSH_PRIVATE_KEY" ]] || fail POWDER_SSH_PRIVATE_KEY_MISSING 2
rm -rf "$TMP" /tmp/portal-api
mkdir -p "$TMP"
chmod 700 "$TMP"
umask 077

bar 5 'Authenticating without exposing credentials'; echo
python3 - <<'PY'
import os
from pathlib import Path
raw=os.environ['POWDER_SSH_PRIVATE_KEY'].replace('\\r\\n','\n').replace('\\r','\n').lstrip('\ufeff').strip()+"\n"
Path('/tmp/wp2-a3-q0-prepare/private.key').write_text(raw,encoding='utf-8',newline='\n')
PY
chmod 600 "$TMP/private.key"
cat > "$TMP/askpass" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' "$POWDER_SSH_KEY_PASSPHRASE"
EOF
chmod 700 "$TMP/askpass"
export SSH_ASKPASS="$TMP/askpass" SSH_ASKPASS_REQUIRE=force DISPLAY=:0
setsid -w ssh-keygen -y -f "$TMP/private.key" > "$TMP/public.key" </dev/null || fail SSH_KEY_DERIVATION 3
eval "$(ssh-agent -s)" >/dev/null
SSH_AGENT_STARTED=1
setsid -w ssh-add "$TMP/private.key" </dev/null >/dev/null || fail SSH_KEY_LOAD 3

bar 10 'Binding to A3 through official Portal API'; echo
git clone --depth 1 https://gitlab.flux.utah.edu/emulab/portal-api.git /tmp/portal-api >/dev/null 2>&1 || fail PORTAL_CLIENT_CLONE 4
python3 -m pip install --quiet '/tmp/portal-api[cli]' || fail PORTAL_CLIENT_INSTALL 4
portal-cli experiment get --experiment-id "$A3_ID" > "$TMP/a3.json" || fail A3_NOT_FOUND 5
STATUS="$(jq -r '.status // empty' "$TMP/a3.json")"
[[ "$STATUS" == ready ]] || fail "A3_NOT_READY:$STATUS" 5
portal-cli experiment manifests get --experiment-id "$A3_ID" > "$TMP/manifests.json" || fail A3_MANIFEST 5

python3 - "$TMP/manifests.json" "$TMP/nodes.json" <<'PY'
import json,sys,xml.etree.ElementTree as ET
obj=json.load(open(sys.argv[1])); xmls=[]
def walk(x):
    if isinstance(x,dict):
        for v in x.values(): walk(v)
    elif isinstance(x,list):
        for v in x: walk(v)
    elif isinstance(x,str) and '<' in x and 'rspec' in x.lower(): xmls.append(x)
walk(obj); out={}
for text in xmls:
    try: root=ET.fromstring(text)
    except Exception: continue
    for node in root.iter():
        if node.tag.rsplit('}',1)[-1] != 'node': continue
        cid=node.attrib.get('client_id','')
        if cid not in {'enb1','rue1'}: continue
        row={'client_id':cid}
        for ch in node.iter():
            tag=ch.tag.rsplit('}',1)[-1]
            if tag=='hardware_type' and 'hardware_type' not in row: row['hardware_type']=ch.attrib.get('name','')
            if tag=='login' and ch.attrib.get('hostname') and 'login' not in row:
                row['login']={'username':ch.attrib.get('username','aayoub'),'hostname':ch.attrib['hostname'],'port':int(ch.attrib.get('port','22'))}
        out[cid]=row
for cid in ('enb1','rue1'):
    if cid not in out or 'login' not in out[cid]: raise SystemExit('missing '+cid)
    if out[cid].get('hardware_type')!='nuc5300': raise SystemExit('unexpected hardware '+cid)
json.dump(out,open(sys.argv[2],'w'),indent=2,sort_keys=True)
PY

get_login(){ jq -r --arg n "$1" '.[$n].login | [.username,.hostname,(.port|tostring)] | @tsv' "$TMP/nodes.json"; }
IFS=$'\t' read -r CORE_USER CORE_HOST CORE_PORT < <(get_login enb1)
IFS=$'\t' read -r UE_USER UE_HOST UE_PORT < <(get_login rue1)
CORE_USER="${CORE_USER:-$POWDER_USERNAME}"; UE_USER="${UE_USER:-$POWDER_USERNAME}"
SSH=(-A -o BatchMode=yes -o IdentitiesOnly=no -o ConnectTimeout=15 -o ServerAliveInterval=10 -o ServerAliveCountMax=3 -o StrictHostKeyChecking=accept-new -o UserKnownHostsFile="$TMP/known_hosts")

bar 20 'Pre-mutation dependency and storage gate'; echo
ssh "${SSH[@]}" -p "$CORE_PORT" "$CORE_USER@$CORE_HOST" 'set -eu
test -x /local/repository/bin/start.sh
test -d /proj/WellPulse && test -w /proj/WellPulse
for c in tmux sudo pgrep rsync openssl mosquitto; do command -v "$c" >/dev/null; done
printf "CORE_PREMUTATION=PASS\n"' || fail CORE_PREMUTATION 6
ssh "${SSH[@]}" -p "$UE_PORT" "$UE_USER@$UE_HOST" 'set -eu
test -x /local/repository/bin/start.sh
test -x /usr/local/etc/emulab/tmcc
test -d /proj/WellPulse && test -w /proj/WellPulse
for c in tmux sudo pgrep rsync openssl ip ping curl; do command -v "$c" >/dev/null; done
printf "UE_PREMUTATION=PASS\n"' || fail UE_PREMUTATION 6

bar 32 'Stopping stale UE state'; echo
ssh "${SSH[@]}" -p "$UE_PORT" "$UE_USER@$UE_HOST" 'set -u
tmux kill-session -t ue >/dev/null 2>&1 || true
sudo killall srsue >/dev/null 2>&1 || true
sudo ip link del tun_srsue >/dev/null 2>&1 || true
sleep 2
! pgrep -x srsue >/dev/null 2>&1' || fail STOP_UE 7

bar 42 'Stopping stale EPC/eNB state'; echo
ssh "${SSH[@]}" -p "$CORE_PORT" "$CORE_USER@$CORE_HOST" 'set -u
tmux kill-session -t enb >/dev/null 2>&1 || true
sudo killall srsenb srsepc >/dev/null 2>&1 || true
sleep 2
! pgrep -x srsepc >/dev/null 2>&1
! pgrep -x srsenb >/dev/null 2>&1' || fail STOP_CORE 8

bar 54 'Starting clean EPC/eNB through profile start.sh'; echo
ssh "${SSH[@]}" -p "$CORE_PORT" "$CORE_USER@$CORE_HOST" 'cd /local/repository && set +e; bash bin/start.sh > /tmp/wp2-a3-q0-core.console 2>&1; rc=$?; printf "%s\n" "$rc" > /tmp/wp2-a3-q0-core.start_rc; exit 0' || fail CORE_START_TRANSPORT 9
CORE_READY=0
for i in $(seq 1 45); do
  if ssh "${SSH[@]}" -p "$CORE_PORT" "$CORE_USER@$CORE_HOST" 'tmux has-session -t enb 2>/dev/null && pgrep -x srsepc >/dev/null && pgrep -x srsenb >/dev/null'; then CORE_READY=1; break; fi
  printf '\rCORE_READY_WAIT=%02d/45' "$i"; sleep 2
done
echo
[[ "$CORE_READY" -eq 1 ]] || fail CORE_NOT_READY 9
sleep 10
ssh "${SSH[@]}" -p "$CORE_PORT" "$CORE_USER@$CORE_HOST" 'tmux has-session -t enb 2>/dev/null && pgrep -x srsepc >/dev/null && pgrep -x srsenb >/dev/null' || fail CORE_NOT_STABLE 9
CORE_START_RC="$(ssh "${SSH[@]}" -p "$CORE_PORT" "$CORE_USER@$CORE_HOST" 'cat /tmp/wp2-a3-q0-core.start_rc 2>/dev/null || echo unknown')"
echo "CORE_PROFILE_START_RC=$CORE_START_RC"

bar 70 'Starting fresh UE through profile start.sh'; echo
ssh "${SSH[@]}" -p "$UE_PORT" "$UE_USER@$UE_HOST" 'cd /local/repository && set +e; bash bin/start.sh > /tmp/wp2-a3-q0-ue.console 2>&1; rc=$?; printf "%s\n" "$rc" > /tmp/wp2-a3-q0-ue.start_rc; exit 0' || fail UE_START_TRANSPORT 10
UE_READY=0
for i in $(seq 1 60); do
  if ssh "${SSH[@]}" -p "$UE_PORT" "$UE_USER@$UE_HOST" 'tmux has-session -t ue 2>/dev/null && pgrep -x srsue >/dev/null && ip link show tun_srsue >/dev/null 2>&1 && ip -4 addr show dev tun_srsue | grep -q "inet "'; then UE_READY=1; break; fi
  printf '\rUE_READY_WAIT=%02d/60' "$i"; sleep 2
done
echo
[[ "$UE_READY" -eq 1 ]] || fail UE_TUN_NOT_READY 10
UE_START_RC="$(ssh "${SSH[@]}" -p "$UE_PORT" "$UE_USER@$UE_HOST" 'cat /tmp/wp2-a3-q0-ue.start_rc 2>/dev/null || echo unknown')"
echo "UE_PROFILE_START_RC=$UE_START_RC"

bar 86 'Verifying Q0 user plane 5/5'; echo
ssh "${SSH[@]}" -p "$UE_PORT" "$UE_USER@$UE_HOST" 'set -eu
ip route get 172.16.0.1 | grep -q tun_srsue
ping -I tun_srsue -c 5 -W 2 172.16.0.1 | tee /tmp/wp2-a3-q0-ping.txt
grep -Eq "5 packets transmitted, 5 received|5 packets transmitted, 5 packets received" /tmp/wp2-a3-q0-ping.txt' || fail Q0_USER_PLANE 11

bar 100 'A3 pre-science Q0 baseline PASS'; echo
printf 'A3_ID=%s\n' "$A3_ID"
printf 'A3_STATUS=ready\n'
printf 'A3_Q0_BASELINE=PASS\n'
printf 'GOLDEN_EXECUTED=NO\n'
printf 'RF_ATTENUATION_CHANGED=NO\n'
printf 'SCORED_RUN_EXECUTED=NO\n'
