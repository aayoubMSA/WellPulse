# WP-PWD01 — Consortium P1 Pre-Score Amendment

**Date:** 2026-08-26  
**Authority:** approved independent pre-WP3 consortium review + local B2 semantics PASS  
**Status:** FROZEN PRE-SCORE AMENDMENT  
**Scored runs authorized:** **NO**

This amendment is read with `protocol.md` v0.4, the P0 amendment, the analysis plan, evidence schema, run matrix, randomization plan, `B2_SEMANTICS_GATE_v1.md`, and the consortium review.

It does not reopen RF calibration, change Q0-Q3, change the H formula, or authorize WP3.

## P1-1 — Scientific question is failure-domain bounded

The study no longer assumes that application-level durability improves every network outage.

Frozen scenario interpretation:

- `S0_HEALTHY`: healthy-path integrity equivalence and overhead sanity;
- `S1_INTERMITTENT`: network-only intermittent-link integrity plus descriptive recovery/overhead characterization;
- `S2_HARD_OUTAGE`: network-only hard-outage integrity plus descriptive recovery/overhead characterization while volatile client-process state survives;
- `S3_OUTAGE_RESTART`: primary durability/integrity stress test when gateway/client volatile state is destroyed.

Frozen RQ wording for the POWDER campaign:

- **RQ1 — Network-only integrity:** Under controlled real-RF intermittency and hard outage, do matched B1 and W1 differ in unique telemetry completeness/integrity at the common horizon H, and what recovery/overhead trade-offs are observed?
- **RQ2 — Process-state durability:** When the gateway/client process restarts during a real RF outage, what additional record-level integrity/reconciliation value does W1 provide relative to volatile B1, and does that distinction remain meaningful against qualified durable standard-client B2?
- **RQ3 — Cross-testbed consistency:** Are the bounded findings directionally consistent across the existing FIT evidence, POWDER conducted RF and compact POWDER OTA replication, without pooling them as one statistical population or claiming agricultural/field validation?

The manuscript must not describe S1/S2 recovery-time differences as a confirmatory primary claim unless a later pre-score amendment explicitly changes the estimand and replication rule.

## P1-2 — Keep completeness primary; recovery remains predeclared secondary engineering characterization

The consortium's minimal defensible route is adopted to avoid adding an underpowered second confirmatory stopping target.

Primary inferential endpoint remains:

`unique_primary_cohort_telemetry_completeness_at_H`

The existing precision-stopping rule remains driven only by the paired run-level completeness difference for S1/S2/S3.

Recovery endpoints remain mandatory and predeclared secondary engineering metrics, including:

- reconnect time;
- first successful post-recovery delivery;
- sink/backlog drain time where defined;
- reconciliation completion time;
- latency distribution;
- queue/resource overhead.

They are reported with run-level distributions/effect estimates but are not used to claim a separately powered confirmatory recovery advantage.

## P1-3 — H anti-bias interpretation

H is an **operational common observation horizon**, not a treatment-optimized outcome threshold.

Frozen safeguards:

1. H is calculated once before any scored B1/W1/B2 result exists.
2. The same H is used for all scored architectures and scenarios.
3. H is never recomputed by architecture, scenario, observed effect direction or favorable result.
4. Uncensored recovery-time evidence is reported separately from completeness at H.
5. With exactly three successful calibration trials, the empirical nearest-rank p95 is described precisely as the **maximum of the three observed W1 calibration drain times**, not as a stable population 95th-percentile estimate.

No additional B1 H-calibration campaign is added.

## P1-4 — B2 qualified and frozen as compact sensitivity comparator

Canonical local semantics evidence:

`evidence/local/wp2-b2-semantics-latest.md`

Gate result: **PASS, 3/3 independent trials**.

Exact B2 client semantics:

- Eclipse Paho Java `1.2.5`;
- MQTT v3.1.1;
- QoS1;
- `cleanSession=false`;
- `MqttDefaultFilePersistence`;
- disconnected buffering enabled;
- buffer size 4096;
- `persistBuffer=true`;
- delete-oldest disabled;
- stable run-specific client identity across the intentional intra-run process restart.

B2 remains a **sensitivity comparator**, not the primary arm, because Java/runtime/client implementation differs from the matched Python B1/W1 transport.

Frozen smallest B2 scientific scope:

- `S2_HARD_OUTAGE`: exactly **3 B2 scored runs**;
- `S3_OUTAGE_RESTART`: exactly **3 B2 scored runs**;
- no B2 in S0 or S1;
- no adaptive B2 replication;
- reuse the corresponding first three mandatory W1 blocks for sensitivity comparison; do not create additional W1 runs merely for B2;
- execute one B2 run adjacent to each mandatory B1/W1 block according to `b2-sensitivity-plan.csv` to limit temporal drift;
- B2-vs-W1 results are labeled sensitivity/non-primary and are not pooled into the primary B1/W1 inference.

Before any B2 scored run, the remote B2 implementation must pass a non-scored runtime/path/restart-domain gate on the same POWDER data path, TLS/payload schema and evidence contract.

## P1-5 — Strong inter-run washout/readiness gate

Every scored run must begin only after all of the following PASS:

1. Q0 end-to-end LTE user-plane health passes over the frozen readiness window;
2. route to the MQTT destination is proven through the experimental LTE tunnel;
3. run-unique MQTT clients/topic namespace are fresh and isolated;
4. architecture-appropriate application state is empty/fresh, with no prior-run durable or volatile residue;
5. no unresolved prior-run broker/session residue exists;
6. baseline Q0 radio metrics are within the accepted calibrated envelope;
7. runtime/version/configuration matches the frozen arm;
8. clock/evidence capture is healthy before impairment begins.

Failure of washout/readiness is technical invalidity, preserved and replaceable under the predefined invalid-run rules; it is never a basis to replace an unfavorable valid scientific outcome.

### S0 order correction

Because no scored data exist yet, the all-B1-first S0 sequence is amended before scoring to reduce avoidable order confounding. Pair 2 is counterbalanced to W1-first. All S1-S3 B1/W1 orders remain unchanged.

This documented pre-score change supersedes the earlier no-randomization-change statement only for S0 pair 2.

## P1-6 — Cross-testbed wording

Replace broad `transportability` wording with:

- `cross-testbed consistency`, or
- `cross-testbed triangulation`.

FIT, conducted POWDER and OTA evidence remain separate layers. They are not pooled as one population. `external replication` is reserved for the compact POWDER OTA B1/W1 replication layer.

## P1-7 — Immutable pre-score reproducibility snapshot

Immediately before `scored_runs_authorized=true`, create an immutable pre-score snapshot containing at minimum:

- protocol and all pre-score amendments;
- analysis-plan version;
- run-matrix version/hash;
- B1/W1 randomization hash;
- B2 sensitivity-plan hash;
- implementation commit;
- environment/runtime locks for B1, W1 and B2;
- evidence schema;
- frozen H and its calibration evidence manifest;
- comparator decision;
- explicit scored authorization decision.

A Git tag/release or immutable manifest anchored to a commit is acceptable. No scored result may precede this snapshot.

## Claim boundary

The confirmatory workload remains **1 record/s low-rate telemetry**. No multi-rate scored sweep is added. CPU, memory, network and queue headroom remain mandatory contextual measurements so the paper can show that the observed behavior is not accidental host/broker saturation.

## State after this amendment

```text
RF calibration = PASS / FROZEN
B2 local semantics = PASS / QUALIFIED
B2 remote implementation = OPEN
H physical calibration = OPEN
scored_runs_authorized = false
WP3 = BLOCKED
scientific weighted completion = 20%
```
