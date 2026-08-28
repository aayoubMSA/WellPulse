# WP2-P8 — Modular Manual RF Experiment Campaign

Date: 2026-08-28  
Repository: `aayoubMSA/WellPulse`  
Branch: `main`  
Platform: POWDER / srsLTE controlled RF  
Status: **PLANNED / NON-SCORED / MANUAL-REFERENCE CAMPAIGN**

## 1. Purpose

Exploit a known-working two-node POWDER LTE/MQTT experiment to obtain the maximum scientifically useful, publication-relevant evidence without mixing this exploratory/manual campaign with the frozen scored P7B contract.

This work package is a **manual reference campaign**. It exists to characterize the controlled RF failure/recovery surface, isolate recovery mechanisms, quantify repeatability, and create a validated reference implementation for any later automation.

It does **not** convert the historical P7B state into a scored PASS and does not authorize scored execution.

## 2. Permanent two-node rule

Every experiment in this campaign MUST expose both node roles explicitly:

- `nuc1 / CORE`: EPC, eNB, MQTT broker, receiver, CORE-side observation and raw evidence.
- `nuc2 / UE`: srsUE, publisher, RF attenuation control, UE-side observation and raw evidence.

A one-node experiment script is not acceptable unless an independent equivalence test has first proven that it correctly executes, observes, timestamps, and preserves both node roles.

Manual two-node execution is the reference implementation.

## 3. Common experimental skeleton

Every experiment MUST use the same structure:

1. assign one shared `RUN_ID`;
2. CORE readiness;
3. UE readiness;
4. bidirectional LTE ping gate;
5. MQTT end-to-end probe;
6. start CORE receiver;
7. start UE publisher;
8. establish stable baseline;
9. timestamp treatment;
10. apply only the declared treatment;
11. observe impairment;
12. timestamp recovery action;
13. observe LTE recovery;
14. observe MQTT/application recovery;
15. stop publisher and receiver;
16. freeze CORE raw evidence;
17. freeze UE raw evidence;
18. hash each node independently;
19. off-platform export;
20. independent sequence/timeline reconciliation.

Any failed prerequisite blocks the experiment before treatment.

## 4. Common measurements

At minimum derive from raw evidence:

- attenuation level and direction;
- packet loss;
- RTT distribution;
- first impairment timestamp;
- last pre-fault received sequence;
- first post-recovery received sequence;
- missing sequence IDs;
- duplicate sequence IDs;
- delayed/buffered records;
- LTE recovery time;
- application/MQTT recovery time;
- recovery backlog behavior;
- post-recovery continuity;
- run-to-run variation;
- treatment-specific service/process state.

## 5. Experiment matrix

### P8-E1 — Fine RF Threshold Sweep

**Question:** At what attenuation does degradation begin, and at what attenuation does the LTE/MQTT path fail?

**Treatment sequence:**

`0 -> 20 -> 30 -> 35 -> 40 -> 45 -> 48 -> 50 -> 52 -> 54 -> 55 -> 56 -> 58 -> 60 -> 0 dB`

**CORE / nuc1 responsibilities:**
- keep broker and receiver live;
- timestamp every received application record;
- collect process/socket/network state;
- preserve receiver and LTE-side logs.

**UE / nuc2 responsibilities:**
- set all attenuators `[1,33,2,34]` to each declared level;
- collect ping samples per level;
- publish sequenced MQTT observations per level;
- preserve attenuation events and UE logs.

**Primary outputs:** failure threshold, degradation curve, RTT/loss versus attenuation, MQTT delivery versus attenuation.

---

### P8-E2 — RF Hysteresis Sweep

**Question:** Is the recovery attenuation the same as the failure attenuation?

**Treatment:** sweep upward from 0 dB until failure, then sweep downward until stable recovery.

**Primary outputs:** failure threshold, recovery threshold, hysteresis width, application recovery behavior.

---

### P8-E3 — Near-Threshold Repeatability

**Question:** Is the transition deterministic or stochastic near the RF boundary?

**Treatment set:** `50, 52, 54, 55, 56 dB`.

**Replication:** minimum 3 independent repetitions per level if reservation time permits.

**Primary outputs:** probability of LTE/MQTT survival by attenuation, RTT/loss variability, threshold repeatability.

---

### P8-E4 — RF-Only Recovery

**Question:** After an RF-induced outage, does restoring attenuation to 0 dB recover the system without restarting any LTE/application service?

**Treatment:** healthy baseline -> RF outage -> restore RF to 0 dB -> no process restart.

**Primary outputs:** spontaneous LTE recovery time, spontaneous MQTT recovery time, missing/delayed records.

**Scientific value:** separates radio restoration from explicit software recovery.

---

### P8-E5 — UE-Restart Recovery

**Question:** What additional recovery benefit is obtained by restarting only `srsue` after RF restoration?

**Treatment:** healthy baseline -> RF outage -> restore RF -> restart `srsue` only.

**Primary outputs:** UE reattachment time, LTE recovery time, application recovery time, sequence loss/backlog.

---

### P8-E6 — CORE-Restart Recovery

