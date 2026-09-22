# WellPulse Revival — Sanitized Reproducibility Supplement

Date: 2026-09-22
Status: R7f-R3 sanitized reviewer-facing supplement
Scope: execution configuration, code authority, clock procedure, and evidence-preservation map.
Raw private archives, credentials, FIT account details, SSH keys, and private Drive identifiers are excluded.

## 1. Scientific reproduction boundary

This supplement supports the manuscript's bounded communications/recovery claims only. It does not create a new experiment, regenerate missing measurements, or expose private testbed credentials.

The scientific unit is the run. Record identities are used for deterministic reconciliation and are not independent statistical replicates.

## 2. Historical FIT final campaign

Authority:
- GitHub Actions run: 32628193889
- executed checkout: e257d22e1e6589b3e28ca2f2c14d3fab2ba2e483
- FIT experiments: 448265, 448266, 448269
- site: Grenoble
- hardware recorded by final status: A8-100
- matrix: B0/W1 × C0/C1/C2 × 3 replicates
- records per cell: 10,000

Software / transport:
- source runner: experiments/WP-RT01/fit_runner_py35.py
- executed Git blob: 3683737f9756c8b96c4c2e41f4372fc388fadb7d
- A8 execution code is Python-3.5-compatible; capability evidence records Python 3.5.1
- paho-mqtt bundle: 1.6.1
- broker endpoint: mqtt4.iot-lab.info:8883
- MQTT QoS: 1
- TLS: peer verification enabled; TLS 1.2 requested by the source runner
- trust anchor used after compatibility qualification: ISRG Root X1, fingerprint
  96BCEC06264976F37460779ACF28C5A7CFE8A3C0AAE11A8FFCEE05C0BDDF08C6
- receiver capture: FIT frontend mosquitto_sub, QoS 1
- receiver mosquitto_sub version: not recorded in the preserved final metadata and is therefore not invented here

Treatments:
- C0: normal connectivity, no restart
- C1: Linux iptables OUTPUT REJECT to runtime-resolved broker IPv4 TCP/8883 during records 3001–5000
- C2: same broker-specific transport block plus WellPulse gateway-process exec restart after record 4000
- C2 is not a whole-node reboot

W1 persistence:
- SQLite queue with per-record enqueue and persisted record identity
- executed source calls PRAGMA journal_mode=WAL
- executed source calls PRAGMA synchronous=FULL
- pending rows are replayed serially after transport restoration

### Provenance discrepancy — preserved, not normalized

AMENDMENT_002_PREFINAL_CORRECTIONS.md states that the intended FIT adapter should use PRAGMA journal_mode=DELETE because the preserved work path was considered NFS. The actual frozen runner blob executed by the final campaign, however, contains PRAGMA journal_mode=WAL.

For reproduction, executed code authority takes precedence: the exact runner blob above is the source of truth for what ran. The manuscript does not attribute any result to SQLite journal-mode choice, and no comparison between WAL and DELETE is claimed.

## 3. Prospective FIT Stage-A campaign

Authority:
- GitHub Actions run: 35653569079
- FIT experiment: 449953
- node: Grenoble A8-102
- frozen authority: c9fd8968f1408d9a2e3a57dd825df05c2f1d9147
- scored runs: exactly R1, R2, R3
- records per run: 10,000
- treatment: W1/C1 only, no process restart
- H: sequences 3001–5000, exactly 2,000 records
- live witness: sequence 5001

Qualified code authorities:
- frozen runner blob:
  3683737f9756c8b96c4c2e41f4372fc388fadb7d
- instrumentation wrapper blob:
  9a0585ecacc9bdb87ec469d9ea1ad9ce998ccc9e
- receiver timestamp stream blob:
  51a31081990c4d92e99462f7c6cd88736260036e
- Stage-A loop blob:
  74bd757f02fe16fb9b91809863641300d99527e3
- per-run adjudicator blob:
  860372c2ebfe4830c2cdd10da4b89b4fec6d7647
- aggregate adjudicator blob:
  1df21625b788b5c19db17a779da03fa08be5a2b2

