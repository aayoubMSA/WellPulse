# Pre-Integration Compatibility Gate

**Status:** mandatory / fail-closed  
**Scope:** every integration between two or more platforms, modules, services, devices, repositories, workflows, remote testbeds, APIs, or execution environments.  
**Authority:** root `AGENTS.md` and current handover.

## Purpose

Prevent time/resource loss caused by discovering interface assumptions, version mismatches, side effects, lifecycle constraints, observability hazards, or evidence-loss risks during a live integration.

The gate must be completed **before** implementation of a materially new cross-platform live path, and refreshed when either side changes materially.

## Required compatibility record

For each side of the integration, record the exact current values and source/evidence for the following.

### C1 — Contract and command semantics

- official API/CLI/interface contract;
- exact endpoints/commands/actions used;
- inputs, outputs, status/error codes;
- read-only vs mutating semantics;
- hidden/implicit side effects;
- idempotency/retry behavior;
- deprecated/unsupported calls.

**Rule:** if side effects are not proven read-only, classify the operation as mutating/unsafe.

### C2 — Hardware and topology

- device/resource types;
- CPU/architecture where relevant;
- firmware/FPGA/radio revisions where relevant;
- physical/logical bindings;
- network topology;
- resource exclusivity/sharing constraints.

### C3 — Software/runtime fingerprint

Freeze exact versions/revisions for:

- OS/image;
- runtime/interpreter;
- libraries/packages;
- drivers;
- profile/template;
- Git commit;
- GitHub Action/runtime image or equivalent automation runner;
- external client/SDK/CLI;
- protocol implementations.

Use exact versions where possible; avoid `latest` in a reproducibility-critical path.

### C4 — Identity, auth, authorization, and secrets

- account/project/tenant identity;
- permissions required;
- auth mechanism;
- key/certificate/token lifecycle;
- secret injection path;
- redaction rules;
- whether diagnostics can expose credential or session material.

No secret/session material belongs in scientific evidence or repository logs.

### C5 — Network and protocol contract

- addresses/hostnames;
- routes/interfaces;
- ports;
- protocol/version;
- TLS mode and identity verification;
- MTU/firewall/NAT assumptions where relevant;
- time synchronization/timezone rules;
- connectivity readiness criterion.

### C6 — Data and state semantics

- schemas/formats;
- units;
- timestamp clocks and precision;
- IDs/keys;
- ordering and duplication behavior;
- session/state persistence;
- null/error semantics;
- serialization/encoding.

### C7 — Lifecycle and time budget

- reservation/lease validity window;
- instantiation time;
- boot/startup time;
- readiness criteria;
- keepalive/idle timeout;
- hard expiry;
- teardown/destruction semantics;
- extension/rebooking rules;
- estimated minimum remaining time required for a full safe run including evidence escrow.

A live run must not start when the remaining window is insufficient for the full run **plus fail-closed evidence preservation and safe shutdown margin**.

### C8 — Persistence and evidence boundary

- ephemeral paths;
- persistent paths;
- off-platform evidence destination;
- what is destroyed on termination;
- required raw artifacts;
- manifests/hashes;
- retention duration;
- evidence escrow/verification procedure.

Raw record-level evidence must be preserved independently of dashboards, counters, summaries, screenshots, or derived plots.

### C9 — Observability and HCI contract

For every diagnostic/status action, prove whether it is read-only.

- safe status queries;
- unsafe/mutating queries;
- polling frequency;
- logging volume;
- redaction;
- whether observation changes timing/state/load;
- whether an independent probe can contaminate the experiment;
- which process is authoritative for each displayed status/counter.

For scientifically material runs, prefer a **push model**:

`experiment/orchestrator emits bounded status -> passive HCI renders it`

Do not use a pull/probe model during the protected scientific window unless it has been independently qualified as non-perturbing and scientifically acceptable.

The HCI must not have control actions during the protected scientific window.

Required state:

`HCI_CONTROL_ACTIONS_ENABLED=false`

During a scientific window, do not run unqualified status/probe actions.

