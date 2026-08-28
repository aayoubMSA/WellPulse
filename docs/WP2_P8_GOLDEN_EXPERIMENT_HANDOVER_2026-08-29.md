# WP2-P8 Golden Experiment Handover — 2026-08-29

## Canonical status

- POWDER reservation: `WP-07-C`
- Profile: `srslte-controlled-rf`
- Topology: `enb1 -> nuc1 / CORE`; `rue1 -> nuc2 / UE`
- Campaign: `WP2-P8`
- Classification: **manual-reference / non-scored**
- Live POWDER campaign: **COMPLETE**
- Scored P7B status: **UNCHANGED / NOT PASSED**
- Historical B1: **NULL / ABORTED**

P8 evidence must never be promoted into scored P7B.

## Scientific result envelope

The campaign produced controlled two-node LTE/RF evidence spanning baseline qualification, attenuation threshold characterization, hysteresis, near-threshold repeatability, RF-only recovery behavior, UE-restart recovery, CORE-restart recovery, combined recovery stress, broker-only interruption/recovery, no-fault control, recovery timing, and three UE-restart replication runs.

No new POWDER experiment is required for the current offline reporting/preservation phase.

## Key observations

- `<=49 dB` was a healthy reference region in the fine sweep.
- `50–51 dB` was a degradation region in which MQTT remained comparatively resilient.
- `52 dB` was a severe region with major ICMP loss and MQTT incompleteness.
- E2 showed autonomous recovery as attenuation was reduced.
- E3 showed repeatable severity at 52 dB and material variability near the transition.
- E5 demonstrated recovery after RF restore + srsUE restart.
- E6 demonstrated recovery after CORE restart under impairment followed by RF restore.
- E7 demonstrated combined recovery after severe impairment, CORE restart, RF restore and UE restart.
- E8 isolated broker failure: LTE remained healthy while MQTT failed, then recovered after broker restart.
- E9 provided a no-fault control with repeated clean delivery.
- E10-A observed no RF-only recovery within the observation window, showing that autonomous RF-only recovery was not deterministic across runs.
- E10-B recovered after RF restore + UE restart in approximately six seconds from the recovery action; receiver-side MQTT receipt was observed.
- E10-C valid run is suffix `B`; suffix `A` is an invalid setup artifact. The valid run recovered roughly 29.25 s after RF restore action. Primary MQTT timing is publish-side; later end-to-end verification exists.
- E10-D yields an upper bound only because the first manually started MQTT probe succeeded after broker restart; exact broker-restart latency is unresolved.
- E11 executed three UE-restart replications after severe impairment; recovery runs were clean.

## Immutable anomaly register

1. E5 forward UE recovery-ping artifact was observed live but not frozen.
2. E8 contains a documented duplicate recovery-send attempt.
3. E10-A did not recover within its observation window.
4. E10-C attempt A is invalid setup evidence; attempt B is valid.
5. E10-D is an upper bound, not an exact broker recovery latency.
6. Departure `CAPTURE_STATUS.txt` was appended after manifest generation on both nodes. All other files verified; classify as `DOCUMENTED_POST_MANIFEST_APPEND`, not corruption.
7. Final profile/RSpec capture contains credential-bearing/encrypted portal material and must remain private or be sanitized before sharing.
8. Runtime UHD probes did not independently expose a USRP device. Profile/RSpec evidence identifies the NUC5300/B210 topology, but no runtime B210 serial/firmware identity may be claimed.
9. Individual attenuator ID -> physical-path mapping was not conclusively established and must not be inferred.

## Claim boundary

Supported: controlled POWDER LTE/RF impairment and recovery observations, cross-layer network/application behavior, recovery-mechanism comparisons, carefully qualified timing endpoints, and the evidence-first two-node methodology.

Not supported by P8 alone: scored P7B acceptance, population reliability percentages, Siwa/field/pump/hydraulic/agronomic claims, a universal RF threshold beyond this profile, exact broker restart latency from E10-D, or a runtime USRP serial/firmware claim.

## Preservation doctrine

1. **Google Drive** — primary durable raw-evidence store for frozen ZIPs, manifests, hashes, private/sanitized departure captures, platform specs and publication evidence bundles.
2. **GitHub** — canonical scientific/control record for contracts, handovers, evidence indexes, hashes, anomaly register, analysis/reconciliation scripts and derived small tables. Do not commit credential-bearing or large raw archives to ordinary Git history.
3. **Home PC** — independent third copy until Drive upload/read-back verification is complete.

## Offline next phase

1. E0–E11 evidence reconciliation.
2. Per-experiment outcome table.
3. Timing endpoint-semantics audit.
4. Threshold/hysteresis/repeatability analysis.
5. Recovery-mechanism comparison.
6. No-fault control comparison.
7. Platform/testbed reproducibility table.
8. Figures/tables from verified raw evidence only.
9. Claim-evidence matrix.
10. Internal scientific report and manuscript-ready methods/results candidate.
11. Drive read-back verification and final GitHub closure.

`POWDER_LIVE_CAMPAIGN=COMPLETE`

`P8_CLASS=MANUAL_NON_SCORED_REFERENCE`

`SCORED_P7B_STATUS=UNCHANGED_NOT_PASSED`

`NEXT_PHASE=OFFLINE_EVIDENCE_RECONCILIATION_REPORTING_AND_PRESERVATION`
