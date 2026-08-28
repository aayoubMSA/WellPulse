# WP2-P9 — Reconstructed Metric Tables

Status: `P9-C=PASS`

All values below were recomputed from immutable raw files. Prior prose was not used as a numeric source.

## E0 clean baseline

- UE→CORE: 10 transmitted / 10 received / 0% loss.
- CORE→UE: 10 transmitted / 10 received / 0% loss.

## E1 primary fine-threshold run — `p8-e1r4-20260828A`

| dB | ICMP tx/rx/loss | MQTT sent/received/completeness |
|---:|---|---|
| 48 | 20/20/0% | 20/20/100% |
| 49 | 20/20/0% | 20/20/100% |
| 50 | 20/20/0% | 20/20/100% |
| 51 | 20/14/30% | 20/20/100% |
| 52 | 20/8/60% | 20/13/65% |

52 dB confirmation ping: 30/6/80% loss. Post-restore 0 dB ping: 20/20/0% loss.

## E2 hysteresis/recovery run — `p8-e2-20260828A`

| dB | ICMP tx/rx/loss | MQTT sent/received/completeness |
|---:|---|---|
| 52 | 20/7/65% | 20/11/55% |
| 51 | 20/18/10% | 20/20/100% |
| 50 | 20/20/0% | 20/20/100% |
| 49 | 20/20/0% | 20/20/100% |
| 48 | 20/20/0% | 20/20/100% |
| 46 | 20/20/0% | 20/20/100% |

The preserved 0 dB start and final-restore ping samples are both 20/20/0% loss.

## E3 three-cycle near-threshold repeatability

| cycle | dB | ICMP loss | MQTT sent/received/completeness |
|---:|---:|---:|---|
| 1 | 49 | 0% | 20/20/100% |
| 1 | 50 | 5% | 20/20/100% |
| 1 | 51 | 10% | 20/20/100% |
| 1 | 52 | 80% | 20/12/60% |
| 2 | 49 | 0% | 20/20/100% |
| 2 | 50 | 0% | 20/20/100% |
| 2 | 51 | 5% | 20/19/95% |
| 2 | 52 | 65% | 20/5/25% |
| 3 | 49 | 0% | 20/20/100% |
| 3 | 50 | 5% | 20/20/100% |
| 3 | 51 | 50% | 20/20/100% |
| 3 | 52 | 70% | 20/11/55% |

## E4–E9 reconstruction

| Exp | Phase | ICMP | MQTT sent/received | Notes |
|---|---|---|---|---|
| E4 | BASELINE | 20/20/0% | 20/20 | RF-only recovery reference |
| E4 | IMPAIRMENT | 20/1/95% | 20/0 | 55 dB |
| E4 | RECOVERY | 20/20/0% | 20/20 | RF restored only |
| E5 | BASELINE | not separately frozen | 20/20 | manual valid run |
| E5 | IMPAIRMENT | 20/0/100% | 20/0 | 55 dB |
| E5 | RECOVERY | forward ping artifact missing | 20/20 | reverse ping 20/20/0%; UE restart |
| E6 | BASELINE | 20/20/0% | 20/20 | CORE restart run |
| E6 | IMPAIRMENT | 20/0/100% | 20/0 | 55 dB |
| E6 | RECOVERY | 20/20/0% | 20/20 | reverse also 20/20/0% |
| E7 | BASELINE | 20/20/0% | 20/20 | combined stress |
| E7 | IMPAIRMENT | 20/1/95% | 20/0 | 55 dB |
| E7 | RECOVERY | 20/20/0% | 20/20 | reverse also 20/20/0% |
| E8 | BROKER_DOWN | 20/20/0% | 20/0 | LTE stayed healthy |
| E8 | RECOVERY | 10/10/0% | 40 send-log rows / 20 receiver rows | sender contains duplicate recovery attempt; 20 unique recovery IDs |
| E9 | NO_FAULT | 10/10/0% | 60/60 | 60 unique sent and 60 unique received; reverse 10/10/0% |

## E10 timing reconstruction

| Experiment | Endpoint | Reconstructed value | Raw basis |
|---|---|---:|---|
| E10-A | RF restore → end of preserved ping non-recovery window | 120.159434 s without recovery | UE `events.log` + 100 failed ping probes |
| E10-B | RF0+UE restart action begin → first ping success | 6.609430 s | UE events + ping timing |
| E10-B | RF0+UE restart action begin → receiver-side MQTT receipt | 6.123490 s | UE events + CORE receiver timing |
| E10-C(B) | RF restore action → first ping success | 29.247733 s | UE events + ping timing |
| E10-C(B) | RF restore action → first MQTT publish success | 29.248129 s | publish-side timing; later independent receiver verification exists |
| E10-D | broker-start command complete → first manually initiated successful MQTT publish | 10.872618 s | upper bound only; not exact broker recovery latency |

For E10-B, publish timestamp `22:30:50.547615427Z` was observed at CORE at `22:30:50.607787413Z`, i.e. 0.060172 s later.

## E11 UE-restart replications

| Run | impairment ICMP | recovery ICMP | UE source-IP transition |
|---|---|---|---|
| R1 | 10/0/100% | 20/20/0% | `172.16.0.2 → 172.16.0.3` |
| R2 | 10/0/100% | 20/20/0% | `172.16.0.3 → 172.16.0.4` |
| R3 | 10/0/100% | 20/20/0% | `172.16.0.4 → 172.16.0.6` |

No MQTT completeness or reverse-path metric is reported for E11 because the frozen E11 collector contains UE-side event/ping evidence but no independent nuc1/CORE run archive.

## Evidence chain

E0–E6 numeric sources are within `WellPulse-P8-Evidence-ALL-20260829-004254.zip` SHA256 `6952565D8ED630496EB7A801DB90583F2FED2EFCDC81FEACD1A2072F18FA8878`, Drive `1TYqlzrsYLWqmM0jEEmrFWS8_QUuLShiR`. E7–E9 standalone frozen archives are preserved inside the Drive-backed golden/private packages with their indexed SHA256s. E10–E11 numeric sources are within `WellPulse-P8-E10-E11-20260829-015817-FROZEN.zip` SHA256 `A6CEBA5107610639E62709F0041FB463CACBC45AA07847AFFE6600008B77C8F6`, Drive `1ldR77IpSX5leGPQf-ISzl4qXCjHhiit0`.

`P9_C_METRIC_RECONSTRUCTION=PASS`