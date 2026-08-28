#!/usr/bin/env bash
set -euo pipefail

CMD=${1:?usage: wp2_p7b_rq2_controller.sh portal|stage-preflight|run-module|pull-evidence [arg]}
ROOT=$(cd "$(dirname "$0")/.." && pwd)
TMP="/tmp/wp2-p7b-rq2-${GITHUB_RUN_ID:-manual}-${CMD}"
mkdir -p "$TMP"

fail(){ echo "P7B_RQ2_CONTROLLER=BLOCKED:$1" >&2; exit "${2:-90}"; }
need(){ local n=$1; test -n "${!n:-}" || fail "MISSING_ENV_$n"; }

setup_ssh(){
  need POWDER_SSH_PRIVATE_KEY
  need POWDER_SSH_KEY_PASSPHRASE
  umask 077
  mkdir -p "$HOME/.ssh"
  python3 - "$TMP/private.key" <<'PY'
import os,sys
from pathlib import Path
raw=os.environ['POWDER_SSH_PRIVATE_KEY'].replace('\r\n','\n').replace('\r','\n').lstrip('\ufeff').strip()+'\n'
Path(sys.argv[1]).write_text(raw,encoding='utf-8',newline='\n')
PY
  chmod 600 "$TMP/private.key"
  cat > "$TMP/askpass" <<'EOF'
#!/usr/bin/env bash
printf '%s\n' "$POWDER_SSH_KEY_PASSPHRASE"
EOF
  chmod 700 "$TMP/askpass"
  export SSH_ASKPASS="$TMP/askpass" SSH_ASKPASS_REQUIRE=force DISPLAY=:0
  eval "$(ssh-agent -s)" >/dev/null
  setsid -w ssh-add "$TMP/private.key" </dev/null >/dev/null || fail SSH_KEY_LOAD
  : > "$HOME/.ssh/known_hosts"; chmod 600 "$HOME/.ssh/known_hosts"
  SSH_OPTS=(-A -o BatchMode=yes -o IdentitiesOnly=no -o ConnectTimeout=15 -o ServerAliveInterval=10 -o ServerAliveCountMax=3 -o StrictHostKeyChecking=accept-new -o UserKnownHostsFile="$HOME/.ssh/known_hosts")
}

ssh_do(){ local user=$1 host=$2 port=$3; shift 3; ssh "${SSH_OPTS[@]}" -p "$port" "$user@$host" "$@"; }
scp_to(){ local src=$1 user=$2 host=$3 port=$4 dst=$5; scp "${SSH_OPTS[@]}" -P "$port" "$src" "$user@$host:$dst" >/dev/null; }
scp_from(){ local user=$1 host=$2 port=$3 src=$4 dst=$5; scp "${SSH_OPTS[@]}" -P "$port" "$user@$host:$src" "$dst" >/dev/null; }

