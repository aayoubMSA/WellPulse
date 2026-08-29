#!/usr/bin/env python3
"""Generate the P18 architecture/evidence-role display and canonical CSV tables.

The script intentionally keeps FIT and POWDER on separate inferential paths and
creates no pooled cross-platform quantitative display.
"""
from pathlib import Path
import hashlib
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = Path(__file__).resolve().parent / "p18_outputs"
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9.0,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "svg.fonttype": "none",
})

fig, ax = plt.subplots(figsize=(7.16, 4.45))
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
ax.set_xlim(0, 12)
ax.set_ylim(0, 8)
ax.axis("off")

def box(cx,cy,w,h,title,sub=None,tfs=8.8,sfs=7.7):
    p = FancyBboxPatch((cx-w/2,cy-h/2),w,h,
        boxstyle="round,pad=0.02,rounding_size=0.04",
        fill=False, linewidth=0.9)
    ax.add_patch(p)
    ax.text(cx, cy+(0.13 if sub else 0), title, ha="center", va="center",
            fontweight="bold", fontsize=tfs)
    if sub:
        ax.text(cx, cy-0.21, sub, ha="center", va="center", fontsize=sfs)

def arrow(a,b,rad=0):
    ax.add_patch(FancyArrowPatch(a,b,arrowstyle="-|>",mutation_scale=9,
        linewidth=0.9,connectionstyle=f"arc3,rad={rad}"))

ax.text(0.35,7.55,"A  W1 record lifecycle",fontweight="bold",fontsize=10.5)
c=[1.15,3.45,5.75,8.05,10.50]
box(c[0],6.55,1.55,0.90,"Generate","telemetry record")
box(c[1],6.55,1.75,0.90,"Identity","ID + SHA-256")
box(c[2],6.55,1.75,0.90,"Durable queue","WAL • PENDING")
box(c[3],6.55,1.55,0.90,"Publish","MQTT attempt")
box(c[4],6.55,1.90,0.90,"Receiver","unique IDs")
for a,b in zip(c[:-1],c[1:]): arrow((a+0.88,6.55),(b-0.98,6.55))
box(10.50,5.12,1.90,0.76,"Reconcile","receiver-side",tfs=8.6,sfs=7.5)
arrow((10.50,6.10),(10.50,5.53))
box(8.05,5.12,1.55,0.76,"SENT","after success",tfs=8.6,sfs=7.5)
arrow((9.53,5.12),(8.84,5.12))
ax.text(6.86,5.58,"unavailable",ha="center",fontsize=7.3)
arrow((7.82,6.11),(6.35,5.70),rad=0.08)
arrow((6.35,5.70),(5.76,6.10),rad=0.08)
ax.plot([0.35,11.65],[4.42,4.42],linewidth=0.7)

ax.text(0.35,4.06,"B  Non-overlapping evidence roles",fontweight="bold",fontsize=10.5)
box(1.85,3.02,2.50,0.93,"FIT IoT-LAB","B0 vs W1 • C0/C1/C2",tfs=9.0,sfs=7.8)
box(1.85,1.84,2.50,0.93,"Record survival","completeness • backlog drain",tfs=8.7,sfs=7.5)
arrow((1.85,2.55),(1.85,2.32))
box(10.15,3.02,2.50,0.93,"POWDER","E0–E11 characterization",tfs=9.0,sfs=7.8)
box(10.15,1.84,2.50,0.93,"Path recovery","ICMP • MQTT • timing",tfs=8.7,sfs=7.5)
arrow((10.15,2.55),(10.15,2.32))
box(6.00,1.15,2.90,1.03,"Structured synthesis","failure-domain-aware\ntriangulation only",tfs=8.8,sfs=7.6)
arrow((3.10,1.84),(4.52,1.32)); arrow((8.90,1.84),(7.48,1.32))
ax.text(6.0,0.34,"No pooled cross-platform reliability statistic • no POWDER W1-vs-baseline effect",
        ha="center",va="center",fontsize=7.6)

