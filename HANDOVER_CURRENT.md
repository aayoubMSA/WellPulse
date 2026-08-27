# WellPulse — Current Handover

Last updated: 2026-08-27 after defining the H1-PSH local PowerShell-history salvage subpatch.

## Executive state

- Canonical repository: `aayoubMSA/WellPulse`, branch `main`.
- FIT IoT-LAB scientific layer: **FINAL PASS**.
- POWDER G0–G5 infrastructure/RF qualification: **PASS**.
- RF calibration: **PASS / FROZEN**.
- Recovery-semantics RS-2..RS-7: **PASS / FROZEN**.
- WP2: **ACTIVE — GOLDEN REHEARSAL NOT YET PASSED**.
- Scientific weighted completion: **20%**.
- Repository workflow cleanup: **CLOSED / 100% — C0..C4 PASS**.
- H1 GitHub salvage: **PASS as derived-evidence/provenance consolidation; raw recovery from GitHub failed**.
- New recovery opportunity: **H1-PSH — home-PC PowerShell history salvage, PLANNED / NEXT**.
- `H=UNFROZEN`.
- `scored_runs_authorized=false`.
- `REBOOK_GOLDEN=false`.

## Mandatory patch discipline

All work remains bounded:

`execute exactly one declared patch -> PASS/BLOCKED -> update canonical handover/status -> STOP -> resume only on explicit user instruction`

Never start the next patch before the user explicitly resumes, even when it is offline-only.

## Current scientific frontier

### H1 experiment of record

- Experiment: `WP-HCAL-E`
- UUID: `9153e16a-1eb1-45f5-88bf-303636a9d1ec`
- Profile: `PowderProfiles/srslte-controlled-rf`
- Profile revision: `a6da96560b6526dc6816761282722c996418fd8c`
- Mapping: `enb1 -> nuc1`, `rue1 -> nuc2`
- Exact deployed WellPulse source commit: `95ba9a57bef159450b00b8a439d393d22e1c0519`
- H1 run: `wp2h1-a1-20260826-001`
- Scored: **NO**
- Frozen classification: `VALID_W1_RECOVERY_FAILURE`

H1 must never be replaced or reclassified.

### H1 surviving high-level record

- Q0/Q1/Q2/Q3: `0/40/52/55 dB`; attenuator IDs `1 33 2 34` remain coupled.
- Q3 full-state duration: `120.000117905 s`.
- RF restoration / primary-cohort cutoff: `2026-08-26T18:16:00.428045+00:00`.
- Generated records: `361`.
- Primary cohort: `211`.
- Final pending: `270`.
- Application inflight: `20`.
- Publish calls: `111`.
- PUBACK callbacks: `91`.
- Q0 pre-readiness: `5/5` ping PASS through `tun_srsue`.
- Post-restoration health: `0/3` ping.
- Sender status: `STOP_AND_INVESTIGATE_H_WOULD_EXCEED_300S`.
- Sender rc: `20`.

These are Git-native derived/live-captured summaries, not a substitute for the missing record-level corpus.

### H1 failure localization and recovery characterization

Preserved evidence indicates RF/eNB recovery while the LTE user plane remained unusable. EPC/MME/SPGW showed stale/session-context/IP continuity pathology. This does **not** demonstrate WellPulse durable-queue failure; H1 remains a valid W1 recovery failure because required user-plane recovery did not occur inside the frozen bound.

Recovery characterization:

- UE-only restart: **FAIL**.
- EPC/eNB reset while UE remained running: core/RAN reset PASS; user-plane recovery **FAIL**.
- Clean ordered recovery `stop UE -> EPC -> eNB -> fresh UE`: **PASS**.
- After clean-order recovery: 10/10 Q0 packets, 0% loss.
- Full LTE/TLS/MQTT v3.1.1/QoS1 application path then passed **3/3 fresh sessions**, including payload SHA-256 equality.

This recovery procedure is operational/testbed knowledge only; it does not retroactively repair H1 or authorize scored work.

## H1 GitHub salvage — CLOSED

Canonical artifacts:

