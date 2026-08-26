#!/usr/bin/env bash
set -euo pipefail

REQUEST="${1:?request JSON required}"
TMP="/tmp/wp2-golden-owner"
mkdir -p "$TMP" evidence/powder

PORTAL_HTTP="${PORTAL_HTTP:-https://boss.emulab.net:43794}"
PORTAL_TOKEN="${PORTAL_TOKEN:?POWDER_API_TOKEN/PORTAL_TOKEN is required}"
POWDER_USERNAME="${POWDER_USERNAME:-aayoub}"
POWDER_SSH_PRIVATE_KEY="${POWDER_SSH_PRIVATE_KEY:?POWDER_SSH_PRIVATE_KEY is required}"
POWDER_SSH_KEY_PASSPHRASE="${POWDER_SSH_KEY_PASSPHRASE:-}"
RCLONE_CONFIG_B64="${RCLONE_CONFIG_B64:?WP_RCLONE_CONFIG_B64 is required before experiment creation}"
EXPECTED_KEY_FP="${WP_EXPECTED_KEY_FP:-SHA256:jQGQvU86rtuEchT50N1HuB4Cmizpvbmp0zSBR4rowxY}"
PROFILE_PROJECT="PowderProfiles"
PROFILE_NAME="srslte-controlled-rf"
BINDINGS='{"enb_node":"nuc1","ue_node":"nuc2","ue_type":"srsue"}'

bar(){ local p="$1" m="$2" n=$((p/5)); printf '\r['; printf '%*s' "$n" ''|tr ' ' '#'; printf '%*s' "$((20-n))" ''|tr ' ' '-'; printf '] %3d%%  %-58s' "$p" "$m"; }
fail(){ echo; echo "WP2_GOLDEN_OWNER=FAIL:$1" >&2; exit "${2:-90}"; }
utc(){ date -u +%Y-%m-%dT%H:%M:%SZ; }

[[ -f "$REQUEST" ]] || fail REQUEST_MISSING 2
EXECUTE="$(jq -r '.execute // ""' "$REQUEST")"
EXP_NAME="$(jq -r '.experiment_name // ""' "$REQUEST")"
STOP_AT="$(jq -r '.stop_at // ""' "$REQUEST")"
[[ "$EXECUTE" == "GOLDEN_E2E_NON_SCORED" ]] || fail REQUEST_NOT_AUTHORIZED 3
[[ "$EXP_NAME" =~ ^WP-GOLDEN-[A-Za-z0-9._-]+$ ]] || fail BAD_EXPERIMENT_NAME 3
[[ -n "$STOP_AT" ]] || fail STOP_AT_MISSING 3

# Secrets are validated before any Portal mutation.
bar 3 'Validating GitHub-held credentials before mutation'; echo
[[ -n "$PORTAL_TOKEN" && -n "$POWDER_SSH_PRIVATE_KEY" && -n "$RCLONE_CONFIG_B64" ]] || fail REQUIRED_SECRET_MISSING 4

rm -rf /tmp/portal-api "$TMP/ssh"
mkdir -p "$TMP/ssh" "$HOME/.ssh"
chmod 700 "$HOME/.ssh"
umask 077
python3 - <<'PY'
import os
from pathlib import Path
raw=os.environ['POWDER_SSH_PRIVATE_KEY'].replace('\\r\\n','\n').replace('\\r','\n').lstrip('\ufeff').strip()+"\n"
p=Path.home()/'.ssh'/'id_ed25519_powder'
p.write_text(raw,encoding='utf-8',newline='\n')
PY
chmod 600 "$HOME/.ssh/id_ed25519_powder"
cat > "$TMP/askpass" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' "$POWDER_SSH_KEY_PASSPHRASE"
EOF
chmod 700 "$TMP/askpass"
export SSH_ASKPASS="$TMP/askpass" SSH_ASKPASS_REQUIRE=force DISPLAY=:0
setsid -w ssh-keygen -y -f "$HOME/.ssh/id_ed25519_powder" > "$TMP/public.key" </dev/null
ACTUAL_FP="$(ssh-keygen -lf "$TMP/public.key" | awk '{print $2}')"
[[ "$ACTUAL_FP" == "$EXPECTED_KEY_FP" ]] || fail SSH_KEY_FINGERPRINT_MISMATCH 5

eval "$(ssh-agent -s)" >/dev/null
setsid -w ssh-add "$HOME/.ssh/id_ed25519_powder" </dev/null >/dev/null
trap 'ssh-agent -k >/dev/null 2>&1 || true' EXIT

