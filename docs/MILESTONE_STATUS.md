# WellPulse — Milestone Status

Last updated: 2026-08-27 after **P7B-R1 receiver-path repair + observability regression QA PASS**.

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

The remaining 5/100 is still gated by successful pre-score physical qualification plus an immutable authorization snapshot. R1 is a repair patch and creates no additional management/scientific credit.

## Frozen scientific state

- FIT IoT-LAB layer: FINAL PASS.
- POWDER G0-G5: PASS.
- RF calibration: PASS / FROZEN.
- Q0/Q1/Q2/Q3 = `0/40/52/55 dB`.
- attenuation IDs `1 33 2 34` move together.
- primary cohort cutoff = `t_rf_restore`.
- `t_rf_restore`, `t_service_ready`, `t_app_complete` remain distinct.
- `H_app=300 s` from `t_service_ready` remains frozen.
- primary endpoint remains `completeness_300` at `t_service_ready + 300 s`.
- no outcome-derived/W1-derived/Golden-derived/scored-derived horizon re-estimation.
- H1 remains valid adverse non-scored evidence.
- K1-K8 remain PASS / CLOSED absent material interface change.

## P6/P7 baseline

- `WP2_P6=PASS_RECOVERED_SINGLE_RUN`.
- P6 valid run `wp2-p6r-33099648133-20260827T174149Z`, primary cohort 181, valid by 300 s 181/181, `completeness_300=1.0`.
- P6 raw evidence, `/proj` escrow, independent artifact round-trip and teardown: PASS.
- `WP2_P7_HARDENING_QA=PASS`.
- scored authorization remained blocked on mandatory physical qualification.

## P7B qualification history

Canonical blocked closure:

`docs/WP2_P7B_E_CANONICAL_BLOCKED_CLOSURE_2026-08-27.md`

| P7B patch | Status | Key evidence |
|---|---|---|
| A | PASS | offline contract freeze + 41/41 tests |
| B | PASS | implementation/reconstruction + 56/56 tests + B2 Java semantics PASS |
| C | **BLOCKED** | one authorized live reservation; failed in B1 readiness before measurement |
| D | **BLOCKED STRICT COMPLETENESS** | declared roots preserved/read back and teardown complete; receiver event ledger unrecovered |
| E | **PASS CANONICAL BLOCKED CLOSURE** | failed/partial result frozen without relabelling |

Successful P7B physical-qualification credit remains **40/100** from A+B only.

### P7B-C live reservation

- experiment UUID `26b6f315-459d-4a56-9167-69228e339f24`;
- experiment name `wp7b3016138`;
- GitHub run `33113016138`;
- node run ID `wp2-p7b-c-33113016138-20260827T203140Z`;
- non-scored pre-score physical qualification only;
- reservation reached Portal `ready`;
- core/UE SSH PASS;
- frozen profile revision matched;
- B1 Q0 route via `tun_srsue` PASS;
- five Q0 probes: 0% packet loss;
- TLS/MQTT readiness publish: PASS;
- broker proves B1 receiver connected, got CONNACK, subscribed to exact topic and remained alive;
- controller timed out waiting for expected receiver event ledger;
- completed cells: NONE;
- scientific measurement started: NO;
- W1 and B2: NOT STARTED;
- retained verdict: `WP2_P7B_C=BLOCKED:RECEIVER_CONNECT_TIMEOUT`.

Root-cause classification: **orchestration/evidence-path quoting defect**, not demonstrated LTE/MQTT transport failure.

### P7B-D preservation

