# WellPulse — Milestone Status

Last updated: 2026-08-25 late session, Africa/Cairo

## Scientific work packages

| WP | Scope | Weight | Progress | Status |
|---|---|---:|---:|---|
| WP0 | Novelty & Venue Lock | 8% | 100% | PASS — serious related-work/comparator benchmark attached |
| WP1 | Confirmatory Protocol & Statistics Freeze | 12% | 100% design work | PRE-SCORE COMPARATOR REVIEW OPEN |
| WP2 | RF Calibration & Measurement Validation | 15% | 0% | **NEXT / AUTHORIZED NON-SCORED STAGE** |
| WP3 | Conducted-RF Confirmatory Campaign | 30% | 0% | BLOCKED BY WP2 + comparator freeze + explicit scored authorization |
| WP4 | OTA External Replication | 15% | 0% | BLOCKED BY WP3 |
| WP5 | Analysis + Artifact + Paper Closure | 20% | 0% scientific closure | PREPARED, NOT EXECUTED |

Scientific weighted completion remains **20%**.

```text
WP0  ████████████████████  8/8
WP1  ████████████████████ 12/12 design work; comparator sufficiency under review
WP2  ░░░░░░░░░░░░░░░░░░░  0/15
WP3  ░░░░░░░░░░░░░░░░░░░  0/30
WP4  ░░░░░░░░░░░░░░░░░░░  0/15
WP5  ░░░░░░░░░░░░░░░░░░░  0/20

OVERALL  ████░░░░░░░░░░░░░░░░  20%
```

## POWDER infrastructure gates

```text
G0 Account + WellPulse project      ████████████████████ PASS
G1 Manual compute provisioning      ████████████████████ PASS
G2 Explicit-key SSH + teardown      ████████████████████ PASS
G3 Simulated stack/data path        ████████████████████ PASS
G4 Controlled physical-RF lifecycle ████████████████████ PASS
G5 RF impairment plumbing           ░░░░░░░░░░░░░░░░░░░ NEXT
```

G0–G4 are enabling infrastructure qualification and add **0%** scientific completion.

## G4 final accepted state

Canonical evidence: `evidence/powder/g4-ue-attach-2026-08-25.md`.

Successful rerun:

- experiment `WP-G4-CTRL-RF`;
- UUID `0e4269fb-06dd-432b-abec-4bca685a05af`;
- profile `srslte-controlled-rf`, RefSpec `a6da9656`;
- live binding: `enb1 -> nuc2`, `rue1 -> nuc1`;
- physical B210 network/eNodeB path PASS;
- physical B210 srsUE path PASS;
- LTE attach PASS;
- UE IP `172.16.0.2`, EPC SGi `172.16.0.1`;
- E-RAB/bearer establishment PASS;
- bounded user-plane test via `tun_srsue`: **5/5 replies, 0% loss**;
- manual termination PASS;
- final portal: no active experiments, `Current Usage: 0 Node Hours`.

**G4 = PASS.** No G4 result is scored science.

## Comparator gate

The durable-client issue remains open. B1 remains the matched same-Paho-Python comparator but is not the strongest durable MQTT client generally. Candidate `B2_MQTT_DURABLE_CLIENT` semantics must be locally qualified and the exact sensitivity amendment explicitly frozen before scoring.

`scored_runs_authorized = false`.

## Immediate next action

**G5 / WP2 — RF impairment and measurement calibration.**

Use the proven G4 lifecycle rather than rediscovering the platform. Automation may clone the proven G4 lifecycle. Any new RF-control/impairment layer must first receive one bounded manual qualification. Do not begin B1/W1/B2 scored runs.

An approved `nuc1+nuc2` fallback reservation still exists for **2026-08-26 19:00–22:00 Africa/Cairo**. It may be reused for G5/WP2 if the required RF-control path is prepared and manually bounded first; do not waste it on repeating G4.

## Critical path

```text
G4 controlled physical-RF lifecycle PASS
        ↓
G5 / WP2 RF impairment + measurement calibration
        ↓
close durable-client B2 comparator gate
        ↓
freeze Q0-Q3 + H + exact scored amendment if needed
        ↓
WP3 conducted scored campaign
        ↓
WP4 compact OTA replication
        ↓
WP5 deterministic analysis + artifact + manuscript closure
```

## Evidence boundary

G4 proves a controlled physical-RF LTE lifecycle and bounded user-plane connectivity on POWDER. It does not establish RF calibration, WellPulse/MQTT resilience effects, pump/hydraulic/agronomic performance, Siwa field performance, or generic rural generalization.