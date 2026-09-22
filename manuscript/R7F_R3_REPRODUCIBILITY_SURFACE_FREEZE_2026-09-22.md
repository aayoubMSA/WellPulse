# WellPulse IEEE Revival — R7f-R3 Reproducibility-Surface Repair Freeze

**Date:** 2026-09-22
**Status:** PASS
**Parent authority:** R7f-R2 + R7f hostile review
**Scope:** execution-configuration exposure + sanitized reviewer supplement + reproducibility section

## 1. New manuscript source

`manuscript/revival_2026-09-22/WellPulse_Revival_R7fR3_ReproSurface_20260922.tex`

R7f-R2 remains preserved unchanged.

## 2. Reproducibility surface added

The manuscript now exposes a compact execution-configuration table covering the two FIT campaigns.

Historical FIT final campaign:
- GitHub Actions run 32628193889;
- FIT experiments 448265 / 448266 / 448269;
- Grenoble A8-100 as recorded by the final status;
- Python-3.5-compatible A8 runner;
- paho-mqtt 1.6.1;
- broker mqtt4.iot-lab.info:8883;
- QoS 1;
- TLS peer verification;
- C1/C2 iptables OUTPUT REJECT on broker TCP/8883 for records 3001–5000;
- C2 gateway-process exec restart after record 4000;
- SQLite queue with synchronous=FULL;
- exact historical M3 timestamp not instrumented;
- receiver mosquitto_sub version was not preserved and is not invented.

Prospective FIT Stage A:
- GitHub Actions run 35653569079;
- FIT experiment 449953;
- Grenoble A8-102;
- frozen authority c9fd8968f1408d9a2e3a57dd825df05c2f1d9147;
- controller Python 3.12.14;
- Python-3.5-compatible A8 runner;
- paho-mqtt 1.6.1;
- W1/C1 only;
- H = sequences 3001–5000;
- no process restart;
- sidecar CONNACK/PUBACK/source events;
- receiver timestamp stream;
- 9-sample pre/post midpoint clock bounds;
- same-receiver causal-witness rule.

## 3. Provenance discrepancy disclosed

A real documentation/execution inconsistency was discovered and preserved:
- AMENDMENT_002_PREFINAL_CORRECTIONS.md says the intended FIT adapter should use SQLite journal_mode=DELETE;
- the actual executed frozen runner blob calls PRAGMA journal_mode=WAL.

Reproduction authority is therefore the executed code blob:
`3683737f9756c8b96c4c2e41f4372fc388fadb7d`.

The manuscript/supplement explicitly states:
- reproduction follows executed code authority;
- no scientific claim is attributed to SQLite journal-mode choice;
- the inconsistency is not silently normalized.

No new experiment was required.

## 4. Sanitized reviewer supplement

Created:
`manuscript/revival_2026-09-22/supplement_r7fr3/`

Contents:
- R7fR3_REPRODUCIBILITY_SUPPLEMENT.md;
- R7fR3_EXECUTION_CONFIG.csv;
- R7fR3_CODE_MANIFEST.csv;
- r7fr3_selfcheck.py.

The package contains only sanitized reproducibility material plus safe execution code/protocol authorities:
- frozen FIT runner;
- qualified instrumentation wrapper;
- receiver timestamp stream;
- scored Stage-A loop;
- deterministic per-run adjudicator;
- aggregate adjudicator;
- Stage-A tests;
- experiment contract;
- Amendment 001;
- Amendment 002.

Internal raw-preservation ledgers and old result/status files containing storage identifiers are excluded.

## 5. Code authority verification

The supplement self-check verifies Git blob identity for the listed code/protocol files and checks:
- broker/port authority;
- outage boundaries 3001–5000;
- restart position 4000;
- executed WAL + synchronous FULL source semantics;
- instrumentation events CONNACK/PUBACK/SOURCE_GENERATED;
- exact R1/R2/R3 boundedness;
- no Stage-B execution.

## 6. Clock-method disclosure

The supplement now records the prospective clock procedure:
- 9 receiver samples pre/post;
- 9 source samples pre/post;
- t0/t1 midpoint offset estimate;
- RTT/2 uncertainty;
- minimum-RTT sample selection;
- pre/post host interval hull;
- conservative receiver-minus-source relative interval;
- D23 positive only when the entire conservative interval is above zero;
- otherwise UNRESOLVED;
- same-receiver seq5001 causal witness as an independent clock-free route.

