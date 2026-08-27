# WellPulse — Current Handover

Last updated: 2026-08-27 after **WP2-P7B-R1 receiver-path repair + observability regression QA PASS / stopped before R2**.

## Executive state

- Canonical repository: `aayoubMSA/WellPulse`, branch `main`.
- Last accepted checkpoint: **P7B-R1 PASS_OFFLINE_RECEIVER_PATH_OBSERVABILITY_QA / STOPPED**.
- Scientific weighted completion: **20%**.
- WP2 management/readiness: **95/100**; no partial scientific credit.
- WP0: **PASS**, 8/8.
- WP1: **PASS / FROZEN**, 12/12.
- WP2: **ACTIVE / PRE-SCORE BLOCKED**.
- WP3: **BLOCKED ON WP2**, 0/30.
- WP4: **BLOCKED**, 0/15.
- WP5: **PREPARED / NOT EXECUTED**, 0/20.
- FIT IoT-LAB layer: **FINAL PASS**.
- POWDER G0-G5: **PASS**.
- RF calibration: **PASS / FROZEN**.
- K1-K8 compatibility: **PASS / CLOSED**.
- `PRE_INTEGRATION_COMPATIBILITY_GATE=PASS`.
- `AUDIT_R1=PASS`.
- `LIVE_HCI_AND_RAW_EVIDENCE_GATE=PASS`.
- `WP2_P6=PASS_RECOVERED_SINGLE_RUN`.
- `WP2_P7_HARDENING_QA=PASS`.
- `WP2_P7B_A=PASS_OFFLINE_CONTRACT_FREEZE`.
- `WP2_P7B_B=PASS_OFFLINE_IMPLEMENTATION_PREMUTATION_QA`.
- `WP2_P7B_C=BLOCKED:RECEIVER_CONNECT_TIMEOUT`.
- `WP2_P7B_D=BLOCKED_STRICT_COMPLETENESS_RECEIVER_EVENT_LEDGER_NOT_RECOVERED`.
- `WP2_P7B_E=PASS_CANONICAL_BLOCKED_CLOSURE`.
- `WP2_P7B_R1=PASS_OFFLINE_RECEIVER_PATH_OBSERVABILITY_QA`.
- `FUTURE_PHYSICAL_REQUALIFICATION_RECOMMENDATION=GO_CONDITIONAL`.
- successful P7B physical-qualification credit remains **40/100** from A+B only.
- `SCORED_AUTHORIZATION=BLOCKED:PRE_SCORE_PHYSICAL_QUALIFICATION_REQUIRED`.
- `scored_runs_authorized=false`.
- `HCI_CONTROL_ACTIONS_ENABLED=false`.

## P6 — final non-scored Golden baseline

Canonical record:

`docs/WP2_P6_GOLDEN_CLOSURE_2026-08-27.md`

- experiment UUID `5579cf25-dbb1-4d04-87e3-ff558e3be2af`, name `wpg7498036`;
- profile `PowderProfiles/srslte-controlled-rf`, revision `a6da96560b6526dc6816761282722c996418fd8c`;
- valid non-scored run `wp2-p6r-33099648133-20260827T174149Z`;
- one reservation only; no scientific rerun;
- `T_service=25.088240 s`, `T_app=5.293835 s`, `T_total=30.382075 s`;
- primary cohort `181`, valid by 300 s `181/181`, `completeness_300=1.0`;
- missing/checksum/duplicate/late = `0/0/0/0`;
- raw evidence, persistent `/proj` escrow, controller pull and independent artifact round-trip all PASS;
- deterministic TAR SHA-256 `ff72a50fd11db1d308f4049b49fffa317c8220c9290845434dbadc8dbef847cf`;
- GitHub artifact ID `9658678808`;
- teardown confirmed `2026-08-27T18:04:31Z`.

P6 Attempt 1 and later evidence-pipeline failures remain preserved as infrastructure/provenance evidence and did not create a second scientific measurement/reservation.

## P7 — hardening and authorization decision

