#!/usr/bin/env python3
"""WP2-P11 offline analysis helper.

No network/testbed access. Reads already extracted immutable evidence only.
FIT: reconstructs generated/received record identity sets for the 18 final cells.
POWDER: reconstructs per-level MQTT completeness for E1R4/E2/E3 and parses ping summaries.
"""
from pathlib import Path
import argparse, csv, json, re, statistics

PING_TXRX = re.compile(r"(\d+) packets transmitted,\s*(\d+) received")
PING_LOSS = re.compile(r"([\d.]+)% packet loss")
PING_RTT = re.compile(r"=\s*[\d.]+/([\d.]+)/")
POWDER_SEQ = re.compile(r"(?:cycle=(\d+)\s+)?db=(\d+)\s+seq=(\d+)")


def read_record_ids(path):
    vals=[]
    with Path(path).open() as f:
        for line in f:
            vals.append(json.loads(line)["record_id"])
    return vals


def analyze_fit(root):
    rows=[]
    root=Path(root)
    for rep in (1,2,3):
        rr=root/f"R{rep}"
        for arch in ("b0","w1"):
            for cond in ("c0","c1","c2"):
                key=arch+cond
                generated=read_record_ids(rr/key/"generated.jsonl")
                received=read_record_ids(rr/f"{key}_received.jsonl")
                gs,rs=set(generated),set(received)
                metrics=json.loads((rr/key/"edge_metrics.json").read_text())
                rows.append({
                    "replicate":rep,"architecture":arch.upper(),"condition":cond.upper(),
                    "generated":len(generated),"received_lines":len(received),
                    "unique_received":len(rs),"permanent_missing":len(gs-rs),
                    "duplicates":len(received)-len(rs),"unexpected":len(rs-gs),
                    "completeness_pct":100.0*len(gs&rs)/len(gs),
                    "reconnect_s":metrics.get("reconnect_s"),
                    "backlog_drain_s":metrics.get("backlog_drain_s"),
                    "restart_count":metrics.get("restart_count")})
    return rows


def parse_ping(path):
    text=Path(path).read_text(errors="replace")
    txrx=PING_TXRX.search(text); loss=PING_LOSS.search(text); rtt=PING_RTT.search(text)
    if not txrx or not loss:
        raise ValueError(f"unparseable ping: {path}")
    return int(txrx.group(1)),int(txrx.group(2)),float(loss.group(1)),float(rtt.group(1)) if rtt else None


def parse_powder_sequences(path):
    groups={}
    for line in Path(path).read_text(errors="replace").splitlines():
        m=POWDER_SEQ.search(line)
        if not m: continue
        key=(int(m.group(1)) if m.group(1) else None,int(m.group(2)))
        groups.setdefault(key,set()).add(int(m.group(3)))
    return groups


def analyze_powder(master_root):
    master=Path(master_root)/"remote"
    specs={
      "E1R4":("p8-e1r4-20260828A",[(None,48),(None,49),(None,50),(None,51),(None,52)]),
      "E2":("p8-e2-20260828A",[(None,52),(None,51),(None,50),(None,49),(None,48),(None,46)]),
      "E3":("p8-e3-20260828A",[(c,d) for c in (1,2,3) for d in (49,50,51,52)])}
    rows=[]
    for exp,(run,keys) in specs.items():
        ue=master/run/"nuc2"/"UE"; core=master/run/"nuc1"/"CORE"
        sent=parse_powder_sequences(ue/"sent.log"); recv=parse_powder_sequences(core/"received.log")
        for cyc,db in keys:
            s=sent.get((cyc,db),set()); r=recv.get((cyc,db),set())
            if exp=="E3": ping=ue/f"ping_c{cyc}_{db}dB.log"
            else: ping=ue/f"ping_{db}dB.log"
            tx,rx,loss,avg=parse_ping(ping)
            rows.append({"experiment":exp,"cycle":cyc,"attenuation_db":db,
                         "icmp_tx":tx,"icmp_rx":rx,"icmp_loss_pct":loss,"icmp_avg_rtt_ms":avg,
                         "mqtt_sent_unique":len(s),"mqtt_received_unique":len(r&s),
                         "mqtt_completeness_pct":100.0*len(r&s)/len(s) if s else None,
                         "missing_ids":sorted(s-r)})
    return rows


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--fit-root"); ap.add_argument("--powder-master")
    args=ap.parse_args(); out={}
    if args.fit_root: out["fit"]=analyze_fit(args.fit_root)
    if args.powder_master: out["powder"]=analyze_powder(args.powder_master)
    print(json.dumps(out,indent=2))

if __name__=="__main__": main()
