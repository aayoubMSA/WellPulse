# Next Gate — WP2-P6 One Clean Non-Scored Golden

**Current frontier:** WP2-P6 ACTIVE after explicit user continuation + short QA PASS  
**Scientific completion:** 20%  
**WP2 management/readiness before P6 result:** 80/100  
**K1–K8 compatibility:** `PASS / CLOSED`  
**Pre-integration compatibility:** `PASS`  
**AUDIT-R1:** `PASS`  
**Live HCI/raw-evidence gate:** `PASS / CLOSED`  
**P6 short QA:** `PASS`  
**Golden rebook authorization:** `true — exactly one non-scored P6 reservation/run`  
**Scored authorization:** `false`

Canonical P5 closure:

`docs/WP2_P5_HCI_RAW_EVIDENCE_CLOSURE_2026-08-27.md`

P6 short QA:

`docs/WP2_P6_SHORT_QA_2026-08-27.md`

P6 live workflow:

`.github/workflows/wp2-p6-golden.yml`

P6 live execution controller:

`powder/wp2_p6_golden_execute.sh`

## Exact P6 path — authorized once

1. Run the premutation offline QA inside the P6 workflow.
2. Immediately before booking, inspect `https://www.powderwireless.net/resinfo.php` and record `RESOURCE_AVAILABILITY_PREFLIGHT=PASS|DEFER|UNKNOWN`. Ambiguous/unparseable advisory output is `UNKNOWN` and defers authority to the Portal lifecycle gates; it never changes frozen hardware/profile/bindings.
3. Create exactly one reservation using `PowderProfiles/srslte-controlled-rf`, revision target `a6da96560b6526dc6816761282722c996418fd8c`, bindings `enb_node=nuc1`, `ue_node=nuc2`, `ue_type=srsue`.
4. Require authoritative Portal READY, experiment identity, hard-expiry/time budget, exact `nuc5300` hardware, expected image, exact manifested logical/physical mapping and exact profile repository revision before science.
5. Establish a clean Q0 5/5 user-plane baseline before protected science.
6. Execute exactly one non-scored Golden G0-G10 with passive HCI only and frozen `H_app=300 s from t_service_ready`.
7. After protected observation/reconstruction, require verified `/proj/WellPulse` persistent escrow and `TEARDOWN_AUTHORIZED=NO` on the node side.
8. Controller-pull the exact persistent bundle and create deterministic TAR + SHA-256.
9. Upload the TAR through the qualified pinned GitHub artifact action, independently download/read it back, and verify outer TAR SHA-256 plus internal `SOURCE_SHA256SUMS`.
10. Only after `CONTROLLER_OFFPOWDER_GATE=PASS`, `EVIDENCE_ESCROW_GATE=PASS`, and `TEARDOWN_AUTHORIZED=YES` may the workflow terminate the reservation and confirm teardown.
11. STOP. WP2-P7 formal scientific closure/scored authorization remains separate.

## Fail-closed behavior

- Failure before protected science starts: bounded reservation cleanup is allowed.
- Failure after protected science starts before final evidence closure: automatic teardown is prohibited; preserve the experiment live for evidence recovery.
- HCI failure alone is non-authoritative and cannot invalidate science.
- Unfavorable application completeness is a valid non-scored Golden outcome and is not a reason to alter the protocol or horizon.

## Frozen controls

- H1 remains `VALID_W1_RECOVERY_FAILURE`; original H1 node-local raw bundles were not recovered.
- Q0/Q1/Q2/Q3 remain `0/40/52/55 dB`; IDs `1 33 2 34` remain coupled.
- K1–K8 remain PASS/CLOSED absent a material interface change.
- `H_app=300 s from t_service_ready` is frozen.
- outcome-derived/W1-derived/Golden-derived H recalibration is prohibited.
- `HCI_CONTROL_ACTIONS_ENABLED=false`.
- `scored_runs_authorized=false`.
- no WP3 B1/W1/B2 scored execution is authorized.

Shortest path:

`P6 short QA PASS -> one P6 Golden -> evidence round-trip -> teardown -> STOP -> WP2-P7 closure/scored authorization -> WP3 -> WP4 -> WP5`
