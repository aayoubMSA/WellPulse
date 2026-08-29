# WP2-P9 Canonical Evidence Census — 2026-08-29

## Scope and boundary

This census belongs only to `WP2-P9 — GOLDEN EVIDENCE FORENSIC RECONCILIATION`.

`P8_CLASS=MANUAL_NON_SCORED_REFERENCE`

`SCORED_P7B_STATUS=UNCHANGED_NOT_PASSED`

No P8 item is promoted or re-labelled as scored P7B evidence.

## Frozen Drive authorities used for forensic reconstruction

| Authority archive | SHA256 | Drive ID | P9 authenticated download/hash |
|---|---|---|---|
| `WellPulse-P8-Evidence-ALL-20260829-004254.zip` | `6952565D8ED630496EB7A801DB90583F2FED2EFCDC81FEACD1A2072F18FA8878` | `1TYqlzrsYLWqmM0jEEmrFWS8_QUuLShiR` | PASS |
| `WellPulse-P8-E10-E11-20260829-015817-FROZEN.zip` | `A6CEBA5107610639E62709F0041FB463CACBC45AA07847AFFE6600008B77C8F6` | `1ldR77IpSX5leGPQf-ISzl4qXCjHhiit0` | PASS |
| `WellPulse_POWDER_Golden_Preservation_PRIVATE_2026-08-29.zip` | `520B9EAE154EAF2527BC61E19A08547712C11555BAFC29C2743D34930D5FADD8` | `1GL1cLSBjKU9v_pyOd5Sl7SDF_S6-xT7K` | PASS |

The three SHA256 values above were recomputed from authenticated Drive downloads during P9 and match the P8 GitHub/Drive anchors.

## Canonical member inventory

A read-only ZIP central-directory census across the three verified authorities enumerates **598 immutable file members**:

- master P8 archive: **357** file members;
- E10/E11 collector: **46** file members;
- private golden-preservation archive: **195** file members.

By extension these are: 262 `.log`, 173 `.txt`, 89 `.png`, 28 `.ps1`, 19 `.zip`, 12 `.sh`, 6 `.tgz`, 4 `.json`, 2 `.md`, 2 `.csv`, and 1 `.pid`.

Full path/hash enumeration remains inside the immutable archive-native manifests:

- master: `meta/SHA256_ALL_FILES.txt` + `meta/FILE_INVENTORY.csv`;
- E10/E11: `meta/SHA256_ALL_COLLECTED.txt` + `meta/RUN_STATUS.csv` + node-local SHA256 manifests;
- private preservation: `SHA256_ALL.txt` + `PRESERVATION_MANIFEST.json`.

The private `SHA256_ALL.txt` enumerates all **89** `screenshots_unclassified/*.png` files by filename and individual SHA256. Their UUID names do not support defensible run attribution, so they are preserved but not used for metric reconstruction.

## Run / attempt inventory

| Slot | Enumerated identities | Disposition source |
|---|---|---|
| E0 | `p8-e0-20260828T173715Z`; `p8-e0-clean-20260828` | validity register |
| E1 | `p8-e1-20260828T1707Z`; `p8-e1r2-20260828A`; `p8-e1r3-20260828A`; `p8-e1r4-20260828A` | validity register |
| E2 | `p8-e2-20260828A` | validity register |
| E3 | `p8-e3-20260828A` | validity register |
| E4 | `p8-master-20260828A-e4` | validity register |
| E5 | `p8-master-20260828A-e5`; `p8-master-20260828A-e5-a01`; `p8-e5-20260829-000402`; `p8-e5-20260829-000744`; `p8-e5-manual-20260829A` | four setup/pre-science attempts/fragments plus the valid-with-caveat manual run |
| E6 | `p8-e6-manual-20260829A` | validity register |
| E7 | `p8-e7-manual-20260829A` | validity register |
| E8 | `p8-e8-manual-20260829A` | validity register |
| E9 | `p8-e9-manual-20260829A` | validity register |
| E10-A | `p8-e10a-manual-20260829A` | validity register |
| E10-B | `p8-e10b-manual-20260829A` | validity register |
| E10-C | `p8-e10c-manual-20260829A`; `p8-e10c-manual-20260829B` | A setup artifact; B valid-with-caveat |
| E10-D | `p8-e10d-manual-20260829A` | validity register |
| E11 | `p8-e11-r1-20260829A`; `p8-e11-r2-20260829A`; `p8-e11-r3-20260829A` | UE-side-only valid-with-caveat replications |

