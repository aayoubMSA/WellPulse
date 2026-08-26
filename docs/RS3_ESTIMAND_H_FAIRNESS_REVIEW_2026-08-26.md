# WellPulse WP2 — RS-3 Estimand / H / Fairness Review

Date: 2026-08-26
Stage: POST-H1 / PRE-AMENDMENT / PRE-SCORE
Scored runs authorized: false
H: UNFROZEN
H1 Trial #1: VALID_W1_RECOVERY_FAILURE; preserved unchanged.

## RS-3 verdict

**PASS — recommend a prospective two-clock recovery decomposition, with a common service-ready measurement boundary and an application-drain horizon calibrated from service readiness.**

This is a recommendation for RS-4 adversarial review. It is not yet a protocol amendment and does not authorize H calibration or scored runs.

## Evidence constraints

The frozen H-calibration plan currently defines the cohort cutoff at the final Q3->Q0 RF restoration timestamp and defines backlog-drain time from that same timestamp. H1 then showed that RF restoration did not imply restoration of usable LTE user-plane service: radio recovery occurred, but EPC/MME/SPGW context pathology prevented service recovery. A coordinated clean-order LTE restart subsequently restored the LTE path, after which the application path passed independently 3/3.

Therefore one scalar clock from RF restoration to application completion conflates two mechanisms:

1. substrate/testbed service restoration; and
2. architecture/application backlog recovery.

That conflation is not acceptable for the intended B1-vs-W1 application-level reliability comparison.

## Frozen observable clocks recommended for amendment

### t_rf_restore
The earliest UTC timestamp at which all four frozen attenuator IDs `1 33 2 34` have completed the Q3->Q0 transition.

This remains the physical treatment endpoint. It must always be preserved and reported.

### t_service_ready
The first UTC timestamp after `t_rf_restore` at which a prospectively frozen, architecture-blind qualification proves usable experimental network service. At minimum:

- the UE experimental tunnel exists and has the expected run-specific addressing state;
- route to the experimental broker endpoint traverses `tun_srsue`;
- bounded user-plane reachability through that path passes;
- no architecture-specific queue/drain state is consulted in declaring readiness.

The exact probe and thresholds must be frozen in RS-5/RS-6 before any new H trial.

### t_app_complete
For the predefined application cohort, the first UTC timestamp at which all required cohort records have arrived at the sink with matching identity/checksum and the architecture-defined pending cohort state is cleared, using prospectively frozen architecture-specific completion semantics.

For W1, the existing conservative completion rule remains conceptually appropriate: sink cohort complete AND durable pending cohort cleared. Broker PUBACK alone is insufficient.

## Primary estimands

RS-3 recommends reporting two separate quantities rather than hiding substrate recovery inside one H metric:

`T_service = t_service_ready - t_rf_restore`

`T_app = t_app_complete - t_service_ready`

A descriptive total may also be reported:

`T_total = t_app_complete - t_rf_restore = T_service + T_app`

But `T_total` must not be the sole primary architecture-recovery estimand because it contains LTE/testbed recovery behavior that is not the WellPulse mechanism under comparison.

## H recommendation

**AMEND prospectively.**

The current H is not salvageable unchanged because it begins at `t_rf_restore`, while H1 demonstrated that this origin can include a substrate-specific service outage unrelated to the application comparator.

Recommended semantics:

- retain `t_rf_restore` and `T_service` as mandatory real-RF/testbed outcomes;
- calibrate the common application observation horizon `H_app` from successful W1 `T_app` values measured from `t_service_ready`;
- preserve the existing conservative calculation structure unless RS-4 identifies a statistical defect:

`p95_app = max(T_app across exactly 3 successful non-scored W1 calibration trials)`

`H_app = max(120 s, ceil_to_30s(2 * p95_app))`

- preserve the existing `H_app > 300 s => STOP AND INVESTIGATE` safeguard;
- do not reinterpret the n=3 maximum as a stable population p95.

The old H remains UNFROZEN and must not be retroactively computed from H1.

## Service-restoration action classification

