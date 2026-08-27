# WellPulse — Current Handover

Last updated: 2026-08-27 after comprehensive pre-agent-handover project audit.

## Executive state

- Canonical repository: `aayoubMSA/WellPulse`, branch `main`.
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
- `LIVE_HCI_AND_RAW_EVIDENCE_GATE=BLOCKED`.
- `REBOOK_GOLDEN=false`.
- `scored_runs_authorized=false`.
- `HCI_CONTROL_ACTIONS_ENABLED=false`.

## Mandatory audit state

Canonical audit:

`docs/PROJECT_AUDIT_HANDOVER_2026-08-27.md`

Audit verdict:

`PROJECT_AUDIT=COMPLETE`

`SCIENTIFIC_FROZEN_STATE=PRESERVED`

`PASS_WITH_MANDATORY_OFFLINE_RECONCILIATION_BEFORE_GOLDEN`

The audit found no basis to reopen the frozen scientific results, RF calibration, K1–K8, or H1 classification. It did find material document/control-plane drift that must be reconciled **offline** before the HCI/raw gate can pass or Golden can be booked.

## Governing scientific state

Recovery Semantics Amendment v1 is the authority for current recovery clocks and horizon:

- `t_rf_restore`, `t_service_ready`, `t_app_complete` are distinct;
- primary cohort = valid records generated at or before `t_rf_restore`;
- fixed application observation window = **300 s from `t_service_ready`**;
- primary endpoint = `completeness_300` at `t_service_ready + 300 s`;
- preserve `T_service`, `T_app`, `T_total`;
- S2/S3 clean-order substrate restoration = `stop UE -> EPC -> eNB -> fresh UE -> architecture-blind service-ready probe`;
- Golden G6 qualification bound = 120 s;
- negative/null outcomes remain valid and never justify outcome-driven protocol changes.

Q0/Q1/Q2/Q3 remain `0/40/52/55 dB`; attenuation IDs `1 33 2 34` remain coupled. Do not reopen the RF sweep.

## Protocol

Current protocol is:

`experiments/WP-PWD01/protocol.md` **v0.6.1**

v0.6.1 added only an operational advisory pre-reservation resource-availability check:

`https://www.powderwireless.net/resinfo.php`

Record availability as `PASS|DEFER|UNKNOWN`. Do not change frozen nodes/hardware/profile merely to obtain capacity. Portal create/get/READY/manifest remains authoritative. This availability preflight does not authorize Golden, H work, scoring, or teardown.

## H1 — frozen adverse experiment of record

- experiment `WP-HCAL-E`;
- UUID `9153e16a-1eb1-45f5-88bf-303636a9d1ec`;
- run `wp2h1-a1-20260826-001`;
- profile revision `a6da96560b6526dc6816761282722c996418fd8c`;
- mapping `enb1 -> nuc1`, `rue1 -> nuc2`;
- exact deployed WellPulse commit `95ba9a57bef159450b00b8a439d393d22e1c0519`;
- classification **`VALID_W1_RECOVERY_FAILURE`**;
- scored: **NO**.

The original node-local H1 raw bundles were **not recovered** after teardown. GitHub/local salvage is derived/provenance only. Never claim raw record-level H1 recovery and do not reopen salvage without a genuinely new evidence source.

## K1–K8 — closed

Canonical record:

`docs/K8_PREINTEGRATION_COMPATIBILITY_CLOSURE_2026-08-27.md`

Decisive live compatibility run:

- workflow `.github/workflows/wp2-kfastlane-live-compat-v2.yml`;
- Actions run `33085406598` — success;
- experiment `fc7c2187-2376-4a92-8de1-4665a06ea943`;
- classification `INFRASTRUCTURE_ONLY_NON_SCORED`.

It verified Portal READY/expiry binding, exact profile/hardware/image, controller SSH, K4 detached launch, cross-node `/proj/WellPulse`, controller artifact round-trip, hashes, and teardown authority. Post-live K3/K7/integrated-static QA also passed.

Do not reopen K1–K8 absent a material interface change.

## Qualified evidence architecture

Critical path:

`POWDER raw -> /proj/WellPulse persistent escrow -> controller pull -> GitHub Actions artifact -> independent controller download/read-back -> outer + internal hash verification -> teardown authority`

Google Drive/rclone is not teardown-critical; it may be an optional secondary mirror only.

The node-side Golden phase must never authorize teardown by itself. Only verified controller round-trip may emit `TEARDOWN_AUTHORIZED=YES`.

## Audit blockers to reconcile before Golden

The detailed evidence and exact affected files are in `docs/PROJECT_AUDIT_HANDOVER_2026-08-27.md`.

### P0-A — amended endpoint clock is not propagated everywhere

The governing amendment/Golden reconstructor use `t_rf_restore` for cohort cutoff and `t_service_ready + 300 s` for endpoint observation, but these still carry pre-amendment `cutoff + H` / old-H semantics:

- `analysis-plan.md` v0.3;
- `evidence-schema.md` v0.3;
- `run-matrix.yaml`;
- `src/wellpulse/powder_analysis.py` contract/naming and tests;
- `.github/workflows/wp2-h-preflight.yml`.

