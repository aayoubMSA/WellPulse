#!/usr/bin/env python3
"""Generate the deterministic WellPulse P18R Figure-1 hotfix.

This generator consumes no AI-generated image asset. It verifies the canonical
source semantics that distinguish sender-local SENT state from receiver-side
delivery evidence, then renders PDF/SVG/600-dpi PNG outputs.
"""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

FIG_W = 7.16


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_source_semantics(repo: Path) -> None:
    powder_w1 = (repo / "src/wellpulse/powder_w1.py").read_text(encoding="utf-8")
    receiver = (repo / "src/wellpulse/receiver.py").read_text(encoding="utf-8")
    reconcile = (repo / "src/wellpulse/reconcile.py").read_text(encoding="utf-8")
    records = (repo / "src/wellpulse/records.py").read_text(encoding="utf-8")
    store = (repo / "src/wellpulse/store.py").read_text(encoding="utf-8")

    required = [
        ("powder_w1 mark_sent", "queue.mark_sent" in powder_w1),
        ("powder_w1 QoS1 acknowledged", "QoS1 publish was" in powder_w1 and "acknowledged" in powder_w1),
        ("receiver unique primary key", "record_id TEXT PRIMARY KEY" in receiver),
        ("reconcile completeness", '"completeness_pct"' in reconcile),
        ("record stable ID", "run_id" in records and "boot_id" in records and "sequence" in records),
        ("record SHA-256", "checksum_sha256" in records),
        ("queue WAL", "journal_mode=WAL" in store),
        ("queue synchronous FULL", "synchronous=FULL" in store),
        ("queue PENDING", "'PENDING'" in store or '"PENDING"' in store),
        ("queue SENT", "'SENT'" in store or '"SENT"' in store),
    ]
    failed = [name for name, ok in required if not ok]
    if failed:
        raise RuntimeError("canonical source-semantic assertion(s) failed: " + ", ".join(failed))


