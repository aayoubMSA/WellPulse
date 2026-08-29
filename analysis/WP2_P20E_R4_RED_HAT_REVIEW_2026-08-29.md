# WP2-P20E-R4 — Independent Red-Hat Review

Date: 2026-08-29
Target: **Internet of Things (Elsevier)**
Article type: **Full Research paper**
Current manuscript: **R4-R1**
Status: **PASS AFTER FINITE PRODUCTION REPAIR / NO SUBMISSION**

## Review posture

P20E-R4 independently reviewed the from-scratch R4 manuscript and did not inherit the prior R3/R3-R2 red-hat PASS. Frozen FIT/POWDER authorities, P13/P17V claim limits, P18RC figures, P19 reproducibility evidence, authorship, rights and publication identity remained immutable.

## Finite defects found in initial R4 bytes

Three submission-production defects were found:

1. abstract = **269 words**, above the current Internet of Things limit of 250;
2. keywords = **8**, above the current journal allowance of 1–7;
3. all five highlights were <=85 characters but several used project/testbed acronyms (`W1`, `B0`, `FIT`, `POWDER`) despite current Elsevier highlights guidance to avoid acronyms/jargon.

R4-R1 therefore changes only submission-facing production text:

- abstract = **250 words**;
- keywords = **7**;
- highlights = **5**, each **59–69 characters**, rewritten without project/testbed acronyms;
- editable `highlights.docx` added;
- generative-AI declaration heading normalized to Elsevier's current `...in the writing process` wording.

No experiment, figure, result, statistical unit, reference set, claim class or inferential role changed.

## Scientific red-hat result

### Literature / novelty

- 32 source/axis groups retained: 25 peer-reviewed articles + 1 normative standard + 6 official technical/project sources;
- 17 wording-narrowing, 15 contextual/no-impact, 0 scientific blockers;
- audit remains targeted/claim-bounding, not systematic/PRISMA/meta-analysis;
- all **32/32** bibliography items are cited; unresolved citation keys = 0;
- material/new comparator DOI records rechecked against publisher/institutional sources;
- no unsupported historical-firstness or generic MQTT-superiority claim.

### Comparator fairness

- B0 remains explicitly **non-durable publish-only baseline**;
- no `WellPulse beats MQTT` claim;
- no strongest-durable-MQTT superiority claim;
- a matched durable MQTT comparator is disclosed as the highest-value future extension.

### FIT independent recomputation

From the reviewer-facing reconstruction CSV:

- B0/W1 × C0/C1/C2 × 3 = 18 cells;
- 10,000 generated records/cell;
- C0 B0/W1 = 100% all runs;
- C1 B0 = 80%, W1 = 100% all runs;
- C2 B0 = 80%, W1 = 100% all runs;
- B0 C1/C2 permanent missing = exactly 2,000/run;
- W1 final missing/duplicate/unexpected = 0;
- C1 reconnect means: B0 1.325412 s, W1 1.317088 s;
- C2 reconnect means: B0 1.362121 s, W1 1.344870 s;
- W1 backlog drain: C1 67.731246 s, C2 67.870252 s.

Run/replicate remains the scientific unit. The 10,000 within-run records are not treated as independent samples. No population reliability inference or unsupported CI was introduced.

### POWDER semantics

- E1/E2/E3 transition remains experiment-specific; no universal 52 dB threshold;
- E10-A remains censored / no scalar latency;
- E10-B exact first MQTT 6.063318 s;
- E10-B exact first ping 6.609430 s;
- E10-B publish-to-CORE receipt 0.060172 s;
- E10-C-B exact first ping 29.247733 s;
- E10-C-B exact first MQTT 29.248129 s;
- E10-D remains upper bound `<=10.908749 s`;
- E8 receiver authority remains 40/60 unique delivery despite duplicate sender activity;
- E9 no-fault control remains 60/60;
- FIT and POWDER remain complementary/non-substitutable and are not statistically pooled.

### Scope discipline

No affirmative field/rural/pump/hydraulic/groundwater/agronomic/crop/industrial-process validation claim was detected.

## Reproducibility / privacy / rendering

- S1 rows = 32; S1 PDF visual QA PASS;
- S2 has no `__pycache__` or `.pyc`;
- isolated `python -I artifact_selfcheck.py`: PASS;
- main manuscript private-RFC1918 scan: none;
- legacy expanded publication-name variants: none;
- PDF author metadata: `Ahmed Ayoub`;
- all main-PDF fonts embedded;
- PDF preflight warnings = 0;
- four main scientific figures are byte-identical to the R4 figure inputs.

## Deterministic rebuild

R4-R1 was independently rebuilt from packaged TeX + figures:

- packaged pages = 21;
- rebuild pages = 21;
- render comparison = **0 changed pages / 0.0% changed pixels**.

Minor underfull-box warnings and one sub-point overfull warning are non-clipping and visually acceptable in the preprint layout.

## Residual reviewer risks — disclosed, not blockers

1. durable MQTT comparator may be requested;
2. three FIT replicates limit inferential breadth;
3. literature audit is targeted, not exhaustive/systematic;
4. Gaspar et al. remains context/scope-level only; no unsupported detailed method/result comparison;
5. 21-page survey-visible preprint is intentional; no verified journal page-limit blocker was found.

## Verdict

`WP2_P20E_R4=PASS_AFTER_FINITE_PRODUCTION_REPAIR`

`CURRENT_MANUSCRIPT=R4R1`

`SCIENTIFIC_BLOCKERS=0`

`PRODUCTION_BLOCKERS=0`

`NEW_EXPERIMENT_REQUIRED=NO`

`NEW_EMPIRICAL_CLAIM_REQUIRED=NO`

`P21_R4_UNLOCKED=YES`

`P22_LOCKED=YES`

`SUBMISSION_AUTHORIZED=NO`
