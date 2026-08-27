# WellPulse — Current Handover

Last updated: 2026-08-27 after **WP2-P7B-A offline contract freeze PASS / stopped before P7B-B**.

## Executive state

- Canonical repository: `aayoubMSA/WellPulse`, branch `main`.
- Last accepted checkpoint: **WP2-P7B-A PASS / STOPPED**.
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
- `WP2_P7B_PROGRESS=20/100`.
- `SCORED_AUTHORIZATION=BLOCKED:PRE_SCORE_PHYSICAL_QUALIFICATION_REQUIRED`.
- `scored_runs_authorized=false`.
- `HCI_CONTROL_ACTIONS_ENABLED=false`.

## P6 — final non-scored Golden state

Canonical detailed record:

`docs/WP2_P6_GOLDEN_CLOSURE_2026-08-27.md`

Final P6 experiment:

- UUID: `5579cf25-dbb1-4d04-87e3-ff558e3be2af`;
- name: `wpg7498036`;
- profile: `PowderProfiles/srslte-controlled-rf`;
- profile repository revision: `a6da96560b6526dc6816761282722c996418fd8c`;
- bindings: `enb_node=nuc1`, `ue_node=nuc2`, `ue_type=srsue`;
- original authorized source SHA: `bd1b5e12f3d2eca27ec81ccadbeec5afaa2f2159`;
- valid scientific run: `wp2-p6r-33099648133-20260827T174149Z`;
- scored: **NO**;
- scientific rerun: **NO**;
- second reservation: **NO**.

P6 scientific reconstruction:

- `t_rf_restore=2026-08-27T17:45:06.913285Z`;
- `t_service_ready=2026-08-27T17:45:32.001525Z`;
- `T_service=25.088240 s`;
- `t_app_complete=2026-08-27T17:45:37.295360Z`;
- `T_app=5.293835 s`;
- `T_total=30.382075 s`;
- primary cohort `181`;
- valid by the 300 s horizon `181/181`;
- `completeness_300=1.0`;
- primary-cohort missing/checksum/duplicate/late = `0/0/0/0`.

Evidence survival/finalization:

- `RAW_EVIDENCE_COMPLETE=PASS`;
- persistent `/proj` escrow PASS;
- controller pull PASS;
- deterministic TAR SHA-256 `ff72a50fd11db1d308f4049b49fffa317c8220c9290845434dbadc8dbef847cf`;
- GitHub artifact ID `9658678808`;
- independent artifact read-back + outer/internal SHA-256 PASS;
- teardown confirmed `2026-08-27T18:04:31Z`.

P6 Attempt 1 and later G8/escrow salvage failures remain preserved as infrastructure/provenance evidence. They did not create a second scientific measurement or a second reservation.

## P7 — hardening and authorization decision

Canonical decision:

`docs/WP2_P7_SCORED_AUTHORIZATION_2026-08-27.md`

P7 changed no frozen RF/scientific semantics and contacted no POWDER resource. Accepted reusable-path hardening:

1. management aliases `enb1/rue1` are now manifest-derived and SSH-proven before G0;
2. G8 receiver evidence uses the live-qualified tar-stream transfer instead of `scp .../receiver/.`;
3. planned post-cohort generated traffic is separated from truly unexpected record identities;
4. clock-authority/post-cohort/transport/retirement regressions are executable under the actual `unittest discover` gate.

Bounded P7 offline closure evidence:

- GitHub run `33103997677`;
- job `98628861177`;
- result **SUCCESS**;
- **36/36 tests PASS**;
- Golden offline reconstruction/escrow/interlock QA PASS;
- outer-hash corruption fails closed;
- internal raw-hash corruption fails closed;
- `POWDER_CONTACT=NO`;
- `POWDER_MUTATION=NO`;
- `SCIENTIFIC_RUN=NO`;
- `SCORED_RUN=NO`.

Temporary P7 workflow/trigger were deleted after PASS. Current workflow surface is back to the six standing offline/static workflows and four standing root sentinels documented in `docs/WORKFLOW_REGISTRY.md`.

## P7B-A — offline contract freeze

Canonical closure:

`docs/WP2_P7B_A_OFFLINE_CONTRACT_FREEZE_2026-08-27.md`

- one future reservation and exactly three sequential non-scored S3 cells are frozen: B1, W1, B2;
- fail-closed washout/readiness precedes every cell;
- generator/gateway restart-domain separation, runtime locks, arm-specific acceptance and evidence survival are machine-readable;
- accepted run `33106623492`, job `98638079325`, **41/41 tests PASS**;
- failed formatting assertion run `33106551326` is preserved as QA provenance;
- no POWDER contact, reservation, SSH, mutation, science or scored run occurred;
- workflow surface remains six offline/static workflows and four root sentinels.

## Current pre-score blockers

P7 deliberately did **not** convert offline hardening PASS into scored authorization. Mandatory physical qualification remains open for:

1. B1 accepted/unacknowledged instrumentation on the real remote path;
2. B1/W1 matched runtime/config proof on POWDER;
3. S3 process-restart-domain separation non-scored proof;
4. B2 Eclipse Paho Java 1.2.5 remote runtime/path/restart qualification;
5. full inter-run washout/readiness enforcement for B1/W1/B2;
6. immutable pre-score reproducibility snapshot only after items 1-5 PASS.

