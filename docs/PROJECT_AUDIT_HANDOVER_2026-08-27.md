# WellPulse Project Audit Before Agent Handover — 2026-08-27

## Audit verdict

`PROJECT_AUDIT=COMPLETE`

`SCIENTIFIC_FROZEN_STATE=PRESERVED`

`K1_K8_COMPATIBILITY=PASS_CLOSED`

`PRE_INTEGRATION_COMPATIBILITY_GATE=PASS`

`LIVE_HCI_AND_RAW_EVIDENCE_GATE=BLOCKED`

`REBOOK_GOLDEN=false`

`scored_runs_authorized=false`

`SCIENTIFIC_WEIGHTED_COMPLETION=20%`

**Overall audit classification:** `PASS_WITH_MANDATORY_OFFLINE_RECONCILIATION_BEFORE_GOLDEN`.

No reservation, Golden, H-calibration, or scored experiment was executed during this audit.

## 1. Scope audited

The audit reviewed the current canonical handover/frontier, scientific milestone plan, recovery-semantics amendment, protocol, Golden design, evidence inventory/schema, analysis plan and analysis implementation, K-series closure/evidence architecture, repository workflow governance, and selected stale historical status/readiness artifacts.

Key sources included:

- `HANDOVER_CURRENT.md`
- `docs/NEXT_GATE.md`
- `docs/MILESTONE_STATUS.md`
- `docs/K8_PREINTEGRATION_COMPATIBILITY_CLOSURE_2026-08-27.md`
- `docs/LIVE_EXPERIMENT_HCI_AND_RAW_EVIDENCE.md`
- `experiments/WP-PWD01/RECOVERY_SEMANTICS_AMENDMENT_v1.md`
- `experiments/WP-PWD01/protocol.md` v0.6.1
- `experiments/WP-PWD01/GOLDEN_E2E_REHEARSAL_v1.md`
- `experiments/WP-PWD01/evidence_inventory_golden_v1.txt`
- `experiments/WP-PWD01/evidence-schema.md`
- `experiments/WP-PWD01/analysis-plan.md`
- `experiments/WP-PWD01/run-matrix.yaml`
- `src/wellpulse/powder_analysis.py`
- `scripts/reconstruct_wp2_golden.py`
- `scripts/wp2_golden_orchestrator.sh`
- `scripts/wp2_golden_evidence_escrow.sh`
- `docs/WORKFLOW_REGISTRY.md`
- `docs/REPOSITORY_HYGIENE_FINAL_QA_2026-08-27.md`
- `docs/STATUS.md`
- `docs/DECISIONS.md`
- `docs/RS7_IMPLEMENTATION_READINESS_STATUS_2026-08-26.md`
- `.github/workflows/wp2-h-preflight.yml`

Audit baseline includes protocol v0.6.1 commit `733c7a180eccc8aa99883ab149bfd39da4c2bbfa`.

## 2. What is scientifically sound and must remain frozen

### 2.1 Work-package state

- WP0 Novelty & Venue Lock: PASS, 8/8.
- WP1 Confirmatory Protocol & Statistics Freeze: PASS/FROZEN, 12/12.
- WP2 RF Calibration & Measurement Validation: ACTIVE.
- WP3 Conducted-RF Confirmatory Campaign: BLOCKED ON WP2.
- WP4 OTA External Replication: BLOCKED.
- WP5 Analysis + Artifact + Paper Closure: PREPARED / NOT EXECUTED.
- Scientific weighted completion remains 20% until WP2 closes.

### 2.2 RF and recovery semantics

Preserve without reopening:

- Q0/Q1/Q2/Q3 = `0/40/52/55 dB`;
- attenuation IDs `1 33 2 34`, always coupled;
- primary cohort cutoff = `t_rf_restore`;
- `t_rf_restore`, `t_service_ready`, and `t_app_complete` are distinct clocks;
- `T_service`, `T_app`, and `T_total` are preserved;
- fixed application observation horizon = **300 s from `t_service_ready`**;
- primary endpoint under the governing recovery amendment = `completeness_300` at `t_service_ready + 300 s`;
- S2/S3 standardized substrate restoration = `stop UE -> EPC -> eNB -> fresh UE -> architecture-blind service-ready probe`;
- Golden G6 service-ready bound = 120 s;
- negative/null application outcomes remain valid scientific outcomes and never justify post-hoc protocol changes.

### 2.3 H1

H1 remains permanently:

`VALID_W1_RECOVERY_FAILURE`

The original H1 node-local raw bundles were **not recovered** after teardown. GitHub/local salvage is derived/provenance only. Any document claiming that the H1 raw bundles remain preserved and accessible is stale and must not be used as authority.

### 2.4 K-series

K1–K8 are PASS/CLOSED. Decisive compatibility run:

- GitHub Actions run `33085406598` — success;
- experiment `fc7c2187-2376-4a92-8de1-4665a06ea943`;
- infrastructure-only, non-scored;
- live Portal/expiry, hardware/profile identity, SSH, detached launch, cross-node `/proj`, controller pull, GitHub artifact round-trip, hash verification and teardown authority all passed.

Do not reopen K1–K8 absent a material interface change.

## 3. Qualified evidence architecture

The current qualified critical path is:

`POWDER raw -> /proj/WellPulse persistent escrow -> controller pull -> GitHub Actions artifact -> independent controller download/read-back -> outer + internal hash verification -> teardown authority`

Google Drive/rclone is **not** teardown-critical. It may be used later only as an optional secondary mirror.

The node-side Golden phase may emit only:

- `RAW_EVIDENCE_COMPLETE=PASS` after mandatory source inventory/freeze;
- `CONTROLLER_OFFPOWDER_GATE=PENDING`;
- `EVIDENCE_ESCROW_GATE=PENDING_CONTROLLER_COPY`;
- `TEARDOWN_AUTHORIZED=NO`.

Only the verified controller round-trip may emit:

- `CONTROLLER_OFFPOWDER_GATE=PASS`;
- `EVIDENCE_ESCROW_GATE=PASS`;
- `TEARDOWN_AUTHORIZED=YES`.

## 4. P0 audit findings — must be reconciled offline before Golden

### P0-A — Endpoint-clock drift in scored-analysis artifacts

The governing amendment/protocol/Golden reconstruction correctly use:

`primary cohort cutoff = t_rf_restore`

and

`endpoint horizon = t_service_ready + 300 s`.

However several pre-amendment artifacts still encode the former `cutoff + H` model:

- `experiments/WP-PWD01/analysis-plan.md` v0.3;
- `experiments/WP-PWD01/evidence-schema.md` v0.3;
- `experiments/WP-PWD01/run-matrix.yaml` (protocol v0.4 / old H-calibration state);
- `src/wellpulse/powder_analysis.py` naming/contract and its tests;
- `.github/workflows/wp2-h-preflight.yml` explicitly asserts the old H-calibration/run-matrix state.

The Golden-specific implementation `scripts/reconstruct_wp2_golden.py` is aligned with the amended semantics: it takes the final Q0 restoration as `t_rf_restore`, obtains `t_service_ready`, and sets the horizon to `t_service_ready + 300 s`.

**Required reconciliation:** prospectively align the general/scored analysis plan, schema, run matrix, implementation contract and tests with Recovery Semantics Amendment v1 without changing the already-frozen estimand.

### P0-B — Ambiguous legacy `H` terminology

Recovery Semantics Amendment v1 already freezes `H_app=300 s` from `t_service_ready`, superseding the old W1-only H-calibration selection rule. Yet some current/historical files still state `H=UNFROZEN`, `recovery_horizon_H=OPEN`, or instruct a future H-calibration/freeze.

**Required reconciliation:** explicitly retire/supersede the old W1-derived H-selection procedure and define the canonical current term/state. Do not invent a new horizon from outcomes. The governing scientific value remains the prospective 300 s application window unless an explicit new scientific amendment is approved.

### P0-C — Golden evidence inventory still contains old Drive/rclone generated marker

`experiments/WP-PWD01/evidence_inventory_golden_v1.txt` v1.3 still lists:

`escrow/OFF_POWDER_RCLONE.PASS`

as a generated artifact. This conflicts with the now-qualified controller/GitHub artifact evidence path. The persistent-escrow script checks only `REQUIRED` source entries, so this stale generated marker does not currently invalidate source-inventory enforcement, but the formal evidence/provenance contract is inconsistent.

**Required reconciliation:** update the generated/controller evidence inventory to the qualified controller off-POWDER round-trip markers and preserve exact filenames/hashes required for G9/G10.

### P0-D — Workflow registry/hygiene state is stale after K-fastlane

`docs/WORKFLOW_REGISTRY.md` and `docs/REPOSITORY_HYGIENE_FINAL_QA_2026-08-27.md` describe exactly six active workflows and no active POWDER lifecycle/SSH workflow. The current `.github/workflows/` tree contains additional K-era QA, diagnostic and live compatibility workflows added after that cleanup, including the completed live K-fastlane workflows. Their trigger sentinels also remain in the active root tree.

This does **not** invalidate the K evidence, but the old workflow registry is no longer an accurate inventory/control record.

**Required reconciliation:** inventory the actual current workflow/trigger surface; archive or otherwise make non-runnable the completed K live/diagnostic execution surface unless it remains materially required; update the registry/hygiene record. Do not trigger a K compatibility reservation during this cleanup.

### P0-E — stale status/readiness documents can issue wrong instructions

At least these files are historically useful but operationally superseded:

- `docs/STATUS.md` — pre-amendment state; incorrectly says original H1 raw archives are preserved;
- `docs/RS7_IMPLEMENTATION_READINESS_STATUS_2026-08-26.md` — says `RESERVE=true`, treats Google Drive as teardown-critical and predates the later HCI/raw gate and controller/GitHub evidence architecture;
- `experiments/WP-PWD01/H_CALIBRATION_PLAN_v1.md` — old W1-derived H selection, superseded by Recovery Semantics Amendment v1;
- `docs/DECISIONS.md` D-017 and horizon portions of D-019 — historical old-H decisions superseded by the later prospective recovery-semantics amendment.

**Required reconciliation:** preserve these as provenance but add explicit supersession notices or a canonical supersession map. Never follow their old reservation/H instructions over the current handover/amendment/audit.

## 5. P1 findings — required to close HCI/raw gate

### P1-A — passive HCI contract is designed but not fully frozen in implementation

Current Golden orchestration writes `orchestration/gate_events.jsonl`, but the event records are currently minimal (`utc`, `gate`, `status`, `detail`). The HCI design calls for bounded one-way machine-readable status including phase/progress and safety/evidence state, with no independent POWDER probe.

Required state remains:

`HCI_CONTROL_ACTIONS_ENABLED=false`.

The next implementation should remain minimal: enrich orchestrator-emitted events/stdout only. Do not build a separate probing dashboard.

### P1-B — in-run checkpointing is not required

The HCI/raw design says any proposed in-run `/proj` checkpoint must first be benchmarked for non-interference. No such checkpoint is required for the shortest path.

Recommended audit decision: **do not perform background/in-run `/proj` checkpointing during the protected scientific window.** Reserve enough post-G7 time for immediate freeze/hash/persistent escrow. This avoids unnecessary benchmark/infrastructure work.

### P1-C — resource availability preflight added but not yet reconciled into handover/frontier

Protocol v0.6.1 adds an advisory pre-reservation check at:

`https://www.powderwireless.net/resinfo.php`

Record `PASS|DEFER|UNKNOWN`; never silently change frozen nodes/hardware/profile to chase capacity. Portal create/get/READY/manifest remains authoritative.

This is operational only and does not authorize reservation/scoring.

## 6. Documents that remain good authorities

Use these as governing sources unless a later explicit amendment supersedes them:

1. `HANDOVER_CURRENT.md` as the top operational pointer, after this audit refresh;
2. this audit;
3. `experiments/WP-PWD01/RECOVERY_SEMANTICS_AMENDMENT_v1.md` for recovery clocks/horizon/fairness;
4. `experiments/WP-PWD01/protocol.md` v0.6.1 for current protocol and availability preflight;
5. `experiments/WP-PWD01/GOLDEN_E2E_REHEARSAL_v1.md` for Golden sequence/gates;
6. `docs/K8_PREINTEGRATION_COMPATIBILITY_CLOSURE_2026-08-27.md` for compatibility closure;
7. `docs/LIVE_EXPERIMENT_HCI_AND_RAW_EVIDENCE.md` for the HCI/raw design, subject to the reconciliation items above;
8. `docs/MILESTONE_STATUS.md` for scientific WP weights/status.

## 7. Exact safe frontier after audit

Do **not** reserve Golden yet.

The next bounded patch is offline only:

`AUDIT-R1 — PRE-GOLDEN SCIENTIFIC/EVIDENCE/GOVERNANCE RECONCILIATION`

It must:

1. align analysis plan, evidence schema, run matrix, general analysis implementation/tests with `t_rf_restore` cohort + `t_service_ready+300 s` horizon;
2. explicitly supersede/retire the old W1-derived H-calibration selection rule and remove ambiguous operational `H=UNFROZEN` instructions;
3. reconcile Golden evidence inventory with the controller/GitHub artifact path;
4. reconcile/clean the active workflow and trigger registry, especially completed K live workflows and the obsolete H-preflight;
5. mark stale status/RS7/H-calibration/decision text as superseded without deleting historical provenance;
6. incorporate protocol v0.6.1 resource-availability preflight into the current handover/frontier;
7. run only offline/static QA needed to prove the reconciliation;
8. update canonical handover and STOP.

No POWDER reservation/contact is required for AUDIT-R1.

Only after AUDIT-R1 PASS should the next bounded patch close `LIVE_HCI_AND_RAW_EVIDENCE_GATE` by implementing/verifying the minimal passive HCI event contract and exact raw-evidence/finalization contract. Then STOP before Golden.

## 8. Shortest mission path

`AUDIT-R1 offline reconciliation -> HCI/raw gate PASS -> resinfo advisory preflight -> one clean non-scored Golden -> formal WP2 closure/scored authorization -> WP3 -> WP4 -> WP5`

Do not reopen K1–K8, RF calibration, H1 salvage, or the old W1-derived H-calibration scheme unless genuinely new evidence or an explicit scientific amendment requires it.