Canonical record:

`docs/WP2_P7_SCORED_AUTHORIZATION_2026-08-27.md`

- reusable-path hardening PASS without frozen-science change;
- run `33103997677`, job `98628861177`: **36/36 tests PASS**;
- offline escrow/interlock and corruption fail-closed QA PASS;
- no POWDER contact, mutation, science or scored run;
- scored authorization remained blocked on mandatory pre-score physical qualification.

## P7B-A/B — offline contract and implementation

Canonical records:

- `docs/WP2_P7B_A_OFFLINE_CONTRACT_FREEZE_2026-08-27.md`
- `docs/WP2_P7B_B_OFFLINE_IMPLEMENTATION_CLOSURE_2026-08-27.md`

Frozen qualification design:

- original limit: exactly one future reservation;
- exactly three sequential non-scored S3 cells: `P7B-B1-S3 -> P7B-W1-S3 -> P7B-B2-S3`;
- independent fail-closed Q0 washout/readiness before every cell;
- generator outside gateway restart domain;
- exact B1/W1 low-level match except intended application persistence difference;
- B1 accepted/PUBACK/unacknowledged reconstruction;
- W1 SQLite durable survival/replay;
- B2 Eclipse Paho Java 1.2.5 durable-client semantics;
- deterministic evidence reconstruction and strict evidence-survival requirements.

Offline accepted evidence:

- P7B-A run `33106623492`, job `98638079325`: **41/41 PASS**;
- P7B-B full reconstruction QA run `33108767123`, job `98645668213`: **56/56 PASS**;
- initial B2 Java API run `33108767171` FAILED and remains provenance;
- one-line compatibility fix `6892ad26810d598965dfbe85ecb38f53b1097a5c`;
- accepted B2 semantics run `33108848011`, job `98645950042`: exact Paho Java 1.2.5 plus three independent 5/5 restart-recovery trials, zero missing/duplicates.

Verdicts:

- `WP2_P7B_A=PASS_OFFLINE_CONTRACT_FREEZE`
- `WP2_P7B_B=PASS_OFFLINE_IMPLEMENTATION_PREMUTATION_QA`

## P7B-C — first authorized live qualification result

Authoritative retained status:

`evidence/powder/wp2-p7b-c-live-status.md`

Authorized live reservation:

- experiment UUID `26b6f315-459d-4a56-9167-69228e339f24`;
- experiment name `wp7b3016138`;
- GitHub run `33113016138`;
- node run ID `wp2-p7b-c-33113016138-20260827T203140Z`;
- evidence class: NON-SCORED PRE-SCORE PHYSICAL QUALIFICATION.

Observed before block:

- Portal reservation reached `ready`;
- core and UE SSH passed;
- frozen profile revision matched;
- B1 Q0 route used `tun_srsue` to `172.16.0.1`;
- five Q0 probes passed with 0% packet loss;
- TLS/MQTT readiness publish passed (`rc=0`);
- broker proved receiver `wp-hcrx-885b10cacb1c` connected, received CONNACK, subscribed to the exact B1 topic and remained alive through repeated PINGREQ/PINGRESP exchanges.

Controller result:

- first failure `RECEIVER_CONNECT_TIMEOUT`;
- completed cells: NONE;
- scientific measurement started: NO;
- W1: NOT STARTED;
- B2: NOT STARTED;
- controller RC `70`;
- scored: NO.

Retained verdict:

`WP2_P7B_C=BLOCKED:RECEIVER_CONNECT_TIMEOUT`

Root-cause classification is **orchestration/evidence-path quoting defect**, not demonstrated LTE/MQTT transport failure. The old node runner built the core receiver path with literal `$HOME`, passed `--output-dir` through single quotes, but watched an expanded path. Broker-alive/event-ledger-unseen is consistent with that writer/watcher mismatch.

## P7B-D — evidence survival/read-back/teardown

Authoritative retained strict status:

`evidence/powder/wp2-p7b-d-live-status.md`

