# WP2-P7B-R3B — Executable Contract Unification + QA Closure

**Date:** 2026-08-28  
**Verdict:** `WP2_P7B_R3B=PASS_EXECUTABLE_CONTRACT_UNIFICATION_QA`  
**Evidence class:** OFFLINE / NON-SCORED / CONTRACT-REPAIR QA  
**POWDER contact by R3B:** NO  
**Reservation by R3B:** NO  
**Scored authorization:** BLOCKED

## Purpose

R3B repairs the contract drift identified by `WP2-P7B-R3A`. It does not reinterpret the first blocked P7B attempt, does not create physical-qualification credit, and does not authorize a new live run.

Historical v1/R1/R2 artifacts remain immutable provenance. Future requalification may use only the new executable-contract surface after a fresh explicit live authorization.

## Unified executable contract

Canonical machine-readable authority:

`experiments/WP-PWD01/p7b-executable-contract-v2.json`

The v2 contract unifies:

- profile revision, hardware/image/bindings;
- RF levels and attenuator IDs;
- Q0/Q3/restart/H_app schedule;
- B1/W1 transport locks;
- B2 Java/JAR durability locks;
- cell order and restart domain;
- evidence ownership and exact runtime file paths;
- absolute root templates for UE/core/escrow;
- evidence completeness rules;
- evidence survival chain;
- teardown prerequisites;
- authority and retry prohibitions;
- the only prospective authoritative node entrypoint.

The contract remains `live_authorized=false` and requires fresh explicit live authorization after R3B.

## Contract loader

`src/wellpulse/p7b_contract_v2.py`

The loader validates the schema and fails closed on:

- scored/live authority drift;
- reservation/retry/second-replacement drift;
- RF or timing drift;
- cell-order mismatch;
- unresolved shell-token evidence roots;
- unexpected future entrypoint;
- teardown gate drift.

It also renders a legacy qualification view from v2 so existing scientific gate functions can be reused without treating the old v1 JSON as the runtime authority.

## Future authoritative node entrypoint

`scripts/wp2_p7b_c_node_r2.py`

This wrapper loads v2 and injects the contract values into the historical base implementation before execution. The following runtime authorities are contract-derived:

- broker host/port;
- attenuator IDs;
- Q0/Q3;
- pre-Q0 duration;
- Q3 duration;
- restart offset;
- H_app;
- B2 JAR SHA-256;
- readiness contract view.

It also replaces unresolved status evidence roots with resolved absolute paths and redirects reconstruction to the v2 contract-driven reconstruction path.

Historical `scripts/wp2_p7b_c_node.py` and `scripts/wp2_p7b_c_node_r1.py` are prohibited as future authority-bearing entrypoints.

## Evidence contract gate

`scripts/wp2_p7b_evidence_gate_v2.py`

This gate derives required paths directly from v2. It checks:

- all reservation-level evidence;
- every per-cell UE/core evidence path;
- B1/W1/B2 architecture-specific evidence;
- receiver writer/watcher path equality;
- resolved absolute receiver paths;
- complete cell status and cell order;
- reconstruction PASS;
- no unresolved `$HOME`/`~` status path.

Therefore a reconstruction cannot be treated as complete merely because scientific gate files pass while raw evidence is missing.

## Contract-driven reconstruction

`scripts/reconstruct_wp2_p7b_v2.py`

The v2 reconstruction:

1. derives the legacy scientific gate view from v2;
2. runs the existing qualification reconstruction logic;
3. runs the v2 evidence-contract gate;
4. returns overall PASS only when both scientific reconstruction and evidence completeness PASS.

## QA

Adversarial QA:

`tests/test_wp2_p7b_r3b_executable_contract.py`

The first QA run correctly failed because an older test still required the now-retired R3 live workflow. That stale test was repaired to require the live workflow/trigger to remain absent.

Accepted Local Unit Tests:

- run `33120430635`;
- job `98685661308`;
- tested SHA `c9e96a21399b0a7011af235e0e51b3a8064714a1`;
- Python `3.12.14`;
- `paho-mqtt==2.1.0`;
- **91/91 tests PASS**;
- final enforcement PASS.

R3B-specific adversarial QA proves:

1. v2 is offline/non-scored and requires fresh live authorization;
2. all frozen v1 scientific controls are preserved;
3. evidence roots resolve to absolute paths and contain no shell tokens;
4. only `scripts/wp2_p7b_c_node_r2.py` is prospective authority;
5. a synthetic complete evidence tree passes;
6. deleting one required evidence file fails closed;
7. an unresolved `$HOME` status path fails closed;
8. teardown requires all three gates: `EVIDENCE_CONTRACT_GATE`, `EVIDENCE_ESCROW_GATE`, and `CONTROLLER_OFFPOWDER_GATE`;
9. no R3 live workflow or trigger remains on `main`.

## Important concurrent-run provenance

A previously armed R3 GitHub Actions run, `33119810043` / job `98683578418`, had already entered its live execution step before the R3A HOLD was applied. R3B did not start that run and did not contact POWDER. At R3B closure time the older run was still reported `in_progress` by GitHub.

The R3 live workflow and trigger have been removed from `main`, preventing a new run from being launched through that surface. The older in-flight run remains separate provenance and must not be interpreted as using executable contract v2; it checked out its earlier SHA before R3B.

## Verdict

`WP2_P7B_R3B=PASS_EXECUTABLE_CONTRACT_UNIFICATION_QA`

`EXECUTABLE_CONTRACT_V2=PASS_OFFLINE`

`LIVE_REQUALIFICATION_AUTHORIZED=false`

`SCORED_AUTHORIZATION=BLOCKED`

No physical-qualification, WP2 management, or scientific completion credit is added by R3B.

## Next gate

Before any future physical requalification:

1. resolve/close the already in-flight historical R3 run and preserve its provenance;
2. perform an offline future-controller freeze against executable contract v2;
3. require a fresh explicit user live authorization because the authority-bearing execution surface materially changed;
4. only then may one bounded non-scored physical requalification be considered.
