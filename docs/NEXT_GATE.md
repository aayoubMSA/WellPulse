# Next Gate — WP2 K-Fastlane Recovery to Compatibility Closure

**Current frontier:** first bounded K-fastlane live compatibility reservation failed during POWDER provisioning  
**Scientific completion:** 20%  
**Scored authorization:** `false`  
**Golden rebook authorization:** `false`

## Current live result

GitHub Actions run:

`33084240768`

Workflow:

`.github/workflows/wp2-kfastlane-live-compat.yml`

Trigger commit:

`dd275a3f7dbc75a7096b587ae3f01d61ff801411`

Compatibility experiment:

`02bc305d-5d84-48f9-b518-dbebd1728ee6`

Classification:

`INFRASTRUCTURE_ONLY_NON_SCORED`

Observed Portal sequence:

`provisioning -> failed`

The run failed at the READY/status/expiry binding step with rc `21` before any Golden workload, H calibration, or scored science.

Subsequent live compatibility checks were skipped:

- manifest hardware/image/login identity;
- runtime/profile fingerprints;
- K4 detached-process timing;
- K6 cross-node `/proj/WellPulse` persistence;
- actual controller artifact round-trip.

Mandatory cleanup executed and returned:

`COMPAT_CLEANUP=TERMINATE_REQUESTED`

Before any replacement reservation, verify the failed experiment no longer resolves.

## Current K status

- `K1=PASS`
- `K2=OFFLINE_PASS_LIVE_OPEN`
- `K3=STATIC_PASS_LIVE_BLOCKED_ON_PROVISIONING_FAILURE`
- `K4=IMPLEMENTED_LIVE_NOT_RUN`
- `K5=IMPLEMENTED_LIVE_NOT_RUN`
- `K6=IMPLEMENTED_LIVE_NOT_RUN`
- `K7=POLICY_FROZEN_STATIC_ASSERTION_NEEDS_FIX`
- `K8=BLOCKED`

`PRE_INTEGRATION_COMPATIBILITY_GATE=BLOCKED`

`LIVE_HCI_AND_RAW_EVIDENCE_GATE=BLOCKED`

`REBOOK_GOLDEN=false`

## Evidence architecture now frozen for the fastlane

Critical evidence chain:

`raw -> /proj/WellPulse -> SHA verification -> controller pull -> GitHub Actions artifact -> independent download/read-back -> outer + internal hash verification -> teardown authority`

Google Drive is no longer a teardown-critical dependency. It may be used later only as an optional secondary mirror.

The node-side Golden orchestrator must never emit teardown authority by itself.

Before teardown of future science require:

- `RAW_EVIDENCE_COMPLETE=PASS`
- `EVIDENCE_ESCROW_GATE=PASS`
- `TEARDOWN_AUTHORIZED=YES`

## Exact next bounded work

Do not book another reservation immediately.

1. Verify experiment `02bc305d-5d84-48f9-b518-dbebd1728ee6` is absent/terminated.
2. Obtain the smallest authoritative reason/evidence for why provisioning entered `failed`.
3. Re-run corrected offline K3 CLI QA once.
4. Fix the K7 static checker false-confidence issue and rerun static acceptance once.
5. Decide whether the provisioning failure is transient/bounded or requires a profile/resource correction.
6. Only then, if justified, use **one** replacement compatibility-only reservation to finish K3/K5, manifest/runtime identity, K4, K6, controller round-trip, and cleanup.
7. Reconcile the compatibility matrix.
8. Set K8 PASS only from actual evidence.

## After K8

Immediately return to the WP2 mission:

1. close `LIVE_HCI_AND_RAW_EVIDENCE_GATE` with passive/one-way HCI and complete raw evidence contract;
2. then request one fresh non-scored Golden reservation;
3. run one clean G0–G10 Golden rehearsal;
4. preserve verified complete raw evidence before teardown;
5. only after Golden PASS requalify/freeze H;
6. close WP2 scientifically;
7. scored WP3 remains separately gated.

## Frozen scientific state

- H1 remains `VALID_W1_RECOVERY_FAILURE`.
- H1 raw recovery remains closed/failed; do not reopen salvage without genuinely new evidence.
- Q0/Q1/Q2/Q3 remain `0/40/52/55 dB` with attenuator IDs `1 33 2 34` coupled.
- Primary cohort cutoff remains `t_rf_restore`.
- Application horizon remains 300 s from `t_service_ready`.
- `H=UNFROZEN`.
- `scored_runs_authorized=false`.
- no B1/W1/B2 scored work.

## HCI rule

Future HCI remains passive, one-way, and non-authoritative:

`HCI_CONTROL_ACTIONS_ENABLED=false`

No independent unqualified probe may run during the protected scientific window.

## Read first

1. `HANDOVER_CURRENT.md`
2. `docs/AGENT_HANDOVER_WP2_KFASTLANE_2026-08-27.md`
3. this file
4. `.github/workflows/wp2-kfastlane-live-compat.yml`
5. `docs/PRE_INTEGRATION_COMPATIBILITY_GATE.md`
6. `docs/LIVE_EXPERIMENT_HCI_AND_RAW_EVIDENCE.md`

Shortest mission path:

`provisioning failure -> remaining K live proofs -> K7 fix -> K8 -> HCI/raw gate -> clean Golden -> H -> WP2 close -> WP3 -> WP4 -> WP5`
