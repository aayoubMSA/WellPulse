# WellPulse — New Agent Mandate — WP2-P7B

Date: 2026-08-27

## Role

You are taking ownership of the **WellPulse WP2 execution lane only** from the canonical private repository:

- repository: `aayoubMSA/WellPulse`
- branch: `main`

Do **not** reconstruct project state from conversation memory. GitHub canonical files are authoritative for scientific state, gates, provenance, and execution authority.

## Exact retrieval point

Resume exactly at:

`WP2-P7B — SINGLE NON-SCORED PRE-SCORE PHYSICAL QUALIFICATION`

Current state before P7B:

- `WP2_P6=PASS_RECOVERED_SINGLE_RUN`
- `WP2_P7_HARDENING_QA=PASS`
- `SCORED_AUTHORIZATION=BLOCKED:PRE_SCORE_PHYSICAL_QUALIFICATION_REQUIRED`
- `scored_runs_authorized=false`
- `WP2_MANAGEMENT_READINESS_PROGRESS=95/100`
- scientific weighted completion = **20%**
- WP3 remains blocked.

P7B is **NOT STARTED** and requires explicit user continuation before any POWDER contact, reservation, SSH, or mutation.

## Mandatory read order

Read completely, in this order, before taking action:

1. `HANDOVER_CURRENT.md`
2. `docs/NEW_AGENT_PROMPT_WP2_P7B_2026-08-27.md`
3. `docs/WP2_P7_SCORED_AUTHORIZATION_2026-08-27.md`
4. `docs/NEXT_GATE.md`
5. `docs/MILESTONE_STATUS.md`
6. `docs/WP2_P6_GOLDEN_CLOSURE_2026-08-27.md`
7. `evidence/powder/wp2-p6-live-status.md`
8. `experiments/WP-PWD01/PRE_SCORE_P0_AMENDMENT_2026-08-26.md`
9. `experiments/WP-PWD01/PRE_SCORE_P1_AMENDMENT_2026-08-26.md`
10. `experiments/WP-PWD01/run-matrix.yaml`
11. `experiments/WP-PWD01/RECOVERY_SEMANTICS_AMENDMENT_v1.md`
12. `experiments/WP-PWD01/protocol.md`
13. `evidence/powder/wp2-pre-h-runtime-path-qualification-2026-08-26.md`
14. `experiments/WP-PWD01/B2_SEMANTICS_GATE_v1.md`
15. `docs/K8_PREINTEGRATION_COMPATIBILITY_CLOSURE_2026-08-27.md`
16. `docs/WP2_P5_HCI_RAW_EVIDENCE_CLOSURE_2026-08-27.md`
17. `scripts/wp2_golden_prepare_management_aliases.sh`
18. `scripts/wp2_golden_orchestrator.sh`
19. `scripts/reconstruct_wp2_golden.py`
20. `scripts/wp2_golden_evidence_escrow.sh`
21. `scripts/wp2_controller_pull_persistent_escrow.sh`
22. `scripts/wp2_controller_verify_artifact_roundtrip.sh`
23. `docs/WORKFLOW_REGISTRY.md`
24. `AGENTS.md`

If any later canonical file materially contradicts an earlier historical operational note, follow the authority/supersession rules stated in `HANDOVER_CURRENT.md` and the P7 decision.

## Supporting experience sources in Google Drive

These are supporting operating doctrine, **not substitutes for GitHub canonical scientific state**:

1. **Physical Validation Asset Ledger**
   - Google Sheet ID: `1BbRSUVl1QulgEaPeoUGzT6euMb6feAxVgBTMDxmAgM0`
   - tab: `REMOTE_TESTBEDS`
   - relevant row: `RPT-006 — POWDER — University of Utah`
   - critical lesson: node-local experiment home directories are transient; mandatory scientific evidence must reach `/proj` before teardown and then receive an independently verified off-platform copy/read-back before teardown authorization.

2. **Research Operating Doctrine — Evidence-First Execution v2.1**
   - Google Doc ID: `1aq_lX4WtkFHGyzL6niN7ipdes2Eqv87fG19b1Y7-w4E`
   - use as general doctrine only where it does not weaken stricter project-specific WellPulse controls.

## Frozen scientific controls — do not reopen

Preserve all accepted scientific decisions:

- Q0/Q1/Q2/Q3 = `0/40/52/55 dB`.
- attenuation IDs `1 33 2 34` remain coupled.
- primary cohort cutoff = `t_rf_restore`.
- `t_rf_restore`, `t_service_ready`, `t_app_complete` remain distinct clocks.
- `H_app=300 s from t_service_ready`.
- primary endpoint = `completeness_300` at `t_service_ready + 300 s`.
- preserve `T_service`, `T_app`, `T_total`.
- no outcome-derived, W1-derived, Golden-derived, or scored-derived H re-estimation.
- S2/S3 clean restore order remains frozen.
- H1 remains valid adverse non-scored evidence; do not reopen H1 salvage.
- RF calibration remains frozen.
- K1-K8 remain closed absent a material interface change.
- negative/null/unfavorable outcomes remain valid evidence and never justify protocol drift or rerun selection.
- HCI remains passive: `HCI_CONTROL_ACTIONS_ENABLED=false`.

## P6/P7 facts that must be preserved

P6 closed as:

`WP2_P6=PASS_RECOVERED_SINGLE_RUN`

This means:

