# WellPulse — Milestone Status

Last updated: 2026-08-26 after G5 RF-state freeze, Africa/Cairo

## Scientific work packages

| WP | Scope | Weight | Progress | Status |
|---|---|---:|---:|---|
| WP0 | Novelty & Venue Lock | 8% | 100% | PASS — serious related-work/comparator benchmark attached |
| WP1 | Confirmatory Protocol & Statistics Freeze | 12% | 100% design work | PRE-SCORE COMPARATOR REVIEW OPEN |
| WP2 | RF Calibration & Measurement Validation | 15% | ACTIVE | **RF-STATE CALIBRATION PASS; H + remaining measurement/evidence gates OPEN** |
| WP3 | Conducted-RF Confirmatory Campaign | 30% | 0% | BLOCKED BY WP2 + comparator freeze + explicit scored authorization |
| WP4 | OTA External Replication | 15% | 0% | BLOCKED BY WP3 |
| WP5 | Analysis + Artifact + Paper Closure | 20% | 0% scientific closure | PREPARED, NOT EXECUTED |

Under gate-based credit, scientific weighted completion remains **20%** until WP2 closes.

```text
WP0  ████████████████████  8/8
WP1  ████████████████████ 12/12 design work; comparator sufficiency under review
WP2  ───────── ACTIVE ───  RF numeric calibration frozen; no weight credited yet
WP3  ░░░░░░░░░░░░░░░░░░░  0/30
WP4  ░░░░░░░░░░░░░░░░░░░  0/15
WP5  ░░░░░░░░░░░░░░░░░░░  0/20

OVERALL  ████░░░░░░░░░░░░░░░░  20%
```

## POWDER infrastructure/calibration gates

```text
G0 Account + WellPulse project      ████████████████████ PASS
G1 Manual compute provisioning      ████████████████████ PASS
G2 Explicit-key SSH + teardown      ████████████████████ PASS
G3 Simulated stack/data path        ████████████████████ PASS
G4 Controlled physical-RF lifecycle ████████████████████ PASS
G5 RF control + numeric calibration ████████████████████ PASS
```

G0–G5 are non-scored enabling/calibration work. G5 closes the numeric RF-state sub-gate but does not by itself close WP2 or add scientific percentage.

## G5 accepted state

Canonical freeze: `experiments/WP-PWD01/RF_CALIBRATION_FREEZE_v1.md`.
Canonical ledger: `evidence/powder/g5-rf-calibration-ledger-2026-08-26.md`.

Frozen programmed attenuation:

- Q0 = **0 dB** — strong/stable reference.
- Q1 = **40 dB** — degraded but continuously connected.
- Q2 = **52 dB** — near-threshold/intermittent; clean 20 s test = **6 replies / 12 misses**.
- Q3 = **55 dB** — effective application-data outage from first isolated valid test.

Clean boundary checks after bearer reset:

- +41 dB: 20/20 replies;
- +42 dB: 20/20 replies;
- +49 dB: 21 replies, 0 misses;
- +52 dB: 6 replies, 12 misses.

No further attenuation sweep is authorized.

## Technical invalidity learned during G5

Repeated severe RLF/re-attach testing eventually left the LTE user-plane bearer stale even while the UE remained attached and had an IP. Contaminated-period 48/50/52/54, 42/44/46/47 and first +41 classifications are retained for provenance but excluded from canonical RF-state classification.

Future scored blocks require an explicit Q0 user-plane readiness gate; attach/IP alone is insufficient.

## Comparator gate

The durable-client issue remains open. B1 remains the matched same-Paho-Python comparator but is not the strongest durable MQTT client generally. Candidate `B2_MQTT_DURABLE_CLIENT` semantics must be locally qualified and the exact sensitivity amendment explicitly frozen before scoring.

`scored_runs_authorized = false`.

## Immediate next action

If the live `WP-G5-RF-CAL` experiment is still active, preserve any desired sanitized ephemeral logs, leave attenuation at 0, terminate cleanly and verify zero active usage.

Then remain in WP2 and run the smallest valid non-scored W1 recovery pilot needed to calibrate/freeze common recovery horizon `H`; close the remaining measurement/evidence/analysis-pilot gates before WP3.

An approved fallback `nuc1+nuc2` reservation still exists for **2026-08-26 19:00–22:00 Africa/Cairo**. Do not spend it on RF hunting.

## Critical path

```text
G5 numeric RF calibration PASS
        ↓
freeze H + remaining WP2 measurement/evidence gates
        ↓
close durable-client B2 comparator gate
        ↓
explicit scored authorization
        ↓
WP3 conducted scored campaign
        ↓
WP4 compact OTA replication
        ↓
WP5 deterministic analysis + artifact + manuscript closure
```

## Evidence boundary

G5 establishes controlled physical-RF attenuation states and their accepted user-plane/radio behavior on the qualified LTE path. It does not establish B1/W1 scientific effects, pump/hydraulic/agronomic performance, Siwa field performance, or generic rural-field generalization.