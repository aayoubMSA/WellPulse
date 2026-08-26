# WP-PWD01 — Recovery Semantics Amendment v1

Date frozen: 2026-08-26
Stage: PRE-SCORE
Authority: RS-2, RS-3, RS-4 consortium outputs
Status: FROZEN FOR NON-SCORED REHEARSAL ONLY
Scored runs authorized: false
H1 remains: VALID_W1_RECOVERY_FAILURE

## 1. Purpose

Prospectively separate physical RF restoration, usable LTE service restoration, and application recovery so that srsLTE substrate pathology does not contaminate the B1/W1/B2 application-level comparison.

This amendment does not reopen Q0–Q3, the 1 Hz workload, B1/W1 comparator semantics, S0–S3 definitions, pairing/randomization, or the primary completeness concept.

## 2. Frozen clocks

- `t_rf_restore`: UTC time when all four attenuator IDs `1 33 2 34` have completed Q3 -> Q0.
- `t_service_ready`: UTC time when the frozen architecture-blind service probe first passes after the standardized service-restoration procedure.
- `t_app_complete`: UTC time when the predefined primary cohort is complete at the sink with valid identity/checksum and the architecture's prospectively defined pending cohort state is cleared.

Derived outcomes:

- `T_service = t_service_ready - t_rf_restore`
- `T_app = t_app_complete - t_service_ready`
- `T_total = t_app_complete - t_rf_restore`

All three must be preserved. `T_app` isolates application recovery; `T_total` remains the end-to-end operational consequence.

## 3. Primary cohort

The primary cohort remains:

`all valid records generated at or before t_rf_restore`

The cohort cutoff must not move to `t_service_ready`. Outage-generated records remain part of the durability obligation.

## 4. Architecture-independent observation horizon

Freeze one common fixed application observation horizon:

`H_app = 300 s`

measured from `t_service_ready` for every architecture and applicable scenario.

Justification: 300 s was already the pre-H1 engineering feasibility ceiling in the frozen H design. It therefore predates comparative scored outcomes and is independent of B1/W1/B2 performance. RS-5 promotes that existing engineering ceiling into a fixed common observation window to eliminate arm-informed horizon calibration.

The confirmatory primary endpoint becomes:

`completeness_300 = unique valid primary-cohort records received no later than (t_service_ready + 300 s) / primary-cohort generated records`

No W1-only, pooled-outcome, scenario-specific, or post-hoc horizon calibration is permitted.

Recovery speed remains secondary through `T_app` and `T_total`. Ceiling completeness in S1/S2 is scientifically acceptable and should be interpreted as evidence that standard QoS1 is sufficient under those network-only conditions.

## 5. Standardized service-restoration rule

### S2 and S3

Immediately after `t_rf_restore`, execute the same scripted clean-order LTE substrate reinitialization in every B1/W1/B2 run where applicable:

1. stop UE LTE process only; do not stop the application publisher except for the prospectively specified S3 gateway-process restart already defined by the scenario;
2. reset/start EPC and wait for deterministic core readiness;
3. start eNB and wait for deterministic RAN readiness;
4. start a fresh UE only after EPC/eNB readiness;
5. run the frozen architecture-blind service probe;
6. set `t_service_ready` only when that probe passes.

The broker and application treatment must remain identical across architectures, except for the already frozen S3 gateway-process restart factor.

This clean-order LTE sequence is a **measurement-boundary substrate operation**, not WellPulse recovery and not an architecture treatment.

### S0 and S1

No forced LTE restart is added. At the scenario cutoff/pseudo-cutoff, execute the same service-ready probe. Failure of the architecture-blind probe within the frozen qualification bound defined in RS-6 is handled under the same infrastructure-invalidity rule below.

## 6. Frozen service-ready probe requirements

RS-6 must implement one command that proves, without inspecting architecture/application outcomes:

- expected UE tunnel exists;
- route to broker endpoint uses `tun_srsue`;
- bounded user-plane reachability to the experimental endpoint passes;
- TLS handshake to the broker endpoint passes;
- timestamps for restoration start/end and probe PASS are emitted.

The exact packet counts/timeouts are implementation details to be frozen in RS-6 before execution. The probe must not inspect queue depth, record delivery, application identity, or comparative outcomes.

## 7. Service-restoration failure / invalidity

A run may be classified `TECHNICALLY_INVALID_SERVICE_RESTORE` only if:

- the frozen RF schedule was applied correctly;
- the standardized architecture-blind service-restoration procedure was executed exactly;
- the frozen service probe fails within its predeclared RS-6 bound;
- classification occurs before inspection of application delivery/completeness outcomes.

The attempt remains preserved and counted in the infrastructure-failure ledger. Replacement is allowed only under this exact rule and receives a new run ID.

An unfavorable B1/W1/B2 application outcome after `t_service_ready` is never technical invalidity.

## 8. Fairness invariant

No architecture may receive a different RF schedule, service-restoration trigger, restoration procedure, service-ready test, 300 s application horizon, stopping rule, or exclusion rule because of architecture identity or observed performance.

## 9. Negative/null-result interpretation tree — frozen before scoring

- B1 approximately W1 in S1/S2: standard QoS1 is sufficient while volatile process state survives; informative boundary result.
- W1 > B1 in S3: evidence for application-level durability across volatile-state destruction.
- B2 approximately W1 in S3: standard durable MQTT can close much of the gap; narrow the WellPulse contribution accordingly.
- B2 > W1 or W1 has no material advantage: valid negative result; do not change RF states, horizon, scenarios, or exclusions to recover a preferred story.

## 10. H1 treatment

H1 remains valid adverse evidence under the prior frozen protocol. It is not retroactively reclassified, not used to estimate `H_app`, and not replaced. Its role is methodological/substrate characterization and provenance.

## 11. Evidence escrow — mandatory

Every future rehearsal/calibration/scored run must pass the fail-closed Evidence Escrow Gate before experiment teardown:

source raw bundle -> SHA-256 -> `/proj/WellPulse` verified copy -> off-POWDER verified copy -> provenance record -> `EVIDENCE_ESCROW_GATE=PASS` -> only then terminate.

## 12. Acceptance gate

RS-5 = PASS only if this amendment is treated as prospective and no new physical run is executed until RS-6 freezes a one-command Golden E2E rehearsal implementing:

- exact service-restoration workflow;
- exact service-ready probe and timeout;
- exact evidence schema;
- exact progress-visible fail-closed escrow;
- deterministic PASS/FAIL classifications.

Until RS-6 and RS-7 pass: `scored_runs_authorized=false`.
