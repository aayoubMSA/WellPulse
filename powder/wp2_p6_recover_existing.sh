#!/usr/bin/env bash
set -euo pipefail

EXPID="${WP_P6_EXPERIMENT_ID:?WP_P6_EXPERIMENT_ID is required}"
SOURCE_SHA="${WP_P6_SOURCE_SHA:?WP_P6_SOURCE_SHA is required}"
TMP="/tmp/wp2-p6-recover"
RESULT="$TMP/result.env"
mkdir -p "$TMP" "$TMP/controller" "$TMP/upload"
: > "$RESULT"

PORTAL_HTTP="${PORTAL_HTTP:-https://boss.emulab.net:43794}"
PORTAL_TOKEN="${PORTAL_TOKEN:-}"
POWDER_USERNAME="${POWDER_USERNAME:-aayoub}"
POWDER_SSH_PRIVATE_KEY="${POWDER_SSH_PRIVATE_KEY:-}"
POWDER_SSH_KEY_PASSPHRASE="${POWDER_SSH_KEY_PASSPHRASE:-}"
EXPECTED_PROFILE_REVISION="a6da96560b6526dc6816761282722c996418fd8c"
EXPECTED_HARDWARE="nuc5300"
EXPECTED_IMAGE="urn:publicid:IDN+emulab.net+image+PowderProfiles:U18LL-SRSLTE:1"
SSH_AGENT_STARTED=0
ORCHESTRATOR_INVOKED=0
G3_REACHED=0
RECOVERY_PHASE_COMPLETE=0
RUN_ID=""

export PORTAL_HTTP PORTAL_TOKEN

bar(){ local p="$1" m="$2" n; n=$((p/5)); printf '\r['; printf '%*s' "$n" ''|tr ' ' '#'; printf '%*s' "$((20-n))" ''|tr ' ' '-'; printf '] %3d%%  %-58s' "$p" "$m"; }
utc(){ date -u +%Y-%m-%dT%H:%M:%SZ; }
fail(){ echo; echo "WP2_P6_RECOVER=FAIL:$1" >&2; exit "${2:-90}"; }

terminate_exact(){
  local id="$1"
  set +e
  portal-cli experiment terminate --experiment-id "$id" > "$TMP/terminate-early.json" 2>"$TMP/terminate-early.err"
  for _ in $(seq 1 45); do
    portal-cli experiment get --experiment-id "$id" > "$TMP/postterm-early.json" 2>/dev/null
    rc=$?
    if [[ "$rc" -ne 0 ]]; then set -e; return 0; fi
    st="$(jq -r '.status // "unknown"' "$TMP/postterm-early.json" 2>/dev/null)"
    [[ "$st" =~ ^(terminated|destroyed)$ ]] && { set -e; return 0; }
    sleep 4
  done
  set -e
  return 1
}

on_exit(){
  local rc=$?
  set +e
  if [[ "$SSH_AGENT_STARTED" -eq 1 ]]; then ssh-agent -k >/dev/null 2>&1 || true; fi
  if [[ "$rc" -ne 0 && "$RECOVERY_PHASE_COMPLETE" -ne 1 ]]; then
    if [[ "$ORCHESTRATOR_INVOKED" -eq 0 || "$G3_REACHED" -eq 0 ]]; then
      echo 'P6_RECOVERY_FAILURE_CLASS=PRE_SCIENCE'
      if terminate_exact "$EXPID"; then
        echo 'P6_RECOVERY_PRE_SCIENCE_CLEANUP=TERMINATED'
      else
        echo 'P6_RECOVERY_PRE_SCIENCE_CLEANUP=NOT_CONFIRMED'
      fi
    else
      echo 'P6_RECOVERY_FAILURE_CLASS=POST_G3_PROTECTED_SCIENCE'
      echo "EXPERIMENT_LEFT_LIVE=$EXPID"
      echo 'AUTOMATIC_TERMINATION=PROHIBITED'
      echo 'TEARDOWN_AUTHORIZED=NO'
    fi
  fi
  rm -f "$TMP/private.key" "$TMP/askpass"
  exit "$rc"
}
trap on_exit EXIT

[[ -n "$PORTAL_TOKEN" ]] || fail POWDER_API_TOKEN_MISSING 2
[[ -n "$POWDER_SSH_PRIVATE_KEY" ]] || fail POWDER_SSH_PRIVATE_KEY_MISSING 2

