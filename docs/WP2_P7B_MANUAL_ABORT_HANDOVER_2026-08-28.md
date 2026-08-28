# WellPulse WP2 — P7B Manual Qualification Handover

Date: 2026-08-28
Repository: `aayoubMSA/WellPulse`
Branch: `main`
Scope: WP2 / POWDER / P7B non-scored pre-score physical qualification

## Authority of this record

This document is the **latest live-state override** for WP2-P7B as of 2026-08-28. It supplements the older `HANDOVER_CURRENT.md`, which remains required historical context but predates the manual RQ2 recovery and the aborted Q3 attempt documented here.

The next agent must not reconstruct the latest state from conversation memory. Read this document first, then the older canonical handover and the P7B contract/runtime records listed below.

## Exact current scientific state

- WP0: PASS.
- WP1: PASS / FROZEN.
- WP2: ACTIVE / PRE-SCORE BLOCKED.
- Scored execution remains unauthorized.
- P6 Golden baseline remains valid and frozen.
- P7B offline contract/implementation/runtime QA remains valid.
- Current P7B physical qualification is **NOT PASSED**.
- B1 has **no scientific PASS/FAIL verdict** from the latest attempt.
- W1: NOT STARTED.
- B2: NOT STARTED.

Latest live attempt must be classified exactly as:

`P7B_B1_ATTEMPT=ABORTED_AFTER_SCIENTIFIC_IMPAIRMENT`

`B1_SCIENTIFIC_VERDICT=NULL`

`AUTOMATIC_RETRY=PROHIBITED`

`MANUAL_RETRY=PROHIBITED_UNDER_CURRENT_FROZEN_CONTRACT`

## Current POWDER reservation

Reservation observed during the manual recovery lane:

- UUID: `f6de95cb-a13a-421e-bd0e-766dfc1d3fb3`
- name: `wp7brq2609012`
- profile: `srslte-controlled-rf`
- frozen profile revision: `a6da96560b6526dc6816761282722c996418fd8c`
- CORE role: `nuc1`
- UE role: `nuc2`
- management IP observed for CORE/nuc1: `155.98.36.173`
- management IP observed for UE/nuc2: `155.98.36.162`

Do not assume this reservation is still live when the next agent starts. Re-check Portal state before any future live plan. Do not create a replacement reservation without a new explicit authority decision.

## RQ2 environment recovery — PASS before the scientific attempt

The current reservation was recovered manually using the historical known-good provisioning sequence.

Both nodes passed the authoritative frozen target preflight:

### CORE / nuc1

- Ubuntu 18.04
- system Python 3.6.9
- pinned project Python 3.11.13
- paho-mqtt 2.1.0
- Mosquitto 1.4.15
- `EFCC_RUNTIME_BINDING=PASS`
- `WP2_P7B_TARGET_NODE_PREFLIGHT=PASS`
- `CR2_NODE=PASS`

### UE / nuc2

- Ubuntu 18.04
- system Python 3.6.9
- pinned project Python 3.11.13
- paho-mqtt 2.1.0
- Java major 11
- Eclipse Paho Java 1.2.5 JAR SHA-256 exactly:
  `59914287adac506a28d5e8172eed262a22605f3df4d426b9d92f41dae2448185`
- `EFCC_RUNTIME_BINDING=PASS`
- `WP2_P7B_TARGET_NODE_PREFLIGHT=PASS`
- `CR2_NODE=PASS`

Key root-cause lesson from RQ2 recovery: the earlier RQ2 bootstrap had replayed only the Python bootstrap and omitted the full historical system bootstrap. The correct historical provisioning sequence includes system packages first, then `scripts/wp2_a3_runtime_bootstrap.sh`.

## Q0 physical path recovery — PASS before P7B execution

Manual Q0 recovery eventually established:

- CORE/nuc1: `SRSEPC=PASS`, `SRSENB=PASS`
- UE/nuc2: `srsue` attached successfully
- observed UE IP: `172.16.0.2`
- route to `172.16.0.1` via `tun_srsue`
- five Q0 probes: 0% packet loss
- `Q0_USER_PLANE_GATE=PASS`
- `WP2_Q0_FINAL_GATE=PASS`

The RF set command for attenuators `[1,33,2,34]` at Q0=0 dB returned successful command acknowledgements. Physical dB readback is unsupported by the observed TMCC interface; do not upgrade command ACK to a physical-readback claim.

