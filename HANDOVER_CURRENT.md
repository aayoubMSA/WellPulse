# WellPulse — Current Handover

Last updated: 2026-08-27 after Golden A3 attempts 6–7 and expiration/removal of experiment A3.

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

1. `.github/workflows/wp2-a3-attempt6-status-readonly.yml` no longer queries live attenuators; it relies only on recorded evidence for RF status.
2. `scripts/wp2_golden_service_ready_probe.sh` now uses `openssl s_client -brief` so TLS verification evidence is retained without verbose TLS session-secret material.
3. `scripts/wp2_golden_orchestrator.sh` uses the same bounded TLS logging at the Q0 TLS gate.

## New dominant integration rule

Before any future connection between two platforms/modules (for example GitHub Actions ↔ POWDER, repository automation ↔ remote testbed, data pipeline ↔ external API), agents must pass the **Pre-Integration Compatibility Gate** defined in `docs/PRE_INTEGRATION_COMPATIBILITY_GATE.md` and summarized in root `AGENTS.md`.

The gate is mandatory before implementation or live integration. It covers contracts/APIs, hardware and topology, software/runtime types and exact versions, authentication/secrets, lifecycle/reservation/timeouts, commands and side effects, data/schema/time semantics, network/ports/TLS, storage/persistence, observability/redaction, concurrency/idempotency, failure modes, rollback/cleanup, quotas/rate limits, evidence requirements, and ownership boundaries.

A command or API whose side-effect semantics are not verified must be treated as **MUTATING/UNSAFE**, not read-only.

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

1. Do not attempt to reuse A3.
2. Complete the Pre-Integration Compatibility Gate specifically for the GitHub Actions ↔ POWDER interface using verified platform contracts and exact runtime/profile versions.
3. Correct any remaining integration assumptions exposed by that review.
4. Only then request/instantiate the smallest new non-scored Golden reservation/experiment.
5. Run one clean Golden G0–G10 rehearsal with no independent live probes during the scientific window.
6. Keep `scored_runs_authorized=false` until Golden G10 and evidence escrow both PASS and H is subsequently requalified.

## Handover acceptance test

A replacement agent is ready only if it can state:

- A3 is expired/removed and must not be reused;
- Attempt 6 is diagnostic noncanonical because a supposedly read-only attenuator query had mutation semantics during G7;
- Attempt 7 never reached science because A3 no longer existed;
- no scored run occurred;
- the Pre-Integration Compatibility Gate is mandatory before the next cross-platform integration;
- H1 adverse evidence and the fail-closed Evidence Escrow Gate remain preserved;
- `H=UNFROZEN` and `scored_runs_authorized=false` remain mandatory.
