# WellPulse — Current Handover

Last updated: 2026-08-27 after repository Cleanup Patch C4.

## Executive state

- Canonical repository: `aayoubMSA/WellPulse`, branch `main`.
- FIT IoT-LAB scientific layer: **FINAL PASS**.
- POWDER G0–G5 infrastructure/RF qualification: **PASS**.
- RF calibration: **PASS / FROZEN**.
- Recovery-semantics RS-2..RS-7: **PASS / frozen**.
- WP2: **ACTIVE — GOLDEN REHEARSAL NOT YET PASSED**.
- Scientific weighted completion: **20%**.
- Repository workflow cleanup: **100% — C0..C4 PASS**.
- `H = UNFROZEN`.
- `scored_runs_authorized = false`.
- `REBOOK_GOLDEN=false`.

## Current scientific frontier

Experiment `WP-GOLDEN-A3`, UUID `357f3275-403d-491a-906f-99677bdf454f`, is expired/removed and must not be reused.

- Attempt 6: G0..G6 PASS; G7 became `DIAGNOSTIC_NONCANONICAL` because a supposedly read-only attenuator action had mutation semantics (`changing attenuation`). G8/G9/G10 were not reached. Scored: NO.
- Attempt 7: static/no-scored and encrypted Drive pre-mutation gates passed, then stopped before science because A3 no longer existed. Scored: NO.

No new POWDER reservation or live experiment is authorized until both mandatory integration gates PASS.

## Mandatory patch discipline

All work remains bounded:

`execute one patch -> PASS/BLOCKED -> update handover/status -> STOP -> resume only on explicit user instruction`

## Repository hygiene program — CLOSED

### C0 — Inventory / contamination classification

**PASS**.

### C1 — Expired A3 workflow/trigger archival

**PASS**.

- 12 A3-specific workflows archived.
- 12 A3-specific request/trigger files archived.
- Key commit: `169b5632d2db20a9cda0ac7cc2633f68b2316024`.

### C2 — Legacy FIT consolidation

**PASS**.

- 16 FIT-specific workflows archived after `FINAL FIT GATE: PASS` and 18/18 final reconciliation PASS.
- Canonical final FIT workflow retained in `archive/workflows/fit-final-2026-08-23/`.
- No FIT workflow remains active.
- Key archive commit: `4d10df3bc6de3492d661d34dee51599452d6eed1`.

### C3 — Legacy/live POWDER workflow and trigger archival

**PASS**.

- 22 live/historical POWDER workflows archived under `archive/workflows/powder-legacy-2026-08/`.
- 20 stale POWDER/live-allocation trigger/request files archived under `archive/triggers/powder-legacy-2026-08/`.
- No active workflow now allocates, probes, SSHes into, controls, terminates, or independently observes live POWDER.
- Execution commit: `1cde375d07504567afe78383db3f3eb6a69e46b5`.

### C4 — Canonical Workflow Registry + final hygiene QA

**PASS**.

Canonical registry:

- `docs/WORKFLOW_REGISTRY.md`
- commit `26df27c09c540f57d79dc45f8428624f0d36a8da`

Final QA:

- `docs/REPOSITORY_HYGIENE_FINAL_QA_2026-08-27.md`
- commit `439a3d66a5981d37bedfa36b46a2b45a7374dae7`

C4 verified:

- exactly six workflows remain under `.github/workflows/`;
- all six are local/offline/static only;
- exactly four root sentinel trigger files remain and each maps to an active local/static workflow;
- no orphaned live POWDER trigger/request remains active;
- 50 workflow files in total were removed from the active Actions path across C1–C3 while provenance was preserved;
- historical workflow names/runs may remain visible in the GitHub Actions sidebar/history and are audit history, not approved active workflow definitions;
- old archived live-testbed runs must not be manually re-run as a workaround around current gates.

Current active workflow set:

1. `local-gate-once.yml`
2. `local-unit-tests.yml`
3. `wp2-b2-semantics.yml`
4. `wp2-golden-offline-qa.yml`
5. `wp2-h-preflight.yml`
6. `wp2-preintegration-static.yml`

Repository cleanup is therefore **CLOSED / 100%**.

## H1 GitHub salvage state

