#!/usr/bin/env bash
set -euo pipefail

# Non-scored Q0 qualification for the WellPulse IEEE revival path.
# Run from a checkout of branch revival-r4-q0-instrumentation.
# This script does NOT execute R5 scored science.

: "${FIT_IDENTIFIER:?FIT_IDENTIFIER required}"
: "${FIT_PASSWORD:?FIT_PASSWORD required}"

ROOT="${Q0_ROOT:-q0-revival-live}"
SITE="${FIT_SITE:-grenoble}"
NODE_ID=""
LOC=""
mkdir -p "$ROOT" "$HOME/.ssh"
EXP_ID=""
FIT_LOGIN=""
FRONTEND=""
REMOTE_BASE="shared/.wellpulse-q0-revival"

cleanup() {
  set +e
  if [[ -n "$FRONTEND" && -f "$HOME/.ssh/id_rsa" ]]; then
    ssh -i "$HOME/.ssh/id_rsa" -o StrictHostKeyChecking=accept-new -o ConnectTimeout=20 "$FRONTEND"       "pkill -f 'mosquitto_sub.*wellpulse/q0-revival' >/dev/null 2>&1 || true; rm -f ~/.config/mosquitto_sub; rm -rf ~/$REMOTE_BASE" >/dev/null 2>&1 || true
  fi
  [[ -n "$EXP_ID" ]] && iotlab-experiment stop -i "$EXP_ID" >/dev/null 2>&1 || true
  if [[ -f "$HOME/.iotlabrc" && -f "$HOME/.ssh/id_rsa.pub" ]]; then
    python3 - <<'PY' >/dev/null 2>&1 || true
from pathlib import Path
from iotlabcli import auth
from iotlabcli.rest import Api
k=Path.home()/'.ssh'/'id_rsa.pub'
if k.exists():
    key=k.read_text().strip()
    user,password=auth._read_password_file()
    if user and password:
        api=Api(user,password)
        obj=api.get_ssh_keys()
        if key in obj.get('sshkeys',[]):
            obj['sshkeys']=[x for x in obj['sshkeys'] if x!=key]
            api.set_ssh_keys(obj)
PY
  fi
  rm -f "$HOME/.ssh/id_rsa" "$HOME/.ssh/id_rsa.pub" "$HOME/.iotlabrc" "$ROOT/wp_auth.json" "$ROOT/mosq_auth.conf"
}
trap cleanup EXIT

for cmd in python3 ssh scp ssh-keygen iotlab-experiment iotlab-ssh iotlab-auth; do
  command -v "$cmd" >/dev/null || { echo "missing prerequisite: $cmd" >&2; exit 2; }
done
python3 -m py_compile experiments/WP-RT01/fit_runner_py35.py experiments/WP-RT01/fit_runner_q0_instrumented_py35.py

bash scripts/fetch_mqtt_trust_anchor.sh "$ROOT/iot-lab-ca.pem" > "$ROOT/trust_anchor.txt"
python3 -m pip download --no-deps paho-mqtt==1.6.1 -d "$ROOT" >/dev/null
python3 - "$ROOT" <<'PY'
import sys,tarfile,zipfile,shutil
from pathlib import Path
r=Path(sys.argv[1]); src=next(r.glob('paho-mqtt-1.6.1*')); out=r/'paho_extract'; out.mkdir(exist_ok=True)
if src.suffix=='.whl': zipfile.ZipFile(src).extractall(out)
else: tarfile.open(src).extractall(out)
c=[p for p in list(out.glob('**/src/paho'))+list(out.glob('**/paho')) if (p/'mqtt').is_dir()]
if not c: raise SystemExit('paho package missing')
shutil.make_archive(str(r/'paho_py35'),'gztar',root_dir=str(c[0].parent),base_dir='paho')
PY

python3 - <<'PY'
import base64,os,re
from pathlib import Path
from iotlabcli.rest import Api
ident=os.environ['FIT_IDENTIFIER']; password=os.environ['FIT_PASSWORD']; p=Api(ident,password).method('user'); login=p.get('login') if isinstance(p,dict) else None
if not login or not re.fullmatch(r'[a-z][0-9a-z]{3,19}',login): raise SystemExit('No valid FIT login')
Path.home().joinpath('.iotlabrc').write_text(login+':'+base64.b64encode(password.encode()).decode())
Path.home().joinpath('.iotlabrc').chmod(0o600)
print(login)
PY
FIT_LOGIN=$(python3 - <<'PY'
from iotlabcli import auth
print(auth._read_password_file()[0])
PY
)
export FIT_LOGIN
FRONTEND="${FIT_LOGIN}@${SITE}.iot-lab.info"

