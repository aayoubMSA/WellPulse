# Next Gate — WP2 Recovery-Semantics Amendment

**Current frontier:** POST-H1 / PRE-AMENDMENT / PRE-SCORE  
**Scientific completion:** 20%  
**Scored authorization:** `false`  
**H:** `UNFROZEN`

## Governing consortium

Read first:

1. `docs/CONSORTIUM_WP2_RECOVERY_SEMANTICS_GATE_2026-08-26.md`
2. `evidence/powder/wp2-h1-valid-recovery-failure-2026-08-26.md`
3. `experiments/WP-PWD01/H_CALIBRATION_PLAN_v1.md`
4. `docs/CONSORTIUM_PRE_WP3_REVIEW_2026-08-26.md`

## Frozen state

- H1 Trial #1 remains `VALID_W1_RECOVERY_FAILURE`.
- H is not frozen.
- No replacement H trial is authorized under the current plan.
- No scored B1/W1/B2 run is authorized.
- Q0=0 dB, Q1=40 dB, Q2=52 dB, Q3=55 dB remain frozen.
- Attenuator IDs `1 33 2 34` remain coupled.
- The demonstrated clean-order recovery sequence `stop UE -> EPC -> eNB -> fresh UE` is a qualified testbed recovery primitive only; it is not yet an approved scientific treatment.

## What the 2026-08-26 physical session proved

- correct physical Q0 readiness and `tun_srsue` route before H1;
- exact Q3 55 dB hard-outage schedule with approximately 120.0001 s full-state duration;
- technically valid failure to recover within the frozen post-Q0 bound;
- LTE core/session-context pathology rather than an application/MQTT failure dominated the non-recovery;
- UE-only recovery failed;
- EPC/eNB reset with live UE failed;
- coordinated clean-order LTE recovery passed;
- exact post-recovery TLS/MQTT/QoS1/payload-integrity path passed in 3/3 independent fresh sessions;
- raw artifacts, runtime fingerprints, and node-local chain-of-custody manifests are preserved.

## Current execution rule

Do **not** run H again yet.

The only authorized scientific work is the Recovery-Semantics consortium gate:

`RS-1 evidence reconstruction -> RS-2 LTE recovery review -> RS-3 estimand/H review -> RS-4 adversarial review -> RS-5 prospective amendment -> RS-6 Golden E2E rehearsal design -> RS-7 GO/KILL`

## Immediate action

**RS-1 — Evidence Reconstruction.**

Reconstruct the H1 timeline and recovery chain from the preserved sender/receiver CSV/JSON/SQLite artifacts and LTE logs. The purpose is to establish exact `t_rf_restore`, service-loss/recovery evidence, application queue state, and the causal boundary between LTE substrate failure and WellPulse behavior.

No protocol amendment is frozen until RS-1 through RS-4 are complete.
