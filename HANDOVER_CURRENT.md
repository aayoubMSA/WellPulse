# WellPulse — Current Handover

Last updated: 2026-08-27 after K1-P2 authoritative Portal API pin closure and offline static validation.

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
- K1 supply-chain/runtime pin closure: **PASS**.
- `H=UNFROZEN`.
- `scored_runs_authorized=false`.
- `REBOOK_GOLDEN=false`.

## Mandatory patch discipline

`execute exactly one declared patch -> PASS/BLOCKED -> update canonical handover/status -> STOP -> resume only on explicit user instruction`

Never start the next patch before explicit user resume/continue.

## Workstation-independence rule

Home and work PCs are interchangeable operator terminals only. No future Golden/scored execution may depend on workstation-local history, downloads, unique filesystem state, or workstation-local experiment authority. Canonical control state remains GitHub + frozen repository state + GitHub Actions/secrets. One-time local bootstrap/capture steps may establish immutable provenance but are not part of normal experiment execution.

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

## H1 evidence salvage — CLOSED

### GitHub salvage

- `H1_GITHUB_SALVAGE=PASS`
- `H1_FULL_RAW_FROM_GITHUB=NOT_RECOVERED`
- `H1_DERIVED_LOG_EVIDENCE=AVAILABLE`
- `H1_RECORD_LEVEL_RECONSTRUCTION_FROM_GITHUB=BLOCKED`
- `RS1_RAW_RECONSTRUCTION=BLOCKED_ON_RAW_BUNDLES`

Canonical artifacts:

- `evidence/powder/h1-github-salvage-2026-08-27.md`
- `evidence/powder/h1-github-salvage-manifest-2026-08-27.json`

### Home-PC PowerShell/local provenance salvage

Canonical result records:

- `evidence/powder/h1-psh0-history-freeze-result-2026-08-27.md`
- `evidence/powder/h1-psh1-local-discovery-result-2026-08-27.md`
- `evidence/powder/h1-psh2-targeted-provenance-result-2026-08-27.md`

Final verdict:

- `H1_POWERSHELL_SALVAGE=CLOSED_NO_RECOVERY`
- `H1_FULL_RAW_FROM_HOME_PC=NOT_RECOVERED`
- `H1_MATERIAL_LOCAL_PROVENANCE_LEAD=NONE`
- `RS1_RAW_RECONSTRUCTION=BLOCKED_ON_RAW_BUNDLES`

Do not expand into forensic recovery unless a genuinely new evidence source appears.

## K1 — Offline supply-chain/runtime pin closure — PASS

Canonical records:

- `docs/K1_SUPPLY_CHAIN_RUNTIME_PIN_CLOSURE_2026-08-27.md`
- `docs/K1P_PORTAL_API_REVISION_RESOLUTION_2026-08-27.md` — historical blocked attempt retained as provenance.
- `docs/K1P2_PORTAL_API_PIN_CLOSURE_2026-08-27.md` — final PASS closure.

Verdict:

`K1=PASS`

Closed K1 contracts:

1. `actions/checkout@11d5960a326750d5838078e36cf38b85af677262` for the pre-integration/future integration contract.
2. Explicit pre-integration runner label `ubuntu-24.04`.
3. uv `0.12.1`, archive `uv-x86_64-unknown-linux-gnu.tar.gz`, SHA-256 `90b2f223fb69d19db49e117da601f64978593417988530aa733d456141b4bcbb`.
4. rclone `1.75.0`, Linux amd64 ZIP SHA-256 `aa2804e08f48250e71009c727124b6341cd0288465804a9a09d14663cabafbaa`.
5. Authoritative Portal API repository `https://gitlab.flux.utah.edu/emulab/portal-api.git` pinned to revision `01be03b2f60c067815a7654437320dd981ca3617`.
6. Portal API capture archive provenance SHA-256 `3e9f0073b2df6840801baa38333f1f04debd02a2eaa57997939b6f7ee678d4c8`, size `1003520` bytes.
7. Accepted future Portal bootstrap: `scripts/wp2_portal_client_bootstrap.sh`; implementation commit `4a88d439b4084f0f0155a94166304150018e2fac`.
8. Portal-pin static fail-close implementation commit `76aa56c202d66b12ec7bf9239b2177c2007da73e`.
9. Offline static validation trigger commit `479459d801e4b08e438eb1aa793a5c747121fe3b`; workflow run `33081196297` completed `success`.