def render(out: Path) -> Path:
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 8.2,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
    })
    fig, ax = plt.subplots(figsize=(FIG_W, 5.35))
    fig.subplots_adjust(left=0.012, right=0.988, bottom=0.018, top=0.985)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    def box(x, y, w, h, title, sub=None, lw=0.85, ls="-", title_fs=7.8, sub_fs=6.3):
        patch = FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.006,rounding_size=0.012",
            fill=False, linewidth=lw, linestyle=ls, edgecolor="black",
        )
        ax.add_patch(patch)
        if sub:
            ax.text(x + w / 2, y + h * 0.63, title, ha="center", va="center",
                    fontweight="bold", fontsize=title_fs)
            ax.text(x + w / 2, y + h * 0.27, sub, ha="center", va="center", fontsize=sub_fs)
        else:
            ax.text(x + w / 2, y + h / 2, title, ha="center", va="center",
                    fontweight="bold", fontsize=title_fs)

    def arrow(x1, y1, x2, y2, ls="-", rad=0.0, lw=0.80):
        ax.add_patch(FancyArrowPatch(
            (x1, y1), (x2, y2),
            arrowstyle="-|>", mutation_scale=9,
            linewidth=lw, linestyle=ls, color="black",
            connectionstyle=f"arc3,rad={rad}",
        ))

    ax.text(0.015, 0.975, "A  W1 durable record and evidence lifecycle",
            ha="left", va="top", fontweight="bold", fontsize=9.3)

    y = 0.835
    h = 0.090
    top = [
        (0.020, 0.115, "Generate", "record"),
        (0.165, 0.145, "Stable identity", "run:boot:sequence\n+ SHA-256"),
        (0.340, 0.145, "Durable queue", "SQLite WAL\nPENDING"),
        (0.515, 0.120, "Publish", "MQTT QoS1"),
        (0.760, 0.185, "Receiver", "idempotent unique IDs"),
    ]
    for x, w, title, sub in top:
        box(x, y, w, h, title, sub)
    for i in range(3):
        x, w, *_ = top[i]
        nx = top[i + 1][0]
        arrow(x + w + 0.006, y + h / 2, nx - 0.006, y + h / 2)
    arrow(0.641, y + h / 2, 0.754, y + h / 2)

    box(0.505, 0.685, 0.140, 0.067, "Local SENT", "after QoS1 PUBACK",
        title_fs=7.3, sub_fs=5.9)
    arrow(0.575, y, 0.575, 0.752)
    ax.text(0.590, 0.786, "PUBACK", ha="left", va="center", fontsize=5.9)

    arrow(0.545, 0.825, 0.415, 0.825, ls="--", rad=-0.58, lw=0.72)
    ax.text(0.480, 0.765, "unavailable / retry", ha="center", va="center", fontsize=6.1)

    box(0.165, 0.685, 0.145, 0.067, "Conflict guard", "conflicting content → error",
        lw=0.72, ls="--", title_fs=7.1, sub_fs=5.8)
    arrow(0.238, y, 0.238, 0.752, ls="--", lw=0.72)

    box(0.760, 0.685, 0.185, 0.067, "Reconciliation", "generated IDs ↔ received IDs",
        title_fs=7.2, sub_fs=5.8)
    box(0.760, 0.575, 0.185, 0.067, "Reported endpoint", "final completeness",
        title_fs=7.2, sub_fs=5.9)
    arrow(0.8525, y, 0.8525, 0.752)
    arrow(0.8525, 0.685, 0.8525, 0.642)
    ax.text(0.575, 0.650, "sender-local state", ha="center", va="center", fontsize=6.0)
    ax.text(0.8525, 0.540, "receiver-side evidence authority", ha="center", va="center", fontsize=6.0)

    ax.plot([0.015, 0.985], [0.505, 0.505], linewidth=0.7, color="black")

    fit_x, fit_y, fit_w, fit_h = 0.020, 0.190, 0.455, 0.275
    ax.add_patch(FancyBboxPatch(
        (fit_x, fit_y), fit_w, fit_h,
        boxstyle="round,pad=0.008,rounding_size=0.012",
        fill=False, linewidth=0.9, edgecolor="black",
    ))
    ax.text(fit_x + 0.015, fit_y + fit_h - 0.026,
            "B  FIT IoT-LAB — record-state survival",
            ha="left", va="top", fontweight="bold", fontsize=8.0)
    box(fit_x + 0.025, 0.355, fit_w - 0.050, 0.055, "Design",
        "B0 vs W1 • C0/C1/C2 • 3 runs/cell • 10,000 records/run",
        title_fs=7.3, sub_fs=5.8)
    box(fit_x + 0.025, 0.285, fit_w - 0.050, 0.055, "Treatment",
        "C1 broker outage 3001–5000 • C2 + gateway exec restart",
        title_fs=7.3, sub_fs=5.8)
    box(fit_x + 0.025, 0.215, fit_w - 0.050, 0.055, "Endpoints",
        "receiver completeness • reconnect • W1 backlog drain",
        title_fs=7.3, sub_fs=5.8)
    arrow(fit_x + fit_w / 2, 0.355, fit_x + fit_w / 2, 0.340)
    arrow(fit_x + fit_w / 2, 0.285, fit_x + fit_w / 2, 0.270)

    pw_x, pw_y, pw_w, pw_h = 0.525, 0.190, 0.455, 0.275
    ax.add_patch(FancyBboxPatch(
        (pw_x, pw_y), pw_w, pw_h,
        boxstyle="round,pad=0.008,rounding_size=0.012",
        fill=False, linewidth=0.9, edgecolor="black",
    ))
    ax.text(pw_x + 0.015, pw_y + pw_h - 0.026,
            "C  POWDER — communication-path evidence",
            ha="left", va="top", fontweight="bold", fontsize=8.0)
    box(pw_x + 0.025, 0.355, pw_w - 0.050, 0.055, "Campaign",
        "E0–E11 controlled RF / service / recovery characterization",
        title_fs=7.3, sub_fs=5.8)
    box(pw_x + 0.025, 0.285, pw_w - 0.050, 0.055, "Failure domains",
        "RF • UE • CORE • broker • no-fault controls",
        title_fs=7.3, sub_fs=5.8)
    box(pw_x + 0.025, 0.215, pw_w - 0.050, 0.055, "Endpoints",
        "ICMP • MQTT unique delivery • mechanism-specific timing",
        title_fs=7.3, sub_fs=5.8)
    arrow(pw_x + pw_w / 2, 0.355, pw_x + pw_w / 2, 0.340)
    arrow(pw_x + pw_w / 2, 0.285, pw_x + pw_w / 2, 0.270)

    box(0.300, 0.075, 0.400, 0.075,
        "Two distinct resilience properties",
        "record-state survival  +  communication-path recovery",
        lw=1.05, title_fs=7.8, sub_fs=6.4)
    arrow(fit_x + fit_w / 2, fit_y, 0.355, 0.150, rad=0.10)
    arrow(pw_x + pw_w / 2, pw_y, 0.645, 0.150, rad=-0.10)
    ax.text(0.500, 0.036,
            "Complementary evidence only — no quantitative pooling and no POWDER W1-vs-baseline effect.",
            ha="center", va="center", fontsize=6.4)

    out.mkdir(parents=True, exist_ok=True)
    stem = out / "Figure01_system_evidence_architecture"
    pdf_meta = {
        "Title": "WellPulse Figure 1 — System and evidence architecture",
        "Author": "Dr. Ahmed Elsayed Ayoub",
        "Subject": "WellPulse resilient IoT telemetry; MSA University, Faculty of Engineering, Department of Computer Systems Engineering",
        "Keywords": "WellPulse, IoT, MQTT, FIT IoT-LAB, POWDER, reproducibility",
        "Creator": "WellPulse P18R F1 deterministic generator",
        "CreationDate": None,
        "ModDate": None,
    }
    svg_meta = {
        "Title": "WellPulse Figure 1 — System and evidence architecture",
        "Creator": "Dr. Ahmed Elsayed Ayoub; WellPulse P18R F1 deterministic generator",
        "Description": "Author affiliation: Assistant Professor of Computer Engineering, Department of Computer Systems Engineering, Faculty of Engineering, MSA University, Giza, Egypt.",
        "Date": "2026-08-29",
        "Rights": "Internal research artifact. Rights and venue-specific reuse terms require verification before external release.",
    }
    png_meta = {
        "Title": "WellPulse Figure 1 — System and evidence architecture",
        "Author": "Dr. Ahmed Elsayed Ayoub",
        "Affiliation": "Assistant Professor of Computer Engineering, Department of Computer Systems Engineering, Faculty of Engineering, MSA University, Giza, Egypt",
        "Copyright": "Internal research artifact; rights subject to applicable institutional/testbed/venue policies.",
        "Software": "WellPulse P18R F1 deterministic generator",
    }
    fig.savefig(stem.with_suffix(".pdf"), metadata=pdf_meta)
    fig.savefig(stem.with_suffix(".svg"), metadata=svg_meta)
    fig.savefig(stem.with_suffix(".png"), dpi=600, metadata=png_meta)
    plt.close(fig)
    return stem.with_suffix(".pdf")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", required=True)
    ap.add_argument("--out-dir", required=True)
    a = ap.parse_args()
    repo = Path(a.repo_root).resolve()
    out = Path(a.out_dir).resolve()
    verify_source_semantics(repo)
    pdf = render(out)
    print("Figure01 PDF SHA256", sha256(pdf))


if __name__ == "__main__":
    main()
