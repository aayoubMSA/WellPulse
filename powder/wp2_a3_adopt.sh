#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-PRECHECK}"
A3_ID="357f3275-403d-491a-906f-99677bdf454f"
A3_NAME="WP-GOLDEN-A3"
PORTAL_HTTP="${PORTAL_HTTP:-https://boss.emulab.net:43794}"
PORTAL_TOKEN="${PORTAL_TOKEN:-}"
POWDER_USERNAME="${POWDER_USERNAME:-aayoub}"
POWDER_SSH_PRIVATE_KEY="${POWDER_SSH_PRIVATE_KEY:-}"
POWDER_SSH_KEY_PASSPHRASE="${POWDER_SSH_KEY_PASSPHRASE:-}"
RCLONE_CONFIG_B64="${RCLONE_CONFIG_B64:-}"
TMP="/tmp/wp2-a3-adopt"
GIT_SHA="$(git rev-parse HEAD)"
SSH_AGENT_STARTED=0

export PORTAL_HTTP PORTAL_TOKEN POWDER_SSH_PRIVATE_KEY POWDER_SSH_KEY_PASSPHRASE RCLONE_CONFIG_B64

bar(){ local p="$1" m="$2" n; n=$((p/5)); printf '\r['; printf '%*s' "$n" ''|tr ' ' '#'; printf '%*s' "$((20-n))" ''|tr ' ' '-'; printf '] %3d%%  %-58s' "$p" "$m"; }
fail(){ echo; echo "WP2_A3_ADOPTION=FAIL:$1" >&2; exit "${2:-90}"; }
utc(){ date -u +%Y-%m-%dT%H:%M:%S.%NZ; }

cleanup(){
  set +e
  [[ "$SSH_AGENT_STARTED" -eq 1 ]] && ssh-agent -k >/dev/null 2>&1 || true
  rm -f "$TMP/rclone.conf" "$TMP/private.key" "$TMP/askpass"
}
trap cleanup EXIT

[[ "$MODE" == PRECHECK || "$MODE" == RUN ]] || fail BAD_MODE 2
[[ -n "$PORTAL_TOKEN" ]] || fail POWDER_API_TOKEN_MISSING 3
[[ -n "$POWDER_SSH_PRIVATE_KEY" ]] || fail POWDER_SSH_PRIVATE_KEY_MISSING 3
if [[ "$MODE" == RUN ]]; then
  [[ -n "$RCLONE_CONFIG_B64" ]] || fail RCLONE_CONFIG_MISSING 3
fi

rm -rf "$TMP"
mkdir -p "$TMP" "$HOME/.ssh" evidence/powder
chmod 700 "$TMP" "$HOME/.ssh"
umask 077

bar 4 'Preparing authenticated read path'; echo
python3 - <<'PY'
import os
from pathlib import Path
raw=os.environ['POWDER_SSH_PRIVATE_KEY'].replace('\\r\\n','\n').replace('\\r','\n').lstrip('\ufeff').strip()+"\n"
Path('/tmp/wp2-a3-adopt/private.key').write_text(raw,encoding='utf-8',newline='\n')
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

bar 8 'Loading official POWDER Portal API client'; echo
rm -rf /tmp/portal-api
command -v portal-cli >/dev/null 2>&1 || {
  git clone --depth 1 https://gitlab.flux.utah.edu/emulab/portal-api.git /tmp/portal-api >/dev/null 2>&1 || fail PORTAL_CLIENT_CLONE 5
  python3 -m pip install --quiet '/tmp/portal-api[cli]' || fail PORTAL_CLIENT_INSTALL 5
}

bar 12 'Binding exclusively to existing WP-GOLDEN-A3'; echo
portal-cli experiment get --experiment-id "$A3_ID" > "$TMP/a3.json" || fail A3_NOT_FOUND 6
STATUS="$(jq -r '.status // empty' "$TMP/a3.json")"
NAME="$(jq -r '.name // empty' "$TMP/a3.json")"
[[ "$STATUS" == ready ]] || fail "A3_NOT_READY:$STATUS" 6
[[ -z "$NAME" || "$NAME" == "$A3_NAME" ]] || fail "A3_NAME_MISMATCH:$NAME" 6
printf 'A3_ID=%s\nA3_STATUS=%s\n' "$A3_ID" "$STATUS"

bar 17 'Reading A3 manifest and exact node endpoints'; echo
portal-cli experiment manifests get --experiment-id "$A3_ID" > "$TMP/manifests.json" || fail A3_MANIFEST 7
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
                row['login']={'username':ch.attrib.get('username','aayoub'),'hostname':ch.attrib['hostname'],'port':int(ch.attrib.get('port','22'))}
        out[cid]=row
