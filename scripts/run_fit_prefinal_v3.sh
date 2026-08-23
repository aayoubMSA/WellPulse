#!/usr/bin/env bash
set -euo pipefail

: "${FIT_IDENTIFIER:?FIT_IDENTIFIER required}"
: "${FIT_PASSWORD:?FIT_PASSWORD required}"
RUN_DIR="${RUN_DIR:-fit-prefinal-v3}"
NODE_ID="${FIT_A8_NODE_ID:-100}"
SITE="saclay"
LOC="${SITE},a8,${NODE_ID}"
mkdir -p "$RUN_DIR" "$HOME/.ssh"
EXP_ID=""
FIT_LOGIN=""
FRONTEND=""

cleanup() {
  set +e
  if [[ -n "$FRONTEND" && -f "$HOME/.ssh/id_rsa" ]]; then
    ssh -i "$HOME/.ssh/id_rsa" -o StrictHostKeyChecking=accept-new -o ConnectTimeout=20 "$FRONTEND" \
      'pkill -f "mosquitto_sub.*wellpulse/prefinal" >/dev/null 2>&1 || true; rm -rf ~/shared/.wellpulse-prefinal-v3; rm -f ~/.config/mosquitto_sub' >/dev/null 2>&1 || true
  fi
  [[ -n "$EXP_ID" ]] && iotlab-experiment stop -i "$EXP_ID" >/dev/null 2>&1 || true
  if [[ -f "$HOME/.iotlabrc" && -f "$HOME/.ssh/id_rsa.pub" ]]; then
    python - <<'PY'
from pathlib import Path
from iotlabcli import auth
from iotlabcli.rest import Api
k=Path.home()/'.ssh'/'id_rsa.pub'
if k.exists():
    key=k.read_text().strip(); user,password=auth._read_password_file()
    if user and password:
        api=Api(user,password); obj=api.get_ssh_keys()
        if key in obj.get('sshkeys',[]):
            obj['sshkeys']=[x for x in obj['sshkeys'] if x!=key]; api.set_ssh_keys(obj)
PY
  fi
  rm -f "$HOME/.ssh/id_rsa" "$HOME/.ssh/id_rsa.pub" "$HOME/.iotlabrc" "$RUNNER_TEMP/wp_auth.json" "$RUNNER_TEMP/mosq_auth.conf"
}
trap cleanup EXIT

bash scripts/fetch_mqtt_trust_anchor.sh "$RUN_DIR/iot-lab-ca.pem" | tee "$RUN_DIR/trust_anchor.txt"
python -m pip download --no-deps paho-mqtt==1.6.1 -d "$RUN_DIR"
python - <<'PY'
import tarfile,zipfile,shutil
from pathlib import Path
r=Path('fit-prefinal-v3'); src=next(r.glob('paho-mqtt-1.6.1*')); out=r/'paho_extract'; out.mkdir(exist_ok=True)
if src.suffix=='.whl': zipfile.ZipFile(src).extractall(out)
else: tarfile.open(src).extractall(out)
c=[p for p in list(out.glob('**/src/paho'))+list(out.glob('**/paho')) if (p/'mqtt').is_dir()]
if not c: raise SystemExit('paho package missing')
shutil.make_archive(str(r/'paho_py35'),'gztar',root_dir=str(c[0].parent),base_dir='paho')
PY

python - <<'PY'
import base64,os,re
from pathlib import Path
from iotlabcli.rest import Api
ident=os.environ['FIT_IDENTIFIER']; password=os.environ['FIT_PASSWORD']; p=Api(ident,password).method('user'); login=p.get('login') if isinstance(p,dict) else None
if not login or not re.fullmatch(r'[a-z][0-9a-z]{3,19}',login): raise SystemExit('No valid FIT login')
Path('fit-prefinal-v3/resolved_login.marker').write_text('FIT generated login resolved without disclosure.\n')
Path.home().joinpath('.iotlabrc').write_text(login+':'+base64.b64encode(password.encode()).decode())
Path.home().joinpath('.iotlabrc').chmod(0o600)
with open(os.environ['GITHUB_ENV'],'a') as f: f.write('FIT_LOGIN=%s\n'%login)
PY
FIT_LOGIN=$(python - <<'PY'
from iotlabcli import auth
print(auth._read_password_file()[0])
PY
)
FRONTEND="${FIT_LOGIN}@${SITE}.iot-lab.info"

