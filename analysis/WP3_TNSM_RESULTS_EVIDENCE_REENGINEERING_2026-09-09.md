# WP3 — IEEE TNSM Results & Evidence Re-engineering

**Date:** 2026-09-09  
**Target:** IEEE Transactions on Network and Service Management (TNSM)  
**Status:** PASS / RESULTS NARRATIVE FROZEN  
**Scientific authority:** P11 raw-data reconstruction + P12 cross-evidence integration + P13 claim–evidence matrix + current R14/RF9H figures/captions. No experimental value is changed.

## 1. WP3 decision

The TNSM paper must be data-first rather than framework-first. The strongest evidence is the direct separation between connectivity restoration and receiver-confirmed application recovery. The current manuscript already contains all required measurements; the revision changes only the narrative hierarchy, section ordering, figure emphasis, and service-management interpretation.

The primary TNSM empirical sequence is:

1. **Restored communication can coexist with incomplete receiver state.**
2. **Durable record survival does not imply immediate complete service recovery.**
3. **Cross-layer health indicators can disagree under controlled degradation.**
4. **Recovery timing is meaningful only with explicit failure-domain, action, endpoint, and censoring semantics.**

## 2. Evidence integrity gate

P11 independently reconstructed all 18 FIT cells from generated and receiver-side record identities. No unsupported surviving values or unresolved evidence discrepancies remain. P13 maps every manuscript-eligible claim to traceable evidence, and P14 maps quantitative displays only to P13-PASS claims.

TNSM rewrite therefore operates under these hard rules:

- no new experimental values;
- no message-level pseudo-replication;
- no pooled FIT+POWDER statistic;
- no confidence intervals manufactured from the three deterministic FIT replicates;
- no universal RF threshold;
- no durable-MQTT superiority claim;
- exact/censored/upper-bound observations remain separate.

## 3. Revised empirical claim hierarchy

The earlier manuscript hierarchy gave substantial prominence to the evaluation framework. For TNSM the hierarchy becomes:

### Primary A-level empirical claims

**TNSM-P1 — Receiver-state divergence under outage.**  
Under FIT C1 and C2, B0 reconciled 8,000/10,000 records in every run while W1 reconciled 10,000/10,000 in every run. Under C0 both reconciled 10,000/10,000. B0 is a non-durable mechanism-isolation control, not a durable MQTT competitor.

**TNSM-P2 — Reconnect and complete application-state recovery are different timescales.**  
For W1, mean reconnect time was 1.317088 s in C1 and 1.344870 s in C2. Mean post-reconnect backlog-drain time was 67.731246 s in C1 and 67.870252 s in C2. These measurements demonstrate an extended interval in which communication is available while historical receiver state is still incomplete.

### Primary B-level characterization claim

**TNSM-P3 — Recovery observations depend on failure domain and endpoint.**  
POWDER E10-A is censored with no scalar recovery latency; E10-B provides exact endpoint-defined restart-assisted observations; E10-C-B provides exact core-related recovery observations; E10-D remains an upper bound only. They must not be collapsed into one recovery-latency distribution.

### Supporting B-level claims

**TNSM-S1 — Cross-layer status can disagree.**  
At E1R4 51 dB, ICMP loss was 30% while MQTT remained 20/20. In E8, broker interruption removed MQTT records while the LTE ping path remained healthy.

**TNSM-S2 — RF degradation is a profile-specific region, not a deterministic threshold.**  
POWDER E1R4/E2/E3 shows healthy 48–49 dB samples, variable degradation around 50–51 dB, and severe but variable impairment at 52 dB in the tested profile.

### Methodological synthesis

Receiver-side identity reconciliation and explicit recovery semantics are retained as the mechanism that makes the empirical service-assurance result auditable. They support the paper; they are not presented as an independent effect or a universal theory.

## 4. Results section rewrite map

Recommended Results structure:

### 4.1 Receiver-confirmed service state under broker disruption

Lead with C0/C1/C2 FIT completeness. State the 8,000/10,000 versus 10,000/10,000 result immediately. Explain that the missing 2,000 B0 records correspond to the imposed outage interval at the declared receiver endpoint. Reiterate that the run, not each message, is the scientific unit.