bar 5 'Installing pinned Portal client and SSH identity'; echo
bash scripts/wp2_portal_client_bootstrap.sh /tmp/portal-api-recover | tee "$TMP/portal-pin.txt"
grep -q '^PORTAL_API_PIN_GATE=PASS$' "$TMP/portal-pin.txt" || fail PORTAL_PIN 3
umask 077
mkdir -p "$HOME/.ssh"
python3 - <<'PY'
import os
from pathlib import Path
raw=os.environ['POWDER_SSH_PRIVATE_KEY'].replace('\r\n','\n').replace('\r','\n').lstrip('\ufeff').strip()+"\n"
Path('/tmp/wp2-p6-recover/private.key').write_text(raw,encoding='utf-8',newline='\n')
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
: > "$HOME/.ssh/known_hosts"
chmod 600 "$HOME/.ssh/known_hosts"

bar 12 'Rebinding exact existing reservation and time gate'; echo
portal-cli experiment get --experiment-id "$EXPID" > "$TMP/status.json" || fail EXPERIMENT_NOT_FOUND 4
STATUS="$(jq -r '.status // "unknown"' "$TMP/status.json")"
[[ "$STATUS" == ready ]] || fail "EXPERIMENT_NOT_READY_$STATUS" 4
python3 scripts/wp2_portal_record_guard.py --json "$TMP/status.json" --expected-experiment-id "$EXPID" | tee "$TMP/portal-record.txt"
grep -q '^PORTAL_RECORD_GATE=PASS$' "$TMP/portal-record.txt" || fail PORTAL_RECORD_GATE 4
EXPIRES="$(awk -F= '$1=="EXPIRES_UTC" {print $2}' "$TMP/portal-record.txt" | tail -1)"
python3 scripts/wp2_prelaunch_time_guard.py --now-utc "$(utc)" --expires-utc "$EXPIRES" --min-remaining-s 2700 | tee "$TMP/time-gate.txt"
grep -q '^PRELAUNCH_TIME_GATE=PASS$' "$TMP/time-gate.txt" || fail RECOVERY_TIME_GATE 4
[[ "$(jq -r '.bindings.enb_node // empty' "$TMP/status.json")" == nuc1 ]] || fail BINDING_ENB 4
[[ "$(jq -r '.bindings.ue_node // empty' "$TMP/status.json")" == nuc2 ]] || fail BINDING_UE 4
[[ "$(jq -r '.bindings.ue_type // empty' "$TMP/status.json")" == srsue ]] || fail BINDING_UE_TYPE 4
printf 'EXPERIMENT_ID=%s\nHARD_EXPIRY_UTC=%s\nSOURCE_SHA=%s\n' "$EXPID" "$EXPIRES" "$SOURCE_SHA" | tee -a "$RESULT"

bar 20 'Refreezing exact manifest identity and login endpoints'; echo
portal-cli experiment manifests get --experiment-id "$EXPID" > "$TMP/manifests.json" || fail MANIFEST_FETCH 5
python3 - "$TMP/manifests.json" "$TMP/nodes.json" "$EXPECTED_HARDWARE" "$EXPECTED_IMAGE" <<'PY'
import json,sys,xml.etree.ElementTree as ET
obj=json.load(open(sys.argv[1])); out={}; xmls=[]
expected_hw,expected_img=sys.argv[3],sys.argv[4]
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
        if node.tag.rsplit('}',1)[-1] != 'node': continue
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
    r=out.get(cid) or {}
    assert r.get('login'), f'missing login {cid}'
    assert r.get('hardware_type')==expected_hw, (cid,r.get('hardware_type'))
    assert r.get('disk_image')==expected_img, (cid,r.get('disk_image'))
    assert r.get('component_id','').endswith('+'+node), (cid,r.get('component_id'))
    assert int(r['login']['port'])==22, (cid,'non-22 login port',r['login']['port'])
json.dump(out,open(sys.argv[2],'w'),indent=2,sort_keys=True)
print('P6_RECOVERY_MANIFEST_IDENTITY=PASS')
PY
get_login(){ jq -r --arg n "$1" '.[$n].login | [.username,.hostname,(.port|tostring)] | @tsv' "$TMP/nodes.json"; }
IFS=$'\t' read -r CORE_USER CORE_EXT CORE_PORT < <(get_login enb1)
IFS=$'\t' read -r UE_USER UE_EXT UE_PORT < <(get_login rue1)
CORE_USER="${CORE_USER:-$POWDER_USERNAME}"; UE_USER="${UE_USER:-$POWDER_USERNAME}"
SSH=(-A -o BatchMode=yes -o IdentitiesOnly=no -o ConnectTimeout=15 -o ServerAliveInterval=10 -o ServerAliveCountMax=3 -o StrictHostKeyChecking=accept-new -o UserKnownHostsFile="$HOME/.ssh/known_hosts")
ssh "${SSH[@]}" -p "$CORE_PORT" "$CORE_USER@$CORE_EXT" 'true' || fail CORE_CONTROLLER_SSH 5
ssh "${SSH[@]}" -p "$UE_PORT" "$UE_USER@$UE_EXT" 'true' || fail UE_CONTROLLER_SSH 5