chmod 700 "$HOME/.ssh"
ssh-keygen -t rsa -b 3072 -N '' -f "$HOME/.ssh/id_rsa" -C "WellPulse-prefinal-v3-${GITHUB_RUN_ID}" >/dev/null
chmod 600 "$HOME/.ssh/id_rsa"; chmod 644 "$HOME/.ssh/id_rsa.pub"
iotlab-auth --add-ssh-key | tee "$RUN_DIR/add_ssh_key.log"

# Physical reservation removes scheduler node randomness; A8-100 already passed two capability smokes.
submit=$(iotlab-experiment submit -n "WP-RT01-prefinal-v3-${GITHUB_RUN_ID}" -d 45 -l "${SITE},a8,${NODE_ID}")
printf '%s\n' "$submit" | tee "$RUN_DIR/reservation_submit.json"
EXP_ID=$(printf '%s' "$submit" | python -c 'import json,sys; print(json.load(sys.stdin)["id"])')
echo "$EXP_ID" > "$RUN_DIR/experiment_id.txt"
iotlab-experiment wait -i "$EXP_ID" --timeout 300 --cancel-on-timeout | tee "$RUN_DIR/reservation_wait.txt"
iotlab-experiment get -i "$EXP_ID" -n > "$RUN_DIR/experiment_nodes.json"

iotlab-ssh -i "$EXP_ID" wait-for-boot --max-wait 180 -l "$LOC" > "$RUN_DIR/wait_for_boot.json"
cat "$RUN_DIR/wait_for_boot.json"
python - <<'PY'
import json
d=json.load(open('fit-prefinal-v3/wait_for_boot.json'))
if not d.get('wait-for-boot',{}).get('0',[]): raise SystemExit('Pinned A8 boot failed')
PY

SSH=(-i "$HOME/.ssh/id_rsa" -o StrictHostKeyChecking=accept-new -o ConnectTimeout=20)
JSON_AUTH="$RUNNER_TEMP/wp_auth.json"; MOSQ_AUTH="$RUNNER_TEMP/mosq_auth.conf"; umask 077
python - <<'PY' > "$JSON_AUTH"
import json,os
print(json.dumps({'username':os.environ['FIT_LOGIN'],'password':os.environ['FIT_PASSWORD']}))
PY
printf '%s\n%s\n' "-u $FIT_LOGIN" "-P $FIT_PASSWORD" > "$MOSQ_AUTH"
ssh "${SSH[@]}" "$FRONTEND" 'mkdir -p ~/shared/.wellpulse-prefinal-v3 && chmod 700 ~/shared/.wellpulse-prefinal-v3'
scp "${SSH[@]}" "$RUN_DIR/iot-lab-ca.pem" "$RUN_DIR/paho_py35.tar.gz" experiments/WP-RT01/fit_runner_py35.py "$JSON_AUTH" "$MOSQ_AUTH" "$FRONTEND:shared/.wellpulse-prefinal-v3/"
ssh "${SSH[@]}" "$FRONTEND" 'chmod 600 ~/shared/.wellpulse-prefinal-v3/wp_auth.json ~/shared/.wellpulse-prefinal-v3/mosq_auth.conf; cd ~/shared/.wellpulse-prefinal-v3; mkdir -p vendor recv; tar -xzf paho_py35.tar.gz -C vendor'
rm -f "$JSON_AUTH" "$MOSQ_AUTH"

iotlab-ssh -i "$EXP_ID" --verbose run-cmd 'PYTHONPATH="$HOME/shared/.wellpulse-prefinal-v3/vendor" python3 -c "import paho.mqtt.client; print(\"paho_import=PASS\")"' -l "$LOC" | tee "$RUN_DIR/paho_import.json"
grep -F '"0"' "$RUN_DIR/paho_import.json"

