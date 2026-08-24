# Decision Register

## D-001 — Validation order
FIT IoT-LAB is the first completed remote-testbed layer. POWDER is the next controlled real-RF layer; compact indoor OTA follows only after the conducted-RF gate. Outdoor/rural validation remains a later distinct layer rather than an automatic extension.

## D-002 — Smallest publishable experiment
Keep the paper focused on durable telemetry resilience. Do not expand into GPU, massive MIMO, O-RAN/RIC, mobility, multi-rate sweeps, or unrelated networking features merely because POWDER exposes them.

## D-003 — Baseline evolution
The publish-only/non-durable baseline remains valid historical evidence for FIT WP-RT01 and as a lower-bound sanity reference. For POWDER and the Q1-oriented manuscript, the **primary comparator is upgraded to a stronger standard MQTT QoS 1 + automatic reconnect baseline with volatile client state and no application-level disk durability/reconciliation**. This avoids a strawman comparison and separates network-only resilience from restart durability.

## D-004 — No evidence inflation
Remote networking evidence is not pump, hydraulic, groundwater, agronomic, Siwa field, or rural-generalization evidence.

## D-005 — No unnecessary BYOD initially
Use existing testbed compute/radio resources first. Custom hardware shipping is deferred unless it becomes necessary for a material claim.

## D-006 — Publication novelty position
Do not claim novelty for generic MQTT, buffering, store-and-forward, offline-first operation, or 5G. The publication contribution is the combination of lightweight durable record semantics, idempotent reconciliation, a strong matched MQTT baseline, a cross-layer FIT -> controlled real-RF -> OTA validation ladder, and publication-grade reproducibility.

## D-007 — Primary venue-fit target
Design the manuscript first for **Internet of Things (Elsevier)**, with **Computer Networks** and **Computer Communications** as backups depending on final network-measurement emphasis. Re-verify current Q1/indexing/APC/author guidance immediately before submission; do not freeze a static quartile claim months in advance.

## D-008 — Statistical unit and anti-pseudoreplication
The run is the statistical unit. Telemetry messages within a run are repeated observations, not thousands of independent replicates. Use paired run-level comparisons and effect-size-first reporting.

## D-009 — Precision-based replication
POWDER impairment scenarios start at three paired B1/W1 blocks and may extend to five pairs only under the frozen precision rule. Stopping may not depend on p-values, effect direction, or whether the result favors WellPulse.