K1 does **not** close the whole compatibility gate.

## Compatibility / Golden state

Experiment `WP-GOLDEN-A3` is expired/removed and must not be reused.

- Attempt 6: G0..G6 PASS; G7 `DIAGNOSTIC_NONCANONICAL` due mutating `tmcc attenuator <id>` semantics; scored NO.
- Attempt 7: stopped before science after A3 returned 404; scored NO.

Before any future GitHub Actions <-> POWDER live integration both remain mandatory:

`PRE_INTEGRATION_COMPATIBILITY_GATE=PASS`

`LIVE_HCI_AND_RAW_EVIDENCE_GATE=PASS`

Current compatibility status: **BLOCKED**.

Remaining material compatibility blockers include:

- dedicated Google Drive OAuth + write/read/hash verification;
- Portal lifecycle/status/error/expiry semantics;
- exact live OpenSSL/Mosquitto/runtime fingerprints;
- fresh receiver detach/launch-time proof;
- authoritative reservation-expiry semantics feeding the time guard;
- `/proj/WellPulse` live write/read/hash validation;
- observation semantics closure for any live RF-status mechanism.

No live reservation, Golden run, H requalification, or scored work is authorized.

Future HCI remains passive/one-way/non-authoritative:

`HCI_CONTROL_ACTIONS_ENABLED=false`

Before teardown of every future live experiment require:

`RAW_EVIDENCE_COMPLETE=PASS`

`EVIDENCE_ESCROW_GATE=PASS`

`TEARDOWN_AUTHORIZED=YES`

Required evidence path:

`freeze writers -> inventory mandatory raw -> hash -> /proj/WellPulse/evidence-escrow/... -> verify -> off-POWDER copy -> read-back/hash verify -> provenance record -> teardown`

## Repository hygiene — CLOSED / 100%

- C0..C4 PASS.
- 50 workflow files removed from active Actions path with provenance retained.
- Exactly six local/offline/static workflows remain active; none contacts live POWDER.

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
2. `docs/K1P2_PORTAL_API_PIN_CLOSURE_2026-08-27.md`
3. `docs/K1_SUPPLY_CHAIN_RUNTIME_PIN_CLOSURE_2026-08-27.md`
4. `docs/GITHUB_POWDER_COMPATIBILITY_MATRIX_2026-08-27.md`
5. `docs/PRE_INTEGRATION_COMPATIBILITY_GATE.md`
6. `evidence/powder/h1-psh2-targeted-provenance-result-2026-08-27.md`
7. `evidence/powder/h1-github-salvage-2026-08-27.md`
8. `evidence/powder/h1-github-salvage-manifest-2026-08-27.json`
9. `docs/NEXT_GATE.md`
10. `docs/WORKFLOW_REGISTRY.md`
11. `docs/REPOSITORY_HYGIENE_FINAL_QA_2026-08-27.md`
12. `AGENTS.md`
13. `docs/LIVE_EXPERIMENT_HCI_AND_RAW_EVIDENCE.md`
14. `experiments/WP-PWD01/GOLDEN_E2E_REHEARSAL_v1.md`
15. `evidence/powder/wp2-h1-valid-recovery-failure-2026-08-26.md`
16. `experiments/WP-PWD01/protocol.md`
17. `experiments/WP-PWD01/evidence-schema.md`

## Exact next action

**STOP after K1 closure.**

On the next explicit user resume, execute exactly one bounded patch:

### K2 — Auth / Drive transport contract closure

Goal:

Replace the shared rclone Google Drive OAuth client dependency with a dedicated OAuth/client contract suitable for unattended GitHub-Actions-driven evidence escrow, then perform a disposable write → read/list → hash/byte equality → delete verification without contacting POWDER.

Constraints:

- no POWDER reservation or live experiment contact;
- no scientific run;
- secrets remain in GitHub Secrets / approved local one-time bootstrap only, never committed;
- workstation independence is mandatory for normal operation;
- fail closed if a dedicated unattended Drive transport cannot be established and verified.

After K2: update canonical handover/status and STOP again.