### C10 — Concurrency and orchestration

- single source of truth for state;
- lock/concurrency policy;
- retry ownership;
- race conditions;
- duplicate trigger behavior;
- cross-system clock/order assumptions;
- re-entry/resume semantics.

### C11 — Failure/recovery/rollback

Enumerate likely failures at each boundary:

- auth failure;
- resource unavailable;
- version mismatch;
- partial startup;
- connectivity loss;
- stale state;
- timeout;
- HCI/rendering failure;
- evidence-copy failure;
- remote expiry;
- runner failure;
- API deprecation/change.

For each material failure define:

- detection signal;
- safe stop;
- rollback/recovery primitive;
- whether recovery invalidates the run;
- evidence preserved before cleanup.

An HCI failure must not stop, alter, or invalidate the scientific acquisition path.

### C12 — Quotas and platform constraints

- rate limits;
- job/runtime limits;
- reservation limits;
- storage limits;
- API quotas;
- concurrent session limits;
- scheduler/resource constraints;
- external service deprecation notices.

### C13 — Ownership and authority matrix

For each information type, assign one authoritative source:

- experiment identity/status;
- code version;
- hardware binding;
- runtime version;
- time/event clocks;
- raw scientific records;
- HCI status/counters;
- evidence location;
- teardown authority;
- scientific classification.

Avoid duplicated competing state registers.

### C14 — Boundary acceptance tests

Before E2E, run the smallest discriminating tests possible:

1. offline/static contract validation;
2. local/mock/dry-run where feasible;
3. auth/connectivity preflight;
4. version/fingerprint validation;
5. safe read-only status verification;
6. bounded interface smoke test;
7. passive-HCI status-stream test with no control path;
8. raw-evidence inventory/freeze/hash test;
9. evidence-path write/read/hash verification;
10. teardown guard dry-run;
11. benchmark any proposed in-run checkpoint/background-copy mechanism for non-interference.

Only then launch the end-to-end live path.

## Required artifact

Create a compact compatibility matrix containing:

| Boundary | Side A | Side B | Exact versions/contracts | Risk | Acceptance evidence | Status |
|---|---|---|---|---|---|---|

Material unknowns must be explicit.

## Gate decision

PASS only when every material item is verified or explicitly bounded and accepted:

`PRE_INTEGRATION_COMPATIBILITY_GATE=PASS`

For experimental integrations, also require:

`LIVE_HCI_AND_RAW_EVIDENCE_GATE=PASS`

Otherwise:

`PRE_INTEGRATION_COMPATIBILITY_GATE=BLOCKED`

No live integration under BLOCKED.

## WellPulse-specific immediate application

Before the next GitHub Actions ↔ POWDER Golden rehearsal, verify at minimum:

- Portal API experiment create/get/manifest/status semantics and lifecycle/expiry behavior;
- POWDER profile revision and NUC hardware bindings;
- `tmcc attenuator` command syntax and side effects from authoritative platform documentation/source, including a proven read-only status path if one exists;
- srsLTE profile startup/cleanup semantics;
- exact OS/Python/Paho/OpenSSL/rclone/GitHub runner/action versions;
- TLS diagnostics that do not persist session secrets;
- GitHub workflow concurrency and trigger ownership;
- full Golden duration plus startup/recovery/G8/G9/Drive escrow margin against reservation expiry;
- `/proj/WellPulse` and off-POWDER evidence persistence before teardown;
- explicit ban on independent unqualified live probes during G3–G10;
- a simple PI-facing HCI fed only by orchestrator/process-emitted status events;
- complete raw-data inventory independent of HCI summaries;
- benchmarked decision on whether in-run `/proj` checkpoints are non-perturbing;
- final raw freeze/hash/persistent-copy/off-platform-copy/read-back verification path.

Canonical HCI/raw-evidence design: `docs/LIVE_EXPERIMENT_HCI_AND_RAW_EVIDENCE.md`.

Only after this matrix and the HCI/raw-evidence design both pass should a new non-scored Golden reservation be requested/instantiated.
