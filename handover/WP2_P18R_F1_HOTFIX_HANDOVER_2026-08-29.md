# WellPulse — P18R Figure-1 Hotfix Handover

Date: 2026-08-29
Status: **PASS / HANDOVER READY**

## Purpose

This file is the continuation delta after the P18R scientific-figure engineering lifecycle. It records the accepted deterministic replacement for Figure 1 and the exact next project retrieval point.

The repository `HANDOVER_CURRENT.md` remains the broad project handover and must be read first. This file is the latest bounded delta for Figure 1 and continuation into the next production gate.

## Frozen project state

- Canonical repository: `aayoubMSA/WellPulse`
- Branch: `main`
- Current manuscript baseline: `manuscript/WELLPULSE_MANUSCRIPT_DRAFT_P17_CONSORTIUM_REVISION_2026-08-29.md`
- P13 claim envelope remains authoritative.
- P17V independent verdict remains **VALIDATED WITH PRE-SUBMISSION CONDITIONS**.
- No new experiment is required.
- No new empirical claim is required.
- Submission remains **NOT AUTHORIZED**.
- Live POWDER dependency: **NONE**.

## Figure-1 hotfix result

The prior P18R Figure 1 was rejected for layout/readability problems. A visually improved AI-generated version was reviewed by the consortium and was **REJECTED AS A PUBLICATION ASSET**; it is design-reference only and has no canonical scientific authority.

The accepted replacement is deterministic and code-generated.

### Scientific corrections frozen in the accepted Figure 1

1. Sender-local `SENT` is separated from receiver-side evidence.
2. Local `SENT` occurs after MQTT QoS 1 PUBACK in the canonical W1 implementation.
3. Receiver-side evidence is an independent path: unique receiver IDs → generated/received reconciliation → reported final completeness.
4. The publication-facing figure contains no internal `IC-xx` project-control identifiers.
5. FIT design visibly states `3 runs/cell` and `10,000 records/run`.
6. POWDER is represented as the full `E0–E11` controlled RF/service/recovery characterization campaign.
7. Synthesis wording is `two distinct resilience properties`: record-state survival + communication-path recovery.
8. The figure explicitly preserves: complementary evidence only; no FIT+POWDER quantitative pooling; no POWDER W1-vs-baseline effect.

### Accepted artifact identities

Final deterministic Figure-1 PDF SHA-256:

`4733d6fe171f14fd62e8d50d38f16a276a953481ee991045fbea86b7a5ab3578`

Standalone generator SHA-256:

`201897de563448037798678a73c998bd8b7a01f74bb4096995587f13d6667d48`

Local release package produced during execution:

`WellPulse_P18R_F1_Hotfix_Final_2026-08-29.zip`

### QA verdict

- known text overlaps: `0`
- known clipping: `0`
- known arrow/text crossings: `0`
- unintended color-cycle artefacts: `0`
- PDF width: `7.16 in`
- PDF fonts embedded: `PASS`
- two consecutive deterministic builds produced identical PDF SHA-256: `PASS`
- AI-generated asset dependency: `NONE`

`P18R_F1_HOTFIX=PASS_DETERMINISTIC_F1_ACCEPTED`

`AI_F1=REFERENCE_ONLY_NOT_CANONICAL`

## Important source-of-truth correction

A prior chat response described `P18RB` as completed. No canonical `P18RB` artifact is present in the repository at this handover point. Therefore the repository state wins: **P18RB is NOT yet canonically complete** and must be treated as the next bounded gate unless a future canonical artifact proves otherwise.

Do not reconstruct P18RB from chat memory.

## Exact next move

### WP2-P18RB — post-P18R high-standard benchmark

Benchmark the complete P18R main-figure set, using the accepted F1 hotfix as the Figure-1 authority, against the highest applicable venue-neutral standards before P19.

Required benchmark dimensions:

- scientific claim-to-display completeness;
- final-width typography and spacing;
- grayscale / non-color-only readability;
- vector source and embedded-font quality;
- publisher-neutral artwork production discipline;
- accessibility / alt-text readiness;
- deterministic rebuild / source-data traceability;
- consistent metadata / attribution / rights across F1–F4;
- no accidental Matplotlib color-cycle semantics;
- no scientific encoding changes without reopening P18R V&V.

P18RB may recommend evidence-neutral production normalization. It must not silently alter results, axes, aggregations, claims, or failure-domain semantics.

After P18RB PASS, proceed to:

### WP2-P19 — reviewer-facing supplementary atlas + sanitized artifact

- derive concise reviewer supplement from dossier v2.2;
- include E0–E11, validity/anomaly evidence, FIT ledger, and endpoint semantics;
- package analysis code, derived non-sensitive data, figures and manifests;
- perform privacy/security sanitization before any release;
- aim for an artifact capable of meeting an ACM-style Functional bar and approaching Reusable.

## Immutable prohibitions

Do not claim:

- scored P7B success;
- POWDER B1-vs-W1 advantage;
- strongest-durable-MQTT superiority;
- generic `WellPulse beats MQTT`;
- universal 52 dB threshold;
- deterministic RF-only recovery;
- exact broker latency from E10-D;
- population reliability from message counts or three FIT replicates;
- pooled FIT+POWDER inferential statistics;
- field/rural/Siwa/pump/hydraulic/agronomic validation.

## Attribution / affiliation

Canonical project identity for internal documents:

**Dr. Ahmed Elsayed Ayoub**  
Assistant Professor of Computer Engineering  
Department of Computer Systems Engineering  
Faculty of Engineering, MSA University  
Giza, Egypt

Do not invent coauthors, CRediT roles, funding, copyright ownership, or licensing terms.

## Handover close

`BRANCH_RESULT=PASS`

`VERIFIED_RESULT=F1_DETERMINISTIC_HOTFIX_ACCEPTED`

`DECISION_CHANGE=AI_F1_REJECTED_AS_PUBLICATION_ASSET`

`REMAINING_SCIENTIFIC_BLOCKERS=0`

`SUBMISSION_AUTHORIZED=NO`

`NEXT_EXACT_MOVE=WP2_P18RB_POST_P18R_HIGH_STANDARD_BENCHMARK`
