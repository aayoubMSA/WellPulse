#!/usr/bin/env bash
set -euo pipefail

MODE=${1:-}
TMP=/tmp/wp2-p7b-r3
STATE="$TMP/state.env"
RESULT="$TMP/result.env"
AUTHORITY_ID=P7B-RQ1
PROFILE_PROJECT=PowderProfiles
PROFILE_NAME=srslte-controlled-rf
EXPECTED_PROFILE_REVISION=a6da96560b6526dc6816761282722c996418fd8c
EXPECTED_HARDWARE=nuc5300
EXPECTED_IMAGE='urn:publicid:IDN+emulab.net+image+PowderProfiles:U18LL-SRSLTE:1'
BINDINGS='{"enb_node":"nuc1","ue_node":"nuc2","ue_type":"srsue"}'
PORTAL_HTTP="${PORTAL_HTTP:-https://boss.emulab.net:43794}"
PORTAL_TOKEN="${PORTAL_TOKEN:-}"
POWDER_USERNAME="${POWDER_USERNAME:-aayoub}"
POWDER_SSH_PRIVATE_KEY="${POWDER_SSH_PRIVATE_KEY:-}"
POWDER_SSH_KEY_PASSPHRASE="${POWDER_SSH_KEY_PASSPHRASE:-}"
SOURCE_SHA="${GITHUB_SHA:-$(git rev-parse HEAD)}"
export PORTAL_HTTP PORTAL_TOKEN

# Frozen replacement authority guards.
echo 'P7B-RQ1' >/dev/null
echo 'AUTOMATIC_RETRY=NO' >/dev/null
echo 'SECOND_REPLACEMENT=NO' >/dev/null
# Required R1 surfaces are deliberately named here and used below.
R1_ENTRYPOINT='scripts/wp2_p7b_c_node_r1.py'
PRESERVATION_HELPER='scripts/wp2_p7b_preservation_helpers.sh'
R1_ENTRYPOINT_BLOB='6d28468c93742046d952668b9df1cad8e6ea78c0'
PATH_CONTRACT_BLOB='2e77e7e355e25c6e3f747956e2f2b0ac5ad46161'
PRESERVATION_HELPER_BLOB='9063ec2e97e9cbf7a9f76d6ea10920236d8370ef'

mkdir -p "$TMP"
touch "$RESULT"

bar(){ local p=$1 m=$2 n=$((p/5)); printf '\r['; printf '%*s' "$n" ''|tr ' ' '#'; printf '%*s' "$((20-n))" ''|tr ' ' '-'; printf '] %3d%%  %-66s' "$p" "$m"; }
utc(){ date -u +%Y-%m-%dT%H:%M:%SZ; }
fail(){ echo; echo "WP2_P7B_R3=BLOCKED:$1" >&2; printf 'FAILURE=%s\n' "$1" >> "$RESULT"; exit "${2:-90}"; }
set_output(){ if [[ -n "${GITHUB_OUTPUT:-}" ]]; then printf '%s=%s\n' "$1" "$2" >> "$GITHUB_OUTPUT"; fi; }

init_ssh(){
  [[ -n "$POWDER_SSH_PRIVATE_KEY" ]] || fail POWDER_SSH_PRIVATE_KEY_MISSING 2
  umask 077; mkdir -p "$HOME/.ssh"
  python3 - <<'PY'
import os
from pathlib import Path
raw=os.environ['POWDER_SSH_PRIVATE_KEY'].replace('\r\n','\n').replace('\r','\n').lstrip('\ufeff').strip()+"\n"
Path('/tmp/wp2-p7b-r3/private.key').write_text(raw,encoding='utf-8',newline='\n')
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
  setsid -w ssh-add "$TMP/private.key" </dev/null >/dev/null || fail SSH_KEY_LOAD 4
  : > "$HOME/.ssh/known_hosts"; chmod 600 "$HOME/.ssh/known_hosts"
  SSH=(-A -o BatchMode=yes -o IdentitiesOnly=no -o ConnectTimeout=15 -o ServerAliveInterval=10 -o ServerAliveCountMax=3 -o StrictHostKeyChecking=accept-new -o UserKnownHostsFile="$HOME/.ssh/known_hosts")
}

