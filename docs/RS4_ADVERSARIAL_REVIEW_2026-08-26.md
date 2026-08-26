# WellPulse WP2 — RS-4 Adversarial Reviewer Attack

Date: 2026-08-26
Stage: POST-H1 / PRE-AMENDMENT / PRE-SCORE
Input: `docs/RS3_ESTIMAND_H_FAIRNESS_REVIEW_2026-08-26.md`
Scored runs authorized: false
H: UNFROZEN
H1: `VALID_W1_RECOVERY_FAILURE`, preserved unchanged

## Verdict

**CONDITIONAL PASS — the RS-3 two-clock decomposition survives, but one material design weakness must be removed before RS-5: the primary application observation horizon must not be calibrated from W1 performance alone.**

The consortium therefore accepts:

- `t_rf_restore`, `t_service_ready`, `t_app_complete` as distinct clocks;
- mandatory reporting of substrate recovery `T_service`;
- architecture recovery `T_app` measured from a common service-ready boundary;
- `cohort_cutoff_utc = t_rf_restore`;
- architecture-blind service-restoration rules;
- H1 preserved as adverse evidence.

But RS-4 rejects the proposed W1-only `H_app` calibration because the primary completeness endpoint would then be observed at a horizon chosen from the performance of one architecture under comparison. Even though the calibration is non-scored and does not inspect B1, a skeptical reviewer can reasonably argue that this structurally privileges W1.

RS-5 must replace that rule with an architecture-independent observation horizon or an architecture-independent calibration mechanism.

## Seven-role adversarial review

### 1. Controlled-RF / wireless experimentation lead

**Attack:** A scripted LTE restart after Q3 risks converting a real-RF recovery experiment into an operator-assisted infrastructure-reset experiment.

**Finding:** The attack is valid if the restart is hidden, discretionary, or triggered after observing application behavior. It is substantially mitigated if the paper states that the physical treatment is the Q3 RF outage, while service restoration is a separate standardized measurement-boundary operation necessitated by the specific srsLTE testbed substrate.

**Required hardening:**

- preserve `t_rf_restore` independently;
- never call the clean-order restart “WellPulse recovery”;
- report `T_service` for every applicable run;
- define the exact restoration rule before scoring;
- do not shorten Q3 or change Q0–Q3.

Position: **PASS WITH DISCLOSURE**.

### 2. LTE/EPC/RAN systems lead

**Attack:** If service restoration is conditional on whether natural LTE recovery happens, then different runs may receive materially different substrate treatments.

**Finding:** H1 showed stale context/IP continuity behavior. A conditional operator decision would be vulnerable to bias and non-reproducibility.

**Required hardening:** For each scenario to which standardized restoration applies, RS-5 must define one deterministic trigger based only on RF/testbed state. Two acceptable forms are:

1. always execute the same clean-order service reinitialization at the frozen post-Q3 boundary; or
2. allow a short, fixed, architecture-blind autonomous-recovery grace interval, followed by the same scripted clean-order restoration if and only if the predeclared service probe fails.

No queue depth, delivery state, architecture identity, or comparative outcome may participate in the decision.

Position: **PASS IF DETERMINISTIC**.

### 3. Distributed-systems reliability lead

**Attack:** Subtracting `T_service` from recovery can make operational downtime look artificially small and may hide a real system cost.

**Finding:** Valid concern. `T_app` is suitable for isolating the application mechanism but is not sufficient as the sole operational recovery metric.

**Required hardening:** Always report all three:

- `T_service = t_service_ready - t_rf_restore`;
- `T_app = t_app_complete - t_service_ready`;
- `T_total = t_app_complete - t_rf_restore`.

The paper may use `T_app` for architecture-mechanism interpretation, but must discuss `T_total` as the end-to-end operational consequence.

Position: **PASS WITH THREE-CLOCK REPORTING**.

### 4. MQTT / IIoT protocol lead