- `evidence/powder/h1-github-salvage-2026-08-27.md`
  - creation commit `a3cccf1cb6999e213ac47da681ecc31c0cd4fc6e`
  - evidence class `DERIVED_GIT_GITHUB_SALVAGE`
- `evidence/powder/h1-github-salvage-manifest-2026-08-27.json`
  - creation commit `e438e910a80495bc76351def6c6080fb6aa2cb60`
  - schema `wellpulse.h1-github-salvage.v1`

Verdict:

- `H1_GITHUB_SALVAGE=PASS`
- `H1_FULL_RAW_FROM_GITHUB=NOT_RECOVERED`
- `H1_DERIVED_LOG_EVIDENCE=AVAILABLE`
- `H1_RECORD_LEVEL_RECONSTRUCTION_FROM_GITHUB=BLOCKED`
- `RS1_RAW_RECONSTRUCTION=BLOCKED_ON_RAW_BUNDLES`

Negative recovery checks:

- H1 classification commit `9cd7789a8960fd396ba35806127c16251ea8574a`: 0 associated Actions workflow runs.
- H1 archive-hash commit `375f767bae237729458f558b1c64c60633c00673`: 0 associated Actions workflow runs.
- Pre-H live SSH workflow run `32993568290`: 0 uploaded Actions artifacts.
- `data/raw/`: only `.gitkeep`.
- `results/runs/`: only `.gitkeep`.

Historical `/users/aayoub/...` storage was later determined non-durable for the teardown lifecycle. Historical files remain unchanged as provenance, but the current lifecycle interpretation supersedes the old persistence characterization.

Known historical H1 archive hashes remain integrity anchors:

- nuc1 H1 archive: `3e3d4c44847bfb7e6304de89d8c1cc05ff9722b6a54d93dd08ce0acfa7418210`
- nuc2 H1 archive: `c5d3b212af015061c092c79025258a7f3378e3351051eef48318f12964af2593`
- nuc1 recovery archive: `71aaea25a50ad955fa797a358b14cce4efc0e76ec0861468b3b99dd224c7dd55`
- nuc2 recovery archive: `431855c8662fa46a82f7baca60b5f3deeda4fd849cf4d90bfc4889800be3e71d`
- nuc1 runtime record: `1ef8b04a8d3a634c1cc3ded2b84c80a7140d877758a0d63010411971eab8607f`
- nuc2 runtime record: `fc1c131602c49b8376733ad8e190c4fc5d8d1976b62fe59c1e5becbe41cf8d5a`
- nuc1 reproducibility archive: `af601716237082be410be3680f1e33b36240beae77e7b644f0f5bef811c1b647`
- nuc2 reproducibility archive: `ada35310a2dd46dba6c28a26604d41f28884799e0fc27c0846a7bf66421935bc`
- nuc1 chain-of-custody manifest: 22 files, `9596f23f4e9359d3395f29f6e0081d5acdec05dc6a986c0e0b0f19ac5fa35811`
- nuc2 chain-of-custody manifest: 34 files, `343a9deb1e432c0f5d30cbf55def3d133726a214a595d9f7f0723a5e87d8ec2e`

## H1-PSH — Home-PC PowerShell History Salvage — NEXT

Canonical subpatch specification:

`docs/H1_POWERSHELL_HISTORY_SALVAGE_2026-08-27.md`

Creation commit:

`35e528493a9ec1c33d9e1a14fa093ab6d38bf48a`

### Rationale

The H1 experiment was operated from the user's home PC through PowerShell. The local PowerShell/terminal history may retain exact H1 commands, local transfer destinations, archive/file paths, hashes, or references to local copies that are absent from GitHub and unavailable on the destroyed POWDER nodes.

This path has higher immediate scientific ROI than K1 supply-chain pinning because it may recover the missing H1 raw bytes or identify where they were copied.

### Evidence boundary

PowerShell history is initially **provenance/recovery evidence**, not scientific raw data. A command appearing in history does not prove it succeeded.

H1-PSH must begin read-only:

1. determine the actual PowerShell history path(s), preferably from `(Get-PSReadLineOption).HistorySavePath` rather than guessing;
2. preserve original history files byte-for-byte before analysis;
3. compute SHA-256 and record path/size/timestamp/version metadata;
4. search a preserved copy for H1 anchors;
5. inspect any candidate local artifact destinations read-only;
6. hash recovered files and compare against known H1 archive/hash anchors;
7. quarantine/redact secret-bearing material and never commit credentials/tokens/private keys;
8. classify recovered objects as raw bytes, transcript, command history, derived local output, provenance pointer, or secret-bearing quarantine;
9. never alter H1's frozen `VALID_W1_RECOVERY_FAILURE` classification.

High-value search anchors include:

- `WP-HCAL-E`
- `wp2h1-a1-20260826-001`
- `9153e16a-1eb1-45f5-88bf-303636a9d1ec`
- `nuc1`, `nuc2`
- `wellpulse-powder-evidence`
- `wp2-h1-valid-failure-20260826`
- `sender_summary.json`
- `calibration_manifest.json`
- `attenuation_timeline.csv`
- `telemetry_generated.csv`
- `queue_timeline.csv`
- `mqtt_events.jsonl`
- `w1_queue.sqlite`
- `SHA256SUMS`, `tar.gz`, `scp`, `sftp`, `rclone`
- the two original H1 archive SHA-256 values.

Possible H1-PSH outcomes:

- `PASS_FULL_RAW_RECOVERED` — original/independently verifiable record-level H1 corpus recovered;
- `PASS_PARTIAL` — useful raw subset, transcript, commands, or provenance path recovered;
- `CLOSED_NO_RECOVERY` — history preserved/searched correctly but no material evidence recovered.

If full or partial raw bytes are recovered, verify hashes/provenance before re-opening any RS-1 reconstruction subtask. Do not infer record-level science from command history alone.

## RS-1 status

`docs/RS1_OFFLINE_RECONSTRUCTION.md` remains methodologically valid, but GitHub alone cannot currently supply its required raw artifacts, including sender CSV/JSON/SQLite files, receiver raw events/identities, and full LTE/EPC/eNB/UE logs.

RS-1A..RS-1E remain blocked **unless H1-PSH or another legitimate source recovers sufficient raw bytes**.

## Golden A3 state

Experiment `WP-GOLDEN-A3`, UUID `357f3275-403d-491a-906f-99677bdf454f`, is expired/removed and must not be reused.

- Attempt 6, run `33067316888`: G0..G6 PASS; G7 `DIAGNOSTIC_NONCANONICAL` because `tmcc attenuator <id>` had mutation semantics (`changing attenuation`); G8/G9/G10 not reached; scored NO.
- Attempt 7, run `33069500256`: static/no-scored and Drive pre-mutation gates passed; stopped before science after A3 returned 404; scored NO.

## Repository hygiene — CLOSED / 100%

- C0 PASS.
- C1 archived expired A3 workflows/triggers; key commit `169b5632d2db20a9cda0ac7cc2633f68b2316024`.
- C2 archived 16 FIT-specific workflows after FINAL FIT PASS; key commit `4d10df3bc6de3492d661d34dee51599452d6eed1`.
- C3 archived 22 historical/live POWDER workflows plus 20 stale trigger/request files; key commit `1cde375d07504567afe78383db3f3eb6a69e46b5`.
- C4 workflow registry/final hygiene QA PASS.
- 50 workflow files removed from the active Actions path while provenance was preserved.
- Exactly six local/offline/static workflows remain active; none contacts live POWDER.
- Historical Actions sidebar entries are audit history, not approved active workflow definitions.

## Mandatory integration and evidence gates

Before any future GitHub Actions <-> POWDER live integration:

`PRE_INTEGRATION_COMPATIBILITY_GATE=PASS`

and

`LIVE_HCI_AND_RAW_EVIDENCE_GATE=PASS`

are mandatory.

Current compatibility status: **BLOCKED**.

No live reservation, live integration, Golden run, H requalification, or scored work is allowed while the relevant gates remain blocked.

Future HCI must remain passive/one-way/non-authoritative with:

`HCI_CONTROL_ACTIONS_ENABLED=false`