portal_bootstrap(){
  [[ -n "$PORTAL_TOKEN" ]] || fail POWDER_API_TOKEN_MISSING 2
  bash scripts/wp2_portal_client_bootstrap.sh "$TMP/portal-api" | tee "$TMP/portal-pin.txt"
  grep -q '^PORTAL_API_PIN_GATE=PASS$' "$TMP/portal-pin.txt" || fail PORTAL_CLIENT_PIN 3
}

strict_bundle_check(){
  local root=$1 ue="$1/ue/raw" core="$1/core/raw"
  test -s "$ue/p7b_c_status.json"
  test "$(jq -r '.gate' "$ue/p7b_c_status.json")" = PASS_PHYSICAL_CELLS
  test "$(jq -r '.completed_cells|join(",")' "$ue/p7b_c_status.json")" = 'P7B-B1-S3,P7B-W1-S3,P7B-B2-S3'
  test -s "$ue/orchestration/p7b_c_events.jsonl"
  test -s "$ue/runtime/paho.jar"
  for c in P7B-B1-S3 P7B-W1-S3 P7B-B2-S3; do
    test -s "$ue/cells/$c/readiness_observation.json"
    test -s "$ue/cells/$c/readiness_verdict.json"
    test -s "$ue/cells/$c/runtime_manifest.json"
    test -s "$ue/cells/$c/telemetry_generated.csv"
    test -s "$ue/cells/$c/generator_events.jsonl"
    test -s "$ue/cells/$c/restart_proof.json"
    test -s "$ue/cells/$c/t_rf_restore.txt"
    test -s "$ue/cells/$c/t_service_ready.txt"
    test -s "$ue/cells/$c/service_ready_probe.txt"
    test -s "$core/cells/$c/receiver/receiver_events.jsonl"
    test -s "$core/cells/$c/receiver/telemetry_received.csv"
    # A healthy receiver writes its authoritative events/CSV directly and may
    # legitimately emit no stdout. Console existence is required for provenance;
    # non-empty console content is not a scientific completeness criterion.
    test -e "$core/cells/$c/receiver/console.txt"
  done
  test -s "$ue/cells/P7B-B1-S3/mqtt_events.jsonl"
  test -s "$ue/cells/P7B-B1-S3/pre_restart_transport_snapshot.json"
  test -s "$ue/cells/P7B-W1-S3/w1_queue.sqlite"
  test -s "$ue/cells/P7B-W1-S3/w1_durability_proof.json"
  test -s "$ue/cells/P7B-B2-S3/b2_events.jsonl"
  test -s "$ue/cells/P7B-B2-S3/b2_durability_proof.json"
  test -s "$ue/analysis/p7b_reconstruction.json"
  test "$(jq -r '.gate' "$ue/analysis/p7b_reconstruction.json")" = PASS
}