The H1 full raw record-level bundles were **not recovered from GitHub Actions**.

Verified state:

- H1 result commit had no associated Actions workflow run.
- H1 archive-hash commit had no associated Actions workflow run.
- Relevant pre-H1 SSH workflow inspected had zero uploaded Actions artifacts.
- GitHub does preserve useful derived/live-captured H1 evidence: sender summary, timestamps, generated/cohort/pending/inflight counts, network checks, failure chronology, recovery observations, archive paths, runtime fingerprints, and SHA-256 hashes.

Therefore:

- `H1_FULL_RAW_FROM_GITHUB=NOT_RECOVERED`
- `H1_DERIVED_LOG_EVIDENCE=AVAILABLE`
- full record-level reconstruction from GitHub alone is not currently supported.

## Dominant integration and evidence rules

Before any future GitHub Actions <-> POWDER live integration:

- `PRE_INTEGRATION_COMPATIBILITY_GATE=PASS` is mandatory.
- `LIVE_HCI_AND_RAW_EVIDENCE_GATE=PASS` is mandatory.
- unknown side effects are treated as mutating/unsafe;
- HCI must be passive, one-way, and non-authoritative;
- raw scientific data remain authoritative;
- before teardown require:
  - `RAW_EVIDENCE_COMPLETE=PASS`
  - `EVIDENCE_ESCROW_GATE=PASS`
  - `TEARDOWN_AUTHORIZED=YES`

The compatibility matrix remains **BLOCKED**. Repository cleanup did not resolve runtime/platform compatibility requirements such as immutable live-integration pins, Portal API exact semantics/revision, exact POWDER runtime versions, Drive OAuth/rclone validation, `/proj/WellPulse` persistence validation, HCI runtime acceptance, or Golden reservation time-budget proof.

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
3. `docs/WORKFLOW_REGISTRY.md`
4. `docs/REPOSITORY_HYGIENE_FINAL_QA_2026-08-27.md`
5. `AGENTS.md`
6. `docs/PRE_INTEGRATION_COMPATIBILITY_GATE.md`
7. `docs/LIVE_EXPERIMENT_HCI_AND_RAW_EVIDENCE.md`
8. `experiments/WP-PWD01/GOLDEN_E2E_REHEARSAL_v1.md`
9. `docs/CONSORTIUM_WP2_RECOVERY_SEMANTICS_GATE_2026-08-26.md`
10. `evidence/powder/wp2-h1-valid-recovery-failure-2026-08-26.md`
11. `experiments/WP-PWD01/protocol.md`
12. `experiments/WP-PWD01/evidence-schema.md`

## Exact next action

**STOP after C4 handover closure.**

On the next explicit user resume, execute exactly one bounded patch:

### H1-GitHub Salvage

Consolidate every surviving H1 Git/GitHub-Actions/log-derived datum into one reconstruction package with explicit evidence classes:

- raw evidence actually available;
- derived/log-captured evidence;
- hashes and provenance pointers;
- unrecovered/missing raw artifacts;
- reconstruction limits.

Do not label derived evidence as raw data and do not alter H1's frozen classification.

After that patch: update this handover and STOP again.

No POWDER reservation or scientific run is authorized during H1 salvage.

## Handover acceptance test

A replacement agent is ready only if it can state:

- A3 is expired/removed and must not be reused.
- Attempt 6 is diagnostic noncanonical; Attempt 7 never reached science.
- No scored run occurred.
- Repository cleanup C0–C4 is complete at 100%.
- 50 historical/unsafe workflow files were removed from the active workflow path while provenance was preserved.
- Exactly six local/offline/static workflows remain active and none interacts with live POWDER.
- Old Actions sidebar entries/runs are historical audit records, not approved active workflow definitions.
- H1 full raw data were not recovered from GitHub Actions, while derived/log evidence remains available.
- H1-GitHub Salvage is the next bounded patch.
- Every patch must end in a handover update and STOP.
- Pre-Integration and Live-HCI/Raw-Evidence gates remain mandatory before any new POWDER booking.
- `H=UNFROZEN`, `scored_runs_authorized=false`, and `REBOOK_GOLDEN=false` remain mandatory.
