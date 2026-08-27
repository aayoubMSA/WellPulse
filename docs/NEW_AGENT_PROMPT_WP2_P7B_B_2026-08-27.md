# WellPulse — New Agent Mandate — WP2-P7B-B

Date: 2026-08-27

## Role and canonical state

Own the WellPulse WP2 execution lane in `aayoubMSA/WellPulse`, branch `main`. Reconstruct state only from the canonical repository.

Resume exactly at:

`WP2-P7B-B — OFFLINE IMPLEMENTATION + PREMUTATION COMPATIBILITY/READINESS QA`

Current state:

- `WP2_P6=PASS_RECOVERED_SINGLE_RUN`;
- `WP2_P7_HARDENING_QA=PASS`;
- `WP2_P7B_A=PASS_OFFLINE_CONTRACT_FREEZE`;
- `WP2_P7B_PROGRESS=20/100`;
- `SCORED_AUTHORIZATION=BLOCKED:PRE_SCORE_PHYSICAL_QUALIFICATION_REQUIRED`;
- `scored_runs_authorized=false`;
- WP2 management/readiness = 95/100;
- scientific weighted completion = 20%;
- WP3 blocked.

P7B-B is offline only and is NOT STARTED. Do not contact POWDER, reserve, SSH, mutate the testbed or begin P7B-C without separate explicit authorization.

## Mandatory read order

1. `HANDOVER_CURRENT.md`
2. `docs/NEW_AGENT_PROMPT_WP2_P7B_B_2026-08-27.md`
3. `docs/WP2_P7B_A_OFFLINE_CONTRACT_FREEZE_2026-08-27.md`
4. `experiments/WP-PWD01/P7B_PHYSICAL_QUALIFICATION_PLAN_v1.md`
5. `experiments/WP-PWD01/p7b-qualification-contract.json`
6. `docs/WP2_P7_SCORED_AUTHORIZATION_2026-08-27.md`
7. `docs/NEXT_GATE.md`
8. `docs/MILESTONE_STATUS.md`
9. `docs/WP2_P6_GOLDEN_CLOSURE_2026-08-27.md`
10. `evidence/powder/wp2-p6-live-status.md`
11. `experiments/WP-PWD01/PRE_SCORE_P0_AMENDMENT_2026-08-26.md`
12. `experiments/WP-PWD01/PRE_SCORE_P1_AMENDMENT_2026-08-26.md`
13. `experiments/WP-PWD01/run-matrix.yaml`
14. `experiments/WP-PWD01/RECOVERY_SEMANTICS_AMENDMENT_v1.md`
15. `experiments/WP-PWD01/protocol.md`
16. `experiments/WP-PWD01/B2_SEMANTICS_GATE_v1.md`
17. `evidence/local/wp2-b2-semantics-latest.md`
18. `src/wellpulse/transport.py`
19. `src/wellpulse/powder_w1.py`
20. `src/wellpulse/store.py`
21. `scripts/wp2_golden_orchestrator.sh`
22. `scripts/wp2_golden_evidence_escrow.sh`
23. `scripts/wp2_controller_pull_persistent_escrow.sh`
24. `scripts/wp2_controller_verify_artifact_roundtrip.sh`
25. `docs/WORKFLOW_REGISTRY.md`
26. `AGENTS.md`

## Exact P7B-B ownership

Implement only the frozen P7B-A contract:

- separated generator and gateway restart domains;
- B1 volatile non-durable handoff and accepted/unacknowledged event reconstruction;
- W1 durable SQLite replay process;
- exact B1/W1 manifest comparator;
- remote-capable B2 Java 1.2.5 TLS adapter with pinned JAR/config;
- complete washout/readiness gate;
- deterministic qualification reconstruction and evidence inventory;
- offline PASS/failure/interlock QA.

Do not change Q0-Q3, the four attenuator mapping, workload rate, S3 restart timing, clock semantics, H_app=300 s, endpoints, scored matrix, or evidence-survival doctrine.

## Stop condition

P7B-B PASS requires all offline implementation, syntax, compatibility, washout, reconstruction, evidence and fail-closed tests to pass. Then update canonical state and STOP before P7B-C.

P7B-B failure must be preserved with the first actionable failure. Do not weaken the contract.

**HANDOVER READY — P7B-B OFFLINE ONLY; P7B-C REQUIRES SEPARATE EXPLICIT LIVE AUTHORIZATION.**
