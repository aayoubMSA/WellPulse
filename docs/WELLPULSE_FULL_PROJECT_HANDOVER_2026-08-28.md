# WellPulse — Full Project Handover

Date: 2026-08-28
Repository: `aayoubMSA/WellPulse`
Branch: `main`

## Authority and purpose

This document transfers ownership of the **entire WellPulse research project** to a new agent while preserving `HANDOVER_CURRENT.md` as the canonical operational source of truth.

Do not reconstruct state from chat memory. If anything in this document conflicts with `HANDOVER_CURRENT.md`, the latter governs.

The project must continue as finite, bounded patches with explicit QA, PASS/BLOCKED verdicts, and STOP conditions. Negative/null/unfavourable scientific results are valid evidence and must never be suppressed or relabelled.

## Executive project state

- WP0 — Novelty & Venue Lock: **PASS**; credited 8/8.
- WP1 — Confirmatory Protocol & Statistics Freeze: **PASS / FROZEN**; credited 12/12.
- WP2 — RF Calibration & Measurement Validation: **ACTIVE / PRE-SCORE BLOCKED**.
- WP3 — Conducted-RF Confirmatory Campaign: **BLOCKED ON WP2**; 0/30.
- WP4 — OTA External Replication: **BLOCKED**; 0/15.
- WP5 — Analysis + Artifact + Paper Closure: **PREPARED / NOT EXECUTED**; 0/20 scientific closure.
- Scientific weighted completion remains **20%** until WP2 closes.

Within WP2:

- FIT IoT-LAB scientific layer: **FINAL PASS**.
- POWDER G0-G5: **PASS**.
- RF calibration: **PASS / FROZEN**.
- K1-K8 compatibility: **PASS / CLOSED** absent material interface change.
- `PRE_INTEGRATION_COMPATIBILITY_GATE=PASS`.
- `AUDIT_R1=PASS`.
- `LIVE_HCI_AND_RAW_EVIDENCE_GATE=PASS`.
- `WP2_P6=PASS_RECOVERED_SINGLE_RUN`.
- `WP2_P7_HARDENING_QA=PASS`.
- P7B-A/B offline contract + implementation: **PASS**.
- P7B-R1/R2/R3D and target-runtime/EFCC work: retained as valid provenance unless explicitly superseded.
- P7B physical qualification: **NOT PASSED**.
- Scored execution: **NOT AUTHORIZED**.

## Golden baseline retained

Canonical closure:

`docs/WP2_P6_GOLDEN_CLOSURE_2026-08-27.md`

Key frozen provenance:

- experiment UUID `5579cf25-dbb1-4d04-87e3-ff558e3be2af`
- experiment name `wpg7498036`
- profile `PowderProfiles/srslte-controlled-rf`
- profile revision `a6da96560b6526dc6816761282722c996418fd8c`
- valid run `wp2-p6r-33099648133-20260827T174149Z`
- `T_service=25.088240 s`
- `T_app=5.293835 s`
- `T_total=30.382075 s`
- primary cohort 181
- `completeness_300=1.0`
- persistent escrow/readback: PASS

This is the valid non-scored Golden baseline and must not be re-estimated from later outcomes.

## Current P7B scientific state

Latest attempted B1 is frozen exactly as:

`P7B_B1_ATTEMPT=ABORTED_AFTER_SCIENTIFIC_IMPAIRMENT`

`B1_SCIENTIFIC_VERDICT=NULL`

`B1=NULL_ABORTED_AFTER_Q3`

`W1=NOT_STARTED`

`B2=NOT_STARTED`

`AUTOMATIC_RETRY=PROHIBITED`

`MANUAL_RETRY=PROHIBITED_UNDER_CURRENT_FROZEN_CONTRACT`

`SCORED=NO`

No partial PASS/FAIL scientific credit may be inferred from the aborted B1 attempt.

Historical reservation used for the aborted attempt:

- UUID `f6de95cb-a13a-421e-bd0e-766dfc1d3fb3`
- name `wp7brq2609012`
- profile revision `a6da96560b6526dc6816761282722c996418fd8c`
- CORE `nuc1`
- UE `nuc2`
- run ID `wp2-p7b-manual-20260828T024433Z`

Do not assume this reservation is still live.

## H1 abort-evidence closure

