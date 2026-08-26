#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import importlib.metadata
import json
from pathlib import Path
import re
import sqlite3
import subprocess
import sys
import threading
import time

from wellpulse.powder_w1 import DurablePahoReplay
from wellpulse.records import make_record
from wellpulse.store import DurableQueue
from wellpulse.transport import PahoQoS1Config, PahoQoS1Session, make_run_client_id, make_run_topic

ATTENUATOR_IDS=(1,33,2,34)
Q0_DB=0
Q3_DB=55
PRE_Q0_S=60.0
Q3_S=120.0
H_APP_S=300.0


def utc_now(): return datetime.now(timezone.utc).isoformat()

def parse_utc(v):
    if v.endswith('Z'): v=v[:-1]+'+00:00'
    x=datetime.fromisoformat(v)
    if x.tzinfo is None: raise ValueError('timezone required')
    return x.astimezone(timezone.utc)

def run(cmd):
    p=subprocess.run(cmd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,check=False)
    return p.returncode,p.stdout.strip()

def zero_loss(s):
    m=re.search(r'([0-9]+(?:\.[0-9]+)?)% packet loss',s)
    return bool(m and float(m.group(1))==0.0)


def main():
    ap=argparse.ArgumentParser(description='WP-PWD01 non-scored Golden W1 sender')
    ap.add_argument('--run-id',required=True)
    ap.add_argument('--host',default='172.16.0.1')
    ap.add_argument('--port',type=int,default=8883)
    ap.add_argument('--ca-file',required=True)
    ap.add_argument('--output-dir',required=True)
    ap.add_argument('--service-ready-file',required=True)
    args=ap.parse_args()
    if importlib.metadata.version('paho-mqtt')!='2.1.0': raise RuntimeError('requires paho-mqtt==2.1.0')

    out=Path(args.output_dir); out.mkdir(parents=True,exist_ok=True)
    genp=out/'telemetry_generated.csv'; attp=out/'attenuation_timeline.csv'; qtp=out/'queue_timeline.csv'
    evp=out/'mqtt_events.jsonl'; sump=out/'sender_summary.json'; manp=out/'golden_manifest.json'; dbp=out/'w1_queue.sqlite'
    rfp=out/'rf_restore.ready'
    topic=make_run_topic(args.run_id,'GOLDEN'); cid=make_run_client_id(args.run_id,'GOLDENW1')

    def set_att(db):
        s=utc_now()
        for i in ATTENUATOR_IDS:
            rc,o=run(['/usr/local/etc/emulab/tmcc','attenuator',str(i),str(db)])
            if rc: raise RuntimeError(f'attenuator {i} rc={rc}: {o}')
        e=utc_now()
        with attp.open('a',newline='',encoding='utf-8') as f: csv.writer(f).writerow([s,e,db,' '.join(map(str,ATTENUATOR_IDS))])
        return e

    with attp.open('w',newline='',encoding='utf-8') as f: csv.writer(f).writerow(['command_start_utc','command_end_utc','programmed_attenuation_db','attenuator_ids'])
    route_rc,route=run(['ip','route','get',args.host])
    git_rc,git_sha=run(['git','rev-parse','HEAD'])
    manifest={'evidence_class':'NON_SCORED_WP2_GOLDEN_REHEARSAL','run_id':args.run_id,'architecture':'W1_REHEARSAL_ONLY','protocol_version':'v0.6','wellpulse_git_sha':git_sha if git_rc==0 else 'unknown','python_version':sys.version.split()[0],'paho_mqtt_version':importlib.metadata.version('paho-mqtt'),'sqlite_version':sqlite3.sqlite_version,'mqtt_topic':topic,'mqtt_client_id':cid,'rf':{'Q0_db':0,'Q3_db':55,'attenuator_ids':list(ATTENUATOR_IDS)},'schedule_s':{'pre_Q0':PRE_Q0_S,'Q3':Q3_S,'H_app':H_APP_S},'route_check':{'rc':route_rc,'output':route},'scored':False}
    manp.write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    if route_rc or 'tun_srsue' not in route: raise RuntimeError('experimental route gate failed')

    cfg=PahoQoS1Config(host=args.host,port=args.port,topic=topic,ca_file=args.ca_file,tls=True,qos=1,keepalive_s=60,clean_session=False,reconnect_min_delay_s=1,reconnect_max_delay_s=8,max_queued_messages=4096,max_inflight_messages=20)
    q=DurableQueue(dbp); sess=PahoQoS1Session(cfg,client_id=cid,event_log=evp)
    stop=threading.Event(); worker_error=[]; shared={}
    def replay_worker():
        qq=DurableQueue(dbp); rp=DurablePahoReplay(qq,sess); last=0.0
        try:
            with qtp.open('w',newline='',encoding='utf-8') as f:
                w=csv.writer(f); w.writerow(['utc','connected','pending_count','app_inflight_count','published_calls','puback_callbacks'])
                while not stop.is_set():
                    s=rp.pump_once(); shared['snap']=s; now=time.monotonic()
                    if now-last>=0.5:
                        w.writerow([utc_now(),s.connected,s.pending_count,s.app_inflight_count,s.published_calls,s.puback_callbacks]); f.flush(); last=now
                    stop.wait(0.05)
        except Exception as e: worker_error.append(f'{type(e).__name__}: {e}')
        finally: qq.close()

    summary={'run_id':args.run_id,'scored':False,'status':'STARTING','t_rf_restore':None,'t_service_ready':None,'cohort_record_count':None,'generated_record_count':0,'generation_max_lag_s':0.0,'final_replay_snapshot':None,'worker_error':None}
    th=None; generated=[]
    try:
        set_att(Q0_DB)
        rc,ping=run(['ping','-I','tun_srsue','-c','5','-W','2',args.host])
        if rc or not zero_loss(ping): raise RuntimeError('Q0 readiness failed')
        sess.connect(); deadline=time.monotonic()+20
        while time.monotonic()<deadline and not sess.snapshot()['connected']: time.sleep(0.1)
        if not sess.snapshot()['connected']: raise RuntimeError('MQTT connect failed')
        if sess.snapshot()['session_present'] is not False: raise RuntimeError('fresh session isolation failed')
        th=threading.Thread(target=replay_worker,daemon=True); th.start()

        with genp.open('w',newline='',encoding='utf-8') as gf:
            w=csv.DictWriter(gf,fieldnames=['record_id','generated_ts_utc','payload_sha256','payload_json']); w.writeheader(); gf.flush()
            t0=time.monotonic(); next_t=t0; seq=0; q3_done=False; restore_done=False; service_ready=None
            while True:
                if worker_error: raise RuntimeError(worker_error[-1])
                now=time.monotonic()
                if now>=next_t:
                    lag=max(0.0,now-next_t); summary['generation_max_lag_s']=max(summary['generation_max_lag_s'],lag)
                    seq+=1; rec=make_record(args.run_id,'BOOT-001',seq); q.enqueue(rec); generated.append((rec.record_id,rec.generated_at_utc))
                    w.writerow({'record_id':rec.record_id,'generated_ts_utc':rec.generated_at_utc,'payload_sha256':rec.checksum_sha256,'payload_json':rec.canonical_payload()}); gf.flush(); next_t+=1.0
                if not q3_done and now-t0>=PRE_Q0_S:
                    set_att(Q3_DB); q3_start=time.monotonic(); q3_done=True
                if q3_done and not restore_done and now-q3_start>=Q3_S:
                    t_rf=set_att(Q0_DB); summary['t_rf_restore']=t_rf; cutoff=parse_utc(t_rf); summary['cohort_record_count']=sum(parse_utc(ts)<=cutoff for _,ts in generated); rfp.write_text(t_rf+'\n'); restore_done=True
                if restore_done and service_ready is None and Path(args.service_ready_file).is_file():
                    text=Path(args.service_ready_file).read_text().strip(); service_ready=parse_utc(text); summary['t_service_ready']=service_ready.isoformat(); service_ready_mono=time.monotonic()
                if service_ready is not None and time.monotonic()-service_ready_mono>=H_APP_S:
                    summary['status']='GOLDEN_FIXED_HORIZON_COMPLETE'; break
                time.sleep(max(0.005,min(0.05,next_t-time.monotonic())))
        summary['generated_record_count']=len(generated)
    finally:
        try: set_att(Q0_DB)
        except Exception: pass
        stop.set()
        if th: th.join(timeout=5)
        try: sess.disconnect()
        except Exception: pass
        snap=shared.get('snap')
        if snap: summary['final_replay_snapshot']={'connected':snap.connected,'pending_count':snap.pending_count,'app_inflight_count':snap.app_inflight_count,'published_calls':snap.published_calls,'puback_callbacks':snap.puback_callbacks}
        summary['worker_error']=worker_error[-1] if worker_error else None
        summary['generated_record_count']=len(generated)
        sump.write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
        q.close()
    if summary['status']!='GOLDEN_FIXED_HORIZON_COMPLETE': return 20
    print('WP2_GOLDEN_SENDER=PASS'); return 0

if __name__=='__main__': raise SystemExit(main())
