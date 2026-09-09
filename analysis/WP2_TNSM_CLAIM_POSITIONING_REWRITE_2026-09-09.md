# WP2 — IEEE TNSM Claim Architecture & Positioning Rewrite

**Date:** 2026-09-09  
**Status:** CANDIDATE POSITIONING FREEZE  
**Target:** IEEE Transactions on Network and Service Management (TNSM)  
**Source scientific authority:** submitted WellPulse evidence; no experimental values changed  

## 1. WP2 decision

The TNSM version must not be positioned primarily as a new IoT resilience "evaluation contract." The paper is stronger when treated as an **experimentally grounded service-recovery assurance study**: it asks when an MQTT telemetry service may legitimately be declared recovered, and what operational evidence is required when connectivity restoration, receiver-confirmed application state, and recovery timing diverge across failure domains.

The scientific evidence remains unchanged. The positioning changes from a framework-first narrative to a **service-management problem + physical experimental evidence + assurance implications** narrative.

## 2. Frozen title

**Beyond Reconnection: Receiver-Verified Service Recovery in MQTT Telemetry Across Failure Domains**

Rejected alternatives:
- titles centered on "evaluation framework/contract" — too close to the novelty weakness identified at the Internet of Things desk decision;
- titles implying durable-MQTT superiority — unsupported by the comparator design;
- titles claiming a universal recovery model — explicitly outside the evidence.

## 3. Frozen primary research question

> **How should recovery of an MQTT telemetry service be declared and measured when path restoration, receiver-confirmed data completeness, and recovery timing can diverge across failure domains?**

Operational subquestions:

**RQ1 — False/partial recovery:** Under controlled broker-disruption conditions, can communication reconnect while the receiver-side application state is still incomplete or irreversibly missing records at the declared endpoint?

**RQ2 — Recovery-state timing:** When durable state survives an outage, how different can path reconnection and complete backlog reconciliation be under the tested workload?

**RQ3 — Cross-domain observability:** How should recovery observations be interpreted when RF, client, core-network, and broker/service failures produce endpoint-dependent measurements with exact, censored, or upper-bound timing semantics?

## 4. Replacement abstract

Operational monitoring of IoT telemetry often treats restored connectivity as service recovery, although records generated during disruption may still be missing or queued. This paper studies when such recovery declarations are justified. We formulate a service-recovery assurance method that aligns the active failure domain, recovery endpoint, receiver-confirmed application state, and timing semantics. Two physical testbeds provide complementary evidence. On FIT IoT-LAB, an intentionally non-durable control reconciled 8,000/10,000 records under broker-outage conditions, whereas an application-buffered durable path reconciled 10,000/10,000 across three run-level replicates per condition. Connectivity returned in about 1.3 s, while complete durable backlog drainage required about 68 s, exposing a prolonged interval in which communication was restored but receiver-confirmed application state was not yet complete. POWDER separately exercised RF, client, core-network, and broker/service failure domains; recovery observations depended on the affected domain and endpoint, and were preserved as exact, censored, or upper-bound where warranted. Receiver-side identity reconciliation also exposed missing and duplicate activity that sender-side status alone could not establish. Within the tested configurations, the results show that path restoration, service availability, and application-state recovery are distinct assurance states. The contribution is an experimentally grounded method for declaring and auditing MQTT telemetry recovery without claiming a new persistence mechanism, generic superiority over durable MQTT configurations, or a universal recovery model.

## 5. Frozen contribution architecture

The introduction should claim exactly these three primary contributions.

### C1 — Receiver-verified service-recovery assurance

A management-oriented recovery definition that requires four aligned elements before a recovery claim is interpreted: **failure domain, declared recovery endpoint, receiver-confirmed application state, and timing semantics**. Connectivity indicators and sender acknowledgments remain useful diagnostic signals but are not treated as final evidence of end-to-end telemetry recovery.

### C2 — Physical evidence of non-equivalent recovery states

Controlled FIT IoT-LAB experiments quantify the difference between communication restoration and receiver-confirmed application recovery. Under the tested broker-outage treatments, the non-durable control reconciles 8,000/10,000 records while the application-buffered durable path reconciles 10,000/10,000 in each of three run-level replicates. For the durable path, reconnection occurs in about 1.3 s while complete backlog drainage requires about 68 s. These are bounded experimental observations, not a generic comparison against durable MQTT mechanisms.