Older OPEN labels in `experiments/WP-PWD01/run-matrix.yaml` for remote Paho reproduction, LTE/MQTT path, run/session isolation, W1 physical checksum preservation, clock alignment, deterministic non-scored reconstruction, controller SSH path and evidence-survival transport are superseded by the later physical/non-scored evidence summarized in the P7 decision. **Only the gate-status bookkeeping is superseded; the scientific design, schedules, endpoint definitions, freeze requirements and all still-open gates in the run matrix remain authoritative.**

Do not set `scored_runs_authorized=true` until every still-open mandatory gate closes and the immutable pre-score snapshot is frozen.

## Frozen scientific controls

- Q0/Q1/Q2/Q3 = `0/40/52/55 dB`.
- attenuation IDs `1 33 2 34` remain coupled.
- primary cohort cutoff = `t_rf_restore`.
- `t_rf_restore`, `t_service_ready`, `t_app_complete` remain distinct.
- `H_app=300 s from t_service_ready`.
- primary endpoint = `completeness_300` at `t_service_ready + 300 s`.
- preserve `T_service`, `T_app`, `T_total`.
- no outcome-derived/W1-derived/Golden-derived/scored-derived H re-estimation.
- S2/S3 clean restore order remains frozen.
- H1 remains valid adverse non-scored evidence and is not reopened.
- K1-K8 remain closed absent material interface change.
- negative/null/unfavorable outcomes remain valid evidence and never justify protocol drift.

## Exact next bounded patch — DO NOT START YET

`WP2-P7B-B — OFFLINE IMPLEMENTATION + PREMUTATION COMPATIBILITY/READINESS QA`

Status: **BLOCKED / NOT STARTED pending explicit continuation**.

Implement only the frozen P7B-A contract: separated generator/gateway processes; B1 event reconstruction; W1 durable replay; exact B1/W1 manifest comparison; remote-capable B2 Java adapter; per-cell washout/readiness; deterministic evidence reconstruction; and fail-closed offline QA.

P7B-B remains offline. It grants no authority to contact POWDER, reserve, SSH, mutate the testbed or run a physical cell. After P7B-B PASS, STOP before P7B-C and request separate explicit live authorization.

## Prohibited before separate P7B-C live authorization

- no POWDER contact/reservation/mutation;
- no SSH to POWDER;
- no Golden rerun;
- no H calibration;
- no RF recalibration;
- no B1/W1/B2 scored work;
- no OTA replication;
- no WP3 execution;
- no `scored_runs_authorized=true`;
- no pre-score snapshot claiming authorization while physical gates are open.

## Mandatory read order for next agent

1. `HANDOVER_CURRENT.md`
2. `docs/NEW_AGENT_PROMPT_WP2_P7B_B_2026-08-27.md`
3. `docs/WP2_P7B_A_OFFLINE_CONTRACT_FREEZE_2026-08-27.md`
4. `experiments/WP-PWD01/P7B_PHYSICAL_QUALIFICATION_PLAN_v1.md`
5. `experiments/WP-PWD01/p7b-qualification-contract.json`
6. `docs/WP2_P7_SCORED_AUTHORIZATION_2026-08-27.md`
7. `docs/NEXT_GATE.md`
8. `docs/MILESTONE_STATUS.md`
9. `docs/WP2_P6_GOLDEN_CLOSURE_2026-08-27.md`
10. `evidence/powder/wp2-p6-live-status.md`
11. `experiments/WP-PWD01/PRE_SCORE_P0_AMENDMENT_2026-08-26.md`
12. `experiments/WP-PWD01/PRE_SCORE_P1_AMENDMENT_2026-08-26.md`
13. `experiments/WP-PWD01/run-matrix.yaml`
14. `experiments/WP-PWD01/RECOVERY_SEMANTICS_AMENDMENT_v1.md`
15. `experiments/WP-PWD01/protocol.md`
16. `experiments/WP-PWD01/B2_SEMANTICS_GATE_v1.md`
17. `evidence/local/wp2-b2-semantics-latest.md`
18. `src/wellpulse/transport.py`
19. `src/wellpulse/powder_w1.py`
20. `src/wellpulse/store.py`
21. `scripts/wp2_golden_orchestrator.sh`
22. `scripts/wp2_golden_evidence_escrow.sh`
23. `scripts/wp2_controller_pull_persistent_escrow.sh`
24. `scripts/wp2_controller_verify_artifact_roundtrip.sh`
25. `docs/WORKFLOW_REGISTRY.md`
26. `AGENTS.md`

## Shortest path

`P6 PASS -> P7 hardening PASS -> P7B-A contract PASS -> STOP -> explicit P7B-B offline implementation -> STOP -> separate P7B-C live authorization -> P7B-D/E -> STOP -> immutable snapshot + scored authorization -> WP3 -> WP4 -> WP5`

**STOP / HANDOVER READY — P7B-B OFFLINE ONLY.**
