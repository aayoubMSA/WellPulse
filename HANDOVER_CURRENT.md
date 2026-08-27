# WellPulse — Current Handover

Last updated: 2026-08-27 after **WP2-P7B-R2 one-replacement requalification contract freeze PASS / stopped before live R3**.

## Executive state

- Canonical repository: `aayoubMSA/WellPulse`, branch `main`.
- Last accepted checkpoint: **P7B-R2 PASS_ONE_REPLACEMENT_CONTRACT_FREEZE / STOPPED**.
- Scientific weighted completion: **20%**.
- WP2 management/readiness: **95/100**; no partial scientific credit.
- WP0: **PASS**, 8/8.
- WP1: **PASS / FROZEN**, 12/12.
- WP2: **ACTIVE / PRE-SCORE BLOCKED**.
- WP3: **BLOCKED ON WP2**, 0/30.
- WP4: **BLOCKED**, 0/15.
- WP5: **PREPARED / NOT EXECUTED**, 0/20.
- FIT IoT-LAB: **FINAL PASS**.
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
- `WP2_P7B_R2=PASS_ONE_REPLACEMENT_CONTRACT_FREEZE`.
- `REQUALIFICATION_DECISION=GO_ONE_REPLACEMENT_NON_SCORED`.
- `P7B_RQ1_AUTHORITY_CONTRACT=FROZEN`.
- `P7B_RQ1_LIVE_AUTHORIZED=false`.
- successful P7B physical-qualification credit remains **40/100** from A+B only.
- `SCORED_AUTHORIZATION=BLOCKED:PRE_SCORE_PHYSICAL_QUALIFICATION_REQUIRED`.
- `scored_runs_authorized=false`.
- `HCI_CONTROL_ACTIONS_ENABLED=false`.

## P6 — final non-scored Golden baseline

Canonical record:

`docs/WP2_P6_GOLDEN_CLOSURE_2026-08-27.md`

Accepted Golden evidence:

- reservation UUID `5579cf25-dbb1-4d04-87e3-ff558e3be2af`;
- name `wpg7498036`;
- profile `PowderProfiles/srslte-controlled-rf`;
- profile revision `a6da96560b6526dc6816761282722c996418fd8c`;
- valid non-scored run `wp2-p6r-33099648133-20260827T174149Z`;
- scientific source SHA `bd1b5e12f3d2eca27ec81ccadbeec5afaa2f2159`;
- one reservation only; no scientific rerun;
- `t_rf_restore=2026-08-27T17:45:06.913285Z`;
- `t_service_ready=2026-08-27T17:45:32.001525Z`;
- `T_service=25.088240 s`;
- `t_app_complete=2026-08-27T17:45:37.295360Z`;
- `T_app=5.293835 s`;
- `T_total=30.382075 s`;
- primary cohort 181;
- valid by 300 s 181/181;
- `completeness_300=1.0`;
- missing/checksum/duplicate/late = 0/0/0/0;
- raw evidence + `/proj` escrow + controller pull + independent artifact round-trip PASS;
- deterministic TAR SHA-256 `ff72a50fd11db1d308f4049b49fffa317c8220c9290845434dbadc8dbef847cf`;
- GitHub artifact ID `9658678808`;
- teardown confirmed `2026-08-27T18:04:31Z`.

P6 Attempt 1 and later evidence-pipeline failures remain provenance and did not create a second scientific run/reservation.

## P7 — reusable-path hardening / scored authorization decision

Canonical record:

`docs/WP2_P7_SCORED_AUTHORIZATION_2026-08-27.md`

- management alias preparation hardened;
- receiver evidence collection uses live-qualified tar-stream semantics;
- planned post-cohort traffic separated from truly unexpected identities;
- clock/post-cohort/transport/retirement regressions executable under unittest discovery;
- Actions run `33103997677`, job `98628861177`: **36/36 PASS**;
- Golden offline reconstruction/escrow/interlock PASS;
- corruption fail-closed;
- no POWDER contact or scientific/scored run during P7.

P7 left scored authorization blocked because physical arm/restart/B2/washout qualification remained mandatory.

## P7B-A/B — original qualification contract and implementation

