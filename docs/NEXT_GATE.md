# Next Gate — AUDIT-R1 Pre-Golden Reconciliation

**Current frontier:** comprehensive project audit complete  
**Scientific completion:** 20%  
**K1–K8 compatibility:** `PASS / CLOSED`  
**Pre-integration compatibility:** `PASS`  
**Live HCI/raw-evidence gate:** `BLOCKED`  
**Golden rebook authorization:** `false`  
**Scored authorization:** `false`

Canonical audit:

`docs/PROJECT_AUDIT_HANDOVER_2026-08-27.md`

Audit classification:

`PASS_WITH_MANDATORY_OFFLINE_RECONCILIATION_BEFORE_GOLDEN`

## Why the next patch changed

The K-series is closed and its decisive live compatibility evidence is valid. However, the handover audit found several pre-amendment artifacts and governance records that were not reconciled after Recovery Semantics Amendment v1 and the K-fastlane evidence architecture.

This is documentation/execution-contract drift, not evidence that the frozen RF/scientific results are invalid.

The highest-risk discrepancies are:

1. `analysis-plan.md`, `evidence-schema.md`, `run-matrix.yaml`, the general POWDER analysis contract/tests, and `wp2-h-preflight.yml` still contain the former `cutoff + H` / W1-derived-H semantics, while the governing amendment freezes cohort cutoff at `t_rf_restore` and endpoint observation at `t_service_ready + 300 s`;
2. `evidence_inventory_golden_v1.txt` still contains the old Drive/rclone generated marker even though controller/GitHub artifact read-back is now the qualified off-POWDER authority;
3. workflow registry/hygiene documents predate the additional K-era workflows/triggers and no longer describe the actual active Actions surface;
4. stale `STATUS`, RS7 readiness, old H-calibration and old decision text can still issue superseded instructions such as `RESERVE=true`, Drive-critical teardown, or W1-derived H calibration;
5. protocol v0.6.1 added the advisory POWDER resource-availability preflight and this must remain in the canonical operational path.

## Exact next bounded patch

`AUDIT-R1 — PRE-GOLDEN SCIENTIFIC/EVIDENCE/GOVERNANCE RECONCILIATION`

AUDIT-R1 is **offline only**. It must not contact POWDER, create a reservation, run Golden, calibrate H, or execute scored work.

Required tasks:

1. align the general/scored analysis plan, schema, run matrix, implementation contract and tests with Recovery Semantics Amendment v1:
   - cohort cutoff = `t_rf_restore`;
   - fixed endpoint horizon = `t_service_ready + 300 s`;
   - primary endpoint = `completeness_300`;
   - preserve `T_service`, `T_app`, `T_total`;
2. explicitly supersede/retire the former W1-derived H-selection scheme; do not collect new W1 H-calibration trials and do not estimate a new horizon from outcomes;
3. reconcile the Golden evidence inventory/finalization contract to the qualified path:
   `raw -> /proj -> controller pull -> GitHub artifact -> independent read-back/hash -> teardown authority`;
4. inventory and reconcile the actual `.github/workflows/` and root-trigger surface; completed K live/diagnostic execution paths must not remain accidentally runnable merely because the old registry is stale;
5. retire or update the obsolete `wp2-h-preflight.yml` so a green result cannot validate superseded H semantics;
6. preserve stale status/readiness/H-calibration/decision files as historical provenance but add explicit supersession control;
7. preserve protocol v0.6.1 resource preflight:
   `https://www.powderwireless.net/resinfo.php` as advisory `PASS|DEFER|UNKNOWN`, with Portal lifecycle/manifest authoritative;
8. run the smallest offline/static QA necessary to prove consistency;
9. update canonical audit/handover/status and STOP.

## After AUDIT-R1 PASS

Only after explicit user resume:

1. execute one bounded `LIVE_HCI_AND_RAW_EVIDENCE_GATE` closure patch;
2. use a passive, one-way HCI only with `HCI_CONTROL_ACTIONS_ENABLED=false`;
3. enrich orchestrator-emitted status/events only; do not add independent POWDER probes;
4. freeze exact mandatory raw filenames and controller finalization evidence;
5. choose **no in-run/background `/proj` checkpoint** during protected science unless separately benchmarked non-perturbing;
6. close `LIVE_HCI_AND_RAW_EVIDENCE_GATE=PASS` only from actual offline/bounded evidence;
7. STOP before Golden.

Only after a separate explicit authorization should the project perform the resource-availability advisory preflight and book one clean non-scored Golden.

## Frozen controls

- H1 remains `VALID_W1_RECOVERY_FAILURE`.
- H1 original raw bundles were not recovered.
- Q0/Q1/Q2/Q3 remain `0/40/52/55 dB`, IDs `1 33 2 34` coupled.
- Recovery Semantics Amendment v1 governs the 300 s `t_service_ready` horizon.
- `scored_runs_authorized=false`.
- `REBOOK_GOLDEN=false`.
- no WP3 B1/W1/B2 scored execution.

Shortest path:

`AUDIT-R1 -> HCI/raw gate -> resinfo advisory preflight -> clean non-scored Golden -> WP2 closure/scored authorization -> WP3 -> WP4 -> WP5`
