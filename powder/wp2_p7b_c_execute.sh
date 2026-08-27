#!/usr/bin/env bash
set -euo pipefail

TMP="/tmp/wp2-p7b-c"
RESULT="$TMP/result.env"
mkdir -p "$TMP"
: > "$RESULT"

PORTAL_HTTP="${PORTAL_HTTP:-https://boss.emulab.net:43794}"
PORTAL_TOKEN="${PORTAL_TOKEN:-}"
POWDER_USERNAME="${POWDER_USERNAME:-aayoub}"
POWDER_SSH_PRIVATE_KEY="${POWDER_SSH_PRIVATE_KEY:-}"
POWDER_SSH_KEY_PASSPHRASE="${POWDER_SSH_KEY_PASSPHRASE:-}"
PROFILE_PROJECT="PowderProfiles"
PROFILE_NAME="srslte-controlled-rf"
EXPECTED_PROFILE_REVISION="a6da96560b6526dc6816761282722c996418fd8c"
EXPECTED_HARDWARE="nuc5300"
EXPECTED_IMAGE="urn:publicid:IDN+emulab.net+image+PowderProfiles:U18LL-SRSLTE:1"
BINDINGS='{"enb_node":"nuc1","ue_node":"nuc2","ue_type":"srsue"}'
SOURCE_SHA="${GITHUB_SHA:-$(git rev-parse HEAD)}"
export PORTAL_HTTP PORTAL_TOKEN

EXPID=""
EXP_NAME=""
RUN_ID=""
SSH_AGENT_STARTED=0
NODE_RC=99

bar(){ local p="$1" m="$2" n; n=$((p/5)); printf '\r['; printf '%*s' "$n" ''|tr ' ' '#'; printf '%*s' "$((20-n))" ''|tr ' ' '-'; printf '] %3d%%  %-62s' "$p" "$m"; }
utc(){ date -u +%Y-%m-%dT%H:%M:%SZ; }
fail(){ echo; echo "WP2_P7B_C_EXECUTE=FAIL:$1" >&2; printf 'FAILURE=%s\n' "$1" >> "$RESULT"; exit "${2:-90}"; }

on_exit(){
  local rc=$?
  set +e
  if [[ "$SSH_AGENT_STARTED" -eq 1 ]]; then ssh-agent -k >/dev/null 2>&1 || true; fi
  rm -f "$TMP/private.key" "$TMP/askpass"
  if [[ -n "$EXPID" ]]; then
    echo "EXPERIMENT_LEFT_LIVE=$EXPID"
    echo "P7B_D=NOT_STARTED"
    echo "AUTOMATIC_TERMINATION=PROHIBITED"
    echo "TEARDOWN_AUTHORIZED=NO"
  fi
  exit "$rc"
}
trap on_exit EXIT

[[ -n "$PORTAL_TOKEN" ]] || fail POWDER_API_TOKEN_MISSING 2
[[ -n "$POWDER_SSH_PRIVATE_KEY" ]] || fail POWDER_SSH_PRIVATE_KEY_MISSING 2
command -v jq >/dev/null || fail JQ_MISSING 2
command -v curl >/dev/null || fail CURL_MISSING 2

bar 3 'Pinning Portal client and loading approved SSH identity'; echo
bash scripts/wp2_portal_client_bootstrap.sh /tmp/portal-api | tee "$TMP/portal-pin.txt"
grep -q '^PORTAL_API_PIN_GATE=PASS$' "$TMP/portal-pin.txt" || fail PORTAL_CLIENT_PIN 3
umask 077
mkdir -p "$HOME/.ssh"
python3 - <<'PY'
import os
from pathlib import Path
raw=os.environ['POWDER_SSH_PRIVATE_KEY'].replace('\r\n','\n').replace('\r','\n').lstrip('\ufeff').strip()+"\n"
Path('/tmp/wp2-p7b-c/private.key').write_text(raw,encoding='utf-8',newline='\n')
PY
chmod 600 "$TMP/private.key"
cat > "$TMP/askpass" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' "$POWDER_SSH_KEY_PASSPHRASE"
EOF
chmod 700 "$TMP/askpass"
export SSH_ASKPASS="$TMP/askpass" SSH_ASKPASS_REQUIRE=force DISPLAY=:0
setsid -w ssh-keygen -y -f "$TMP/private.key" > "$TMP/public.key" </dev/null || fail SSH_KEY_DERIVATION 4
eval "$(ssh-agent -s)" >/dev/null
SSH_AGENT_STARTED=1
setsid -w ssh-add "$TMP/private.key" </dev/null >/dev/null || fail SSH_KEY_LOAD 4
: > "$HOME/.ssh/known_hosts"
chmod 600 "$HOME/.ssh/known_hosts"