The Golden-specific `scripts/reconstruct_wp2_golden.py` is aligned with the current amendment.

### P0-B — legacy H-calibration terminology is ambiguous

Recovery Semantics Amendment v1 prospectively fixed `H_app=300 s` from `t_service_ready`, superseding the former W1-derived H-selection scheme. Historical files and some status text still say H is open/unfrozen or instruct W1 H calibration. Do not execute that old calibration scheme. Reconcile the terminology prospectively; do not derive a new horizon from outcomes.

### P0-C — evidence inventory has an obsolete Drive marker

`evidence_inventory_golden_v1.txt` still names `escrow/OFF_POWDER_RCLONE.PASS`, while the qualified teardown authority now comes from the controller/GitHub artifact read-back path. Reconcile the generated evidence/finalization contract before HCI/raw PASS.

### P0-D — workflow registry/hygiene is stale

The old registry/hygiene record says exactly six active workflows and no active POWDER lifecycle workflow. K-fastlane later added additional active QA/diagnostic/live workflows and trigger sentinels. The completed K live surface must be inventoried and archived/disabled or explicitly controlled; do not trigger another K reservation during cleanup.

### P0-E — stale historical documents can issue wrong instructions

Treat these as provenance, not current operational authority, until explicitly marked superseded/reconciled:

- `docs/STATUS.md`;
- `docs/RS7_IMPLEMENTATION_READINESS_STATUS_2026-08-26.md`;
- `experiments/WP-PWD01/H_CALIBRATION_PLAN_v1.md` old horizon-selection portions;
- `docs/DECISIONS.md` D-017 and horizon portions of D-019;
- old workflow registry/hygiene counts.

In particular, ignore old `RESERVE=true` and Drive-critical instructions.

## HCI/raw gate

After audit reconciliation, the next scientific-support gate remains:

`LIVE_HCI_AND_RAW_EVIDENCE_GATE=PASS`

Use a minimal passive one-way HCI only. The existing Golden orchestrator emits progress and `gate_events.jsonl`, but the machine-readable event contract is not yet fully aligned with the HCI design. Enrich orchestrator-emitted events only; do not build a probing dashboard.

Do **not** add in-run/background `/proj` checkpointing during the protected scientific window unless separately benchmarked non-perturbing. Shortest path: no in-run checkpoint; reserve sufficient post-G7 time for freeze/hash/escrow.

## Exact next action

**No reservation. Execute one bounded offline patch only:**

`AUDIT-R1 — PRE-GOLDEN SCIENTIFIC/EVIDENCE/GOVERNANCE RECONCILIATION`

AUDIT-R1 must:

1. align analysis plan, evidence schema, run matrix, general analysis implementation/tests to the governing `t_rf_restore` cohort + `t_service_ready+300 s` endpoint;
2. explicitly supersede/retire the old W1-derived H-selection procedure and resolve legacy H terminology without changing the frozen 300 s amended horizon;
3. reconcile the Golden evidence inventory/finalization markers to the qualified controller/GitHub artifact path;
4. inventory and clean/control the current active workflow + trigger surface, including completed K live workflows and obsolete H-preflight;
5. mark stale STATUS/RS7/H-calibration/decision text as superseded while preserving provenance;
6. preserve protocol v0.6.1 resource-availability preflight;
7. run offline/static QA only;
8. update canonical audit/status/handover and **STOP**.

Only after explicit resume following AUDIT-R1 PASS may the HCI/raw-evidence closure patch run. That patch must itself STOP before Golden unless the user separately authorizes the Golden reservation.

## Shortest mission path

`AUDIT-R1 -> HCI/raw gate PASS -> resinfo advisory preflight -> one clean non-scored Golden -> formal WP2 scientific closure/scored authorization -> WP3 -> WP4 -> WP5`

## Mandatory read order for the next agent

1. `HANDOVER_CURRENT.md`
2. `docs/PROJECT_AUDIT_HANDOVER_2026-08-27.md`
3. `experiments/WP-PWD01/RECOVERY_SEMANTICS_AMENDMENT_v1.md`
4. `experiments/WP-PWD01/protocol.md`
5. `docs/K8_PREINTEGRATION_COMPATIBILITY_CLOSURE_2026-08-27.md`
6. `docs/LIVE_EXPERIMENT_HCI_AND_RAW_EVIDENCE.md`
7. `docs/NEXT_GATE.md`
8. `docs/MILESTONE_STATUS.md`
9. `experiments/WP-PWD01/GOLDEN_E2E_REHEARSAL_v1.md`
10. `experiments/WP-PWD01/evidence_inventory_golden_v1.txt`
11. `experiments/WP-PWD01/evidence-schema.md`
12. `experiments/WP-PWD01/analysis-plan.md`
13. `experiments/WP-PWD01/run-matrix.yaml`
14. `src/wellpulse/powder_analysis.py`
15. `scripts/reconstruct_wp2_golden.py`
16. `scripts/wp2_golden_orchestrator.sh`
17. `docs/WORKFLOW_REGISTRY.md`
18. `AGENTS.md`

**STOP / HANDOVER READY.**
