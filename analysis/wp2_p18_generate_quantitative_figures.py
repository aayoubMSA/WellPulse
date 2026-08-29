#!/usr/bin/env python3
"""Generate P18 publication-facing quantitative figures from frozen P11 values.

Percentage endpoints use a full 0–100% scale to avoid visual exaggeration.
"""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

OUT=Path(__file__).resolve().parent/'p18_outputs'
OUT.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({
    'font.family':'DejaVu Sans','font.size':9.0,'axes.labelsize':9.0,
    'xtick.labelsize':8.0,'ytick.labelsize':8.0,'legend.fontsize':8.0,
    'pdf.fonttype':42,'ps.fonttype':42,'svg.fonttype':'none',
    'axes.linewidth':0.8,'lines.linewidth':1.2,'lines.markersize':5.5,
})

def save(fig,stem):
    fig.savefig(OUT/f'{stem}.pdf')
    fig.savefig(OUT/f'{stem}.svg')
    fig.savefig(OUT/f'{stem}.png',dpi=600)
    plt.close(fig)

fit=[]
for rep in [1,2,3]:
    fit += [[rep,'B0','C0',100],[rep,'B0','C1',80],[rep,'B0','C2',80],
            [rep,'W1','C0',100],[rep,'W1','C1',100],[rep,'W1','C2',100]]
fit=pd.DataFrame(fit,columns=['rep','arch','cond','pct'])
fig,ax=plt.subplots(figsize=(3.5,2.72));fig.subplots_adjust(left=0.18,right=0.98,bottom=0.29,top=0.97)
x=np.arange(3);off={'B0':-0.10,'W1':0.10};jit={1:-0.025,2:0,3:0.025}
for arch,mk in [('B0','o'),('W1','s')]:
    xs=[];ys=[]
    for ci,c in enumerate(['C0','C1','C2']):
        for r in [1,2,3]:
            row=fit[(fit.arch==arch)&(fit.cond==c)&(fit.rep==r)].iloc[0]
            xs.append(ci+off[arch]+jit[r]);ys.append(row.pct)
    ax.plot(xs,ys,marker=mk,linestyle='None',label=arch)
ax.set_xticks(x);ax.set_xticklabels(['C0\nHealthy','C1\nBroker\noutage','C2\nOutage +\ngateway\nrestart'])
ax.set_ylabel('Final completeness (%)');ax.set_ylim(0,105);ax.set_yticks([0,20,40,60,80,100])
ax.grid(axis='y',linewidth=0.4,alpha=0.28);ax.legend(frameon=False,ncol=2,loc='lower left')
save(fig,'Fig_P18_02_FIT_completeness')

e1=pd.DataFrame([[48,0,100],[49,0,100],[50,0,100],[51,30,100],[52,60,65]],columns=['db','loss','mqtt'])
e2=pd.DataFrame([[52,65,55],[51,10,100],[50,0,100],[49,0,100],[48,0,100],[46,0,100]],columns=['db','loss','mqtt'])
fig,ax=plt.subplots(figsize=(3.5,2.65));fig.subplots_adjust(left=0.18,right=0.98,bottom=0.20,top=0.97)
for d,ls,mi,mm,lab1,lab2 in [(e1,'-','o','^','Asc. ICMP','Asc. MQTT'),(e2,'--','s','v','Desc. ICMP','Desc. MQTT')]:
    ds=d.sort_values('db')
    ax.plot(ds.db,100-ds.loss,linestyle=ls,marker=mi,label=lab1)
    ax.plot(ds.db,ds.mqtt,linestyle=ls,marker=mm,label=lab2)
ax.set_xlabel('Programmed attenuation (dB)');ax.set_ylabel('Response / completeness (%)')
ax.set_xlim(45.7,52.3);ax.set_ylim(0,105);ax.set_xticks([46,48,49,50,51,52]);ax.set_yticks([0,20,40,60,80,100])
ax.grid(linewidth=0.4,alpha=0.28);ax.legend(frameon=False,ncol=2,loc='lower left',columnspacing=0.7,handlelength=2.0)
save(fig,'Fig_P18_03_POWDER_transition_direction')

e3=pd.DataFrame([[1,49,100],[1,50,100],[1,51,100],[1,52,60],[2,49,100],[2,50,100],[2,51,95],[2,52,25],[3,49,100],[3,50,100],[3,51,100],[3,52,55]],columns=['cycle','db','mqtt'])
fig,ax=plt.subplots(figsize=(3.5,2.65));fig.subplots_adjust(left=0.18,right=0.98,bottom=0.20,top=0.97)
for cyc,ls,mk in [(1,'-','o'),(2,'--','s'),(3,':','^')]:
    d=e3[e3.cycle==cyc]
    ax.plot(d.db,d.mqtt,linestyle=ls,marker=mk,label=f'Cycle {cyc}')
ax.set_xlabel('Programmed attenuation (dB)');ax.set_ylabel('MQTT completeness (%)')
ax.set_xlim(48.8,52.2);ax.set_ylim(0,105);ax.set_xticks([49,50,51,52]);ax.set_yticks([0,20,40,60,80,100])
ax.grid(linewidth=0.4,alpha=0.28);ax.legend(frameon=False,loc='lower left')
save(fig,'Fig_P18_04_POWDER_E3_repeatability')
