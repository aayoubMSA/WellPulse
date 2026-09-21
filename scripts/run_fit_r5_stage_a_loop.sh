#!/usr/bin/env bash
set -euo pipefail

# R5 Stage-A scored loop only.
# PRECONDITION: FIT reservation, SSH access, MQTT auth, trust anchor, paho vendor,
# and qualified runner are already staged by an approved bootstrap.
# Executes R1,R2,R3 only. No automatic replacement and no Stage B.

: "${EXP_ID:?}"
: "${FIT_LOGIN:?}"
: "${SITE:?}"
: "${LOC:?}"
: "${SSH_KEY:?}"
: "${REMOTE_BASE:?}"

ROOT="${R5_ROOT:-r5-stage-a}"
FRONTEND="${FIT_LOGIN}@${SITE}.iot-lab.info"
mkdir -p "$ROOT"
SSH=(-i "$SSH_KEY" -o StrictHostKeyChecking=accept-new -o ConnectTimeout=20)

# Qualified-code immutability.
test "$(git rev-parse HEAD:experiments/WP-RT01/fit_runner_q0_instrumented_py35.py)" = "9a0585ecacc9bdb87ec469d9ea1ad9ce998ccc9e"
test "$(git rev-parse HEAD:experiments/WP-RT01/fit_runner_py35.py)" = "3683737f9756c8b96c4c2e41f4372fc388fadb7d"
test "$(git rev-parse HEAD:scripts/fit_rt01_stamp_stream.py)" = "51a31081990c4d92e99462f7c6cd88736260036e"

clock_sample() {
  local label="$1" outpath="$2"
  python3 - "$label" "$EXP_ID" "$LOC" "$FRONTEND" "$SSH_KEY" "$outpath" "$REMOTE_BASE" <<'PY'
import json,subprocess,sys,time
label,exp,loc,frontend,key,outpath,remote_base=sys.argv[1:]
ssh=['ssh','-i',key,'-o','StrictHostKeyChecking=accept-new','-o','ConnectTimeout=20',frontend]
def receiver():
    rows=[]
    for _ in range(9):
        t0=time.time()
        p=subprocess.run(ssh+['python3 -c "import time; print(\\"%.9f\\"%time.time())"'],
                         text=True,capture_output=True,check=True)
        t1=time.time(); remote=float(p.stdout.strip().splitlines()[-1]); mid=(t0+t1)/2
        rows.append({'t0':t0,'t1':t1,'remote':remote,'rtt_s':t1-t0,
                     'offset_remote_minus_controller_s':remote-mid,
                     'midpoint_bound_s':(t1-t0)/2})
    return {'samples':rows,'best':min(rows,key=lambda x:x['rtt_s'])}
def source():
    rows=[]
    for i in range(9):
        name='r5_clock_%s_%02d.txt'%(label,i)
        node='$HOME/'+remote_base+'/common/'+name
        front='~/'+remote_base+'/common/'+name
        cmd='python3 -c \'import time; print("%.9f"%time.time())\' > "'+node+'"'
        t0=time.time()
        p=subprocess.run(['iotlab-ssh','-i',exp,'run-cmd',cmd,'-l',loc],
                         text=True,capture_output=True,check=True)
        status=json.loads(p.stdout).get('run-cmd',{})
        if not status.get('0'): raise RuntimeError('A8 clock command failed')
        q=subprocess.run(ssh+['cat '+front],text=True,capture_output=True,check=True)
        t1=time.time(); remote=float(q.stdout.strip().splitlines()[-1]); mid=(t0+t1)/2
        rows.append({'t0':t0,'t1':t1,'remote':remote,'rtt_s':t1-t0,
                     'offset_remote_minus_controller_s':remote-mid,
                     'midpoint_bound_s':(t1-t0)/2,'status_map':status})
    return {'samples':rows,'best':min(rows,key=lambda x:x['rtt_s'])}
obj={'label':label,'source':source(),'receiver':receiver()}
obj['cross_host_bound_s']=obj['source']['best']['midpoint_bound_s']+obj['receiver']['best']['midpoint_bound_s']
open(outpath,'w').write(json.dumps(obj,indent=2,sort_keys=True)+'\n')
print(json.dumps({'label':label,'cross_host_bound_s':obj['cross_host_bound_s']},sort_keys=True))
PY
}

