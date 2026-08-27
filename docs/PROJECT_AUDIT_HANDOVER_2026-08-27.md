# WellPulse Project Audit & AUDIT-R1 Closure — 2026-08-27

## Current verdict

`PROJECT_AUDIT=COMPLETE`

`AUDIT_R1=PASS`

`SCIENTIFIC_FROZEN_STATE=PRESERVED`

`K1_K8_COMPATIBILITY=PASS_CLOSED`

`PRE_INTEGRATION_COMPATIBILITY_GATE=PASS`

`LIVE_HCI_AND_RAW_EVIDENCE_GATE=BLOCKED_NOT_STARTED`

`REBOOK_GOLDEN=false`

`scored_runs_authorized=false`

`SCIENTIFIC_WEIGHTED_COMPLETION=20%`

The original audit classification was `PASS_WITH_MANDATORY_OFFLINE_RECONCILIATION_BEFORE_GOLDEN`. That mandatory offline reconciliation is now complete and closed as **AUDIT-R1 PASS**.

No POWDER contact/reservation/SSH, Golden execution, H calibration, B1/W1/B2 scored work, RF recalibration, K-series reopening, or H1 salvage occurred during AUDIT-R1.

## 1. AUDIT-R1 work-package closure

The reconciliation was executed as five finite acceptance-gated work packages. Progress was credited only after the corresponding acceptance gate closed.

| Package | Weight | Acceptance result | Closure evidence |
|---|---:|---|---|
| A1 — analysis semantics | 30% | PASS | General/scored analysis plan, schema, run matrix, analysis implementation and tests use `t_rf_restore` cohort + fixed `t_service_ready+300 s`; old outcome-derived H calculation is fail-closed. |
| A2 — evidence contract | 20% | PASS | Golden inventory and persistent escrow use the qualified controller/GitHub artifact finalization markers; persistent escrow now emits the required controller-handoff marker; Drive/rclone is optional secondary only. |
| A3 — workflow/governance control | 20% | PASS | Active tree re-enumerated and reconciled to exactly 6 offline/static workflows + 4 root sentinels; stale K live/diagnostic and obsolete H-preflight surfaces removed from the active path without dispatching them. |
| A4 — provenance/supersession | 15% | PASS | Canonical supersession map added; stale STATUS, RS7, H-calibration and old-H decision text retained as provenance but prevented from issuing current instructions. |
| A5 — offline QA + canonical control | 15% | PASS | Current deterministic unit-test gate PASS; independent GitHub artifact upload/download/hash round-trip PASS; negative searches/static inspection and current workflow/root inventory reconciled; canonical frontier/handover updated. |

`AUDIT_R1_ACCEPTED_PROGRESS=100/100`

This 100/100 is **audit-patch acceptance only**. Scientific weighted completion remains **20%** because WP2 is not scientifically closed.

## 2. Frozen scientific state preserved

### 2.1 Work packages

- WP0 Novelty & Venue Lock: PASS, 8/8.
- WP1 Confirmatory Protocol & Statistics Freeze: PASS/FROZEN, 12/12.
- WP2 RF Calibration & Measurement Validation: ACTIVE.
- WP3 Conducted-RF Confirmatory Campaign: BLOCKED ON WP2.
- WP4 OTA External Replication: BLOCKED.
- WP5 Analysis + Artifact + Paper Closure: PREPARED / NOT EXECUTED.
- Scientific weighted completion remains 20% until WP2 closes.

### 2.2 RF and recovery semantics

Preserved without reopening:

- Q0/Q1/Q2/Q3 = `0/40/52/55 dB`;
- attenuation IDs `1 33 2 34`, always coupled;
- RF calibration remains frozen;
- primary cohort cutoff = `t_rf_restore`;
- `t_rf_restore`, `t_service_ready`, and `t_app_complete` remain distinct clocks;
- `T_service`, `T_app`, and `T_total` remain preserved;
- prospective application observation horizon = **`H_app=300 s` from `t_service_ready`**;
- primary endpoint = `completeness_300` at `t_service_ready + 300 s`;
- S2/S3 standardized substrate restoration = `stop UE -> EPC -> eNB -> fresh UE -> architecture-blind service-ready probe`;
- Golden G6 service-ready bound = 120 s;
- negative/null application outcomes remain valid scientific outcomes and never justify post-hoc protocol changes;
- W1/Golden/scored outcome-derived H re-estimation is prohibited.

### 2.3 H1

H1 remains permanently:

`VALID_W1_RECOVERY_FAILURE`

Experiment: `WP-HCAL-E`  
UUID: `9153e16a-1eb1-45f5-88bf-303636a9d1ec`  
Run: `wp2h1-a1-20260826-001`  
Scored: NO

The original H1 node-local raw bundles were **not recovered** after teardown. GitHub/local salvage is derived/provenance only. AUDIT-R1 did not reopen H1 salvage, rerun H1, or relabel the adverse outcome.

### 2.4 K-series

K1–K8 remain PASS/CLOSED. Decisive compatibility evidence remains:

- GitHub Actions run `33085406598` — success;
- experiment `fc7c2187-2376-4a92-8de1-4665a06ea943`;
- classification `INFRASTRUCTURE_ONLY_NON_SCORED`.

The K closure verified Portal/expiry binding, hardware/profile identity, controller SSH, detached launch, cross-node `/proj`, controller pull, GitHub artifact round-trip, outer/internal hash verification and teardown authority. AUDIT-R1 removed stale runnable K-era workflow surfaces but did not reopen or alter K evidence.

## 3. Qualified evidence architecture

The mandatory teardown-critical path is:

`POWDER raw -> /proj/WellPulse persistent escrow -> controller pull -> GitHub Actions artifact -> independent controller download/read-back -> outer + internal SHA-256 verification -> teardown authority`

Google Drive/rclone is **not** teardown-critical. It may be used only as an optional secondary mirror unless a future explicit amendment re-qualifies it.

Node/persistent side may establish only that the persistent evidence copy is verified and controller finalization is required. It must not self-authorize teardown.

Current mandatory progression is:

- `PERSISTENT_ESCROW_GATE=PASS`;
- `CONTROLLER_OFFPOWDER_REQUIRED`;
- `CONTROLLER_PULL_GATE=PASS`;
- `CONTROLLER_BUNDLE_SHA256=<64hex>`;
- independent GitHub artifact round-trip;
- `CONTROLLER_OFFPOWDER_GATE=PASS`;
- `ROUNDTRIP_BUNDLE_SHA256=<same_64hex>`;
- `EVIDENCE_ESCROW_GATE=PASS`;
- only then `TEARDOWN_AUTHORIZED=YES`.

## 4. Original P0 audit findings and AUDIT-R1 resolution

### P0-A — endpoint-clock drift — CLOSED

Original drift affected the pre-amendment general/scored analysis plan, evidence schema, run matrix, POWDER analysis contract/tests and old H-preflight surface.

AUDIT-R1 aligned all current operational artifacts to:

`primary cohort = generated_ts_utc <= t_rf_restore_utc`

and

`endpoint horizon = t_service_ready_utc + 300 s`.

The current primary endpoint is `completeness_300`. `T_service`, `T_app`, and `T_total` remain distinct secondary recovery clocks.

### P0-B — ambiguous legacy H terminology — CLOSED

Recovery Semantics Amendment v1 is now explicit operational authority. The old W1-derived H-selection procedure is historical/provenance only and execution is fail-closed.

Current canonical rule:

`H_app=300 s from t_service_ready`

No W1-only pilot, Golden result, or scored outcome may re-estimate that horizon.

### P0-C — stale Drive/rclone evidence marker — CLOSED

`experiments/WP-PWD01/evidence_inventory_golden_v1.txt` was reconciled to the qualified controller/GitHub artifact path. `OFF_POWDER_RCLONE.PASS` is no longer a teardown-critical generated requirement.

A contract mismatch discovered during reconciliation was also closed: `scripts/wp2_golden_evidence_escrow.sh` now creates the persistent `escrow/CONTROLLER_OFFPOWDER_REQUIRED` marker required by the controller verifier, while keeping teardown fail-closed until the independent round-trip passes.

The Golden offline QA script/workflow was also reconciled so its acceptance contract no longer treats rclone as teardown authority.

### P0-D — stale workflow registry/hygiene — CLOSED

Before cleanup the active tree contained 14 workflows and 12 root sentinels. AUDIT-R1 retired the stale runnable H/K surface in fail-safe order: workflow YAML first, corresponding trigger sentinel second.

Current verified active workflow set is exactly **6**:

1. `local-gate-once.yml`
2. `local-unit-tests.yml`
3. `wp2-b2-semantics.yml`
4. `wp2-golden-offline-qa.yml`
5. `wp2-offpowder-artifact-qa.yml`
6. `wp2-preintegration-static.yml`

Current verified root sentinels are exactly **4**:

- `.local-gate-trigger`
- `.wp2-b2-semantics-trigger`
- `.wp2-offpowder-artifact-qa-trigger`
- `.wp2-preintegration-static-trigger`

No active K live/diagnostic workflow and no old-H preflight workflow remains in `.github/workflows/`.

Historical K/workflow provenance remains available through Git history and existing closure evidence.

### P0-E — stale status/readiness instructions — CLOSED

Canonical control file:

`docs/AUDIT_R1_SUPERSESSION_MAP_2026-08-27.md`

It preserves but supersedes dangerous old operational instructions in:

- `docs/STATUS.md`;
- `docs/RS7_IMPLEMENTATION_READINESS_STATUS_2026-08-26.md`;
- `experiments/WP-PWD01/H_CALIBRATION_PLAN_v1.md`;
- `docs/DECISIONS.md` D-017 and the old horizon-selection portions of D-019;
- the original C4 workflow-hygiene snapshot where later K-fastlane additions made it stale.

