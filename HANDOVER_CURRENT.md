# WellPulse — Current Handover

Last updated: 2026-08-27 after Golden A3 attempts 6–7, A3 expiration/removal, H1 GitHub salvage check, and repository Cleanup Patch 1.

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

## Current frontier

The approved Golden reservation was used for non-scored rehearsal attempts only. Experiment `WP-GOLDEN-A3`, UUID `357f3275-403d-491a-906f-99677bdf454f`, is no longer resolvable by the POWDER Portal API as of `2026-08-27T11:55:56Z` (`404 No such experiment`). Treat A3 as expired/removed and **do not attempt to reuse it**.

### Attempt 6

- Workflow run: `33067316888`.
- Run ID: `wp2-golden-a3-gh-33067316888-20260827T112727Z`.
- G0..G6: **PASS**.
- G7: **FAIL-CLOSED / diagnostic noncanonical**.
- Scored: **NO**.
- G8/G9/G10: **NOT REACHED**.
- Root contamination: a workflow labelled read-only invoked `tmcc attenuator <id>` during G7; POWDER output reported `changing attenuation`. This invalidated the fixed 300 s observation as a canonical Golden rehearsal.
- A targeted fail-close terminated the Attempt 6 sender and prevented progression to G8–G10.

### Attempt 7

- Workflow run: `33069500256`.
- Trigger commit: `d195f00121828f052025a898ce952708176b8322`.
- Request/static no-create/no-scored gate: **PASS**.
- Encrypted Google Drive pre-mutation gate: **PASS**.
- Clean Q0 preparation: **STOPPED BEFORE MUTATION/SCIENCE** because the Portal API returned `404 No such experiment` for A3.
- Golden adopter: **SKIPPED**.
- Scored run: **NO**.

## Immediate technical hardening already applied

1. The former `.github/workflows/wp2-a3-attempt6-status-readonly.yml` was hardened to remove live attenuator queries and, after A3 expiration, was archived with the other A3-specific workflows so it cannot be accidentally retriggered as an active workflow.
2. `scripts/wp2_golden_service_ready_probe.sh` now uses `openssl s_client -brief` so TLS verification evidence is retained without verbose TLS session-secret material.
3. `scripts/wp2_golden_orchestrator.sh` uses the same bounded TLS logging at the Q0 TLS gate.

## Repository hygiene — Cleanup Patch 1

Cleanup Patch 1 is **PASS**.

- Commit: `169b5632d2db20a9cda0ac7cc2633f68b2316024` (`Archive expired A3 workflows and triggers`).
- Twelve A3-specific workflows were removed from `.github/workflows/` and preserved under `archive/workflows/a3-2026-08-27/`.
- Twelve A3-specific request/trigger files were removed from active locations and preserved under `archive/triggers/a3-2026-08-27/`.
- No scientific evidence, provenance, or Git history was deleted.
- Further cleanup remains pending; legacy FIT/POWDER diagnostics and older workflow variants must be classified before archival.

Repository-cleanup next patch is **C2 — classify/consolidate legacy FIT workflows**, but it must not start until the user explicitly resumes after this handover stop.

## H1 GitHub salvage check

The H1 raw record-level bundles were **not recovered from GitHub Actions**.

Verified findings:

- The commit recording the H1 valid recovery failure (`9cd7789a8960fd396ba35806127c16251ea8574a`) had no associated Actions workflow run.
- The commit recording H1/recovery archive hashes (`375f767bae237729458f558b1c64c60633c00673`) had no associated Actions workflow run.
- The relevant pre-H1 SSH workflow inspected had zero uploaded Actions artifacts.
- GitHub nevertheless preserves valuable derived/live-captured H1 evidence: sender summary, timestamps, generated/cohort/pending/inflight counts, network checks, failure chronology, recovery observations, archive paths, and SHA-256 hashes.

Therefore:

- `H1_FULL_RAW_FROM_GITHUB=NOT_RECOVERED`
- `H1_DERIVED_LOG_EVIDENCE=AVAILABLE`
- Full record-level reconstruction from GitHub alone is not currently supported.

A later bounded **H1-GitHub Salvage Patch** may consolidate every surviving derived/log fragment into one explicit reconstruction package, but it is not the current patch.

## New dominant integration rule

Before any future connection between two platforms/modules (for example GitHub Actions ↔ POWDER, repository automation ↔ remote testbed, data pipeline ↔ external API), agents must pass the **Pre-Integration Compatibility Gate** defined in `docs/PRE_INTEGRATION_COMPATIBILITY_GATE.md` and summarized in root `AGENTS.md`.

