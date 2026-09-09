# WP4 — IEEE TNSM Reviewer Attack-Surface Closure

**Date:** 2026-09-09  
**Target:** IEEE Transactions on Network and Service Management (TNSM)  
**Status:** PASS WITH POSITIONING CORRECTION  
**Scientific authority:** existing FIT IoT-LAB and POWDER evidence only; no new experiments and no numerical changes.

## 1. Executive decision

The TNSM route remains viable, but WP4 identified one material novelty correction: the paper must **not** claim novelty merely from separating network/path recovery, application/service recovery, and data continuity. Recent prior work already makes that distinction explicitly.

The protected contribution is narrower and stronger:

> **Receiver-verified recovery closure for stateful MQTT telemetry: a recovery declaration is not complete until the relevant receiver-side application state is reconciled, and the evidence must preserve the active failure domain, declared endpoint, and timing semantics. Physical experiments show both (i) a durable catch-up interval that persists long after connectivity returns and (ii) failure-domain-dependent recovery observations that cannot be collapsed into a single latency.**

The manuscript should therefore foreground the **post-reconnect incomplete-state interval** and the **recovery-declaration evidence semantics**, not the generic observation that recovery is layered.

## 2. Most dangerous prior art and resulting correction

### A. Digital Twins at the Edge (Future Internet, 2026)

This work already separates:
- network-layer recovery (VIP reachability),
- application-layer recovery (MQTT broker and processing-service readiness), and
- data-layer continuity (message loss).

It reports approximately 1.35 s network failover, MQTT broker recovery, and message loss during failover. Therefore the following claims are **NOT novel and must be explicitly disclaimed**:
- network recovery is different from application recovery;
- service recovery requires more than reachability;
- message continuity should be checked separately from path recovery.

### Retained delta versus that work

WellPulse is not an HA architecture paper and does not compete on failover design. Its differentiated evidence is:

1. **Durable catch-up after connectivity is already restored.** FIT shows a state that is neither simple outage nor permanent loss: the path reconnects at roughly 1.3 s, all records eventually survive, yet receiver-confirmed historical completeness is not reached until roughly 68 s. This exposes a prolonged *post-reconnect incomplete-state interval* that a binary availability or broker-readiness monitor would close prematurely.

2. **Receiver-side closure rather than service-process readiness.** A sender PUBACK, successful publish, ping, broker connection, or process status is diagnostic evidence; final data-state closure is established by reconciliation of generated versus receiver-observed identities at the declared endpoint.

3. **Heterogeneous failure-domain evidence.** POWDER covers RF, UE/client, core-network, and broker/service interventions rather than one HA failover mechanism.

4. **Observation semantics are preserved.** Exact, censored, and upper-bound recovery observations remain distinct; unsupported scalar latencies are not manufactured.

The novelty statement must be written around these four points, not around generic multi-layer recovery.

## 3. Reviewer attack matrix