**Interpretation:** a restored communication path cannot retroactively establish that outage-period application records survived.

### 4.2 Connectivity recovery versus complete durable catch-up

Report run-level reconnect and W1 backlog-drain measurements together because their separation is the core TNSM service-recovery result.

C1:
- B0 reconnect mean 1.325412 s;
- W1 reconnect mean 1.317088 s;
- W1 backlog drain mean 67.731246 s.

C2:
- B0 reconnect mean 1.362121 s;
- W1 reconnect mean 1.344870 s;
- W1 backlog drain mean 67.870252 s.

Do not emphasize small B0/W1 reconnect differences; they are descriptive only. The main result is that W1 can preserve all records while complete historical-state reconciliation continues long after connectivity returns.

### 4.3 Cross-layer disagreement during controlled POWDER degradation

Use E1R4/E2/E3 to show that path-health indicators and MQTT delivery do not move synchronously. The 51 dB examples are especially useful because lower-layer degradation is visible while MQTT delivery remains nearly/fully complete. Preserve direction and cycle variability. No universal threshold language.

### 4.4 Failure-domain-specific recovery observations

Organize around domain/action/endpoint/semantics rather than around experiment IDs alone:

- RF-only restoration: censored example retained;
- RF restore + UE restart: exact action-begin→first-publish and first-ping observations;
- core-related recovery sequence: exact endpoint-defined observations;
- broker restart: upper-bound only;
- broker-only interruption: MQTT can fail while LTE remains healthy.

### 4.5 Cross-testbed service-assurance synthesis

Do not pool values. State only the shared operational conclusion: FIT shows the distinction between durable record survival and complete catch-up; POWDER shows that the communication substrate and service components expose different recovery states. Together they demonstrate why a single binary up/down or reconnect metric is insufficient for stateful telemetry service assurance.

## 5. Figure strategy for TNSM

### Main recommendation: data first

The current R14/RF9H **Figure 2** is the strongest TNSM figure because it already combines:
- receiver-reconciled completeness;
- reconnect times;
- W1 backlog-drain times.

For the TNSM version it should become the **first principal empirical figure** and its caption should use service-recovery language rather than architecture-comparison language.

### Current Figure 1 — methodology schematic

The current failure-domain/evidence-lifecycle schematic is scientifically valid but should no longer be the visual front door of the paper. Preferred treatment:

- move it later in the methodology section if page budget permits; or
- move it to supplementary/reproducibility material if the IEEE page budget is tight.

Do not delete its scientific role before WP5 page engineering, but do not let it lead the novelty story.

### Current Figure 3 — POWDER cross-layer transition

Retain in the main paper. Its TNSM role is not to establish an RF threshold; it demonstrates that network-layer and application-layer health indicators can disagree and that degradation/recovery is profile-specific.

### Current Figure 4 — failure-domain and timing semantics

Retain in the main paper because it directly supports the management argument that recovery timers cannot be interpreted without endpoint and censoring semantics.

### Figure-data policy

No new scientific figure is required in WP3. Existing verified vector assets can be reused/reordered. Any later visual modification must be regenerated from canonical data/code and pass the existing figure QA doctrine; no AI-generated scientific graphics.

## 6. Table strategy

### Keep / promote

**POWDER recovery timing semantics table** should remain in the main manuscript. It protects the strongest domain/endpoint claim:
- E10-A: censored;
- E10-B: exact 6.063318 s to first publish and 6.609430 s to first ping;
- E10-C-B: exact ~29.248 s endpoint observations;
- E10-D: ≤10.908749 s upper bound.

### Compress

The broad prior-capability/claim-boundary table from the IoT version should be compressed or moved to supplementary material. In TNSM, main-paper table space is more valuable for empirical/service-management evidence than for a large framework novelty matrix.

### Optional derived main-text table

If page budget permits, create a compact **Recovery Evidence State Table** using only already-supported observations. Columns: failure/treatment, path/service indicator, receiver-state evidence, recovery endpoint, timing semantics, operational declaration. This is a presentation synthesis only; it must not introduce new measurements or causal claims.

