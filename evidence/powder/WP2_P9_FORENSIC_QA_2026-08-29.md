# WP2-P9 — Claim-Independent Forensic QA

Status: `P9-F=PASS`

## Gate

Every surviving result must satisfy:

`reported value → P9 derived artifact → raw file → frozen archive → SHA256 → Drive evidence`

No manuscript claim evaluation is performed here.

## Archive chain verification

| Evidence class | Frozen authority | SHA256 / Drive evidence | Result |
|---|---|---|---|
| E0–E6 | `WellPulse-P8-Evidence-ALL-20260829-004254.zip` | `6952565D8ED630496EB7A801DB90583F2FED2EFCDC81FEACD1A2072F18FA8878`; Drive `1TYqlzrsYLWqmM0jEEmrFWS8_QUuLShiR` | PASS |
| E7–E9 | standalone frozen E7/E8/E9 archives nested in golden/private preservation packages | E7 `88667677...22D`, E8 `CA71214B...7AFA`, E9 `B8990613...0118`; golden Drive `1DeRhsO5vrG1SH5w1uGXUuNy0Jiod7WgF`, private Drive `1GL1cLSBjKU9v_pyOd5Sl7SDF_S6-xT7K` | PASS |
| E10–E11 | `WellPulse-P8-E10-E11-20260829-015817-FROZEN.zip` | `A6CEBA5107610639E62709F0041FB463CACBC45AA07847AFFE6600008B77C8F6`; Drive `1ldR77IpSX5leGPQf-ISzl4qXCjHhiit0` | PASS |
| Departure evidence | PRIVATE + SANITIZED frozen archives | Drive read-back SHA256 PASS per preservation receipt | PASS_WITH_DOCUMENTED_POST_MANIFEST_APPEND |
| Context screenshots | private golden-preservation archive | private archive SHA256 `520B9EAE154EAF2527BC61E19A08547712C11555BAFC29C2743D34930D5FADD8`; Drive `1GL1cLSBjKU9v_pyOd5Sl7SDF_S6-xT7K` | PASS; not used for metrics |

The current Drive preservation receipt and GitHub evidence index agree on all primary bundle hashes used by P9. No unresolved archive/hash discrepancy was found.

## Metric trace audit

| Metric family | Derived artifact | Raw basis | Result |
|---|---|---|---|
| E0 ICMP | `WP2_P9_RECONSTRUCTED_METRICS_2026-08-29.md` | clean forward/reverse ping logs | PASS |
| E1 threshold | same | E1r4 UE ping + sent logs; CORE receiver log | PASS |
| E2 hysteresis | same | E2 UE ping/events/sent + CORE receiver | PASS |
| E3 repeatability | same | E3 cycle ping/events/sent + CORE receiver | PASS |
| E4–E7 recovery | same | per-run UE events/ping/sent + CORE receiver/reverse/event evidence where present | PASS; E5 forward recovery ping excluded |
| E8 broker control | same | CORE broker events/receiver/reverse ping + UE sent/events/pings | PASS_WITH_DUPLICATE_SEND_CAVEAT |
| E9 no-fault control | same | UE sent/ping/events + CORE receiver/reverse ping | PASS |
| E10 timing | same | per-node action/timing logs | PASS_WITH_ENDPOINT_CAVEATS |
| E11 replication | same | UE events + impairment/recovery ping logs | PASS_WITH_ONE_SIDED_SCOPE |

## Adversarial second pass

1. Prior prose values were not used as computation inputs when raw evidence was available.
2. Receiver-side unique sequence reconciliation governs end-to-end MQTT completeness.
3. E1 initial run remains `NULL`; its failed prerequisite is not hidden by later successful runs.
4. E5 pre-treatment/controller failures remain `SETUP_ARTIFACT` and are not merged into the valid manual run.
5. E5 forward recovery-ping value is not reconstructed because the artifact is missing.
6. E8 duplicate recovery send is retained; 80 physical send rows are not misreported as 80 unique records.
7. E10-A remains a censored no-recovery observation; no exact recovery latency is invented.
8. E10-C attempt A is excluded; attempt B remains the valid timing run.
9. E10-D endpoints are typed explicitly: 10.908749 s from broker-start action begin and 10.872618 s from command-complete to first manually initiated successful probe. Both are upper bounds only.
10. E11 lacks independent CORE archives; reverse-path and MQTT metrics are therefore omitted.
11. The unresolved attenuator-ID→physical-path mapping is not inferred.
12. Runtime UHD identity is not inferred from profile/RSpec evidence.
13. 89 unclassified screenshots are retained as contextual evidence but not attributed to runs or used numerically.
14. P8 remains `MANUAL_NON_SCORED_REFERENCE`; no P8 result is promoted to scored P7B.

## Cross-artifact consistency

- Canonical census: PASS.
- Validity register: PASS after inclusion of all discovered E5 pre-manual/setup attempts.
- Reconstructed metrics: PASS.
- Cross-node reconciliation: PASS with explicitly preserved disagreements.
- Anomaly register: PASS.
- Drive/GitHub authority alignment: PASS.

`UNSUPPORTED_SURVIVING_VALUES=0`

`UNRESOLVED_ARCHIVE_HASH_DISCREPANCIES=0`

`P9_FORENSIC_QA=PASS`