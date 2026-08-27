# WellPulse — Current Handover

Last updated: 2026-08-27 after repository Cleanup Patch C2.

## Executive state

- Canonical repository: `aayoubMSA/WellPulse`, branch `main`.
- FIT IoT-LAB scientific layer: **FINAL PASS**.
- POWDER G0–G5 infrastructure/RF qualification: **PASS**.
- RF calibration: **PASS / FROZEN**.
- Recovery-semantics RS-2..RS-7: **PASS / frozen**.
- WP2: **ACTIVE — GOLDEN REHEARSAL NOT YET PASSED**.
- `H = UNFROZEN`.
- `scored_runs_authorized = false`.
- Scientific weighted completion remains **20%**; infrastructure/recovery work does not earn scientific completion.
- `REBOOK_GOLDEN=false`.

## Current frontier

Experiment `WP-GOLDEN-A3`, UUID `357f3275-403d-491a-906f-99677bdf454f`, is expired/removed and must not be reused.

### Attempt 6

- Workflow run: `33067316888`.
- G0..G6: **PASS**.
- G7: **FAIL-CLOSED / diagnostic noncanonical**.
- Root contamination: a workflow labelled read-only invoked `tmcc attenuator <id>` during G7; POWDER reported `changing attenuation`.
- G8/G9/G10 were not reached.
- Scored: **NO**.

### Attempt 7

- Workflow run: `33069500256`.
- Static/no-scored and encrypted Drive pre-mutation gates passed.
- Stopped before science because Portal API returned `404 No such experiment` for A3.
- Scored: **NO**.

## Repository hygiene program

Patch discipline is mandatory:

`execute one patch -> PASS/BLOCKED -> update handover/status -> STOP -> resume only on explicit user instruction`

### C0 — Inventory / contamination classification

**PASS**.

### C1 — Archive expired A3 workflows and triggers

**PASS**.

- Commit: `169b5632d2db20a9cda0ac7cc2633f68b2316024`.
- 12 A3-specific workflows archived from `.github/workflows/`.
- 12 A3 request/trigger files archived from active locations.
- Provenance retained; no scientific evidence deleted.

### C2 — Consolidate legacy FIT workflows

**PASS**.

Evidence basis: the FIT scientific layer is formally closed with `FINAL FIT GATE: PASS`, final run `32628193889`, 18/18 reconciliation PASS, and canonical results in `experiments/WP-RT01/FINAL_RESULTS_2026-08-23.md`.

Actions completed:

- Created archive registry: `archive/workflows/fit-final-2026-08-23/README.md`.
- Archived all 16 FIT-specific GitHub Actions workflows from `.github/workflows/` into `archive/workflows/fit-final-2026-08-23/`.
- The canonical final workflow is preserved as `archive/workflows/fit-final-2026-08-23/fit-wp-rt01-final.yml`.
- Smoke, diagnostic, pre-final, portability, and dry-run variants are preserved byte-for-byte for audit/reproducibility only.
- No FIT workflow remains in the active `.github/workflows/` directory.
- No FIT scientific evidence, scripts, artifacts, or Git history were deleted.

Key commits:

- `809409c292feb586d9f23b99a0803d7e6c924ce8` — document FIT archive provenance.
- `4d10df3bc6de3492d661d34dee51599452d6eed1` — archive closed FIT workflows after final PASS.

Cleanup program progress: **3/5 patches closed = 60%**.

Exact next cleanup patch: **C3 — classify/archive obsolete POWDER diagnostics/probes and stale trigger paths**.

Do not start C3 until the user explicitly resumes.

## H1 GitHub salvage state

The H1 raw record-level bundles were **not recovered from GitHub Actions**.

Verified state:

- H1 result commit had no associated Actions workflow run.
- H1 archive-hash commit had no associated Actions workflow run.
- Relevant pre-H1 SSH workflow inspected had zero uploaded Actions artifacts.
- GitHub does preserve valuable derived/live-captured evidence: sender summary, timing, generated/cohort/pending/inflight counts, network checks, failure chronology, recovery observations, archive paths, and hashes.

Therefore:

- `H1_FULL_RAW_FROM_GITHUB=NOT_RECOVERED`
- `H1_DERIVED_LOG_EVIDENCE=AVAILABLE`

A bounded H1-GitHub Salvage Patch remains planned after repository cleanup unless explicitly reprioritized.

## Dominant integration rule

Before any future GitHub Actions ↔ POWDER live integration, the Pre-Integration Compatibility Gate must PASS. Unknown command side effects are treated as mutating/unsafe.

The additional live-experiment HCI/raw-evidence gate is also mandatory. The HCI must remain passive and non-authoritative; raw data remain authoritative and must be frozen, hashed, copied to persistent `/proj/WellPulse`, copied off POWDER, read-back verified, and recorded before teardown.

Required before teardown:

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

**STOP after C2 handover closure.**

On the next explicit user resume:

1. Execute **C3 only** — classify/archive obsolete POWDER diagnostics/probes and stale trigger paths.
2. Close C3 with PASS/BLOCKED.
3. Update this handover/status.
4. STOP again.

No POWDER reservation or scientific run is authorized during repository cleanup.

## Handover acceptance test

A replacement agent is ready only if it can state:

- A3 is expired/removed and must not be reused.
- Attempt 6 is diagnostic noncanonical; Attempt 7 never reached science.
- No scored run occurred.
- C1 archived A3-specific workflows/triggers.
- C2 archived all 16 FIT-specific workflows because FIT is scientifically FINAL PASS; no FIT workflow remains active.
- Repository cleanup is 60% complete and C3 is next.
- H1 full raw data were not recovered from Actions, while derived/log evidence remains available.
- Every patch must end in a handover update and STOP.
- Pre-Integration and Live-HCI/Raw-Evidence gates remain mandatory before any new POWDER booking.
- `H=UNFROZEN`, `scored_runs_authorized=false`, and `REBOOK_GOLDEN=false` remain mandatory.
