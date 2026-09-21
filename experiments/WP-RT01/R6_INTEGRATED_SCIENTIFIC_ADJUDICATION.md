# WellPulse IEEE Revival — R6 Integrated Scientific Adjudication

## Scope
R6 integrates the frozen protocol semantics, historical FIT evidence, prospective R5 Stage-A evidence, and POWDER physical evidence. It does not rewrite the manuscript and does not select a venue.

## Evidence classes

### E1 — Protocol semantics / implementation audit
Frozen facts:
- MQTT QoS-1 PUBACK closes a publisher-to-broker acceptance obligation; it is not subscriber receipt.
- M0, M1, M2, M3, M4, and M5 remain distinct observables by definition and instrumentation.
- The frozen W1 implementation serially drains historical backlog before resuming new record generation.

These are semantic / implementation facts. They do not by themselves prove a measurable positive M2→M3 delay.

### E2 — Historical FIT campaign
Historical W1 C1 evidence remains valid as provenance-bounded evidence:
- six observed seq5000→seq5001 gaps:
  68.992, 69.466, 68.944, 68.785, 70.264, 68.852 s;
- campaign mean = 69.217 s;
- range = 68.785–70.264 s;
- final receiver reconciliation verified 10,000/10,000 records;
- the old approximately 68 s “recovery” wording is invalid because the measured endpoint was sender-side QoS-1 acknowledgement closure, not receiver-side completion.

Interpretation:
This is evidence of an implementation-specific replay-associated live-generation discontinuity under W1. It is not evidence that MQTT durability generically harms freshness.

### E3 — Prospective scored FIT Stage A
Authority:
- GitHub Actions run 35653569079;
- FIT experiment 449953;
- frozen authority c9fd8968f1408d9a2e3a57dd825df05c2f1d9147;
- raw artifact SHA-256:
  5b52005e48d8987091c447186eb39261824f32df15653c3d2773a031b062d4a2.

Three planned scored W1/C1 runs were all valid.

R1:
- generation gap seq5000→seq5001 = 75.208044774 s;
- H PUBACK coverage = 2000/2000;
- H receiver completion = 2000/2000;
- no historical record arrived after receiver observation of seq5001;
- conservative D23 interval = [-5.037870646, +4.800559282] s;
- verdict = UNRESOLVED.

R2:
- generation gap seq5000→seq5001 = 76.307649507 s;
- H PUBACK coverage = 2000/2000;
- H receiver completion = 2000/2000;
- no historical record arrived after receiver observation of seq5001;
- conservative D23 interval = [-4.857098222, +4.932285786] s;
- verdict = UNRESOLVED.

R3:
- generation gap seq5000→seq5001 = 74.797521961 s;
- H PUBACK coverage = 2000/2000;
- H receiver completion = 2000/2000;
- no historical record arrived after receiver observation of seq5001;
- conservative D23 interval = [-4.858398557, +4.814558148] s;
- verdict = UNRESOLVED.

Prospective campaign summary:
- 3/3 valid;
- 0/3 positive under the frozen decision rule;
- 3/3 UNRESOLVED;
- prospective generation-gap mean = 75.438 s;
- prospective range = 74.798–76.308 s;
- no causal witness in any run;
- no stale-arrival event in any run;
- Stage-A decision = NOT_CONFIRMED_STOP;
- Stage B is neither required nor authorized.

Historical and prospective FIT values must be reported as separate campaigns; they must not be pooled into one effect estimate because execution conditions and instrumentation differed.

### E4 — POWDER physical trace
Frozen POWDER evidence remains:
- at 52 dB in E3 cycle 3, receiver-side arrivals included newer seq251–255 before older seq231;
- this proves that stale carryover / arrival-order inversion can occur after restoration in at least one physical test instance;
- it does not establish prevalence, probability, or generic MQTT behavior.

## Final claim disposition

### C1 — PUBACK closure is not receiver completion
Disposition: ACCEPT — semantic / protocol fact.

Allowed:
“Broker-side QoS-1 acknowledgement closure and receiver-side historical-state completion are distinct endpoints.”

Not allowed:
“PUBACK closure systematically precedes receiver completion by a material interval.”
The prospective campaign did not establish that claim.

### C2 — Serialized W1 replay creates a live-generation discontinuity
Disposition: ACCEPT — strong, implementation-specific empirical result.

Evidence:
- 6/6 historical FIT observations around 69 s;
- 3/3 prospective scored FIT observations around 75–76 s.

Allowed:
“In the tested W1 implementation, serialized historical replay repeatedly delayed generation of the first post-backlog record by roughly 69 s in the historical campaign and roughly 75–76 s in the prospective campaign.”

Not allowed:
- generic durability/freshness causality;
- an assumed periodic source-rate interpretation;
- pooling the two campaign means.

### C3 — Eventual completeness
Disposition: ACCEPT — end-state only.

Allowed:
“Receiver reconciliation verified complete delivery of the tested record set.”

Not allowed:
“Completeness was restored at the sender-side PUBACK endpoint.”

### C4 — Network/session/application recovery are distinct observables
Disposition: ACCEPT — bounded measurement framework.