Canonical records:

- `docs/WP2_P7B_A_OFFLINE_CONTRACT_FREEZE_2026-08-27.md`
- `docs/WP2_P7B_B_OFFLINE_IMPLEMENTATION_CLOSURE_2026-08-27.md`
- `experiments/WP-PWD01/P7B_PHYSICAL_QUALIFICATION_PLAN_v1.md`
- `experiments/WP-PWD01/p7b-qualification-contract.json`

Original frozen design:

- reservation limit = exactly 1;
- automatic replacement = NO;
- automatic retry = NO;
- exactly three sequential non-scored S3 cells:
  `P7B-B1-S3 -> P7B-W1-S3 -> P7B-B2-S3`;
- fail-closed Q0 washout/readiness before every cell;
- generator outside gateway restart domain;
- gateway/client restart 60 s into Q3;
- exact B1/W1 low-level runtime/config matching except intended application-level persistence difference;
- B1 accepted/PUBACK/unacknowledged reconstruction;
- W1 SQLite WAL synchronous=FULL survival/replay;
- B2 Eclipse Paho Java 1.2.5 file persistence/disconnected buffer;
- deterministic reconstruction;
- strict raw-evidence survival/read-back before teardown.

Accepted offline QA:

- P7B-A run `33106623492`, job `98638079325`: **41/41 PASS**;
- P7B-B run `33108767123`, job `98645668213`: **56/56 PASS**;
- initial B2 Java API run `33108767171` FAILED and retained;
- compatibility correction commit `6892ad26810d598965dfbe85ecb38f53b1097a5c`;
- accepted B2 semantics run `33108848011`, job `98645950042`: three independent 5/5 restart-recovery trials, zero missing/duplicates.

## P7B-C — first authorized live qualification

Authoritative retained status:

`evidence/powder/wp2-p7b-c-live-status.md`

Reservation:

- UUID `26b6f315-459d-4a56-9167-69228e339f24`;
- name `wp7b3016138`;
- GitHub run `33113016138`;
- node run ID `wp2-p7b-c-33113016138-20260827T203140Z`;
- evidence class NON-SCORED PRE-SCORE PHYSICAL QUALIFICATION.

Passed before block:

- Portal READY;
- core/UE SSH;
- frozen profile revision;
- B1 Q0 route via `tun_srsue` to `172.16.0.1`;
- five Q0 probes with 0% loss;
- TLS/MQTT readiness publish;
- broker later proved receiver client `wp-hcrx-885b10cacb1c` connected, got CONNACK, subscribed to the exact B1 topic and remained alive through MQTT keepalive exchanges.

Controller result:

- first failure `RECEIVER_CONNECT_TIMEOUT`;
- completed cells: NONE;
- scientific measurement started: NO;
- W1: NOT STARTED;
- B2: NOT STARTED;
- controller RC 70;
- scored: NO.

Retained verdict:

`WP2_P7B_C=BLOCKED:RECEIVER_CONNECT_TIMEOUT`

Root cause is classified as an orchestration/evidence-path quoting defect, not demonstrated LTE/MQTT failure. The historical node runner passed receiver `--output-dir` through a single-quoted path containing literal `$HOME`, while the readiness watcher used the expanded expected path.

## P7B-D — first evidence survival/read-back/teardown

Authoritative retained status:

`evidence/powder/wp2-p7b-d-live-status.md`

- first preservation attempt run `33114265831`: fail-closed before persistent copy because of a preservation-path quoting defect;
- same-reservation retry run `33114517583`, job `98665610066`: workflow SUCCESS;
- `/proj` persistence for captured declared roots PASS;
- controller pull/internal SHA-256 verification PASS;
- GitHub artifact ID `9663926250`;
- ZIP digest `0bd31f534712d2f1fe3793008e7b00c1e6df85f58277686b3de5ffb5fd6455bb`;
- deterministic inner TAR SHA-256 `f49263f77d673cf5961dd6efb3b0ce2a3d7dde5969d48f20e0c383f105693877`;
- inner TAR bytes `296960`;
- independent artifact download and internal read-back PASS;
- teardown confirmed after off-POWDER verification.