Future evidence closeout must require before teardown:

`RAW_EVIDENCE_COMPLETE=PASS`

`EVIDENCE_ESCROW_GATE=PASS`

`TEARDOWN_AUTHORIZED=YES`

Required future sequence:

`freeze writers -> inventory mandatory raw -> hash -> /proj/WellPulse/evidence-escrow/... -> verify -> off-POWDER copy -> read-back/hash verify -> provenance record -> teardown`

## Frozen scientific state

- H1: `VALID_W1_RECOVERY_FAILURE`.
- `H=UNFROZEN`.
- `scored_runs_authorized=false`.
- `REBOOK_GOLDEN=false`.
- Scientific weighted completion: **20%**.
- Recovery-semantics amendment v1 and protocol v0.6 remain frozen.
- Primary cohort cutoff remains `t_rf_restore`.
- Application horizon remains 300 s from `t_service_ready`.
- No scored B1/W1/B2 run is authorized.

## Mandatory current read order

1. `HANDOVER_CURRENT.md`
2. `docs/H1_POWERSHELL_HISTORY_SALVAGE_2026-08-27.md`
3. `evidence/powder/h1-github-salvage-2026-08-27.md`
4. `evidence/powder/h1-github-salvage-manifest-2026-08-27.json`
5. `docs/NEXT_GATE.md`
6. `docs/WORKFLOW_REGISTRY.md`
7. `docs/REPOSITORY_HYGIENE_FINAL_QA_2026-08-27.md`
8. `AGENTS.md`
9. `docs/PRE_INTEGRATION_COMPATIBILITY_GATE.md`
10. `docs/GITHUB_POWDER_COMPATIBILITY_MATRIX_2026-08-27.md`
11. `docs/LIVE_EXPERIMENT_HCI_AND_RAW_EVIDENCE.md`
12. `experiments/WP-PWD01/GOLDEN_E2E_REHEARSAL_v1.md`
13. `evidence/powder/wp2-h1-valid-recovery-failure-2026-08-26.md`
14. `experiments/WP-PWD01/protocol.md`
15. `experiments/WP-PWD01/evidence-schema.md`

## Exact next action

**STOP after insertion of H1-PSH into the canonical workflow.**

On the next explicit user resume, execute exactly one bounded patch:

### H1-PSH — Home-PC PowerShell History Salvage

Do not start K1 first.

Execution must follow `docs/H1_POWERSHELL_HISTORY_SALVAGE_2026-08-27.md`:

`PSH-0 freeze source -> PSH-1 bounded H1 extraction -> PSH-2 local artifact-path recovery -> PSH-3 evidence classification -> PSH-4 reconcile with canonical H1 salvage`

This requires user access to the home PC/PowerShell because ChatGPT does not directly access that local filesystem. The assistant should provide the smallest safe read-only commands, then analyze returned output/files without asking the user to perform unnecessary manual interpretation.

After H1-PSH execution, update this handover with PASS_FULL_RAW_RECOVERED / PASS_PARTIAL / CLOSED_NO_RECOVERY and STOP again.

### Deferred patch

`K1 — Offline supply-chain/runtime pin closure` remains deferred until H1-PSH is closed.

## Handover acceptance test

A replacement agent is ready only if it can state:

- scientific completion remains 20%;
- H1 is permanently `VALID_W1_RECOVERY_FAILURE`; H remains unfrozen;
- GitHub salvage did not recover H1 raw record-level bytes;
- H1-PSH is now the next high-ROI recovery subpatch because H1 was operated from the user's home PC using PowerShell;
- PowerShell history is provenance, not automatically raw evidence;
- recovered local files must be hash/provenance verified before scientific use;
- RS-1 remains blocked unless sufficient legitimate raw bytes are recovered;
- A3 is expired and scored work remains prohibited;
- repository cleanup is closed at 100%;
- Pre-Integration and Live-HCI/Raw-Evidence gates remain mandatory and not passed;
- `scored_runs_authorized=false` and `REBOOK_GOLDEN=false`;
- K1 is deferred until H1-PSH closes;
- every patch must end with a handover update and STOP.