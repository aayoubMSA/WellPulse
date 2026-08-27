# WellPulse — Current Handover

Last updated: 2026-08-27 after **AUDIT-R1 offline pre-Golden reconciliation PASS and final offline QA review**.

## Executive state

- Canonical repository: `aayoubMSA/WellPulse`, branch `main`.
- Last accepted checkpoint: **AUDIT-R1 PASS / CLOSED / STOPPED**.
- Scientific weighted completion: **20%**.
- WP0: **PASS**, 8/8.
- WP1: **PASS / FROZEN**, 12/12.
- WP2: **ACTIVE**.
- WP3: **BLOCKED ON WP2**, 0/30.
- WP4: **BLOCKED**, 0/15.
- WP5: **PREPARED / NOT EXECUTED**, 0/20.
- FIT IoT-LAB layer: **FINAL PASS**.
- POWDER G0–G5: **PASS**.
- RF calibration: **PASS / FROZEN**.
- K1–K8 compatibility series: **PASS / CLOSED**.
- `PRE_INTEGRATION_COMPATIBILITY_GATE=PASS`.
- `AUDIT_R1=PASS`.
- `LIVE_HCI_AND_RAW_EVIDENCE_GATE=BLOCKED_NOT_STARTED`.
- `REBOOK_GOLDEN=false`.
- `scored_runs_authorized=false`.
- `HCI_CONTROL_ACTIONS_ENABLED=false`.

AUDIT-R1 acceptance: **100/100**. It earns no additional scientific WP credit; scientific weighted completion remains **20%** until WP2 closes.

## Canonical closure records

Audit + AUDIT-R1 closure:

`docs/PROJECT_AUDIT_HANDOVER_2026-08-27.md`

Canonical supersession map:

`docs/AUDIT_R1_SUPERSESSION_MAP_2026-08-27.md`

Workflow deactivation provenance:

`docs/AUDIT_R1_WORKFLOW_DEACTIVATION_2026-08-27.md`

Current next-gate record:

`docs/NEXT_GATE.md`

## AUDIT-R1 closure summary

All mandatory P0 audit inconsistencies were reconciled **offline only**.

### A1 — analysis semantics — PASS — 30/30

Current operational analysis artifacts agree with Recovery Semantics Amendment v1:

- primary cohort cutoff = `t_rf_restore`;
- fixed application observation horizon = `t_service_ready + 300 s`;
- primary endpoint = `completeness_300`;
- preserve separate `T_service`, `T_app`, `T_total`;
- no outcome-derived/W1-derived H re-estimation.

The old H-calculation path is fail-closed rather than silently reusable.

### A2 — evidence contract — PASS — 20/20

Mandatory teardown-critical path is:

`POWDER raw -> /proj/WellPulse persistent escrow -> controller pull -> GitHub Actions artifact -> independent controller download/read-back -> outer + internal SHA-256 verification -> teardown authority`

Google Drive/rclone is optional secondary only.

Persistent escrow emits the controller-handoff marker required by controller verification and remains fail-closed:

- `PERSISTENT_ESCROW_GATE=PASS`;
- `CONTROLLER_OFFPOWDER_REQUIRED`;
- `TEARDOWN_AUTHORIZED=NO` until controller round-trip verification.

Only successful controller/artifact verification may emit:

- `CONTROLLER_OFFPOWDER_GATE=PASS`;
- `EVIDENCE_ESCROW_GATE=PASS`;
- `TEARDOWN_AUTHORIZED=YES`.

### A3 — workflow/governance control — PASS — 20/20

Current active GitHub Actions surface is exactly **6** offline/static workflows:

1. `local-gate-once.yml`
2. `local-unit-tests.yml`
3. `wp2-b2-semantics.yml`
4. `wp2-golden-offline-qa.yml`
5. `wp2-offpowder-artifact-qa.yml`
6. `wp2-preintegration-static.yml`

Exactly **4** root sentinels remain:

- `.local-gate-trigger`
- `.wp2-b2-semantics-trigger`
- `.wp2-offpowder-artifact-qa-trigger`
- `.wp2-preintegration-static-trigger`

Completed K live/diagnostic workflows and the obsolete H-preflight workflow are no longer active. Historical content remains preserved in Git history and the canonical K closure record. Do not re-enable these historical workflows or their trigger paths without a new compatibility review and explicit authorization.

### A4 — provenance/supersession — PASS — 15/15

Historical status/readiness/old-H material is preserved but cannot override current authority. In particular:

