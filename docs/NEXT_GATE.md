# Next Gate — LIVE HCI & Raw-Evidence Closure

**Current frontier:** AUDIT-R1 complete / closed  
**Scientific completion:** 20%  
**K1–K8 compatibility:** `PASS / CLOSED`  
**Pre-integration compatibility:** `PASS`  
**AUDIT-R1:** `PASS`  
**Live HCI/raw-evidence gate:** `BLOCKED / NOT STARTED`  
**Golden rebook authorization:** `false`  
**Scored authorization:** `false`

Canonical audit:

`docs/PROJECT_AUDIT_HANDOVER_2026-08-27.md`

Canonical supersession control:

`docs/AUDIT_R1_SUPERSESSION_MAP_2026-08-27.md`

## AUDIT-R1 closure

The offline pre-Golden reconciliation is complete. The following P0 drift is closed without reopening frozen science:

1. analysis plan, evidence schema, run matrix, general analysis implementation and tests now use:
   - primary cohort cutoff = `t_rf_restore`;
   - application horizon = `t_service_ready + 300 s`;
   - primary endpoint = `completeness_300`;
   - distinct `T_service`, `T_app`, `T_total`;
2. the former W1/outcome-derived H-selection procedure is explicitly superseded and fail-closed; current `H_app=300 s` is already prospectively frozen;
3. Golden evidence inventory/finalization now uses the qualified controller/GitHub artifact path rather than Drive/rclone as teardown authority;
4. active workflow/trigger governance is reconciled to exactly 6 offline/static workflows and 4 root sentinels; completed K live/diagnostic and obsolete H-preflight workflows are no longer active;
5. stale STATUS/RS7/H-calibration/decision instructions are controlled by an explicit supersession map;
6. protocol v0.6.1 advisory resource-availability preflight remains in the future booking path only;
7. offline QA evidence includes successful current unit tests and successful off-POWDER GitHub artifact upload/download/hash round-trip with `POWDER_CONTACT=NO`, `DRIVE_CONTACT=NO`, `SCIENTIFIC_RUN=NO`.

No POWDER contact/reservation/SSH, Golden execution, H calibration, scored B1/W1/B2 work, RF recalibration, K-series reopening, or H1 salvage occurred during AUDIT-R1.

## Exact next bounded patch — only after explicit user continuation

`LIVE_HCI_AND_RAW_EVIDENCE_GATE — CLOSURE PATCH`

This patch remains **not started**. When explicitly authorized, it must stay bounded to:

1. minimal passive one-way HCI with `HCI_CONTROL_ACTIONS_ENABLED=false`;
2. orchestrator-emitted status/events only; no independent POWDER probe;
3. exact mandatory raw-evidence/finalization contract;
4. no in-run/background `/proj` checkpoint during protected science unless separately proven non-perturbing;
5. offline/bounded QA sufficient to close `LIVE_HCI_AND_RAW_EVIDENCE_GATE=PASS`;
6. canonical handover update and STOP before Golden.

## Golden remains prohibited

Do **not** book or run Golden after this file update.

Only after the HCI/raw-evidence gate passes **and** a separate explicit user authorization should the project:

1. immediately before booking, perform protocol v0.6.1 advisory resource-availability preflight at `https://www.powderwireless.net/resinfo.php`;
2. record `PASS|DEFER|UNKNOWN` without automatically changing frozen hardware/profile;
3. use Portal lifecycle/READY/manifest as authoritative;
4. book and execute one clean non-scored G0–G10 Golden rehearsal;
5. verify complete raw evidence and controller artifact round-trip before teardown;
6. then decide formal WP2 scientific closure/scored authorization.

## Frozen controls

- H1 remains `VALID_W1_RECOVERY_FAILURE`; original H1 raw bundles were not recovered.
- Q0/Q1/Q2/Q3 remain `0/40/52/55 dB`; IDs `1 33 2 34` remain coupled.
- K1–K8 remain PASS/CLOSED absent a material interface change.
- `H_app=300 s from t_service_ready` is frozen.
- outcome-derived/W1-derived H recalibration is prohibited.
- `scored_runs_authorized=false`.
- `REBOOK_GOLDEN=false`.
- no WP3 B1/W1/B2 scored execution is authorized.

Shortest path:

`AUDIT-R1 PASS -> explicit resume -> HCI/raw gate PASS -> STOP -> separate explicit resume -> resinfo advisory preflight -> clean non-scored Golden -> WP2 closure/scored authorization -> WP3 -> WP4 -> WP5`