Canonical closure:

`docs/WP2_P7B_H1_ABORT_EVIDENCE_FREEZE_ROOT_CAUSE_CLOSURE_2026-08-28.md`

Machine record:

`evidence/powder/wp2-p7b-h1-abort-root-cause.json`

Terminal verdict:

`WP2_P7B_H1=PASS_ABORT_EVIDENCE_FROZEN_ROOT_CAUSE_CLASSIFIED`

Classified first technical root cause:

`FIRST_TECHNICAL_ROOT_CAUSE=CONTROLLER_SESSION_COLLISION_SERVICE_RESTORE_KILLED_OPERATOR_TMUX_UE`

`ROOT_CAUSE_CLASS=CONTROLLER_SESSION_INFRASTRUCTURE`

`ROOT_CAUSE_CONFIDENCE=HIGH`

The frozen execution frontier proves Q3 began, the intended gateway was destroyed, the replacement gateway started, Q0 restore was commanded, and `wp2_golden_service_restore.sh` then stopped at its first UE cleanup phase. The parent controller disappeared while detached child processes survived. `restart_proof.json=MISSING` therefore must not be interpreted as “gateway restart did not occur.”

### Additional preservation-only readback after H1 closure

A later preservation-only GitHub Actions run also completed successfully and did **not** change scientific state:

- workflow: `WP2 P7B-H1 Abort Evidence Preservation`
- run `33138392609`
- preserve job `98743506446`: SUCCESS
- verify job `98743549028`: SUCCESS
- artifact ID `9672927868`
- artifact name `wp2-p7b-h1-wp2-p7b-manual-20260828T024433Z`
- artifact ZIP digest `sha256:a6db4d209528a9cf326e92807e234170a71e8e03b9d7893bfb58ad57b5b79519`
- deterministic inner TAR SHA-256 `786a7b511ef3fb06341dbfccae9dad4cfdb1b2432a3a7ead03f050525451dd53`
- off-node readback: PASS
- confirmed frontier: Q3 set exists, `t_rf_restore` exists, `restart_proof.json` absent
- `SCIENTIFIC_RETRY=NO`
- `RF_MUTATION=NO`
- `RESTART=NO`
- `TEARDOWN=NO`

This is redundant preservation provenance only; it does not authorize retry or supersede the H1 closure.

## Frozen scientific controls

These remain authoritative unless changed only through a separately reviewed prospective amendment:

- Q0/Q1/Q2/Q3 = `0/40/52/55 dB`.
- attenuator IDs `[1,33,2,34]`, coupled.
- primary cohort cutoff = `t_rf_restore`.
- `t_rf_restore`, `t_service_ready`, `t_app_complete` are distinct clocks.
- `H_app=300 s` from `t_service_ready`.
- primary endpoint = `completeness_300` at `t_service_ready + 300 s`.
- preserve `T_service`, `T_app`, `T_total`.
- no outcome/W1/Golden/scored-derived H re-estimation.
- pre-Q0 = `60 s`.
- Q3 duration = `120 s`.
- gateway/client restart offset = `60 s` into Q3.
- exact cell order = `B1 -> W1 -> B2`.
- generator remains outside gateway restart domain.
- no automatic scientific retry.

## Controller/runtime doctrine retained

Target/runtime contract remains based on:

- Ubuntu 18.04 target family.
- system Python 3.6.9 forbidden for project code.
- project Python `$HOME/.wp2-golden-venv/bin/python` exact 3.11.13.
- `paho-mqtt==2.1.0`.
- Bash 4.4.19 family.
- no remote jq dependency.
- CORE Mosquitto daemon 1.4.15.
- UE Java major 11.
- exact B2 Paho JAR SHA-256 `59914287adac506a28d5e8172eed262a22605f3df4d426b9d92f41dae2448185`.
- authoritative target preflight `scripts/wp2_p7b_target_node_preflight.sh`.
- authoritative prospective P7B entrypoint family culminates in `scripts/wp2_p7b_c_node_r2.py` under the currently frozen contract history.

Historical recovery work established that environment repair must replay the known-good provisioning sequence rather than patch missing dependencies symptom-by-symptom.

## Human-operation doctrine

Every manual command block must explicitly identify the target:

- `nuc1 / CORE`, or
- `nuc2 / UE`.