## 7. Discussion rewrite hierarchy

The Discussion must open from observations, not from framework vocabulary.

### D1 — Why reconnect is an unsafe recovery declaration

Use FIT as the central proof: B0 can reconnect while outage-period receiver state remains incomplete; W1 can reconnect while backlog reconciliation is still ongoing.

### D2 — Service objectives determine the required endpoint

Separate at least:
- reachability restoration;
- current-message availability;
- historical-record completeness;
- complete backlog reconciliation.

A monitor may legitimately close one objective while another remains open.

### D3 — Failure-domain identity changes interpretation

Use POWDER E8 and E10 cases to show that broker/service failure, RF impairment, client restart, and core-related recovery are not interchangeable events.

### D4 — Comparator limitation

Keep the limitation explicit: B0 is intentionally non-durable. A strong persistent MQTT client or durable broker/session configuration could reduce/eliminate the completeness difference. Therefore the paper does not establish mechanism superiority. The result that survives this limitation is the service-assurance distinction between connectivity evidence and receiver-confirmed application-state evidence.

### D5 — External validity

Preserve limits on hardware, workload, generation rate, outage duration, queue capacity, broker/client implementation, RF profile, and testbed-specific conditions. No field/agronomic claim.

## 8. Caption rewrite targets

### TNSM empirical figure caption target

**Receiver-confirmed service recovery on FIT IoT-LAB.** Panel A reports unique receiver-reconciled records under healthy operation, broker outage, and broker outage plus gateway-process restart. Under C1/C2, the non-durable control ends at 8,000/10,000 records in every run, whereas the application-buffered durable path reconciles 10,000/10,000. Panels B–C report run-level path reconnection and W1 backlog drainage. Connectivity returns in approximately 1.3 s, while complete durable backlog reconciliation requires approximately 68 s under the tested workload. The comparison is bounded to the tested non-durable control and durable application-buffered path and does not establish superiority over durable MQTT configurations generally.

### POWDER cross-layer caption target

Emphasize disagreement between health indicators, direction/cycle variability, receiver-observed MQTT completeness, and profile-specific—not universal—attenuation behavior.

### Failure-domain caption target

Emphasize that each timing value is meaningful only with its intervention, endpoint and exact/censored/upper-bound semantics; no pooled recovery statistic.

## 9. Numerical audit

FIT values verified directly against the reconstructed run CSV:

- C1 B0: 8,000/10,000 in R1/R2/R3;
- C1 W1: 10,000/10,000 in R1/R2/R3;
- C2 B0: 8,000/10,000 in R1/R2/R3;
- C2 W1: 10,000/10,000 in R1/R2/R3;
- W1 C1 reconnect: 1.309382, 1.331298, 1.310584 s;
- W1 C1 drain: 67.596918, 68.047688, 67.549132 s;
- W1 C2 reconnect: 1.377100, 1.329536, 1.327973 s;
- W1 C2 drain: 67.320791, 68.851579, 67.438386 s.

POWDER values verified against the derived metrics and timing tables, including E1R4 51 dB ICMP 30% loss with MQTT 20/20, E3 variability, E10 censoring/exact/upper-bound classes, and E8 broker/path separation as preserved by P11/P13.

`WP3_UNSUPPORTED_VALUES=0`

## 10. Acceptance gate

- raw-to-claim traceability rechecked: PASS;
- FIT principal values rechecked from reconstructed runs: PASS;
- POWDER transition values rechecked from derived metrics: PASS;
- POWDER recovery semantics rechecked from frozen timing table: PASS;
- TNSM empirical hierarchy frozen: PASS;
- figures mapped to service-management claims: PASS;
- framework-first visual emphasis removed: PASS;
- new experiment required: NO;
- unsupported scientific claim introduced: NO;
- canonical raw/scientific evidence modified: NO.

**WP3 = PASS — RESULTS & EVIDENCE RE-ENGINEERING FROZEN**

**NEXT = WP4 — Related Work + Reviewer Attack-Surface Closure**