- old `H=UNFROZEN` / future H-calibration instructions are superseded;
- old `RESERVE=true` is superseded;
- Drive-critical teardown instructions are superseded;
- original H1 raw bundles must not be represented as recovered;
- old decision text D-017 and old horizon-selection portions of D-019 are historical only where superseded by Recovery Semantics Amendment v1.

### A5 — offline QA + canonical closure — PASS — 15/15

Current runtime acceptance evidence:

- `Local Unit Tests` Actions run `33092273688`: **SUCCESS** on commit `bc42add0a3e1ea58f7c5f4d88055ba8587fbd9a7`.
- **33/33 tests PASS** under Python 3.12.14 / `paho-mqtt==2.1.0`.
- Tests explicitly verify `H_app=300`, anchor=`t_service_ready`, `completeness_300`, inconsistent/non-300 horizons rejected, and the historical H finalizer/CLI fail closed with outcome-derived H re-estimation prohibited.
- `WP2 Off-POWDER Artifact Transport QA` Actions run `33092849805`: **SUCCESS** on commit `4f0d94d3e8c02284c5d92c80a0c1260f91701b51`.
- Artifact ID `9655099849`; deterministic round-trip TAR SHA-256 `1a5c78b3ff588cef38338d12b7891793aca8f436f312c501b5712bb74d423605`.
- Artifact QA verified independent upload/download byte equality and internal raw SHA-256 manifest; it logged `POWDER_CONTACT=NO`, `DRIVE_CONTACT=NO`, `SCIENTIFIC_RUN=NO`.
- The current `scripts/wp2_golden_offline_qa.sh` was statically reviewed after reconciliation: it exercises synthetic Golden reconstruction, persistent escrow + `CONTROLLER_OFFPOWDER_REQUIRED`, controller round-trip verification, outer-hash corruption fail-closed, and internal raw-hash corruption fail-closed. A connector-created no-op trigger did not dispatch a new Actions run and is **not counted as runtime evidence**; the no-op trigger stamps were removed.
- Historical Golden Offline QA run `33014162397` remains prior regression evidence only; it is not represented as current-controller-contract runtime acceptance.
- Current workflow/trigger surface was re-enumerated after cleanup: 6 workflows / 4 root sentinels, zero active K/H-calibration execution surface.

No POWDER contact, reservation, SSH, Golden run, H calibration, scored run, RF recalibration, K reopening, or H1 salvage occurred during AUDIT-R1.

## Governing scientific state — frozen

Recovery Semantics Amendment v1 remains authority:

- `t_rf_restore`, `t_service_ready`, `t_app_complete` are distinct;
- primary cohort = valid records generated at or before `t_rf_restore`;
- **`H_app=300 s from t_service_ready`** is prospectively frozen;
- primary endpoint = `completeness_300` at `t_service_ready + 300 s`;
- preserve `T_service`, `T_app`, `T_total`;
- S2/S3 clean ordered restore = `stop UE -> EPC -> eNB -> fresh UE -> architecture-blind service-ready probe`;
- Golden G6 qualification bound = 120 s;
- negative/null outcomes remain valid scientific evidence;
- W1/Golden/scored outcome-driven H changes are prohibited.

Q0/Q1/Q2/Q3 remain `0/40/52/55 dB`; attenuation IDs `1 33 2 34` remain coupled. Do not reopen RF calibration.

## Protocol v0.6.1

Current protocol:

`experiments/WP-PWD01/protocol.md`

The advisory pre-reservation resource-availability check remains **future-only**:

`https://www.powderwireless.net/resinfo.php`

Immediately before a later authorized booking attempt, record `PASS|DEFER|UNKNOWN`. Never silently change frozen nodes/hardware/profile to chase capacity. Portal lifecycle/READY/manifest remains authoritative.

AUDIT-R1 did not contact this page or POWDER.

## H1 — frozen adverse experiment of record

- experiment `WP-HCAL-E`;
- UUID `9153e16a-1eb1-45f5-88bf-303636a9d1ec`;
- run `wp2h1-a1-20260826-001`;
- profile revision `a6da96560b6526dc6816761282722c996418fd8c`;
- mapping `enb1 -> nuc1`, `rue1 -> nuc2`;
- exact deployed WellPulse commit `95ba9a57bef159450b00b8a439d393d22e1c0519`;
- classification **`VALID_W1_RECOVERY_FAILURE`**;
- scored: **NO**.

