# WellPulse — Current Handover

Last updated: 2026-08-27 after H1-PSH PSH-1 local provenance/artifact discovery.

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
- H1-PSH local salvage: **ACTIVE**.
- PSH-0 history freeze/search: **PASS; no H1-specific hit**.
- PSH-1 bounded local provenance/artifact discovery: **PASS; no material H1 recovery**.
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

## H1-PSH — Home-PC PowerShell/local provenance salvage

Canonical specification:

`docs/H1_POWERSHELL_HISTORY_SALVAGE_2026-08-27.md`

### PSH-0 — PASS / CLOSED

Canonical result:

`evidence/powder/h1-psh0-history-freeze-result-2026-08-27.md`

Result commit:

`c140d1b4a87f412b38f352ed71bc5cd9d24476c5`

User-returned local evidence reported:

- `PSEdition=Core`
- `PSVersion=7.6.5`
- current-host PSReadLine history: `C:\Users\admino\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt`
- history sources found: `1`
- `ALL_HASH_VERIFICATION=PASS`
- `SOURCE_FILES_MODIFIED=NO`
- `NETWORK_USED=NO`
- total broad keyword hits: `1335`
- high-specificity H1 hits: `0`

Interpretation: the single discovered PSReadLine source was preserved and searched safely but contained no H1-specific anchors. Broad-hit counts were noise from generic terms.

### PSH-1 — PASS / CLOSED

Canonical result:

`evidence/powder/h1-psh1-local-discovery-result-2026-08-27.md`

Result commit:

`1f0398fab2b4dcdd5668e8d8e74bf59d201a0618`

User-returned PSH-1 bundle reported:

- runtime: PowerShell Core `7.6.5`
- network used: NO
- source mutation: NO
- temp included: NO
- root count: `8`
- candidate files: `9`
- transcript files: `0`
- high-specificity content hits: `43`
- exact known-hash matches: `0`
- errors: none

Interpretation:

- All nine candidate files were unrelated false positives from other projects/packages.
- All 43 high-specificity content hits came from the PSH-0/PSH-1 salvage scripts themselves and are excluded as recovery evidence.
- No PowerShell transcript was discovered in the scanned roots.
- No file matched any known H1/recovery/reproducibility archive SHA-256.
- The scanned roots included `E:\` because the resolved Desktop root on this PC mapped there, so the negative result is stronger than a Downloads-only check.

Scientific consequence: PSH-1 recovered no H1 raw bytes. H1 remains `VALID_W1_RECOVERY_FAILURE`; `H=UNFROZEN`; RS-1 remains blocked.

### PSH-2 — NEXT / NOT STARTED

Purpose: targeted **provenance-source recovery**, not another generic file scan.

Allowed targets only:

- Windows Terminal local state/session provenance;
- PowerShell transcript configuration/registry evidence and any non-default transcript destinations;
- OpenSSH/SSH/SCP client traces or known-host/session metadata that may reveal the actual operating path;
- Windows Recent Items / Jump Lists / shell-link provenance around 2026-08-26;
- filesystem metadata for files created/modified around the H1 execution window on likely user drives;
- command/shell artifacts outside PSReadLine if a concrete Windows mechanism supports them.

Mandatory PSH-2 contract:

1. local-only, read-only;
2. no network, POWDER, GitHub, SSH, SCP, SFTP, rclone, cloud, or API contact;
3. no installs or system configuration changes;
4. do not repeat the same full filename/content scan from PSH-1;
5. target provenance mechanisms and the 2026-08-26 time window;
6. preserve/hash any discovered provenance source before analysis where practical;
7. never commit credentials, private keys, tokens, or secret-bearing session material;
8. treat path/session evidence as provenance unless original artifact bytes are recovered;
9. if an H1 candidate file/path is found, stop broad discovery and move to targeted hash verification only;
10. do not reopen RS-1 without sufficient legitimate raw bytes.

Possible final H1-PSH outcomes remain:

- `PASS_FULL_RAW_RECOVERED`
- `PASS_PARTIAL`
- `CLOSED_NO_RECOVERY`

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
2. `docs/H1_POWERSHELL_HISTORY_SALVAGE_2026-08-27.md`
3. `evidence/powder/h1-psh1-local-discovery-result-2026-08-27.md`
4. `evidence/powder/h1-psh0-history-freeze-result-2026-08-27.md`
5. `evidence/powder/h1-github-salvage-2026-08-27.md`
6. `evidence/powder/h1-github-salvage-manifest-2026-08-27.json`
7. `docs/NEXT_GATE.md`
8. `docs/WORKFLOW_REGISTRY.md`
9. `docs/REPOSITORY_HYGIENE_FINAL_QA_2026-08-27.md`
10. `AGENTS.md`
11. `docs/PRE_INTEGRATION_COMPATIBILITY_GATE.md`
12. `docs/GITHUB_POWDER_COMPATIBILITY_MATRIX_2026-08-27.md`
13. `docs/LIVE_EXPERIMENT_HCI_AND_RAW_EVIDENCE.md`
14. `experiments/WP-PWD01/GOLDEN_E2E_REHEARSAL_v1.md`
15. `evidence/powder/wp2-h1-valid-recovery-failure-2026-08-26.md`
16. `experiments/WP-PWD01/protocol.md`
17. `experiments/WP-PWD01/evidence-schema.md`

## Exact next action

**STOP after PSH-1 closure.**

On the next explicit user resume, execute exactly one bounded patch:

### PSH-2 — Targeted local provenance-source recovery

Provide the smallest safe PowerShell 7.6.5-compatible read-only script/commands to inspect only Windows Terminal/PowerShell transcript provenance, SSH/OpenSSH local traces, Recent Items/Jump Lists, and time-bounded filesystem metadata around 2026-08-26. Do not repeat the PSH-1 generic filename/content scan. If a concrete H1 path/file appears, stop and verify that target only.

After PSH-2: update this handover with PASS/BLOCKED/result evidence and STOP again.

### Deferred

`K1 — Offline supply-chain/runtime pin closure` remains deferred until H1-PSH is closed or explicitly reprioritized.