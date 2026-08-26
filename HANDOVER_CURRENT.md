# WellPulse — Current Handover

Last updated: 2026-08-26 after POWDER H1, recovery characterization, and RS-0 raw-evidence recovery investigation.

## Executive state

- Canonical repository: `aayoubMSA/WellPulse`, branch `main`.
- FIT IoT-LAB scientific layer: **FINAL PASS**.
- POWDER G0–G5 infrastructure/RF qualification: **PASS**.
- RF calibration: **PASS / FROZEN**.
- WP2: **ACTIVE — POST-H1 / PRE-AMENDMENT / PRE-SCORE**.
- `H = UNFROZEN`.
- `scored_runs_authorized = false`.
- Scientific weighted completion remains **20%**; infrastructure/recovery activity does not earn scientific completion.

## Mandatory current read order

1. `HANDOVER_CURRENT.md`
2. `docs/AGENT_HANDOVER_POWDER_NEXT.md`
3. `docs/NEXT_GATE.md`
4. `docs/CONSORTIUM_WP2_RECOVERY_SEMANTICS_GATE_2026-08-26.md`
5. `evidence/powder/wp2-h1-valid-recovery-failure-2026-08-26.md`
6. `docs/RS1_OFFLINE_RECONSTRUCTION.md`
7. `experiments/WP-PWD01/protocol.md`
8. `experiments/WP-PWD01/evidence-schema.md`

## H1 experiment of record

Experiment `WP-HCAL-E`, UUID `9153e16a-1eb1-45f5-88bf-303636a9d1ec`, mapping `enb1 -> nuc1`, `rue1 -> nuc2`. Exact H code commit `95ba9a57bef159450b00b8a439d393d22e1c0519`.

Run `wp2h1-a1-20260826-001` remains classified **VALID_W1_RECOVERY_FAILURE**, non-scored. H remains unfrozen and no scored run is authorized.

Key preserved observations: Q3 duration `120.000117905 s`; generated `361`; pre-restoration cohort `211`; final pending `270`; inflight `20`; published `111`; PUBACK `91`; Q0 pre-readiness `5/5`; post-restoration health `0/3`; queue pending zero not reached; sender status `STOP_AND_INVESTIGATE_H_WOULD_EXCEED_300S`.

Recovery characterization remains: UE-only recovery FAIL; core/RAN reset with live UE user-plane recovery FAIL; coordinated clean-order recovery PASS; post-recovery exact LTE/TLS/MQTT QoS1 application path PASS 3/3.

## CRITICAL EVIDENCE INCIDENT — 2026-08-26

The H1 raw evidence archives and recovery/reproducibility bundles were created and hashed successfully during the live experiment, but were stored under node-local:

`/users/aayoub/wellpulse-powder-evidence/`

They were **not escrowed to persistent `/proj/WellPulse` storage or copied off POWDER before `WP-HCAL-E` was destroyed**.

Known integrity anchors include:

- H1 nuc1 archive SHA-256 `3e3d4c44847bfb7e6304de89d8c1cc05ff9722b6a54d93dd08ce0acfa7418210`
- H1 nuc2 archive SHA-256 `c5d3b212af015061c092c79025258a7f3378e3351051eef48318f12964af2593`
- recovery nuc1 `71aaea25a50ad955fa797a358b14cce4efc0e76ec0861468b3b99dd224c7dd55`
- recovery nuc2 `431855c8662fa46a82f7baca60b5f3deeda4fd849cf4d90bfc4889800be3e71d`
- reproducibility nuc1 `af601716237082be410be3680f1e33b36240beae77e7b644f0f5bef811c1b647`
- reproducibility nuc2 `ada35310a2dd46dba6c28a26604d41f28884799e0fc27c0846a7bf66421935bc`

RS-0 recovery probe on a fresh WellPulse node verified:

