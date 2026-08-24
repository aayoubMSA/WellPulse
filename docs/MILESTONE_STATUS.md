# WellPulse — Milestone Status

Last updated: 2026-08-25 01:42 Africa/Cairo

This is the compact dashboard for scientific WP completion, POWDER infrastructure gates, comparator status, critical path, and planning time.

## Scientific work packages

| WP | Scope | Weight | Progress | Status | Remaining active-work estimate |
|---|---|---:|---:|---|---:|
| WP0 | Novelty & Venue Lock | 8% | 100% | PASS — serious related-work benchmark added | 0 h core; manuscript check remains |
| WP1 | Confirmatory Protocol & Statistics Freeze | 12% | 100% design work | PRE-SCORE COMPARATOR REVIEW OPEN | small B2 semantics/audit task |
| WP2 | RF Calibration & Measurement Validation | 15% | 0% | NEXT after G4 | ~4–8 h |
| WP3 | Conducted-RF Confirmatory Campaign | 30% | 0% | BLOCKED BY WP2 + comparator freeze | ~6–10 h plus any compact B2 sensitivity |
| WP4 | OTA External Replication | 15% | 0% | BLOCKED BY WP3 | ~3–6 h |
| WP5 | Analysis + Artifact + Paper Closure | 20% | 0% scientific closure | PREPARED, NOT EXECUTED | ~12–20 h |

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
G4 Controlled physical-RF lifecycle ████████░░░░░░░░░░░░ SCHEDULED / LIFECYCLE PENDING
G5 RF impairment plumbing           ░░░░░░░░░░░░░░░░░░░ PENDING
```

G0–G4 are enabling infrastructure qualification and add **0%** scientific completion.

### G4 scheduled state

- profile `PowderProfiles/srslte-controlled-rf`;
- repo hash `a6da9656`;
- UE `srsLTE UE (B210)`;
- approved WellPulse reservation: `nuc1` + `nuc2`, one each;
- window: **2026-08-25 19:00–22:00 Africa/Cairo**;
- scheduled experiment: `WP-G4-CTRL-RF`;
- state after scheduling: `scheduled`;
- current usage after scheduling: `0 Node Hours`.

G4 PASS still requires READY -> actual manifest/radio binding -> explicit-key SSH -> controlled physical-RF LTE sanity -> clean terminate -> zero active usage.

Canonical G4 evidence:

- `evidence/powder/g4-live-discovery-2026-08-25.md`

## Serious related-work / comparator gate

Canonical artifacts:

- `docs/WP0_RELATED_WORK_BENCHMARK_2026-08-25.md`
- `docs/WP0_RELATED_WORK_MATRIX_2026-08-25.csv`
- `docs/WP0_COMPARATOR_AUDIT_2026-08-25.md`
- `docs/WP0_NOVELTY_VENUE_LOCK_2026-08-24.md`

The serious pre-G4 survey confirmed that MQTT resilience, buffering/store-and-forward, durable local databases, offline-first operation, identifiers, reconciliation, agricultural/cellular MQTT and testbed validation are all prior art in isolation.

The material new finding is that standard Eclipse Paho implementations outside Python can provide file-backed persistence and persistent disconnected buffering. Therefore current `B1_MQTT_QOS1` remains a useful same-Paho-Python matched comparator but is **not** claimed as the strongest durable MQTT-client configuration generally.

Provisional preferred defense:

1. retain B1 for the full matched B1/W1 primary campaign;
2. locally qualify a candidate `B2_MQTT_DURABLE_CLIENT` using authoritative durable-client settings;
3. if B2 semantics pass, freeze only a compact S2/S3 sensitivity comparison rather than inflate the full primary matrix;
4. keep B2 secondary/sensitivity evidence separate from the B1/W1 primary paired inference.

No scored execution is permitted until this comparator review is explicitly closed.

`scored_runs_authorized = false`.

G4 is not blocked because it is infrastructure-only.

## Time remaining

Previous planning estimate remains approximately:

- active hands-on work: **~27–48 hours**;
- best case: **~3–4 intensive working days** after infrastructure access is stable;
- realistic elapsed: **~5–8 calendar days**;
- resource constrained: **~1–2 weeks**.

A validated compact B2 sensitivity experiment may add a small amount of active work. It is not yet included as a fixed scored matrix and must not be estimated as a full third arm.

## Critical path

```text
G4 scheduled manual controlled-RF lifecycle
        ↓
G5 / WP2 user-plane + RF calibration + freeze Q0-Q3 and H
        ↓
close durable-client B2 comparator gate
        ↓
freeze any protocol v0.5 amendment before scoring
        ↓
WP3 24–36 primary B1/W1 conducted scored runs
        + compact B2 sensitivity only if qualified/frozen
        ↓
WP4 12-run compact OTA replication
        ↓
WP5 deterministic analysis + artifact + manuscript closure
```

## Immediate action

No POWDER action before the approved 19:00 Cairo window.

At 19:00:

`WP-G4-CTRL-RF -> READY -> manifest/radio binding -> SSH -> controlled LTE sanity -> terminate -> 0 Node Hours`

In the scientific-preparation lane, continue citation snowballing and durable-client comparator qualification work, but do not mutate the scored protocol or authorize runs until that evidence is frozen.

## Evidence boundary

Current accepted POWDER evidence through G3 proves infrastructure/plumbing and file-based LTE-stack feasibility only. A successful G4 will prove a controlled physical-RF lifecycle, not a WellPulse performance effect. No remote-testbed result validates pumps, hydraulics, groundwater, agronomy, Siwa field performance, or generic rural-field performance.
