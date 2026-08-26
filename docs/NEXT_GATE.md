# Next Gate — WP2 Recovery-Semantics Amendment

**Current frontier:** RS-3 CAUSAL ESTIMAND / H / FAIRNESS REVIEW  
**Scientific completion:** 20%  
**Scored authorization:** `false`  
**H:** `UNFROZEN`

## Governing read order

1. `HANDOVER_CURRENT.md`
2. `docs/AGENT_HANDOVER_POWDER_NEXT.md`
3. `docs/CONSORTIUM_WP2_RECOVERY_SEMANTICS_GATE_2026-08-26.md`
4. `docs/RS2_LTE_RECOVERY_MECHANISM_REVIEW_2026-08-26.md`
5. `evidence/powder/wp2-h1-valid-recovery-failure-2026-08-26.md`
6. `experiments/WP-PWD01/protocol.md`
7. `experiments/WP-PWD01/analysis-plan.md`

## Frozen state

- H1 Trial #1 remains `VALID_W1_RECOVERY_FAILURE`.
- H is not frozen.
- No replacement H trial is authorized under the old plan.
- No scored B1/W1/B2 run is authorized.
- Q0/Q1/Q2/Q3 remain `0/40/52/55 dB`; attenuator IDs `1 33 2 34` remain coupled.
- Clean-order `stop UE -> EPC -> eNB -> fresh UE` is a demonstrated testbed restoration primitive, not yet an approved scientific treatment.
- Raw H1 record-level bundles are unavailable from user-accessible persistent storage; backend recovery is pending with POWDER support.
- Mandatory future Evidence Escrow Gate is fail-closed before every teardown.

## RS-2 — PASS

Canonical verdict: `docs/RS2_LTE_RECOVERY_MECHANISM_REVIEW_2026-08-26.md`.

RS-2 established:

- persistent RF/eNB failure is not supported as the dominant blocker;
- MQTT/WellPulse is not supported as the cause of service non-recovery;
- UE-only restart is insufficient;
- EPC/eNB-only reset with a live UE is insufficient;
- the dominant diagnosis is cross-node LTE/NAS/MME/GTP-C/session-context inconsistency after the long outage;
- clean-order reinitialization of both sides is the only demonstrated deterministic recovery primitive;
- no specific bounded configuration-only/autonomous repair has been demonstrated.

RS-2 verdict:

`PASS — MECHANISM CHARACTERIZED; NO PROVEN BOUNDED AUTONOMOUS REPAIR`

Do not spend a new reservation broadly engineering old srsLTE recovery. One bounded offline source/config check remains permissible; absent a specific defect + deterministic fix + falsifiable micro-test, Strategy A closes for this paper.

## Immediate action — RS-3

RS-3 must prospectively determine the causal estimands and fairness semantics for:

- `t_rf_restore`
- `t_service_ready`
- `t_app_complete`
- H / observation horizon
- substrate-recovery reporting vs application-recovery reporting
- identical architecture-neutral service-restoration treatment across B1/W1/B2

Mandatory fairness invariant:

> A restoration action may not inspect architecture identity, queue depth, delivery success, or emerging B1/W1/B2 outcomes. It must be triggered solely by prospectively frozen substrate/testbed state and applied identically where applicable.

RS-3 must also freeze the interpretation of null/negative outcomes before scored execution.

No protocol amendment is frozen until RS-3 and the subsequent adversarial review pass.