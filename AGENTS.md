# AGENTS.md — Dominant Integration Rule

This rule is **dominant for all agents working in this repository**. It overrides convenience, speed, and implementation-first behavior unless a higher-authority explicit user instruction says otherwise.

## Mandatory Pre-Integration Compatibility Gate

Before connecting, automating, or coupling any two platforms, modules, services, devices, repositories, workflows, testbeds, APIs, or execution environments, **do not implement the live integration first**.

First study and freeze a compatibility contract for both sides. At minimum verify:

1. Interface/API/CLI contracts and exact command semantics.
2. Which operations are read-only versus mutating; unknown semantics are **MUTATING/UNSAFE**.
3. Hardware types, topology, bindings, firmware where relevant, and resource constraints.
4. OS, runtime, libraries, drivers, tools, actions, images, profiles, and exact versions/revisions.
5. Authentication, authorization, secret transport, key/certificate requirements, and redaction boundaries.
6. Network addresses, routes, ports, protocols, TLS behavior, time synchronization, and DNS assumptions.
7. Data formats, schemas, units, timestamps, identifiers, ordering, and state/session semantics.
8. Lifecycle: creation, startup, readiness, reservation/lease expiry, keepalive, teardown, timeout, and destruction behavior.
9. Storage/persistence semantics, evidence locations, retention, and what is lost on termination.
10. Concurrency, retries, idempotency, locking, race conditions, and re-entrancy.
11. Observability: what can be safely queried during execution without changing state; logging must not leak secrets/session material.
12. Failure modes, partial failures, recovery primitives, rollback, cleanup, and safe-stop behavior.
13. Quotas, rate limits, scheduling/resource availability, and platform-side constraints.
14. Version drift/deprecation risk and compatibility matrix.
15. Ownership boundaries: which platform is authoritative for state, timing, identity, evidence, and teardown.
16. Acceptance tests for each interface boundary before an end-to-end live run.

### Gate outcome

Live cross-platform work may proceed only when:

`PRE_INTEGRATION_COMPATIBILITY_GATE=PASS`

If any material interface behavior, side effect, version, persistence rule, or lifecycle condition is unknown:

`PRE_INTEGRATION_COMPATIBILITY_GATE=BLOCKED`

Do not discover material contract behavior during a scientifically material or time-limited live run when it can be established beforehand.

## Mandatory Experimental Observability and Raw-Evidence Rule

For any scientifically material or time-limited experiment, the human-facing HCI and the scientific raw-data plane must be separated.

### HCI / display plane

- The PI must be able to follow experiment progress through a simple live HCI.
- During the protected scientific window, the HCI may consume only status/events already emitted by the orchestrator or experiment processes.
- The HCI must not issue independent SSH/API/CLI/testbed commands, polling probes, attenuation queries, restarts, reconfiguration, or teardown actions.
- Unknown observability semantics are treated as mutating/unsafe.
- HCI failure must not alter or invalidate the scientific run.
- HCI logs must not contain credentials, private key material, tokens, certificate private material, or TLS session secrets.

Required design state:

`HCI_CONTROL_ACTIONS_ENABLED=false`

### Scientific raw-data plane

- Raw scientific data remains authoritative and must be saved independently of the HCI.
- Derived dashboards, counters, summaries, screenshots, or plots never substitute for raw record-level evidence.
- Raw artifacts must be inventoried, frozen, SHA-256 hashed, copied to qualified persistent storage, copied off-platform, and read-back verified before teardown.
- Any proposed in-run checkpoint/background-copy mechanism must first be shown not to materially perturb experiment timing or load.

Required completion states before teardown:

`RAW_EVIDENCE_COMPLETE=PASS`

`EVIDENCE_ESCROW_GATE=PASS`

`TEARDOWN_AUTHORIZED=YES`

Canonical WellPulse design: `docs/LIVE_EXPERIMENT_HCI_AND_RAW_EVIDENCE.md`.

## Design principle

Prefer:

`study contracts -> fingerprint both sides -> compatibility matrix -> offline/mock/dry-run -> bounded interface test -> live E2E`

not:

`connect first -> debug mismatches during live execution`.

For experiments, also prefer:

`experiment emits status -> passive HCI displays status`

not:

`HCI probes experiment to discover status`.

The objective is minimum total effort, fewer invalid runs, lower evidence risk, reproducible integration by design, clear human oversight, and complete raw scientific provenance.

Canonical detailed checklist: `docs/PRE_INTEGRATION_COMPATIBILITY_GATE.md`.