portal_identity(){
  need TARGET_EXPID; need TARGET_NAME; need PORTAL_TOKEN
  export PORTAL_HTTP=${PORTAL_HTTP:-https://boss.emulab.net:43794}
  bash "$ROOT/scripts/wp2_portal_client_bootstrap.sh" "$TMP/portal-api" | tee "$TMP/portal-pin.txt"
  grep -q '^PORTAL_API_PIN_GATE=PASS$' "$TMP/portal-pin.txt" || fail PORTAL_PIN
  portal-cli experiment get --experiment-id "$TARGET_EXPID" > "$TMP/experiment.json" || fail PORTAL_GET
  python3 "$ROOT/scripts/wp2_portal_record_guard.py" --json "$TMP/experiment.json" --expected-experiment-id "$TARGET_EXPID" | tee "$TMP/portal-gate.txt"
  grep -q '^PORTAL_RECORD_GATE=PASS$' "$TMP/portal-gate.txt" || fail PORTAL_RECORD
  EXPIRES=$(awk -F= '$1=="EXPIRES_UTC"{print $2}' "$TMP/portal-gate.txt" | tail -1)
  python3 "$ROOT/scripts/wp2_prelaunch_time_guard.py" --expires-utc "$EXPIRES" --min-remaining-s 7200 | tee "$TMP/time-gate.txt"
  grep -q '^PRELAUNCH_TIME_GATE=PASS$' "$TMP/time-gate.txt" || fail TIME_BUDGET
  python3 - "$TMP/experiment.json" "$TARGET_EXPID" "$TARGET_NAME" <<'PY'
import json,sys
x=json.load(open(sys.argv[1])); eid,name=sys.argv[2:4]
assert x.get('id')==eid
assert x.get('name')==name
assert x.get('project')=='WellPulse'
assert x.get('status')=='ready'
print('P7B_RQ2_EXISTING_RESERVATION_IDENTITY=PASS')
PY
  portal-cli experiment manifests get --experiment-id "$TARGET_EXPID" > "$TMP/manifests.json" || fail MANIFEST_FETCH
  python3 - "$TMP/manifests.json" "$TMP/nodes.json" <<'PY'
import json,sys,xml.etree.ElementTree as ET
obj=json.load(open(sys.argv[1])); out={}; xmls=[]
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
                row['login']={'username':ch.attrib.get('username','aayoub'),'hostname':ch.attrib['hostname'],'port':int(ch.attrib.get('port','22'))}
        out[cid]=row
expected_hw='nuc5300'; expected_img='urn:publicid:IDN+emulab.net+image+PowderProfiles:U18LL-SRSLTE:1'
for cid,node_name in (('enb1','nuc1'),('rue1','nuc2')):
    r=out.get(cid) or {}; assert r.get('login'),f'missing login {cid}'
    assert r.get('hardware_type')==expected_hw,(cid,r.get('hardware_type'))
    assert r.get('disk_image')==expected_img,(cid,r.get('disk_image'))
    assert r.get('component_id','').endswith('+'+node_name),(cid,r.get('component_id'))
json.dump(out,open(sys.argv[2],'w'),indent=2,sort_keys=True)
print('P7B_RQ2_MANIFEST_IDENTITY=PASS')
PY
  python3 - "$TMP/nodes.json" "$GITHUB_OUTPUT" "$EXPIRES" <<'PY'
import json,sys
x=json.load(open(sys.argv[1])); out=sys.argv[2]
with open(out,'a') as f:
    for prefix,cid in [('core','enb1'),('ue','rue1')]:
        l=x[cid]['login']
        f.write(f"{prefix}_user={l.get('username','aayoub')}\n{prefix}_host={l['hostname']}\n{prefix}_port={l.get('port',22)}\n")
    f.write(f"expires_utc={sys.argv[3]}\n")
PY
}

stage_preflight(){
  for n in SCIENTIFIC_SOURCE_SHA CORE_USER CORE_HOST CORE_PORT UE_USER UE_HOST UE_PORT; do need "$n"; done
  setup_ssh
  git cat-file -e "$SCIENTIFIC_SOURCE_SHA^{commit}" || fail SOURCE_COMMIT_MISSING
  git archive --format=tar "$SCIENTIFIC_SOURCE_SHA" | gzip -n > "$TMP/science.tgz"
  curl -fsSL 'https://repo.maven.apache.org/maven2/org/eclipse/paho/org.eclipse.paho.client.mqttv3/1.2.5/org.eclipse.paho.client.mqttv3-1.2.5.jar' -o "$TMP/paho.jar"
  echo '59914287adac506a28d5e8172eed262a22605f3df4d426b9d92f41dae2448185  '"$TMP/paho.jar" | sha256sum -c -
  stage(){ local user=$1 host=$2 port=$3; scp_to "$TMP/science.tgz" "$user" "$host" "$port" /tmp/wp2-rq2-science.tgz; ssh_do "$user" "$host" "$port" 'set -eu; rm -rf "$HOME/WellPulse"; mkdir -p "$HOME/WellPulse"; tar -xzf /tmp/wp2-rq2-science.tgz -C "$HOME/WellPulse"; rm -f /tmp/wp2-rq2-science.tgz'; }
  stage "$CORE_USER" "$CORE_HOST" "$CORE_PORT"
  stage "$UE_USER" "$UE_HOST" "$UE_PORT"
  scp_to "$TMP/paho.jar" "$UE_USER" "$UE_HOST" "$UE_PORT" /tmp/wp2-p7b-rq2-paho.jar
  core_home=$(ssh_do "$CORE_USER" "$CORE_HOST" "$CORE_PORT" 'printf "%s" "$HOME"')
  ue_home=$(ssh_do "$UE_USER" "$UE_HOST" "$UE_PORT" 'printf "%s" "$HOME"')
  core_repo=$(ssh_do "$CORE_USER" "$CORE_HOST" "$CORE_PORT" 'cd "$HOME/WellPulse"; pwd -P')
  ue_repo=$(ssh_do "$UE_USER" "$UE_HOST" "$UE_PORT" 'cd "$HOME/WellPulse"; pwd -P')
  ssh_do "$CORE_USER" "$CORE_HOST" "$CORE_PORT" "cd '$core_repo'; WP_REPO_ROOT='$core_repo' bash scripts/wp2_p7b_target_node_preflight.sh core" | tee "$TMP/core-preflight.txt"
  grep -q '^WP2_P7B_TARGET_NODE_PREFLIGHT=PASS$' "$TMP/core-preflight.txt" || fail CORE_TARGET_PREFLIGHT
  ssh_do "$UE_USER" "$UE_HOST" "$UE_PORT" "cd '$ue_repo'; WP_REPO_ROOT='$ue_repo' WP_B2_JAR_PATH=/tmp/wp2-p7b-rq2-paho.jar bash scripts/wp2_p7b_target_node_preflight.sh ue" | tee "$TMP/ue-preflight.txt"
  grep -q '^WP2_P7B_TARGET_NODE_PREFLIGHT=PASS$' "$TMP/ue-preflight.txt" || fail UE_TARGET_PREFLIGHT
  for spec in "CORE:$CORE_USER:$CORE_HOST:$CORE_PORT" "UE:$UE_USER:$UE_HOST:$UE_PORT"; do
    IFS=: read -r label user host port <<< "$spec"
    rev=$(ssh_do "$user" "$host" "$port" 'git -C /local/repository rev-parse HEAD')
    test "$rev" = a6da96560b6526dc6816761282722c996418fd8c || fail "${label}_PROFILE_REVISION_$rev"
  done
  {
    echo "core_home=$core_home"; echo "ue_home=$ue_home"; echo "core_repo=$core_repo"; echo "ue_repo=$ue_repo";
  } >> "$GITHUB_OUTPUT"
  echo 'P7B_RQ2_M2=PASS_TARGET_PREFLIGHT'
}

run_module(){
  MODULE=${2:?module required}
  for n in RUN_ID TARGET_EXPID SCIENTIFIC_SOURCE_SHA EXPIRES_UTC CORE_USER CORE_HOST CORE_PORT UE_USER UE_HOST UE_PORT CORE_HOME UE_HOME CORE_REPO UE_REPO; do need "$n"; done
  case "$MODULE" in prepare|B1|W1|B2|reconstruct) ;; *) fail BAD_MODULE;; esac
  setup_ssh
  remote="cd '$UE_REPO' && env WP_RUN_ID='$RUN_ID' WP_EXPERIMENT_ID='$TARGET_EXPID' WP_CORE_HOST='enb1' WP_UE_HOST='rue1' WP_REMOTE_USER='aayoub' WP_REPO_ROOT='$UE_REPO' WP_PYTHON='$UE_HOME/.wp2-golden-venv/bin/python' WP_HARD_EXPIRY_UTC='$EXPIRES_UTC' WP_CORE_MANAGEMENT_HOST='$CORE_HOST' WP_UE_MANAGEMENT_HOST='$UE_HOST' WP_CORE_REPO_ROOT='$CORE_REPO' WP_AUTHORITY_ID='P7B-RQ2' WP_SCIENTIFIC_SOURCE_SHA='$SCIENTIFIC_SOURCE_SHA' WP_B2_JAR_STAGED='/tmp/wp2-p7b-rq2-paho.jar' WP_CONTROLLER_HOST_ROLE='UE' '$UE_HOME/.wp2-golden-venv/bin/python' scripts/wp2_p7b_rq2_module_adapter.py '$MODULE'"
  ssh_do "$UE_USER" "$UE_HOST" "$UE_PORT" "$remote"
}

