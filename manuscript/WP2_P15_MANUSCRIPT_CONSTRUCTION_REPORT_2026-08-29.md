# WP2-P15 — Manuscript Construction Report

Date: 2026-08-29  
Repository: `aayoubMSA/WellPulse`  
Branch: `main`  
Status: **PASS / COMPLETE / INTERNAL DRAFT ONLY**

## 1. Scope

P15 constructs the first complete evidence-bounded manuscript from the frozen P10–P14 scientific record. It does not authorize submission, select a final journal, create new experiments, alter raw data, execute B2, or reinterpret the failed scored P7B lane.

Canonical manuscript:

`manuscript/WELLPULSE_MANUSCRIPT_DRAFT_P15_2026-08-29.md`

Working title:

**WellPulse: Failure-Domain-Aware Validation of Durable IIoT Telemetry Across Embedded and Controlled-RF Testbeds**

## 2. Construction order

The manuscript was built in the required evidence-first order:

1. Methods;
2. Results;
3. Discussion;
4. Introduction / related work;
5. Abstract and title;
6. limitations, reproducibility and conclusion;
7. reference list.

This order was used to prevent the Introduction or desired narrative from expanding claims beyond measured evidence.

## 3. Frozen manuscript thesis

The manuscript does **not** present one global WellPulse reliability score.

It presents two complementary resilience properties:

- **record-state survival**, supported by the FIT `B0 vs W1` architecture comparison;
- **communication-path degradation/recovery**, supported by the manual non-scored POWDER physical-RF campaign.

The integrated contribution is failure-domain-aware triangulation with receiver-side evidence reconciliation.

## 4. Architecture source-level check

P15 re-read the canonical implementation rather than describing W1 from memory.

`src/wellpulse/records.py` confirms:

- stable `record_id = run_id:boot_id:sequence`;
- canonical sorted JSON serialization;
- SHA-256 checksum over the canonical record;
- explicit run, boot and sequence identity.

`src/wellpulse/store.py` confirms:

- SQLite-backed durable queue;
- `PRAGMA journal_mode=WAL`;
- `PRAGMA synchronous=FULL`;
- explicit `PENDING` / `SENT` state;
- record identity is the primary key;
- exact re-enqueue is idempotent;
- conflicting reuse of a record identity raises an integrity error rather than silently overwriting/ignoring it.

`src/wellpulse/transport.py` confirms the separate matched MQTT transport implementation used in the historical planned POWDER comparison and explicitly documents that Paho application-level disk persistence is absent there. This supports the conceptual distinction between transport/session behavior and WellPulse application-level durability. The manuscript does not claim that the uncompleted scored comparison occurred.

## 5. Literature refresh — 2026-08-29

P15 refreshed the closest literature through the current manuscript date.

Confirmed/current anchors include:

1. Asgari Araghi & Khendek (2026), application-layer IoT protocol testing SLR, DOI `10.1007/s43926-026-00322-w`.
2. Jesus, Lins & Laranjeiro (2025), MQTT robustness assessment, DOI `10.1016/j.iot.2025.101590`.
3. Colarusso, Falco & Zimeo (2025), Edge–Cloud business continuity/reconciliation, DOI `10.1016/j.iot.2025.101723`.
4. Domingues, Faria & Portugal (2024), MQTT disconnection retransmission/payload optimization, DOI `10.1186/s13638-023-02327-3`.
5. Gaspar et al. (2026), *The Price of Reliability: Stress-Testing MQTT in Practical IoT Communications*, DOI `10.1109/MIOT.2026.3681190`.
6. Herrera et al. (2026), CAMS F Edge DTN offline-first/CRDT/MQTT-SN, DOI `10.3390/fi18040180`.
7. Monzon Baeza et al. (2026), distributed 5G core store-and-forward for IoT sensing, DOI `10.3390/s26154919`.
8. Breen et al. (2021), POWDER platform, DOI `10.1016/j.comnet.2021.108281`.

### Novelty consequence

The literature confirms that none of the following can be claimed as standalone novelty:

- buffering;
- store-and-forward;
- offline-first operation;
- MQTT retransmission;
- MQTT robustness testing;
- edge/cloud reconciliation;
- 5G plus store-and-forward;
- use of a wireless testbed by itself.

The surviving novelty package is therefore deliberately compound and empirical:

- application-level durable identity/state with receiver reconciliation;
- explicit failure-domain decomposition;
- real-embedded architecture evidence;
- separate controlled physical-RF characterization;
- claim-to-immutable-evidence reproducibility.

### Gaspar 2026 control

