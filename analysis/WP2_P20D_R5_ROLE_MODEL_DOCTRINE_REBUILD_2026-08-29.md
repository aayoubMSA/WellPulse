# WP2-P20D-R5 — Role Model Paper Doctrine Rebuild

Date: 2026-08-29  
Target: **Internet of Things (Elsevier)**  
Article type: **Full Research paper**  
Status: **PASS / CURRENT MANUSCRIPT AUTHORITY / NO SUBMISSION**

## Mandate

Apply the cross-project **Role Model Paper Doctrine (LL-049 / Research Operating Doctrine v2.2 §22A)** to the current WellPulse paper so it reads as a mature IoT/reliability systems study rather than a student-project experiment.

Hard constraints:
- frozen FIT/POWDER science unchanged;
- no new empirical claim;
- no generic MQTT superiority;
- no field/industrial-process validation claim;
- no cross-testbed statistical pooling;
- canonical publication identity remains **Ahmed Ayoub**.

## Role Model doctrine applied

Target: **Teach → Prove → Translate → Persuade**.

### Field-Native Glossary Gate

Applied before the rewrite from current MQTT/IoT robustness, persistence, store-and-forward, testbed, and dependability literature. Reader-facing vocabulary now uses field-native terms including data durability, end-to-end delivery completeness, persistent sessions, failure domains, fault injection, communication-path recovery, queue drain/catch-up, receiver-side reconciliation, programmed attenuation, transition region, repeatability, and censored/upper-bound timing.

Project-control vocabulary is removed from reader-facing narrative and figure legends where unnecessary: W1/B0/C0/C1/C2, E-series run codes, WP/gate/red-hat/claim-envelope/frozen-authority terminology.

### New scientific title

**Beyond Reconnection: Failure-Domain-Aware Evaluation of Data Durability and Recovery in MQTT-Based IoT Telemetry**

The scientific problem now leads; the project brand does not lead the paper.

### Literature architecture

- 32 source/axis groups remain the direct targeted novelty-control audit;
- 25 peer-reviewed scholarly articles + 1 normative MQTT standard + 6 official technical/platform sources;
- 2 additional framing references support dependability terminology and current MQTT deployment context;
- bibliography = **34 / 34 cited**;
- audit remains targeted/claim-bounding, not systematic/PRISMA/meta-analysis/exhaustive.

The literature synthesis explicitly removes mechanism claims already owned by persistent sessions, durable client state, queued delivery, store-and-forward, downstream acknowledgment, end-to-end confirmation, robustness/fault testing, and testbed practice. The retained contribution is the bounded evaluation question.

### Mathematical foundation

R5 formalizes only quantities that remove ambiguity:
- `C_e2e = |G ∩ R| / |G|` for receiver-reconciled completeness;
- `M = G \ R` for permanent missing records;
- `D = N_R - |R|` for duplicates;
- `T_path(e)=t_e-t_0` for endpoint-specific path recovery;
- `T_drain=t_complete-t_reconnect` for queue catch-up;
- a recovery-observation tuple retaining failure domain, action, endpoint, timing, and exact/censored/upper-bound semantics.

These are measurement definitions, not a claimed universal reliability theory.

### Figure rebuild

Four deterministic main figures now answer reviewer-level questions:
1. failure-domain-aware evaluation framework and complementary evidence roles;
2. end-to-end delivery completeness plus reconnection and queue-drain cost;
3. cross-layer transition behavior plus near-transition repeatability;
4. failure-domain interventions plus exact/censored/upper-bound recovery semantics.

### Practical/industrial translation

A dedicated **Engineering Interpretation and Design Guidance** section maps measured endpoints to:
- historical data integrity;
- service restoration;
- freshness after outage;
- fault diagnosis;
- delivery auditability.

The table explicitly states that these are design implications, **not field-validation claims**.

## Frozen science check

No accepted measurement or inferential role changed. FIT remains 18 run-level cells with 10,000 records/run; non-durable outage cells remain 80% and durable application-buffered cells 100%; durable queue-drain means remain 67.731246 s and 67.870252 s. POWDER recovery timings and exact/censored/upper-bound semantics remain unchanged. B0 remains non-durable and not the strongest durable MQTT comparator. FIT and POWDER remain unpooled.

## Production state

- pages: **23**;
- abstract: **240 words**;
- keywords: **7**;
- references: **34 / 34 cited**;
- PDF SHA-256: `28f508b1c6abf91c555e9cfa72148a47efde6dda6e7c91fc8054d27f4d4af7e3`;
- TeX SHA-256: `46d95f42b2bbbf8d9d561ad866248058e63bb36d03c75149020d4a89ae628402`.

## Verdict

`WP2_P20D_R5=PASS_ROLE_MODEL_DOCTRINE_REBUILD`

`R5_CURRENT_MANUSCRIPT_AUTHORITY=YES`

`NEW_EXPERIMENT_REQUIRED=NO`

`NEW_EMPIRICAL_CLAIM_REQUIRED=NO`

`SUBMISSION_AUTHORIZED=NO`
