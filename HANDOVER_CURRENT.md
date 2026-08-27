# WellPulse — Current Handover

Last updated: 2026-08-27 after **WP2-P7B-E canonical blocked closure**.

## Executive state

- Canonical repository: `aayoubMSA/WellPulse`, branch `main`.
- Last accepted checkpoint: **P7B-E PASS_CANONICAL_BLOCKED_CLOSURE / STOPPED**.
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
- Successful P7B qualification credit remains **40/100** from A+B only.
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

P6 Attempt 1 and later G8/escrow salvage failures remain preserved as infrastructure/provenance evidence and did not create a second scientific measurement/reservation.

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

Frozen qualification contract:

- one future reservation;
- exactly three sequential non-scored S3 cells: `P7B-B1-S3 -> P7B-W1-S3 -> P7B-B2-S3`;
- independent fail-closed Q0 washout/readiness before each cell;
- generator outside gateway restart domain;
- exact B1/W1 low-level runtime/config match except intended persistence difference;
- B1 accepted/PUBACK/unacknowledged reconstruction;
- W1 SQLite durable survival/replay;
- B2 Eclipse Paho Java 1.2.5 durable-client semantics;
- deterministic evidence reconstruction and strict evidence-survival requirements.

Offline implementation/QA:

- 51/51 then 56/56 unit tests PASS;
- initial B2 Java API run `33108767171` FAILED and retained as provenance;
- one-line compatibility fix `6892ad26810d598965dfbe85ecb38f53b1097a5c`;
- accepted B2 semantics run `33108848011`, job `98645950042`: exact Paho Java 1.2.5 build PASS plus three independent 5/5 restart-recovery trials, zero missing/duplicates.

Verdicts:

- `WP2_P7B_A=PASS_OFFLINE_CONTRACT_FREEZE`
- `WP2_P7B_B=PASS_OFFLINE_IMPLEMENTATION_PREMUTATION_QA`

## P7B-C — authorized live qualification result

Canonical retained status:

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
- broker later proved receiver `wp-hcrx-885b10cacb1c` connected, received CONNACK, subscribed to the exact B1 topic, and remained alive through repeated MQTT PINGREQ/PINGRESP exchanges.

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

Root-cause classification is **orchestration/evidence-path quoting defect**, not demonstrated LTE/MQTT transport failure. In `scripts/wp2_p7b_c_node.py`, receiver `--output-dir` is built through a single-quoted path containing `$HOME`, whereas the console redirection/readiness watcher uses an expanded expected path. The broker-alive / event-ledger-unseen contradiction is consistent with this path mismatch.

## P7B-D — evidence survival/read-back/teardown

Canonical retained strict status:

`evidence/powder/wp2-p7b-d-live-status.md`

First preservation attempt:

- run `33114265831`;
- failed closed before persistent copy due a preservation-script path quoting defect;
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
- independent artifact download PASS;
- independent inner TAR and internal source-hash read-back PASS;
- teardown authorized only after off-POWDER verification;
- teardown confirmed after Portal `terminating` then exact UUID not found.

Strict evidence gap:

- expected core root contained receiver `console.txt` but did not contain expected `receiver_events.jsonl`;
- exact receiver event ledger was not recovered before teardown;
- complete raw-evidence survival must not be claimed.

Retained strict verdict:

`WP2_P7B_D=BLOCKED_STRICT_COMPLETENESS_RECEIVER_EVENT_LEDGER_NOT_RECOVERED`

## P7B-E — canonical blocked closure

Canonical record:

`docs/WP2_P7B_E_CANONICAL_BLOCKED_CLOSURE_2026-08-27.md`

Verdict:

`WP2_P7B_E=PASS_CANONICAL_BLOCKED_CLOSURE`

Meaning: the canonical closure itself is complete and preserves the failed/partial evidence without relabelling. It does not mean physical qualification passed.

Successful P7B qualification credit remains **40/100** from A+B only. C did not pass, D did not pass strict completeness, and E administrative closure creates no physical qualification credit.

## Retirement cleanup provenance

All temporary P7B live workflows/triggers are now retired from `main`:

- `wp2-p7b-c-live.yml` + `.wp2-p7b-c-live-trigger`;
- `wp2-p7b-d-evidence-survival.yml` + `.wp2-p7b-d-trigger`;
- `wp2-p7b-d-evidence-survival-retry.yml` + `.wp2-p7b-d-retry-trigger`.

Deletion of the P7B-C trigger generated retirement run `33115086371` because GitHub path filters also react to deletions. It failed at the **Premutation authority and syntax gate**; controller prerequisites and reservation execution were skipped. No reservation and no POWDER contact occurred.