json.dump(out,open(sys.argv[2],'w'),indent=2,sort_keys=True)
for cid in ('enb1','rue1'):
    if cid not in out or 'login' not in out[cid]: raise SystemExit('missing '+cid)
    if out[cid].get('hardware_type')!='nuc5300': raise SystemExit(f'unexpected hardware {cid}={out[cid].get("hardware_type")}')
PY
jq '{enb1:{hardware_type:.enb1.hardware_type,disk_image:.enb1.disk_image},rue1:{hardware_type:.rue1.hardware_type,disk_image:.rue1.disk_image}}' "$TMP/nodes.json"

get_login(){ jq -r --arg n "$1" '.[$n].login | [.username,.hostname,(.port|tostring)] | @tsv' "$TMP/nodes.json"; }
IFS=$'\t' read -r CORE_USER CORE_EXT CORE_PORT < <(get_login enb1)
IFS=$'\t' read -r UE_USER UE_EXT UE_PORT < <(get_login rue1)
CORE_USER="${CORE_USER:-$POWDER_USERNAME}"
UE_USER="${UE_USER:-$POWDER_USERNAME}"
SSH=(-A -o BatchMode=yes -o IdentitiesOnly=no -o ConnectTimeout=15 -o ServerAliveInterval=10 -o ServerAliveCountMax=3 -o StrictHostKeyChecking=accept-new -o UserKnownHostsFile="$TMP/known_hosts")

bar 23 'Verifying external SSH to both A3 nodes'; echo
ssh "${SSH[@]}" -p "$CORE_PORT" "$CORE_USER@$CORE_EXT" 'true' || fail CORE_SSH 8
ssh "${SSH[@]}" -p "$UE_PORT" "$UE_USER@$UE_EXT" 'true' || fail UE_SSH 8
printf 'CORE_SSH=PASS\nUE_SSH=PASS\n'

bar 30 'Read-only core runtime inspection'; echo
ssh "${SSH[@]}" -p "$CORE_PORT" "$CORE_USER@$CORE_EXT" 'set -eu
printf "host=%s\n" "$(hostname)"
printf "python3=%s\n" "$(python3 --version 2>&1)"
test -x /local/repository/bin/start.sh
for c in mosquitto openssl rsync tmux curl sha256sum; do command -v "$c"; done
test -d /proj/WellPulse
test -w /proj/WellPulse
printf "CORE_READONLY_RUNTIME=PASS\n"' | tee "$TMP/core-readonly.txt" || fail CORE_RUNTIME_PRECHECK 9

bar 37 'Read-only UE/RF/runtime inspection'; echo
ssh "${SSH[@]}" -p "$UE_PORT" "$UE_USER@$UE_EXT" 'set -eu
printf "host=%s\n" "$(hostname)"
printf "python3=%s\n" "$(python3 --version 2>&1)"
test -x /local/repository/bin/start.sh
test -x /usr/local/etc/emulab/tmcc
for c in openssl tmux curl sha256sum ip ping getent; do command -v "$c"; done
test -d /proj/WellPulse
test -w /proj/WellPulse
ip link show tun_srsue >/dev/null
ip route get 172.16.0.1
ping -I tun_srsue -c 1 -W 2 172.16.0.1 >/dev/null
curl -fsSI --max-time 15 https://astral.sh/uv/install.sh >/dev/null
curl -fsSI --max-time 15 https://downloads.rclone.org/rclone-current-linux-amd64.zip >/dev/null
printf "UE_READONLY_RUNTIME=PASS\n"' | tee "$TMP/ue-readonly.txt" || fail UE_RUNTIME_PRECHECK 10

bar 44 'Read-only internal SSH topology check'; echo
ssh "${SSH[@]}" -p "$UE_PORT" "$UE_USER@$UE_EXT" "ssh -o BatchMode=yes -o ConnectTimeout=10 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null '$POWDER_USERNAME@enb1' true && ssh -o BatchMode=yes -o ConnectTimeout=10 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null '$POWDER_USERNAME@rue1' true" || fail INTERNAL_SSH_TOPOLOGY 11
printf 'A3_INTERNAL_SSH=PASS\n'

if [[ "$MODE" == PRECHECK ]]; then
  bar 100 'A3 read-only adoption precheck PASS'; echo
  printf 'WP2_A3_PRECHECK=PASS\n'
  printf 'POWDER_MUTATION_EXECUTED=NO\n'
  printf 'GOLDEN_EXECUTED=NO\n'
  printf 'EXPERIMENT_CREATE_COMMAND_AVAILABLE=NO\n'
  exit 0
fi