The 5 s Q0 bound is explicitly identified as a qualification usability ceiling, not a scientific effect threshold.

## 7. Privacy / release boundary

Fail-closed package QA verifies exclusion of:
- FIT credential material;
- SSH private keys;
- private Drive file/folder identifiers;
- internal raw-preservation records;
- historical durable Drive archive IDs.

Protected raw archives remain the immutable measurement authorities but are not exposed in the reviewer package.

## 8. Manuscript reproducibility section

The manuscript now points reviewers to the sanitized supplement and states:
- exact public code authorities are versioned;
- protected raw evidence remains hash-preserved;
- live reruns require an authorized FIT IoT-LAB account;
- unknown receiver mosquitto_sub versions are left unreported rather than inferred;
- no archival DOI is invented.

## 9. Final QA

Temporary QA PR: `#47`.

Earlier QA attempts were not accepted:
- 35708049250: escaped supplement-path assertion defect;
- 35708196467: superseded because its initial package builder could include internal storage identifiers;
- 35708572563: fail-closed privacy gate correctly caught literal sensitive markers in the self-check;
- 35708991525: fail-closed overfull-box gate correctly caught execution-table layout overflow.

Final accepted run:
`35709304425` — SUCCESS.

Passed:
- exact R7f-R3 authority checkout;
- R7f-R2 science locks;
- supplement self-check;
- Git blob identity checks;
- fail-closed privacy scan;
- IEEEtran compile;
- undefined citations = 0;
- undefined references = 0;
- LaTeX errors = 0;
- overfull boxes = 0;
- sanitized package build;
- SHA-256 manifests.

Final manuscript build:
- pages: 8;
- R7f-R3 TEX SHA-256:
  `946790584d61571a257533a6b59c1df0256a10bb765faf6a113900343165ffd7`;
- R7f-R3 PDF SHA-256:
  `898ee156f02b502950a52e340089180ef3f74dea4d7f1a164352f2baa096f690`;
- sanitized reproducibility TAR.GZ SHA-256:
  `7f12ba57ca5a3c2b4fa84073dbb81107050a0bbfd67c1cac09e77e092c2fc0c8`.

Final Actions artifact:
- artifact ID: 10685642255;
- size: 252,433 bytes;
- digest:
  `sha256:503d9d953e75e3fe7a83c8e1b6bad9f294197f4b936f9348e0b41a5f0684c16e`.

## 10. Durable preservation

Drive folder:
`P12_WellPulse / R7fR3_Reproducibility_Surface_2026-09-22`

Drive folder ID:
`1y5IFTGVZO6UU87ZG0GnDxXt3ard1SCEx`

Drive file:
`WellPulse_R7fR3_Reproducibility_QA_35709304425.zip`

Drive file ID:
`1--MwBB_wRSNGnJ3rnAq7tsiwN3QYnNnS`

Drive read-back:
- size = 252,433 bytes;
- SHA-256 = `503d9d953e75e3fe7a83c8e1b6bad9f294197f4b936f9348e0b41a5f0684c16e`;
- exact match to GitHub Actions artifact digest.

## 11. Repository authority

- manuscript source blob:
  `0a4455866cb22ce21083e2bd3ac67c01a455d6f7`;
- supplement blob:
  `ca80b83b753eb8f5f1980ee5f91cfd6cc500d88c`;
- config blob:
  `bc4b6c85037c5571bc8187b5fd1d3d1fd644ba6c`;
- code-manifest blob:
  `d07cd79d3d82fba750809cf000bc0087174c647a`;
- self-check blob:
  `05751a640931facd25483235d1b65ad9445f9b2a`.

## 12. Gate

`R7f_R3_REPRODUCIBILITY_SURFACE=PASS`

`R7f_R3_SANITIZED_SUPPLEMENT=PASS`

`R7f_R3_PRIVACY_GATE=PASS`

`R7f_R3_PACKAGE_PRESERVATION=PASS`

`NEXT=R7f-R4_EVIDENCE_PRESENTATION_REPAIR`

`R7g_ENTRY=LOCKED`

R7g remains locked until R7f-R4 passes.