RS-3 recommends that the demonstrated clean-order LTE recovery primitive, if RS-4/RS-5 ultimately admit it, be classified as a **MEASUREMENT-BOUNDARY ACTION**, not an architecture treatment and not a hidden in-scenario recovery behavior.

It must be:

- prospectively scripted;
- triggered by architecture-blind rules only;
- identical for B1/W1/B2 where applicable;
- completed before `t_service_ready`;
- fully timestamped;
- excluded from `T_app` but included in `T_service` and `T_total`;
- never initiated based on queue depth, record delivery, architecture identity, or observed comparative performance.

This preserves real-RF outage exposure while preventing an srsLTE-specific stale-context failure from being scored as WellPulse application behavior.

## Fairness invariant

The following invariant is mandatory for any later amendment:

> No architecture may receive a different RF schedule, service-restoration trigger, restoration procedure, service-readiness test, application observation horizon, stopping rule, or run-exclusion rule because of its identity or observed performance.

The service boundary must be architecture-blind. Application-specific completion semantics may differ only where required by the architecture's predeclared state model, and those semantics must be frozen before scored execution.

## Cohort boundary recommendation

The application cohort should remain tied to the physical treatment, not moved to service readiness merely because the network is unavailable.

Recommended cohort cutoff:

`cohort_cutoff_utc = t_rf_restore`

Thus records generated during the Q3 outage remain part of the recovery obligation. Moving the cohort cutoff to `t_service_ready` would discard exactly the records whose durability under outage is scientifically important and would bias the comparison.

Records generated after `t_rf_restore` require a separately frozen rule in RS-5; RS-3 recommends retaining the existing cutoff at RF restoration for the recovery cohort so post-restore ongoing workload cannot make completion a moving target.

## Treatment of H1

No change:

- H1 remains `VALID_W1_RECOVERY_FAILURE` under protocol v1 semantics;
- it is not eligible as one of the three future successful H_app calibration trials;
- it is not relabeled TECHNICALLY_INVALID;
- its LTE pathology is retained as negative/testbed-characterization evidence;
- it cannot be used to estimate H_app because `t_service_ready` under the prospective definition was not part of the frozen H1 protocol.

## Alternatives rejected at RS-3

1. **Keep old H from t_rf_restore.** Rejected because it conflates substrate restoration with application recovery after H1 demonstrated the separation empirically.
2. **Start both cohort and H at t_service_ready.** Rejected because this would remove outage-generated records from the durability obligation and weaken the scientific question.
3. **Treat clean-order LTE restart as W1 recovery.** Rejected because it is testbed substrate recovery, not WellPulse application behavior.
4. **Ignore T_service and publish only T_app.** Rejected because the experiment claims real-RF validity; service restoration is material evidence and must remain visible.
5. **Architecture-dependent restart/readiness rules.** Rejected as direct fairness/confounding violation.
6. **Retroactively repair/reclassify H1.** Rejected as outcome-dependent protocol revision.

## RS-3 acceptance gate

PASS because the review now provides explicit, non-overlapping definitions for:

- physical RF restoration;
- usable service restoration;
- application completion;
- primary application recovery estimand;
- mandatory substrate-recovery outcome;
- cohort boundary;
- prospective H semantics;
- fairness invariant;
- treatment of H1.

## Remaining attack surface for RS-4

RS-4 must attempt to falsify this recommendation, especially:

1. whether a scripted LTE restart after every Q3 creates an artificial network treatment;
2. whether service-ready detection can truly be architecture-blind;
3. whether `T_app` unfairly removes an operationally meaningful outage component;
4. whether the W1-only H_app calibration can define a fair common horizon for B1/W1/B2;
5. whether censoring/failure rules remain symmetric when service restoration itself fails;
6. whether the n=3 max-based H_app remains defensible as an operational horizon rather than inferential percentile;
7. whether the proposed cohort cutoff at t_rf_restore preserves the intended reliability estimand without introducing post-outage generation ambiguity.

Until RS-4 through RS-7 pass, `scored_runs_authorized=false` and no new H calibration is authorized.
