# WP2-P9 Forensic Trace Map — 2026-08-29

## Trace rule

Every reconstructed metric in `WP2_P9_RECONSTRUCTED_METRIC_TABLES_2026-08-29.md` is keyed by experiment/run and source filename/scope. Resolve it using this map:

`reported value → run + source scope → raw root below → frozen authority → SHA256 → Drive ID`

## Master P8 authority

Authority: `WellPulse-P8-Evidence-ALL-20260829-004254.zip`  
SHA256: `6952565D8ED630496EB7A801DB90583F2FED2EFCDC81FEACD1A2072F18FA8878`  
Drive ID: `1TYqlzrsYLWqmM0jEEmrFWS8_QUuLShiR`

| Run | CORE raw root | UE raw root / relevant source |
|---|---|---|
| `p8-e0-clean-20260828` | `remote/p8-e0-clean-20260828/nuc1/CORE/` | `remote/p8-e0-clean-20260828/nuc2/UE/` |
| `p8-e1-20260828T1707Z` | `remote/p8-e1-20260828T1707Z/nuc1/CORE/` | `remote/p8-e1-20260828T1707Z/nuc2/UE/` |
| `p8-e1r2-20260828A` | `remote/p8-e1r2-20260828A/nuc1/CORE/` | `remote/p8-e1r2-20260828A/nuc2/UE/` |
| `p8-e1r3-20260828A` | `remote/p8-e1r3-20260828A/nuc1/CORE/` | `remote/p8-e1r3-20260828A/nuc2/UE/` |
| `p8-e1r4-20260828A` | `remote/p8-e1r4-20260828A/nuc1/CORE/` | `remote/p8-e1r4-20260828A/nuc2/UE/` |
| `p8-e2-20260828A` | `remote/p8-e2-20260828A/nuc1/CORE/` | `remote/p8-e2-20260828A/nuc2/UE/` |
| `p8-e3-20260828A` | `remote/p8-e3-20260828A/nuc1/CORE/` | `remote/p8-e3-20260828A/nuc2/UE/` |
| `p8-master-20260828A-e4` | `remote/p8-master-20260828A-e4/nuc1/CORE/` | `remote/p8-master-20260828A-e4/nuc2/UE/` |
| `p8-e5-manual-20260829A` | nested frozen E5 archive under `local/` | nested frozen E5 archive under `local/` |
| `p8-e6-manual-20260829A` | nested frozen E6 archive under `local/` | nested frozen E6 archive under `local/` |

For MQTT completeness, the source pair is `UE/sent.log` + `CORE/received.log`. For ICMP, the filename stated in the metric table is appended to the applicable node root. Treatment/action timestamps are in the run event/timing logs under the same roots.

## E7/E8/E9 private-preservation authority

Authority: `WellPulse_POWDER_Golden_Preservation_PRIVATE_2026-08-29.zip`  
SHA256: `520B9EAE154EAF2527BC61E19A08547712C11555BAFC29C2743D34930D5FADD8`  
Drive ID: `1GL1cLSBjKU9v_pyOd5Sl7SDF_S6-xT7K`

The following standalone frozen archives are members of the authority bundle and are preserved redundantly in its handover package:

| Run | Nested frozen archive | Standalone SHA256 | Raw roots inside nested archive |
|---|---|---|---|
| E7 `p8-e7-manual-20260829A` | `artifacts/WellPulse-p8-e7-manual-20260829A-FROZEN.zip` | `886676778C667CB9B368456364972C91C4BF494DCC5FB1DA87D6EB14858DD22D` | `raw/CORE/`, `raw/UE/` |
| E8 `p8-e8-manual-20260829A` | `artifacts/WellPulse-p8-e8-manual-20260829A-FROZEN.zip` | `CA71214B12392C7349511B4400E288D59E6DE3A1507C043DB876E4642C227AFA` | `raw/CORE/`, `raw/UE/` |
| E9 `p8-e9-manual-20260829A` | `artifacts/WellPulse-p8-e9-manual-20260829A-FROZEN.zip` | `B89906139DD87EC2AF18CEF15072EFC065C8DA104C433F7FFAA431B41DCF0118` | `raw/CORE/`, `raw/UE/` |

E8 completeness specifically resolves `raw/UE/sent.log` against `raw/CORE/received.log`; the duplicate recovery send remains visible in the sender file.

## E10/E11 authority

Authority: `WellPulse-P8-E10-E11-20260829-015817-FROZEN.zip`  
SHA256: `A6CEBA5107610639E62709F0041FB463CACBC45AA07847AFFE6600008B77C8F6`  
Drive ID: `1ldR77IpSX5leGPQf-ISzl4qXCjHhiit0`

| Run | Raw root | Trace limitation |
|---|---|---|
| `p8-e10a-manual-20260829A` | `raw/p8-e10a-manual-20260829A/` | censored no-recovery observation |
| `p8-e10b-manual-20260829A` | `raw/p8-e10b-manual-20260829A/` | action/ping/publish/CORE receipt available |
| `p8-e10c-manual-20260829A` | `raw/p8-e10c-manual-20260829A/` | setup artifact only |
| `p8-e10c-manual-20260829B` | `raw/p8-e10c-manual-20260829B/` | valid B timing; later CORE verification duplicated |
| `p8-e10d-manual-20260829A` | `raw/p8-e10d-manual-20260829A/` | upper-bound endpoint only |
| `p8-e11-r1-20260829A` | `raw/p8-e11-r1-20260829A/nuc2/p8-e11-r1-20260829A/UE/` | nuc2-only |
| `p8-e11-r2-20260829A` | `raw/p8-e11-r2-20260829A/nuc2/p8-e11-r2-20260829A/UE/` | nuc2-only |
| `p8-e11-r3-20260829A` | `raw/p8-e11-r3-20260829A/nuc2/p8-e11-r3-20260829A/UE/` | nuc2-only |

## Full artifact enumeration

The canonical census records **598** immutable members with per-entry SHA256. The census covers logs, screenshots, manifests/receipts and archived artifacts; raw binaries remain in Drive and are not committed to ordinary Git history.

`P9_FORENSIC_TRACE_MAP=PASS`