bar 50 'RUN gate: decoding verified Drive config locally'; echo
python3 - <<'PY'
import base64,os,pathlib
p=pathlib.Path('/tmp/wp2-a3-adopt/rclone.conf')
p.write_bytes(base64.b64decode(os.environ['RCLONE_CONFIG_B64'],validate=True))
p.chmod(0o600)
PY
[[ -s "$TMP/rclone.conf" ]] || fail RCLONE_CONFIG_DECODE 20

bar 55 'Deploying exact audited repository state to A3'; echo
git config --local --unset-all http.https://github.com/.extraheader >/dev/null 2>&1 || true
tar -czf "$TMP/repo.tgz" .
copy_repo(){
  local user="$1" host="$2" port="$3"
  scp "${SSH[@]}" -P "$port" "$TMP/repo.tgz" "$user@$host:/tmp/wp2-a3-repo.tgz" >/dev/null || return 1
  ssh "${SSH[@]}" -p "$port" "$user@$host" 'set -eu; rm -rf "$HOME/WellPulse"; mkdir -p "$HOME/WellPulse"; tar -xzf /tmp/wp2-a3-repo.tgz -C "$HOME/WellPulse"; rm -f /tmp/wp2-a3-repo.tgz' || return 1
}
copy_repo "$CORE_USER" "$CORE_EXT" "$CORE_PORT" || fail CORE_REPO_DEPLOY 21
copy_repo "$UE_USER" "$UE_EXT" "$UE_PORT" || fail UE_REPO_DEPLOY 21
ssh "${SSH[@]}" -p "$CORE_PORT" "$CORE_USER@$CORE_EXT" "cd \"\$HOME/WellPulse\" && test \"\$(git rev-parse HEAD)\" = '$GIT_SHA'" || fail CORE_SHA_MISMATCH 21
ssh "${SSH[@]}" -p "$UE_PORT" "$UE_USER@$UE_EXT" "cd \"\$HOME/WellPulse\" && test \"\$(git rev-parse HEAD)\" = '$GIT_SHA'" || fail UE_SHA_MISMATCH 21

bar 62 'Installing isolated Python/paho runtime on both A3 nodes'; echo
ssh "${SSH[@]}" -p "$CORE_PORT" "$CORE_USER@$CORE_EXT" 'cd "$HOME/WellPulse" && bash scripts/wp2_a3_runtime_bootstrap.sh' | tee "$TMP/core-bootstrap.txt" || fail CORE_RUNTIME_BOOTSTRAP 22
ssh "${SSH[@]}" -p "$UE_PORT" "$UE_USER@$UE_EXT" 'cd "$HOME/WellPulse" && bash scripts/wp2_a3_runtime_bootstrap.sh' | tee "$TMP/ue-bootstrap.txt" || fail UE_RUNTIME_BOOTSTRAP 22

bar 69 'Installing and verifying Drive config on UE only'; echo
scp "${SSH[@]}" -P "$UE_PORT" "$TMP/rclone.conf" "$UE_USER@$UE_EXT:/tmp/wp2-rclone.conf" >/dev/null || fail RCLONE_CONFIG_COPY 23
ssh "${SSH[@]}" -p "$UE_PORT" "$UE_USER@$UE_EXT" 'set -eu
mkdir -p "$HOME/.config/rclone"
chmod 700 "$HOME/.config/rclone"
install -m 600 /tmp/wp2-rclone.conf "$HOME/.config/rclone/rclone.conf"
rm -f /tmp/wp2-rclone.conf
export PATH="$HOME/.local/bin:$PATH"
rclone lsf gdrive: >/dev/null
printf "A3_DRIVE_RUNTIME=PASS\n"' || fail UE_DRIVE_VERIFY 23
rm -f "$TMP/rclone.conf"

bar 75 'Final pre-science runtime contract'; echo
ssh "${SSH[@]}" -p "$CORE_PORT" "$CORE_USER@$CORE_EXT" '$HOME/.wp2-golden-venv/bin/python -c '\''import importlib.metadata,sys; assert sys.version_info>=(3,10); assert importlib.metadata.version("paho-mqtt")=="2.1.0"'\''' || fail CORE_FINAL_RUNTIME 24
ssh "${SSH[@]}" -p "$UE_PORT" "$UE_USER@$UE_EXT" '$HOME/.wp2-golden-venv/bin/python -c '\''import importlib.metadata,sys; assert sys.version_info>=(3,10); assert importlib.metadata.version("paho-mqtt")=="2.1.0"'\''' || fail UE_FINAL_RUNTIME 24

