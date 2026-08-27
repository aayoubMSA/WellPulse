# WellPulse — Next Gate

Status date: 2026-08-27 after **P7B-R2 one-replacement requalification contract freeze PASS**.

## Current frontier

- `WP2_P6=PASS_RECOVERED_SINGLE_RUN`
- `WP2_P7_HARDENING_QA=PASS`
- `WP2_P7B_A=PASS_OFFLINE_CONTRACT_FREEZE`
- `WP2_P7B_B=PASS_OFFLINE_IMPLEMENTATION_PREMUTATION_QA`
- `WP2_P7B_C=BLOCKED:RECEIVER_CONNECT_TIMEOUT`
- `WP2_P7B_D=BLOCKED_STRICT_COMPLETENESS_RECEIVER_EVENT_LEDGER_NOT_RECOVERED`
- `WP2_P7B_E=PASS_CANONICAL_BLOCKED_CLOSURE`
- `WP2_P7B_R1=PASS_OFFLINE_RECEIVER_PATH_OBSERVABILITY_QA`
- `WP2_P7B_R2=PASS_ONE_REPLACEMENT_CONTRACT_FREEZE`
- `REQUALIFICATION_DECISION=GO_ONE_REPLACEMENT_NON_SCORED`
- `P7B_RQ1_AUTHORITY_CONTRACT=FROZEN`
- `P7B_RQ1_LIVE_AUTHORIZED=false`
- successful P7B physical-qualification credit: **40/100** from A+B only
- `SCORED_AUTHORIZATION=BLOCKED:PRE_SCORE_PHYSICAL_QUALIFICATION_REQUIRED`
- `scored_runs_authorized=false`
- `WP3=BLOCKED`
- WP2 management/readiness: **95/100**
- scientific weighted completion: **20%**

Canonical R2 closure:

`docs/WP2_P7B_R2_REQUALIFICATION_CONTRACT_FREEZE_2026-08-27.md`

Machine-readable R2 contract:

`experiments/WP-PWD01/p7b-requalification-r2-contract.json`

Retained first-attempt provenance remains unchanged in:

- `docs/WP2_P7B_E_CANONICAL_BLOCKED_CLOSURE_2026-08-27.md`
- `evidence/powder/wp2-p7b-c-live-status.md`
- `evidence/powder/wp2-p7b-d-live-status.md`

## What R2 froze

The original P7B contract remains unchanged and its one allowed reservation remains consumed. R2 prospectively permits **at most one replacement authority ID `P7B-RQ1`**, but does not authorize it live.

Frozen replacement rules:

1. maximum new reservations = **1**;
2. automatic retry = **NO**;
3. automatic new reservation = **NO**;
4. second replacement = **NO**;
5. separate explicit live authorization = **REQUIRED**;
6. only node entrypoint = `scripts/wp2_p7b_c_node_r1.py`;
7. historical `scripts/wp2_p7b_c_node.py` is prohibited for the replacement;
8. receiver/preservation paths must be resolved absolute paths;
9. cell order remains `P7B-B1-S3 -> P7B-W1-S3 -> P7B-B2-S3`;
10. Q0/Q3/timing/H_app/scientific semantics remain unchanged;
11. bounded root-cause diagnostics must precede a generic final failure presentation;
12. raw evidence must be persisted, pulled, independently read back and hash-verified before teardown;
13. if evidence survival fails, leave the experiment live and STOP.

R2 also added `scripts/wp2_p7b_r2_validate_controller.py`. The retired historical controller fails this static gate. A synthetic compliant future controller passes it.

Accepted R2 Local Unit Tests:

- run `33117108893`;
- job `98674462071`;
- SHA `b77609bfb9256a0eb189c0e5dd29a2f1f68c3bc2`;
- Python `3.12.14`;
- `paho-mqtt==2.1.0`;
- **73/73 PASS**.

R2 contacted no POWDER system and created no workflow, trigger, reservation, SSH session, scientific run or scored run.

## Exact next bounded patch — LIVE, NOT AUTHORIZED

`WP2-P7B-R3 — ONE REPLACEMENT NON-SCORED PHYSICAL REQUALIFICATION + EVIDENCE SURVIVAL`

Status:

`P7B_RQ1_LIVE_AUTHORIZED=false`

R3 requires **separate explicit live authorization**. R2 GO does not itself authorize POWDER contact.

If separately authorized, R3 may:

1. create exactly one replacement reservation under authority ID `P7B-RQ1`;
2. execute only `P7B-B1-S3 -> P7B-W1-S3 -> P7B-B2-S3`;
3. fail closed before each cell on the frozen Q0/readiness contract;
4. stop later cells after any cell failure;
5. use only `scripts/wp2_p7b_c_node_r1.py` for node execution;
6. emit bounded raw diagnostics on first failure;
7. preserve complete raw evidence to `/proj`, pull it off POWDER, upload/read back the artifact and verify hashes;
8. authorize teardown only after `EVIDENCE_ESCROW_GATE=PASS` and `CONTROLLER_OFFPOWDER_GATE=PASS`;
9. leave the experiment live if the evidence gate does not pass;
10. create no retry or second replacement.

After terminal R3 evidence, STOP for an offline closure/snapshot decision. R3 itself never sets `scored_runs_authorized=true`.

## P7B ledger

| Patch | Role | Status | Result |
|---|---|---|---|
| P7B-A | design/contract freeze | **PASS** | original contract + offline QA |
| P7B-B | implementation/premutation QA | **PASS** | implementation/reconstruction + B2 semantics QA |
| P7B-C | first physical qualification | **BLOCKED** | pre-measurement receiver path orchestration defect |
| P7B-D | first evidence survival + teardown | **BLOCKED STRICT COMPLETENESS** | declared roots verified; receiver event ledger unrecovered; teardown complete |
| P7B-E | canonical blocked closure | **PASS CLOSURE** | blocked result frozen without relabelling |
| P7B-R1 | repair/observability QA | **PASS OFFLINE** | path repair + fail-fast + diagnostics + 65/65 |
| P7B-R2 | replacement authority contract | **PASS OFFLINE** | one replacement frozen + static controller gate + 73/73 |

R1/R2 create no physical-qualification credit. Successful qualification credit remains **40/100**.

## Authority boundary

Until the user separately authorizes R3:

- no POWDER contact, reservation or SSH;
- no `P7B-RQ1` reservation;
- no physical B1/W1/B2 requalification;
- no Golden/H/RF recalibration;
- no scored B1/W1/B2;
- no OTA replication or WP3;
- no `scored_runs_authorized=true`;
- no immutable pre-score snapshot claiming physical readiness.

**STOP — R2 PASS; P7B-R3 LIVE NOT AUTHORIZED.**
