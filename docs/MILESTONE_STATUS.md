# WellPulse — Milestone Status

Last updated: 2026-08-27 after **P7B-R2 one-replacement requalification contract freeze PASS**.

## Scientific work packages

| WP | Scope | Weight | Credited progress | Status |
|---|---|---:|---:|---|
| WP0 | Novelty & Venue Lock | 8% | 8/8 | PASS |
| WP1 | Confirmatory Protocol & Statistics Freeze | 12% | 12/12 | PASS / FROZEN |
| WP2 | RF Calibration & Measurement Validation | 15% | gate-open | **ACTIVE — pre-score physical qualification still blocked** |
| WP3 | Conducted-RF Confirmatory Campaign | 30% | 0/30 | BLOCKED ON WP2 |
| WP4 | OTA External Replication | 15% | 0/15 | BLOCKED |
| WP5 | Analysis + Artifact + Paper Closure | 20% | 0/20 scientific closure | PREPARED, NOT EXECUTED |

Under gate-based scientific credit, weighted completion remains **20%** until WP2 closes.

## WP2 management/readiness decomposition

| Patch | Scope | Internal share | Status |
|---|---|---:|---|
| WP2-P1 | RF Foundation | 20% | PASS / FROZEN |
| WP2-P2 | Recovery Semantics | 15% | PASS / FROZEN |
| WP2-P3 | Platform Compatibility | 20% | PASS / CLOSED |
| WP2-P4 | Pre-Golden Reconciliation / AUDIT-R1 | 15% | PASS / CLOSED |
| WP2-P5 | HCI & Raw-Evidence Closure | 10% | PASS / CLOSED |
| WP2-P6 | One clean non-scored Golden | 15% | PASS_RECOVERED_SINGLE_RUN / CLOSED |
| WP2-P7 | Reusable-path hardening + scored authorization decision | 5% | HARDENING PASS / SCORED AUTHORIZATION BLOCKED |

`WP2_MANAGEMENT_READINESS_PROGRESS=95/100`

The remaining 5/100 is gated by successful pre-score physical qualification plus the immutable pre-score authorization snapshot. R1 and R2 are repair/authority-control patches and create no additional management or scientific credit.

## Frozen scientific state

- FIT IoT-LAB: FINAL PASS.
- POWDER G0-G5: PASS.
- RF calibration: PASS / FROZEN.
- Q0/Q1/Q2/Q3 = `0/40/52/55 dB`.
- attenuation IDs `1 33 2 34` move together.
- pre-impairment Q0 = 60 s.
- Q3 = 120 s.
- S3 gateway restart = 60 s into Q3.
- primary cohort cutoff = `t_rf_restore`.
- `t_rf_restore`, `t_service_ready`, `t_app_complete` remain distinct.
- `H_app=300 s` from `t_service_ready`.
- primary endpoint remains `completeness_300` at `t_service_ready + 300 s`.
- no outcome-derived/W1-derived/Golden-derived/scored-derived horizon re-estimation.
- H1 remains valid adverse non-scored evidence.
- K1-K8 remain PASS / CLOSED absent material interface change.

## P6/P7 baseline

- `WP2_P6=PASS_RECOVERED_SINGLE_RUN`.
- P6 valid run `wp2-p6r-33099648133-20260827T174149Z`: primary cohort 181, valid by 300 s 181/181, `completeness_300=1.0`.
- P6 raw evidence, `/proj` escrow, independent artifact round-trip and teardown: PASS.
- `WP2_P7_HARDENING_QA=PASS`.
- scored authorization remained blocked on mandatory physical qualification.

## P7B qualification history

| P7B patch | Status | Key evidence |
|---|---|---|
| A | PASS | original offline contract freeze + 41/41 tests |
| B | PASS | implementation/reconstruction + 56/56 tests + B2 Java semantics PASS |
| C | **BLOCKED** | first authorized reservation stopped in B1 readiness before measurement |
| D | **BLOCKED STRICT COMPLETENESS** | declared roots preserved/read back; receiver event ledger unrecovered; teardown complete |
| E | **PASS CANONICAL BLOCKED CLOSURE** | failed/partial result frozen without relabelling |
| R1 | **PASS OFFLINE** | receiver-path repair + fail-fast diagnostics + 65/65 tests |
| R2 | **PASS OFFLINE** | one-replacement authority contract + controller static gate + 73/73 tests |

Successful P7B physical-qualification credit remains **40/100** from A+B only.

### First P7B-C reservation

- UUID `26b6f315-459d-4a56-9167-69228e339f24`;
- name `wp7b3016138`;
- GitHub run `33113016138`;
- reservation READY, core/UE SSH PASS, frozen profile matched;
- B1 Q0 route via `tun_srsue` PASS;
- five Q0 probes at 0% packet loss;
- TLS/MQTT readiness PASS;
- broker proved receiver connected/subscribed/alive;
- controller timed out on the expected receiver event ledger;
- completed cells: NONE;
- scientific measurement started: NO;
- retained verdict: `WP2_P7B_C=BLOCKED:RECEIVER_CONNECT_TIMEOUT`.