First preservation attempt:

- run `33114265831`;
- failed closed before persistent copy due the same class of path-quoting defect;
- no artifact;
- no teardown in that attempt.

Same-reservation preservation retry:

- run `33114517583`, job `98665610066`: SUCCESS;
- no new reservation;
- no scientific rerun;
- no scored run;
- `/proj` persistence for declared UE/core roots PASS;
- controller pull/internal SHA-256 verification PASS;
- GitHub artifact ID `9663926250`;
- artifact ZIP digest `0bd31f534712d2f1fe3793008e7b00c1e6df85f58277686b3de5ffb5fd6455bb`;
- deterministic inner TAR SHA-256 `f49263f77d673cf5961dd6efb3b0ce2a3d7dde5969d48f20e0c383f105693877`;
- deterministic inner TAR bytes `296960`;
- independent artifact download/hash read-back PASS;
- teardown authorized only after off-POWDER verification;
- teardown confirmed after Portal `terminating`, then exact UUID not found.

Strict evidence gap:

- expected core root contained receiver `console.txt` but did not contain expected `receiver_events.jsonl`;
- exact receiver event ledger was not recovered before teardown;
- complete raw-evidence survival cannot be claimed.

Retained strict verdict:

`WP2_P7B_D=BLOCKED_STRICT_COMPLETENESS_RECEIVER_EVENT_LEDGER_NOT_RECOVERED`

## P7B-E — canonical blocked closure

Canonical record:

`docs/WP2_P7B_E_CANONICAL_BLOCKED_CLOSURE_2026-08-27.md`

Verdict:

`WP2_P7B_E=PASS_CANONICAL_BLOCKED_CLOSURE`

This means canonical closure itself is complete and preserves the failed/partial evidence without relabelling. It does not mean physical qualification passed.

All temporary P7B-C/D live workflows/triggers were retired after terminal evidence/teardown. Retirement deletion pushes caused two fail-closed QA-provenance Actions runs, but both stopped before live actions and created no new reservation/POWDER contact.

## P7B-R1 — receiver-path repair + observability QA

Canonical closure:

`docs/WP2_P7B_R1_RECEIVER_PATH_OBSERVABILITY_CLOSURE_2026-08-27.md`

Verdict:

`WP2_P7B_R1=PASS_OFFLINE_RECEIVER_PATH_OBSERVABILITY_QA`

R1 is entirely offline. It created no POWDER reservation, SSH, testbed mutation, scientific run, scored run, workflow or trigger.

### Accepted implementation

1. `576354a84be46683b5ff94ce6f6b4ced883b2402` — `scripts/wp2_p7b_path_contract.py`
   - absolute remote-path contract;
   - rejects literal `$HOME`, `~`, relative paths and unsafe path tokens;
   - derives one receiver path tree;
   - proves event writer/watcher equality.

2. `f6a709508db46e8b99448abdf05ec37964aa3f4e` — `scripts/wp2_p7b_c_node_r1.py`
   - wraps frozen base runner rather than rewriting scientific cell logic;
   - resolves remote core home to an absolute path;
   - launches receiver with one absolute writer/watcher path;
   - writes `receiver_path_contract.json`;
   - detects receiver process exit while awaiting connect;
   - emits `RECEIVER_EXITED_BEFORE_CONNECT` rather than waiting for a generic timeout;
   - emits bounded GitHub-compatible diagnostics on failure.

3. `544c0b9b40c6d845bf20bf7627f546ddbdceb55b` — `scripts/wp2_p7b_preservation_helpers.sh`
   - no SSH/POWDER authority itself;
   - requires already-resolved absolute source/destination paths;
   - rejects literal shell-expansion paths;
   - source-hash manifests and verifies copied trees.

4. `695b31cba6c0256b3637223abdfef4f4b11bf6ca` — regression expansion in `tests/test_wp2_p7b_c_premutation.py`.

### R1 observability contract

On receiver startup/connection failure, bounded diagnostics now include:

