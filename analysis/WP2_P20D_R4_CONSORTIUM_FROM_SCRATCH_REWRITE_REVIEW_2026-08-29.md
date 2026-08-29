# WP2-P20D-R4 — Consortium From-Scratch Rewrite Review

Date: 2026-08-29
Target venue: **Internet of Things (Elsevier)**
Status: **PASS / NEW NARRATIVE AUTHORITY / NO SUBMISSION**

## Mandate

The author requested that the consortium read the red-hat findings and rewrite the paper from scratch.

The rewrite therefore preserved only:

- frozen scientific measurements and endpoint semantics;
- P18/P18RC figure assets;
- verified bibliography records;
- publication identity, disclosures, and rights metadata.

The prior R3-R2 manuscript prose was not used as the narrative template.

## Consortium lenses

The new manuscript was evaluated through distinct lenses:

1. editorial narrative and desk-review coherence;
2. IoT/MQTT systems and comparator fairness;
3. experimental design and statistical inference;
4. wireless/testbed methodology;
5. literature/novelty positioning;
6. evidence provenance and receiver reconciliation;
7. reproducibility and privacy/security;
8. adversarial reviewer risk.

## Red-hat issues carried into the rewrite

1. The manuscript must visibly reflect the amount of literature/novelty work.
2. The reference backbone must be large enough to support an explicit audit.
3. B0 is non-durable and cannot become a generic MQTT comparator.
4. Three FIT replicates do not justify population reliability inference.
5. FIT and POWDER cannot be statistically pooled.
6. Recovery endpoints must preserve exact/censored/upper-bound semantics.
7. Negative/anomalous evidence must constrain the narrative rather than be cleaned away.
8. The literature audit must not be presented as a PRISMA/systematic review.
9. No field/agronomic/industrial-process validation may be implied.

## R4 narrative architecture

The paper now follows one argument:

`prior-art audit -> claim boundary -> two-property model -> FIT record survival -> POWDER path recovery -> synthesis`

This replaces the previous impression of an experiment report with a survey added beside it.

## Literature/novelty state

The R4 main text explicitly reports the targeted submission-date audit:

- 32 source/axis groups;
- 25 peer-reviewed scholarly articles;
- 1 normative MQTT standard;
- 6 official technical/platform sources;
- 17 wording-narrowing outcomes;
- 15 contextual/no-impact outcomes;
- 0 scientific blockers.

All 32 bibliography entries are cited in the main paper. Supplement S1 remains the complete source-level collision matrix.

The audit is described as **claim-bounding and non-exhaustive**, not a systematic review, meta-analysis, PRISMA review, or literature-prevalence estimate.

## Scientific checks

### FIT

PASS.

- matrix remains B0/W1 × C0/C1/C2 × three runs;
- 10,000 generated records/cell;
- C0 B0/W1 = 100%;
- C1/C2 B0 = 80%; W1 = 100%;
- 2,000 B0 misses correspond exactly to the outage interval;
- W1 final reconciliation contains all generated IDs exactly once;
- backlog-drain means remain 67.731246 s and 67.870252 s;
- C2 remains gateway-process `exec` restart, not node reboot;
- B0 is explicitly non-durable in the Introduction, system model, Results interpretation, and Discussion.

### Statistical discipline

PASS.

- run/replicate remains the scientific unit;
- 10,000 within-run messages are not treated as independent samples;
- no population reliability probability is inferred;
- no unsupported confidence interval is introduced.

### POWDER

PASS.

- 52 dB remains experiment-specific, not universal;
- E10-A remains censored;
- E10-B remains 6.063318 s first MQTT, 6.609430 s first ping, 0.060172 s publish-to-CORE receipt;
- E10-C-B remains 29.247733 s first ping, 29.248129 s first MQTT;
- E10-D remains <=10.908749 s upper bound only;
- E8 broker-only fault remains separated from healthy LTE;
- receiver-side unique IDs govern final delivery;
- FIT and POWDER remain conceptually integrated but statistically unpooled.

## Reproducibility / evidence checks

PASS.

- receiver-side reconciliation is explicit in the main methodology;
- sender/receiver disagreements and E8 duplicate-send behavior remain visible examples;
- reported value -> reconstructed table -> raw source -> archive -> SHA-256 chain remains explicit;
- Supplement S1 is the novelty-control chain;
- Supplement S2 is the empirical/reproducibility chain;
- private/restricted platform material remains excluded from reviewer/public package.

## Publication checks

PASS.

- publication name: **Ahmed Ayoub**;
- target: Internet of Things (Elsevier);
- article class: Full Research paper;
- 21-page preprint build;
- 32/32 references cited;
- fonts embedded;
- PDF opens and renders without clipping/overlap;
- Elsevier highlights reduced to five bullets, each <=85 characters;
- funding/COI/CRediT/testbed acknowledgment/generative-AI declaration retained.

Current Elsevier journal scope remains compatible with IoT reliability, software engineering, testbeds and quality assurance; the journal also accepts Full Research papers.

## Residual reviewer risks — disclosed, not blockers

1. **Matched durable MQTT comparator** — a reviewer may ask for one. R4 explicitly states that this is the highest-value extension for any future architecture-superiority claim.
2. **Three FIT replicates** — a reviewer may ask for more. R4 limits inference to repeated observed run-level outcomes and makes no population reliability claim.
3. **Audit methodology** — a reviewer may ask for systematic-review machinery because the literature effort is substantial. R4 explicitly states that the audit is targeted and claim-bounding rather than exhaustive.

## Consortium verdict

The R4 rewrite is scientifically stronger than R3-R2 because the literature survey now controls the interpretation of the experiments rather than appearing as an appended literature section.

No new science is required for this rewrite.

`WP2_P20D_R4=PASS_FROM_SCRATCH_CONSORTIUM_REWRITE`

`SCIENTIFIC_BLOCKERS=0`

`PRODUCTION_BLOCKERS=0`

`NEW_EXPERIMENT_REQUIRED=NO`

`NEW_EMPIRICAL_CLAIM_REQUIRED=NO`

`SUBMISSION_AUTHORIZED=NO`
