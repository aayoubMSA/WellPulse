# WellPulse — Independent Pre-WP3 Consortium Review

**Date:** 2026-08-26  
**Review stage:** PRE-SCORE / PRE-WP3  
**Decision status:** RECOMMENDATIONS ONLY — no frozen protocol, RF state, H rule, randomization, or scored-run authorization is changed by this document.  
**Scientific completion:** remains **20%**.  
**Scored runs:** remain **NOT AUTHORIZED**.

## 1. Consortium mandate

This review stress-tests the complete WellPulse validation programme before the confirmatory POWDER campaign. The objective is not to redesign the project from scratch or add experiments for appearance. The objective is to identify hidden methodological, implementation, comparator, measurement, reproducibility, and publication risks while changes are still cheap.

The review is conducted from seven professional perspectives:

1. controlled-RF / wireless experimentation;
2. IoT and MQTT systems;
3. distributed systems and reliability;
4. experimental design and statistics;
5. systems measurement and testbed validity;
6. reproducibility / open-science artifact review;
7. adversarial scientific red-team / reviewer attack.

Allowed verdicts are `KEEP`, `AMEND`, `MERGE`, `KILL`, and `ADD GATE`.

## 2. Evidence reviewed

Canonical project evidence reviewed includes:

- `HANDOVER_CURRENT.md`;
- `docs/MILESTONE_STATUS.md`;
- `docs/STATUS.md`;
- `docs/DECISIONS.md`;
- `docs/WP0_NOVELTY_VENUE_LOCK_2026-08-24.md`;
- `docs/WP0_RELATED_WORK_BENCHMARK_2026-08-25.md`;
- `docs/WP0_COMPARATOR_AUDIT_2026-08-25.md`;
- `experiments/WP-PWD01/protocol.md`;
- `experiments/WP-PWD01/analysis-plan.md`;
- `experiments/WP-PWD01/evidence-schema.md`;
- `experiments/WP-PWD01/randomization-plan.csv`;
- `experiments/WP-PWD01/run-matrix.yaml`;
- `experiments/WP-PWD01/RF_CALIBRATION_FREEZE_v1.md`;
- `experiments/WP-PWD01/H_CALIBRATION_PLAN_v1.md`;
- `src/wellpulse/transport.py`;
- `src/wellpulse/powder_w1.py`;
- `src/wellpulse/store.py`;
- `src/wellpulse/records.py`;
- `src/wellpulse/harness.py`.

External checks included current Eclipse Paho Python documentation, the OASIS MQTT 5.0 standard, current Internet of Things journal scope, and a recent 2026 experimental MQTT flow-control study.

## 3. Executive verdict

**PROCEED WITH MATERIAL PRE-SCORE AMENDMENTS.**

The project is scientifically viable and its core architecture is worth testing. The consortium does **not** recommend reopening RF calibration, replacing POWDER, adding a broad traffic-rate grid, expanding into 5G/O-RAN/mobility, or rebuilding the WP structure.

However, several issues should be corrected before physical H calibration and certainly before WP3. The most important result of this review is that the strongest scientific story is narrower and better than a generic claim that WellPulse “beats MQTT during outages”.

The current matched B1 client is intentionally volatile across **process restart**, but Eclipse Paho Python documents that its outgoing QoS>0 messages are retained in memory across ordinary network disconnect/reconnect while the same process remains alive. The scored hard outage is only 120 s at 1 record/s, while B1 is configured with a 4096-message volatile queue. Therefore S1/S2 may legitimately show near-complete eventual delivery for both B1 and W1. This would not invalidate WellPulse. It would establish an important boundary: application-level durability is expected to add its clearest integrity value when failure destroys volatile client state, especially S3, while network-only scenarios can expose recovery-time and overhead trade-offs.

That is a stronger, less vulnerable research question:

> **When does application-level durable record semantics add measurable value beyond a correctly configured standard MQTT QoS1 client, and what reliability/overhead price is paid for that value?**

## 4. P0 findings — close before physical H execution or before any scored run

### P0-1 — H-calibration invalidity rule can create outcome-dependent exclusion

**Verdict:** `AMEND`  
**Affected:** WP2 / `H_CALIBRATION_PLAN_v1.md`

Current H validity gate requires every pre-restoration W1 record eventually to arrive and the durable pending cohort to reach zero. A failed gate is currently classified as an invalid calibration trial and replaced.

This mixes two different states:

- a **technical invalidity**, such as wrong RF schedule, broken route, missing evidence, or failed Q0 readiness;
- a **valid scientific/implementation failure**, in which the frozen experiment was applied correctly but W1 itself failed to preserve or drain a record.

A technically valid W1 loss must never be replaced as “invalid” merely because the desired durability property failed. That would create outcome-dependent exclusion.