run_case() {
  local key="$1" arch="$2" cond="$3" expect="$4"
  local rid="PREFINAL-${arch}-${cond}-${GITHUB_RUN_ID}"
  local topic="iotlab/${FIT_LOGIN}/wellpulse/prefinal/${GITHUB_RUN_ID}/${key}"
  ssh "${SSH[@]}" "$FRONTEND" "mkdir -p ~/.config; rm -f ~/shared/.wellpulse-prefinal-v3/recv/${key}.jsonl; cp ~/shared/.wellpulse-prefinal-v3/mosq_auth.conf ~/.config/mosquitto_sub; chmod 600 ~/.config/mosquitto_sub; nohup mosquitto_sub --cafile ~/shared/.wellpulse-prefinal-v3/iot-lab-ca.pem -h mqtt4.iot-lab.info -p 8883 -q 1 -C ${expect} -t '$topic' > ~/shared/.wellpulse-prefinal-v3/recv/${key}.jsonl 2>~/shared/.wellpulse-prefinal-v3/recv/${key}.err &"
  sleep 2
  iotlab-ssh -i "$EXP_ID" --verbose run-cmd "rm -rf \"\$HOME/shared/.wellpulse-prefinal-v3/${key}\"; mkdir -p \"\$HOME/shared/.wellpulse-prefinal-v3/${key}\"; PYTHONPATH=\"\$HOME/shared/.wellpulse-prefinal-v3/vendor\" python3 \"\$HOME/shared/.wellpulse-prefinal-v3/fit_runner_py35.py\" --run-id '$rid' --architecture '$arch' --condition '$cond' --topic '$topic' --auth-file \"\$HOME/shared/.wellpulse-prefinal-v3/wp_auth.json\" --ca-file \"\$HOME/shared/.wellpulse-prefinal-v3/iot-lab-ca.pem\" --work-dir \"\$HOME/shared/.wellpulse-prefinal-v3/${key}\" --records 10000" -l "$LOC" 2>&1 | tee "$RUN_DIR/${key}_remote.log"
  grep -F '"0"' "$RUN_DIR/${key}_remote.log"
  ssh "${SSH[@]}" "$FRONTEND" "for i in \$(seq 1 30); do n=\$(wc -l < ~/shared/.wellpulse-prefinal-v3/recv/${key}.jsonl 2>/dev/null || echo 0); [ \"\$n\" -ge ${expect} ] && break; sleep 1; done; wc -l ~/shared/.wellpulse-prefinal-v3/recv/${key}.jsonl; rm -f ~/.config/mosquitto_sub"
  scp -r "${SSH[@]}" "$FRONTEND:shared/.wellpulse-prefinal-v3/${key}" "$RUN_DIR/"
  scp "${SSH[@]}" "$FRONTEND:shared/.wellpulse-prefinal-v3/recv/${key}.jsonl" "$RUN_DIR/${key}_received.jsonl"
  scp "${SSH[@]}" "$FRONTEND:shared/.wellpulse-prefinal-v3/recv/${key}.err" "$RUN_DIR/${key}_receiver.err" || true
}

run_case w1c2 W1 C2 10000
run_case b0c1 B0 C1 8000

python - <<'PY'
import json
from pathlib import Path
root=Path('fit-prefinal-v3')
def ids(p): return [json.loads(x)['record_id'] for x in Path(p).read_text().splitlines() if x.strip()]
out={}
for key in ('w1c2','b0c1'):
    g=ids(root/key/'generated.jsonl'); r=ids(root/(key+'_received.jsonl')); gs=set(g); rs=set(r)
    out[key]={'evidence_class':'PREFINAL_REAL_A8_DRY_RUN_NOT_FINAL_EXPERIMENT','generated':len(g),'cloud_received':len(r),'cloud_unique':len(rs),'duplicates':len(r)-len(rs),'permanent_missing':len(gs-rs),'completeness_pct':100.0*len(rs)/len(g)}
assert out['w1c2']==dict(out['w1c2'], generated=10000, cloud_received=10000, cloud_unique=10000, duplicates=0, permanent_missing=0, completeness_pct=100.0)
assert out['b0c1']['generated']==10000 and out['b0c1']['cloud_received']==8000 and out['b0c1']['cloud_unique']==8000 and out['b0c1']['duplicates']==0 and out['b0c1']['permanent_missing']==2000 and abs(out['b0c1']['completeness_pct']-80.0)<1e-9
(root/'reconciliation.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n'); print(json.dumps(out,indent=2,sort_keys=True))
PY

python - <<'PY'
import json,os
from datetime import datetime,timezone
from pathlib import Path
p=Path('fit-prefinal-v3')
(p/'metadata.json').write_text(json.dumps({'evidence_class':'PREFINAL_REAL_A8_DRY_RUN_NOT_FINAL_EXPERIMENT','github_run_id':os.getenv('GITHUB_RUN_ID'),'git_commit':os.getenv('GITHUB_SHA'),'fit_experiment_id':open(p/'experiment_id.txt').read().strip(),'site':'saclay','node_id':'100','outage_method':'iptables REJECT broker TCP 8883 records 3001-5000','restart_definition':'gateway process exec restart after record 4000','trust_anchor':'ISRG Root X1 SHA256 fingerprint pinned','end_utc':datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')},indent=2)+'\n')
PY
find "$RUN_DIR" -type f -print0 | sort -z | xargs -0 sha256sum > "$RUN_DIR/SHA256SUMS.txt"
echo PREFINAL_GATE=PASS
