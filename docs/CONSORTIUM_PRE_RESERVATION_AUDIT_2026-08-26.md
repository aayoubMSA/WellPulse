# WellPulse WP2 — Consortium Pre-Reservation Scientific & Operational Audit

Date: 2026-08-26
Scope: RS-6 Golden E2E rehearsal v1 and Recovery Semantics Amendment v1
Decision authority: advisory consortium; final implementation gate remains RS-7

## Consortium

1. Experimental Systems Lead — treatment fidelity, automation boundaries, failure classification.
2. LTE/POWDER Operator — srsLTE recovery sequence, timing, testbed feasibility.
3. Reproducibility & Artifact Engineer — raw evidence inventory, escrow, teardown interlock.
4. Statistics/Methods Reviewer — estimand, censoring, horizon, technical invalidity.
5. Adversarial Reviewer — leakage, post-hoc discretion, failure modes capable of invalidating the campaign.

## Executive verdict

**REPAIR_OFFLINE_FIRST.**

The science is sufficiently mature to justify another POWDER reservation, but the implementation is not yet reservation-ready. No new scientific redesign is required. The remaining blockers are finite engineering artifacts that RS-7 must complete and statically QA before reservation.

The consortium rejects `RESERVE` today because the Golden document still contains semantic requirements that have not yet been converted into exact executable scripts, exact filenames, exact readiness predicates, and a verified off-POWDER escrow mechanism. Reserving before those exist risks consuming scarce testbed time on implementation/debugging rather than the Golden rehearsal.

The consortium also rejects `DO_NOT_RESERVE`: the Golden design is coherent, bounded, scientifically useful, and directly addresses the H1 substrate pathology without changing the application comparison.

## Findings by reviewer

### 1. Experimental Systems Lead — CONDITIONAL PASS

Strengths:

- one S2-style non-scored rehearsal is the minimum adequate rehearsal;
- G0–G10 create a clear state machine;
- application outcome is correctly separated from Golden readiness;
- no discretionary human branch is intended after launch;
- RF restoration and service restoration are separated prospectively.

Required before reservation:

- implement a single top-level orchestrator with explicit machine-readable gate outputs;
- define abort cleanup and Q0 restoration behavior for every failure state;
- freeze all command return-code handling;
- make run identity unique and propagated to every artifact.

### 2. LTE/POWDER Operator — CONDITIONAL PASS

The clean-order sequence is supported by the observed recovery characterization: UE-only recovery failed, core/RAN reset with a live UE failed, while coordinated clean-order restoration recovered the path and subsequent application E2E passed.

The 120 s infrastructure qualification bound is acceptable for the Golden rehearsal, but RS-7 must freeze deterministic predicates for:

- EPC ready;
- eNB ready;
- UE process replacement and tunnel/address freshness;
- retry cadence for the service-ready probe;
- the exact ICMP timeout used to establish 5/5 success;
- TLS handshake timeout and certificate-verification behavior.

No manual inspection of logs may determine readiness during the run.

### 3. Reproducibility & Artifact Engineer — BLOCKING UNTIL IMPLEMENTED

The H1 incident demonstrates that successful hashing on node-local storage is insufficient. The Golden design correctly requires two verified copies, but the following must exist before reservation:

- exact raw evidence filenames and required/non-required classification;
- source directory layout;
- `/proj/WellPulse/evidence-escrow/<experiment>/<run-id>/` destination layout;
- an actual persistent-copy verification script;
- an actual off-POWDER transfer target and transfer method;
- independent verification of the off-POWDER copy;
- a teardown interlock that cannot emit authorization unless both verifications pass;
- a manifest that includes files, sizes, SHA-256, source/destination, run ID, experiment UUID and timestamps.

This is the principal reservation blocker.

### 4. Statistics/Methods Reviewer — PASS

The amended estimand is acceptable for a confirmatory architecture comparison:

- primary cohort remains tied to `t_rf_restore`;
- `T_service` exposes substrate recovery cost;
- `T_app` measures application recovery after a common usable-service boundary;
- `T_total` preserves operational consequence;
- fixed `H_app=300 s` is architecture-independent and predates comparative outcomes;
- service-restoration failure is classified before application outcome inspection;
- unfavorable application outcomes after `t_service_ready` remain valid scientific results.

No additional H calibration should be performed. Do not reopen the 300 s horizon based on Golden outcome.

### 5. Adversarial Reviewer — CONDITIONAL PASS

The design survives the main scientific attacks, but implementation could still introduce hidden discretion. RS-7 must close these attack surfaces:

1. No manual decision may determine when EPC/eNB/UE is ready.
2. No application topic, queue, database, or delivery state may be queried by G5/G6.
3. Golden must run the full 300 s even if the cohort completes early.
4. Escrow must operate before teardown and must not depend on remembering a manual copy step.
5. A failed escrow is a failed Golden even if all scientific measurements succeeded.
6. Console output cannot be the sole copy of any scientific value.
7. Reconstruction must consume escrowed raw files, not live node-local files.
8. The Golden architecture choice must be recorded as rehearsal-only and not used for comparative inference.

## Mandatory RS-7 repair package

RS-7 must produce and QA the following before a reservation is recommended:

1. `golden_e2e_orchestrator.sh` — progress-visible G0–G10 state machine.
2. `service_restore.sh` — deterministic UE/EPC/eNB clean-order restoration.
3. `service_ready_probe.sh` — architecture-blind 120 s qualification with exact retry/timeouts.
4. `evidence_inventory_v1.txt` or equivalent schema — exact required filenames/patterns and non-empty rules.
5. `reconstruct_golden.py` — offline reconstruction from escrowed raw artifacts only.
6. `evidence_escrow.sh` — source hashing, persistent copy, persistent verification, off-POWDER copy, off-POWDER verification.
7. `teardown_guard.sh` — fail-closed interlock requiring verified dual escrow.
8. static/syntax QA and dry-run tests that do not require POWDER RF resources where possible.
9. reservation budget with setup, Golden execution, escrow, contingency and safe teardown time.
10. one final readiness matrix mapping every G0–G10 requirement to script, evidence artifact and PASS predicate.

## Reservation acceptance gate

RS-7 may issue `RESERVE` only when all mandatory repair artifacts exist at a frozen Git commit and static/dry-run QA passes.

The reservation must be sized to execute the already-frozen Golden rehearsal, not to develop/debug the orchestration interactively.

If the off-POWDER escrow destination cannot be made operational before reservation, verdict remains `REPAIR_OFFLINE_FIRST`.

## What must not be reopened

- Q0/Q1/Q2/Q3 values;
- 1 Hz workload;
- S2 Golden selection;
- 120 s service-restoration qualification bound;
- 5/5 ICMP + verified TLS service-ready semantics;
- `H_app=300 s`;
- primary cohort cutoff at `t_rf_restore`;
- H1 classification/provenance;
- B1/W1/B2 scientific semantics;
- negative/null-result interpretation tree.

## Final consortium decision

`CONSORTIUM_PRE_RESERVATION_VERDICT=REPAIR_OFFLINE_FIRST`

Exact next action: execute RS-7 offline implementation/readiness QA. When all ten mandatory repair outputs pass, issue `RESERVE` and only then obtain a new POWDER slot.
