# WellPulse — Current Handover

Last updated: 2026-08-29 after completion and independent closure re-audit of **WP2-P9 — GOLDEN EVIDENCE FORENSIC RECONCILIATION**.

## Canonical authority

Repository: `aayoubMSA/WellPulse`  
Branch: `main`

This file is the current operational retrieval point. Do not reconstruct current state from conversation memory.

## Executive scientific state

- WP0: **PASS**
- WP1: **PASS / FROZEN**
- WP2: **ACTIVE — OFFLINE SCIENTIFIC INTEGRATION**
- WP2-P8 manual RF campaign: **COMPLETE / GOLDEN EVIDENCE PRESERVED / NON-SCORED MANUAL REFERENCE**
- WP2-P9 golden evidence forensic reconciliation: **PASS / COMPLETE / INDEPENDENT CLOSURE RE-AUDIT PASS**
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

No P8/P9 result may be promoted, reinterpreted or relabelled as scored P7B.

## Completed live lane

Campaign: `WP2-P8 — Modular Manual RF Experiment Campaign`

Platform:

- POWDER reservation `WP-07-C`
- profile `srslte-controlled-rf`
- `enb1 -> nuc1 / CORE`
- `rue1 -> nuc2 / UE`

The live campaign is complete. P9 was entirely offline: no POWDER contact, RF mutation, service restart, reservation action, or new live experiment occurred.

## WP2-P9 closure

### P9-A — Evidence census: PASS

Three authenticated Drive authorities were downloaded read-only and their SHA256 values recomputed successfully. Their ZIP central directories enumerate **598 immutable file members**: master P8 `357`, E10/E11 `46`, private golden preservation `195`.

Full path/hash enumeration remains inside the immutable archive-native manifests:

- master: `meta/SHA256_ALL_FILES.txt` + `meta/FILE_INVENTORY.csv`;
- E10/E11: `meta/SHA256_ALL_COLLECTED.txt` + `meta/RUN_STATUS.csv` + node SHA manifests;
- private preservation: `SHA256_ALL.txt` + `PRESERVATION_MANIFEST.json`.

Independent closure re-audit found two deterministic archive-native self-log post-manifest appends: master `meta/collection.log` and E10/E11 `meta/collector.log` each received only their final `creating final ZIP` line after their own hash was recorded. The stored hashes exactly match the pre-append byte prefixes, the outer ZIP SHA256 values match Drive, all other parsed manifest entries verify, and neither collector log is used for metrics. Classified `A-018 / DOCUMENTED_POST_MANIFEST_SELF_LOG_APPEND`, not corruption.

All **89** unclassified PNG screenshots are individually preserved and hashed in the private package; their UUID names do not support defensible run attribution and they are not used numerically.

### P9-B — Validity classification: PASS

Allowed classes only:

`VALID / VALID_WITH_CAVEAT / CONTROL / NULL / ABORTED / SETUP_ARTIFACT`

Important classifications:

- E1 initial `p8-e1-20260828T1707Z`: `NULL` — treatment proceeded after a failed 0 dB prerequisite.
- E5 setup/pre-science artifacts/fragments: `p8-master-20260828A-e5`, `p8-master-20260828A-e5-a01`, `p8-e5-20260829-000402`, `p8-e5-20260829-000744`.
- E5 manual: `VALID_WITH_CAVEAT` — forward recovery-ping observed live but not frozen.
- E8: `VALID_WITH_CAVEAT` — duplicate recovery send preserved.
- E9: `CONTROL`.
- E10-A: `VALID_WITH_CAVEAT` — censored non-recovery observation; no exact latency.
- E10-C attempt A: `SETUP_ARTIFACT`; suffix B: `VALID_WITH_CAVEAT`.
- E10-D: `VALID_WITH_CAVEAT` — upper-bound timing only.
- E11 R1–R3: `VALID_WITH_CAVEAT` for UE-side impairment/recovery/IP-transition replication only; no independent CORE collector archive.

### P9-C — Metric reconstruction: PASS

