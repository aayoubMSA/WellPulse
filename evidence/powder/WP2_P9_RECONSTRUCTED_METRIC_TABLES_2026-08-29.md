# WP2-P9 Reconstructed Metric Tables — 2026-08-29

## Reconstruction rule

All values in this file were recomputed from immutable raw files. Prior prose values were not used when the raw file allowed reconstruction.

Machine-readable metric and timing tables are represented by the trace rows in the forensic QA package; every surviving value carries a raw-file and frozen-authority pointer.

## MQTT sequence completeness

| Experiment/run | Unique sent | Unique received | Completeness | Forensic note |
|---|---:|---:|---:|---|
| E1R2 | 65 | 65 | 100.000% | valid refinement |
| E1R3 | 100 | 100 | 100.000% | valid partial refinement |
| E1R4 main sweep | 100 | 93 | 93.000% | missing 82,84,90,91,92,96,97; recovery records excluded from main sweep |
| E2 | 160 | 151 | 94.375% | missing 22,23,24,29,33,36,38,39,40, all in 52 dB segment |
| E3 | 255 | 222 | 87.0588% | receiver-side unique reconciliation |
| E4 | 60 | 40 | 66.6667% | missing 21–40 during impairment; baseline and recovery complete |
| E5 manual | 60 | 40 | 66.6667% | missing 21–40 during impairment; baseline and recovery complete |
| E6 | 60 | 40 | 66.6667% | missing 21–40 during impairment; baseline and recovery complete |
| E7 | 60 | 40 | 66.6667% | missing 21–40 during impairment; baseline and recovery complete |
| E8 | 60 unique | 40 unique | 66.6667% | sent.log has 80 lines due duplicate 41–60 recovery attempt; unique IDs govern |
| E9 control | 60 | 60 | 100.000% | no-fault control |

Receiver-side unique sequence reconciliation governs completeness. Sender-side failure/event flags are diagnostic only.

## E10 recovery timing

| Experiment | Action | Action timestamp | Observed endpoint | Derived interval |
|---|---|---|---|---|
| E10-A | RF restore | 2026-08-28T22:22:45.102014350Z | no ping recovery in 100 attempts through 22:24:45.261448500Z; no MQTT recovery in 100 attempts through 22:26:46.487773643Z | censored; no exact value |
| E10-B | RF0 + srsUE restart action begin | 2026-08-28T22:30:44.484297427Z | FIRST_MQTT_PUBLISH_SUCCESS 22:30:50.547615427Z | 6.063318 s |
| E10-B | same | 2026-08-28T22:30:44.484297427Z | FIRST_PING_SUCCESS 22:30:51.093727341Z | 6.609430 s |
| E10-B | MQTT publish success | 2026-08-28T22:30:50.547615427Z | CORE receipt 22:30:50.607787413Z | 0.060172 s publish→receive |
| E10-C-B | RF restore action | 2026-08-28T22:34:56.276421190Z | FIRST_PING_SUCCESS 22:35:25.524153797Z | 29.247733 s |
| E10-C-B | RF restore action | 2026-08-28T22:34:56.276421190Z | FIRST_MQTT_PUBLISH_SUCCESS 22:35:25.524550136Z | 29.248129 s |
| E10-D | broker start action begin | 2026-08-28T22:40:25.508181979Z | first manually initiated MQTT publish success 22:40:36.416931071Z | <=10.908749 s upper bound only |

Timing semantics are intentionally narrow: E10-A has no scalar latency; E10-C primary application timing is publish-side; E10-D is not exact broker-recovery latency.

## Scientifically relevant UE IP transitions

| Run | Before | After | Evidence role |
|---|---|---|---|
| E5 manual | `172.16.0.3` observed during impairment/monitoring | `172.16.0.4` reverse-recovery target after UE restart | cross-node recovery context |
| E11-R1 | `172.16.0.2` | `172.16.0.3` | UE-side replication |
| E11-R2 | `172.16.0.3` | `172.16.0.4` | UE-side replication |
| E11-R3 | `172.16.0.4` | `172.16.0.6` | UE-side replication |