bar 30 'Repairing and proving internal management aliases from UE'; echo
CORE_IP="$(ssh "${SSH[@]}" -p "$UE_PORT" "$UE_USER@$UE_EXT" "getent ahostsv4 '$CORE_EXT' | awk 'NR==1{print \$1}'")"
UE_IP="$(ssh "${SSH[@]}" -p "$UE_PORT" "$UE_USER@$UE_EXT" "getent ahostsv4 '$UE_EXT' | awk 'NR==1{print \$1}'")"
[[ "$CORE_IP" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]] || fail CORE_EXTERNAL_IP_RESOLUTION 6
[[ "$UE_IP" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]] || fail UE_EXTERNAL_IP_RESOLUTION 6
ssh "${SSH[@]}" -p "$UE_PORT" "$UE_USER@$UE_EXT" "set -eu
  sudo sed -i -E '/[[:space:]]enb1([[:space:]]|$)/d; /[[:space:]]rue1([[:space:]]|$)/d' /etc/hosts
  printf '%s enb1\\n%s rue1\\n' '$CORE_IP' '$UE_IP' | sudo tee -a /etc/hosts >/dev/null
  getent hosts enb1
  getent hosts rue1
  ssh -o BatchMode=yes -o ConnectTimeout=10 -o StrictHostKeyChecking=accept-new '$CORE_USER'@enb1 'echo P6_UE_TO_CORE_ALIAS_SSH=PASS'
  ssh -o BatchMode=yes -o ConnectTimeout=10 -o StrictHostKeyChecking=accept-new '$UE_USER'@rue1 'echo P6_UE_TO_UE_ALIAS_SSH=PASS'" | tee "$TMP/alias-gate.txt" || fail INTERNAL_ALIAS_SSH_GATE 6
grep -q '^P6_UE_TO_CORE_ALIAS_SSH=PASS$' "$TMP/alias-gate.txt" || fail CORE_ALIAS_NOT_PROVEN 6
grep -q '^P6_UE_TO_UE_ALIAS_SSH=PASS$' "$TMP/alias-gate.txt" || fail UE_ALIAS_NOT_PROVEN 6
echo 'P6_INTERNAL_MANAGEMENT_ALIAS_GATE=PASS'