Strict gap:

- expected core receiver `console.txt` existed;
- expected `receiver_events.jsonl` was not recovered before teardown;
- complete raw-evidence survival cannot be claimed.

Retained verdict:

`WP2_P7B_D=BLOCKED_STRICT_COMPLETENESS_RECEIVER_EVENT_LEDGER_NOT_RECOVERED`

## P7B-E — canonical blocked closure

Canonical record:

`docs/WP2_P7B_E_CANONICAL_BLOCKED_CLOSURE_2026-08-27.md`

Verdict:

`WP2_P7B_E=PASS_CANONICAL_BLOCKED_CLOSURE`

This freezes the failed/partial physical evidence without relabelling it. It does not mean P7B physical qualification passed.

All temporary P7B-C/D live workflows/triggers were retired. Retirement deletion runs `33115086371` and `33115100803` failed closed before live actions and created no new reservation/POWDER contact.

## P7B-R1 — receiver-path repair + observability QA

Canonical record:

`docs/WP2_P7B_R1_RECEIVER_PATH_OBSERVABILITY_CLOSURE_2026-08-27.md`

Verdict:

`WP2_P7B_R1=PASS_OFFLINE_RECEIVER_PATH_OBSERVABILITY_QA`

R1 implementation:

1. `scripts/wp2_p7b_path_contract.py`
   - absolute remote-path contract;
   - rejects literal `$HOME`, `~`, relative paths and unsafe path tokens;
   - derives one receiver path tree;
   - proves writer/watcher event path equality.

2. `scripts/wp2_p7b_c_node_r1.py`
   - wraps frozen base node runner rather than rewriting scientific cell logic;
   - resolves remote core home to an absolute path;
   - uses one receiver writer/watcher path;
   - writes `receiver_path_contract.json`;
   - checks receiver PID liveness while awaiting connect;
   - emits `RECEIVER_EXITED_BEFORE_CONNECT` on early exit;
   - emits bounded GitHub-compatible diagnostics before timeout/exit verdicts.

3. `scripts/wp2_p7b_preservation_helpers.sh`
   - no POWDER/SSH authority itself;
   - requires resolved absolute paths;
   - rejects literal shell-expansion paths;
   - source-hash manifests and verifies copied trees.

Accepted R1 QA:

- implementation/regression SHA `695b31cba6c0256b3637223abdfef4f4b11bf6ca`;
- Actions run `33116073295`, job `98670934415`;
- Python 3.12.14;
- paho-mqtt 2.1.0;
- **65/65 PASS**.

R1 recommendation:

`FUTURE_PHYSICAL_REQUALIFICATION_RECOMMENDATION=GO_CONDITIONAL`

R1 created no reservation/live authority.

## P7B-R2 — one-replacement requalification authority freeze

Canonical closure:

`docs/WP2_P7B_R2_REQUALIFICATION_CONTRACT_FREEZE_2026-08-27.md`

Machine-readable contract:

`experiments/WP-PWD01/p7b-requalification-r2-contract.json`

Contract Git blob SHA:

`2a5b7b4ca025811da665dd0159403abc12d4f4a8`

Verdict:

`WP2_P7B_R2=PASS_ONE_REPLACEMENT_CONTRACT_FREEZE`

Decision:

`REQUALIFICATION_DECISION=GO_ONE_REPLACEMENT_NON_SCORED`

Frozen replacement authority:

- authority ID `P7B-RQ1`;
- experiment name prefix `wp7brq1`;
- maximum new reservations = 1;
- second replacement = NO;
- automatic retry = NO;
- automatic new reservation = NO;
- requires separate explicit live authorization = YES;
- current live authorization = NO;
- scored authorization = NO.

Execution lock:

- tested R1 implementation commit `695b31cba6c0256b3637223abdfef4f4b11bf6ca`;
- only permitted node entrypoint `scripts/wp2_p7b_c_node_r1.py`;
- node entrypoint blob `6d28468c93742046d952668b9df1cad8e6ea78c0`;
- path contract blob `2e77e7e355e25c6e3f747956e2f2b0ac5ad46161`;
- preservation helper blob `9063ec2e97e9cbf7a9f76d6ea10920236d8370ef`;
- legacy `scripts/wp2_p7b_c_node.py` prohibited for replacement authority.

