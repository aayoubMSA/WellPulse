# New-Agent Prompt — WellPulse WP2 AUDIT-R1 Continuation

Copy the text below into a fresh ChatGPT agent/chat.

---

Take ownership of the **WellPulse** project from the canonical private repository:

`aayoubMSA/WellPulse`

Canonical branch:

`main`

Do not reconstruct state from conversation memory. Treat GitHub as the source of truth.

## Mandatory read order

First read, in this exact order:

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

Follow any higher-authority mandatory rules referenced by those files.

## Exact retrieval point

The comprehensive project audit is complete.

Current scientific state:

- WP0 = PASS, 8/8.
- WP1 = PASS/FROZEN, 12/12.
- WP2 = ACTIVE.
- WP3 = BLOCKED ON WP2.
- WP4 = BLOCKED.
- WP5 = PREPARED / NOT EXECUTED.
- Scientific weighted completion = 20%.

Compatibility state:

- K1–K8 = PASS / CLOSED.
- `PRE_INTEGRATION_COMPATIBILITY_GATE=PASS`.
- `LIVE_HCI_AND_RAW_EVIDENCE_GATE=BLOCKED`.
- `REBOOK_GOLDEN=false`.
- `scored_runs_authorized=false`.
- `HCI_CONTROL_ACTIONS_ENABLED=false`.

Do **not** reopen K1–K8 unless a material interface change is found.

H1 remains permanently:

`VALID_W1_RECOVERY_FAILURE`

The original H1 node-local raw bundles were not recovered. Do not claim raw recovery and do not reopen salvage without a genuinely new evidence source.

RF state remains frozen:

- Q0/Q1/Q2/Q3 = `0/40/52/55 dB`;
- attenuation IDs `1 33 2 34` always coupled.

Recovery Semantics Amendment v1 is governing:

- cohort cutoff = `t_rf_restore`;
- fixed application horizon = **300 s from `t_service_ready`**;
- primary endpoint = `completeness_300` at `t_service_ready + 300 s`;
- preserve `T_service`, `T_app`, `T_total`;
- do not estimate a new horizon from B1/W1/B2 outcomes.

Protocol is v0.6.1. It includes a later advisory resource-availability preflight at:

`https://www.powderwireless.net/resinfo.php`

That page is advisory only; Portal lifecycle/manifest remains authoritative. Do not use this preflight yet because the first patch is offline only.

## Your first and only authorized patch

Execute exactly:

`AUDIT-R1 — PRE-GOLDEN SCIENTIFIC/EVIDENCE/GOVERNANCE RECONCILIATION`

This patch is **OFFLINE ONLY**.

You must **not**:

- contact POWDER;
- create/extend/terminate any POWDER experiment;
- SSH to POWDER nodes;
- run Golden;
- run H calibration;
- execute B1/W1/B2 scored experiments;
- change Q0–Q3;
- reopen H1 salvage;
- add new automation unrelated to closing the audited inconsistencies.

### AUDIT-R1 required work

1. Reconcile all general/scored analysis artifacts to the governing Recovery Semantics Amendment v1:
   - primary cohort remains `generated_ts <= t_rf_restore`;
   - endpoint observation closes at `t_service_ready + 300 s`;
   - primary endpoint is `completeness_300`;
   - `T_service`, `T_app`, `T_total` remain explicit;
   - update `analysis-plan.md`, `evidence-schema.md`, `run-matrix.yaml`, `src/wellpulse/powder_analysis.py`, relevant CLI/tests and any static checks that still encode the old `cutoff + H` semantics.

2. Explicitly supersede/retire the former W1-derived H-selection scheme. Preserve historical provenance but do not execute new W1 H-calibration trials and do not calculate a new outcome-derived horizon. Resolve ambiguous operational `H=UNFROZEN` wording consistently with the already-frozen 300 s amended application horizon.

3. Reconcile `evidence_inventory_golden_v1.txt` and finalization evidence to the qualified current path:

   `raw -> /proj/WellPulse -> controller pull -> GitHub Actions artifact -> independent download/read-back/hash -> teardown authority`

   Google Drive/rclone is not teardown-critical. It may remain only as an optional secondary mirror.

4. Audit the actual current `.github/workflows/` and root trigger surface. The old workflow registry/hygiene record predates K-fastlane and is stale. Completed K live/diagnostic workflows must not remain accidentally runnable merely because their YAML/trigger sentinels survived. Archive/disable or otherwise fail-close them as appropriate without contacting POWDER. Update `docs/WORKFLOW_REGISTRY.md` and hygiene status accordingly.

5. Retire or update `.github/workflows/wp2-h-preflight.yml`; its current green checks explicitly validate the obsolete old-H run-matrix state and must not be allowed to certify current protocol readiness.

6. Preserve historical documents but add explicit supersession control where needed. In particular, do not use these as current operational authority:
   - `docs/STATUS.md`;
   - `docs/RS7_IMPLEMENTATION_READINESS_STATUS_2026-08-26.md`;
   - old-H portions of `experiments/WP-PWD01/H_CALIBRATION_PLAN_v1.md`;
   - D-017 and horizon portions of D-019 in `docs/DECISIONS.md`.

7. Preserve protocol v0.6.1 and its resource-availability advisory preflight unchanged unless a clear defect is found.

8. Run the smallest offline/static QA needed to prove the reconciled analysis/evidence/governance contracts. Do not create a live testbed dependency to prove an offline invariant.

9. Create/update canonical reconciliation evidence and then update:
   - `HANDOVER_CURRENT.md`;
   - `docs/NEXT_GATE.md`;
   - relevant status/registry/audit records.

10. Finish the patch with a binary verdict:

   `AUDIT_R1=PASS`

   or

   `AUDIT_R1=BLOCKED:<reason>`

Then **STOP**. Do not begin the HCI/raw-evidence closure patch until I explicitly tell you to continue.

## What follows later — not authorized in AUDIT-R1

After AUDIT-R1 PASS and a separate explicit resume, the next patch is the minimal `LIVE_HCI_AND_RAW_EVIDENCE_GATE` closure:

- passive, one-way HCI only;
- orchestrator/process-emitted events only;
- `HCI_CONTROL_ACTIONS_ENABLED=false`;
- exact mandatory raw inventory;
- no independent unqualified live probe;
- no in-run/background `/proj` checkpoint during protected science unless separately benchmarked non-perturbing;
- controller-side verified off-POWDER finalization before teardown authority.

That later patch must also STOP before Golden.

Only after a further explicit authorization may one non-scored Golden reservation be booked, preceded by the advisory `resinfo.php` availability check.

## Mission discipline

This is a scientific project, not an automation project. Infrastructure work is permitted only when it directly protects or enables the next scientific result.

Shortest mission path:

`AUDIT-R1 -> HCI/raw gate -> resource availability preflight -> one clean non-scored Golden -> WP2 scientific closure/scored authorization -> WP3 conducted-RF campaign -> WP4 OTA replication -> WP5 analysis/artifact/manuscript`

At every patch boundary:

`execute declared patch -> PASS/BLOCKED -> update canonical handover -> STOP`

---
