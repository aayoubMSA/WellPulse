# Next Gate — WP2 Recovery-Semantics Amendment

**Current frontier:** RS-6 GOLDEN E2E REHEARSAL DESIGN  
**Scientific completion:** 20%  
**Scored authorization:** `false`

## Governing read order

1. `HANDOVER_CURRENT.md`
2. `docs/AGENT_HANDOVER_POWDER_NEXT.md`
3. `docs/CONSORTIUM_WP2_RECOVERY_SEMANTICS_GATE_2026-08-26.md`
4. `docs/RS2_LTE_RECOVERY_MECHANISM_REVIEW_2026-08-26.md`
5. `docs/RS3_ESTIMAND_H_FAIRNESS_REVIEW_2026-08-26.md`
6. `docs/RS4_ADVERSARIAL_REVIEW_2026-08-26.md`
7. `experiments/WP-PWD01/RECOVERY_SEMANTICS_AMENDMENT_v1.md`
8. `experiments/WP-PWD01/protocol.md`
9. `experiments/WP-PWD01/analysis-plan.md`

## Frozen state

- H1 remains `VALID_W1_RECOVERY_FAILURE`; no reclassification.
- Q0/Q1/Q2/Q3 remain `0/40/52/55 dB`; attenuation IDs `1 33 2 34` remain coupled.
- No scored B1/W1/B2 run is authorized.
- Raw H1 record-level bundles remain unavailable from user-accessible persistent storage; backend recovery is pending.
- Future evidence escrow is fail-closed before teardown.

## RS-2 — PASS

Mechanism characterized as cross-node LTE/NAS/MME/GTP-C/session-context inconsistency after the hard outage. No proven bounded autonomous repair. Broad srsLTE engineering is not authorized.

## RS-3 — PASS

Accepted distinct clocks and fairness framework:

- `t_rf_restore`
- `t_service_ready`
- `t_app_complete`
- `T_service`, `T_app`, `T_total`
- primary cohort cutoff remains `t_rf_restore`.

## RS-4 — PASS WITH REQUIRED MODIFICATION

Two-clock decomposition survived. W1-only horizon calibration was rejected as arm-informed.

## RS-5 — PASS / PROSPECTIVE AMENDMENT FROZEN

Authority: `experiments/WP-PWD01/RECOVERY_SEMANTICS_AMENDMENT_v1.md` and protocol v0.6.

Frozen decisions:

- fixed common architecture-independent application horizon: **300 s from `t_service_ready`**;
- 300 s is inherited from the pre-H1 engineering feasibility ceiling, not from B1/W1/B2 outcomes;
- primary endpoint becomes `completeness_300` at `t_service_ready + 300 s`;
- primary cohort remains records generated at or before `t_rf_restore`;
- `T_service`, `T_app`, and `T_total` are mandatory companion outcomes;
- S2/S3 use identical scripted clean-order LTE service restoration as a measurement-boundary substrate operation;
- S0/S1 do not receive forced LTE reset and use the same architecture-blind readiness probe;
- service-restoration invalidity must be decided before inspecting application outcomes;
- negative/null-result interpretation tree is frozen;
- no outcome-driven horizon calibration is permitted.

RS-5 commits:

- amendment: `b2307cf15c1021f80847f6a0f5622114926770d0`
- protocol v0.6: `d7209e05fd447e1a0b9ba7e3c2eb399e4ca0a7af`

## Immediate action — RS-6

Design one **non-scored Golden E2E rehearsal** only. No reservation is required until this design is frozen.

RS-6 must specify exactly:

1. initial deterministic clean state;
2. exact S2-style Q0 -> Q3 -> Q0 schedule used for rehearsal;
3. exact one-command clean-order service-restoration workflow;
4. exact architecture-blind service-ready probe including packet counts, timeouts and TLS check;
5. exact service-restoration timeout and `TECHNICALLY_INVALID_SERVICE_RESTORE` rule;
6. exact 300 s application observation window;
7. exact mandatory raw evidence schema and timestamps;
8. exact one-command analysis/reconstruction check;
9. exact fail-closed `/proj/WellPulse` + off-POWDER evidence escrow workflow;
10. visible shell progress and deterministic final `GOLDEN_E2E=PASS/FAIL`;
11. fail-safe teardown refusal unless `EVIDENCE_ESCROW_GATE=PASS`.

RS-6 is design-only. Only after it is frozen may RS-7 decide whether to reserve POWDER and execute the Golden rehearsal.