No failed, NULL, aborted, or setup evidence is removed by this census.

## Standalone frozen run anchors

| Artifact | SHA256 | Durable route |
|---|---|---|
| E6 frozen | `93AC4E0BE040B3A3FF7815BA7A43354C4F69971DF1468A0BD55C75DD97C01539` | preserved in golden packages / P8 index |
| E7 frozen | `886676778C667CB9B368456364972C91C4BF494DCC5FB1DA87D6EB14858DD22D` | nested in private golden preservation |
| E8 frozen | `CA71214B12392C7349511B4400E288D59E6DE3A1507C043DB876E4642C227AFA` | nested in private golden preservation |
| E9 frozen | `B89906139DD87EC2AF18CEF15072EFC065C8DA104C433F7FFAA431B41DCF0118` | nested in private golden preservation |

## Additional durable Drive anchors

| Artifact | SHA256 | Drive ID |
|---|---|---|
| Golden handover bundle | `F94951A42C2DF429297CEC888EA81D3DC374B6E47F34D71AA2F3BCE7898642B4` | `1DeRhsO5vrG1SH5w1uGXUuNy0Jiod7WgF` |
| Platform specs | `5537947B03373FB6869C3E154CCCECAC387FF12481D74634AFB192CA03F26E18` | `1PtIFgFvN1uBFttfub_NsfH00zKS9OPR4` |
| Final documentation, PRIVATE | `2B015A8FD4655F5615D570230C8989E54A4BD6EEB6E727D04D219B9013320C19` | `1aLuYZ7rJpkHExiX2ZyzZR1U3Y7gtYl6m` |
| Departure PRIVATE | `7DBA8CE95CF06B254939C692915325E369FFA114080AE10BACA446D4BF62A66E` | `1ApIoF5CGphcvsFvMnuoizgZf1u_lQpZI` |
| Departure SANITIZED | `236C6E269CDA6F7814B50415917D277CD7D0ED78D7D9DB0C3C4D1FE185EAE7A4` | `1lhiw_HR-rQ1e9yugKe7GxhCPfewBXDji` |

Departure raw Drive read-back/hash verification was already PASS. The `CAPTURE_STATUS.txt` post-manifest append exception remains documented rather than treated as corruption.

## Canonical GitHub P9 outputs

- `evidence/powder/WP2_P9_CANONICAL_EVIDENCE_CENSUS_2026-08-29.md`
- `evidence/powder/WP2_P9_RUN_VALIDITY_REGISTER_2026-08-29.md`
- `evidence/powder/WP2_P9_RECONSTRUCTED_METRIC_TABLES_2026-08-29.md`
- `evidence/powder/WP2_P9_CROSS_NODE_RECONCILIATION_2026-08-29.md`
- `evidence/powder/WP2_P9_ANOMALY_REGISTER_2026-08-29.md`
- `evidence/powder/WP2_P9_FORENSIC_TRACE_MAP_2026-08-29.md`
- `evidence/powder/WP2_P9_FORENSIC_QA_REPORT_2026-08-29.md`
- `analysis/powder/wp2_p9_reconstruct.py`
- `HANDOVER_CURRENT.md` after P9 closure.

No raw archive was modified.

`P9_A_EVIDENCE_CENSUS=PASS`