| Attack | Severity before WP4 | Closure | Residual risk |
|---|---|---|---|
| "Layered recovery is already known." | CRITICAL | Concede explicitly; remove firstness. Cite the 2026 HA work and reposition on receiver-verified closure, post-reconnect durable catch-up, failure-domain/endpoint/timing semantics. | LOW-MEDIUM |
| "The B0 vs W1 result is trivial because B0 is intentionally non-durable." | HIGH | Agree. B0 is only a negative mechanism-isolation control. Do not sell 80% vs 100% as mechanism novelty or superiority. The primary TNSM result is W1's own reconnect-to-complete-state separation plus cross-domain recovery observability. | LOW |
| "Why no durable MQTT baseline?" | HIGH | State directly that comparison among durable MQTT mechanisms is outside the claim. A stronger persistent client/broker may eliminate the completeness gap; this does not remove the recovery-declaration problem because a durable configuration can still have a non-zero post-reconnect catch-up interval. | MEDIUM |
| "Only three FIT replicates." | HIGH | No population reliability inference, CI, or p-value. Run is the unit; all raw run values are shown. Treat repeated identical completeness outcomes as bounded engineering observations. Timing values are descriptive with ranges. | MEDIUM |
| "10,000 messages are pseudo-replication." | HIGH | Explicitly state messages are reconciliation records, not independent experimental samples. Scientific n is three runs per cell. | LOW |
| "Two testbeds are heterogeneous and cannot validate each other." | HIGH | Do not call them replication or cross-validation. FIT = record-state survival/catch-up; POWDER = path/failure-domain characterization. No pooling or cross-platform effect estimate. | LOW |
| "POWDER 52 dB threshold is arbitrary/universalized." | HIGH | Preserve experiment-specific transition-region language; no universal threshold, interpolation, or fitted boundary. | LOW |
| "Recovery latency values are incomparable." | HIGH | Agree and make this a result. FIT backlog drain, POWDER exact endpoints, censored E10-A, and upper-bound E10-D are separate constructs and must not share one generic latency distribution. | LOW |
| "MQTT robustness/fault injection is prior art." | HIGH | Concede. Jesus et al. 2025 evaluates robustness by MQTT-message fault injection. WellPulse does not claim novelty from fault injection; it studies recovery declarations and receiver-side application-state closure under service/network disruptions. | LOW |
| "MQTT reliability stress testing is prior art." | HIGH | Concede. Gaspar et al. 2026 studies parameter-driven RTT/loss/delay and reliability tradeoffs. WellPulse's question is incident/recovery-state semantics, not protocol parameter benchmarking. | LOW |
| "TNSM contribution is too IoT-specific." | MEDIUM-HIGH | Translate results into service-management artifacts: separate incident closure for path availability and application-state recovery; define recovery endpoint and evidence authority; preserve domain-specific timing semantics. | MEDIUM |
| "This is only a methodology paper." | HIGH | Data-first narrative. Physical FIT and POWDER results lead; assurance method is derived from observed contradictions between path, service, and state evidence. | LOW-MEDIUM |

## 4. Corrected novelty statement for manuscript use

Recommended wording:

> Prior work has established MQTT persistence mechanisms, robustness and performance testing, broker high availability, and the need to distinguish network, application-service, and data-continuity recovery. This study does not claim those distinctions as new. Instead, it operationalizes **receiver-verified recovery closure** for stateful telemetry: a recovery declaration is tied to a named failure domain and endpoint and remains incomplete when the required receiver-side application state has not yet been reconciled. The physical experiments expose two cases that matter to service management: durable records can remain in catch-up for tens of seconds after connectivity returns, and recovery observations across RF, client, core-network, and broker failures may be exact, censored, or only upper-bounded. The contribution is therefore the evidence required to close a telemetry recovery incident, not a new MQTT persistence or failover mechanism.

## 5. Revised result hierarchy after hostile review

WP3's data-first direction remains correct, but the hierarchy is refined:

### Primary result P1 — Post-reconnect incomplete-state interval

For W1 under the tested FIT workload:
- path reconnect ≈ 1.3 s;
- complete receiver-reconciled backlog recovery ≈ 67.7–67.9 s.

This is the strongest TNSM result because it does not depend on claiming superiority over B0.

### Primary result P2 — Receiver-state consequence of absent durability

B0 C1/C2 = 8,000/10,000 versus W1 = 10,000/10,000 in all three runs. Use only to demonstrate why a path-up signal cannot establish historical completeness and why persistence boundary must be named. Do not present as novel durable-mechanism comparison.

### Primary result P3 — Cross-layer/path indicators can disagree

POWDER E1R4 at 51 dB: ICMP loss 30% while MQTT receiver completeness remains 20/20. This supports the management need to avoid treating one lower-layer health metric as a universal application-state proxy.

### Primary result P4 — Recovery evidence is endpoint/domain-specific

- E10-A: censored, no scalar latency;
- E10-B: exact action-begin → first MQTT publish 6.063318 s and first ping 6.609430 s;
- E10-C-B: exact RF restore → first publish 29.248129 s;
- E10-D: upper bound <=10.908749 s.

Do not combine these into one mean or distribution.

## 6. Service-management artifact to add

Add one compact **Recovery Declaration Matrix** (table, not a new experimental result) in the Discussion or model section:

| Management state | Evidence needed | Incident interpretation |
|---|---|---|
| Path restored | declared network/transport endpoint succeeds | Connectivity incident may close; data-state incident remains open |
| Current publish path available | declared MQTT/service endpoint succeeds | New traffic may flow; historical completeness still unknown |
| Durable backlog pending | receiver state incomplete / queue not fully reconciled | Recovery ongoing despite path availability |
| Application state recovered | generated/required identities reconciled at receiver endpoint | Historical-data recovery incident may close |
| Recovery not observed | observation window ends without endpoint success | Censored; do not assign scalar latency |
| Recovery only bounded | first observed success follows an interval with unknown exact transition | Report upper bound only |

This table makes the TNSM management contribution actionable without inventing a new mechanism or dataset.

## 7. Related-work structure required

Use four direct blocks only:

1. **MQTT persistence and reliable delivery mechanisms** — establish that persistence/store-and-forward are prior art.
2. **MQTT robustness, stress testing, broker performance and clustering** — establish that fault testing and availability engineering are prior art.
3. **Layered/high-availability recovery and data continuity** — explicitly discuss the 2026 multi-layer HA work and concede overlap.
4. **Retained gap: recovery-incident closure evidence** — receiver-confirmed state, durable catch-up after reconnect, named failure-domain/endpoint semantics, and censored/upper-bound timing.

Do not end Related Work with "we are the first to separate recovery layers." Do not use "novel framework" as the central phrase.

## 8. Sample-size defense language

Recommended wording:

> The FIT experiment uses the run as the scientific unit; the 10,000 within-run records are used for deterministic identity reconciliation and are not treated as independent samples. Each architecture-condition cell contains three independent run-level replicates. Because the completeness outcomes repeat exactly across those runs, they are reported as bounded repeated engineering observations rather than estimates of population reliability. No confidence interval or hypothesis test is constructed from message counts. Timing results are reported descriptively with the preserved run-level values and ranges.

This is a limitation, not a statistical strength claim.

## 9. Two-testbed defense language

Recommended wording:

> FIT IoT-LAB and POWDER are deliberately assigned non-overlapping evidence roles. FIT evaluates record-state survival and backlog reconciliation under controlled broker/process disruption. POWDER characterizes physical/network/service failure domains and endpoint-specific recovery. Their results are not pooled, and agreement between the platforms is not treated as replication. The synthesis concerns the management semantics exposed by both evidence classes, not a cross-platform reliability estimate.

## 10. New experiments decision

**No new experiment is required before TNSM submission.**

Rationale:
- the remaining durable-comparator limitation is acknowledged and removed from the novelty claim;
- the principal W1 reconnect-versus-catch-up result is internally supported without B0 superiority;
- the physical POWDER evidence adds distinct failure-domain and recovery-semantics observations;
- additional experimentation would improve external validity but is not required to make the bounded service-management claim truthful.

Trigger for reopening experiments only if manuscript construction reveals that the TNSM contribution still depends on durable-mechanism superiority or a population reliability estimate. Under the current protected wedge, it does not.

## 11. WP4 gate

- dangerous direct prior art identified: PASS;
- overlapping novelty explicitly surrendered: PASS;
- protected novelty narrowed to evidence-supported delta: PASS;
- durable-comparator attack contained without concealment: PASS;
- sample-size semantics defensible and non-pseudoreplicated: PASS;
- two-testbed heterogeneity bounded: PASS;
- service-management significance made operational: PASS;
- unsupported new experiment requirement: NO;
- numerical changes to evidence: NONE;
- new scientific claim outside frozen evidence: NONE.

`WP4_TNSM_ATTACK_SURFACE=PASS`

`WP4_MATERIAL_CORRECTION=DO_NOT_CLAIM_LAYERED_RECOVERY_SEPARATION_AS_NOVEL`

`WP4_PROTECTED_WEDGE=RECEIVER_VERIFIED_RECOVERY_CLOSURE_PLUS_POST_RECONNECT_STATE_LAG_PLUS_DOMAIN_ENDPOINT_TIMING_SEMANTICS`

`WP4_NEW_EXPERIMENT_REQUIRED=NO`

`WP4_NEXT=WP5_IEEE_TNSM_MANUSCRIPT_CONVERSION_AND_SUBMISSION_PACKAGE`