RUN_ID="wp2-golden-a3-gh-${GITHUB_RUN_ID:-manual}-$(date -u +%Y%m%dT%H%M%SZ)"
printf '%s\n' "$RUN_ID" > "$TMP/run-id"
bar 80 'Launching exactly one non-scored Golden rehearsal on existing A3'; echo
set +e
ssh "${SSH[@]}" -p "$UE_PORT" "$UE_USER@$UE_EXT" "export PATH=\"\$HOME/.local/bin:\$PATH\"; cd \"\$HOME/WellPulse\"; WP_RUN_ID='$RUN_ID' WP_EXPERIMENT_ID='$A3_ID' WP_CORE_HOST='enb1' WP_UE_HOST='rue1' WP_REMOTE_USER='$POWDER_USERNAME' WP_REPO_ROOT=\"\$HOME/WellPulse\" WP_PYTHON=\"\$HOME/.wp2-golden-venv/bin/python\" WP_RCLONE_REMOTE_ROOT='gdrive:' bash scripts/wp2_golden_orchestrator.sh" 2>&1 | tee "$TMP/golden-console.txt"
GOLDEN_RC=${PIPESTATUS[0]}
set -e

CHECKPOINT="evidence/powder/wp2-a3-adoption-latest.md"
{
  echo '# WP2 A3 adoption checkpoint'
  echo
  echo "- Checked UTC: $(utc)"
  echo "- Experiment ID: $A3_ID"
  echo "- Experiment name: $A3_NAME"
  echo "- Git SHA: $GIT_SHA"
  echo "- Run ID: $RUN_ID"
  echo "- Golden exit code: $GOLDEN_RC"
  echo '- Scored run: NO'
  echo '- Credential material recorded: NO'
} > "$CHECKPOINT"

if [[ "$GOLDEN_RC" -ne 0 ]] || ! grep -q '^GOLDEN_E2E=PASS$' "$TMP/golden-console.txt" || ! grep -q '^EVIDENCE_ESCROW_GATE=PASS$' "$TMP/golden-console.txt" || ! grep -q '^TEARDOWN_AUTHORIZED=YES$' "$TMP/golden-console.txt"; then
  echo '- Verdict: FAIL_CLOSED_LEFT_LIVE' >> "$CHECKPOINT"
  echo "WP2_A3_ADOPTION=FAIL_CLOSED_LEFT_LIVE"
  echo "A3_ID=$A3_ID"
  echo 'AUTOMATIC_TERMINATION=PROHIBITED'
  exit 70
fi

bar 96 'G9/G10 verified: terminating A3 via Portal API'; echo
portal-cli experiment terminate --experiment-id "$A3_ID" > "$TMP/terminate.json" 2>"$TMP/terminate.err" || fail A3_TERMINATE_COMMAND 30
TERMINATED=0
for i in $(seq 1 60); do
  set +e
  portal-cli experiment get --experiment-id "$A3_ID" > "$TMP/postterm.json" 2>"$TMP/postterm.err"
  grc=$?
  set -e
  if [[ "$grc" -eq 0 ]]; then
    st="$(jq -r '.status // empty' "$TMP/postterm.json")"
    printf '\rA3_TERMINATION_WAIT=%02d/60 STATUS=%-18s' "$i" "$st"
    if [[ "$st" =~ ^(terminated|destroyed)$ ]]; then TERMINATED=1; break; fi
  else
    # A missing experiment is accepted only when a fresh list call succeeds and proves A3 absent.
    set +e
    portal-cli experiment list > "$TMP/postterm-list.json" 2>"$TMP/postterm-list.err"
    lrc=$?
    set -e
    if [[ "$lrc" -eq 0 ]]; then
      if python3 - "$TMP/postterm-list.json" "$A3_ID" <<'PY'
import json,sys
raw=json.load(open(sys.argv[1]))
xs=raw if isinstance(raw,list) else raw.get('experiments',[])
for x in xs:
    if isinstance(x,dict) and str(x.get('id','')) == sys.argv[2]:
        raise SystemExit(1)
raise SystemExit(0)
PY
      then
        printf '\rA3_TERMINATION_WAIT=%02d/60 STATUS=%-18s' "$i" 'absent-from-list'
        TERMINATED=1
        break
      fi
    fi
  fi
  sleep 5
done
echo
[[ "$TERMINATED" -eq 1 ]] || fail A3_TERMINATION_NOT_CONFIRMED 31

echo '- Verdict: PASS_DUAL_ESCROW_AND_TERMINATED' >> "$CHECKPOINT"
bar 100 'A3 Golden lifecycle PASS'; echo
printf 'WP2_A3_ADOPTION=PASS\n'
printf 'GOLDEN_E2E=PASS\n'
printf 'EVIDENCE_ESCROW_GATE=PASS\n'
printf 'A3_TERMINATION_CONFIRMED=YES\n'