run_t1() {
  local rep="$1"
  local local_dir="$ROOT/$rep"
  local remote_run="$REMOTE_BASE/runs/$rep"
  local rid="R5-SA-${rep}-EXP${EXP_ID}"
  local topic="iotlab/${FIT_LOGIN}/wellpulse/r5-stage-a/${EXP_ID}/${rep}"
  mkdir -p "$local_dir"
  echo "$rid" > "$local_dir/run_id.txt"

  clock_sample "${rep}-pre" "$local_dir/clock_pre.json" | tee "$local_dir/clock_pre_summary.txt"

  recv_start=$(ssh "${SSH[@]}" "$FRONTEND" "python3 -c 'import time; print("%.9f"%time.time())'")
  ssh "${SSH[@]}" "$FRONTEND" "rm -rf ~/$remote_run; mkdir -p ~/$remote_run; cp ~/$REMOTE_BASE/common/mosq_auth.conf ~/.config/mosquitto_sub; chmod 600 ~/.config/mosquitto_sub; rm -f ~/$REMOTE_BASE/recv/${rep}.tsv ~/$REMOTE_BASE/recv/${rep}.err; nohup sh -c 'mosquitto_sub --cafile "\$HOME/$REMOTE_BASE/common/iot-lab-ca.pem" -h mqtt4.iot-lab.info -p 8883 -q 1 -t "$topic" | python3 "\$HOME/$REMOTE_BASE/common/fit_rt01_stamp_stream.py" > "\$HOME/$REMOTE_BASE/recv/${rep}.tsv"' > ~/$REMOTE_BASE/recv/${rep}.err 2>&1 & echo \$! > ~/$REMOTE_BASE/recv/${rep}.pid"
  sleep 2
  ssh "${SSH[@]}" "$FRONTEND" "kill -0 \$(cat ~/$REMOTE_BASE/recv/${rep}.pid)"

  iotlab-ssh -i "$EXP_ID" run-cmd     "cd "\$HOME/$REMOTE_BASE/common"; PYTHONPATH="\$HOME/$REMOTE_BASE/common/vendor" python3 "\$HOME/$REMOTE_BASE/common/fit_runner_q0_instrumented_py35.py" --run-id '$rid' --architecture W1 --condition C1 --topic '$topic' --auth-file "\$HOME/$REMOTE_BASE/common/wp_auth.json" --ca-file "\$HOME/$REMOTE_BASE/common/iot-lab-ca.pem" --work-dir "\$HOME/$remote_run" --records 10000 --evidence-class R5_SCORED_STAGE_A"     -l "$LOC" > "$local_dir/remote_command.json"

  python3 - "$local_dir/remote_command.json" <<'PY'
import json,sys
if not json.load(open(sys.argv[1])).get('run-cmd',{}).get('0',[]):
    raise SystemExit('source command failed')
PY

  for _ in $(seq 1 60); do
    n=$(ssh "${SSH[@]}" "$FRONTEND" "wc -l < ~/$REMOTE_BASE/recv/${rep}.tsv 2>/dev/null || echo 0" | tr -dc '0-9')
    n=${n:-0}; [[ "$n" -ge 10000 ]] && break; sleep 1
  done

  recv_stop=$(ssh "${SSH[@]}" "$FRONTEND" "python3 -c 'import time; print("%.9f"%time.time())'")
  recv_lines=$(ssh "${SSH[@]}" "$FRONTEND" "wc -l < ~/$REMOTE_BASE/recv/${rep}.tsv 2>/dev/null || echo 0" | tr -dc '0-9')
  recv_lines=${recv_lines:-0}
  printf '{"receiver_start_epoch_s":%s,"receiver_stop_epoch_s":%s,"raw_lines":%s}\n' "$recv_start" "$recv_stop" "$recv_lines" > "$local_dir/receiver_capture_meta.json"
  ssh "${SSH[@]}" "$FRONTEND" "pid=\$(cat ~/$REMOTE_BASE/recv/${rep}.pid 2>/dev/null || true); [ -n "\$pid" ] && kill "\$pid" >/dev/null 2>&1 || true; rm -f ~/.config/mosquitto_sub"
  scp -r "${SSH[@]}" "$FRONTEND:$remote_run" "$local_dir/source"
  scp "${SSH[@]}" "$FRONTEND:$REMOTE_BASE/recv/${rep}.tsv" "$local_dir/receiver_raw.tsv"
  scp "${SSH[@]}" "$FRONTEND:$REMOTE_BASE/recv/${rep}.err" "$local_dir/receiver.err" || true

  clock_sample "${rep}-post" "$local_dir/clock_post.json" | tee "$local_dir/clock_post_summary.txt"

  set +e
  python3 scripts/analyze_r5_stage_a_run.py     --run-dir "$local_dir" --run-id "$rid"     --out "$local_dir/run_analysis.json"     --reconciliation "$local_dir/reconciliation.csv"     | tee "$local_dir/analysis_console.txt"
  rc=${PIPESTATUS[0]}
  set -e

  find "$local_dir" -type f ! -name SHA256SUMS.txt -print0 | sort -z | xargs -0 sha256sum > "$local_dir/SHA256SUMS.txt"
  if [[ "$rc" -ne 0 ]]; then
    echo "R5_STAGE_A_ABORTED_INVALID_RUN=$rep" | tee "$ROOT/STAGE_A_ABORT.txt"
    exit "$rc"
  fi
}

# All three are executed regardless of scientific outcome; INVALID is the only stop.
run_t1 R1
run_t1 R2
run_t1 R3

python3 scripts/adjudicate_r5_stage_a.py   --run-analysis "$ROOT/R1/run_analysis.json"   --run-analysis "$ROOT/R2/run_analysis.json"   --run-analysis "$ROOT/R3/run_analysis.json"   --out "$ROOT/STAGE_A_VERDICT.json"   | tee "$ROOT/stage_a_adjudication_console.txt"

find "$ROOT" -type f ! -name SHA256SUMS.txt -print0 | sort -z | xargs -0 sha256sum > "$ROOT/SHA256SUMS.txt"
echo "R5_STAGE_A_EXECUTION_COMPLETE"
echo "No Stage-B run was executed."