## Management SSH alias repair — PASS before the latest attempt

The first manual runner invocations exposed SSH identity gaps rather than scientific failures.

Repairs completed:

- ephemeral ED25519 key created on nuc2;
- key authorized on nuc1 for `enb1` access;
- same key authorized on nuc2 for `rue1` self-SSH;
- explicit SSH config bindings created;
- `scripts/wp2_golden_prepare_management_aliases.sh` passed with:
  `WP2_GOLDEN_MANAGEMENT_ALIAS_GATE=PASS`.

The pre-cell SSH failures are technical provenance only; they did not execute a scientific cell.

## Latest authoritative P7B attempt

Run ID:

`wp2-p7b-manual-20260828T024433Z`

Raw wrapper root:

`/proj/WellPulse/evidence/p7b-live-wp2-p7b-manual-20260828T024433Z`

Node evidence root on UE:

`$HOME/wellpulse-powder-evidence/p7b/wp2-p7b-manual-20260828T024433Z`

Authoritative entrypoint used:

`scripts/wp2_p7b_c_node_r2.py`

Observed runner milestones:

- executable contract v2 PASS;
- target runtime contract v2 PASS;
- EFCC binding PASS;
- R1 repaired receiver/path layer active;
- live non-scored authority accepted;
- shared TLS broker started;
- exact Eclipse Paho Java 1.2.5 runtime compiled;
- entered `P7B-B1-S3: independent Q0 washout/readiness`.

## Scientific boundary crossed

The abrupt-exit RCA established:

- `Q3_STARTED=YES`
- `attenuator_q3_set.txt=EXISTS`
- `t_rf_restore.txt=EXISTS`
- `restart_proof.json=MISSING`
- `SCIENTIFIC_IMPAIRMENT_STARTED=YES`
- `READINESS_VERDICT=EXISTS`
- `WRAPPER_OBSERVED_NODE_EXIT=NO`
- authoritative runner no longer running
- `SRSUE=NOT_RUNNING`
- `TUN_SRSUE=MISSING`
- `COMPLETED_CELLS=` empty
- `CURRENT_CELL=None`
- `FAILURE=None`
- `VERDICT=None`

This is the decisive no-retry boundary. The attempt crossed into the scientific Q3 impairment, therefore the current frozen contract does not permit rerunning B1 on this reservation.

The presence of `t_rf_restore.txt` means the runner reached the RF-restore stage and recorded the restore timestamp. It does **not** by itself prove physical attenuator readback. Inspect `attenuator_restore_q0_set.txt` before making any RF-state claim.

## Radio/NAS observations during the aborted attempt

Observed on live consoles during/after the B1 attempt:

- repeated Radio-Link Failure / RRC reconnect behavior;
- CORE showed `SECURITY_MODE_REJECT` / NAS integrity-related messages;
- UE later lost `srsue` and `tun_srsue` after the runner disappeared.

These are retained observations, not yet a proven root cause. Do not reinterpret them as a B1 architecture failure.

## Evidence preservation state

Important evidence already exists under `/proj/WellPulse/evidence/`.

Latest RCA directory:

`/proj/WellPulse/evidence/p7b-live-wp2-p7b-manual-20260828T024433Z/abrupt-exit-rca`

Earlier pre-cell failed-run bundle also exists:

`/proj/WellPulse/evidence/wp2-p7b-manual-20260828T023743Z-RAW-EVIDENCE.tar.gz`

A final aborted-run freeze/package sprint was drafted in the previous session but **was not executed before handover**. Therefore the next bounded patch should prioritize evidence freeze/pull **before any additional live mutation**, if the reservation/evidence path is still accessible.

Do not delete, overwrite, normalize, or relabel negative/null evidence.

## Mandatory next-agent read order

Read in this order:

1. `docs/WP2_P7B_MANUAL_ABORT_HANDOVER_2026-08-28.md` — this document.
2. `HANDOVER_CURRENT.md` — historical canonical project handover.
3. `docs/WP2_P7B_R3D_EFCC_CONTRACT_DELTA_CLOSURE_2026-08-28.md`.
4. `docs/WP2_POWDER_RUNTIME_COMPATIBILITY_MATRIX_2026-08-28.md`.
5. `docs/WP2_P7B_RQ2_CONTRACT_RECOVERY_SPRINT_2026-08-28.md`.
6. `docs/WP2_P7B_RQ2_CR2_RECOVERY_EXECUTION_SPRINT_2026-08-28.md`.
7. `experiments/WP-PWD01/p7b-executable-contract-v2.json`.
8. `experiments/WP-PWD01/p7b-target-runtime-contract-v2.json`.
9. `scripts/wp2_p7b_c_node_r2.py`.
10. `scripts/wp2_p7b_c_node_r1.py`.
11. `scripts/wp2_p7b_c_node.py`.
12. `scripts/wp2_golden_prepare_management_aliases.sh`.
13. `scripts/wp2_p7b_target_node_preflight.sh`.
14. `docs/RESEARCH_GRANTS_LESSONS_LEARNED_LEDGER.md` if present; otherwise locate the current lessons ledger before proposing fixes.

## Frozen scientific controls — do not change

- Q0/Q1/Q2/Q3 = `0/40/52/55 dB`.
- attenuator IDs `[1,33,2,34]`, coupled.
- primary cohort cutoff = `t_rf_restore`.
- `t_rf_restore`, `t_service_ready`, `t_app_complete` are distinct clocks.
- H_app = 300 s from `t_service_ready`.
- primary endpoint = `completeness_300` at `t_service_ready + 300 s`.
- preserve `T_service`, `T_app`, `T_total`.
- no outcome/W1/Golden/scored-derived re-estimation of H.
- P7B pre-Q0 = 60 s.
- Q3 duration = 120 s.
- gateway/client restart offset = 60 s into Q3.
- exact cell order = `B1 -> W1 -> B2`.
- generator remains outside gateway restart domain.
- no automatic scientific retry.
- negative/null evidence remains valid evidence.

## Manual-operation doctrine learned in this session

1. Always label every command block explicitly `nuc1 / CORE` or `nuc2 / UE`.
2. Prefer node-detecting scripts where practical to prevent wrong-node execution.
3. Do not add diagnostic `sleep`/wait delays for a human-driven console workflow. Scientific timing inside the frozen runner remains mandatory and must not be removed.
4. Save raw output to `/proj/WellPulse/evidence/` whenever possible.
5. Hash evidence and package it before teardown.
6. Never interpret an early gate failure as a scientific failure until the scientific mutation boundary is checked.
7. Once Q3 starts, no retry is allowed under the current frozen contract.
8. Distinguish controller/session-survival defects from RF/LTE/application architecture failures.
9. Do not repair environment symptoms one dependency at a time; replay the known-good provisioning sequence.
10. Do not trust terminal scrollback timestamps as current state; query live process/state/evidence files.

## Exact next bounded patch

`WP2-P7B-H1 — ABORTED-Q3 EVIDENCE FREEZE + OFFLINE ROOT-CAUSE HANDOVER`

Allowed work in H1:

1. Re-check whether the current reservation/evidence paths are still accessible.
2. Freeze/copy the complete current aborted-run UE evidence tree and CORE evidence tree into `/proj` or off-testbed storage without changing scientific state.
3. Hash/package the frozen evidence.
4. Pull/download the package off POWDER if possible.
5. Inspect the exact execution frontier around Q3 start, restart request, RF restore, and runner disappearance.
6. Classify the first technical root cause without relabelling B1 scientifically.
7. Draft a **new future-qualification contract amendment** only if root cause is controller/session/infrastructure and only offline.

H1 forbidden actions:

- no B1 retry;
- no W1/B2 execution;
- no new Q3;
- no RF mutation unless separately authorized for safety recovery after evidence inspection;
- no service restart;
- no new reservation;
- no teardown unless separately authorized after evidence survival is proven;
- no scored execution;
- no scientific-control changes.

H1 terminal verdict must be one of:

`WP2_P7B_H1=PASS_ABORT_EVIDENCE_FROZEN_ROOT_CAUSE_CLASSIFIED`

or

`WP2_P7B_H1=BLOCKED:<first_named_reason>`

Then STOP.

## Current stop state

At handover:

`B1=NULL_ABORTED_AFTER_Q3`

`W1=NOT_STARTED`

`B2=NOT_STARTED`

`SCORED=NO`

`AUTOMATIC_RETRY=NO`

`MANUAL_RETRY=NO_UNDER_CURRENT_CONTRACT`

`TEARDOWN=NOT_AUTHORIZED_BY_THIS_HANDOVER`

The next agent must report the retrieved canonical state and exact H1 plan before taking any live action.