### C3 — Failure-domain-aware recovery observability

POWDER experiments show that recovery timing cannot be treated as one interchangeable KPI across RF, client, core-network, and broker/service failures. Endpoint identity and observation semantics matter; exact, censored, and upper-bound recovery observations must remain distinct rather than being forced into a single latency distribution.

## 6. Replacement introduction opening

**Service recovery is not equivalent to restored connectivity.** In an MQTT telemetry service, a successful ping, TCP reconnection, broker session, or publish can show that communication has resumed while saying little about records generated during the disruption. Those records may have been lost, may remain queued locally, or may still be draining toward the receiver. For operational monitoring and service assurance, these conditions are materially different: the network path can be available while the application state required by the service remains incomplete.

This distinction creates a management problem rather than a protocol-firstness problem. MQTT already provides established session and quality-of-service semantics, and practical clients and platforms provide persistent state, offline buffering, and store-and-forward mechanisms. Fault injection, broker robustness testing, layered recovery, and reliable messaging are also established research areas. The unresolved question addressed here is therefore **when an operator or monitoring system has sufficient evidence to declare an MQTT telemetry service recovered**. A recovery declaration must identify what failed, which endpoint defines restoration, what application state is actually present at the receiver, and what kind of timing observation supports the declaration.

The distinction is operationally important because commonly observed recovery signals can disagree. Communication may return quickly after a broker or network impairment while historical records remain absent or queued; lower-layer reachability can remain healthy during a broker-specific failure; and failure-domain interventions can yield exact recovery times in one case but only censored or upper-bound observations in another. Collapsing these states into a single reconnect latency or reliability percentage can therefore hide the condition that service management is intended to detect.

We investigate this problem using two physical experimental infrastructures with deliberately different evidence roles. FIT IoT-LAB isolates receiver-confirmed record survival and durable catch-up under controlled broker outage and broker-outage-plus-process-restart treatments. POWDER separately characterizes RF, client, core-network, and broker/service degradation and recovery. The two testbeds are not statistically pooled; instead, they provide complementary evidence about application-state recovery and communication-path recovery.

The resulting research question is: **How should recovery of an MQTT telemetry service be declared and measured when path restoration, receiver-confirmed data completeness, and recovery timing can diverge across failure domains?**

The paper makes three contributions. First, it defines a receiver-verified service-recovery assurance method that aligns failure domain, recovery endpoint, application-state evidence, and timing semantics. Second, controlled FIT IoT-LAB experiments quantify cases in which restored connectivity does not establish receiver-confirmed recovery, including the separation between approximately 1.3 s path reconnection and approximately 68 s durable backlog drainage under the tested workload. Third, POWDER experiments show why cross-domain recovery observations must retain their endpoint and timing semantics rather than being collapsed into one recovery-latency measure. The claims are deliberately bounded: the study does not propose a new persistence mechanism, does not claim superiority over strong durable MQTT configurations, and does not infer a universal RF or recovery model.

## 7. Related-work positioning rule

The related-work section must no longer culminate in "the novelty is the compound evaluation contract." It must instead establish the following gap:

> Existing work provides persistence mechanisms, MQTT robustness testing, broker performance/reliability evaluation, disruption recovery, and layered continuity mechanisms. What remains insufficiently operationalized for service management is the **evidence required to declare recovery when network/path state and receiver-confirmed application state disagree, and when recovery observations across failure domains have heterogeneous endpoint and timing semantics.**

The literature table should be retained only if every row directly supports this service-assurance gap. Rows that merely prove broad prior art without affecting the retained claim should be shortened or moved to supplementary material.

## 8. Results narrative rewrite rules

The numerical results do not change. Their narrative hierarchy does.

### Headline 1
**Restored communication can coexist with incomplete receiver state.**

Use the B0 result only as a mechanism-isolation negative control: 8,000/10,000 at the declared receiver endpoint under C1/C2 versus 10,000/10,000 for W1. Do not frame this as an architectural competition or as "WellPulse beats MQTT."

### Headline 2
**Durability does not make recovery instantaneous.**

The strongest TNSM result is the separation between path reconnection (~1.3 s) and complete durable backlog drainage (~67.7–67.9 s). The management interpretation is that a connectivity alarm can clear while the application-level historical state remains incomplete.

### Headline 3
**Recovery latency has domain and endpoint semantics.**