bar 7 'Installing official Emulab Portal API client'; echo
git clone --depth 1 https://gitlab.flux.utah.edu/emulab/portal-api.git /tmp/portal-api >/dev/null 2>&1
python -m pip install --quiet '/tmp/portal-api[cli]'

bar 10 'Checking for conflicting active Golden experiment'; echo
portal-cli experiment list > "$TMP/list-before.json"
python3 - "$TMP/list-before.json" "$EXP_NAME" <<'PY'
import json,sys
raw=json.load(open(sys.argv[1]))
xs=raw if isinstance(raw,list) else raw.get('experiments',[])
terminal={'terminated','destroyed','failed','error'}
active=[]
for x in xs:
    if not isinstance(x,dict) or x.get('project')!='WellPulse': continue
    name=str(x.get('name','')); st=str(x.get('status','')).lower()
    if (name==sys.argv[2] or name.startswith('WP-GOLDEN-')) and st not in terminal:
        active.append({'id':x.get('id'),'name':name,'status':st})
if active:
    print('ACTIVE_GOLDEN_CONFLICT',active)
    raise SystemExit(20)
print('ACTIVE_GOLDEN_CONFLICT=NONE')
PY

bar 14 'Creating exactly one reserved non-scored experiment'; echo
PUB="$(cat "$TMP/public.key")"
portal-cli experiment create \
  --name "$EXP_NAME" \
  --project WellPulse \
  --profile-name "$PROFILE_NAME" \
  --profile-project "$PROFILE_PROJECT" \
  --stop-at "$STOP_AT" \
  --bindings "$BINDINGS" \
  --sshpubkey "$PUB" > "$TMP/create.json"
EXPID="$(jq -r '.id // empty' "$TMP/create.json")"
[[ "$EXPID" =~ ^[0-9A-Fa-f-]{36}$ ]] || fail CREATE_RETURNED_NO_UUID 21
echo "$EXPID" > "$TMP/experiment-id"
echo "EXPERIMENT_ID=$EXPID"

# After mutation, every failure is fail-closed with no automatic termination unless
# the Golden run later proves dual verified escrow and emits TEARDOWN_AUTHORIZED=YES.
leave_live(){
  local rc=$?
  set +e
  echo "OWNER_FAIL_CLOSED=1"
  echo "EXPERIMENT_LEFT_LIVE=$EXPID"
  echo "AUTOMATIC_TERMINATION=PROHIBITED"
  write_summary "$rc" "FAIL_CLOSED_LEFT_LIVE"
  exit "$rc"
}
trap leave_live ERR

bar 18 'Waiting for POWDER READY state'; echo
READY=0
for i in $(seq 1 120); do
  portal-cli experiment get --experiment-id "$EXPID" > "$TMP/status.json" 2>"$TMP/status.err" || true
  STATUS="$(jq -r '.status // "unknown"' "$TMP/status.json" 2>/dev/null || echo unknown)"
  printf '\rREADY_WAIT=%03d/120 STATUS=%-20s' "$i" "$STATUS"
  if [[ "$STATUS" == ready ]]; then READY=1; break; fi
  [[ "$STATUS" =~ ^(failed|error|terminated|destroyed)$ ]] && fail "PORTAL_TERMINAL_$STATUS" 22
  sleep 10
done
echo
[[ "$READY" -eq 1 ]] || fail READY_TIMEOUT 23

bar 25 'Retrieving manifests and exact node login endpoints'; echo
portal-cli experiment manifests get --experiment-id "$EXPID" > "$TMP/manifests.json"
python3 - "$TMP/manifests.json" "$TMP/nodes.json" <<'PY'
import json,sys,xml.etree.ElementTree as ET
obj=json.load(open(sys.argv[1]))
xmls=[]
def walk(x):
    if isinstance(x,dict):
        for v in x.values(): walk(v)
    elif isinstance(x,list):
        for v in x: walk(v)
    elif isinstance(x,str) and '<' in x and 'rspec' in x.lower(): xmls.append(x)
walk(obj)
out={}
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
json.dump(out,open(sys.argv[2],'w'),indent=2,sort_keys=True)
missing=[x for x in ('enb1','rue1') if x not in out or 'login' not in out[x]]
if missing: raise SystemExit('Missing login endpoints: '+','.join(missing))
PY
cat "$TMP/nodes.json" | jq '{enb1:{client_id:.enb1.client_id,hardware_type:.enb1.hardware_type},rue1:{client_id:.rue1.client_id,hardware_type:.rue1.hardware_type}}'

