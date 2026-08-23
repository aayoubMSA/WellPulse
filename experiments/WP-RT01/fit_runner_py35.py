#!/usr/bin/env python3
"""Python-3.5-compatible FIT execution adapter for WP-RT01.

Preserves the frozen WP-RT01 experiment semantics on the FIT A8 image.
"""
from __future__ import print_function
import argparse, datetime, hashlib, json, os, socket, sqlite3, ssl, subprocess, sys, time
try:
    import paho.mqtt.client as mqtt
except ImportError:
    mqtt = None
BROKER="mqtt4.iot-lab.info"; PORT=8883; OUTAGE_START=3001; OUTAGE_END=5000; RESTART_AT=4000

def utc_now():
    return datetime.datetime.utcnow().isoformat()+"Z"

def make_payload(run_id,boot_id,sequence):
    body={"run_id":run_id,"boot_id":boot_id,"sequence":sequence,"generated_at_utc":utc_now(),"source":"synthetic_modbus_like","payload":{"register_1":1000+sequence,"status":sequence%4},"quality_flag":"OK"}
    rid="%s:%s:%08d"%(run_id,boot_id,sequence); body["record_id"]=rid
    payload=json.dumps(body,sort_keys=True,separators=(",",":")); checksum=hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return rid,payload,checksum

class DurableQueue(object):
    def __init__(self,path):
        self.conn=sqlite3.connect(path); self.conn.execute("PRAGMA journal_mode=WAL"); self.conn.execute("PRAGMA synchronous=FULL")
        self.conn.execute("CREATE TABLE IF NOT EXISTS queue (record_id TEXT PRIMARY KEY,payload_json TEXT NOT NULL,checksum_sha256 TEXT NOT NULL,state TEXT NOT NULL DEFAULT 'PENDING')"); self.conn.commit()
    def enqueue(self,rid,payload,checksum): self.conn.execute("INSERT OR IGNORE INTO queue(record_id,payload_json,checksum_sha256,state) VALUES(?,?,?,'PENDING')",(rid,payload,checksum)); self.conn.commit()
    def pending_rows(self): return list(self.conn.execute("SELECT record_id,payload_json,checksum_sha256,state FROM queue WHERE state='PENDING' ORDER BY record_id"))
    def mark_sent(self,rid,commit=True):
        self.conn.execute("UPDATE queue SET state='SENT' WHERE record_id=?",(rid,));
        if commit: self.conn.commit()
    def commit_state(self): self.conn.commit()
    def count(self): return self.conn.execute("SELECT COUNT(*) FROM queue").fetchone()[0]
    def pending_count(self): return self.conn.execute("SELECT COUNT(*) FROM queue WHERE state='PENDING'").fetchone()[0]
    def close(self): self.conn.close()

class Publisher(object):
    def __init__(self,user,password,ca,client_id):
        if mqtt is None: raise RuntimeError("paho-mqtt is not available")
        self.connected=False; self.client=mqtt.Client(client_id=client_id,clean_session=True); self.client.username_pw_set(user,password)
        self.client.tls_set(ca_certs=ca,cert_reqs=ssl.CERT_REQUIRED,tls_version=ssl.PROTOCOL_TLSv1_2); self.client.on_connect=self._on_connect; self.client.on_disconnect=self._on_disconnect; self.client.loop_start()
    def _on_connect(self,c,u,f,rc): self.connected=(rc==0)
    def _on_disconnect(self,c,u,rc): self.connected=False
    def connect(self,timeout=10.0):
        t=time.time(); self.client.connect(BROKER,PORT,keepalive=20)
        while not self.connected and time.time()-t<timeout: time.sleep(.05)
        if not self.connected: raise RuntimeError("MQTT connect timeout")
        return time.time()-t
    def publish(self,topic,payload,timeout=5.0):
        info=self.client.publish(topic,payload,qos=1,retain=False)
        if info.rc!=mqtt.MQTT_ERR_SUCCESS: return False
        t=time.time()
        while not info.is_published() and time.time()-t<timeout: time.sleep(.01)
        return info.is_published()
    def close(self):
        try: self.client.disconnect()
        except Exception: pass
        try: self.client.loop_stop()
        except Exception: pass
        self.connected=False