**Attack:** The restoration procedure might reset or perturb MQTT/application state differently for B1 and W1.

**Finding:** The demonstrated clean-order primitive stopped/restarted LTE components, not the WellPulse/MQTT application process, and the post-recovery path passed 3/3. Nevertheless the future procedure must explicitly keep broker and application process treatment matched unless the scenario itself specifies a gateway-process restart (S3).

**Required hardening:**

- S2 service restoration must not restart B1/W1 publisher processes;
- S3 keeps exactly the frozen gateway-process restart treatment and must not add architecture-specific restart behavior;
- broker treatment identical across architectures;
- fresh run-unique MQTT identity/topic/session-state isolation remains mandatory.

Position: **PASS**.

### 5. Experimental-design & statistics lead

**Attack A — W1-calibrated horizon:** `H_app` chosen from W1 drain times can structurally favor W1 in the confirmatory completeness endpoint.

**Finding:** **SUSTAINED — MATERIAL.** The old design intentionally avoided comparative outcome inspection, but the observation horizon is still selected from one treatment arm. This is unnecessary and creates avoidable reviewer attack surface.

**Required change:** RS-5 must use an architecture-independent fixed horizon or architecture-independent calibration source. The simplest defensible option should be preferred.

**Attack B — cohort cutoff:** Moving the cohort cutoff to `t_service_ready` would omit outage-generated records.

**Finding:** Rejected. Keeping `cohort_cutoff_utc = t_rf_restore` is correct because the pre-restoration/outage-generated cohort is precisely the durability obligation.

**Attack C — service-restoration failure and censoring:** If service cannot be restored, excluding the run could selectively remove difficult conditions.

**Required hardening:** Define service-restoration failure prospectively as a testbed/infrastructure validity failure only when the frozen RF treatment was applied but the standardized architecture-blind service-boundary procedure cannot establish service. Preserve the attempt, report the failure count, and allow replacement only under the same predeclared rule. Never inspect application outcomes before classifying it.

Position: **CONDITIONAL PASS; HORIZON RULE MUST CHANGE**.

### 6. Reproducibility / artifact lead

**Attack:** The restoration boundary may become an operator-only sequence that cannot be reproduced or audited.

**Finding:** The newly frozen Evidence Escrow Gate substantially improves the design, but RS-5/RS-6 must make restoration and evidence capture one-command and fail-closed.

**Required hardening:**

- one scripted restoration workflow;
- visible shell progress;
- exact timestamps for RF restore, restoration start/end, service-ready probe, and application completion;
- source/runtime/config fingerprints;
- immutable raw evidence copied to `/proj/WellPulse` and off POWDER before teardown;
- no termination without `EVIDENCE_ESCROW_GATE=PASS`.

Position: **PASS IF AUTOMATED**.

### 7. Adversarial reviewer / editor lead

**Attack:** “You discovered your planned experiment failed, then changed the clock until your architecture could win.”

**Finding:** This is the strongest narrative threat. The defense is credible only because:

- H1 is preserved and remains a valid adverse result;
- the amendment occurs before any scored B1/W1 result exists;
- the amendment separates an observed LTE substrate pathology from the application estimand rather than deleting the pathology;
- `T_service` and `T_total` remain visible;
- the same rule applies to all architectures;
- no RF state or failure scenario is weakened.

**Required manuscript language:** State explicitly that H1 exposed a testbed-specific separation between physical RF restoration and usable service restoration, motivating a prospective pre-score decomposition of substrate and application recovery. Do not present the amendment as improving WellPulse performance.

Position: **PASS IF TRANSPARENT AND PRE-SCORE**.

## Decision table

