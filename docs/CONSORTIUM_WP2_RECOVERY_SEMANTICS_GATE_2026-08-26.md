# WellPulse — WP2 Recovery-Semantics Amendment Consortium

**Date:** 2026-08-26  
**Stage:** POST-H1 / PRE-AMENDMENT / PRE-SCORE  
**Scientific completion:** 20%  
**Scored runs:** `NOT AUTHORIZED`  
**H:** `UNFROZEN`  
**H1 Trial #1:** `VALID_W1_RECOVERY_FAILURE` — preserved, never replaced or retroactively reclassified.

## 1. Mission

Resolve one question before WellPulse can reopen physical H calibration:

> **How should network-service recovery be represented in the POWDER protocol so that LTE/testbed recovery pathology does not contaminate the intended B1-vs-W1 application-level reliability comparison, while preserving real-RF validity and avoiding outcome-dependent protocol changes?**

The consortium is not authorized to reopen novelty, Q0–Q3 RF calibration, the matched primary comparator, the frozen failure-model rationale, or scored execution. Its mandate is narrowly bounded to recovery semantics, measurement clocks, testbed hygiene, and the exact gate required before H may restart.

## 2. Consortium composition

This is a multidisciplinary expert-review consortium constituted as seven independent professional roles. Each role must issue its own position before synthesis; disagreement is preserved rather than averaged away.

| Role | Primary responsibility | Failure mode it must guard against |
|---|---|---|
| Controlled-RF / wireless experimentation lead | Preserve the meaning of Q3→Q0 and real-RF validity | Turning a radio experiment into an uncontrolled operator procedure |
| LTE/EPC/RAN systems lead | Diagnose attach/context/IP continuity and realistic service restoration | Misattributing EPC/MME/SPGW pathology to WellPulse |
| Distributed-systems reliability lead | Separate substrate recovery from durable application semantics | Confounding transport availability with record durability |
| MQTT / IIoT protocol lead | Protect B1/W1/B2 comparability and session semantics | Hidden broker/client-state contamination |
| Experimental-design & statistics lead | Protect estimands, censoring, H, and stopping rules | Outcome-dependent exclusion or treatment-informed observation windows |
| Reproducibility / artifact lead | Ensure every amendment is executable and reconstructable | Irreproducible operator-only recovery procedures |
| Adversarial reviewer / editor lead | Attack the final paper as a skeptical reviewer | Overclaiming network resilience from a testbed workaround |

## 3. Evidence admitted into this gate

The consortium shall use, at minimum:

- frozen RF state: Q0=0 dB, Q1=40 dB, Q2=52 dB, Q3=55 dB; attenuator IDs `1 33 2 34` move together;
- `experiments/WP-PWD01/H_CALIBRATION_PLAN_v1.md`;
- `experiments/WP-PWD01/protocol.md` and analysis/evidence plans;
- `docs/CONSORTIUM_PRE_WP3_REVIEW_2026-08-26.md`;
- canonical H1 record: `evidence/powder/wp2-h1-valid-recovery-failure-2026-08-26.md`;
- session closeout/evidence hashes from the 2026-08-26 POWDER reservation;
- exact runtime/config fingerprints from `nuc1` and `nuc2`;
- preserved H1 sender/receiver artifacts and LTE logs.

No adverse result may be discarded because it complicates the planned story.

## 4. Facts frozen from the 2026-08-26 physical session

1. H1 was technically valid at entry: correct Q0 readiness, correct `tun_srsue` route, exact Paho/runtime/session gate, correct four-attenuator Q3 schedule, and evidence capture.
2. Q3 full-state duration was approximately 120.0001 s.
3. Q0 was restored, but the user plane did not recover within the frozen 150 s post-restore bound; H therefore could not be frozen.
4. Radio-layer recovery occurred sufficiently for strong uplink decoding, while EPC/MME/SPGW logs showed stale/context-churn symptoms and successive address allocation.
5. UE-only restart failed to recover service.
6. EPC/eNB reset while leaving UE running failed to recover service.
7. Coordinated clean-order recovery `stop UE -> EPC -> eNB -> fresh UE` restored `tun_srsue`, the original `172.16.0.2` source address, and Q0 user-plane reachability.
8. After clean-order recovery, the exact application path `LTE -> TLS -> MQTT 3.1.1 -> QoS1 -> broker round-trip -> SHA-256 integrity` passed in three independent fresh sessions (3/3).
9. The result therefore supports a testbed/LTE service-recovery dependency; it does not establish a scored WellPulse advantage and does not retroactively convert H1 into a success.

## 5. Decision questions

The consortium must answer all of the following before recommending an amendment:

### Q-A — What is the scientific outage endpoint?

Is the intended experimental treatment:

- RF restoration itself (`Q3 -> Q0`), with completely autonomous LTE recovery required; or
- loss and subsequent **restoration of usable network service**, where testbed-specific LTE reinitialization may be a controlled service-restoration operation?

### Q-B — Where may a clean-order LTE restart occur?

Choose exactly one category:

- **IN-SCENARIO RECOVERY ACTION:** part of every applicable trial and therefore part of the treatment definition;
- **MEASUREMENT-BOUNDARY ACTION:** used to establish a common service-ready time, after which application recovery is measured separately;
- **INTER-RUN HYGIENE ONLY:** allowed before the next trial but never inside a trial;
- **NOT ADMISSIBLE:** repair the LTE stack/configuration until autonomous recovery is reproducible.

A hidden or discretionary restart is forbidden.

### Q-C — What time origin should recovery metrics use?

Candidate clocks must be kept distinct:

- `t_rf_restore`: all four attenuators have returned to Q0;
- `t_service_ready`: usable Q0 user plane is proven through `tun_srsue` and the broker endpoint is reachable;
- `t_app_complete`: the predefined application cohort is complete at the sink and the architecture-specific pending state is cleared.

The consortium must decide whether the primary application-drain estimand is `t_app_complete - t_rf_restore`, `t_app_complete - t_service_ready`, or both as separate estimands.

### Q-D — Does H need amendment?

The current H rule is tied to the original recovery clock. The consortium must determine whether to:

- preserve H unchanged;
- amend H to start from a prospectively defined `t_service_ready` while reporting RF-to-service restoration separately;
- replace H with a two-component observation rule;
- or stop the current POWDER design and repair the LTE substrate first.

Any H change must be prospective, versioned, justified, and applied identically to B1/W1/B2 as applicable.

### Q-E — What evidence is required before reopening H?

At minimum, the amendment must define a non-scored qualification proving:

- deterministic start state;
- deterministic service-restoration procedure;
- no stale LTE/MQTT/application state across runs;
- exact timestamps for RF restore, service ready, and application completion;
- unchanged Q0–Q3 RF states;
- unchanged application/runtime comparator semantics;
- reproducible one-command evidence capture;
- explicit PASS/FAIL classification that cannot depend on which architecture performs better.

## 6. Candidate strategies to compare

| Strategy | Scientific fidelity | Reproducibility | Protocol disturbance | Current assessment |
|---|---:|---:|---:|---|
| **A. Repair/qualify autonomous LTE recovery** | Highest | Unknown until proven | Lowest to paper semantics | Preferred if a bounded engineering fix exists |
| **B. Prospectively standardize clean-order service restoration** | Moderate–high if framed as service restoration | High; already demonstrated once | Requires explicit recovery-clock amendment | Strong fallback |
| **C. Change Q3 duration/attenuation or abandon real-RF hard outage** | Lower because RF design is already frozen | Potentially high | High; reopens settled science | Presumptive KILL unless A/B fail |
| **D. Hide/restart LTE ad hoc when recovery stalls** | Invalid | Low | Outcome/operator dependent | KILL |

## 7. Provisional consortium doctrine

Until the full review is closed:

- do **not** rerun H;
- do **not** insert the clean-order LTE restart silently into the existing H plan;
- do **not** downgrade H1 to technical invalidity;
- do **not** reopen Q0–Q3 or shorten the 120 s Q3 merely to avoid the observed failure;
- treat the demonstrated `EPC -> eNB -> UE` sequence as a **qualified recovery primitive**, not yet an approved scientific treatment;
- prefer separation of **RF restoration**, **network-service restoration**, and **application backlog recovery** as distinct observable events;
- optimize for the narrowest prospective amendment that removes LTE/testbed pathology without changing the B1-vs-W1 scientific question.

## 8. Work packages for this gate

| Micro-WP | Task | Exit condition |
|---|---|---|
| RS-1 | Evidence reconstruction | H1 timeline and failure chain reconstructed from raw artifacts, not narrative only |
| RS-2 | LTE recovery mechanism review | Determine whether a bounded config/runtime repair can produce autonomous recovery without changing RF protocol |
| RS-3 | Estimand/H review | Explicit recommendation for `t_rf_restore`, `t_service_ready`, `t_app_complete`, and H semantics |
| RS-4 | Adversarial reviewer attack | Proposed amendment survives confounding, fairness, censoring, and generalization attacks |
| RS-5 | Amendment draft | Versioned protocol amendment with exact PASS/FAIL gates and no discretionary actions |
| RS-6 | Golden E2E rehearsal design | One non-scored end-to-end rehearsal frozen before the next calibration attempt |
| RS-7 | GO/KILL gate | `GO_REOPEN_H` only if RS-1..RS-6 all PASS; otherwise remain `STOP/INVESTIGATE` |

## 9. Required final deliverables

The consortium must produce:

1. a signed-off synthesis verdict (`KEEP / AMEND / REPAIR-FIRST / KILL`);
2. a recovery-semantics decision table with rejected alternatives and reasons;
3. an amended H/protocol document if and only if scientifically justified;
4. a Golden E2E non-scored rehearsal specification;
5. a reviewer-defense paragraph explaining why the chosen recovery procedure does not bias B1 vs W1;
6. an updated `docs/NEXT_GATE.md` and milestone state;
7. explicit statement that `scored_runs_authorized=false` remains until a later immutable pre-score snapshot and authorization gate.

## 10. Immediate frontier

**Start RS-1 — Evidence Reconstruction.**

The next scientific action is offline reconstruction of the H1 timeline and recovery chain from the preserved sender/receiver CSV/JSON/SQLite artifacts and LTE logs. No further H execution is authorized until the consortium has completed the recovery-semantics gate.