**Required amendment before H execution:** introduce separate states:

- `TECHNICALLY_INVALID` → preserve evidence; replacement allowed under predefined rules;
- `VALID_W1_RECOVERY_FAILURE` → preserve as valid adverse evidence; STOP H freeze and investigate; replacement does not erase the failure.

This amendment does not reopen RF calibration or alter the H formula.

### P0-2 — Missing broker/session isolation between runs

**Verdict:** `ADD GATE`  
**Affected:** WP2 evidence/runtime validation and WP3 execution

The experiment uses `clean_session=False`. Session state is associated with MQTT client identity. The current evidence schema does not explicitly freeze a run-specific client ID, topic namespace, or broker-session isolation rule.

Without explicit isolation, stale MQTT session/inflight state from one run can contaminate another run, especially after the project has already demonstrated that stale state can occur elsewhere in the LTE stack.

**Required pre-score rule:** 

- each scored run gets a deterministic unique MQTT client identity;
- each scored run gets a run-unique topic namespace;
- the same run-specific client identity is reused only across the intentional intra-run restart in S3;
- broker/session state is explicitly reset or proven isolated before each new run;
- client ID, topic, and `session_present` evidence are captured in the run manifest.

### P0-3 — S3 restart domain is not yet operationally frozen

**Verdict:** `ADD GATE`  
**Affected:** WP2 implementation validation / WP3

The protocol says telemetry generation continues throughout impairment and recovery, while S3 intentionally restarts the gateway process. The current local harness does not prove that exact failure-domain separation; its W1 “restart” is mainly a close/reopen of durable storage inside one harness process.

If the actual S3 restart also stops or resets the telemetry generator, S3 no longer cleanly tests gateway durability because the source workload changes at the same time.

**Required pre-score rule:**

- telemetry source/generator remains outside the gateway restart domain and continues at the frozen 1 Hz rate;
- restart target is explicitly named and limited to the gateway/client process;
- restart start/end/downtime are timestamped;
- W1 durable state survives that process restart;
- B1 recreates its volatile client using the same run-specific client identity;
- source sequence continuity is verified across the restart.

### P0-4 — B1 pending-message instrumentation can undercount disconnected QoS1 state

**Verdict:** `AMEND`  
**Affected:** WP2 implementation/evidence validation

`PahoQoS1Session.publish_async()` records a message in `_outstanding_mids` only when `publish()` returns success. Paho may retain QoS>0 outbound messages in its internal memory queue during disconnection and resend them after reconnect. The current counter can therefore fail to represent all accepted/queued B1 work during an outage.

**Required action:** either instrument accepted publish calls and PUBACK completion consistently for disconnected QoS1 messages, or explicitly remove `outstanding_mid_count` from any claim about true B1 queue occupancy. Do not use an implementation counter as a scientific endpoint until its semantics are proven.

### P0-5 — Record-ID collision handling is too permissive for a scientific integrity claim

**Verdict:** `AMEND`  
**Affected:** WP2 implementation

`DurableQueue.enqueue()` currently uses `INSERT OR IGNORE` on `record_id`. A repeated ID can therefore be silently ignored. For an architecture whose contribution includes stable identity and checksum-based reconciliation, silent collision handling is too weak.

**Required action:** fail closed on conflicting duplicate identity, or explicitly verify that an existing `record_id` has the identical canonical payload/checksum before treating it as idempotent. Any identity collision with different content must be surfaced as an integrity error.

## 5. P1 findings — freeze before WP3 scored authorization

### P1-1 — Reframe RQ1 around the failure-domain boundary

**Verdict:** `AMEND`  
**Affected:** WP0/WP1 wording and manuscript story

The current B1 configuration is strong enough that under S1/S2 it may retain all outage-generated records in volatile memory and deliver them after reconnection. At 1 record/s, a 120 s hard outage creates only about 120 outage-period messages versus B1's 4096-message configured queue.

Therefore a null or very small completeness difference in S1/S2 is an expected, informative result rather than evidence that the experiment failed.

Recommended interpretation:

- S0: healthy-path equivalence and overhead sanity;
- S1: intermittent-link recovery dynamics and overhead;
- S2: hard-outage recovery dynamics and overhead while volatile process state survives;
- S3: primary durability/integrity stress test across destruction of volatile client state.

The paper should ask where durable application semantics add value, not assume they improve every outage condition.

### P1-2 — Primary endpoint and precision stopping rule are not fully aligned with the stated recovery question

**Verdict:** `AMEND`  
**Affected:** WP1 analysis plan

The current precision rule decides whether to stop at three pairs using only the CI half-width of the completeness difference. If S1/S2 completeness saturates near 100% for both architectures, the campaign can stop quickly even if recovery time or backlog-drain dynamics differ materially.