def run_cmd(args,log,check=True):
    log.write("CMD %s\n"%" ".join(args)); log.flush(); rc=subprocess.call(args); log.write("RC %d\n"%rc); log.flush()
    if check and rc!=0: raise RuntimeError("command failed: %s"%" ".join(args))
    return rc

def set_outage(ip,enabled,log):
    rule=["-p","tcp","-d",ip,"--dport",str(PORT),"-j","REJECT"]
    run_cmd((["iptables","-I","OUTPUT","1"] if enabled else ["iptables","-D","OUTPUT"])+rule,log)

def assert_blocked(log):
    t=time.time(); blocked=False
    try: s=socket.create_connection((BROKER,PORT),2.0); s.close()
    except Exception: blocked=True
    log.write("outage_socket_blocked=%s elapsed_s=%.6f\n"%(("PASS" if blocked else "FAIL"),time.time()-t)); log.flush()
    if not blocked: raise RuntimeError("iptables outage did not block broker TCP 8883")

def load_auth(path):
    with open(path) as f: d=json.load(f)
    return d["username"],d["password"]
def write_json(path,obj):
    tmp=path+".tmp"
    with open(tmp,"w") as f: json.dump(obj,f,sort_keys=True,indent=2); f.write("\n"); f.flush(); os.fsync(f.fileno())
    os.rename(tmp,path)
def append_line(path,line):
    with open(path,"a") as f: f.write(line+"\n"); f.flush(); os.fsync(f.fileno())