bar 8 'Fail-closing on any existing P7B live reservation'; echo
portal-cli experiment list > "$TMP/list-before.json" || fail PORTAL_LIST 5
python3 - "$TMP/list-before.json" <<'PY'
import json,sys
obj=json.load(open(sys.argv[1])); xs=obj if isinstance(obj,list) else obj.get('experiments',[])
terminal={'terminated','destroyed','failed','error'}; active=[]
for x in xs:
    if not isinstance(x,dict) or x.get('project')!='WellPulse': continue
    name=str(x.get('name','')); status=str(x.get('status','')).lower()
    if (name.startswith('WP-P7B-') or name.startswith('wp7b')) and status not in terminal:
        active.append({'id':x.get('id'),'name':name,'status':status})
if active:
    print('ACTIVE_P7B_CONFLICT='+json.dumps(active,sort_keys=True,separators=(',',':'))); raise SystemExit(20)
print('ACTIVE_P7B_CONFLICT=NONE')
PY

bar 12 'Creating the single authorized non-scored P7B reservation'; echo
SUFFIX="${GITHUB_RUN_ID:-manual}"; SUFFIX="${SUFFIX: -7}"; EXP_NAME="wp7b${SUFFIX}"
[[ ${#EXP_NAME} -le 16 ]] || fail EXPERIMENT_NAME_LENGTH 6
PUB="$(cat "$TMP/public.key")"
portal-cli experiment create \
  --name "$EXP_NAME" --project WellPulse \
  --profile-name "$PROFILE_NAME" --profile-project "$PROFILE_PROJECT" \
  --duration 2 --bindings "$BINDINGS" --sshpubkey "$PUB" > "$TMP/create.json" || fail RESERVATION_CREATE 6
EXPID="$(jq -r '.id // empty' "$TMP/create.json")"
[[ "$EXPID" =~ ^[0-9A-Fa-f-]{36}$ ]] || fail CREATE_RETURNED_NO_UUID 6
printf 'EXPERIMENT_ID=%s\nEXPERIMENT_NAME=%s\nSOURCE_SHA=%s\n' "$EXPID" "$EXP_NAME" "$SOURCE_SHA" | tee -a "$RESULT"

bar 17 'Waiting for authoritative Portal READY'; echo
READY=0
for i in $(seq 1 75); do
  set +e; portal-cli experiment get --experiment-id "$EXPID" > "$TMP/status.json" 2>"$TMP/status.err"; grc=$?; set -e
  if [[ "$grc" -ne 0 ]]; then echo "PORTAL_POLL_${i}=GET_ERROR"; sleep 20; continue; fi
  STATUS="$(jq -r '.status // "unknown"' "$TMP/status.json")"; echo "PORTAL_POLL_${i}=$STATUS"
  [[ "$STATUS" == ready ]] && { READY=1; break; }
  [[ "$STATUS" =~ ^(failed|error|terminated|destroyed)$ ]] && fail "PORTAL_TERMINAL_$STATUS" 7
  sleep 20
done
[[ "$READY" -eq 1 ]] || fail READY_TIMEOUT 7
python3 scripts/wp2_portal_record_guard.py --json "$TMP/status.json" --expected-experiment-id "$EXPID" | tee "$TMP/portal-record-gate.txt"
grep -q '^PORTAL_RECORD_GATE=PASS$' "$TMP/portal-record-gate.txt" || fail PORTAL_RECORD_GATE 7
EXPIRES="$(awk -F= '$1=="EXPIRES_UTC" {print $2}' "$TMP/portal-record-gate.txt" | tail -1)"
python3 scripts/wp2_prelaunch_time_guard.py --now-utc "$(utc)" --expires-utc "$EXPIRES" --min-remaining-s 4800 | tee "$TMP/time-gate.txt"
grep -q '^PRELAUNCH_TIME_GATE=PASS$' "$TMP/time-gate.txt" || fail PRELAUNCH_TIME 7
[[ "$(jq -r '.bindings.enb_node // empty' "$TMP/status.json")" == nuc1 ]] || fail BINDING_ENB 7
[[ "$(jq -r '.bindings.ue_node // empty' "$TMP/status.json")" == nuc2 ]] || fail BINDING_UE 7
[[ "$(jq -r '.bindings.ue_type // empty' "$TMP/status.json")" == srsue ]] || fail BINDING_UE_TYPE 7
printf 'HARD_EXPIRY_UTC=%s\n' "$EXPIRES" | tee -a "$RESULT"

bar 22 'Freezing manifest hardware/image identity and login endpoints'; echo
portal-cli experiment manifests get --experiment-id "$EXPID" > "$TMP/manifests.json" || fail MANIFEST_FETCH 8
python3 - "$TMP/manifests.json" "$TMP/nodes.json" "$EXPECTED_HARDWARE" "$EXPECTED_IMAGE" <<'PY'
import json,sys,xml.etree.ElementTree as ET
obj=json.load(open(sys.argv[1])); out={}; xmls=[]; expected_hw,expected_img=sys.argv[3],sys.argv[4]
def walk(x):
    if isinstance(x,dict):
        for v in x.values(): walk(v)
    elif isinstance(x,list):
        for v in x: walk(v)
    elif isinstance(x,str) and '<' in x and ('rspec' in x.lower() or '<node' in x.lower()): xmls.append(x)
walk(obj)
for text in xmls:
    try: root=ET.fromstring(text)
    except Exception: continue
    for node in root.iter():
        if node.tag.rsplit('}',1)[-1]!='node': continue
        cid=node.attrib.get('client_id','')
        if cid not in {'enb1','rue1'}: continue
        row={'client_id':cid,'component_id':node.attrib.get('component_id','')}
        for ch in node.iter():
            tag=ch.tag.rsplit('}',1)[-1]
            if tag=='hardware_type' and 'hardware_type' not in row: row['hardware_type']=ch.attrib.get('name','')
            if tag=='disk_image' and 'disk_image' not in row: row['disk_image']=ch.attrib.get('name','')
            if tag=='login' and ch.attrib.get('hostname') and 'login' not in row:
                row['login']={'username':ch.attrib.get('username',''),'hostname':ch.attrib['hostname'],'port':int(ch.attrib.get('port','22'))}
        out[cid]=row
for cid,node in (('enb1','nuc1'),('rue1','nuc2')):
    r=out.get(cid) or {}; assert r.get('login'), f'missing login {cid}'
    assert r.get('hardware_type')==expected_hw,(cid,r.get('hardware_type'))
    assert r.get('disk_image')==expected_img,(cid,r.get('disk_image'))
    assert r.get('component_id','').endswith('+'+node),(cid,r.get('component_id'))
json.dump(out,open(sys.argv[2],'w'),indent=2,sort_keys=True); print('P7B_C_MANIFEST_IDENTITY=PASS')
PY
get_login(){ jq -r --arg n "$1" '.[$n].login | [.username,.hostname,(.port|tostring)] | @tsv' "$TMP/nodes.json"; }
IFS=$'\t' read -r CORE_USER CORE_EXT CORE_PORT < <(get_login enb1)
IFS=$'\t' read -r UE_USER UE_EXT UE_PORT < <(get_login rue1)
CORE_USER="${CORE_USER:-$POWDER_USERNAME}"; UE_USER="${UE_USER:-$POWDER_USERNAME}"
printf 'CORE_USER=%s\nCORE_EXT=%s\nCORE_PORT=%s\nUE_USER=%s\nUE_EXT=%s\nUE_PORT=%s\n' "$CORE_USER" "$CORE_EXT" "$CORE_PORT" "$UE_USER" "$UE_EXT" "$UE_PORT" >> "$RESULT"
SSH=(-A -o BatchMode=yes -o IdentitiesOnly=no -o ConnectTimeout=15 -o ServerAliveInterval=10 -o ServerAliveCountMax=3 -o StrictHostKeyChecking=accept-new -o UserKnownHostsFile="$HOME/.ssh/known_hosts")

bar 28 'Waiting for SSH and frozen profile revision'; echo
ssh_wait(){ local user=$1 host=$2 port=$3 label=$4; for i in $(seq 1 36); do if ssh "${SSH[@]}" -p "$port" "$user@$host" true >/dev/null 2>&1; then echo "$label SSH=PASS"; return 0; fi; sleep 10; done; return 1; }
ssh_wait "$CORE_USER" "$CORE_EXT" "$CORE_PORT" CORE || fail CORE_SSH 9
ssh_wait "$UE_USER" "$UE_EXT" "$UE_PORT" UE || fail UE_SSH 9
for spec in "core:$CORE_USER:$CORE_EXT:$CORE_PORT" "ue:$UE_USER:$UE_EXT:$UE_PORT"; do
  IFS=: read -r role user host port <<< "$spec"
  ssh "${SSH[@]}" -p "$port" "$user@$host" 'set -eu; test -x /local/repository/bin/start.sh; test -d /proj/WellPulse && test -w /proj/WellPulse; echo "PROFILE_REPO_SHA=$(git -C /local/repository rev-parse HEAD)"' | tee "$TMP/${role}-profile.txt"
  grep -q "^PROFILE_REPO_SHA=$EXPECTED_PROFILE_REVISION$" "$TMP/${role}-profile.txt" || fail "PROFILE_REVISION_$role" 9
done

bar 34 'Copying exact authorized source checkout to both nodes'; echo
rm -rf "$TMP/repo-copy"
git clone --no-hardlinks . "$TMP/repo-copy" >/dev/null 2>&1 || fail LOCAL_REPO_CLONE 10
git -C "$TMP/repo-copy" checkout -q --detach "$SOURCE_SHA" || fail SOURCE_SHA_CHECKOUT 10
git -C "$TMP/repo-copy" config --local --unset-all http.https://github.com/.extraheader >/dev/null 2>&1 || true
[[ "$(git -C "$TMP/repo-copy" rev-parse HEAD)" == "$SOURCE_SHA" ]] || fail SOURCE_SHA_MISMATCH 10
tar -C "$TMP/repo-copy" -czf "$TMP/wellpulse-repo.tgz" .
copy_repo(){ local user=$1 host=$2 port=$3; scp "${SSH[@]}" -P "$port" "$TMP/wellpulse-repo.tgz" "$user@$host:/tmp/wellpulse-repo.tgz" >/dev/null; ssh "${SSH[@]}" -p "$port" "$user@$host" 'rm -rf "$HOME/WellPulse"; mkdir -p "$HOME/WellPulse"; tar -xzf /tmp/wellpulse-repo.tgz -C "$HOME/WellPulse"; rm -f /tmp/wellpulse-repo.tgz'; }
copy_repo "$CORE_USER" "$CORE_EXT" "$CORE_PORT" || fail COPY_CORE_REPO 10
copy_repo "$UE_USER" "$UE_EXT" "$UE_PORT" || fail COPY_UE_REPO 10

bar 40 'Bootstrapping pinned Python, MQTT and Java runtimes'; echo
CORE_SYS='sudo apt-get update -qq && sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq mosquitto mosquitto-clients rsync tmux curl unzip openssl >/dev/null'
UE_SYS='sudo apt-get update -qq && sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq mosquitto-clients rsync tmux curl unzip openssl default-jdk-headless >/dev/null'
ssh "${SSH[@]}" -p "$CORE_PORT" "$CORE_USER@$CORE_EXT" "$CORE_SYS" || fail CORE_SYSTEM_BOOTSTRAP 11
ssh "${SSH[@]}" -p "$UE_PORT" "$UE_USER@$UE_EXT" "$UE_SYS" || fail UE_SYSTEM_BOOTSTRAP 11
ssh "${SSH[@]}" -p "$CORE_PORT" "$CORE_USER@$CORE_EXT" 'cd "$HOME/WellPulse" && WP_REPO_ROOT="$HOME/WellPulse" bash scripts/wp2_a3_runtime_bootstrap.sh' > "$TMP/core-runtime-bootstrap.txt" || fail CORE_RUNTIME_BOOTSTRAP 11
ssh "${SSH[@]}" -p "$UE_PORT" "$UE_USER@$UE_EXT" 'cd "$HOME/WellPulse" && WP_REPO_ROOT="$HOME/WellPulse" bash scripts/wp2_a3_runtime_bootstrap.sh' > "$TMP/ue-runtime-bootstrap.txt" || fail UE_RUNTIME_BOOTSTRAP 11
grep -q '^A3_RUNTIME_BOOTSTRAP=PASS$' "$TMP/core-runtime-bootstrap.txt" || fail CORE_RUNTIME_CONTRACT 11
grep -q '^A3_RUNTIME_BOOTSTRAP=PASS$' "$TMP/ue-runtime-bootstrap.txt" || fail UE_RUNTIME_CONTRACT 11

bar 47 'Establishing clean initial Q0 LTE path'; echo
ssh "${SSH[@]}" -p "$UE_PORT" "$UE_USER@$UE_EXT" 'set -u; for s in ue srs-ue; do tmux kill-session -t "$s" >/dev/null 2>&1 || true; done; sudo killall srsue >/dev/null 2>&1 || true; sudo ip link del tun_srsue >/dev/null 2>&1 || true; for id in 1 33 2 34; do /usr/local/etc/emulab/tmcc attenuator "$id" 0; done; sleep 2' || fail PRE_Q0_UE_CLEAN 12
ssh "${SSH[@]}" -p "$CORE_PORT" "$CORE_USER@$CORE_EXT" 'set -u; for s in enb srs-epc srs-enb; do tmux kill-session -t "$s" >/dev/null 2>&1 || true; done; sudo killall srsenb srsepc >/dev/null 2>&1 || true; sleep 2; cd /local/repository; set +e; bash bin/start.sh > /tmp/wp2-p7b-q0-core.console 2>&1; exit 0' || fail PRE_Q0_CORE_START 12
CORE_READY=0
for i in $(seq 1 45); do if ssh "${SSH[@]}" -p "$CORE_PORT" "$CORE_USER@$CORE_EXT" 'pgrep -x srsepc >/dev/null && pgrep -x srsenb >/dev/null'; then CORE_READY=1; break; fi; sleep 2; done
[[ "$CORE_READY" -eq 1 ]] || fail PRE_Q0_CORE_NOT_READY 12
sleep 10
ssh "${SSH[@]}" -p "$CORE_PORT" "$CORE_USER@$CORE_EXT" 'pgrep -x srsepc >/dev/null && pgrep -x srsenb >/dev/null' || fail PRE_Q0_CORE_NOT_STABLE 12
ssh "${SSH[@]}" -p "$UE_PORT" "$UE_USER@$UE_EXT" 'cd /local/repository; set +e; bash bin/start.sh > /tmp/wp2-p7b-q0-ue.console 2>&1; exit 0' || fail PRE_Q0_UE_START 12
UE_READY=0
for i in $(seq 1 60); do if ssh "${SSH[@]}" -p "$UE_PORT" "$UE_USER@$UE_EXT" 'pgrep -x srsue >/dev/null && ip link show tun_srsue >/dev/null 2>&1 && ip -4 addr show dev tun_srsue | grep -q "inet "'; then UE_READY=1; break; fi; sleep 2; done
[[ "$UE_READY" -eq 1 ]] || fail PRE_Q0_UE_NOT_READY 12
ssh "${SSH[@]}" -p "$UE_PORT" "$UE_USER@$UE_EXT" 'set -eu; ip route get 172.16.0.1 | grep -q tun_srsue; ping -I tun_srsue -c 5 -W 2 172.16.0.1 | tee /tmp/wp2-p7b-q0-ping.txt; grep -q "0% packet loss" /tmp/wp2-p7b-q0-ping.txt' || fail PRE_Q0_USER_PLANE 12

bar 54 'Executing exactly B1 -> W1 -> B2 non-scored qualification cells'; echo
RUN_ID="wp2-p7b-c-${GITHUB_RUN_ID:-manual}-$(date -u +%Y%m%dT%H%M%SZ)"
printf 'RUN_ID=%s\n' "$RUN_ID" | tee -a "$RESULT"
set +e
ssh "${SSH[@]}" -p "$UE_PORT" "$UE_USER@$UE_EXT" \
  "cd \"\$HOME/WellPulse\" && WP_RUN_ID='$RUN_ID' WP_EXPERIMENT_ID='$EXPID' WP_CORE_HOST='enb1' WP_UE_HOST='rue1' WP_REMOTE_USER='aayoub' WP_REPO_ROOT=\"\$HOME/WellPulse\" WP_PYTHON=\"\$HOME/.wp2-golden-venv/bin/python\" WP_HARD_EXPIRY_UTC='$EXPIRES' WP_CORE_MANAGEMENT_HOST='$CORE_EXT' WP_UE_MANAGEMENT_HOST='$UE_EXT' \"\$HOME/.wp2-golden-venv/bin/python\" scripts/wp2_p7b_c_node.py" \
  2>&1 | tee "$TMP/p7b-c-console.txt"
NODE_RC=${PIPESTATUS[0]}
set -e
printf 'NODE_RC=%s\nUE_EVIDENCE_ROOT=%s\nCORE_EVIDENCE_ROOT=%s\n' "$NODE_RC" "$HOME/wellpulse-powder-evidence/p7b/$RUN_ID" "$HOME/wellpulse-powder-evidence/p7b/$RUN_ID-core" >> "$RESULT"

bar 92 'Pulling sanitized P7B-C status only; raw evidence remains on nodes'; echo
REMOTE_STATUS="\$HOME/wellpulse-powder-evidence/p7b/$RUN_ID/p7b_c_status.json"
set +e
scp "${SSH[@]}" -P "$UE_PORT" "$UE_USER@$UE_EXT:$REMOTE_STATUS" "$TMP/p7b_c_status.json" >/dev/null 2>"$TMP/status-scp.err"
STATUS_SCP_RC=$?
set -e
printf 'STATUS_SCP_RC=%s\n' "$STATUS_SCP_RC" >> "$RESULT"
if [[ "$STATUS_SCP_RC" -eq 0 ]]; then
  GATE="$(jq -r '.gate // "UNKNOWN"' "$TMP/p7b_c_status.json")"
  FAILURE="$(jq -r '.failure // ""' "$TMP/p7b_c_status.json")"
  printf 'P7B_C_GATE=%s\nP7B_C_FAILURE=%s\n' "$GATE" "$FAILURE" >> "$RESULT"
else
  GATE="STATUS_UNAVAILABLE"
fi

bar 100 'P7B-C execution stopped before evidence-survival/teardown patch'; echo
printf 'EXPERIMENT_LEFT_LIVE=%s\nP7B_D=NOT_STARTED\nTEARDOWN_AUTHORIZED=NO\nSCORED_AUTHORIZATION=BLOCKED\n' "$EXPID" | tee -a "$RESULT"
printf 'RESULT_ENV=%s\n' "$RESULT"
if [[ "$NODE_RC" -ne 0 ]]; then
  echo "WP2_P7B_C_EXECUTE=BLOCKED_NODE_RC_$NODE_RC"
  exit "$NODE_RC"
fi
[[ "$GATE" == "PASS_PHYSICAL_CELLS" ]] || fail "P7B_C_GATE_$GATE" 71
echo 'WP2_P7B_C_EXECUTE=PASS_PHYSICAL_CELLS'
exit 0