Allowed:
“The experiment records network-path restoration, MQTT session restoration, broker-side acknowledgement closure, receiver completeness, live-generation continuity, and receiver ordering as separate observables.”

This is a measurement discipline, not an architecture novelty claim.

### C5 — Receiver stale carryover / inversion can occur
Disposition: ACCEPT — single bounded physical observation.

Allowed:
“A POWDER trace exhibited a late older record after newer records had already arrived.”

Not allowed:
- frequency or prevalence claims;
- extrapolation to all outages or MQTT deployments.

### C6 — Endpoint choice materially misclassifies end-to-end service recovery
Disposition: NOT CONFIRMED AS A CENTRAL EMPIRICAL CLAIM.

Reason:
The prospective campaign produced 0/3 positives and 3/3 UNRESOLVED results for M2→M3 under the frozen qualification and causal-witness rules.

Allowed:
“Using broker-side PUBACK closure as a proxy for subscriber completion is semantically unsafe because the endpoints represent different system states.”

Not allowed:
“The study demonstrates repeated material service-state misclassification caused by using M2 instead of M3.”

C6 is removed from the central contribution set and may appear only as a methodological caution / unresolved question.

### C7 — Recovery architecture novelty
Disposition: KILLED.

Known prior work already covers:
- real-time lane plus background synchronization;
- freshness-vs-reconstruction scheduling;
- subscriber-level confirmation.

No paper text may present these mechanisms, their combination, or renamed variants as the primary novelty.

## Surviving scientific object
WellPulse is now an experimental measurement study, not a new recovery architecture.

Frozen scientific object:

“Telemetry recovery should be measured as a set of distinct observables rather than collapsed into a single ‘recovery time.’ Applying that discipline to the tested W1 implementation shows a reproducible completeness–continuity trade-off: serialized backlog replay preserves eventual delivery but repeatedly suspends new record generation for tens of seconds. A separate POWDER trace shows that stale receiver-side carryover can also survive restoration. The prospective campaign did not establish a repeated positive separation between broker-side PUBACK closure and receiver-side historical completion.”

## Contribution set allowed for R7

A1. Recovery-observable measurement protocol
A reproducible protocol that separately records M0–M5 and prevents reconnect, PUBACK closure, receiver completion, continuity, and ordering from being conflated.

A2. Repeated W1 completeness–continuity result
Serialized replay repeatedly produced a large live-generation discontinuity while eventual receiver completeness was preserved.

A3. Cross-environment triangulation without pooling
FIT establishes the implementation-specific replay discontinuity; POWDER contributes a bounded physical stale-carryover observation. The environments are complementary and are not statistically pooled.

A4. Negative / bounded result
The prospective Stage-A campaign did not confirm a repeated positive M2→M3 separation. This negative result is retained explicitly rather than hidden or converted into a favorable claim.

## Prohibited manuscript claims
R7 must not contain any of the following as author conclusions:
- “novel recovery architecture”;
- “first” / “to our knowledge” novelty claims for the architecture;
- “durability harms freshness” as a generic MQTT conclusion;
- “approximately 68 s end-to-end recovery”;
- “PUBACK means subscriber delivery”;
- “the receiver completed after M2 by X seconds” from the current scored campaign;
- “endpoint misclassification was repeatedly demonstrated”;
- pooled FIT+POWDER effect estimates;
- prevalence claims from the single POWDER stale-carryover observation.

## R6 hostile QA

Q1. Does the integrated story contradict the prospective 0/3 result?
PASS. C6 is explicitly demoted and the negative result is preserved.

Q2. Does it over-interpret the negative raw D23 values?
PASS. Raw cross-clock differences are not treated as ordering facts; only conservative intervals are used, and all three cross zero.

Q3. Does it misuse the approximately 75 s generation gaps as periodic-source freshness latency?
PASS. They are described only as replay-associated live-generation discontinuities in the frozen W1 implementation.

Q4. Does it pool historical and prospective FIT values?
PASS. Campaigns are reported separately.

Q5. Does it over-generalize POWDER?
PASS. POWDER remains one bounded physical stale-carryover observation.

Q6. Does it reintroduce killed architecture novelty?
PASS. Architecture novelty remains killed.

Q7. Is eventual completeness confused with recovery latency?
PASS. Completeness is retained only as an end-state result.

Q8. Is a scientifically coherent paper still recoverable?
PASS, with a narrower object: recovery measurement semantics + repeated implementation-specific completeness–continuity behavior + bounded cross-environment evidence + explicit negative M2→M3 result.

## R6 gate
`R6_INTEGRATED_SCIENTIFIC_ADJUDICATION=PASS`

`CENTRAL_C6_MISCLASSIFICATION_CLAIM=NOT_CONFIRMED_AND_DEMOTED`

`SURVIVING_CORE=MEASUREMENT_PROTOCOL_PLUS_W1_COMPLETENESS_CONTINUITY_RESULT`

`R7_ENTRY=UNLOCKED`

R7 must reconstruct the paper around this frozen object and must not restore any killed or demoted claim.