Two defensible routes exist:

**Preferred route:** keep completeness as the integrity endpoint, but add a scenario-aligned recovery estimand for S1/S2 and require adequate predefined reporting/precision for it. This can use the already authorized reserve pairs rather than creating a new scenario grid.

**Minimal route:** explicitly narrow RQ1 so recovery metrics are secondary/descriptive and retain the existing completeness-only precision rule.

Do not leave the manuscript claiming a confirmatory recovery advantage while replication is controlled only by completeness precision.

### P1-3 — W1-only H calibration needs an explicit anti-bias justification

**Verdict:** `AMEND WORDING / REVIEW`  
**Affected:** WP1/WP2

A common H calibrated from W1 only is operationally practical and is frozen before outcome scoring, but a reviewer can still argue that the censoring window is treatment-informed.

The consortium does not recommend automatically adding a full B1 calibration campaign. It recommends explicitly documenting why H is an operational observation window rather than an effect-optimizing parameter, preserving the same H for all architectures/scenarios, and reporting the uncensored recovery-time evidence separately.

Also describe the n=3 estimator precisely: empirical nearest-rank p95 with three trials is simply the **maximum of three observed calibration drains**; do not imply that it is a stable population 95th percentile estimate.

### P1-4 — B2 durable MQTT comparator remains necessary but should stay compact

**Verdict:** `KEEP + CLOSE GATE`  
**Affected:** WP1 comparator freeze

Keep B1 as the primary matched causal comparator because it uses the same Python/Paho transport as W1. Do not replace B1 with Java/C as the primary arm because that would confound architecture with runtime/client implementation.

Qualify a strong durable standard-client B2 locally. If its persistence semantics are verified, use only a compact S2/S3 sensitivity amendment. This directly answers the strongest reviewer objection without turning the study into a three-arm full matrix.

MQTT v5 does not require a separate full scored arm merely because it is newer. Its persistent-session semantics still do not by themselves create durable application records that were generated while the client process was absent. The durable-client sensitivity gate is the more direct comparator question.

### P1-5 — Add a stronger inter-run washout/readiness gate

**Verdict:** `ADD GATE`  
**Affected:** WP2/WP3

The project already discovered a stale LTE user-plane bearer after repeated severe RF failures. The existing Q0 readiness safeguard is correct but the scored campaign should formalize inter-run washout more broadly.

Before every scored run require:

- Q0 end-to-end user-plane health over a bounded readiness window;
- route confirmation through the experimental tunnel;
- empty/fresh application state appropriate to the architecture;
- isolated MQTT broker/session namespace;
- baseline radio metrics within the accepted Q0 envelope;
- no unresolved prior-run queue/session residue.

This is especially important because S0 randomization currently happens to place B1 before W1 in all three healthy pairs. Strong washout prevents order from becoming a practical confound. If protocol amendment is already being made, counterbalancing S0 order is preferable.

### P1-6 — Rename cross-testbed “transportability” to a more defensible claim

**Verdict:** `AMEND WORDING`  
**Affected:** WP0/WP1/WP5

FIT and POWDER use different hardware, impairment mechanisms, and historical baselines, and the current analysis correctly avoids pooling them statistically. Therefore `cross-testbed consistency` or `triangulation` is more defensible than a broad transportability claim.

Reserve the term external replication for the POWDER OTA layer where the B1/W1 comparison is intentionally repeated.

### P1-7 — Freeze a pre-score reproducibility snapshot

**Verdict:** `ADD GATE`  
**Affected:** WP2 exit / WP5 reproducibility

Immediately before `scored_runs_authorized=true`, create a timestamped pre-score snapshot containing:

- exact protocol and amendment version;
- analysis plan version;
- run matrix and randomization hash;
- implementation commit;
- environment/runtime lock;
- evidence schema;
- comparator decision;
- frozen H;
- explicit scored authorization decision.

A Git tag/release or immutable commit manifest is sufficient. This is a cheap, high-value defense against post-outcome design drift.

## 6. P2 findings — manuscript/replication strengthening without scope inflation

### P2-1 — Keep workload scope explicitly low-rate

**Verdict:** `AMEND CLAIM BOUNDARY`, not a new scored WP

The current 1 Hz workload is appropriate for low-rate industrial telemetry. Recent MQTT experiments show that queue growth, latency, and reliability can change substantially as offered load approaches system capacity.

Do not add a multi-rate scored grid. Instead state clearly that the confirmatory claim is for the frozen low-rate telemetry regime and report enough CPU/memory/network/queue headroom to show the experiment is not accidentally broker/host-capacity limited. A local non-scored headroom check is optional if needed.

### P2-2 — Keep compact OTA replication, but predefine “consistent”