Root cause remains an orchestration/evidence-path quoting defect, not demonstrated LTE/MQTT failure.

### P7B-D preservation

- first attempt `33114265831`: fail-closed before persistence due path quoting defect;
- retry `33114517583`, job `98665610066`: preservation/read-back/teardown mechanics SUCCESS for captured declared roots;
- GitHub artifact ID `9663926250`;
- deterministic inner TAR SHA-256 `f49263f77d673cf5961dd6efb3b0ce2a3d7dde5969d48f20e0c383f105693877`;
- expected `receiver_events.jsonl` not recovered before teardown;
- strict verdict: `WP2_P7B_D=BLOCKED_STRICT_COMPLETENESS_RECEIVER_EVENT_LEDGER_NOT_RECOVERED`.

## P7B-R1 — operational repair

Canonical closure:

`docs/WP2_P7B_R1_RECEIVER_PATH_OBSERVABILITY_CLOSURE_2026-08-27.md`

Verdict:

`WP2_P7B_R1=PASS_OFFLINE_RECEIVER_PATH_OBSERVABILITY_QA`

R1 froze:

- absolute remote-path contract rejecting literal `$HOME`/`~`;
- repaired node entrypoint `scripts/wp2_p7b_c_node_r1.py`;
- writer/watcher path equality;
- receiver early-exit fail-fast;
- bounded GitHub-compatible receiver/broker/route/Q0/TLS/runtime diagnostics;
- absolute-path/hash preservation helpers.

Accepted Local Unit Tests: run `33116073295`, job `98670934415`, **65/65 PASS**.

## P7B-R2 — one-replacement authority freeze

Canonical closure:

`docs/WP2_P7B_R2_REQUALIFICATION_CONTRACT_FREEZE_2026-08-27.md`

Machine contract:

`experiments/WP-PWD01/p7b-requalification-r2-contract.json`

Verdict:

`WP2_P7B_R2=PASS_ONE_REPLACEMENT_CONTRACT_FREEZE`

Decision:

`REQUALIFICATION_DECISION=GO_ONE_REPLACEMENT_NON_SCORED`

Frozen replacement authority:

- authority ID `P7B-RQ1`;
- at most one new reservation;
- automatic retry = NO;
- automatic new reservation = NO;
- second replacement = NO;
- separate explicit live authorization required;
- `P7B_RQ1_LIVE_AUTHORIZED=false`;
- only node entrypoint `scripts/wp2_p7b_c_node_r1.py`;
- resolved absolute paths for receiver and preservation;
- same B1 -> W1 -> B2 cell order and unchanged RF/timing/scientific controls;
- complete evidence survival/read-back required before teardown;
- evidence-gate failure leaves the experiment live and stops.

R2 also created `scripts/wp2_p7b_r2_validate_controller.py`. The retired historical controller fails the gate; a synthetic compliant future controller passes.

Accepted Local Unit Tests:

- run `33117108893`;
- job `98674462071`;
- SHA `b77609bfb9256a0eb189c0e5dd29a2f1f68c3bc2`;
- Python `3.12.14`;
- `paho-mqtt==2.1.0`;
- **73/73 PASS**.

R2 contacted no POWDER system and created no live workflow/trigger/reservation.

## Current blockers before scored authorization

1. separate explicit live authorization for `P7B-RQ1`;
2. one successful replacement B1/W1/B2 physical qualification with strict readiness and evidence survival;
3. immutable pre-score reproducibility snapshot;
4. separate scored-authorization decision.

## Current frontier

`WP2-P7B-R3 — ONE REPLACEMENT NON-SCORED PHYSICAL REQUALIFICATION + EVIDENCE SURVIVAL`

Status:

`P7B_RQ1_LIVE_AUTHORIZED=false`

R3 is **LIVE / NOT AUTHORIZED**. No generic continuation should be treated as live permission; explicit authorization is required.

## Remaining scientific path

```text
WP0 PASS + WP1 PASS
        ↓
WP2 foundation / P6 / P7 PASS
        ↓
P7B-A/B offline PASS
        ↓
first P7B-C/D blocked before measurement / strict evidence gap
        ↓
P7B-E closure PASS
        ↓
P7B-R1 repair PASS
        ↓
P7B-R2 one-replacement contract freeze PASS
        ↓
STOP — separate explicit live authorization required
        ↓
(if authorized) P7B-R3: one P7B-RQ1 reservation + B1/W1/B2 + evidence survival
        ↓
(success required)
immutable pre-score snapshot + scored-authorization decision
        ↓
WP3 -> WP4 -> WP5
```

Scientific weighted completion remains **20%**.