- receiver process state;
- receiver console tail;
- receiver event-ledger tail;
- broker log tail;
- route;
- Q0 probes;
- TLS/MQTT probe;
- Q0 radio capture;
- runtime manifest/readiness records when present;
- Python and paho-mqtt version;
- Java version;
- Paho Java JAR SHA-256 when present;
- broker certificate fingerprint when present.

This directly addresses the user's observation that the final generic `exit code 1` repeatedly obscured the first actionable cause.

### R1 QA

Accepted Local Unit Tests:

- run `33116073295`;
- job `98670934415`;
- tested SHA `695b31cba6c0256b3637223abdfef4f4b11bf6ca`;
- Python `3.12.14`;
- `paho-mqtt==2.1.0`;
- **65/65 tests PASS**;
- all prior P7B contract/reconstruction/restart/readiness/no-reservation-authority tests remained PASS.

### Historical controller integration caveat

The retired historical controller `powder/wp2_p7b_c_execute.sh` still invokes the old `scripts/wp2_p7b_c_node.py`. It has no current live workflow/trigger authority and must not be reused directly.

Any future requalification contract must explicitly freeze `scripts/wp2_p7b_c_node_r1.py` as the only allowed node entrypoint and regression-check the authority-bearing controller against that exact entrypoint before a live workflow is created.

### R1 recommendation

`FUTURE_PHYSICAL_REQUALIFICATION_RECOMMENDATION=GO_CONDITIONAL`

Reason: the first live attempt stopped before scientific measurement, the physical LTE/TLS/MQTT path had passed its relevant readiness evidence, broker evidence proved the receiver was alive, and the identified operational defect is now concretely repaired/regression-protected without changing the scientific protocol.

This recommendation is not authority to run again.

## Frozen scientific controls

No frozen science changed during C/D/E/R1:

- Q0/Q1/Q2/Q3 = `0/40/52/55 dB`;
- attenuation IDs `1 33 2 34` remain coupled;
- pre-impairment Q0 = 60 s;
- Q3 = 120 s;
- S3 gateway restart = 60 s into Q3;
- primary cohort cutoff = `t_rf_restore`;
- `t_rf_restore`, `t_service_ready`, `t_app_complete` remain distinct;
- `H_app=300 s` from `t_service_ready`;
- primary endpoint remains `completeness_300` at `t_service_ready + 300 s`;
- preserve `T_service`, `T_app`, `T_total`;
- no outcome/W1/Golden/scored-derived H re-estimation;
- S2/S3 clean restore order frozen;
- H1 remains valid adverse non-scored evidence and is not reopened;
- K1-K8 remain closed absent material interface change;
- negative/null/unfavorable outcomes remain valid evidence and never justify protocol drift.

## Current workflow surface

Canonical registry:

`docs/WORKFLOW_REGISTRY.md`

Exactly six workflows remain, all offline/local. Four standing offline sentinels remain. R1 added no workflow or trigger. There is no current P7B live execution surface.

## Exact next bounded patch

`WP2-P7B-R2 — REQUALIFICATION AUTHORITY + CONTRACT FREEZE`

Status: **OFFLINE ONLY / NOT STARTED**.

Why R2 is required:

- the original P7B contract froze `reservation_limit=1`;
- the original contract prohibits automatic retry and automatic new reservation;
- that one authorized reservation was consumed;
- R1 may recommend requalification but cannot silently create replacement authority.

R2 may only decide and freeze whether one replacement non-scored qualification reservation is justified because the first attempt stopped before scientific measurement on a specific operational defect.

If R2 issues GO, it must at minimum:

1. preserve the original C/D evidence unchanged;
2. explicitly permit at most one named replacement qualification reservation;
3. prohibit automatic retries and any second replacement;
4. freeze `scripts/wp2_p7b_c_node_r1.py` as the only permitted node entrypoint;
5. regression-check that the future authority-bearing controller invokes that entrypoint;
6. freeze validated absolute-path evidence-preservation mechanics before live execution;
7. preserve the exact three-cell order and all scientific controls;
8. require bounded raw diagnostics before a final generic failure status;
9. require one-shot temporary live workflow/trigger retirement after terminal evidence;
10. STOP again before any live contact.