Original H1 node-local raw bundles were **not recovered** after teardown. GitHub/local salvage is derived/provenance only. POWDER support subsequently confirmed that the `nuc1` and `nuc2` node-local disks had been reloaded immediately after experiment termination, while `/proj` storage persists across experiments. This confirms the operational rule now captured in the evidence architecture: mandatory raw evidence must leave node-local home and reach persistent `/proj` plus verified off-platform escrow before teardown. The support confirmation is retained outside the repository in the project experience/asset ledger rather than as scientific raw evidence.

Do not reopen H1 salvage, rerun H1 to select H, or relabel the adverse result.

## K1–K8 — closed

Canonical record:

`docs/K8_PREINTEGRATION_COMPATIBILITY_CLOSURE_2026-08-27.md`

Decisive compatibility evidence:

- historical workflow `wp2-kfastlane-live-compat-v2.yml`;
- Actions run `33085406598` — success;
- experiment `fc7c2187-2376-4a92-8de1-4665a06ea943`;
- classification `INFRASTRUCTURE_ONLY_NON_SCORED`.

It verified Portal READY/expiry binding, exact profile/hardware/image, controller SSH, detached launch, cross-node `/proj/WellPulse`, controller artifact round-trip, hashes and teardown authority.

The historical K workflow is no longer active after AUDIT-R1 cleanup. Do not reopen K1–K8 absent a material interface change.

## Current gate — STOPPED before execution

The next bounded patch is:

`LIVE_HCI_AND_RAW_EVIDENCE_GATE — CLOSURE PATCH`

**Status: BLOCKED / NOT STARTED.**

Do not begin it until the user explicitly says to continue.

When authorized, keep it minimal and bounded:

1. passive one-way HCI only;
2. `HCI_CONTROL_ACTIONS_ENABLED=false`;
3. enrich orchestrator-emitted status/events only; no independent POWDER probe;
4. freeze exact mandatory raw-evidence/finalization contract;
5. no background/in-run `/proj` checkpoint during protected science unless separately proven non-perturbing;
6. run only bounded/offline QA needed for this gate;
7. update canonical handover and **STOP before Golden**.

## Golden remains prohibited

`REBOOK_GOLDEN=false`

Do **not**:

- contact POWDER for this stopped frontier;
- create/modify/terminate a reservation;
- SSH to POWDER;
- run Golden;
- run H calibration;
- execute B1/W1/B2 scored work;
- reopen K1–K8;
- reopen RF calibration;
- reopen H1 salvage.

Only after the HCI/raw-evidence gate passes **and** a separate later explicit user authorization may the project perform the advisory resource preflight and book one clean non-scored Golden.

## Shortest mission path

`AUDIT-R1 PASS -> explicit user resume -> HCI/raw gate PASS -> STOP -> separate explicit user resume -> resinfo advisory preflight -> one clean non-scored Golden -> formal WP2 closure/scored authorization -> WP3 -> WP4 -> WP5`

## Mandatory read order for the next agent

1. `HANDOVER_CURRENT.md`
2. `docs/PROJECT_AUDIT_HANDOVER_2026-08-27.md`
3. `docs/AUDIT_R1_SUPERSESSION_MAP_2026-08-27.md`
4. `docs/AUDIT_R1_WORKFLOW_DEACTIVATION_2026-08-27.md`
5. `experiments/WP-PWD01/RECOVERY_SEMANTICS_AMENDMENT_v1.md`
6. `experiments/WP-PWD01/protocol.md`
7. `docs/NEXT_GATE.md`
8. `docs/MILESTONE_STATUS.md`
9. `docs/K8_PREINTEGRATION_COMPATIBILITY_CLOSURE_2026-08-27.md`
10. `docs/LIVE_EXPERIMENT_HCI_AND_RAW_EVIDENCE.md`
11. `experiments/WP-PWD01/GOLDEN_E2E_REHEARSAL_v1.md`
12. `experiments/WP-PWD01/evidence_inventory_golden_v1.txt`
13. `experiments/WP-PWD01/evidence-schema.md`
14. `experiments/WP-PWD01/analysis-plan.md`
15. `experiments/WP-PWD01/run-matrix.yaml`
16. `src/wellpulse/powder_analysis.py`
17. `scripts/reconstruct_wp2_golden.py`
18. `scripts/wp2_golden_orchestrator.sh`
19. `scripts/wp2_golden_evidence_escrow.sh`
20. `scripts/wp2_controller_pull_persistent_escrow.sh`
21. `scripts/wp2_controller_verify_artifact_roundtrip.sh`
22. `docs/WORKFLOW_REGISTRY.md`
23. `AGENTS.md`

**STOP / HANDOVER READY.**
