# WellPulse — Current Handover

Last updated: 2026-08-27 after closure of H1-PSH local PowerShell/provenance salvage.

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
- H1-PSH local salvage: **CLOSED_NO_RECOVERY**.
- `H=UNFROZEN`.
- `scored_runs_authorized=false`.
- `REBOOK_GOLDEN=false`.

## Mandatory patch discipline

`execute exactly one declared patch -> PASS/BLOCKED -> update canonical handover/status -> STOP -> resume only on explicit user instruction`

Never start the next patch before explicit user resume/continue.

## H1 experiment of record

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

## H1 surviving high-level record

- Q0/Q1/Q2/Q3: `0/40/52/55 dB`; attenuation IDs `1 33 2 34` remain coupled.
- Q3 full-state duration: `120.000117905 s`.
- RF restoration / primary-cohort cutoff: `2026-08-26T18:16:00.428045+00:00`.
- Generated records: `361`.
- Primary cohort records: `211`.
- Final pending: `270`.
- Application inflight: `20`.
- Publish calls: `111`.
- PUBACK callbacks: `91`.
- Q0 pre-readiness: `5/5` ping PASS through `tun_srsue`.
- Post-restoration health: `0/3` ping.
- Sender status: `STOP_AND_INVESTIGATE_H_WOULD_EXCEED_300S`.
- Sender rc: `20`.

These survive as Git-native derived/live-captured summaries, not record-level raw evidence.

## H1 failure localization / recovery

Preserved evidence localizes the dominant H1 non-recovery below the WellPulse application layer in LTE core/session-context/IP continuity behavior. RF/eNB recovery occurred, while EPC/MME/SPGW showed stale/session-context churn. This does not demonstrate a WellPulse durable-queue failure.

Recovery characterization remains:

- UE-only restart: **FAIL**.
- EPC/eNB reset with UE left running: reset PASS; Q0/user-plane recovery **FAIL**.
- Clean ordered recovery `stop UE -> EPC -> eNB -> fresh UE`: **PASS**.
- Post-recovery Q0: 10/10 packets, 0% loss.
- Full LTE/TLS/MQTT v3.1.1/QoS1 application path: **3/3 fresh sessions PASS** with payload hash equality.

This is operational recovery knowledge only and does not retroactively repair H1.

## H1 GitHub salvage — CLOSED

Canonical artifacts:

- `evidence/powder/h1-github-salvage-2026-08-27.md`
- `evidence/powder/h1-github-salvage-manifest-2026-08-27.json`

Verdict:

- `H1_GITHUB_SALVAGE=PASS`
- `H1_FULL_RAW_FROM_GITHUB=NOT_RECOVERED`
- `H1_DERIVED_LOG_EVIDENCE=AVAILABLE`
- `H1_RECORD_LEVEL_RECONSTRUCTION_FROM_GITHUB=BLOCKED`
- `RS1_RAW_RECONSTRUCTION=BLOCKED_ON_RAW_BUNDLES`

Historical H1 archive SHA-256 anchors remain preserved, but the archive bytes are unavailable from GitHub/current user-accessible POWDER storage.

## H1-PSH — Home-PC PowerShell/local provenance salvage — CLOSED

Canonical specification:

`docs/H1_POWERSHELL_HISTORY_SALVAGE_2026-08-27.md`

Canonical result records:

- `evidence/powder/h1-psh0-history-freeze-result-2026-08-27.md`
- `evidence/powder/h1-psh1-local-discovery-result-2026-08-27.md`
- `evidence/powder/h1-psh2-targeted-provenance-result-2026-08-27.md`

### PSH-0 — PASS / CLOSED

- PowerShell Core `7.6.5`.
- Current-host PSReadLine history preserved and hash-verified.
- One history source found.
- Source mutation: NO.
- Network: NO.
- High-specificity H1 hits: `0`.

### PSH-1 — PASS / CLOSED

- Eight bounded roots scanned.
- Candidate files: `9`, all unrelated false positives.
- Transcript files: `0`.
- High-specificity content hits: `43`, all self-generated salvage-script references and excluded from evidence.
- Exact known H1/recovery/reproducibility archive hash matches: `0`.
- No source mutation or network use.

### PSH-2 — PASS / CLOSED

Final low-cost provenance attempt, bounded to Windows mechanisms and the H1 date window:

- PowerShell event H1 hits: `0`.
- Transcripts with H1 anchor: `0`.
- Recent Items with H1 anchor: `0`.
- Shell/SSH prefetch entries in the window: `8`, metadata only.
- `MATERIAL_H1_PROVENANCE_LEAD=False`.
- No network, system mutation, disk forensics, USN journal, undelete, or recovery tooling.