POWDER results should be organized around observability and management interpretation: RF/link, client, core-network, and broker/service states can disagree, and exact/censored/upper-bound observations must not be statistically merged into a single recovery-latency quantity.

## 9. Service-management implication paragraph to add in Discussion

For service management, the experiments imply that a binary up/down indicator is insufficient for stateful telemetry. A practical recovery monitor should maintain at least separate indicators for communication-path availability, the active or recently affected failure domain, receiver-confirmed record completeness/backlog state, and the observation semantics of the recovery timer. A first successful probe or publish may close a connectivity incident, but it should not automatically close an application-data recovery incident. Conversely, persistent records may remain safe while the communication service is still unavailable. The required declaration therefore depends on the service objective: reachability, current-message availability, historical completeness, or complete backlog reconciliation.

## 10. Comparator-defense paragraph

The FIT comparison is intentionally asymmetric and should not be presented as a contest between alternative durable MQTT implementations. B0 is a non-durable mechanism-isolation control used to expose the consequence of declaring recovery from connectivity while application records generated during an outage are not preserved. W1 demonstrates the distinct case in which records survive but complete application-state recovery extends well beyond path reconnection. A matched file-persistent MQTT client or durable broker/session configuration could reduce or eliminate the completeness contrast; evaluating superiority among durable mechanisms is outside the present claim. This limitation does not invalidate the service-assurance result because the central question is whether the evidence used to declare recovery identifies the state that actually matters to the service.

## 11. Replacement conclusion

This study examined MQTT telemetry recovery as a service-assurance problem rather than a reconnect event. Across two physical testbeds, the evidence shows that communication-path restoration, receiver-confirmed application state, and complete recovery should not be treated as interchangeable observations. On FIT IoT-LAB, the intentionally non-durable control reconciled 8,000/10,000 records under the tested broker-outage conditions, whereas the application-buffered durable path reconciled 10,000/10,000 in every run-level replicate. For the durable path, communication returned in about 1.3 s but complete backlog reconciliation required about 68 s, leaving a substantial interval in which the path was available while historical application state was still incomplete. POWDER further showed that recovery observations depend on the affected failure domain and endpoint and may legitimately be exact, censored, or only upper-bounded.

The resulting management implication is concrete: an MQTT telemetry service should not be declared recovered from connectivity evidence alone when its service objective includes data completeness. Recovery assurance should state the relevant failure domain, the endpoint used to declare restoration, the receiver-confirmed application state, and the semantics of the measured recovery time. The study does not establish superiority over durable MQTT configurations or a universal recovery model; instead, it provides physical experimental evidence for separating connectivity recovery from application-state recovery and for making that distinction auditable in network and service management.

## 12. Section-level surgical map

Recommended TNSM narrative structure without changing the experimental program:

1. **Introduction** — service-recovery problem; RQ; contributions.
2. **Related Work and Novelty Boundary** — persistence, robustness/fault injection, broker/service reliability, layered recovery; retained service-assurance gap.
3. **Service-Recovery Assurance Model and Experimental Methodology** — existing quantities and failure-domain/timing semantics; FIT and POWDER roles.
4. **Experimental Results** — preserve empirical results; reorder interpretation around recovery states.
5. **Service-Management Implications and Threats to Validity** — operator/monitoring implications; comparator defense; transfer limits.
6. **Reproducibility** — preserve existing evidence package and provenance.
7. **Conclusion** — service-assurance result, not framework-first novelty.

## 13. Immutable scientific prohibitions carried forward

Do not claim:
- superiority over the strongest durable MQTT configuration;
- generic "WellPulse beats MQTT";
- population reliability from three FIT run-level replicates or from message counts;
- a universal 52 dB threshold or universal RF transition;
- deterministic RF-only recovery;
- exact recovery where only a censored or upper-bound observation exists;
- pooled FIT+POWDER inference;
- historical firstness for persistence, store-and-forward, receiver confirmation, layered recovery, or physical-testbed use;
- field/agronomic/industrial-process validation.

## 14. WP2 acceptance test

WP2 passes only if the manuscript can be summarized truthfully in one sentence as:

> **A physical two-testbed study of how MQTT telemetry service recovery should be declared when connectivity restoration and receiver-confirmed application-state recovery are non-equivalent.**

No new experiment is required for this positioning. Experimental truth, figure data, and bounded limitations remain unchanged.