The bibliographic record and authorship of Gaspar et al. were confirmed from author/institution sources. Publicly retrievable sources in this P15 pass did not expose sufficient methods/results for a detailed methodological comparison. The manuscript therefore cites the work only as evidence that practical MQTT reliability stress testing is current; it does **not** infer unobserved results. A final pre-submission retrieval/comparison remains mandatory in P16/submission QA if full text becomes available.

## 6. Manuscript sections completed

- Title: complete, provisional.
- Abstract: complete, evidence-bounded.
- Keywords: complete, provisional.
- Introduction: complete.
- Research questions: complete and aligned to P10.
- Related work/novelty boundary: complete for P15; final freshness check remains P16.
- Architecture/evaluation model: complete at manuscript-draft level.
- Methods: complete for FIT, POWDER, evidence policy and anomaly handling.
- Results: complete for RQ1–RQ4, with P14 figure/table insertion points.
- Discussion: complete.
- Threats to validity/limitations: complete.
- Reproducibility/evidence availability: complete.
- Conclusion: complete.
- References: eight high-relevance anchors included; final bibliography expansion/formatting remains submission-stage work.

## 7. P13 claim compliance

All nine P13-PASS claims are represented within their frozen strength class.

Primary empirical claims:

- IC-01: FIT W1/B0 completeness difference under C1/C2 — retained with B0 limitation.
- IC-04: POWDER transition region — retained as experiment-specific, not universal threshold.
- IC-06: mechanism-specific recovery — retained with E10-A censoring and E10-D upper-bound semantics.

Supporting claims IC-02/03/05/07 and methodological claims IC-08/09 are also represented without promotion in strength.

## 8. Explicit manuscript prohibitions checked

The draft contains no positive claim of:

- scored P7B success;
- POWDER B1-vs-W1 superiority;
- superiority over the strongest durable MQTT client;
- universal 52 dB failure threshold;
- deterministic RF-only recovery;
- exact broker recovery latency from E10-D;
- population reliability inferred from three FIT replicates or message count;
- field/rural/Siwa/pump/hydraulic/groundwater/agronomic validation;
- unresolved RF-path or runtime USRP identity;
- pooled FIT+POWDER inferential statistics.

The historical failed scored lane is not used as positive evidence.

## 9. P14 display integration

The manuscript includes insertion locations and frozen captions for:

- Figure 1 — FIT completeness;
- Figure 2 — FIT W1 backlog drain;
- Figure 3 — POWDER ascending/descending transition;
- Figure 4 — POWDER E3 repeatability;
- Table 1 — FIT architecture summary;
- Table 2 — POWDER transition summary;
- Table 3 — recovery timing semantics.

No new display or recalculated manuscript-only value was introduced.

## 10. Remaining issues reserved for P16

P15 is a complete scientific draft, not yet submission-ready. P16 must adversarially audit:

1. whether B0 remains too weak for the target venue despite explicit limitation;
2. whether the two-testbed story is sufficiently cohesive for one paper;
3. whether the contribution overweights methodological synthesis relative to direct empirical effects;
4. whether all architecture details required for reproducibility are adequately described in manuscript prose;
5. whether the manual/non-scored POWDER evidence is framed strongly enough to be useful but not overstated;
6. whether literature from late August 2026 or full Gaspar 2026 text changes novelty wording;
7. whether title/abstract wording would lead a reviewer to assume a POWDER W1 architecture experiment that did not occur;
8. whether a venue-specific structure/reference style requires revision;
9. whether public artifact release needs redaction/privacy controls before submission.

No new experiment is authorized by these QA questions.

## 11. Acceptance gate

- full manuscript draft exists: PASS;
- built from P10–P14 evidence envelope: PASS;
- all RQs represented: PASS;
- all primary P13 claims represented with caveats: PASS;
- P14 displays integrated by reference/caption: PASS;
- recent literature refresh performed: PASS;
- generic buffering/store-and-forward novelty removed: PASS;
- scored P7B promotion: NONE;
- POWDER architecture-comparison invention: NONE;
- FIT+POWDER statistical pooling: NONE;
- new experiment/live POWDER action: NONE.

`P15_MANUSCRIPT_FULL_DRAFT=YES`

`P15_PRIMARY_CLAIMS_WITHIN_P13=PASS`

`P15_LITERATURE_REFRESH=PASS_WITH_GASPAR_FULLTEXT_LIMITATION`

`P15_NEW_EXPERIMENT_REQUIRED=NO_AT_THIS_STAGE`

`WP2_P15=PASS_MANUSCRIPT_CONSTRUCTED_EVIDENCE_BOUNDED`

`P15_NEXT=WP2_P16_ADVERSARIAL_PUBLICATION_QA`
