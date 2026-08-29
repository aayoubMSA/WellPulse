#!/usr/bin/env python3
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "analysis" / "p14_figures"
OUT.mkdir(parents=True, exist_ok=True)

fit = pd.read_csv(ROOT / "analysis" / "WP2_P11_FIT_RECONSTRUCTED_RUNS_2026-08-29.csv")
powder = pd.read_csv(ROOT / "analysis" / "WP2_P11_POWDER_DERIVED_METRICS_2026-08-29.csv")

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 8.5,
    "axes.labelsize": 8.5,
    "xtick.labelsize": 7.5,
    "ytick.labelsize": 7.5,
    "legend.fontsize": 7.0,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "svg.fonttype": "none",
    "axes.linewidth": 0.8,
    "lines.linewidth": 1.15,
    "lines.markersize": 4.8,
})

def save_all(fig, stem):
    fig.savefig(OUT / f"{stem}.svg", bbox_inches="tight")
    fig.savefig(OUT / f"{stem}.pdf", bbox_inches="tight")
    fig.savefig(OUT / f"{stem}.png", dpi=600, bbox_inches="tight")
    plt.close(fig)

# Figure 1 — FIT completeness
fig, ax = plt.subplots(figsize=(3.45, 2.45))
conditions = ["C0", "C1", "C2"]
x = np.arange(3)
archoff = {"B0": -0.13, "W1": 0.13}
repjit = {1: -0.035, 2: 0, 3: 0.035}
for arch, marker in [("B0", "o"), ("W1", "s")]:
    xs, ys = [], []
    for ci, cond in enumerate(conditions):
        for rep in [1, 2, 3]:
            r = fit[(fit.condition == cond) & (fit.architecture == arch) & (fit.replicate == rep)].iloc[0]
            xs.append(x[ci] + archoff[arch] + repjit[rep])
            ys.append(r.completeness_pct)
    ax.plot(xs, ys, marker=marker, linestyle="None", label=arch)
ax.set_xticks(x)
ax.set_xticklabels(["Healthy\n(C0)", "Broker outage\n(C1)", "Outage + gateway\nrestart (C2)"])
ax.set_ylabel("Final unique-record completeness (%)")
ax.set_ylim(77.5, 101.5)
ax.set_yticks([80, 85, 90, 95, 100])
ax.grid(axis="y", linewidth=0.45, alpha=0.3)
ax.legend(frameon=False, ncol=2, loc="lower left", borderaxespad=0.2)
fig.tight_layout(pad=0.35)
save_all(fig, "Fig1_FIT_completeness")

# Figure 2 — FIT W1 backlog drain
fig, ax = plt.subplots(figsize=(3.45, 2.35))
conds = ["C1", "C2"]
xpos = np.array([0, 1])
for rep, marker, jitter in [(1, "o", -0.055), (2, "s", 0), (3, "^", 0.055)]:
    vals = []
    for cond in conds:
        r = fit[(fit.architecture == "W1") & (fit.condition == cond) & (fit.replicate == rep)].iloc[0]
        vals.append(r.backlog_drain_s)
    ax.plot(xpos + jitter, vals, marker=marker, linestyle="None", label=f"Replicate {rep}")
means = [fit[(fit.architecture == "W1") & (fit.condition == c)].backlog_drain_s.mean() for c in conds]
for i, mean in enumerate(means):
    ax.hlines(mean, i - 0.16, i + 0.16, linewidth=1.25)
handles, labels = ax.get_legend_handles_labels()
handles.append(Line2D([0], [0], linestyle="-", label="Mean"))
labels.append("Mean")
ax.set_xticks(xpos)
ax.set_xticklabels(["Broker outage\n(C1)", "Outage + gateway\nrestart (C2)"])
ax.set_ylabel("W1 backlog-drain time (s)")
ax.set_ylim(67.15, 69.05)
ax.set_yticks([67.5, 68.0, 68.5, 69.0])
ax.grid(axis="y", linewidth=0.45, alpha=0.3)
ax.legend(handles, labels, frameon=False, ncol=2, loc="upper left", borderaxespad=0.2)
fig.tight_layout(pad=0.35)
save_all(fig, "Fig2_FIT_backlog_drain")

# Figure 3 — POWDER transition/direction
fig, ax = plt.subplots(figsize=(3.45, 2.55))
series = [
    ("E1R4", "-", "o", "Asc. ICMP", lambda d: 100 - d.icmp_loss_pct),
    ("E1R4", "-", "^", "Asc. MQTT", lambda d: d.mqtt_completeness_pct),
    ("E2", "--", "s", "Desc. ICMP", lambda d: 100 - d.icmp_loss_pct),
    ("E2", "--", "^", "Desc. MQTT", lambda d: d.mqtt_completeness_pct),
]
for exp, ls, marker, label, fn in series:
    d = powder[powder.experiment == exp].sort_values("attenuation_db")
    ax.plot(d.attenuation_db, fn(d), linestyle=ls, marker=marker, label=label)
ax.set_xlabel("Programmed attenuation (dB)")
ax.set_ylabel("Response / completeness (%)")
ax.set_xlim(45.6, 52.4)
ax.set_ylim(-2, 102)
ax.set_xticks([46, 48, 49, 50, 51, 52])
ax.set_yticks([0, 20, 40, 60, 80, 100])
ax.grid(linewidth=0.45, alpha=0.28)
ax.legend(frameon=False, ncol=2, loc="lower left", borderaxespad=0.25, columnspacing=0.8, handlelength=2.2)
fig.tight_layout(pad=0.35)
save_all(fig, "Fig3_POWDER_transition_direction")

# Figure 4 — POWDER E3 repeatability
fig, ax = plt.subplots(figsize=(3.45, 2.45))
for cycle, ls, marker in [(1, "-", "o"), (2, "--", "s"), (3, ":", "^")]:
    d = powder[(powder.experiment == "E3") & (powder.cycle == cycle)].sort_values("attenuation_db")
    ax.plot(d.attenuation_db, d.mqtt_completeness_pct, linestyle=ls, marker=marker, label=f"Cycle {cycle}")
ax.set_xlabel("Programmed attenuation (dB)")
ax.set_ylabel("MQTT unique-record completeness (%)")
ax.set_xlim(48.7, 52.3)
ax.set_ylim(20, 102)
ax.set_xticks([49, 50, 51, 52])
ax.set_yticks([20, 40, 60, 80, 100])
ax.grid(linewidth=0.45, alpha=0.28)
ax.legend(frameon=False, loc="lower left", borderaxespad=0.25)
fig.tight_layout(pad=0.35)
save_all(fig, "Fig4_POWDER_E3_repeatability")