- first attempt run `33114265831`: fail-closed due preservation path quoting defect; no artifact; no teardown;
- same-reservation retry run `33114517583`, job `98665610066`: SUCCESS;
- declared UE/core `/proj` escrow: PASS;
- controller pull/internal hashes: PASS;
- GitHub artifact ID `9663926250`;
- artifact ZIP digest `0bd31f534712d2f1fe3793008e7b00c1e6df85f58277686b3de5ffb5fd6455bb`;
- deterministic inner TAR SHA-256 `f49263f77d673cf5961dd6efb3b0ce2a3d7dde5969d48f20e0c383f105693877`;
- deterministic inner TAR bytes `296960`;
- independent download and internal hash read-back: PASS;
- teardown confirmed after off-POWDER verification;
- expected `receiver_events.jsonl` was not recovered before teardown;
- strict retained verdict: `WP2_P7B_D=BLOCKED_STRICT_COMPLETENESS_RECEIVER_EVENT_LEDGER_NOT_RECOVERED`.

## P7B-R1 — operational repair QA

Canonical closure:

`docs/WP2_P7B_R1_RECEIVER_PATH_OBSERVABILITY_CLOSURE_2026-08-27.md`

Verdict:

`WP2_P7B_R1=PASS_OFFLINE_RECEIVER_PATH_OBSERVABILITY_QA`

Implemented offline:

- `scripts/wp2_p7b_path_contract.py` — absolute remote-path contract, rejects literal `$HOME`/`~`, proves receiver writer/watcher equality;
- `scripts/wp2_p7b_c_node_r1.py` — repaired receiver launcher on absolute path, PID fail-fast, bounded GitHub-compatible diagnostics;
- `scripts/wp2_p7b_preservation_helpers.sh` — fail-closed absolute-path/hash-copy helpers;
- updated executable regressions in `tests/test_wp2_p7b_c_premutation.py`.

Accepted Local Unit Tests:

- run `33116073295`;
- job `98670934415`;
- SHA `695b31cba6c0256b3637223abdfef4f4b11bf6ca`;
- Python `3.12.14`;
- `paho-mqtt==2.1.0`;
- **65/65 PASS**.

R1 changed no RF/timing/horizon/scientific rules, contacted no POWDER system, created no reservation and created no live workflow.

The historical retired controller still points to the old runner. Therefore any future authority contract must explicitly bind the controller to `scripts/wp2_p7b_c_node_r1.py`; direct reuse of the historical controller is prohibited.

R1 recommendation:

`FUTURE_PHYSICAL_REQUALIFICATION_RECOMMENDATION=GO_CONDITIONAL`

This recommendation does not override the consumed original `reservation_limit=1` or the prohibition on automatic replacement.

## Current blockers before scored authorization

1. freeze an explicit requalification authority contract if one replacement reservation is judged justified;
2. require the repaired R1 entrypoint and absolute-path preservation contract in that authority surface;
3. if later separately live-authorized, successfully complete B1/W1/B2 physical qualification and strict evidence survival;
4. freeze the immutable pre-score reproducibility snapshot;
5. make a separate scored-authorization decision.

## Current frontier

`WP2-P7B-R2 — REQUALIFICATION AUTHORITY + CONTRACT FREEZE`

Status: **OFFLINE ONLY / NOT STARTED**.

R2 itself carries no POWDER authority. It must stop again before any possible live replacement reservation.

## Remaining scientific path

```text
WP0 PASS + WP1 PASS
        ↓
WP2 K1-K8 + AUDIT-R1 + P5 PASS
        ↓
P6 non-scored Golden PASS
        ↓
P7 hardening PASS / scored authorization BLOCKED
        ↓
P7B-A/B offline PASS
        ↓
P7B-C live qualification BLOCKED before measurement
        ↓
P7B-D strict completeness BLOCKED / teardown complete
        ↓
P7B-E canonical blocked closure PASS
        ↓
P7B-R1 offline receiver-path/observability repair PASS
        ↓
P7B-R2 offline requalification authority/contract freeze
        ↓
STOP / separate explicit live authorization required
        ↓
(if authorized) one bounded replacement physical qualification
        ↓
(successful physical qualification + strict evidence survival required)
        ↓
immutable pre-score snapshot + scored-authorization decision
        ↓
WP3 -> WP4 -> WP5
```

Scientific weighted completion remains **20%**.