bar 38 'Verifying exact node source/profile state'; echo
for spec in "core:$CORE_USER:$CORE_EXT:$CORE_PORT" "ue:$UE_USER:$UE_EXT:$UE_PORT"; do
  IFS=: read -r role user host port <<< "$spec"
  ssh "${SSH[@]}" -p "$port" "$user@$host" "set -eu
    [[ \$(git -C \"\$HOME/WellPulse\" rev-parse HEAD) == '$SOURCE_SHA' ]]
    [[ \$(git -C /local/repository rev-parse HEAD) == '$EXPECTED_PROFILE_REVISION' ]]
    test -d /proj/WellPulse && test -w /proj/WellPulse
    test -x \"\$HOME/.wp2-golden-venv/bin/python\"
    \"\$HOME/.wp2-golden-venv/bin/python\" -c 'import importlib.metadata; assert importlib.metadata.version(\"paho-mqtt\")==\"2.1.0\"'
    echo P6_${role^^}_STATE_GATE=PASS" | tee "$TMP/${role}-state.txt" || fail "${role}_STATE_GATE" 7
done

bar 45 'Re-establishing clean Q0 pre-science gate'; echo
ssh "${SSH[@]}" -p "$UE_PORT" "$UE_USER@$UE_EXT" "set -eu
  for id in 1 33 2 34; do /usr/local/etc/emulab/tmcc attenuator \"\$id\" 0 >/dev/null; done
  pgrep -x srsue >/dev/null
  ip -4 addr show dev tun_srsue | grep -q 'inet '
  ip route get 172.16.0.1 | grep -q tun_srsue
  ping -I tun_srsue -c 5 -W 2 172.16.0.1 | tee /tmp/wp2-p6-recovery-q0-ping.txt
  grep -Eq '5 packets transmitted, 5 received|5 packets transmitted, 5 packets received' /tmp/wp2-p6-recovery-q0-ping.txt" || fail RECOVERY_Q0_USER_PLANE 8
ssh "${SSH[@]}" -p "$CORE_PORT" "$CORE_USER@$CORE_EXT" 'pgrep -x srsepc >/dev/null && pgrep -x srsenb >/dev/null' || fail RECOVERY_CORE_RAN_NOT_READY 8
echo 'P6_RECOVERY_PRE_SCIENCE_Q0=PASS'

bar 52 'Launching first scientifically valid P6 Golden attempt'; echo
RUN_ID="wp2-p6r-${GITHUB_RUN_ID:-manual}-$(date -u +%Y%m%dT%H%M%SZ)"
printf 'RUN_ID=%s\nCORE_EXT=%s\nUE_EXT=%s\n' "$RUN_ID" "$CORE_EXT" "$UE_EXT" | tee -a "$RESULT"
ORCHESTRATOR_INVOKED=1
set +e
ssh "${SSH[@]}" -p "$UE_PORT" "$UE_USER@$UE_EXT" \
  "cd \"\$HOME/WellPulse\" && WP_RUN_ID='$RUN_ID' WP_EXPERIMENT_ID='$EXPID' WP_CORE_HOST='enb1' WP_UE_HOST='rue1' WP_REMOTE_USER='aayoub' WP_REPO_ROOT=\"\$HOME/WellPulse\" WP_PYTHON=\"\$HOME/.wp2-golden-venv/bin/python\" WP_HARD_EXPIRY_UTC='$EXPIRES' WP_PERSIST_ROOT='/proj/WellPulse/evidence-escrow' bash scripts/wp2_golden_orchestrator.sh" \
  2>&1 | tee "$TMP/golden-console.txt"
GOLDEN_RC=${PIPESTATUS[0]}
set -e
if grep -q '"gate":"G3".*"status":"PASS"' "$TMP/golden-console.txt"; then G3_REACHED=1; fi
[[ "$GOLDEN_RC" -eq 0 ]] || fail "GOLDEN_NODE_RC_$GOLDEN_RC" 70
grep -q '^GOLDEN_NODE_PHASE=PASS_PERSISTENT_ESCROW$' "$TMP/golden-console.txt" || fail GOLDEN_NODE_PHASE 70
grep -q '^RAW_EVIDENCE_COMPLETE=PASS$' "$TMP/golden-console.txt" || fail RAW_EVIDENCE_COMPLETE 70
grep -q '^TEARDOWN_AUTHORIZED=NO$' "$TMP/golden-console.txt" || fail NODE_TEARDOWN_INTERLOCK 70
PDIR="$(awk -F= '$1=="PERSISTENT_EVIDENCE" {print $2}' "$TMP/golden-console.txt" | tail -1)"
EXPECTED_PDIR="/proj/WellPulse/evidence-escrow/$EXPID/$RUN_ID"
[[ "$PDIR" == "$EXPECTED_PDIR" ]] || fail PERSISTENT_PATH 70
printf 'PERSISTENT_DIR=%s\n' "$PDIR" | tee -a "$RESULT"

bar 84 'Pulling verified persistent escrow to controller'; echo
BUNDLE="$TMP/upload/wp2-p6-recovery-$RUN_ID.tar"
WP_PERSIST_HOST="$UE_EXT" WP_REMOTE_USER="$UE_USER" WP_SSH_PORT="$UE_PORT" \
WP_PERSIST_REMOTE_DIR="$PDIR" WP_CONTROLLER_LOCAL_DIR="$TMP/controller/$RUN_ID" \
WP_CONTROLLER_BUNDLE_OUT="$BUNDLE" WP_KNOWN_HOSTS_FILE="$HOME/.ssh/known_hosts" \
bash scripts/wp2_controller_pull_persistent_escrow.sh | tee "$TMP/controller-pull.txt" || fail CONTROLLER_PULL 71
grep -q '^CONTROLLER_PULL_GATE=PASS$' "$TMP/controller-pull.txt" || fail CONTROLLER_PULL_GATE 71
BUNDLE_SHA="$(awk -F= '$1=="CONTROLLER_BUNDLE_SHA256" {print $2}' "$TMP/controller-pull.txt" | tail -1)"
[[ "$BUNDLE_SHA" =~ ^[0-9a-f]{64}$ ]] || fail BUNDLE_SHA 71
[[ -s "$BUNDLE" ]] || fail BUNDLE_MISSING 71
printf 'BUNDLE_PATH=%s\nBUNDLE_SHA256=%s\n' "$BUNDLE" "$BUNDLE_SHA" | tee -a "$RESULT"

bar 92 'Recovery node/controller phase PASS; artifact finalization required'; echo
RECOVERY_PHASE_COMPLETE=1
printf 'P6_RECOVERY_EXECUTE_PHASE=PASS\n'
printf 'EVIDENCE_ESCROW_GATE=PENDING_ARTIFACT_ROUNDTRIP\n'
printf 'TEARDOWN_AUTHORIZED=NO\n'