Do not add diagnostic `sleep`, `wait`, or artificial delays to human-operated scripts. Frozen scientific timing inside an authorized experiment runner is separate and remains mandatory.

Evidence survival must be simpler than the application path: shell/coreutils primitives, explicit per-node ownership, persistent escrow, originating-node pull, immutable artifact, independent hash/read-back before teardown.

## Exact current frontier

`WP2-P7B-H2 — CONTROLLER/RESTORE-DOMAIN CONTRACT AMENDMENT QA + FUTURE REQUALIFICATION AUTHORITY DECISION`

Status: **OFFLINE / NOT STARTED**.

H2 is the next bounded patch for the whole project because WP3-WP5 remain gated on WP2.

H2 may only:

1. translate the H1 draft into a finite executable contract delta;
2. repair controller/session ownership boundaries offline;
3. add incremental restart/restoration-frontier evidence offline;
4. add static/adversarial tests proving service cleanup cannot kill the controller;
5. run offline contract-delta/runtime regression QA;
6. decide whether a future **non-scored** physical requalification can be scientifically authorized under a newly frozen contract.

Even an H2 PASS does not authorize POWDER access or a retry.

## Prohibited until a later explicit user authorization

- no POWDER contact;
- no reservation creation;
- no RF mutation;
- no service restart;
- no B1 retry;
- no W1/B2;
- no Golden rerun;
- no H recalibration;
- no scored B1/W1/B2;
- no teardown;
- no WP3 execution;
- no scientific-control drift;
- no third-party contact or paper submission.

## Mandatory new-agent read order

Read completely, in this order:

1. `HANDOVER_CURRENT.md`
2. `docs/WELLPULSE_FULL_PROJECT_HANDOVER_2026-08-28.md`
3. `AGENTS.md`
4. `docs/PROJECT_AUDIT_HANDOVER_2026-08-27.md`
5. `docs/WP0_NOVELTY_VENUE_LOCK_2026-08-24.md`
6. `experiments/WP-PWD01/protocol.md`
7. `experiments/WP-PWD01/analysis-plan.md`
8. `docs/WP2_P6_GOLDEN_CLOSURE_2026-08-27.md`
9. `docs/WP2_P7B_H1_ABORT_EVIDENCE_FREEZE_ROOT_CAUSE_CLOSURE_2026-08-28.md`
10. `evidence/powder/wp2-p7b-h1-abort-root-cause.json`
11. `experiments/WP-PWD01/P7B_CONTROLLER_SESSION_DISJOINTNESS_AMENDMENT_DRAFT_2026-08-28.md`
12. `experiments/WP-PWD01/p7b-executable-contract-v2.json`
13. `experiments/WP-PWD01/p7b-target-runtime-contract-v2.json`
14. `scripts/wp2_p7b_c_node_r2.py`
15. `scripts/wp2_p7b_c_node_r1.py`
16. `scripts/wp2_p7b_c_node.py`
17. `scripts/wp2_golden_service_restore.sh`
18. `scripts/wp2_p7b_target_node_preflight.sh`
19. current `Research & Grants — Lessons Learned Ledger` in Drive.

Do not treat `docs/STATUS.md` or `docs/MILESTONE_STATUS.md` as current operational authority where they conflict with `HANDOVER_CURRENT.md`; they retain historical/project-planning value only.

## Required first response from the new agent

Before editing files or executing any patch, the new agent must report:

1. retrieved canonical whole-project state;
2. WP0-WP5 status with scientific weighted completion;
3. exact P7B aborted-run scientific verdict and H1 root cause;
4. exact frozen scientific controls;
5. exact H2 finite patch list it proposes to own;
6. explicit statement that no live POWDER action is authorized.

Then STOP and wait for explicit continuation authority.

## Transfer stop state

`WHOLE_PROJECT_HANDOVER=READY`

`CURRENT_PATCH=WP2-P7B-H2`

`H2=OFFLINE_NOT_STARTED`

`B1=NULL_ABORTED_AFTER_Q3`

`W1=NOT_STARTED`

`B2=NOT_STARTED`

`SCORED=NO`

`LIVE_POWDER_AUTHORIZATION=NO`

`TEARDOWN_AUTHORIZATION=NO`

**STOP — project transferred; next agent must retrieve canonical state before action.**