Future-controller static gate:

`scripts/wp2_p7b_r2_validate_controller.py`

- Git blob `92961f476ddab32f1df33756d3857ef27df92323`;
- requires exactly one reservation create;
- requires `P7B-RQ1` marker;
- requires repaired R1 entrypoint;
- rejects legacy entrypoint;
- requires `AUTOMATIC_RETRY=NO` and `SECOND_REPLACEMENT=NO`;
- requires resolved-path preservation helper;
- forbids scored authorization;
- requires evidence/off-POWDER gates before the single terminate operation.

Accepted R2 QA:

- regression SHA `b77609bfb9256a0eb189c0e5dd29a2f1f68c3bc2`;
- Actions run `33117108893`, job `98674462071`;
- Python 3.12.14;
- paho-mqtt 2.1.0;
- **73/73 PASS**;
- retired historical controller fails the R2 static gate;
- synthetic compliant future controller passes;
- no P7B live workflow/trigger exists after R2.

R2 contacted no POWDER system and created no reservation, SSH session, workflow, trigger, scientific run or scored run.

## Replacement evidence-survival contract

If `P7B-RQ1` is later explicitly live-authorized, its live patch must combine physical qualification with evidence survival so the earlier manual C->D gap is not repeated.

Required chain:

`node raw -> /proj persistent escrow -> controller pull -> GitHub artifact -> independent controller read-back -> outer/internal SHA-256 -> teardown`

Rules:

- resolved absolute paths only;
- literal `$HOME`/`~` preservation paths prohibited;
- complete raw evidence required;
- `TEARDOWN_AUTHORIZED=YES` only after both `EVIDENCE_ESCROW_GATE=PASS` and `CONTROLLER_OFFPOWDER_GATE=PASS`;
- evidence-gate failure leaves the experiment live and STOPs;
- no automatic retry or second replacement follows any failure.

## Frozen scientific controls

No scientific control changed in C/D/E/R1/R2:

- Q0/Q1/Q2/Q3 = `0/40/52/55 dB`;
- attenuation IDs `1 33 2 34` coupled;
- pre-impairment Q0 = 60 s;
- Q3 = 120 s;
- gateway/client restart = 60 s into Q3;
- exact cell order `P7B-B1-S3 -> P7B-W1-S3 -> P7B-B2-S3`;
- generator remains outside gateway restart domain;
- primary cohort cutoff = `t_rf_restore`;
- `t_rf_restore`, `t_service_ready`, `t_app_complete` distinct;
- `H_app=300 s` from `t_service_ready`;
- primary endpoint remains `completeness_300` at `t_service_ready + 300 s`;
- preserve `T_service`, `T_app`, `T_total`;
- no outcome/W1/Golden/scored-derived H re-estimation;
- S2/S3 clean restore order frozen;
- H1 remains valid adverse non-scored evidence;
- K1-K8 remain closed absent material interface change;
- negative/null/unfavorable outcomes never justify protocol drift.

## Current workflow surface

Canonical registry:

`docs/WORKFLOW_REGISTRY.md`

Exactly six workflows remain and all are offline/local. Exactly four standing offline sentinels remain. There is no P7B-RQ1 live workflow/trigger and no active P7B live execution surface.

## Exact next bounded patch

`WP2-P7B-R3 — ONE REPLACEMENT NON-SCORED PHYSICAL REQUALIFICATION + EVIDENCE SURVIVAL`

Status:

`P7B_RQ1_LIVE_AUTHORIZED=false`

R3 is **LIVE / NOT AUTHORIZED** and requires separate explicit user authorization. The R2 GO decision is only a prospective contract decision and does not itself authorize POWDER contact.

If and only if R3 is explicitly authorized, it may:

1. create exactly one replacement reservation under authority ID `P7B-RQ1`;
2. use the frozen profile/revision and verify live bindings/manifest/runtime before mutation;
3. execute exactly `P7B-B1-S3 -> P7B-W1-S3 -> P7B-B2-S3`;
4. require the independent Q0 fail-closed readiness gate before each cell;
5. stop later cells on any cell failure;
6. use only `scripts/wp2_p7b_c_node_r1.py`;
7. expose bounded first-cause diagnostics directly in GitHub Actions;
8. preserve complete evidence using resolved absolute paths;
9. complete `/proj` escrow, controller pull, artifact upload, independent read-back and hashes before teardown;
10. leave the experiment live if evidence gates fail;
11. create no automatic retry or second replacement;
12. keep `scored_runs_authorized=false` throughout.

After terminal R3 evidence, STOP for offline canonical closure and immutable pre-score snapshot/scored-authorization decision. Do not proceed directly to WP3.

## Prohibited until separate R3 live authorization

- no POWDER contact/reservation/SSH;
- no `P7B-RQ1` reservation;
- no physical B1/W1/B2 requalification;
- no Golden rerun;
- no H calibration;
- no RF recalibration;
- no scored B1/W1/B2;
- no OTA replication;
- no WP3;
- no `scored_runs_authorized=true`;
- no immutable pre-score snapshot claiming physical readiness.

## Mandatory read order for next agent

1. `HANDOVER_CURRENT.md`
2. `docs/WP2_P7B_R2_REQUALIFICATION_CONTRACT_FREEZE_2026-08-27.md`
3. `experiments/WP-PWD01/p7b-requalification-r2-contract.json`
4. `docs/NEXT_GATE.md`
5. `docs/MILESTONE_STATUS.md`
6. `docs/WP2_P7B_R1_RECEIVER_PATH_OBSERVABILITY_CLOSURE_2026-08-27.md`
7. `scripts/wp2_p7b_c_node_r1.py`
8. `scripts/wp2_p7b_path_contract.py`
9. `scripts/wp2_p7b_preservation_helpers.sh`
10. `scripts/wp2_p7b_r2_validate_controller.py`
11. `tests/test_wp2_p7b_r2_contract.py`
12. `docs/WP2_P7B_E_CANONICAL_BLOCKED_CLOSURE_2026-08-27.md`
13. `evidence/powder/wp2-p7b-c-live-status.md`
14. `evidence/powder/wp2-p7b-d-live-status.md`
15. `docs/WP2_P7B_B_OFFLINE_IMPLEMENTATION_CLOSURE_2026-08-27.md`
16. `docs/WP2_P7B_A_OFFLINE_CONTRACT_FREEZE_2026-08-27.md`
17. `experiments/WP-PWD01/P7B_PHYSICAL_QUALIFICATION_PLAN_v1.md`
18. `experiments/WP-PWD01/p7b-qualification-contract.json`
19. `docs/WP2_P7_SCORED_AUTHORIZATION_2026-08-27.md`
20. `docs/WP2_P6_GOLDEN_CLOSURE_2026-08-27.md`
21. `experiments/WP-PWD01/PRE_SCORE_P0_AMENDMENT_2026-08-26.md`
22. `experiments/WP-PWD01/PRE_SCORE_P1_AMENDMENT_2026-08-26.md`
23. `experiments/WP-PWD01/run-matrix.yaml`
24. `experiments/WP-PWD01/RECOVERY_SEMANTICS_AMENDMENT_v1.md`
25. `experiments/WP-PWD01/protocol.md`
26. `experiments/WP-PWD01/B2_SEMANTICS_GATE_v1.md`
27. `evidence/local/wp2-b2-semantics-latest.md`
28. `docs/WORKFLOW_REGISTRY.md`
29. `AGENTS.md`

## Shortest path

`P6 PASS -> P7 hardening PASS -> P7B-A/B offline PASS -> first P7B-C blocked before measurement -> P7B-D strict completeness blocked / teardown complete -> P7B-E blocked closure PASS -> R1 receiver-path/observability repair PASS -> R2 one-replacement contract freeze PASS -> STOP -> separate explicit R3 live authorization -> one P7B-RQ1 physical requalification + evidence survival -> STOP -> immutable pre-score snapshot + scored authorization -> WP3 -> WP4 -> WP5`

**STOP / HANDOVER READY — P7B-R3 LIVE NOT AUTHORIZED.**
