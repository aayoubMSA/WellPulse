# WP2-P9 Canonical Evidence Census — 2026-08-29

## Scope and boundary

This census belongs only to `WP2-P9 — GOLDEN EVIDENCE FORENSIC RECONCILIATION`.

`P8_CLASS=MANUAL_NON_SCORED_REFERENCE`

`SCORED_P7B_STATUS=UNCHANGED_NOT_PASSED`

No P8 item is promoted or re-labelled as scored P7B evidence.

## Frozen Drive authorities used for forensic reconstruction

| Authority archive | SHA256 | Drive ID | Local read-back |
|---|---|---|---|
| `WellPulse-P8-Evidence-ALL-20260829-004254.zip` | `6952565D8ED630496EB7A801DB90583F2FED2EFCDC81FEACD1A2072F18FA8878` | `1TYqlzrsYLWqmM0jEEmrFWS8_QUuLShiR` | PASS |
| `WellPulse-P8-E10-E11-20260829-015817-FROZEN.zip` | `A6CEBA5107610639E62709F0041FB463CACBC45AA07847AFFE6600008B77C8F6` | `1ldR77IpSX5leGPQf-ISzl4qXCjHhiit0` | PASS |
| `WellPulse_POWDER_Golden_Preservation_PRIVATE_2026-08-29.zip` | `520B9EAE154EAF2527BC61E19A08547712C11555BAFC29C2743D34930D5FADD8` | `1GL1cLSBjKU9v_pyOd5Sl7SDF_S6-xT7K` | PASS |

The SHA256 values above were recomputed from authenticated Drive downloads during P9 and matched the GitHub/Drive preservation anchors.

## Census result

- Unique enumerated members across the three verified authorities: **598**
- Logs: **370**
- Screenshots: **89**
- Manifests / receipts: **67**
- Other archived artifacts: **72**
- Full member-level census: `evidence/powder/WP2_P9_CANONICAL_EVIDENCE_CENSUS_2026-08-29.csv`

The census includes authority archive, authority SHA256, Drive ID, inferred run ID, artifact category, internal path, byte size, per-entry SHA256 and GitHub anchor.

## Additional preserved Drive anchors

| Artifact | SHA256 | Drive ID |
|---|---|---|
| Golden handover bundle | `F94951A42C2DF429297CEC888EA81D3DC374B6E47F34D71AA2F3BCE7898642B4` | `1DeRhsO5vrG1SH5w1uGXUuNy0Jiod7WgF` |
| Platform specs | `5537947B03373FB6869C3E154CCCECAC387FF12481D74634AFB192CA03F26E18` | `1PtIFgFvN1uBFttfub_NsfH00zKS9OPR4` |
| Final POWDER documentation, PRIVATE | `2B015A8FD4655F5615D570230C8989E54A4BD6EEB6E727D04D219B9013320C19` | `1aLuYZ7rJpkHExiX2ZyzZR1U3Y7gtYl6m` |
| Departure capture, PRIVATE | `7DBA8CE95CF06B254939C692915325E369FFA114080AE10BACA446D4BF62A66E` | `1ApIoF5CGphcvsFvMnuoizgZf1u_lQpZI` |
| Departure capture, SANITIZED | `236C6E269CDA6F7814B50415917D277CD7D0ED78D7D9DB0C3C4D1FE185EAE7A4` | `1lhiw_HR-rQ1e9yugKe7GxhCPfewBXDji` |

The departure archives were already independently Drive-read-back/hash verified in the P8 preservation receipt and were not needed to reconstruct packet/application metrics.

## Run coverage

The immutable evidence set contains E0 through E11, including multiple threshold-refinement runs, pre-treatment setup attempts, E10-C attempt A/B separation, and three E11 replications. Failed and setup artifacts remain enumerated; none were deleted or normalized away.

## Acceptance

`P9_A_EVIDENCE_CENSUS=PASS`