def main():
    p=argparse.ArgumentParser(); p.add_argument("--run-id",required=True); p.add_argument("--architecture",choices=["B0","W1"],required=True); p.add_argument("--condition",choices=["C0","C1","C2"],required=True); p.add_argument("--topic",required=True); p.add_argument("--auth-file",required=True); p.add_argument("--ca-file",required=True); p.add_argument("--work-dir",required=True); p.add_argument("--records",type=int,default=10000); p.add_argument("--evidence-class",default="PREFINAL_REAL_A8_DRY_RUN_NOT_FINAL_EXPERIMENT"); p.add_argument("--resume",action="store_true"); a=p.parse_args()
    if a.records!=10000: raise SystemExit("WP-RT01 runner requires exactly 10000 records")
    if not os.path.isdir(a.work_dir): os.makedirs(a.work_dir)
    log_path=os.path.join(a.work_dir,"edge_events.log"); gen_path=os.path.join(a.work_dir,"generated.jsonl"); state_path=os.path.join(a.work_dir,"control_state.json"); queue_path=os.path.join(a.work_dir,"queue.sqlite"); metrics_path=os.path.join(a.work_dir,"edge_metrics.json")
    log=open(log_path,"a",1); user,password=load_auth(a.auth_file); broker_ip=socket.gethostbyname(BROKER)
    if a.resume:
        with open(state_path) as f: st=json.load(f)
        start=int(st["next_sequence"]); boot_no=int(st["boot_no"])+1; outage=bool(st["outage_active"]); generated=int(st["generated"]); published=int(st["published"]); reconnect_s=st.get("reconnect_s"); restarts=int(st.get("restart_count",0))+1; log.write("resume_utc=%s next_sequence=%d boot_no=%d\n"%(utc_now(),start,boot_no))
    else:
        start=1; boot_no=1; outage=False; generated=0; published=0; reconnect_s=None; restarts=0
        for path in (gen_path,state_path,metrics_path):
            try: os.remove(path)
            except OSError: pass
        if a.architecture=="W1":
            try: os.remove(queue_path)
            except OSError: pass
    queue=DurableQueue(queue_path) if a.architecture=="W1" else None; publisher=None; backlog_drain_s=None
    if not outage:
        publisher=Publisher(user,password,a.ca_file,"wp-%s-%d"%(a.run_id[-12:],boot_no)); connect_s=publisher.connect(); log.write("mqtt_connect_utc=%s connect_s=%.6f\n"%(utc_now(),connect_s))
    else: log.write("resume_during_outage=YES\n")
    try:
        seq=start
        while seq<=a.records:
            if a.condition in ("C1","C2") and seq==OUTAGE_START and not outage:
                if publisher: publisher.close(); publisher=None
                set_outage(broker_ip,True,log); outage=True; log.write("outage_start_utc=%s sequence=%d broker_ip=%s\n"%(utc_now(),seq,broker_ip)); assert_blocked(log)
            if a.condition in ("C1","C2") and seq==OUTAGE_END+1 and outage:
                set_outage(broker_ip,False,log); outage=False; t=time.time(); publisher=Publisher(user,password,a.ca_file,"wp-%s-%d-r"%(a.run_id[-10:],boot_no)); publisher.connect(); reconnect_s=time.time()-t; log.write("outage_end_utc=%s sequence=%d reconnect_s=%.6f\n"%(utc_now(),seq,reconnect_s))
                if queue:
                    t=time.time()
                    for row in queue.pending_rows():
                        if not publisher.publish(a.topic,row[1]): raise RuntimeError("failed to drain %s"%row[0])
                        queue.mark_sent(row[0],commit=False); published+=1
                    queue.commit_state(); backlog_drain_s=time.time()-t; log.write("backlog_drain_s=%.6f\n"%backlog_drain_s)
            boot_id="BOOT-%03d"%boot_no; rid,payload,checksum=make_payload(a.run_id,boot_id,seq); append_line(gen_path,payload); generated+=1
            if queue:
                queue.enqueue(rid,payload,checksum)
                if not outage:
                    if not publisher.publish(a.topic,payload): raise RuntimeError("publish failed %s"%rid)
                    queue.mark_sent(rid,commit=False); published+=1
                    if seq%100==0: queue.commit_state()
            elif not outage:
                if not publisher.publish(a.topic,payload): raise RuntimeError("baseline publish failed %s"%rid)
                published+=1
            if a.condition=="C2" and seq==RESTART_AT and restarts==0:
                if queue: queue.commit_state(); queue.close()
                write_json(state_path,{"next_sequence":seq+1,"boot_no":boot_no,"outage_active":outage,"generated":generated,"published":published,"reconnect_s":reconnect_s,"restart_count":restarts})
                log.write("gateway_process_restart_utc=%s after_sequence=%d\n"%(utc_now(),seq)); log.flush()
                if publisher: publisher.close()
                os.execv(sys.executable,[sys.executable,os.path.abspath(__file__),"--run-id",a.run_id,"--architecture",a.architecture,"--condition",a.condition,"--topic",a.topic,"--auth-file",a.auth_file,"--ca-file",a.ca_file,"--work-dir",a.work_dir,"--records",str(a.records),"--evidence-class",a.evidence_class,"--resume"])
            seq+=1
        if queue:
            if queue.pending_count()!=0: raise RuntimeError("W1 finished with pending records")
            queue.commit_state()
        write_json(metrics_path,{"evidence_class":a.evidence_class,"run_id":a.run_id,"architecture":a.architecture,"condition":a.condition,"records":a.records,"generated":generated,"published_qos1_acked":published,"queue_count":queue.count() if queue else 0,"queue_pending":queue.pending_count() if queue else 0,"restart_count":restarts,"reconnect_s":reconnect_s,"backlog_drain_s":backlog_drain_s,"outage_method":"iptables_REJECT_tcp_8883_records_3001_5000" if a.condition!="C0" else "none","restart_definition":"WellPulse_gateway_process_exec_restart_after_record_4000" if a.condition=="C2" else "none","completed_utc":utc_now()})
        print(open(metrics_path).read())
    finally:
        if publisher:
            try: publisher.close()
            except Exception: pass
        if outage:
            try: set_outage(broker_ip,False,log)
            except Exception: pass
        if queue:
            try: queue.close()
            except Exception: pass
        log.close()
if __name__=="__main__": main()
