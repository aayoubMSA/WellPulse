# WP2-P9 Claim-Independent Forensic QA Report — 2026-08-29

## Purpose

This is a claim-independent evidence audit. It does not draft manuscript language, choose a venue, generate figures, or integrate P8 into the WellPulse narrative.

## Required trace chain

Every surviving reconstructed value must follow:

`reported value → run/scope in reconstructed table → raw-file root in forensic trace map → frozen authority archive → SHA256 → Drive evidence`

## Authority verification

| Frozen authority used for reconstructed values | GitHub/receipt SHA256 | SHA256 recomputed from authenticated Drive download | Drive ID | Gate |
|---|---|---|---|---|
| Master P8 evidence | `6952565D8ED630496EB7A801DB90583F2FED2EFCDC81FEACD1A2072F18FA8878` | exact match | `1TYqlzrsYLWqmM0jEEmrFWS8_QUuLShiR` | PASS |
| E10/E11 collector | `A6CEBA5107610639E62709F0041FB463CACBC45AA07847AFFE6600008B77C8F6` | exact match | `1ldR77IpSX5leGPQf-ISzl4qXCjHhiit0` | PASS |
| Private golden preservation | `520B9EAE154EAF2527BC61E19A08547712C11555BAFC29C2743D34930D5FADD8` | exact match | `1GL1cLSBjKU9v_pyOd5Sl7SDF_S6-xT7K` | PASS |

For E7/E8/E9, the raw files reside inside standalone frozen run ZIPs preserved redundantly inside the Drive-authoritative private preservation bundle; the standalone hashes are preserved by its manifest, the P8 evidence index and the P9 trace map.

## Reconstruction QA

- ICMP tx/rx/loss and average RTT were parsed from raw ping summaries; no prose value was copied when a ping log existed.
- MQTT sent/received counts use unique sequence IDs and receiver-side reconciliation. Duplicate sender attempts are not counted as additional unique delivered observations.
- Timing endpoints use raw nanosecond timestamps and explicit action/result markers.
- E10-A yields no scalar recovery latency because recovery was not observed.
- E10-D remains an upper bound; exact broker recovery latency is not inferred.
- E5 forward recovery ping is absent from frozen evidence and therefore has no reconstructed forward-ping metric.
- E10-C-A contributes no scientific metric.
- E11 R1-R3 contribute only UE-side ICMP/IP-transition results because independent CORE collector evidence is absent.

## Census QA

The read-only member walk produced 598 immutable member records. Full hash enumeration remains inside the frozen archive-native manifests (`meta/SHA256_ALL_FILES.txt`, `meta/SHA256_ALL_COLLECTED.txt`, `SHA256_ALL.txt`, `PRESERVATION_MANIFEST.json`), while GitHub holds the canonical census/index, the E10/E11 member-level cross-check and raw-to-Drive trace map. This preserves the Drive-as-binary-authority policy without duplicating private/large raw bundles into ordinary Git history.

## Negative/failed evidence QA

Failed, NULL and setup evidence remains present in the census and validity register:
- E1 initial NULL prerequisite-violating treatment run;
- three E5 pre-treatment setup artifacts;
- E10-C attempt A setup artifact;
- E10-A censored non-recovery observation.

No failed or negative artifact was deleted.

## Cross-node QA

Receiver-side evidence governs end-to-end completeness. E1R4 seq 96 and E3 seq 150 are explicit sender/event-vs-receiver disagreements and remain in the anomaly register. E8 duplicate sends are reconciled using unique sequence IDs. E10-C-B duplicated later verification evidence is not double-counted.

## Mapping and hardware QA

No result requires an individual attenuator-ID→physical-path mapping. Runtime UHD identity remains unresolved and is not used to derive any metric.

## P7B boundary QA

`P8_CLASS=MANUAL_NON_SCORED_REFERENCE`

`SCORED_P7B_STATUS=UNCHANGED_NOT_PASSED`

No P9 output changes either classification.

## Unsupported-value gate

Every numeric result retained in the reconstructed metric/timing tables resolves through `WP2_P9_FORENSIC_TRACE_MAP_2026-08-29.md` to raw evidence and a Drive-verified frozen authority. Values blocked by absent evidence are represented as censored/missing/caveated rather than invented.

`P9_F_FORENSIC_QA=PASS`