**Question:** How does restarting EPC/eNB affect recovery under or after controlled RF impairment?

**Treatment:** healthy baseline -> RF impairment -> restart `srsepc` + `srsenb` on CORE -> restore RF according to declared ordering.

**Primary outputs:** CORE service restoration time, UE reattachment behavior, MQTT recovery, sequence-level loss/delay.

---

### P8-E7 — Combined Recovery Stress Case

**Question:** What is the system behavior under a combined controlled RF + CORE restart + UE reattachment scenario?

**Treatment:** RF impairment + CORE restart + RF restore + UE reattachment if required.

**Primary outputs:** worst-case controlled recovery time, data continuity, missing/duplicate/delayed records, recovery ordering.

**Boundary:** this experiment must use one predeclared ordering only; do not change ordering mid-run.

---

### P8-E8 — Broker-Only Fault Control

**Question:** Can application-layer MQTT failure be separated from radio/LTE failure?

**Treatment:** keep LTE/RF healthy; induce only a broker-side interruption/restart; restore broker.

**Primary outputs:** MQTT outage/recovery time while LTE ping remains healthy, sequence loss/backlog.

**Scientific value:** negative/control comparison for RF-specific claims.

---

### P8-E9 — No-Fault Duration-Matched Control

**Question:** What loss, latency, jitter, and continuity occur over the same duration with no treatment?

**Treatment:** no RF mutation and no service mutation.

**Primary outputs:** baseline RTT, MQTT latency, sequence completeness, natural variability.

**Scientific value:** establishes the reference distribution required to interpret treatment effects.

## 6. Execution priority

Highest-ROI order:

1. `P8-E1` Fine RF Threshold Sweep
2. `P8-E2` RF Hysteresis Sweep
3. `P8-E3` Near-Threshold Repeatability
4. `P8-E4` RF-Only Recovery
5. `P8-E5` UE-Restart Recovery
6. `P8-E6` CORE-Restart Recovery
7. `P8-E8` Broker-Only Fault Control
8. `P8-E9` No-Fault Duration-Matched Control
9. `P8-E7` Combined Recovery Stress Case

If reservation time becomes constrained, stop after E5 and preserve/export all evidence rather than starting another incomplete experiment.

## 7. Evidence contract per experiment

Each experiment MUST generate independent node-local evidence before any combined archive.

### CORE / nuc1

Required minimum:
- `received.log`;
- EPC log;
- eNB log;
- broker log/state where available;
- process snapshot;
- socket snapshot;
- `ip addr`;
- `ip route`;
- relevant event timestamps;
- `SHA256_CORE.txt`.

### UE / nuc2

Required minimum:
- `sent.log`;
- `events.log`;
- publisher log;
- UE log;
- attenuation commands/events;
- ping logs;
- process snapshot;
- `ip addr`;
- `ip route`;
- `SHA256_UE.txt`.

### Off-platform

Required before reservation release:
- CORE archive;
- UE archive;
- independent local SHA256 verification;
- shared run manifest;
- reconciliation output.

## 8. Scientific acceptance rules

An experiment is **ACCEPTED FOR EXPLORATORY ANALYSIS** only if:

- both node roles were active and independently evidenced;
- pre-treatment LTE and MQTT gates passed;
- treatment is timestamped and exactly matches the declared experiment;
- recovery action is timestamped;
- raw evidence exists on both nodes;
- hashes were produced;
- sender/receiver sequences can be independently reconciled.

An experiment is **NULL / ABORTED** if scientific treatment began but evidence integrity or declared treatment semantics were violated.

A pre-treatment infrastructure failure is **BLOCKED / PRE-SCIENCE**, not a scientific failure.

## 9. Automation doctrine

Do not build a new monolithic B1-style runner from this campaign.

Any later automation MUST be composed from role-specific modules and prove equivalence to the manual reference:

`manual reference -> modularization -> module QA -> orchestration -> equivalence QA -> live use`

Recommended module families:

- identity/run manifest;
- CORE init/readiness;
- UE init/readiness;
- bidirectional LTE gate;
- MQTT gate;
- CORE receiver;
- UE publisher;
- RF treatment;
- CORE restart;
- UE restart;
- recovery gate;
- CORE evidence freeze;
- UE evidence freeze;
- off-platform pull;
- hash verification;
- reconciliation.

## 10. Publication role

This campaign is intended to support publication later by providing distinct controlled evidence for:

- RF degradation/failure boundary;
- RF hysteresis;
- threshold repeatability;
- spontaneous radio recovery;
- UE-assisted recovery;
- CORE-assisted recovery;
- combined recovery stress;
- radio-versus-application fault separation;
- no-fault reference behavior.

Claims must remain bounded to the physical/network/application layers actually exercised on POWDER. This campaign does not validate Siwa hydraulics, pump physics, agronomic effects, or site-specific field behavior.

## 11. Status

`WP2_P8_STATUS=PLANNED_NON_SCORED_MANUAL_REFERENCE`

`SCORED_P7B_STATUS=UNCHANGED`

`LIVE_EXECUTION_AUTHORITY=NOT_GRANTED_BY_THIS_DOCUMENT`
