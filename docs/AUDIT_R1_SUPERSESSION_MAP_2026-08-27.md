# WellPulse AUDIT-R1 Canonical Supersession Map — 2026-08-27

Status: **ACTIVE CANONICAL CONTROL RECORD / EXTENDED AFTER WP2-P5**

Purpose: preserve historical provenance while preventing pre-amendment or pre-P5 status/readiness text from issuing current operational instructions.

## Authority order for the current WP2 frontier

1. `HANDOVER_CURRENT.md`
2. `docs/WP2_P5_HCI_RAW_EVIDENCE_CLOSURE_2026-08-27.md`
3. `docs/PROJECT_AUDIT_HANDOVER_2026-08-27.md` including AUDIT-R1 closure
4. `experiments/WP-PWD01/RECOVERY_SEMANTICS_AMENDMENT_v1.md`
5. `experiments/WP-PWD01/protocol.md` v0.6.1
6. `docs/NEXT_GATE.md`
7. `docs/MILESTONE_STATUS.md`
8. `docs/K8_PREINTEGRATION_COMPATIBILITY_CLOSURE_2026-08-27.md`
9. `docs/LIVE_EXPERIMENT_HCI_AND_RAW_EVIDENCE.md` as the frozen P5 passive-HCI/raw-evidence contract

## Superseded operational text

| Historical source | Historical content retained | Current status / supersession |
|---|---|---|
| `docs/STATUS.md` | post-H1/pre-amendment status and diagnosis | **PROVENANCE ONLY.** `H=UNFROZEN`, RS-1..RS-7 next-action text, and the claim that original H1 raw bundles remain preserved/accesssible are superseded. Original H1 node-local raw bundles were **not recovered** after teardown. |
| `docs/RS7_IMPLEMENTATION_READINESS_STATUS_2026-08-26.md` | pre-K8 readiness decision | **PROVENANCE ONLY.** `RESERVE=true` and Google Drive/rclone as teardown-critical are superseded. Current `REBOOK_GOLDEN=false`; controller/GitHub artifact round-trip is the qualified off-POWDER evidence authority. |
| `experiments/WP-PWD01/H_CALIBRATION_PLAN_v1.md` | original W1-derived H-calibration design | **PROVENANCE ONLY / DO NOT EXECUTE.** Outcome-derived W1 H selection is retired. Current prospective `H_app=300 s` is anchored at `t_service_ready`. |
| `docs/DECISIONS.md` D-017 | original W1-derived H selection | **SUPERSEDED for future execution** by Recovery Semantics Amendment v1. Preserve D-017 only as historical decision provenance. |
| `docs/DECISIONS.md` D-019 horizon paragraphs | common H language tied to old calibration | **SUPERSEDED only for horizon-selection semantics.** D-019's failure-domain interpretation, completeness-only precision rule, and claim boundaries remain in force. Current horizon is prospectively fixed `H_app=300 s` from `t_service_ready`; no W1/Golden/scored outcome may re-estimate it. |
| `docs/REPOSITORY_HYGIENE_FINAL_QA_2026-08-27.md` original C4 snapshot | six-workflow/four-trigger snapshot at C4 time | **REFRESHED by AUDIT-R1 and retained by P5.** Current verified bounded set remains six workflows/four sentinels; no new live HCI workflow was introduced. |
| pre-P5 copies of `HANDOVER_CURRENT.md`, `docs/NEXT_GATE.md`, `docs/MILESTONE_STATUS.md`, `docs/WORKFLOW_REGISTRY.md` | `LIVE_HCI_AND_RAW_EVIDENCE_GATE=BLOCKED` or `BLOCKED_NOT_STARTED` | **SUPERSEDED by WP2-P5 closure.** Current gate is `LIVE_HCI_AND_RAW_EVIDENCE_GATE=PASS`; this does not alter `REBOOK_GOLDEN=false` or scored authorization. |
| pre-closure status line in `docs/LIVE_EXPERIMENT_HCI_AND_RAW_EVIDENCE.md` | HCI/raw design open/pending QA | **SUPERSEDED by WP2-P5 PASS.** The same file is now the frozen passive-HCI/raw-evidence contract. |

## Frozen scientific facts not superseded

- Q0/Q1/Q2/Q3 = `0/40/52/55 dB`.
- Attenuation IDs `1 33 2 34` remain coupled.
- H1 remains `VALID_W1_RECOVERY_FAILURE`; non-scored; not replaceable/relabelable.
- K1-K8 remain PASS/CLOSED absent a material interface change.
- Primary cohort freezes at `t_rf_restore`.
- `t_rf_restore`, `t_service_ready`, `t_app_complete` remain distinct.
- `T_service`, `T_app`, `T_total` remain preserved.
- Primary endpoint is `completeness_300` at `t_service_ready + 300 s`.
- `HCI_CONTROL_ACTIONS_ENABLED=false`.
- `scored_runs_authorized=false`.
- `REBOOK_GOLDEN=false` until a **separate explicit user continuation** authorizes moving beyond the current STOP to the advisory resource preflight and P6 Golden attempt.

## P5 observer/evidence authority

Current HCI rule:

`orchestrator-owned state -> passive HCI JSONL/stdout`

Never:

`HCI -> SSH/API/tmcc/live probe/control -> experiment`

`orchestration/hci_events.jsonl` is conditional/non-authoritative observer evidence. `orchestration/gate_events.jsonl` plus the frozen raw inventory remain authoritative.

## Evidence architecture

Mandatory qualified path:

`POWDER raw -> /proj/WellPulse persistent escrow -> controller pull -> GitHub Actions artifact -> independent controller download/read-back -> outer + internal SHA-256 verification -> teardown authority`

Google Drive/rclone is optional secondary mirroring only unless explicitly re-qualified by a future amendment.