### Final H1-PSH verdict

- `H1_POWERSHELL_SALVAGE=CLOSED_NO_RECOVERY`
- `H1_FULL_RAW_FROM_HOME_PC=NOT_RECOVERED`
- `H1_MATERIAL_LOCAL_PROVENANCE_LEAD=NONE`
- `RS1_RAW_RECONSTRUCTION=BLOCKED_ON_RAW_BUNDLES`

Per the predeclared kill gate, do not expand into forensic recovery, registry carving, USN journal analysis, undelete utilities, or additional full-disk scans. This lane is closed unless a genuinely new external evidence source appears later.

H1 remains permanently `VALID_W1_RECOVERY_FAILURE`. No scientific completion credit is added.

## Repository hygiene — CLOSED / 100%

- C0 PASS.
- C1 expired A3 workflow/trigger archival PASS.
- C2 16 FIT-specific workflows archived after FINAL FIT PASS.
- C3 22 historical/live POWDER workflows + 20 stale trigger/request files archived.
- C4 Workflow Registry + final hygiene QA PASS.
- 50 workflow files removed from active Actions path with provenance retained.
- Exactly six local/offline/static workflows remain active; none contacts live POWDER.

## Golden / compatibility state

Experiment `WP-GOLDEN-A3` is expired/removed and must not be reused.

- Attempt 6: G0..G6 PASS; G7 `DIAGNOSTIC_NONCANONICAL` due mutating `tmcc attenuator <id>` semantics; scored NO.
- Attempt 7: stopped before science after A3 returned 404; scored NO.

Before any future GitHub Actions <-> POWDER live integration both remain mandatory:

`PRE_INTEGRATION_COMPATIBILITY_GATE=PASS`

`LIVE_HCI_AND_RAW_EVIDENCE_GATE=PASS`

Current compatibility status: **BLOCKED**.

No live reservation, Golden run, H requalification, or scored work is authorized.

Future HCI remains passive/one-way/non-authoritative:

`HCI_CONTROL_ACTIONS_ENABLED=false`

Before teardown of every future live experiment require:

`RAW_EVIDENCE_COMPLETE=PASS`

`EVIDENCE_ESCROW_GATE=PASS`

`TEARDOWN_AUTHORIZED=YES`

Required evidence path:

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
2. `evidence/powder/h1-psh2-targeted-provenance-result-2026-08-27.md`
3. `evidence/powder/h1-psh1-local-discovery-result-2026-08-27.md`
4. `evidence/powder/h1-psh0-history-freeze-result-2026-08-27.md`
5. `docs/H1_POWERSHELL_HISTORY_SALVAGE_2026-08-27.md`
6. `evidence/powder/h1-github-salvage-2026-08-27.md`
7. `evidence/powder/h1-github-salvage-manifest-2026-08-27.json`
8. `docs/NEXT_GATE.md`
9. `docs/WORKFLOW_REGISTRY.md`
10. `docs/REPOSITORY_HYGIENE_FINAL_QA_2026-08-27.md`
11. `AGENTS.md`
12. `docs/PRE_INTEGRATION_COMPATIBILITY_GATE.md`
13. `docs/GITHUB_POWDER_COMPATIBILITY_MATRIX_2026-08-27.md`
14. `docs/LIVE_EXPERIMENT_HCI_AND_RAW_EVIDENCE.md`
15. `experiments/WP-PWD01/GOLDEN_E2E_REHEARSAL_v1.md`
16. `evidence/powder/wp2-h1-valid-recovery-failure-2026-08-26.md`
17. `experiments/WP-PWD01/protocol.md`
18. `experiments/WP-PWD01/evidence-schema.md`

## Exact next action

**STOP after H1-PSH closure.**

On the next explicit user resume, return to the main mission and execute exactly one bounded patch:

### K1 — Offline supply-chain/runtime pin closure

K1 was deferred only while H1-PSH was active and is now the next offline main-path patch.

K1 scope remains strictly offline:

1. inventory moving references in the future Golden/integration path;
2. freeze GitHub Actions to immutable SHAs where applicable;
3. freeze exact Portal API client upstream revision;
4. freeze `uv` and bootstrap tool versions/checksums;
5. verify rclone exact-version/checksum contract;
6. extend static acceptance so moving/unpinned references fail closed;
7. update the compatibility matrix only for evidence actually closed offline.

K1 must NOT contact POWDER, reserve, probe live, or claim the whole compatibility gate PASS.

After K1: update the handover/status and STOP again.
