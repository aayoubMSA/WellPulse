# WellPulse — Current Handover

Last updated: 2026-08-27 after repository Cleanup Patch C3.

## Executive state

- Canonical repository: `aayoubMSA/WellPulse`, branch `main`.
- FIT IoT-LAB scientific layer: **FINAL PASS**.
- POWDER G0–G5 infrastructure/RF qualification: **PASS**.
- RF calibration: **PASS / FROZEN**.
- Recovery-semantics RS-2..RS-7: **PASS / frozen**.
- WP2: **ACTIVE — GOLDEN REHEARSAL NOT YET PASSED**.
- Scientific weighted completion: **20%**.
- `H = UNFROZEN`.
- `scored_runs_authorized = false`.
- `REBOOK_GOLDEN=false`.

## Current scientific frontier

Experiment `WP-GOLDEN-A3`, UUID `357f3275-403d-491a-906f-99677bdf454f`, is expired/removed and must not be reused.

- Attempt 6: G0..G6 PASS; G7 became `DIAGNOSTIC_NONCANONICAL` because a supposedly read-only attenuator status action had mutation semantics. G8/G9/G10 were not reached. Scored: NO.
- Attempt 7: request/static and encrypted Drive pre-mutation gates passed, then stopped before science because A3 no longer existed. Scored: NO.

No new POWDER reservation or live experiment is authorized until the Pre-Integration Compatibility Gate and Live-HCI/Raw-Evidence Gate both PASS.

## Mandatory patch discipline

All work remains bounded:

`execute one patch -> PASS/BLOCKED -> update handover/status -> STOP -> resume only on explicit user instruction`

## Repository hygiene program

### C0 — Inventory / contamination classification

**PASS**.

### C1 — Archive expired A3 workflows and triggers

**PASS**.

- Commit: `169b5632d2db20a9cda0ac7cc2633f68b2316024`.
- 12 A3-specific workflows archived.
- 12 A3-specific request/trigger files archived.
- No scientific provenance deleted.

### C2 — Consolidate legacy FIT workflows

**PASS**.

- FIT scientific evidence remains frozen at `FINAL FIT GATE: PASS`, 18/18 final reconciliation PASS.
- All 16 FIT-specific workflows archived under `archive/workflows/fit-final-2026-08-23/`.
- Canonical final workflow preserved as `fit-wp-rt01-final.yml` in that archive.
- No FIT workflow remains active.
- Key archive commit: `4d10df3bc6de3492d661d34dee51599452d6eed1`.

### C3 — Archive obsolete POWDER diagnostics/probes and stale triggers

**PASS**.

Evidence basis: current science requires `REBOOK_GOLDEN=false`, verified platform compatibility before live integration, and no unqualified live probes. Historical names such as `readonly`, `observer`, `status`, or `probe` are not proof of non-mutating semantics.

Actions completed:

- Archived **22 live/historical POWDER workflows** from `.github/workflows/` into `archive/workflows/powder-legacy-2026-08/`.
- Archived **20 stale POWDER/live-allocation trigger/request files** into `archive/triggers/powder-legacy-2026-08/`.
- Removed old API probe/smoke, cleanup, observer, G3 attach/simstack, handover, H-calibration scheduling/status/release, lifecycle, live-discovery, live-SSH, plumbing, profile-probe, SSH-secret/key checks, early-window allocation, and POWDER-status workflows from the active workflow path.
- Preserved all archived blobs and Git history; nothing scientific was deleted.
- C3 execution commit: `1cde375d07504567afe78383db3f3eb6a69e46b5`.
- Archive provenance documents are under:
  - `archive/workflows/powder-legacy-2026-08/`
  - `archive/triggers/powder-legacy-2026-08/`

### Active workflow set after C3

Exactly six workflows remain active in `.github/workflows/`:

1. `local-gate-once.yml`
2. `local-unit-tests.yml`
3. `wp2-b2-semantics.yml` — local broker semantics; POWDER interaction NONE
4. `wp2-golden-offline-qa.yml` — offline Golden QA
5. `wp2-h-preflight.yml` — local preflight; POWDER resource interaction NONE
6. `wp2-preintegration-static.yml` — static compatibility checks

Therefore no currently active GitHub Actions workflow allocates, probes, mutates, controls, or observes a live POWDER experiment.

Repository cleanup progress: **4/5 patches closed = 80%**.

Exact next cleanup patch: **C4 — Canonical Workflow Registry + final repository-hygiene QA**.