These transitions are reported only where directly evidenced; no unseen path/attenuator mapping is inferred.

## ICMP reconstruction

### E0 clean control

- UE→CORE: 10 transmitted / 10 received / 0% loss / average RTT 16.003 ms.
- CORE→UE: 10 / 10 / 0% / 16.865 ms.

### E1R4 fine boundary

- 48 dB: 20/20, 0% loss, avg 32.274 ms.
- 49 dB: 20/20, 0%, avg 36.963 ms.
- 50 dB: 20/20, 0%, avg 34.452 ms.
- 51 dB: 20/14, 30%, avg 51.171 ms.
- 52 dB: 20/8, 60%, avg 66.578 ms.

### E2 downward recovery sweep

- 52 dB: 20/7, 65%, avg 59.909 ms.
- 51 dB: 20/18, 10%, avg 41.312 ms.
- 50 dB: 20/20, 0%, avg 40.341 ms.
- 49 dB: 20/20, 0%, avg 31.318 ms.
- 48 dB: 20/20, 0%, avg 34.717 ms.
- 46 dB: 20/20, 0%, avg 36.158 ms.
- initial 0 dB: 20/20, 0%, avg 22.803 ms; final 0 dB: 20/20, 0%, avg 24.900 ms.

### E3 near-threshold repeatability

Ping loss by cycle:

| Cycle | 49 dB | 50 dB | 51 dB | 52 dB |
|---|---:|---:|---:|---:|
| 1 | 0% | 5% | 10% | 80% |
| 2 | 0% | 0% | 5% | 65% |
| 3 | 0% | 5% | 50% | 70% |

### Recovery/control runs

- E4: baseline 20/20, 0%, avg 24.239 ms; impairment 20/1, 95%, avg 74.666 ms; recovery 20/20, 0%, avg 26.083 ms.
- E5: frozen UE impairment 20/0, 100%; frozen CORE reverse recovery 20/20, 0%, avg 26.274 ms. Forward UE recovery ping is not frozen and is not reconstructed.
- E6: UE baseline 20/20, impairment 20/0, recovery 20/20; CORE reverse baseline/recovery 20/20.
- E7: UE baseline 20/20, impairment 20/1 (95%), recovery 20/20; CORE reverse baseline/recovery 20/20. A reverse-baseline RTT maximum of 481.046 ms is preserved as an outlier.
- E8: while broker was down, UE and CORE reverse pings were each 20/20 with 0% loss; after broker restore UE ping 10/10, 0%.
- E9 control: both directions 10/10, 0%.
- E11 R1/R2/R3: impairment 10/0 in each run; recovery 20/20 in each run; recovery average RTTs 19.490, 22.042 and 22.359 ms respectively. These are UE-side only.

## Treatment/action timestamps preserved for reconciliation

- E4: RF 55 dB at 20:36:24.136; RF 0 dB at 20:39:01.402; declared RF_RESTORE_ONLY action at 20:39:04.490.
- E5: RF 55 dB at 21:12:09; RF 0 dB at 21:15:22.167; SRSUE_RESTART at 21:15:22.170.
- E6: CORE restart begin 21:33:21.904; restart commands complete 21:33:23.780; RF 55 dB at 21:30:07.320; RF 0 dB at 21:34:04.436.
- E7: CORE restart begin 21:57:01.440; RF 55 dB at 21:54:47.022; RF 0 dB + UE restart at 21:57:52.916/21:57:52.920.
- E8: broker stop 22:06:10.709; broker start 22:08:28.601.
- E9: no-fault interval start 22:14:46.436; complete 22:15:44.023.

## Acceptance

`P9_C_METRIC_RECONSTRUCTION=PASS`