Runtime/bootstrap:
- controller Python in the successful Actions run: 3.12.14
- paho-mqtt bundle staged for A8: 1.6.1
- broker endpoint: mqtt4.iot-lab.info:8883
- source outage mechanism: same iptables OUTPUT REJECT broker TCP/8883 treatment as C1
- source wrapper preserves the frozen runner's main(), queue flow, payload bytes, outage sequencing, and inherited publish wait behavior; instrumentation is sidecar-only

Receiver:
- FIT frontend mosquitto_sub, QoS 1
- each received line is stamped with receiver time.time() by scripts/fit_rt01_stamp_stream.py
- exact mosquitto_sub version was not captured in the scored metadata and is not inferred

## 4. Prospective clock-bound procedure

For every scored run, one pre-run and one post-run clock sample were collected.

Receiver-clock sampling:
- 9 direct SSH samples
- controller records t0 and t1
- remote receiver reports time.time()
- offset estimate = remote - midpoint(t0,t1)
- uncertainty bound = RTT/2
- best sample = minimum RTT sample

Source-clock sampling:
- 9 samples through iotlab-ssh run-cmd on the A8
- A8 writes time.time() into the shared evidence path
- frontend reads the value
- controller again records t0/t1
- offset estimate and RTT/2 bound use the same midpoint rule
- best sample = minimum RTT sample

Adjudication:
- pre/post best-sample offset intervals are hulled per host
- receiver-minus-source relative offset interval is formed conservatively
- D23=M3−M2 is clock-positive only if its entire conservative interval is above zero
- if the interval crosses zero, the result is UNRESOLVED
- an independent same-receiver causal witness can establish M3>M2 without cross-host subtraction when seq5001 arrives before a still-missing member of H
- no scored Stage-A run produced that causal witness

The qualification ceiling of 5 s was a clock-usability gate, not a scientific effect threshold.

## 5. Public/sanitized code surface

The repository contains the code required to inspect or rerun the bounded FIT logic without publishing credentials:

- experiments/WP-RT01/fit_runner_py35.py
- experiments/WP-RT01/fit_runner_q0_instrumented_py35.py
- scripts/fit_rt01_stamp_stream.py
- scripts/run_fit_r5_stage_a_loop.sh
- scripts/analyze_r5_stage_a_run.py
- scripts/adjudicate_r5_stage_a.py
- tests/test_r5_stage_a.py
- experiments/WP-RT01/EXPERIMENT_CONTRACT.md
- experiments/WP-RT01/AMENDMENT_001_FIT_EXECUTION.md
- experiments/WP-RT01/AMENDMENT_002_PREFINAL_CORRECTIONS.md
- experiments/WP-RT01/FINAL_RESULTS_2026-08-23.md
- experiments/WP-RT01/Q0_REVIVAL_STATUS.md
- experiments/WP-RT01/R5_STAGE_A_STATUS.md
- experiments/WP-RT01/R5_RAW_EVIDENCE_PRESERVATION.md

This supplement intentionally omits:
- FIT usernames/passwords
- SSH private keys
- temporary authentication files
- private Drive identifiers
- private raw archives
- unclassified screenshots or captures

## 6. Preserved evidence authority

Historical FIT raw archives remain frozen in their durable preservation locations.

Prospective scored Stage-A raw authority:
SHA-256:
5b52005e48d8987091c447186eb39261824f32df15653c3d2773a031b062d4a2

Archive size:
6,881,643 bytes

Archive entries:
127

The archive contains the three run analyses, aggregate Stage-A verdict, bootstrap evidence, workflow console, adjudication console, and internal SHA-256 manifest.

## 7. Reproduction limits

A full live rerun requires an authorized FIT IoT-LAB account and current platform availability. The supplement therefore supports:
1. source-level audit of the exact frozen algorithms;
2. deterministic re-adjudication from preserved sanitized/authorized evidence;
3. verification of treatment definitions, code authority, and claim ceilings.

It does not claim that private credentials or protected raw archives are publicly downloadable.

## 8. Gate

R7f_R3_SANITIZED_SUPPLEMENT=PREPARED
R7f_R3_PRIVATE_RAW_DATA_EXCLUDED=YES
R7f_R3_EXECUTED_CODE_DISCREPANCY_DISCLOSED=YES
