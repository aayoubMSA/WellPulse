# WP2-P9 Run Validity Register — 2026-08-29

## Classification boundary

Permitted classes: `VALID / VALID_WITH_CAVEAT / CONTROL / NULL / ABORTED / SETUP_ARTIFACT`.

Classification is based on immutable raw evidence and the frozen P8 acceptance contract. A non-VALID row retains its exact reason.

| experiment | run_id | classification | reason |
|:--|:--|:--|:--|
| E0 | p8-e0-20260828T173715Z | CONTROL | CORE 60 s stability baseline; no treatment; partial node-local qualification evidence. |
| E0 | p8-e0-clean-20260828 | CONTROL | Clean bidirectional no-fault baseline: 10/10 each direction, 0% loss; UE tunnel 172.16.0.2. |
| E1 | p8-e1-20260828T1707Z | NULL | Treatment proceeded despite invalid 0 dB prerequisite: all forward ping probes 100% loss and all MQTT sends failed; violates pre-treatment gate. |
| E1 | p8-e1r2-20260828A | VALID | Valid 0–30 dB refinement run; bidirectional baseline healthy and 65/65 MQTT unique sequences received. |
| E1 | p8-e1r3-20260828A | VALID_WITH_CAVEAT | Valid partial threshold refinement stopped at first declared ping-loss stop point (50 dB); 100/100 MQTT complete. |
| E1 | p8-e1r4-20260828A | VALID | Valid fine boundary run 48–52 dB; receiver-side MQTT reconciliation available. |
| E2 | p8-e2-20260828A | VALID | Valid downward hysteresis/recovery sweep with both node evidence and receiver sequence reconciliation. |
| E3 | p8-e3-20260828A | VALID | Valid three-cycle near-threshold repeatability run with receiver reconciliation. |
| E4 | p8-master-20260828A-e4 | VALID | Valid RF-only impairment/recovery reference with baseline, impairment and recovery phases frozen. |
| E5 | p8-master-20260828A-e5 | SETUP_ARTIFACT | Pre-treatment MQTT-gate SSH failure; fail-safe RF restore; no scientific treatment began. |
| E5 | p8-master-20260828A-e5-a01 | SETUP_ARTIFACT | Pre-treatment CORE→UE baseline ping failed 100%; no scientific treatment began. |
| E5 | p8-e5-20260829-000744 | SETUP_ARTIFACT | Gate-only evidence; no treatment phase or valid recovery experiment. |
| E5 | p8-e5-manual-20260829A | VALID_WITH_CAVEAT | Valid UE-restart recovery run; forward UE recovery-ping was observed live but was not frozen. |
| E6 | p8-e6-manual-20260829A | VALID | Valid CORE-restart recovery run with both-node raw evidence. |
| E7 | p8-e7-manual-20260829A | VALID | Valid combined recovery stress run with both-node raw evidence. |
| E8 | p8-e8-manual-20260829A | VALID_WITH_CAVEAT | Valid broker-only control with duplicate recovery-send attempt preserved; unique sequence IDs used for completeness. |
| E9 | p8-e9-manual-20260829A | CONTROL | Duration-matched no-fault control with 60/60 MQTT unique delivery and clean bidirectional ping. |
| E10-A | p8-e10a-manual-20260829A | VALID_WITH_CAVEAT | Valid censored RF-only timing observation: no ping or MQTT recovery inside the recorded observation window; no exact recovery latency. |
| E10-B | p8-e10b-manual-20260829A | VALID | Valid RF restore + UE restart timing run with publish and receiver-side MQTT evidence. |
| E10-C | p8-e10c-manual-20260829A | SETUP_ARTIFACT | Attempt A incomplete/mislocated setup evidence; no complete two-node timing result. |
| E10-C | p8-e10c-manual-20260829B | VALID_WITH_CAVEAT | Valid CORE-restart timing run; primary MQTT timing is publish-side; later receiver verification exists. |
| E10-D | p8-e10d-manual-20260829A | VALID_WITH_CAVEAT | Valid broker-restart observation but timing is an upper bound because the first post-restart MQTT probe was manually initiated. |
| E11 | p8-e11-r1-20260829A | VALID_WITH_CAVEAT | UE-side replication valid for impairment/recovery and IP transition; collector has no independent nuc1/CORE archive. |
| E11 | p8-e11-r2-20260829A | VALID_WITH_CAVEAT | UE-side replication valid for impairment/recovery and IP transition; collector has no independent nuc1/CORE archive. |
| E11 | p8-e11-r3-20260829A | VALID_WITH_CAVEAT | UE-side replication valid for impairment/recovery and IP transition; collector has no independent nuc1/CORE archive. |

## Important interpretation controls

- `p8-e1-20260828T1707Z` is `NULL`, because treatment continued after the 0 dB prerequisite had already failed.
- The three pre-treatment E5 attempts are `SETUP_ARTIFACT`; no scientific treatment began.
- E9 is a `CONTROL`, not a treatment run.
- E10-A is a valid censored observation with a caveat: no recovery occurred inside the recorded observation window; no exact recovery latency exists.
- E10-C attempt A is a setup artifact; suffix B is the valid run.
- E11 R1-R3 are `VALID_WITH_CAVEAT` for UE-side recovery replication only because the collector bundle contains nuc2/UE evidence but no independent nuc1/CORE archive for those replications.

`P9_B_VALIDITY_CLASSIFICATION=PASS`