C4 must verify that every active workflow has an explicit purpose/authority classification, every trigger maps to an active workflow, archived workflows are non-runnable from `.github/workflows`, and no stale live POWDER trigger/path remains. C4 may create the canonical workflow registry but must not re-enable live POWDER execution.

Do not start C4 until the user explicitly resumes.

## H1 GitHub salvage state

The H1 full raw record-level bundles were **not recovered from GitHub Actions**.

Verified state:

- H1 result commit had no associated Actions workflow run.
- H1 archive-hash commit had no associated Actions workflow run.
- Relevant pre-H1 SSH workflow inspected had zero uploaded Actions artifacts.
- GitHub preserves useful derived/live-captured H1 evidence: sender summary, timestamps, generated/cohort/pending/inflight counts, network checks, failure chronology, recovery observations, archive paths, and SHA-256 hashes.

Therefore:

- `H1_FULL_RAW_FROM_GITHUB=NOT_RECOVERED`
- `H1_DERIVED_LOG_EVIDENCE=AVAILABLE`

A bounded H1-GitHub Salvage Patch remains planned after repository cleanup unless explicitly reprioritized.

## Dominant integration and evidence rules

Before any future GitHub Actions ↔ POWDER live integration:

- `PRE_INTEGRATION_COMPATIBILITY_GATE=PASS` is mandatory.
- `LIVE_HCI_AND_RAW_EVIDENCE_GATE=PASS` is mandatory.
- Unknown side effects are treated as mutating/unsafe.
- HCI must be passive, one-way, and non-authoritative.
- Raw scientific data remain authoritative.
- Before teardown require:
  - `RAW_EVIDENCE_COMPLETE=PASS`
  - `EVIDENCE_ESCROW_GATE=PASS`
  - `TEARDOWN_AUTHORIZED=YES`

## Frozen scientific state

- H1 remains `VALID_W1_RECOVERY_FAILURE`; do not reclassify it.
- Q0/Q1/Q2/Q3 remain `0/40/52/55 dB`.
- Attenuation IDs `1 33 2 34` remain coupled.
- Recovery-semantics amendment v1 and protocol v0.6 remain frozen.
- Primary cohort cutoff remains `t_rf_restore`.
- Application horizon remains 300 s from `t_service_ready`.
- No scored B1/W1/B2 run is authorized.
- H1 raw record-level bundles remain unavailable from user-accessible persistent storage.

## Mandatory current read order

1. `HANDOVER_CURRENT.md`
2. `docs/NEXT_GATE.md`
3. `AGENTS.md`
4. `docs/PRE_INTEGRATION_COMPATIBILITY_GATE.md`
5. `docs/LIVE_EXPERIMENT_HCI_AND_RAW_EVIDENCE.md`
6. `experiments/WP-PWD01/GOLDEN_E2E_REHEARSAL_v1.md`
7. `docs/CONSORTIUM_WP2_RECOVERY_SEMANTICS_GATE_2026-08-26.md`
8. `evidence/powder/wp2-h1-valid-recovery-failure-2026-08-26.md`
9. `experiments/WP-PWD01/protocol.md`
10. `experiments/WP-PWD01/evidence-schema.md`

## Exact next action

**STOP after C3 handover closure.**

On the next explicit user resume:

1. Execute **C4 only — Canonical Workflow Registry + final repository-hygiene QA**.
2. Close C4 with PASS/BLOCKED.
3. Update this handover/status.
4. STOP again.

No POWDER reservation or scientific run is authorized during repository cleanup.

## Handover acceptance test

A replacement agent is ready only if it can state:

- A3 is expired/removed and must not be reused.
- Attempt 6 is diagnostic noncanonical; Attempt 7 never reached science.
- No scored run occurred.
- C1 archived A3-specific workflows/triggers.
- C2 archived all FIT workflows after FIT FINAL PASS.
- C3 archived 22 legacy/live POWDER workflows and 20 stale POWDER trigger/request files.
- Exactly six local/offline/static workflows remain active and none interacts with live POWDER.
- Repository cleanup is 80% complete and C4 is next.
- H1 full raw data were not recovered from Actions, while derived/log evidence remains available.
- Every patch must end in a handover update and STOP.
- Pre-Integration and Live-HCI/Raw-Evidence gates remain mandatory before any new POWDER booking.
- `H=UNFROZEN`, `scored_runs_authorized=false`, and `REBOOK_GOLDEN=false` remain mandatory.
