# WP2-P20E-R5 — Role Model Scientific + Editorial Red-Hat

Date: 2026-08-29  
Manuscript: **R5 Role Model Paper**  
Target: Internet of Things (Elsevier)  
Status: **PASS / NO SCIENTIFIC OR PRODUCTION BLOCKER / NO SUBMISSION**

## Independent posture

R5 materially changes narrative architecture, terminology, mathematical endpoint definitions, and all four main figures. Therefore P20E-R4 was not inherited. R5 was freshly checked against P13/P17V frozen science, packaged source data, claim prohibitions, reproducibility artifact, publication identity, and rendered manuscript.

## Scientific Red Hat

### FIT recomputation — PASS

- 18 cells = two implementations × three conditions × three run-level replicates;
- 10,000 generated records/run;
- healthy: both implementations 100% in all runs;
- broker outage: non-durable 80%, durable 100% in all runs;
- outage + gateway-process restart: non-durable 80%, durable 100% in all runs;
- non-durable outage cells permanently miss exactly 2,000/run;
- durable final missing/duplicate/unexpected = 0;
- durable queue-drain means remain 67.731246 s and 67.870252 s;
- run/replicate remains scientific unit; no message-level pseudoreplication.

### POWDER semantics — PASS

- 51 dB ascending: ICMP loss 30%, MQTT complete;
- 52 dB ascending: ICMP loss 60%, MQTT completeness 65%;
- transition remains experiment-specific;
- RF-only timing remains censored/no scalar latency;
- RF + UE restart remains 6.063318 s first MQTT, 6.609430 s first ping, 0.060172 s publish-to-receiver receipt;
- RF + core-side restart remains 29.247733 s first ping and 29.248129 s first MQTT;
- broker restart remains upper bound `<=10.908749 s`;
- exact/censored/upper-bound observations are not collapsed.

### Comparator / inference — PASS

The paper explicitly identifies the comparison as a **non-durable publisher baseline** and states that a matched durable MQTT configuration could reduce or eliminate the observed completeness gap. No generic MQTT superiority or strongest-durable-MQTT superiority is claimed.

FIT and POWDER remain complementary/non-substitutable and statistically unpooled.

### Mathematics — PASS

Added equations define measured endpoints and set operations only; they do not create statistical power, a universal reliability model, or new empirical claims.

### Negative evidence / scope — PASS

The paper preserves the three-run limitation, comparator limitation, variable transition behavior, censored RF-only observation, upper-bound timing, heterogeneous endpoints, and explicit denial of field/agronomic/pump/hydraulic/groundwater/rural/crop/industrial-process validation.

## Editorial / Role Model Red Hat

### Field-native voice — PASS

Mandatory Field-Native Glossary Gate applied. Reader-facing narrative uses native MQTT/IoT/dependability terms. Internal W1/B0/C0/C1/C2, E-series, WP/gate/red-hat/claim-envelope terminology is removed from publication-facing prose/legends where unnecessary.

### Narrative — PASS

Title leads with the scientific problem rather than project branding. Narrative spine:
`established mechanisms -> evaluation ambiguity -> formal endpoint model -> controlled physical evidence -> engineering interpretation -> limitations -> transferable lesson`.

### Literature — PASS

- 32 direct novelty-control groups;
- 2 additional framing references;
- 34/34 bibliography items cited;
- targeted/claim-bounding status explicit;
- no pseudo-systematic-review completeness claim.

### Visual / engineering communication — PASS

Four main figures and two synthesis/design tables were visually inspected at publication width. No clipping, overlap, unreadable labels, or misplaced float. Engineering design implications are explicit but not mislabeled as deployment validation.

### Submission-facing QA — PASS

- pages: 23;
- abstract: 240 words;
- keywords: 7;
- highlights: 5, all <=72 characters;
- PDF openable, unencrypted, not scanned;
- author metadata: Ahmed Ayoub;
- fonts embedded;
- overfull hbox warnings: 0;
- Supplement S2 isolated self-check: PASS;
- independent clean rebuild: 23 pages;
- render diff: **0 changed pages / 0.0% changed pixels**.

## Residual reviewer risks — not blockers

1. a matched durable MQTT comparator may be requested for a stronger architecture-superiority claim;
2. three FIT replicates limit inferential breadth;
3. the literature audit is targeted, not exhaustive/systematic;
4. POWDER is descriptive characterization, not architecture treatment-effect estimation.

## Verdict

`WP2_P20E_R5_SCIENTIFIC_RED_HAT=PASS`

`WP2_P20E_R5_EDITORIAL_RED_HAT=PASS`

`ROLE_MODEL_PAPER_GATE=PASS`

`SCIENTIFIC_BLOCKERS=0`

`PRODUCTION_BLOCKERS=0`

`NEW_EXPERIMENT_REQUIRED=NO_FOR_CURRENT_BOUNDED_CLAIMS`

`P21_R5_UNLOCKED=YES`

`P22_LOCKED=YES`

`SUBMISSION_AUTHORIZED=NO`
