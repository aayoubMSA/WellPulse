# WP2-P7B-H2.1 — Executable Controller/Restore Contract Delta Closure — 2026-08-28

## Terminal verdict

`H2_1_CONTRACT_DELTA=PASS`

This is an **offline-only** closure. It grants no live POWDER, reservation, RF, retry, W1/B2, teardown, scored, or WP3 authority.

## Scope completed

H2.1 translated the H1 controller/session restoration draft controls A1–A7 into one machine-readable prospective contract delta:

- `experiments/WP-PWD01/p7b-h2-controller-restore-contract-delta-v1.json`

The historical/frozen base contract was **not edited**:

- `experiments/WP-PWD01/p7b-executable-contract-v2.json`
- pinned Git blob SHA: `233aabeaf3081470bc3ebc1ee04168f8932fc415`

This separation preserves the exact contract provenance of the aborted B1 attempt while making the prospective operational amendment executable and testable.

## A1–A7 executable delta

The delta now machine-encodes:

- **A1** — controller/service-session disjointness pre-RF gate;
- **A2** — ownership proof before any destructive tmux/session cleanup, with PID-scoped service termination preferred;
- **A3** — controller execution outside the restoration failure domain;
- **A4** — incremental `restart_transition.json` written immediately after replacement gateway start/ready proof;
- **A5** — ordered restoration-frontier markers from restore request through service-ready probe completion, with no artificial scientific delay;
- **A6** — supplementary parent-controller traps/flush behavior without making correctness depend on trap execution;
- **A7** — mandatory static/adversarial QA cases before any future live authority.

## Frozen-science equivalence

The H2.1 QA proves the delta preserves the v2 scientific controls:

- Q0/Q1/Q2/Q3 = `0/40/52/55 dB`;
- attenuators `[1,33,2,34]`;
- pre-Q0 = `60 s`;
- Q3 = `120 s`;
- gateway restart offset = `60 s`;
- `H_app=300 s` anchored at `t_service_ready`;
- primary cohort cutoff = `t_rf_restore`;
- exact sequence `B1 -> W1 -> B2`;
- telemetry generator outside restart domain;
- no automatic scientific retry;
- negative/null/unfavourable evidence retained.

The delta explicitly prohibits RF, timing, attenuator, cell-order, H, endpoint, automatic-retry, scored-authority and live-authority changes.

## Authority state

All prospective authority flags remain false:

`LIVE_AUTHORIZATION=NO`

`NEW_RESERVATION_AUTHORIZATION=NO`

`RF_AUTHORIZATION=NO`

`RETRY_AUTHORIZATION=NO`

`W1_B2_AUTHORIZATION=NO`

`TEARDOWN_AUTHORIZATION=NO`

`SCORED_AUTHORIZATION=NO`

`WP3_AUTHORIZATION=NO`

A future live action still requires H2.2–H2.5 PASS, H2 terminal PASS, and a separate explicit user authorization.

## QA evidence

Implementation commits:

- contract delta: `46ec4dd758847fe2a16325739107b68ca05c811e`
- machine-readable tests: `5d6fa9d74bf5f4b1059434fc46344d264694c52e`

GitHub Actions offline QA:

- workflow: `Local Unit Tests`
- run: `33139803749`
- job: `98747874891`
- head SHA: `5d6fa9d74bf5f4b1059434fc46344d264694c52e`
- Python: `3.12.14`
- Paho MQTT: `2.1.0`
- result: `PASS`
- total unit tests: `135`
- failures/errors: `0`

The H2.1-specific tests prove:

1. the base contract blob is exactly pinned;
2. all authority remains false;
3. exact A1–A7 controls exist;
4. frozen scientific controls equal v2;
5. A1 fails closed before RF;
6. A2 prohibits unsafe generic tmux destruction;
7. A3 separates controller from restore failure domain;
8. A4 incremental restart proof is required without replacing final proof;
9. A5 restoration frontier ordering is exact and adds no diagnostic delay;
10. A6 traps are supplementary only;
11. A7 includes all required adversarial cases and prohibits live POWDER QA;
12. prohibited scientific/authority deltas are explicit;
13. the next patch is H2.2, not live execution.

## Next bounded patch

`WP2-P7B-H2.2 — CONTROLLER/SESSION OWNERSHIP REPAIR`

H2.2 may implement A1–A3 offline and test the ownership/session boundaries. It must not contact POWDER or alter the frozen scientific controls.

## Stop state

`H2_1_CONTRACT_DELTA=PASS`

`H2_PROGRESS=20%`

`NEXT_PATCH=WP2-P7B-H2.2_CONTROLLER_SESSION_OWNERSHIP_REPAIR`

`LIVE_POWDER_AUTHORIZATION=NO`

**STOP — H2.1 CLOSED.**