`docs/STATUS.md`, RS7 readiness and the H-calibration plan also carry explicit local supersession notices.

## 5. Protocol v0.6.1 resource-availability preflight

The advisory resource-availability preflight remains part of the **future** booking path only:

`https://www.powderwireless.net/resinfo.php`

Immediately before any later booking attempt, record `PASS|DEFER|UNKNOWN`. This check is advisory; it must never silently change the frozen hardware/profile. Portal lifecycle/READY/manifest remains authoritative.

AUDIT-R1 did **not** contact this page or POWDER.

## 6. Offline QA acceptance evidence

### 6.1 Deterministic unit tests

GitHub Actions run `33092273688`:

- workflow: `Local Unit Tests`;
- conclusion: `success`;
- deterministic unit-test step: PASS;
- result-enforcement step: PASS;
- pinned `paho-mqtt==2.1.0` installation step: PASS.

The workflow was made read-only/race-free after two earlier runs demonstrated that the tests themselves passed but a concurrent branch-evidence write could make the workflow conclusion fail. Current unit-test QA no longer writes to `main`.

### 6.2 Independent off-POWDER artifact round-trip

GitHub Actions run `33092849805`:

- workflow: `WP2 Off-POWDER Artifact Transport QA`;
- conclusion: `success`;
- deterministic bundle build: PASS;
- artifact upload: PASS;
- independent artifact download: PASS;
- round-trip TAR byte SHA-256 equality: PASS;
- internal raw hashes: PASS;
- artifact ID: `9655099849`;
- round-trip TAR SHA-256: `1a5c78b3ff588cef38338d12b7891793aca8f436f312c501b5712bb74d423605`;
- logged `POWDER_CONTACT=NO`;
- logged `DRIVE_CONTACT=NO`;
- logged `SCIENTIFIC_RUN=NO`.

### 6.3 Static/negative reconciliation checks

Repository searches after reconciliation found no active indexed occurrence of the dangerous current-state strings:

- `H=UNFROZEN`;
- `recovery_horizon_H OPEN_ACTIVE_GATE`;
- `OFF_POWDER_RCLONE.PASS`;
- `completeness_H`.

Current workflow/root inventory was re-enumerated rather than inferred from the old registry.

## 7. P1 findings deliberately NOT executed in AUDIT-R1

The following remain the next separately authorized gate and were not started:

### P1-A — passive HCI contract

The minimal implementation must remain one-way/passive:

`HCI_CONTROL_ACTIONS_ENABLED=false`

Enrich orchestrator-emitted events/stdout only. Do not build an independent POWDER-probing dashboard.

### P1-B — in-run checkpointing

Do not perform background/in-run `/proj` checkpointing during the protected scientific window on the shortest path. No such checkpoint is needed unless separately benchmarked and proven non-perturbing.

### P1-C — exact raw-evidence/finalization closure

Freeze the exact mandatory raw filenames, emitted passive status fields and controller finalization evidence needed to close `LIVE_HCI_AND_RAW_EVIDENCE_GATE=PASS`.

This work begins only after explicit user continuation.

## 8. Current authority order

Use these as governing sources:

1. `HANDOVER_CURRENT.md`;
2. this audit/closure record;
3. `docs/AUDIT_R1_SUPERSESSION_MAP_2026-08-27.md`;
4. `experiments/WP-PWD01/RECOVERY_SEMANTICS_AMENDMENT_v1.md`;
5. `experiments/WP-PWD01/protocol.md` v0.6.1;
6. `docs/NEXT_GATE.md`;
7. `docs/MILESTONE_STATUS.md`;
8. `docs/K8_PREINTEGRATION_COMPATIBILITY_CLOSURE_2026-08-27.md`;
9. `docs/LIVE_EXPERIMENT_HCI_AND_RAW_EVIDENCE.md` for the still-open HCI/raw design only;
10. `experiments/WP-PWD01/GOLDEN_E2E_REHEARSAL_v1.md` for later Golden sequence/gates, not current execution authorization.

## 9. Exact safe frontier after AUDIT-R1

`AUDIT_R1=PASS`

`LIVE_HCI_AND_RAW_EVIDENCE_GATE=BLOCKED_NOT_STARTED`

`REBOOK_GOLDEN=false`

`scored_runs_authorized=false`

Do not reserve or run Golden now.

Only after explicit user continuation may the next bounded patch implement/verify the minimal passive HCI and exact raw-evidence/finalization contract. That patch must then update canonical handover and **STOP before Golden**.

Only after a separate later explicit authorization should the project perform the advisory resource-availability preflight and book one clean non-scored Golden.

Shortest mission path:

`AUDIT-R1 PASS -> explicit resume -> HCI/raw gate PASS -> STOP -> separate explicit resume -> resinfo advisory preflight -> one clean non-scored Golden -> formal WP2 closure/scored authorization -> WP3 -> WP4 -> WP5`

Do not reopen K1–K8, RF calibration, H1 salvage, or the old W1-derived H-calibration scheme absent a material interface change or explicit scientific amendment.
