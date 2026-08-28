# WP2-P9 Canonical Evidence Census — 2026-08-29

## Scope and boundary

This census belongs only to `WP2-P9 — GOLDEN EVIDENCE FORENSIC RECONCILIATION`.

`P8_CLASS=MANUAL_NON_SCORED_REFERENCE`

`SCORED_P7B_STATUS=UNCHANGED_NOT_PASSED`

No P8 item is promoted or re-labelled as scored P7B evidence.

## Frozen Drive authorities used for forensic reconstruction

| Authority archive | SHA256 | Drive ID | P9 authenticated Drive read-back |
|---|---|---|---|
| `WellPulse-P8-Evidence-ALL-20260829-004254.zip` | `6952565D8ED630496EB7A801DB90583F2FED2EFCDC81FEACD1A2072F18FA8878` | `1TYqlzrsYLWqmM0jEEmrFWS8_QUuLShiR` | PASS |
| `WellPulse-P8-E10-E11-20260829-015817-FROZEN.zip` | `A6CEBA5107610639E62709F0041FB463CACBC45AA07847AFFE6600008B77C8F6` | `1ldR77IpSX5leGPQf-ISzl4qXCjHhiit0` | PASS |
| `WellPulse_POWDER_Golden_Preservation_PRIVATE_2026-08-29.zip` | `520B9EAE154EAF2527BC61E19A08547712C11555BAFC29C2743D34930D5FADD8` | `1GL1cLSBjKU9v_pyOd5Sl7SDF_S6-xT7K` | PASS |

The SHA256 values above were recomputed from authenticated Drive downloads during P9 and matched the GitHub/Drive preservation anchors.

## Canonical census result

A read-only member-level walk of all three authorities produced **598 immutable member records**:

- logs: **370**;
- screenshots: **89**;
- manifests / receipts: **67**;
- other archived artifacts: **72**.

The canonical inventory is this document plus the archive-native immutable member manifests below. This avoids duplicating large/private raw bundles into ordinary Git history while retaining full member enumeration and per-file hashes:

| Authority | Full member/hash enumeration inside frozen authority | P9 GitHub cross-check |
|---|---|---|
| Master P8 evidence | `meta/SHA256_ALL_FILES.txt` — 354 hashed file entries, plus archive directory/member census | authority SHA and Drive ID above; run/source map in `WP2_P9_FORENSIC_TRACE_MAP_2026-08-29.md` |
| E10/E11 frozen collector | `meta/SHA256_ALL_COLLECTED.txt`, `meta/RUN_STATUS.csv`, node-local SHA256 manifests | `WP2_P9_CENSUS_E10_E11_SHA256_2026-08-29.csv` reproduces the 46 collector members with per-entry SHA256 |
| Private golden preservation | `SHA256_ALL.txt` and `PRESERVATION_MANIFEST.json` | authority SHA and Drive ID above; contains preserved standalone E7/E8/E9 archives plus screenshots/derived preservation artifacts |

All screenshots, logs, manifests, receipts and other artifacts encountered by the census remain addressable through those frozen manifests. No file was modified to create this census.

## Run inventory

| Scientific slot | Enumerated run/artifact identities | Census disposition |
|---|---|---|
| E0 | `p8-e0-20260828T173715Z`; `p8-e0-clean-20260828` | CONTROL evidence retained |
| E1 | `p8-e1-20260828T1707Z`; `p8-e1r2-20260828A`; `p8-e1r3-20260828A`; `p8-e1r4-20260828A` | NULL initial + valid refinement runs retained |
| E2 | `p8-e2-20260828A` | retained |
| E3 | `p8-e3-20260828A` | retained |
| E4 | `p8-master-20260828A-e4` | retained |
| E5 | `p8-master-20260828A-e5`; `p8-master-20260828A-e5-a01`; `p8-e5-20260829-000744`; `p8-e5-manual-20260829A` | setup attempts + valid-with-caveat manual run all retained |
| E6 | `p8-e6-manual-20260829A` | retained |
| E7 | `p8-e7-manual-20260829A` | standalone frozen archive retained |
| E8 | `p8-e8-manual-20260829A` | standalone frozen archive retained |
| E9 | `p8-e9-manual-20260829A` | control retained |
| E10-A | `p8-e10a-manual-20260829A` | retained censored observation |
| E10-B | `p8-e10b-manual-20260829A` | retained |
| E10-C | `p8-e10c-manual-20260829A`; `p8-e10c-manual-20260829B` | attempt A setup artifact + B valid-with-caveat retained |
| E10-D | `p8-e10d-manual-20260829A` | retained upper-bound observation |
| E11 | `p8-e11-r1-20260829A`; `p8-e11-r2-20260829A`; `p8-e11-r3-20260829A` | three nuc2-side replications retained with caveat |