pull_evidence(){
  LABEL=${2:?label required}
  for n in RUN_ID CORE_USER CORE_HOST CORE_PORT UE_USER UE_HOST UE_PORT CORE_HOME UE_HOME; do need "$n"; done
  setup_ssh
  OUT="$TMP/evidence-$LABEL"; mkdir -p "$OUT"
  ue_root="$UE_HOME/wellpulse-powder-evidence/p7b/$RUN_ID"
  core_root="$CORE_HOME/wellpulse-powder-evidence/p7b/$RUN_ID-core"
  ssh_do "$UE_USER" "$UE_HOST" "$UE_PORT" "test -d '$ue_root'; tar -C '$UE_HOME/wellpulse-powder-evidence/p7b' -cf /tmp/wp2-rq2-$LABEL-ue.tar '$RUN_ID'"
  ssh_do "$CORE_USER" "$CORE_HOST" "$CORE_PORT" "test -d '$core_root'; tar -C '$CORE_HOME/wellpulse-powder-evidence/p7b' -cf /tmp/wp2-rq2-$LABEL-core.tar '$RUN_ID-core'"
  scp_from "$UE_USER" "$UE_HOST" "$UE_PORT" "/tmp/wp2-rq2-$LABEL-ue.tar" "$OUT/ue.tar"
  scp_from "$CORE_USER" "$CORE_HOST" "$CORE_PORT" "/tmp/wp2-rq2-$LABEL-core.tar" "$OUT/core.tar"
  test -s "$OUT/ue.tar"; test -s "$OUT/core.tar"
  tar -tf "$OUT/ue.tar" >/dev/null; tar -tf "$OUT/core.tar" >/dev/null
  (cd "$OUT"; sha256sum ue.tar core.tar > SHA256SUMS.txt; sha256sum -c SHA256SUMS.txt)
  echo "evidence_dir=$OUT" >> "$GITHUB_OUTPUT"
  echo "P7B_RQ2_EVIDENCE_PULL=PASS:$LABEL"
}

case "$CMD" in
  portal) portal_identity ;;
  stage-preflight) stage_preflight ;;
  run-module) run_module "$@" ;;
  pull-evidence) pull_evidence "$@" ;;
  *) fail UNKNOWN_COMMAND ;;
esac