**Verdict:** `KEEP + ADD INTERPRETATION RULE`  
**Affected:** WP4

The current S1/S2-only OTA design is appropriately compact; do not repeat S3 merely because OTA is available.

Before OTA results are seen, define what counts as cross-environment consistency. At minimum preserve separate effect estimates and require a predeclared interpretation based on effect direction, uncertainty, and engineering magnitude rather than narrative selection. Do not pool conducted and OTA runs as one population.

### P2-3 — Venue strategy remains appropriate

**Verdict:** `KEEP`

`Internet of Things` remains a strong primary venue because its current scope explicitly includes IoT reliability, edge/cloud engineering, testbeds, software quality, and full research papers. `Computer Networks` and `Computer Communications` remain sensible backups depending on the final measurement emphasis.

Venue indexing/quartile/APC guidance should still be re-verified immediately before submission.

## 7. WP-by-WP consortium disposition

| WP | Current role | Consortium disposition | Required change before exit |
|---|---|---|---|
| WP0 | Novelty & venue | **AMEND, not reopen** | Narrow story to failure-domain boundary; tighten low-rate and cross-testbed claims; venue stays |
| WP1 | Protocol & statistics | **AMEND** | align recovery estimand/stopping; close B2; strengthen interpretation wording |
| WP2 | RF + measurement validation | **AMEND + ADD GATES** | H invalidity classification; MQTT isolation; S3 failure-domain gate; B1 instrumentation; identity collision; washout; physical H |
| WP3 | Conducted confirmatory campaign | **KEEP / BLOCKED** | start only after amended pre-score gate and explicit authorization |
| WP4 | OTA replication | **KEEP COMPACT** | predefine consistency interpretation; no full matrix expansion |
| WP5 | Analysis/artifact/paper | **KEEP** | add immutable pre-score snapshot and preserve one-command reconstruction |

## 8. Decisions explicitly NOT reopened

The consortium found no material reason to reopen:

- Q0 = 0 dB;
- Q1 = 40 dB;
- Q2 = 52 dB;
- Q3 = 55 dB;
- attenuator IDs `1 33 2 34` changed together;
- the selected `srslte-controlled-rf` conducted profile;
- the run as the statistical unit;
- paired randomized architecture comparisons;
- FIT evidence as a separate evidence class;
- the use of a compact OTA layer rather than a second full campaign;
- prohibition on field/agronomic/rural claims from remote-testbed evidence.

**No additional attenuation hunting is recommended.**

## 9. Revised critical path recommended by the consortium

```text
RF calibration PASS / FROZEN
        ↓
Approve pre-score amendment package
        ↓
Fix H failure classification + session isolation + S3 semantics + instrumentation/integrity gates
        ↓
Execute exactly 3 physical non-scored W1 H trials
        ↓
Freeze H or STOP if valid recovery fails / H > 300 s
        ↓
Close remote runtime/path/clock/identity/analysis gates
        ↓
Qualify/freeze compact B2 semantics amendment
        ↓
Create immutable pre-score snapshot
        ↓
Explicit scored authorization
        ↓
WP3 conducted campaign
        ↓
WP4 compact OTA replication
        ↓
WP5 deterministic analysis + artifact + manuscript
```

## 10. Immediate decision recommendation

The consortium recommends **approving the amendment package before the next physical H execution** because P0-1 affects the scientific validity of how a failed H trial would be classified.

The amendment should be minimal and pre-score. It should not change observed RF states, generate scored evidence, or inflate scientific completion.

Until amendments are formally accepted and implemented:

- WP2 remains `IN PROGRESS`;
- scientific completion remains **20%**;
- WP3 remains `BLOCKED`;
- `scored_runs_authorized=false`.

## 11. External source trail checked during review

- Eclipse Paho MQTT Python documentation — client behavior and known in-memory session limitation: https://eclipse.dev/paho/clients/python/docs/
- Eclipse Paho MQTT Python client API — outgoing messages retained by the live client across disconnect/reconnect: https://eclipse.dev/paho/files/paho.mqtt.python/html/client.html
- OASIS MQTT Version 5.0 standard — session state/session expiry semantics: https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html
- Radwan, Sheldon & Wang, *A backpressure-driven flow control model for stabilizing MQTT communication in IoT systems*, Scientific Reports, published 17 Aug 2026, DOI 10.1038/s41598-026-66865-8.
- Elsevier, *Internet of Things* journal scope — reliability, edge/cloud continuum, testbeds and quality assurance remain in scope.

## 12. Final consortium decision

**PROCEED WITH MATERIAL PRE-SCORE AMENDMENTS.**

No redesign from scratch. No new RF calibration. No broad experiment expansion. The highest-value action is to repair the P0 methodological/implementation gates now, then continue WP2 with the already planned three physical H trials.