- one reservation only;
- one scientifically material non-scored Golden run only;
- no scientific rerun;
- protected measurement completed through G7;
- later G8/evidence-pipeline defects were recovered on the same immutable raw run;
- raw evidence reached persistent `/proj` escrow;
- controller pull + deterministic TAR + GitHub artifact upload/download + outer/internal hash verification all passed;
- teardown occurred only after verified evidence closure.

P7 then hardened the reusable path offline:

- management aliases are manifest-derived and SSH-proven before G0;
- receiver evidence transfer uses the live-qualified tar-stream path, not `scp .../receiver/.`;
- post-cohort generated traffic is separated from truly unknown record identities;
- clock authority uses `sender/rf_restore.ready`, cross-checked to the attenuation timeline;
- bounded offline closure run `33103997677` passed;
- 36/36 unit/regression tests passed;
- P7 contacted no POWDER resource and ran no science.

Do not relabel P6 as an uninterrupted clean G0-G10 automation pass. Preserve the exact `PASS_RECOVERED_SINGLE_RUN` provenance.

## Exact P7B mission

Design and execute the **minimum-information, single non-scored physical qualification reservation** needed to close the five remaining pre-score groups together:

1. **B1 physical instrumentation**
   - prove accepted/unacknowledged accounting on the real remote path;
   - no scored outcome.

2. **B1/W1 matching**
   - prove exact low-level runtime/config/path parity on POWDER;
   - B1 vs W1 difference must remain only the intended application-level durability/reconciliation mechanism.

3. **S3 restart-domain separation**
   - generator outside gateway/client restart domain;
   - 1 Hz source generation continuity through restart;
   - process restart only, not node restart;
   - W1 durable SQLite survives;
   - B1 volatile client state is destroyed/recreated with the same intended intra-run identity;
   - preserve restart timestamps/downtime and source-sequence continuity.

4. **B2 remote qualification**
   - exact Eclipse Paho Java 1.2.5 durable-client implementation;
   - same POWDER LTE/TLS/payload/evidence path;
   - runtime/path/restart mechanics proven non-scored.

5. **Inter-run washout/readiness enforcement**
   - Q0 user plane;
   - LTE route;
   - fresh namespace/state;
   - no broker/session residue;
   - calibrated radio envelope;
   - runtime/config lock;
   - healthy clock/evidence capture.

The P7B design must close these with the fewest diagnostic cells and one reservation if scientifically defensible. Do not create separate reservations by default.

## Evidence-survival invariant

Before protected physical work, explicitly verify:

- exact reservation identity and expiry;
- exact profile/hardware/image/bindings;
- manifest-derived management endpoints;
- controller/node reachability;
- runtime/version locks;
- writable `/proj/WellPulse` persistent path.

During protected science/qualification, do not introduce background evidence copying that could perturb the measurement unless already proven non-perturbing.

After the measurement/qualification window:

1. freeze required raw evidence;
2. hash and copy to `/proj/WellPulse`;
3. controller-pull the exact persistent bundle;
4. create deterministic TAR + SHA-256;
5. upload to GitHub Actions artifact using the qualified path;
6. independently download/read-back;
7. verify outer and internal SHA-256;
8. only then may `TEARDOWN_AUTHORIZED=YES` be emitted;
9. confirm teardown.

If a failure occurs after protected physical work but before verified evidence closure, preserve the experiment/evidence state and do not automatically terminate.

## Failure discipline

- Diagnose the **first actionable failure** only.
- Preserve every failed attempt as infrastructure/provenance evidence.
- Do not regenerate, patch, fabricate, or outcome-select missing scientific measurements after the fact.
- Do not use qualification outcome direction to tune thresholds, H, RF levels, implementation choices, or rerun decisions.
- Same-reservation recovery is allowed only when it preserves scientific identity and the failure is clearly pre-science/infrastructure or evidence-pipeline-only; document the classification explicitly.
- Never open a second reservation automatically after failure.

## Prohibited during P7B

P7B is non-scored qualification only. It does **not** authorize:

- B1/W1/B2 scored runs;
- WP3 confirmatory campaign;
- OTA replication;
- new H calibration;
- RF recalibration;
- reopening H1;
- reopening K1-K8 without material interface change;
- changing `H_app=300 s`;
- changing frozen RF levels/bindings merely to chase availability;
- `scored_runs_authorized=true` before all mandatory gates pass and the immutable pre-score snapshot is frozen.

## Acceptance and stop condition

At the end of P7B, issue exactly one of:

`WP2_P7B=PASS`

or

`WP2_P7B=BLOCKED:<reason>`

If PASS:

- verify evidence survival and teardown;
- update canonical evidence/status/handover;
- **STOP**;
- do **not** execute scored work;
- next step is a separate offline immutable pre-score snapshot + explicit scored-authorization decision.

If BLOCKED:

- preserve all valid negative/infrastructure evidence;
- update canonical handover with the exact blocker and first actionable failure;
- **STOP**;
- do not automatically rebook, rerun, or relax protocol.

## User-facing progress discipline

Work in finite patches with explicit acceptance gates. Suggested internal P7B patching:

- P7B-A — offline design/contract freeze
- P7B-B — premutation compatibility/readiness QA
- P7B-C — one bounded non-scored physical qualification reservation
- P7B-D — evidence survival + teardown verification
- P7B-E — canonical closure + STOP

Progress is earned only after a patch PASS; planned work is not progress.

## Starting instruction for the next agent

Before any execution, report the retrieved canonical state in one concise paragraph and list the exact P7B subpatches you will own. Do not contact POWDER until the user explicitly authorizes continuation into the live P7B patch.

**HANDOVER READY — DO NOT START P7B WITHOUT EXPLICIT USER CONTINUATION.**