R2 itself has no POWDER authority.

## Prohibited until R2 closes and later separate explicit live authorization exists

- no POWDER contact/reservation/SSH;
- no replacement P7B reservation;
- no physical B1/W1/B2 retry;
- no Golden rerun;
- no H calibration;
- no RF recalibration;
- no scored B1/W1/B2;
- no OTA replication;
- no WP3;
- no `scored_runs_authorized=true`;
- no immutable pre-score snapshot claiming readiness.

## Mandatory read order for next agent

1. `HANDOVER_CURRENT.md`
2. `docs/WP2_P7B_R1_RECEIVER_PATH_OBSERVABILITY_CLOSURE_2026-08-27.md`
3. `docs/WP2_P7B_E_CANONICAL_BLOCKED_CLOSURE_2026-08-27.md`
4. `evidence/powder/wp2-p7b-c-live-status.md`
5. `evidence/powder/wp2-p7b-d-live-status.md`
6. `docs/NEXT_GATE.md`
7. `docs/MILESTONE_STATUS.md`
8. `scripts/wp2_p7b_path_contract.py`
9. `scripts/wp2_p7b_c_node_r1.py`
10. `scripts/wp2_p7b_preservation_helpers.sh`
11. `tests/test_wp2_p7b_c_premutation.py`
12. `powder/wp2_p7b_c_execute.sh`
13. `scripts/wp2_p7b_c_node.py`
14. `src/wellpulse/p7b.py`
15. `scripts/wp2_p7b_generator.py`
16. `scripts/wp2_p7b_python_gateway.py`
17. `scripts/wp2_p7b_validate_readiness.py`
18. `scripts/wp2_p7b_compare_manifests.py`
19. `scripts/reconstruct_wp2_p7b.py`
20. `docs/WP2_P7B_B_OFFLINE_IMPLEMENTATION_CLOSURE_2026-08-27.md`
21. `docs/WP2_P7B_A_OFFLINE_CONTRACT_FREEZE_2026-08-27.md`
22. `experiments/WP-PWD01/P7B_PHYSICAL_QUALIFICATION_PLAN_v1.md`
23. `experiments/WP-PWD01/p7b-qualification-contract.json`
24. `docs/WP2_P7_SCORED_AUTHORIZATION_2026-08-27.md`
25. `docs/WP2_P6_GOLDEN_CLOSURE_2026-08-27.md`
26. `experiments/WP-PWD01/PRE_SCORE_P0_AMENDMENT_2026-08-26.md`
27. `experiments/WP-PWD01/PRE_SCORE_P1_AMENDMENT_2026-08-26.md`
28. `experiments/WP-PWD01/run-matrix.yaml`
29. `experiments/WP-PWD01/RECOVERY_SEMANTICS_AMENDMENT_v1.md`
30. `experiments/WP-PWD01/protocol.md`
31. `experiments/WP-PWD01/B2_SEMANTICS_GATE_v1.md`
32. `evidence/local/wp2-b2-semantics-latest.md`
33. `docs/WORKFLOW_REGISTRY.md`
34. `AGENTS.md`

## Shortest path

`P6 PASS -> P7 hardening PASS -> P7B-A/B offline PASS -> P7B-C BLOCKED before measurement -> P7B-D strict completeness BLOCKED / teardown complete -> P7B-E canonical blocked closure PASS -> P7B-R1 offline repair/QA PASS -> STOP -> P7B-R2 offline requalification authority/contract freeze -> STOP -> separate explicit live authorization -> at most one replacement physical qualification -> strict evidence survival -> immutable pre-score snapshot + scored authorization -> WP3 -> WP4 -> WP5`

**STOP / HANDOVER READY — NEXT PATCH P7B-R2 OFFLINE ONLY.**