## Archive and preservation inventory

| Artifact | SHA256 | Drive pointer / preservation route |
|---|---|---|
| Master P8 evidence | `6952565D8ED630496EB7A801DB90583F2FED2EFCDC81FEACD1A2072F18FA8878` | `1TYqlzrsYLWqmM0jEEmrFWS8_QUuLShiR` |
| E10/E11 frozen collector | `A6CEBA5107610639E62709F0041FB463CACBC45AA07847AFFE6600008B77C8F6` | `1ldR77IpSX5leGPQf-ISzl4qXCjHhiit0` |
| Private golden preservation | `520B9EAE154EAF2527BC61E19A08547712C11555BAFC29C2743D34930D5FADD8` | `1GL1cLSBjKU9v_pyOd5Sl7SDF_S6-xT7K` |
| E6 standalone frozen | `93AC4E0BE040B3A3FF7815BA7A43354C4F69971DF1468A0BD55C75DD97C01539` | nested/preserved in golden bundles; GitHub P8 index anchor |
| E7 standalone frozen | `886676778C667CB9B368456364972C91C4BF494DCC5FB1DA87D6EB14858DD22D` | nested in private golden preservation |
| E8 standalone frozen | `CA71214B12392C7349511B4400E288D59E6DE3A1507C043DB876E4642C227AFA` | nested in private golden preservation |
| E9 standalone frozen | `B89906139DD87EC2AF18CEF15072EFC065C8DA104C433F7FFAA431B41DCF0118` | nested in private golden preservation |
| Platform specs | `5537947B03373FB6869C3E154CCCECAC387FF12481D74634AFB192CA03F26E18` | `1PtIFgFvN1uBFttfub_NsfH00zKS9OPR4` |
| Final POWDER documentation, PRIVATE | `2B015A8FD4655F5615D570230C8989E54A4BD6EEB6E727D04D219B9013320C19` | `1aLuYZ7rJpkHExiX2ZyzZR1U3Y7gtYl6m` |
| Departure capture, PRIVATE | `7DBA8CE95CF06B254939C692915325E369FFA114080AE10BACA446D4BF62A66E` | `1ApIoF5CGphcvsFvMnuoizgZf1u_lQpZI`; prior raw Drive read-back PASS |
| Departure capture, SANITIZED | `236C6E269CDA6F7814B50415917D277CD7D0ED78D7D9DB0C3C4D1FE185EAE7A4` | `1lhiw_HR-rQ1e9yugKe7GxhCPfewBXDji`; prior raw Drive read-back PASS |
| Golden handover bundle | `F94951A42C2DF429297CEC888EA81D3DC374B6E47F34D71AA2F3BCE7898642B4` | `1DeRhsO5vrG1SH5w1uGXUuNy0Jiod7WgF`; prior raw Drive read-back PASS |

## GitHub-derived P9 artifacts

- `evidence/powder/WP2_P9_CANONICAL_EVIDENCE_CENSUS_2026-08-29.md`
- `evidence/powder/WP2_P9_CENSUS_E10_E11_SHA256_2026-08-29.csv`
- `evidence/powder/WP2_P9_RUN_VALIDITY_REGISTER_2026-08-29.md`
- `evidence/powder/WP2_P9_RECONSTRUCTED_METRIC_TABLES_2026-08-29.md`
- `evidence/powder/WP2_P9_CROSS_NODE_RECONCILIATION_2026-08-29.md`
- `evidence/powder/WP2_P9_ANOMALY_REGISTER_2026-08-29.md`
- `evidence/powder/WP2_P9_FORENSIC_TRACE_MAP_2026-08-29.md`
- `evidence/powder/WP2_P9_FORENSIC_QA_REPORT_2026-08-29.md`
- `analysis/powder/wp2_p9_reconstruct.py`

The departure archives were not needed to reconstruct packet/application metrics; their manifest exception is retained in the anomaly register.

`P9_A_EVIDENCE_CENSUS=PASS`