| Design element | RS-4 decision | Reason |
|---|---|---|
| Separate `t_rf_restore` | KEEP | preserves physical-treatment evidence |
| Separate `t_service_ready` | KEEP | prevents LTE substrate pathology from contaminating application recovery |
| Separate `t_app_complete` | KEEP | defines actual application completion |
| `cohort_cutoff = t_rf_restore` | KEEP | preserves outage-generated durability obligation |
| Report `T_service` | MANDATORY | prevents hiding substrate downtime |
| Report `T_app` | MANDATORY | isolates architecture recovery |
| Report `T_total` | MANDATORY | preserves operational end-to-end interpretation |
| Clean-order LTE restart | CONDITIONAL KEEP | only as deterministic architecture-blind measurement-boundary operation |
| Architecture-dependent restoration | KILL | direct confounding/fairness violation |
| Hidden/ad-hoc restart | KILL | outcome/operator dependent |
| W1-only `H_app` calibration | **KILL** | primary horizon chosen from one architecture's performance |
| Move cohort cutoff to service-ready | KILL | removes scientifically important outage records |
| Reclassify H1 | KILL | retrospective outcome-driven revision |
| Change Q3/Q0 states | KILL | unnecessary reopening of frozen RF science |

## Required RS-5 horizon decision

RS-5 must choose **one architecture-independent rule before any new physical run**. Ranked by simplicity and reviewer defensibility:

### Preferred: fixed common `H_app`

Choose a single fixed service-ready observation horizon prospectively from protocol/engineering constraints, not B1/W1 outcomes. The existing 300 s stop bound is a candidate upper bound, but RS-5 must justify the exact fixed value rather than inherit it automatically.

Advantages:

- no arm-informed horizon selection;
- no H-calibration campaign solely to choose an endpoint window;
- simpler execution and analysis;
- permanent losses under S3 remain visible;
- recovery speed remains available as secondary `T_app`/`T_total` outcomes.

Risk: too-long H may create ceiling completeness in network-only S1/S2. This is scientifically acceptable if it demonstrates standard QoS1 is adequate there; the principal durability contrast can remain S3.

### Acceptable fallback: architecture-independent calibration

Calibrate a fixed horizon from an architecture-neutral service/load benchmark that does not observe B1 or W1 delivery outcomes. This is more complex and should be used only if a fixed horizon cannot be justified.

### Rejected

- W1-only calibration;
- pooled B1/W1 outcome-driven calibration;
- scenario-specific horizons selected after seeing results.

## Confirmatory endpoint implication

The primary completeness endpoint should remain:

`unique valid primary-cohort records received by t_service_ready + H_app / primary-cohort generated records`

with:

`primary cohort = valid records generated at or before t_rf_restore`.

This preserves equal opportunity after usable service is restored while retaining all outage-generated records in the denominator.

`T_service` and `T_total` are mandatory companion outcomes so the endpoint cannot be interpreted as ignoring substrate recovery.

## Negative/null-result protection

Before scoring, RS-5 must freeze the interpretation tree:

- B1 approximately W1 in S1/S2: standard QoS1 is sufficient when process state survives; informative boundary result.
- W1 > B1 in S3: evidence for application durability across volatile-state destruction.
- B2 approximately W1 in S3: standard durable MQTT can close much of the gap; narrow WellPulse contribution accordingly.
- B2 > W1 or W1 shows no material advantage: preserve as valid negative result; do not modify scenarios/horizon to recover a preferred story.

## RS-4 acceptance gate

**PASS WITH ONE MANDATORY MODIFICATION.**

The two-clock recovery decomposition and fairness framework survive adversarial review. The W1-calibrated observation horizon does not.

RS-5 may proceed only if it:

1. adopts an architecture-independent H rule;
2. freezes a deterministic architecture-blind service-restoration rule;
3. preserves `t_rf_restore`, `T_service`, `T_app`, and `T_total`;
4. keeps cohort cutoff at `t_rf_restore`;
5. defines symmetric service-restoration failure/invalidity rules before outcome inspection;
6. embeds fail-closed evidence escrow into the executable protocol;
7. freezes the negative/null-result interpretation tree.

Until RS-5 through RS-7 pass, no H calibration or scored run is authorized.