The gate is mandatory before implementation or live integration. It covers contracts/APIs, hardware and topology, software/runtime types and exact versions, authentication/secrets, lifecycle/reservation/timeouts, commands and side effects, data/schema/time semantics, network/ports/TLS, storage/persistence, observability/redaction, concurrency/idempotency, failure modes, rollback/cleanup, quotas/rate limits, evidence requirements, and ownership boundaries.

A command or API whose side-effect semantics are not verified must be treated as **MUTATING/UNSAFE**, not read-only.

## Mandatory patch execution discipline

All future work in this branch must use bounded patches.

For every patch:

1. execute only the declared patch scope;
2. finish with an explicit `PASS` or `BLOCKED` gate;
3. update the canonical handover/status with the result, evidence, current frontier, and exact next patch;
4. **STOP** after the handover update;
5. do not start the next patch until the user explicitly resumes/continues.

This rule applies even when the next patch is obvious and immediately executable. The purpose is to preserve a clean recovery point and prevent work from running ahead of the canonical handover.

## Mandatory current read order

1. `HANDOVER_CURRENT.md`
2. `docs/NEXT_GATE.md`
3. `AGENTS.md`
4. `docs/PRE_INTEGRATION_COMPATIBILITY_GATE.md`
5. `experiments/WP-PWD01/GOLDEN_E2E_REHEARSAL_v1.md`
6. `docs/CONSORTIUM_WP2_RECOVERY_SEMANTICS_GATE_2026-08-26.md`
7. `evidence/powder/wp2-h1-valid-recovery-failure-2026-08-26.md`
8. `experiments/WP-PWD01/protocol.md`
9. `experiments/WP-PWD01/evidence-schema.md`

## Frozen scientific state

- H1 remains `VALID_W1_RECOVERY_FAILURE`; do not reclassify it.
- Q0/Q1/Q2/Q3 remain `0/40/52/55 dB`; attenuation IDs `1 33 2 34` remain coupled.
- Recovery-semantics amendment v1 and protocol v0.6 remain frozen.
- Primary cohort cutoff remains `t_rf_restore`.
- Application horizon remains fixed at 300 s from `t_service_ready`.
- No scored B1/W1/B2 run is authorized.
- H1 raw record-level bundles remain unavailable from user-accessible persistent storage; support recovery remains separate.

## Evidence escrow rule — unchanged

Every future POWDER rehearsal/calibration/scored run must fail-closed before teardown unless all raw artifacts are frozen, hashed, copied and verified in persistent `/proj/WellPulse/evidence-escrow/...`, copied off POWDER to the approved external evidence repository, verified again, and the canonical repository records UUID/profile revision/node bindings/code/runtime/evidence locations/hashes.

Required output before teardown:

`EVIDENCE_ESCROW_GATE=PASS`

Anything else means `STOP / DO_NOT_TERMINATE`.

## Exact next action

The immediate next patch is repository hygiene, not POWDER rebooking:

1. **C2 — classify/consolidate legacy FIT workflows** and determine canonical-active vs archive-only status without deleting scientific provenance.
2. Close C2 with explicit PASS/BLOCKED and update this handover.
3. STOP.
4. On a later explicit resume, continue the cleanup sequence and then the bounded H1-GitHub Salvage Patch.
5. Pre-Integration Compatibility Gate closure remains mandatory before any new POWDER reservation/experiment.
6. Keep `scored_runs_authorized=false` until Golden G10 and evidence escrow both PASS and H is subsequently requalified.

`REBOOK_GOLDEN=false`

## Handover acceptance test

A replacement agent is ready only if it can state:

- A3 is expired/removed and must not be reused;
- Attempt 6 is diagnostic noncanonical because a supposedly read-only attenuator query had mutation semantics during G7;
- Attempt 7 never reached science because A3 no longer existed;
- no scored run occurred;
- Cleanup Patch 1 archived the A3-specific active workflows/triggers without deleting provenance;
- H1 full raw data were not recovered from GitHub Actions, while derived/log evidence remains available;
- every future patch must end with a handover update and STOP before the next patch;
- the Pre-Integration Compatibility Gate is mandatory before the next cross-platform integration;
- H1 adverse evidence and the fail-closed Evidence Escrow Gate remain preserved;
- `H=UNFROZEN` and `scored_runs_authorized=false` remain mandatory.