All retained values were recomputed from immutable raw evidence where reconstruction was possible. Receiver-side unique IDs govern MQTT completeness.

Selected forensic values, **not publication claims**:

- E1R4 MQTT main sweep: `93/100` unique received.
- E2: `151/160` unique received.
- E3: `222/255` unique received.
- E9 no-fault control: `60/60`.
- E10-B: action-begin→first MQTT publish `6.063318 s`; action-begin→first ping `6.609430 s`; publish→CORE receipt `0.060172 s`.
- E10-C-B: RF-restore→first ping `29.247733 s`; RF-restore→first publish `29.248129 s`.
- E10-D: broker-start action-begin→first manually initiated successful publish `<=10.908749 s`; command-complete→same probe `<=10.872618 s`; neither is exact broker recovery latency.
- E10-A: no scalar recovery latency because recovery was not observed inside the preserved window.

Independent closure re-audit directly reproduced the principal receiver-side MQTT results from raw files: E1R2 `65/65`, E1R3 `100/100`, E1R4 `93/100`, E2 `151/160`, E3 `222/255`, E4/E5/E6/E7/E8 `40/60` unique, and E9 `60/60`. E8 retains 80 sender lines but only 60 unique sequence IDs.

### P9-D — Cross-node reconciliation: PASS

Explicit surviving disagreements/asymmetries:

1. E1R4 seq `96`: sender present, receiver absent, no matching sender `MQTT_FAIL`; receiver governs completeness.
2. E3 seq `150`: sender present, receiver absent, no matching sender failure event; receiver governs completeness.
3. E5 forward recovery ping is missing from frozen evidence; reverse recovery/MQTT evidence remains available.
4. E8 recovery seq `41–60` was sent twice; unique IDs govern completeness.
5. E10-C-B later CORE verification line is duplicated; it is not double-counted.
6. E11 R1–R3 are nuc2-only in the collector; no reverse-path/MQTT cross-node metric is inferred.

### P9-E — Anomaly register: PASS

Mandatory anomalies are preserved plus additional forensic findings. No negative result, failed attempt, setup artifact, duplicate, outlier, missing artifact or unresolved mapping was cleaned away.

`A-018` additionally records the two collector self-log post-manifest append exceptions discovered during closure re-audit.

### P9-F — Claim-independent forensic QA: PASS

Required trace chain verified for every surviving reconstructed value:

`reported value → reconstructed table → raw-file root → frozen archive → SHA256 → Drive evidence`

`DOCUMENTED_POST_MANIFEST_SELF_LOG_APPEND=2`

`UNSUPPORTED_SURVIVING_VALUES=0`

`UNRESOLVED_ARCHIVE_HASH_DISCREPANCIES=0`

No value requires invented attenuator-ID→physical-path mapping. Runtime UHD identity remains unresolved and is not claimed.

## P9 Drive authority verification

| Authority | SHA256 | Drive ID | P9 verification |
|---|---|---|---|
| Master P8 evidence | `6952565D8ED630496EB7A801DB90583F2FED2EFCDC81FEACD1A2072F18FA8878` | `1TYqlzrsYLWqmM0jEEmrFWS8_QUuLShiR` | PASS |
| E10/E11 frozen collector | `A6CEBA5107610639E62709F0041FB463CACBC45AA07847AFFE6600008B77C8F6` | `1ldR77IpSX5leGPQf-ISzl4qXCjHhiit0` | PASS |
| Private golden preservation | `520B9EAE154EAF2527BC61E19A08547712C11555BAFC29C2743D34930D5FADD8` | `1GL1cLSBjKU9v_pyOd5Sl7SDF_S6-xT7K` | PASS |

Additional preservation anchors remain authoritative in `WP2_P8_GOLDEN_EVIDENCE_INDEX_2026-08-29.md` and `WP2_P8_DRIVE_PRESERVATION_RECEIPT_2026-08-29.md`.

## Canonical P9 outputs

Read these before any P10+ scientific interpretation:

1. `evidence/powder/WP2_P9_CANONICAL_EVIDENCE_CENSUS_2026-08-29.md`
2. `evidence/powder/WP2_P9_CENSUS_E10_E11_SHA256_2026-08-29.csv`
3. `evidence/powder/WP2_P9_RUN_VALIDITY_REGISTER_2026-08-29.md`
4. `evidence/powder/WP2_P9_RECONSTRUCTED_METRIC_TABLES_2026-08-29.md`
5. `evidence/powder/WP2_P9_CROSS_NODE_RECONCILIATION_2026-08-29.md`
6. `evidence/powder/WP2_P9_ANOMALY_REGISTER_2026-08-29.md`
7. `evidence/powder/WP2_P9_FORENSIC_TRACE_MAP_2026-08-29.md`
8. `evidence/powder/WP2_P9_FORENSIC_QA_REPORT_2026-08-29.md`
9. `analysis/powder/wp2_p9_reconstruct.py`

P8 source authorities remain:

- `docs/WP2_P8_GOLDEN_EXPERIMENT_HANDOVER_2026-08-29.md`
- `evidence/powder/WP2_P8_GOLDEN_EVIDENCE_INDEX_2026-08-29.md`
- `evidence/powder/WP2_P8_DRIVE_PRESERVATION_RECEIPT_2026-08-29.md`
- `experiments/WP-PWD01/WP2_P8_MANUAL_RF_EXPERIMENT_CAMPAIGN_2026-08-28.md`
- current Research & Grants Lessons Learned Ledger.

## Immutable caveats carried forward

- E5 missing frozen forward recovery-ping artifact.
- E8 duplicate recovery-send attempt.
- E10-A no recovery within observation window.
- E10-C attempt A invalid setup; attempt B valid with timing caveat.
- E10-D upper-bound timing only.
- Departure `CAPTURE_STATUS.txt` documented post-manifest append on both nodes; not corruption.
- Master `meta/collection.log` and E10/E11 `meta/collector.log` each contain one documented self-log append after their own manifest hash was generated; outer ZIP hashes remain exact and the logs are not metric sources.
- Final profile/RSpec capture is PRIVATE because it contains credential-bearing/encrypted portal material.
- Runtime UHD probes did not independently expose a USRP device; no runtime radio serial/firmware identity may be claimed.
- Individual attenuator ID→physical-path mapping remains unresolved and must not be inferred.
- E1R4 seq 96 and E3 seq 150 are sender/event-vs-receiver disagreements; receiver reconciliation governs completeness.
- E10-C-B later CORE verification line is duplicated and not double-counted.
- E11 collector is UE-side only for R1–R3.
- E7 reverse baseline contains a preserved `481.046 ms` RTT maximum; do not clean it away.
- 89 screenshots are preserved but unclassified by run.

## Storage authority

1. **Google Drive = primary durable authority for frozen/raw binary evidence.**
2. **GitHub = canonical scientific/control record** for manifests, hashes, contracts, analysis scripts, derived tables, anomaly register, results and handovers.
3. **Home PC = independent third copy where applicable.**

Raw archives remain immutable. Do not commit credential-bearing or large raw bundles into ordinary Git history.

## Scope boundary and next phase

`WP2-P10` and later scientific integration/publication work are **NOT STARTED** by this handover.

P9 did not draft manuscript prose, generate publication claims, choose a journal, create final figures, reopen scientific scope, reinterpret negative results, or create a new live experiment.

## Stop state

`WP2_P8_STATUS=COMPLETE_GOLDEN_EVIDENCE_PRESERVED`

`P8_CLASS=MANUAL_NON_SCORED_REFERENCE`

`SCORED_P7B_STATUS=UNCHANGED_NOT_PASSED`

`WP2_P9=PASS_GOLDEN_EVIDENCE_RECONCILED`

`LIVE_POWDER_DEPENDENCY=NONE_FOR_CURRENT_PHASE`

`NEXT_PHASE=WP2_P10_NOT_STARTED`