chmod 700 "$HOME/.ssh"
ssh-keygen -t rsa -b 3072 -N '' -f "$HOME/.ssh/id_rsa" -C "WellPulse-Q0-revival" >/dev/null
chmod 600 "$HOME/.ssh/id_rsa"; chmod 644 "$HOME/.ssh/id_rsa.pub"
iotlab-auth --add-ssh-key > "$ROOT/add_ssh_key.log"

submit=$(iotlab-experiment submit -n "WP-Q0-revival" -d 45 -l "1,archi=a8:at86rf231+site=$SITE")
printf '%s\n' "$submit" > "$ROOT/reservation_submit.json"
EXP_ID=$(printf '%s' "$submit" | python3 -c 'import json,sys; print(json.load(sys.stdin)["id"])')
echo "$EXP_ID" > "$ROOT/experiment_id.txt"
iotlab-experiment wait -i "$EXP_ID" --timeout 300 --cancel-on-timeout > "$ROOT/reservation_wait.txt"
iotlab-experiment get -i "$EXP_ID" -n > "$ROOT/experiment_nodes.json"
NODE_ID=$(python3 - "$ROOT/experiment_nodes.json" <<'PY'
import json,re,sys
items=json.load(open(sys.argv[1])).get('items',[])
if not items:
    raise SystemExit('No A8 node allocated')
addr=items[0]['network_address']
m=re.search(r'(?:node-)?a8-(\d+)\.',addr)
if not m:
    raise SystemExit('Cannot parse allocated A8 node: '+addr)
print(m.group(1))
PY
)
LOC="${SITE},a8,${NODE_ID}"
printf '%s\n' "$LOC" > "$ROOT/resolved_loc.txt"
iotlab-ssh -i "$EXP_ID" wait-for-boot --max-wait 180 -l "$LOC" > "$ROOT/wait_for_boot.json"

SSH=(-i "$HOME/.ssh/id_rsa" -o StrictHostKeyChecking=accept-new -o ConnectTimeout=20)
umask 077
python3 - <<'PY' > "$ROOT/wp_auth.json"
import json,os
print(json.dumps({'username':os.environ['FIT_LOGIN'],'password':os.environ['FIT_PASSWORD']}))
PY
printf '%s\n%s\n' "-u $FIT_LOGIN" "-P $FIT_PASSWORD" > "$ROOT/mosq_auth.conf"

ssh "${SSH[@]}" "$FRONTEND" "mkdir -p ~/$REMOTE_BASE/common ~/$REMOTE_BASE/recv ~/$REMOTE_BASE/runs ~/.config; chmod 700 ~/$REMOTE_BASE"
scp "${SSH[@]}"   "$ROOT/iot-lab-ca.pem" "$ROOT/paho_py35.tar.gz" "$ROOT/wp_auth.json" "$ROOT/mosq_auth.conf"   experiments/WP-RT01/fit_runner_py35.py experiments/WP-RT01/fit_runner_q0_instrumented_py35.py   scripts/fit_rt01_stamp_stream.py   "$FRONTEND:$REMOTE_BASE/common/"
ssh "${SSH[@]}" "$FRONTEND" "cd ~/$REMOTE_BASE/common; mkdir -p vendor; tar -xzf paho_py35.tar.gz -C vendor; chmod 600 wp_auth.json mosq_auth.conf"

