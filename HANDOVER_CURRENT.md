# WellPulse — Current Handover

Last updated: 2026-08-29 after completion of **WP2-P9 — GOLDEN EVIDENCE FORENSIC RECONCILIATION**.

## Canonical authority

Repository: `aayoubMSA/WellPulse`  
Branch: `main`

This file is the current operational retrieval point. Do not reconstruct current state from conversation memory.

## Executive scientific state

- WP0: **PASS**
- WP1: **PASS / FROZEN**
- WP2: **ACTIVE — OFFLINE SCIENTIFIC INTEGRATION**
- WP2-P8 manual RF campaign: **COMPLETE / GOLDEN EVIDENCE PRESERVED / NON-SCORED MANUAL REFERENCE**
- WP2-P9 golden evidence forensic reconciliation: **PASS / COMPLETE**
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

No P8/P9 result may be promoted into scored P7B.

## Completed live lane

Campaign:

`WP2-P8 — Modular Manual RF Experiment Campaign`

Platform:

- POWDER reservation `WP-07-C`
- profile `srslte-controlled-rf`
- `enb1 -> nuc1 / CORE`
- `rue1 -> nuc2 / UE`

The live campaign is complete. No P9 action contacted POWDER, reopened the testbed, or created new live evidence.

## WP2-P9 forensic closure

P9 executed only offline against immutable frozen evidence.

### P9-A — Evidence census: PASS

- authenticated Drive read-back and SHA256 verification PASS for the three frozen authorities used in reconstruction;
- **598** immutable archive members enumerated: 370 logs, 89 screenshots, 67 manifests/receipts, 72 other archived artifacts;
- E0–E11, failed/setup attempts, manifests, receipts, screenshots, logs and SHA anchors retained;
- large/private raw evidence remains on Drive; GitHub stores the canonical inventory/index and trace maps.

### P9-B — Validity classification: PASS

Permitted classes applied without promotion:

`VALID / VALID_WITH_CAVEAT / CONTROL / NULL / ABORTED / SETUP_ARTIFACT`

Important classifications:

- E1 initial run: `NULL` — treatment proceeded after failed 0 dB prerequisite;
- E5 pre-treatment attempts: `SETUP_ARTIFACT`;
- E5 manual: `VALID_WITH_CAVEAT` — missing frozen forward recovery ping;
- E8: `VALID_WITH_CAVEAT` — duplicate recovery send preserved;
- E9: `CONTROL`;
- E10-A: `VALID_WITH_CAVEAT` / censored non-recovery observation;
- E10-C attempt A: `SETUP_ARTIFACT`; suffix B: `VALID_WITH_CAVEAT`;
- E10-D: `VALID_WITH_CAVEAT` / upper-bound timing only;
- E11 R1–R3: `VALID_WITH_CAVEAT` for UE-side recovery/IP-transition replication only because the collector contains no independent CORE archive.

### P9-C — Metric reconstruction: PASS

All retained values were recomputed from raw evidence where raw reconstruction was possible.

Selected forensic results, not publication claims:

- E1R4 main MQTT sweep: `93/100` unique receiver completeness;
- E2: `151/160` unique receiver completeness;
- E3: `222/255` unique receiver completeness;
- E9 no-fault control: `60/60`;
- E10-B: MQTT publish success `6.063318 s` from declared action begin; ping success `6.609430 s`; CORE receipt followed publish by `0.060172 s`;
- E10-C-B: ping `29.247733 s`; publish-side MQTT `29.248129 s` from RF-restore action;
- E10-D: `<=10.908749 s` upper bound only;
- E10-A: no scalar recovery latency because recovery was not observed in the recorded window.

### P9-D — Cross-node reconciliation: PASS

Receiver-side unique sequence evidence governs end-to-end completeness.

Explicit surviving disagreements:

1. E1R4 seq 96 is present in sender log, absent at receiver, and has no matching sender `MQTT_FAIL` event.
2. E3 seq 150 is present in sender log, absent at receiver, and has no matching sender failure event.
3. E10-C-B later CORE verification line is duplicated; it is not double-counted.
4. E11 R1–R3 have nuc2-only collector evidence; no cross-node MQTT result is derived from them.

### P9-E — Anomaly register: PASS

Mandatory anomalies preserved plus additional findings. No anomaly or negative result was cleaned away.

### P9-F — Forensic QA: PASS

Required chain verified for every surviving reconstructed value:

`reported value -> derived result -> raw file -> frozen authority -> SHA256 -> Drive evidence`

No value requiring an unresolved attenuator physical-path mapping survives. No runtime USRP serial/firmware identity is asserted.

## P9 Drive authority verification

| Authority | SHA256 | Drive ID | P9 read-back |
|---|---|---|---|
| Master P8 evidence | `6952565D8ED630496EB7A801DB90583F2FED2EFCDC81FEACD1A2072F18FA8878` | `1TYqlzrsYLWqmM0jEEmrFWS8_QUuLShiR` | PASS |
| E10/E11 frozen collector | `A6CEBA5107610639E62709F0041FB463CACBC45AA07847AFFE6600008B77C8F6` | `1ldR77IpSX5leGPQf-ISzl4qXCjHhiit0` | PASS |
| Private golden preservation | `520B9EAE154EAF2527BC61E19A08547712C11555BAFC29C2743D34930D5FADD8` | `1GL1cLSBjKU9v_pyOd5Sl7SDF_S6-xT7K` | PASS |

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
- current Research & Grants Lessons Learned Ledger

## Immutable caveats carried forward

- E5: forward UE recovery-ping artifact observed live but not frozen.
- E8: duplicate recovery-send attempt documented.
- E10-A: no recovery within observation window.
- E10-C: attempt A invalid setup; attempt B valid with timing caveat.
- E10-D: interval is an upper bound, not exact broker-recovery latency.
- Departure `CAPTURE_STATUS.txt`: documented post-manifest append on both nodes; not corruption.
- Final profile/RSpec capture is PRIVATE because it contains credential-bearing/encrypted portal material.
- Runtime UHD probes did not independently expose a USRP device; no runtime radio serial/firmware identity may be claimed.
- Individual attenuator ID -> physical-path mapping remains unresolved and must not be inferred.
- E1R4 seq 96 and E3 seq 150 are sender/event-vs-receiver disagreements; receiver reconciliation governs completeness.
- E10-C-B later CORE verification line is duplicated and is not double-counted.
- E11 replications are nuc2-only in the collector and cannot support independent cross-node MQTT completeness claims.
- E7 reverse baseline contains a preserved 481.046 ms RTT maximum; do not clean it away.

## Evidence storage policy

1. **Google Drive = primary durable raw-evidence authority.**
2. **GitHub = canonical scientific/control authority** for contracts, inventories, hashes, analysis code, derived tables, anomaly register, QA and handovers.
3. **Home PC = independent third copy where applicable.**

Do not commit large raw archives or credential-bearing bundles into ordinary Git history.

## Next phase boundary

`WP2-P10` and later scientific integration/publication work are **NOT STARTED by this handover**.

P9 did not draft manuscript prose, generate publication claims, choose a journal, create final figures, reopen scientific scope, reinterpret negative results, or create a new experiment.

## Stop state

`WP2_P8_STATUS=COMPLETE_GOLDEN_EVIDENCE_PRESERVED`

`P8_CLASS=MANUAL_NON_SCORED_REFERENCE`

`SCORED_P7B_STATUS=UNCHANGED_NOT_PASSED`

`WP2_P9=PASS_GOLDEN_EVIDENCE_RECONCILED`

`LIVE_POWDER_DEPENDENCY=NONE_FOR_CURRENT_PHASE`

`NEXT_PHASE=WP2_P10_NOT_STARTED`