stem = OUT / "Fig_P18_01_architecture_evidence_roles"
fig.savefig(stem.with_suffix(".pdf"))
fig.savefig(stem.with_suffix(".svg"))
fig.savefig(stem.with_suffix(".png"), dpi=600)
plt.close(fig)

rows = [
    ["Healthy reference","FIT C0","None","Final completeness","B0/W1 both complete in tested workload","Not universal reliability"],
    ["Broker delivery outage","FIT C1","Broker reachability","Receiver completeness; reconnect; W1 drain","Durability consequence vs non-durable B0","Not generic MQTT superiority"],
    ["Broker outage + gateway-process restart","FIT C2","Broker reachability + gateway process","Receiver completeness; W1 drain","Record-state survival across exact exec-restart treatment","Not node/power-failure guarantee"],
    ["Physical RF transition","POWDER E1–E3","Programmed attenuation","ICMP loss/RTT; MQTT completeness","Experiment-specific transition region","No universal 52 dB threshold"],
    ["RF-only recovery","POWDER E4 / E10-A","RF restoration","Recovery/non-recovery evidence","RF-only recovery not uniform across preserved cases","No deterministic recovery probability"],
    ["UE-assisted recovery","POWDER E5 / E10-B","RF restore + UE restart","First publish; first ping; receipt","Mechanism-specific recovery","Not generic 6 s recovery"],
    ["CORE-related recovery","POWDER E6 / E10-C-B","CORE services + RF restore","First ping; first publish","Mechanism-specific recovery","Not directly comparable to UE restart"],
    ["Combined recovery","POWDER E7","CORE + RF + UE sequence","Recovered path/application","Stress-case sequence behavior","Not all ordering permutations"],
    ["Broker-only fault control","POWDER E8 / E10-D","MQTT broker","Healthy LTE ping vs MQTT failure; upper bound","Service failure separable from radio health","E10-D not exact broker latency"],
    ["No-fault control","POWDER E9","None","Ping + MQTT unique delivery","Platform-specific control","No pooling with FIT C0"],
    ["UE-side replication","POWDER E11","UE restart sequence","UE-side recovery RTT/IP transition","One-sided repeatability evidence","No independent CORE/MQTT claim"],
]
pd.DataFrame(rows,columns=["Failure domain","Experiment","Manipulated component","Primary endpoint","Admissible interpretation","Prohibited overreach"]).to_csv(OUT/"Table_P18_01_failure_domain_taxonomy.csv",index=False)

split = [
    ["Main Figure 1","Architecture + evidence-role schematic","IC-08/IC-09 + Methods","MAIN"],
    ["Main Figure 2","FIT final unique-record completeness","IC-01/IC-02","MAIN"],
    ["Main Figure 3","POWDER transition / direction response","IC-04/IC-05","MAIN"],
    ["Main Figure 4","POWDER E3 repeatability","IC-04","MAIN"],
    ["Main Table 1","Failure-domain taxonomy","IC-06/IC-07/IC-08","MAIN"],
    ["Main Table 2","FIT run-level summary","IC-01/IC-02/IC-03","MAIN"],
    ["Main Table 3","Recovery endpoint semantics","IC-06/IC-07","MAIN"],
    ["Supplement Figure S1","FIT backlog-drain raw runs","IC-03","SUPPLEMENT"],
    ["Supplement Atlas","POWDER E0/E4–E11 visuals","supporting/limitations","SUPPLEMENT"],
    ["Supplement Register","Run validity + anomaly register","IC-09","SUPPLEMENT"],
    ["Artifact","Derived CSVs + scripts + manifests","reproducibility","ARTIFACT"],
]
pd.DataFrame(split,columns=["Slot","Display","Claim role","Destination"]).to_csv(OUT/"WP2_P18_MAIN_SUPPLEMENT_DISPLAY_SPLIT.csv",index=False)

manifest=[]
for p in sorted(OUT.iterdir()):
    if p.is_file() and p.name != "SHA256_MANIFEST.csv":
        manifest.append((p.name, hashlib.sha256(p.read_bytes()).hexdigest(), p.stat().st_size))
pd.DataFrame(manifest,columns=["file","sha256","bytes"]).to_csv(OUT/"SHA256_MANIFEST.csv",index=False)