clock_sample() {
  local label="$1"
  python3 - "$label" "$EXP_ID" "$LOC" "$FRONTEND" "$HOME/.ssh/id_rsa" "$ROOT" "$REMOTE_BASE" <<'PY'
import json,subprocess,sys,time
label,exp,loc,frontend,key,root,remote_base=sys.argv[1:]

ssh_base=['ssh','-i',key,'-o','StrictHostKeyChecking=accept-new','-o','ConnectTimeout=20',frontend]

def receiver_sample():
    out=[]
    for _ in range(9):
        t0=time.time()
        p=subprocess.run(ssh_base+['python3 -c "import time; print(\\"%.9f\\"%time.time())"'],
                         stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,check=True)
        t1=time.time()
        remote=float(p.stdout.strip().splitlines()[-1])
        mid=(t0+t1)/2.0
        out.append({'t0':t0,'t1':t1,'remote':remote,'rtt_s':t1-t0,
                    'offset_remote_minus_controller_s':remote-mid,
                    'midpoint_bound_s':(t1-t0)/2.0})
    return {'method':'direct_frontend_ssh_midpoint','samples':out,
            'best':min(out,key=lambda x:x['rtt_s'])}

def source_sample():
    out=[]
    for i in range(9):
        name='q0_clock_source_%s_%02d.txt'%(label,i)
        node_path='$HOME/'+remote_base+'/common/'+name
        frontend_path='~/'+remote_base+'/common/'+name
        cmd='python3 -c \'import time; print("%.9f"%time.time())\' > "'+node_path+'"'
        t0=time.time()
        p=subprocess.run(['iotlab-ssh','-i',exp,'run-cmd',cmd,'-l',loc],
                         stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,check=True)
        try:
            status=json.loads(p.stdout).get('run-cmd',{})
        except Exception:
            raise RuntimeError('unparseable iotlab-ssh status: '+p.stdout[-500:])
        if not status.get('0'):
            raise RuntimeError('A8 clock command failed: '+p.stdout[-500:]+' '+p.stderr[-500:])
        q=subprocess.run(ssh_base+['cat '+frontend_path],
                         stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,check=True)
        t1=time.time()
        remote=float(q.stdout.strip().splitlines()[-1])
        mid=(t0+t1)/2.0
        out.append({'t0':t0,'t1':t1,'remote':remote,'rtt_s':t1-t0,
                    'offset_remote_minus_controller_s':remote-mid,
                    'midpoint_bound_s':(t1-t0)/2.0,
                    'status_map':status})
    return {'method':'A8_write_shared_then_frontend_read_midpoint_conservative',
            'samples':out,'best':min(out,key=lambda x:x['rtt_s'])}

source=source_sample()
receiver=receiver_sample()
obj={'label':label,'controller_epoch_s':time.time(),'source':source,'receiver':receiver,
     'cross_host_bound_s':source['best']['midpoint_bound_s']+receiver['best']['midpoint_bound_s']}
open(root+'/clock_'+label+'.json','w').write(json.dumps(obj,indent=2,sort_keys=True)+'\n')
print(json.dumps({'label':label,'cross_host_bound_s':obj['cross_host_bound_s'],
                  'source_best_rtt_s':source['best']['rtt_s'],
                  'receiver_best_rtt_s':receiver['best']['rtt_s']},sort_keys=True))
PY
}
clock_sample pre | tee "$ROOT/clock_pre_summary.txt"

run_case() {
  local key="$1" runner="$2" condition="$3"
  local rid="Q0-${key}-$(date +%s)"
  local topic="iotlab/${FIT_LOGIN}/wellpulse/q0-revival/${EXP_ID}/${key}"
  local local_dir="$ROOT/$key"
  local remote_run="$REMOTE_BASE/runs/$key"
  mkdir -p "$local_dir"
  ssh "${SSH[@]}" "$FRONTEND" "rm -rf ~/$remote_run; mkdir -p ~/$remote_run; cp ~/$REMOTE_BASE/common/mosq_auth.conf ~/.config/mosquitto_sub; chmod 600 ~/.config/mosquitto_sub; rm -f ~/$REMOTE_BASE/recv/${key}.tsv ~/$REMOTE_BASE/recv/${key}.err; nohup sh -c 'mosquitto_sub --cafile \"\$HOME/$REMOTE_BASE/common/iot-lab-ca.pem\" -h mqtt4.iot-lab.info -p 8883 -q 1 -t \"$topic\" | python3 \"\$HOME/$REMOTE_BASE/common/fit_rt01_stamp_stream.py\" > \"\$HOME/$REMOTE_BASE/recv/${key}.tsv\"' > ~/$REMOTE_BASE/recv/${key}.err 2>&1 & echo \$! > ~/$REMOTE_BASE/recv/${key}.pid"
  sleep 2
  local controller_start controller_end
  controller_start=$(python3 -c 'import time; print("%.9f"%time.time())')
  iotlab-ssh -i "$EXP_ID" --verbose run-cmd "cd \"\$HOME/$REMOTE_BASE/common\"; rm -rf \"\$HOME/$remote_run\"; mkdir -p \"\$HOME/$remote_run\"; PYTHONPATH=\"\$HOME/$REMOTE_BASE/common/vendor\" python3 \"\$HOME/$REMOTE_BASE/common/$runner\" --run-id '$rid' --architecture W1 --condition '$condition' --topic '$topic' --auth-file \"\$HOME/$REMOTE_BASE/common/wp_auth.json\" --ca-file \"\$HOME/$REMOTE_BASE/common/iot-lab-ca.pem\" --work-dir \"\$HOME/$remote_run\" --records 10000 --evidence-class Q0_NON_SCORED_QUALIFICATION" -l "$LOC" > "$local_dir/remote_command.json"
  controller_end=$(python3 -c 'import time; print("%.9f"%time.time())')
  printf '{"controller_start_s":%s,"controller_end_s":%s}\n' "$controller_start" "$controller_end" > "$local_dir/controller_timing.json"
  for _ in $(seq 1 60); do
    n=$(ssh "${SSH[@]}" "$FRONTEND" "wc -l < ~/$REMOTE_BASE/recv/${key}.tsv 2>/dev/null || echo 0" | tr -dc '0-9'); n=${n:-0}
    [[ "$n" -ge 10000 ]] && break
    sleep 1
  done
  ssh "${SSH[@]}" "$FRONTEND" "pid=\$(cat ~/$REMOTE_BASE/recv/${key}.pid 2>/dev/null || true); [ -n \"\$pid\" ] && kill \"\$pid\" >/dev/null 2>&1 || true; rm -f ~/.config/mosquitto_sub"
  scp -r "${SSH[@]}" "$FRONTEND:$remote_run" "$local_dir/"
  scp "${SSH[@]}" "$FRONTEND:$REMOTE_BASE/recv/${key}.tsv" "$local_dir/receiver_raw.tsv"
  scp "${SSH[@]}" "$FRONTEND:$REMOTE_BASE/recv/${key}.err" "$local_dir/receiver.err" || true
}