get_login(){ jq -r --arg n "$1" '.[$n].login | [.username,.hostname,(.port|tostring)] | @tsv' "$TMP/nodes.json"; }
IFS=$'\t' read -r CORE_USER CORE_EXT CORE_PORT < <(get_login enb1)
IFS=$'\t' read -r UE_USER UE_EXT UE_PORT < <(get_login rue1)
CORE_USER="${CORE_USER:-$POWDER_USERNAME}"; UE_USER="${UE_USER:-$POWDER_USERNAME}"
SSH_COMMON=(-o BatchMode=yes -o IdentitiesOnly=no -o ConnectTimeout=15 -o ServerAliveInterval=10 -o ServerAliveCountMax=3 -o StrictHostKeyChecking=accept-new)

bar 30 'Waiting for SSH on both reserved NUCs'; echo
ssh_wait(){ local user=$1 host=$2 port=$3 label=$4; for i in $(seq 1 36); do if ssh -A "${SSH_COMMON[@]}" -p "$port" "$user@$host" 'true' >/dev/null 2>&1; then echo "$label SSH=PASS"; return 0; fi; printf '\r%s_SSH_WAIT=%02d/36' "$label" "$i"; sleep 10; done; echo; return 1; }
ssh_wait "$CORE_USER" "$CORE_EXT" "$CORE_PORT" CORE
ssh_wait "$UE_USER" "$UE_EXT" "$UE_PORT" UE

bar 34 'Packaging exact GitHub checkout for both nodes'; echo
GIT_SHA="$(git rev-parse HEAD)"
tar -czf "$TMP/wellpulse-repo.tgz" --exclude='./.git/objects/pack/*.pack' .

copy_repo(){
  local user=$1 host=$2 port=$3
  scp "${SSH_COMMON[@]}" -P "$port" "$TMP/wellpulse-repo.tgz" "$user@$host:/tmp/wellpulse-repo.tgz" >/dev/null
  ssh -A "${SSH_COMMON[@]}" -p "$port" "$user@$host" 'rm -rf "$HOME/WellPulse"; mkdir -p "$HOME/WellPulse"; tar -xzf /tmp/wellpulse-repo.tgz -C "$HOME/WellPulse"; rm -f /tmp/wellpulse-repo.tgz'
}
copy_repo "$CORE_USER" "$CORE_EXT" "$CORE_PORT"
copy_repo "$UE_USER" "$UE_EXT" "$UE_PORT"

bar 39 'Bootstrapping deterministic runtime dependencies'; echo
CORE_BOOT='sudo apt-get update -qq && sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq mosquitto rsync tmux python3-pip openssl >/dev/null && python3 -m pip install --user --quiet paho-mqtt'
UE_BOOT='sudo apt-get update -qq && sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq rsync tmux python3-pip openssl curl unzip >/dev/null && python3 -m pip install --user --quiet paho-mqtt && curl -fsSL https://rclone.org/install.sh | sudo bash >/dev/null'
ssh -A "${SSH_COMMON[@]}" -p "$CORE_PORT" "$CORE_USER@$CORE_EXT" "$CORE_BOOT"
ssh -A "${SSH_COMMON[@]}" -p "$UE_PORT" "$UE_USER@$UE_EXT" "$UE_BOOT"

bar 44 'Installing Drive OAuth config without logging secret material'; echo
python3 - <<'PY'
import base64,os,pathlib
p=pathlib.Path('/tmp/wp2-golden-owner/rclone.conf')
p.write_bytes(base64.b64decode(os.environ['RCLONE_CONFIG_B64'],validate=True))
p.chmod(0o600)
PY
scp "${SSH_COMMON[@]}" -P "$UE_PORT" "$TMP/rclone.conf" "$UE_USER@$UE_EXT:/tmp/wp2-rclone.conf" >/dev/null
ssh -A "${SSH_COMMON[@]}" -p "$UE_PORT" "$UE_USER@$UE_EXT" 'mkdir -p "$HOME/.config/rclone"; chmod 700 "$HOME/.config/rclone"; install -m 600 /tmp/wp2-rclone.conf "$HOME/.config/rclone/rclone.conf"; rm -f /tmp/wp2-rclone.conf'
rm -f "$TMP/rclone.conf"