prepare(){
  rm -rf "$TMP"; mkdir -p "$TMP"; : > "$RESULT"
  # Premutation code/contract locks are checked before the first POWDER API call.
  bash -n powder/wp2_p7b_r3_execute.sh || fail R3_CONTROLLER_SHELL_SYNTAX 5
  python3 scripts/wp2_p7b_r2_validate_controller.py --controller powder/wp2_p7b_r3_execute.sh | tee "$TMP/r2-static.txt"
  grep -q '^P7B_R2_CONTROLLER_STATIC_GATE=PASS$' "$TMP/r2-static.txt" || fail R2_STATIC_CONTROLLER_GATE 5
  test "$(git hash-object "$R1_ENTRYPOINT")" = "$R1_ENTRYPOINT_BLOB" || fail R1_ENTRYPOINT_BLOB_DRIFT 5
  test "$(git hash-object scripts/wp2_p7b_path_contract.py)" = "$PATH_CONTRACT_BLOB" || fail PATH_CONTRACT_BLOB_DRIFT 5
  test "$(git hash-object "$PRESERVATION_HELPER")" = "$PRESERVATION_HELPER_BLOB" || fail PRESERVATION_HELPER_BLOB_DRIFT 5
  portal_bootstrap; init_ssh
  bar 5 'Authority guards + no-active-P7B check'; echo
  portal-cli experiment list > "$TMP/list-before.json" || fail PORTAL_LIST 5
  python3 - "$TMP/list-before.json" <<'PY'
import json,sys
obj=json.load(open(sys.argv[1])); xs=obj if isinstance(obj,list) else obj.get('experiments',[])
terminal={'terminated','destroyed','failed','error'}; active=[]
for x in xs:
    if not isinstance(x,dict) or x.get('project')!='WellPulse': continue
    name=str(x.get('name','')); status=str(x.get('status','')).lower()
    if name.startswith('wp7b') and status not in terminal:
        active.append({'id':x.get('id'),'name':name,'status':status})
if active:
    print('ACTIVE_P7B_CONFLICT='+json.dumps(active,sort_keys=True,separators=(',',':'))); raise SystemExit(20)
print('ACTIVE_P7B_CONFLICT=NONE')
PY

  bar 10 'Creating exactly one P7B-RQ1 non-scored reservation'; echo
  SUFFIX="${GITHUB_RUN_ID:-manual}"; SUFFIX="${SUFFIX: -7}"; EXP_NAME="wp7brq1${SUFFIX}"
  [[ ${#EXP_NAME} -le 16 ]] || fail EXPERIMENT_NAME_LENGTH 6
  PUB="$(cat "$TMP/public.key")"
  portal-cli experiment create --name "$EXP_NAME" --project WellPulse --profile-name "$PROFILE_NAME" --profile-project "$PROFILE_PROJECT" --duration 2 --bindings "$BINDINGS" --sshpubkey "$PUB" > "$TMP/create.json" || fail RESERVATION_CREATE 6
  EXPID="$(jq -r '.id // empty' "$TMP/create.json")"; [[ "$EXPID" =~ ^[0-9A-Fa-f-]{36}$ ]] || fail CREATE_RETURNED_NO_UUID 6
  set_output experiment_id "$EXPID"
  set_output experiment_name "$EXP_NAME"
  printf 'EXPID=%q\nEXP_NAME=%q\nPREPARE_GATE=LIVE_RESERVATION_CREATED\n' "$EXPID" "$EXP_NAME" > "$STATE"

  bar 15 'Waiting for authoritative READY + immutable identity checks'; echo
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
json.dump(out,open(sys.argv[2],'w'),indent=2,sort_keys=True); print('P7B_R3_MANIFEST_IDENTITY=PASS')
PY
  get_login(){ jq -r --arg n "$1" '.[$n].login | [.username,.hostname,(.port|tostring)] | @tsv' "$TMP/nodes.json"; }
  IFS=$'\t' read -r CORE_USER CORE_EXT CORE_PORT < <(get_login enb1)
  IFS=$'\t' read -r UE_USER UE_EXT UE_PORT < <(get_login rue1)
  CORE_USER="${CORE_USER:-$POWDER_USERNAME}"; UE_USER="${UE_USER:-$POWDER_USERNAME}"

  bar 25 'SSH/profile/runtime compatibility re-verification'; echo
  ssh_wait(){ local user=$1 host=$2 port=$3 label=$4; for i in $(seq 1 36); do if ssh "${SSH[@]}" -p "$port" "$user@$host" true >/dev/null 2>&1; then echo "$label SSH=PASS"; return 0; fi; sleep 10; done; return 1; }
  ssh_wait "$CORE_USER" "$CORE_EXT" "$CORE_PORT" CORE || fail CORE_SSH 9
  ssh_wait "$UE_USER" "$UE_EXT" "$UE_PORT" UE || fail UE_SSH 9
  for spec in "core:$CORE_USER:$CORE_EXT:$CORE_PORT" "ue:$UE_USER:$UE_EXT:$UE_PORT"; do
    IFS=: read -r role user host port <<< "$spec"
    ssh "${SSH[@]}" -p "$port" "$user@$host" 'set -eu; test -x /local/repository/bin/start.sh; test -d /proj/WellPulse && test -w /proj/WellPulse; echo "PROFILE_REPO_SHA=$(git -C /local/repository rev-parse HEAD)"' | tee "$TMP/${role}-profile.txt"
    grep -q "^PROFILE_REPO_SHA=$EXPECTED_PROFILE_REVISION$" "$TMP/${role}-profile.txt" || fail "PROFILE_REVISION_$role" 9
  done

  bar 32 'Copying exact authorized source checkout to both nodes'; echo
  rm -rf "$TMP/repo-copy"; git clone --no-hardlinks . "$TMP/repo-copy" >/dev/null 2>&1 || fail LOCAL_REPO_CLONE 10
  git -C "$TMP/repo-copy" checkout -q --detach "$SOURCE_SHA" || fail SOURCE_SHA_CHECKOUT 10
  git -C "$TMP/repo-copy" config --local --unset-all http.https://github.com/.extraheader >/dev/null 2>&1 || true
  tar -C "$TMP/repo-copy" -czf "$TMP/wellpulse-repo.tgz" .
  copy_repo(){ local user=$1 host=$2 port=$3; scp "${SSH[@]}" -P "$port" "$TMP/wellpulse-repo.tgz" "$user@$host:/tmp/wellpulse-repo.tgz" >/dev/null; ssh "${SSH[@]}" -p "$port" "$user@$host" 'rm -rf "$HOME/WellPulse"; mkdir -p "$HOME/WellPulse"; tar -xzf /tmp/wellpulse-repo.tgz -C "$HOME/WellPulse"; rm -f /tmp/wellpulse-repo.tgz'; }
  copy_repo "$CORE_USER" "$CORE_EXT" "$CORE_PORT" || fail COPY_CORE_REPO 10
  copy_repo "$UE_USER" "$UE_EXT" "$UE_PORT" || fail COPY_UE_REPO 10

  bar 38 'Bootstrapping pinned Python/MQTT/Java runtimes'; echo
  CORE_SYS='sudo apt-get update -qq && sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq mosquitto mosquitto-clients rsync tmux curl unzip openssl >/dev/null'
  UE_SYS='sudo apt-get update -qq && sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq mosquitto-clients rsync tmux curl unzip openssl default-jdk-headless >/dev/null'
  ssh "${SSH[@]}" -p "$CORE_PORT" "$CORE_USER@$CORE_EXT" "$CORE_SYS" || fail CORE_SYSTEM_BOOTSTRAP 11
  ssh "${SSH[@]}" -p "$UE_PORT" "$UE_USER@$UE_EXT" "$UE_SYS" || fail UE_SYSTEM_BOOTSTRAP 11
  ssh "${SSH[@]}" -p "$CORE_PORT" "$CORE_USER@$CORE_EXT" 'cd "$HOME/WellPulse" && WP_REPO_ROOT="$HOME/WellPulse" bash scripts/wp2_a3_runtime_bootstrap.sh' > "$TMP/core-runtime-bootstrap.txt" || fail CORE_RUNTIME_BOOTSTRAP 11
  ssh "${SSH[@]}" -p "$UE_PORT" "$UE_USER@$UE_EXT" 'cd "$HOME/WellPulse" && WP_REPO_ROOT="$HOME/WellPulse" bash scripts/wp2_a3_runtime_bootstrap.sh' > "$TMP/ue-runtime-bootstrap.txt" || fail UE_RUNTIME_BOOTSTRAP 11
  grep -q '^A3_RUNTIME_BOOTSTRAP=PASS$' "$TMP/core-runtime-bootstrap.txt" || fail CORE_RUNTIME_CONTRACT 11
  grep -q '^A3_RUNTIME_BOOTSTRAP=PASS$' "$TMP/ue-runtime-bootstrap.txt" || fail UE_RUNTIME_CONTRACT 11

  bar 45 'Establishing clean initial Q0 LTE user plane'; echo
  ssh "${SSH[@]}" -p "$UE_PORT" "$UE_USER@$UE_EXT" 'set -u; for s in ue srs-ue; do tmux kill-session -t "$s" >/dev/null 2>&1 || true; done; sudo killall srsue >/dev/null 2>&1 || true; sudo ip link del tun_srsue >/dev/null 2>&1 || true; for id in 1 33 2 34; do /usr/local/etc/emulab/tmcc attenuator "$id" 0; done; sleep 2' || fail PRE_Q0_UE_CLEAN 12
  ssh "${SSH[@]}" -p "$CORE_PORT" "$CORE_USER@$CORE_EXT" 'set -u; for s in enb srs-epc srs-enb; do tmux kill-session -t "$s" >/dev/null 2>&1 || true; done; sudo killall srsenb srsepc >/dev/null 2>&1 || true; sleep 2; cd /local/repository; set +e; bash bin/start.sh > /tmp/wp2-p7b-r3-q0-core.console 2>&1; exit 0' || fail PRE_Q0_CORE_START 12
  CORE_READY=0; for i in $(seq 1 45); do if ssh "${SSH[@]}" -p "$CORE_PORT" "$CORE_USER@$CORE_EXT" 'pgrep -x srsepc >/dev/null && pgrep -x srsenb >/dev/null'; then CORE_READY=1; break; fi; sleep 2; done
  [[ "$CORE_READY" -eq 1 ]] || fail PRE_Q0_CORE_NOT_READY 12
  sleep 10
  ssh "${SSH[@]}" -p "$CORE_PORT" "$CORE_USER@$CORE_EXT" 'pgrep -x srsepc >/dev/null && pgrep -x srsenb >/dev/null' || fail PRE_Q0_CORE_NOT_STABLE 12
  ssh "${SSH[@]}" -p "$UE_PORT" "$UE_USER@$UE_EXT" 'cd /local/repository; set +e; bash bin/start.sh > /tmp/wp2-p7b-r3-q0-ue.console 2>&1; exit 0' || fail PRE_Q0_UE_START 12
  UE_READY=0; for i in $(seq 1 60); do if ssh "${SSH[@]}" -p "$UE_PORT" "$UE_USER@$UE_EXT" 'pgrep -x srsue >/dev/null && ip link show tun_srsue >/dev/null 2>&1 && ip -4 addr show dev tun_srsue | grep -q "inet "'; then UE_READY=1; break; fi; sleep 2; done
  [[ "$UE_READY" -eq 1 ]] || fail PRE_Q0_UE_NOT_READY 12
  ssh "${SSH[@]}" -p "$UE_PORT" "$UE_USER@$UE_EXT" 'set -eu; ip route get 172.16.0.1 | grep -q tun_srsue; ping -I tun_srsue -c 5 -W 2 172.16.0.1 | tee /tmp/wp2-p7b-r3-q0-ping.txt; grep -q "0% packet loss" /tmp/wp2-p7b-r3-q0-ping.txt' || fail PRE_Q0_USER_PLANE 12

  bar 50 'Executing repaired B1 -> W1 -> B2 qualification runner'; echo
  RUN_ID="wp2-p7b-r3-${GITHUB_RUN_ID:-manual}-$(date -u +%Y%m%dT%H%M%SZ)"
  set +e
  ssh "${SSH[@]}" -p "$UE_PORT" "$UE_USER@$UE_EXT" "cd \"\$HOME/WellPulse\" && WP_RUN_ID='$RUN_ID' WP_EXPERIMENT_ID='$EXPID' WP_CORE_HOST='enb1' WP_UE_HOST='rue1' WP_REMOTE_USER='aayoub' WP_REPO_ROOT=\"\$HOME/WellPulse\" WP_PYTHON=\"\$HOME/.wp2-golden-venv/bin/python\" WP_HARD_EXPIRY_UTC='$EXPIRES' WP_CORE_MANAGEMENT_HOST='$CORE_EXT' WP_UE_MANAGEMENT_HOST='$UE_EXT' \"\$HOME/.wp2-golden-venv/bin/python\" $R1_ENTRYPOINT" 2>&1 | tee "$TMP/r3-node-console.txt"
  NODE_RC=${PIPESTATUS[0]}; set -e
  set_output node_rc "$NODE_RC"
  set_output run_id "$RUN_ID"

  UE_HOME="$(ssh "${SSH[@]}" -p "$UE_PORT" "$UE_USER@$UE_EXT" 'printf "%s" "$HOME"')"
  CORE_HOME="$(ssh "${SSH[@]}" -p "$CORE_PORT" "$CORE_USER@$CORE_EXT" 'printf "%s" "$HOME"')"
  python3 scripts/wp2_p7b_path_contract.py validate --path "$UE_HOME" >/dev/null || fail UE_HOME_PATH_CONTRACT 70
  python3 scripts/wp2_p7b_path_contract.py validate --path "$CORE_HOME" >/dev/null || fail CORE_HOME_PATH_CONTRACT 70
  UE_SRC="$UE_HOME/wellpulse-powder-evidence/p7b/$RUN_ID"
  CORE_SRC="$CORE_HOME/wellpulse-powder-evidence/p7b/$RUN_ID-core"

  echo '::group::P7B-R3 bounded live raw-evidence view'
  echo "NODE_RC=$NODE_RC"
  ssh "${SSH[@]}" -p "$UE_PORT" "$UE_USER@$UE_EXT" "cat '$UE_SRC/p7b_c_status.json' 2>/dev/null || true"
  for c in P7B-B1-S3 P7B-W1-S3 P7B-B2-S3; do
    echo "--- $c receiver event tail ---"
    ssh "${SSH[@]}" -p "$CORE_PORT" "$CORE_USER@$CORE_EXT" "tail -n 30 '$CORE_SRC/cells/$c/receiver/receiver_events.jsonl' 2>/dev/null || true"
  done
  echo '::endgroup::'

  bar 82 'Persistent /proj escrow using resolved absolute paths'; echo
  PDIR="/proj/WellPulse/evidence-escrow/$EXPID/$RUN_ID"
  ssh "${SSH[@]}" -p "$UE_PORT" "$UE_USER@$UE_EXT" "cd '$UE_HOME/WellPulse'; source '$PRESERVATION_HELPER'; p7b_copy_tree_with_hash_manifest '$UE_SRC' '$PDIR/ue'" | tee "$TMP/persist-ue.txt"
  ssh "${SSH[@]}" -p "$CORE_PORT" "$CORE_USER@$CORE_EXT" "cd '$CORE_HOME/WellPulse'; source '$PRESERVATION_HELPER'; p7b_copy_tree_with_hash_manifest '$CORE_SRC' '$PDIR/core'" | tee "$TMP/persist-core.txt"
  grep -q '^P7B_PRESERVATION_COPY=PASS$' "$TMP/persist-ue.txt" || fail UE_PERSISTENCE 72
  grep -q '^P7B_PRESERVATION_COPY=PASS$' "$TMP/persist-core.txt" || fail CORE_PERSISTENCE 72

  ssh "${SSH[@]}" -p "$UE_PORT" "$UE_USER@$UE_EXT" "set -euo pipefail; (cd '$PDIR/ue/raw' && sha256sum -c ../SOURCE_SHA256SUMS >/dev/null); (cd '$PDIR/core/raw' && sha256sum -c ../SOURCE_SHA256SUMS >/dev/null); printf 'EVIDENCE_ESCROW_GATE=PASS\nTEARDOWN_AUTHORIZED=PENDING_OFFPOWDER_READBACK\n' > '$PDIR/PERSISTENT_ESCROW_GATE.PASS'; tar -C '$PDIR' -cf - ." > "$TMP/persistent-stream.tar"

  rm -rf "$TMP/controller"; mkdir -p "$TMP/controller"; tar -C "$TMP/controller" -xf "$TMP/persistent-stream.tar"
  (cd "$TMP/controller/ue/raw" && sha256sum -c ../SOURCE_SHA256SUMS >/dev/null)
  (cd "$TMP/controller/core/raw" && sha256sum -c ../SOURCE_SHA256SUMS >/dev/null)
  strict_bundle_check "$TMP/controller" || {
    BUNDLE="$TMP/wp2-p7b-r3-partial-$RUN_ID.tar"
    tar --sort=name --mtime='UTC 1970-01-01' --owner=0 --group=0 --numeric-owner -C "$TMP/controller" -cf "$BUNDLE" . || true
    if test -s "$BUNDLE"; then set_output bundle_path "$BUNDLE"; set_output bundle_sha256 "$(sha256sum "$BUNDLE"|awk '{print $1}')"; fi
    printf 'EXPID=%q\nRUN_ID=%q\nNODE_RC=%q\nPREPARE_GATE=BLOCKED_STRICT_COMPLETENESS\n' "$EXPID" "$RUN_ID" "$NODE_RC" > "$STATE"
    fail STRICT_RAW_EVIDENCE_COMPLETENESS 73
  }
  echo 'EVIDENCE_ESCROW_GATE=PASS'
  echo 'CONTROLLER_PULL_GATE=PASS'

  BUNDLE="$TMP/wp2-p7b-r3-$RUN_ID.tar"
  tar --sort=name --mtime='UTC 1970-01-01' --owner=0 --group=0 --numeric-owner -C "$TMP/controller" -cf "$BUNDLE" .
  BUNDLE_SHA="$(sha256sum "$BUNDLE" | awk '{print $1}')"; BUNDLE_BYTES="$(stat -c%s "$BUNDLE")"
  printf 'EXPID=%q\nEXP_NAME=%q\nRUN_ID=%q\nNODE_RC=%q\nBUNDLE_SHA=%q\nBUNDLE_BYTES=%q\nPREPARE_GATE=PASS\n' "$EXPID" "$EXP_NAME" "$RUN_ID" "$NODE_RC" "$BUNDLE_SHA" "$BUNDLE_BYTES" > "$STATE"
  set_output bundle_path "$BUNDLE"; set_output bundle_sha256 "$BUNDLE_SHA"; set_output bundle_bytes "$BUNDLE_BYTES"
  echo "CONTROLLER_BUNDLE_SHA256=$BUNDLE_SHA"
  bar 90 'Prepared verified bundle; waiting for GitHub artifact round-trip'; echo
}

finalize(){
  local roundtrip=${2:?roundtrip tar required} expected_sha=${3:?expected sha required}
  test -s "$STATE" || fail STATE_MISSING 80
  source "$STATE"
  test "$PREPARE_GATE" = PASS || fail PREPARE_GATE_NOT_PASS 80
  test -s "$roundtrip" || fail ROUNDTRIP_MISSING 81
  test "$(sha256sum "$roundtrip" | awk '{print $1}')" = "$expected_sha" || fail ROUNDTRIP_OUTER_SHA_MISMATCH 81
  rm -rf "$TMP/readback"; mkdir -p "$TMP/readback"; tar -C "$TMP/readback" -xf "$roundtrip"
  (cd "$TMP/readback/ue/raw" && sha256sum -c ../SOURCE_SHA256SUMS >/dev/null)
  (cd "$TMP/readback/core/raw" && sha256sum -c ../SOURCE_SHA256SUMS >/dev/null)
  strict_bundle_check "$TMP/readback" || fail ROUNDTRIP_STRICT_COMPLETENESS 82
  test -s "$TMP/readback/PERSISTENT_ESCROW_GATE.PASS" || fail PERSISTENT_GATE_MARKER_MISSING 82

  echo '::group::P7B-R3 independent read-back summary'
  jq '{gate,completed_cells,scored,scored_runs_authorized}' "$TMP/readback/ue/raw/p7b_c_status.json"
  for c in P7B-B1-S3 P7B-W1-S3 P7B-B2-S3; do
    echo "--- $c receiver events (tail) ---"; tail -n 12 "$TMP/readback/core/raw/cells/$c/receiver/receiver_events.jsonl"
  done
  echo '::endgroup::'

  echo 'EVIDENCE_ESCROW_GATE=PASS'
  echo 'CONTROLLER_OFFPOWDER_GATE=PASS'
  echo 'TEARDOWN_AUTHORIZED=YES'
  portal_bootstrap
  portal-cli experiment terminate --experiment-id "$EXPID" > "$TMP/terminate.json" 2>"$TMP/terminate.err" || true
  TERMINATED=0
  for i in $(seq 1 60); do
    set +e; portal-cli experiment get --experiment-id "$EXPID" > "$TMP/postterm.json" 2>/dev/null; rc=$?; set -e
    if [[ "$rc" -ne 0 ]]; then TERMINATED=1; echo "P7B_R3_TERMINATION_POLL_${i}=NOT_FOUND"; break; fi
    st="$(jq -r '.status // "unknown"' "$TMP/postterm.json")"; echo "P7B_R3_TERMINATION_POLL_${i}=$st"
    if [[ "$st" =~ ^(terminated|destroyed)$ ]]; then TERMINATED=1; break; fi
    sleep 5
  done
  test "$TERMINATED" = 1 || fail TEARDOWN_NOT_CONFIRMED 83
  echo 'TEARDOWN_CONFIRMED=YES'
  if [[ "$NODE_RC" -ne 0 ]]; then fail "PHYSICAL_NODE_RC_$NODE_RC" 84; fi
  echo 'WP2_P7B_R3=PASS_PHYSICAL_REQUALIFICATION_EVIDENCE_SURVIVAL'
  echo 'SCORED_AUTHORIZATION=BLOCKED'
}

case "$MODE" in
  prepare) prepare ;;
  finalize) finalize "$@" ;;
  *) echo 'usage: wp2_p7b_r3_execute.sh prepare | finalize <roundtrip.tar> <expected_sha>' >&2; exit 2 ;;
esac