Deletion of the first P7B-D trigger generated retirement run `33115100803`. It failed at **Freeze P7B-D authority boundary**; all preservation/live/teardown actions were skipped. No POWDER contact or state change occurred.

Both runs are QA provenance only. Their temporary status-file writes were explicitly superseded by the restored authoritative C/D retained status files.

`docs/WORKFLOW_REGISTRY.md` is again consistent: exactly six offline/local workflows and four standing offline sentinels remain; no P7B live execution surface remains.

## Frozen scientific controls

No frozen science changed during C/D/E:

- Q0/Q1/Q2/Q3 = `0/40/52/55 dB`;
- attenuation IDs `1 33 2 34` remain coupled;
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

## Exact next bounded patch

`WP2-P7B-R1 — RECEIVER-PATH REPAIR + OBSERVABILITY REGRESSION QA`

Status: **OFFLINE NEXT PATCH ONLY**.

R1 may only:

1. fix `$HOME`/remote-path quoting in P7B-C receiver launch and preservation helpers;
2. make receiver startup fail-fast on process exit and prove writer/watcher path equality;
3. echo bounded raw diagnostics directly into GitHub Actions on failure: receiver process state, receiver console/events, broker tail, route, Q0 probes, TLS probe, runtime/version locks;
4. add regressions that reject literal `$HOME` output paths and any watcher/writer path mismatch;
5. run offline unit/reconstruction/contract QA only;
6. issue a GO/BLOCKED recommendation on whether a future physical requalification reservation is justified.

R1 does **not** authorize POWDER contact, SSH, a replacement reservation, physical requalification, scored work, or WP3.

## Prohibited until R1 closes and later explicit live authorization exists

- no POWDER contact/reservation/SSH;
- no P7B physical retry or replacement reservation;
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
2. `docs/WP2_P7B_E_CANONICAL_BLOCKED_CLOSURE_2026-08-27.md`
3. `evidence/powder/wp2-p7b-c-live-status.md`
4. `evidence/powder/wp2-p7b-d-live-status.md`
5. `docs/NEXT_GATE.md`
6. `docs/MILESTONE_STATUS.md`
7. `scripts/wp2_p7b_c_node.py`
8. `src/wellpulse/p7b.py`
9. `scripts/wp2_p7b_generator.py`
10. `scripts/wp2_p7b_python_gateway.py`
11. `scripts/wp2_p7b_validate_readiness.py`
12. `scripts/wp2_p7b_compare_manifests.py`
13. `scripts/reconstruct_wp2_p7b.py`
14. `docs/WP2_P7B_B_OFFLINE_IMPLEMENTATION_CLOSURE_2026-08-27.md`
15. `docs/WP2_P7B_A_OFFLINE_CONTRACT_FREEZE_2026-08-27.md`
16. `experiments/WP-PWD01/P7B_PHYSICAL_QUALIFICATION_PLAN_v1.md`
17. `experiments/WP-PWD01/p7b-qualification-contract.json`
18. `docs/WP2_P7_SCORED_AUTHORIZATION_2026-08-27.md`
19. `docs/WP2_P6_GOLDEN_CLOSURE_2026-08-27.md`
20. `experiments/WP-PWD01/PRE_SCORE_P0_AMENDMENT_2026-08-26.md`
21. `experiments/WP-PWD01/PRE_SCORE_P1_AMENDMENT_2026-08-26.md`
22. `experiments/WP-PWD01/run-matrix.yaml`
23. `experiments/WP-PWD01/RECOVERY_SEMANTICS_AMENDMENT_v1.md`
24. `experiments/WP-PWD01/protocol.md`
25. `experiments/WP-PWD01/B2_SEMANTICS_GATE_v1.md`
26. `evidence/local/wp2-b2-semantics-latest.md`
27. `docs/WORKFLOW_REGISTRY.md`
28. `AGENTS.md`

## Shortest path

`P6 PASS -> P7 hardening PASS -> P7B-A/B offline PASS -> P7B-C BLOCKED before measurement -> P7B-D strict completeness BLOCKED / teardown complete -> P7B-E canonical blocked closure PASS -> STOP -> P7B-R1 offline repair/QA -> STOP -> separate decision and explicit authority for any future live requalification -> successful physical qualification required -> immutable snapshot + scored authorization -> WP3 -> WP4 -> WP5`

**STOP / HANDOVER READY — NEXT PATCH P7B-R1 OFFLINE ONLY.**
