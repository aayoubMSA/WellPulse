# WellPulse — Current Handover

Last updated: 2026-08-29 after completion and off-platform preservation of the **WP2-P8 POWDER manual-reference campaign**.

## Canonical authority

Repository: `aayoubMSA/WellPulse`  
Branch: `main`

This file is the current operational retrieval point. Do not reconstruct current state from conversation memory.

## Executive scientific state

- WP0: **PASS**
- WP1: **PASS / FROZEN**
- WP2: **ACTIVE — OFFLINE ANALYSIS / REPORTING**
- WP2-P8 manual RF campaign: **COMPLETE / GOLDEN EVIDENCE PRESERVED / NON-SCORED MANUAL REFERENCE**
- WP3: **BLOCKED ON SCIENTIFIC WP2 CLOSURE / CONFIRMATORY DECISION**
- WP4: **BLOCKED**
- WP5: **PREPARED / NOT EXECUTED**
- P6 Golden baseline: **VALID / FROZEN**
- P7B scored physical qualification: **NOT PASSED**
- scored execution: **NOT AUTHORIZED**

Historical scored state remains unchanged:

`B1=NULL_ABORTED_AFTER_Q3`

`HISTORICAL_B1=CONSUMED`

`SCORED_P7B_STATUS=UNCHANGED_NOT_PASSED`

No P8 exploratory/manual result may be promoted into scored P7B.

## Completed live lane

Campaign:

`WP2-P8 — Modular Manual RF Experiment Campaign`

Platform:

- POWDER reservation `WP-07-C`
- profile `srslte-controlled-rf`
- `enb1 -> nuc1 / CORE`
- `rue1 -> nuc2 / UE`

The live campaign is complete. The reservation is no longer required for the current phase.

## Golden campaign coverage

P8 produced preserved evidence for:

- E0 baseline qualification;
- E1 RF threshold characterization;
- E2 hysteresis / spontaneous recovery;
- E3 near-threshold repeatability;
- E4 RF-only recovery reference;
- E5 UE-restart recovery;
- E6 CORE-restart recovery;
- E7 optional combined recovery stress;
- E8 broker-only interruption/recovery;
- E9 no-fault duration-matched control;
- E10 recovery timing (`A` RF-only, `B` UE restart, `C` CORE restart, `D` broker restart);
- E11 three UE-restart replications.

## Canonical current handover

Read completely:

1. `HANDOVER_CURRENT.md`
2. `docs/WP2_P8_GOLDEN_EXPERIMENT_HANDOVER_2026-08-29.md`
3. `evidence/powder/WP2_P8_GOLDEN_EVIDENCE_INDEX_2026-08-29.md`
4. `experiments/WP-PWD01/WP2_P8_MANUAL_RF_EXPERIMENT_CAMPAIGN_2026-08-28.md`
5. current Research & Grants Lessons Learned Ledger

Historical P7B material should be read only when explicitly working on the scored lane.

## Immutable caveats

- E5: forward UE recovery-ping artifact observed live but not frozen.
- E8: duplicate recovery-send attempt documented.
- E10-A: no recovery within observation window.
- E10-C: attempt A invalid setup; attempt B valid.
- E10-D: observed interval is an upper bound, not exact broker-recovery latency.
- Departure `CAPTURE_STATUS.txt`: expected post-manifest append on both nodes; all other files verified.
- Final profile/RSpec capture contains credential-bearing/encrypted portal material; keep private or sanitize before sharing.
- Runtime UHD probes did not independently expose a USRP device; no runtime radio serial/firmware identity may be claimed.
- Individual attenuator ID -> physical-path mapping was not conclusively established.

## Evidence storage policy

Three-layer preservation remains mandatory:

1. **Google Drive = primary durable raw-evidence store** for frozen raw bundles, private/sanitized departure archives, hashes, manifests, platform specs and publication evidence packages.
2. **GitHub = canonical scientific/control record** for experiment contracts, evidence indexes, SHA256 anchors, anomaly register, analysis/reconciliation scripts, derived small tables, results docs, Drive pointer and handovers.
3. **Home PC = independent third copy** until Drive upload/read-back verification is complete.

Do not commit large raw archives or credential-bearing bundles into ordinary Git history.

## Current evidence anchors

- P8 master evidence: `6952565D8ED630496EB7A801DB90583F2FED2EFCDC81FEACD1A2072F18FA8878`
- E10/E11 frozen bundle: `A6CEBA5107610639E62709F0041FB463CACBC45AA07847AFFE6600008B77C8F6`
- platform specs: `5537947B03373FB6869C3E154CCCECAC387FF12481D74634AFB192CA03F26E18`
- final POWDER documentation: `2B015A8FD4655F5615D570230C8989E54A4BD6EEB6E727D04D219B9013320C19`
- private departure archive: `7DBA8CE95CF06B254939C692915325E369FFA114080AE10BACA446D4BF62A66E`
- sanitized departure archive: `236C6E269CDA6F7814B50415917D277CD7D0ED78D7D9DB0C3C4D1FE185EAE7A4`
- assembled golden handover bundle: `F94951A42C2DF429297CEC888EA81D3DC374B6E47F34D71AA2F3BCE7898642B4`

## Immediate next action

Offline only:

1. complete Drive preservation and read-back verification;
2. reconcile E0–E11 raw evidence;
3. build the anomaly register and claim-evidence matrix;
4. normalize timing endpoint semantics;
5. generate threshold/hysteresis/repeatability/recovery tables and figures;
6. build publication-grade testbed/reproducibility table;
7. draft internal scientific report;
8. then prepare manuscript-ready Methods/Results without crossing the non-scored claim boundary.

## Stop state

`WP2_P8_STATUS=COMPLETE_GOLDEN_EVIDENCE_PRESERVED`

`P8_CLASS=MANUAL_NON_SCORED_REFERENCE`

`SCORED_P7B_STATUS=UNCHANGED_NOT_PASSED`

`LIVE_POWDER_DEPENDENCY=NONE_FOR_CURRENT_PHASE`

`NEXT_PHASE=OFFLINE_EVIDENCE_RECONCILIATION_REPORTING_AND_PRESERVATION`