bar 48 'Verifying Drive and internal node-to-node SSH before science'; echo
for i in $(seq 1 5); do
  if ssh -A "${SSH_COMMON[@]}" -p "$UE_PORT" "$UE_USER@$UE_EXT" 'rclone lsf gdrive: >/dev/null 2>&1 && getent hosts enb1 >/dev/null && ssh -o BatchMode=yes -o ConnectTimeout=10 -o StrictHostKeyChecking=accept-new aayoub@enb1 true'; then
    echo "PRE_GOLDEN_REMOTE_AND_INTERNAL_SSH=PASS"; break
  fi
  [[ "$i" -eq 5 ]] && fail PRE_GOLDEN_CONNECTIVITY_FAILED 31
  sleep 15
done

RUN_ID="wp2-golden-gh-${GITHUB_RUN_ID:-manual}-$(date -u +%Y%m%dT%H%M%SZ)"
echo "$RUN_ID" > "$TMP/run-id"

bar 52 'Launching exactly one non-scored Golden E2E rehearsal'; echo
set +e
ssh -A "${SSH_COMMON[@]}" -p "$UE_PORT" "$UE_USER@$UE_EXT" \
  "cd \"\$HOME/WellPulse\" && WP_RUN_ID='$RUN_ID' WP_EXPERIMENT_ID='$EXPID' WP_CORE_HOST='enb1' WP_UE_HOST='rue1' WP_REMOTE_USER='aayoub' WP_REPO_ROOT=\"\$HOME/WellPulse\" WP_RCLONE_REMOTE_ROOT='gdrive:' bash scripts/wp2_golden_orchestrator.sh" \
  2>&1 | tee "$TMP/golden-console.txt"
GOLDEN_RC=${PIPESTATUS[0]}
set -e

TEARDOWN_OK=0
if [[ "$GOLDEN_RC" -eq 0 ]] && grep -q '^GOLDEN_E2E=PASS$' "$TMP/golden-console.txt" && grep -q '^EVIDENCE_ESCROW_GATE=PASS$' "$TMP/golden-console.txt" && grep -q '^TEARDOWN_AUTHORIZED=YES$' "$TMP/golden-console.txt"; then
  TEARDOWN_OK=1
fi

write_summary(){
  local rc="${1:-$GOLDEN_RC}" verdict="${2:-UNKNOWN}"
  local now; now="$(utc)"
  local out="evidence/powder/wp2-golden-owner-${RUN_ID:-pre-run}.md"
  cat > "$out" <<EOF
# WP2 Golden — GitHub-owned execution checkpoint

- Checked UTC: $now
- GitHub run ID: ${GITHUB_RUN_ID:-manual}
- GitHub SHA: $GIT_SHA
- Experiment ID: $EXPID
- Experiment name: $EXP_NAME
- Profile: $PROFILE_PROJECT/$PROFILE_NAME
- Bindings: enb_node=nuc1; ue_node=nuc2; ue_type=srsue
- Golden run ID: ${RUN_ID:-not_started}
- Golden exit code: $rc
- Controller verdict: **$verdict**
- Scored run: **NO**
- Credential material recorded: **NO**
- Automatic termination allowed without verified G9: **NO**
EOF
}

if [[ "$TEARDOWN_OK" -ne 1 ]]; then
  echo "GOLDEN_OWNER_VERDICT=STOP_DO_NOT_TERMINATE"
  echo "EXPERIMENT_ID=$EXPID"
  write_summary "$GOLDEN_RC" "STOP_DO_NOT_TERMINATE"
  exit 70
fi

bar 94 'G9/G10 verified: terminating experiment via Portal API'; echo
portal-cli experiment terminate --experiment-id "$EXPID" > "$TMP/terminate.json" 2>"$TMP/terminate.err" || true
TERMINATED=0
for i in $(seq 1 60); do
  set +e
  portal-cli experiment get --experiment-id "$EXPID" > "$TMP/postterm.json" 2>/dev/null
  grc=$?
  set -e
  if [[ "$grc" -ne 0 ]]; then TERMINATED=1; break; fi
  st="$(jq -r '.status // "unknown"' "$TMP/postterm.json")"
  printf '\rTERMINATION_WAIT=%02d/60 STATUS=%-18s' "$i" "$st"
  if [[ "$st" =~ ^(terminated|destroyed)$ ]]; then TERMINATED=1; break; fi
  sleep 5
done
echo
[[ "$TERMINATED" -eq 1 ]] || fail TERMINATION_NOT_CONFIRMED 72

bar 100 'GitHub-owned Golden lifecycle complete'; echo
write_summary 0 "PASS_DUAL_ESCROW_AND_TERMINATED"
echo "WP2_GOLDEN_OWNER=PASS"
echo "GOLDEN_E2E=PASS"
echo "EVIDENCE_ESCROW_GATE=PASS"
echo "TEARDOWN_CONFIRMED=YES"