- `/proj/WellPulse` is mounted and persistent;
- no H1 raw CSV/JSON/SQLite or named H1 archives were found there;
- no matching evidence was found in `/share`;
- no matching evidence was found in the new node's user home;
- persistent `/proj/WellPulse/logs` contains only small `WP-HCAL-E` startup runlogs (`geni_startup.enb1 returned 0`, `geni_startup.rue1 returned 0`), not scientific raw data.

Current evidence status is therefore:

**RAW H1 NODE-LOCAL EVIDENCE = NOT RECOVERABLE FROM USER-ACCESSIBLE PERSISTENT STORAGE / BACKEND RECOVERY PENDING.**

Do not state that the raw bundles are currently available for RS-1. Hashes and derived observations are preserved, but hashes are not substitutes for raw record-level evidence.

A recovery request was submitted on 2026-08-26 to the POWDER users/support group with POWDER login `aayoub`, project `WellPulse`, experiment UUID, node names, original paths, and known SHA-256 values. Await support response before declaring backend recovery impossible.

## MANDATORY NO-REPEAT CONTROL — FAIL-CLOSED EVIDENCE ESCROW

Effective immediately for **every future POWDER experiment, rehearsal, calibration, scored run, recovery test, and other scientifically material remote-testbed run**:

**Experiment termination/destruction is PROHIBITED until the Evidence Escrow Gate passes.**

Required order:

1. Freeze all raw artifacts and runtime/configuration manifests on the live nodes.
2. Compute SHA-256 manifests on the source nodes.
3. Copy the complete evidence bundle to persistent `/proj/WellPulse/evidence-escrow/<experiment>/<run-id>/`.
4. Verify the persistent copy against the source SHA-256 manifest.
5. Copy a second complete bundle **off POWDER** to the approved external evidence repository/workspace.
6. Verify the off-testbed copy against the same SHA-256 manifest.
7. Confirm mandatory raw tables/logs/databases needed for endpoint reconstruction are present and non-empty.
8. Record experiment UUID/profile revision/node bindings/code commit/runtime versions plus all evidence locations and hashes in the canonical repository/handover.
9. Only after steps 1–8 PASS may teardown/termination/destruction be authorized.

Gate output must be explicit:

`EVIDENCE_ESCROW_GATE=PASS`

Anything else is a hard **STOP / DO_NOT_TERMINATE** condition. Time pressure, reservation expiry, successful derived summaries, or existence of hashes alone does not waive this gate.

Future automation must implement this gate fail-closed and visibly show progress in the shell. A teardown script must refuse to proceed unless both persistent and off-testbed verification have passed.

## Scientific consequence / RS-1

The H1 adverse observation and its derived numerical evidence remain valid and must not be erased or reclassified. However, full RS-1 record-level reconstruction is blocked unless POWDER backend recovery returns the raw bundles. Any paper/report must distinguish preserved derived evidence from unavailable raw record-level evidence.

Do not rerun H merely to hide or replace this incident. A future non-scored run may be justified prospectively only by the consortium protocol/amendment and must preserve this H1 incident as provenance.

## Exact next action

1. Await POWDER support response on backend recovery.
2. Preserve the RS-0 negative recovery finding and support-request provenance.
3. Continue only offline work that does not falsely assume raw H1 availability.
4. Update RS-1 feasibility immediately if support recovers the bundles.
5. No scored run, WP3, RF recalibration, or replacement H run is authorized.

## Handover acceptance test

A replacement agent is ready only if it can state:

- H1 is valid adverse evidence, not an application-layer failure proof;
- H is unfrozen and `scored_runs_authorized=false`;
- raw H1 bundles are presently unavailable from user-accessible storage and backend recovery is pending;
- hashes/derived summaries do not substitute for raw record-level data;
- the Evidence Escrow Gate is mandatory and fail-closed before every future teardown;
- no future POWDER experiment may terminate before verified `/proj/WellPulse` escrow **and** verified off-testbed backup.