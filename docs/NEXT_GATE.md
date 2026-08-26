# Next Gate — WP2 Recovery-Semantics Amendment

**Current frontier:** RS-5 PROSPECTIVE PROTOCOL AMENDMENT  
**Scientific completion:** 20%  
**Scored authorization:** `false`  
**H:** `UNFROZEN`

## Governing read order

1. `HANDOVER_CURRENT.md`
2. `docs/AGENT_HANDOVER_POWDER_NEXT.md`
3. `docs/CONSORTIUM_WP2_RECOVERY_SEMANTICS_GATE_2026-08-26.md`
4. `docs/RS2_LTE_RECOVERY_MECHANISM_REVIEW_2026-08-26.md`
5. `docs/RS3_ESTIMAND_H_FAIRNESS_REVIEW_2026-08-26.md`
6. `docs/RS4_ADVERSARIAL_REVIEW_2026-08-26.md`
7. `evidence/powder/wp2-h1-valid-recovery-failure-2026-08-26.md`
8. `experiments/WP-PWD01/protocol.md`
9. `experiments/WP-PWD01/analysis-plan.md`

## Frozen state

- H1 Trial #1 remains `VALID_W1_RECOVERY_FAILURE`.
- H is not frozen.
- No replacement H trial is authorized under the old plan.
- No scored B1/W1/B2 run is authorized.
- Q0/Q1/Q2/Q3 remain `0/40/52/55 dB`; attenuator IDs `1 33 2 34` remain coupled.
- Raw H1 record-level bundles remain unavailable from user-accessible persistent storage; POWDER backend recovery is pending.
- Mandatory Evidence Escrow Gate remains fail-closed before teardown.

## RS-2 — PASS

Mechanism characterized as cross-node LTE/NAS/MME/GTP-C/session-context inconsistency after the long outage. No proven bounded autonomous repair was identified. Broad engineering of old srsLTE is not authorized.

## RS-3 — PASS

Accepted conceptual decomposition:

- `t_rf_restore` = physical Q3->Q0 treatment endpoint;
- `t_service_ready` = first architecture-blind proof of usable experimental service;
- `t_app_complete` = application-cohort completion;
- `T_service = t_service_ready - t_rf_restore`;
- `T_app = t_app_complete - t_service_ready`;
- `T_total = t_app_complete - t_rf_restore`;
- `cohort_cutoff_utc = t_rf_restore` remains fixed.

## RS-4 — PASS WITH ONE MANDATORY MODIFICATION

Canonical verdict: `docs/RS4_ADVERSARIAL_REVIEW_2026-08-26.md`.

The two-clock recovery decomposition and fairness framework survived adversarial review. The proposed W1-only `H_app` calibration did not.

RS-4 KILLED any observation-horizon rule chosen from W1 performance because the primary endpoint window would then be structurally informed by one architecture under comparison.

RS-5 must therefore:

1. adopt one architecture-independent fixed/common application observation horizon or architecture-independent calibration source;
2. freeze a deterministic architecture-blind service-restoration rule;
3. preserve/report `T_service`, `T_app`, and `T_total`;
4. retain `cohort_cutoff_utc = t_rf_restore`;
5. define symmetric service-restoration failure/technical-invalidity rules;
6. embed the fail-closed Evidence Escrow Gate into the executable protocol;
7. freeze the null/negative-result interpretation tree before scoring.

## Immediate action — RS-5

Draft the prospective protocol amendment only. No live POWDER execution yet.

RS-5 must choose and justify the exact architecture-independent application observation horizon and the exact deterministic service-restoration trigger/procedure. It must then amend the protocol/analysis semantics without changing Q0–Q3, scenario definitions, architecture comparators, or H1 classification.

After RS-5 passes, proceed to RS-6 Golden E2E rehearsal design. Only RS-7 may issue `GO_REOPEN_H`.