run_case frozen_c0 fit_runner_py35.py C0
run_case inst_c0 fit_runner_q0_instrumented_py35.py C0
run_case inst_c1 fit_runner_q0_instrumented_py35.py C1
clock_sample post | tee "$ROOT/clock_post_summary.txt"

python3 - "$ROOT" <<'PY'
import json,sys,datetime
root=sys.argv[1]
def readj(p): return json.load(open(p))
def iso_epoch(s):
    if s.endswith('Z'): s=s[:-1]
    dt=datetime.datetime.strptime(s,'%Y-%m-%dT%H:%M:%S.%f')
    return (dt-datetime.datetime(1970,1,1)).total_seconds()
def gen_stats(path):
    ts=[iso_epoch(json.loads(line)['generated_at_utc']) for line in open(path) if line.strip()]
    gaps=[b-a for a,b in zip(ts,ts[1:])]; xs=sorted(gaps)
    p99=xs[int(round(0.99*(len(xs)-1)))] if xs else None
    return {'n':len(ts),'runtime_s':ts[-1]-ts[0] if len(ts)>1 else 0.0,'p99_gap_s':p99,'max_gap_s':max(gaps) if gaps else None}
def rows(path): return [json.loads(x) for x in open(path) if x.strip()]
frozen=gen_stats(root+'/frozen_c0/frozen_c0/generated.jsonl')
inst=gen_stats(root+'/inst_c0/inst_c0/generated.jsonl')
overhead_pass=(inst['runtime_s'] <= max(1.25*frozen['runtime_s'], frozen['runtime_s']+5.0) and inst['p99_gap_s'] <= max(5.0*frozen['p99_gap_s'], frozen['p99_gap_s']+0.1) and inst['max_gap_s'] <= max(2.0*frozen['max_gap_s'], frozen['max_gap_s']+0.5))
mqtt=rows(root+'/inst_c1/inst_c1/q0_mqtt_events.ndjson'); tr=rows(root+'/inst_c1/inst_c1/q0_transport_events.ndjson')
conn=[x for x in mqtt if x.get('event_type')=='CONNACK_OK']; acks=[x for x in mqtt if x.get('event_type')=='PUBACK']; unresolved=[x for x in acks if x.get('record_id')=='UNRESOLVED']
transport_ok=any(x.get('event_type')=='OUTAGE_CONFIRMED' for x in tr) and any(x.get('event_type')=='RESTORE_APPLY' for x in tr) and any(x.get('event_type')=='PROBE_SUCCESS' for x in tr)
pre=readj(root+'/clock_pre.json'); post=readj(root+'/clock_post.json'); clock_bound=max(pre['cross_host_bound_s'],post['cross_host_bound_s'])
verdict={'evidence_class':'Q0_NON_SCORED_QUALIFICATION','frozen_c0':frozen,'instrumented_c0':inst,'q0_5_overhead_pass':overhead_pass,'q0_2_connack_count':len(conn),'q0_2_pass':len(conn)>=2,'q0_3_puback_count':len(acks),'q0_3_unresolved_pubacks':len(unresolved),'q0_3_pass':len(acks)>=10000 and len(unresolved)==0,'q0_6_cross_host_bound_s':clock_bound,'q0_6_pass':clock_bound<5.0,'q0_7_transport_pass':transport_ok,'q0_gate_pass':overhead_pass and len(conn)>=2 and len(acks)>=10000 and len(unresolved)==0 and clock_bound<5.0 and transport_ok,'note':'5 s is a qualification usability ceiling for clock resolution, not a scientific effect threshold.'}
open(root+'/Q0_LIVE_VERDICT.json','w').write(json.dumps(verdict,indent=2,sort_keys=True)+'\n'); print(json.dumps(verdict,indent=2,sort_keys=True))
if not verdict['q0_gate_pass']: raise SystemExit(3)
PY

find "$ROOT" -type f ! -name 'SHA256SUMS.txt' -print0 | sort -z | xargs -0 sha256sum > "$ROOT/SHA256SUMS.txt"
echo "Q0_LIVE_GATE=PASS"
echo "No scored R5 run was executed."
