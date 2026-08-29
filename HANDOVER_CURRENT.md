# WellPulse — Current Handover

Last updated: 2026-08-29 after **RF9C doctrine/package-lineage cleanup PASS**.  
Repository: `aayoubMSA/WellPulse`  
Branch: `main`

This file is the canonical operational retrieval point. Do not create a competing handover. GitHub remains the scientific/control record; promoted Drive evidence remains the durable binary authority; ChatGPT Library may hold cross-chat checkpoints pending Drive promotion.

## Current state

- **R9 / RF9B manuscript: CURRENT MANUSCRIPT AUTHORITY / SCIENTIFIC + EDITORIAL READY**
- **RF9C package-lineage cleanup: PASS / CURRENT PACKAGE AUTHORITY**
- P21-R9 author-authorization + portal-readiness packet: **NEXT / NOT STARTED**
- P22 external submission: **LOCKED**
- scientific blockers: **0**
- package-lineage blockers: **0**
- new experiment required for current bounded claims: **NO**
- new empirical claim required: **NO**
- submission authorized: **NO**

Publication-lane progress remains **90/100**. The final 10% is protected for author/portal authorization and actual submission/receipt.

## Manuscript authority — unchanged by RF9C

Title: **Beyond Reconnection: Failure-Domain-Aware Evaluation of Data Durability and Recovery in MQTT-Based IoT Telemetry**

Publication-facing author: **Ahmed Ayoub**

Target route:
- journal: **Internet of Things (Elsevier)**;
- article type: **Full Research paper**;
- initial route: **Subscription / non-OA**;
- backup #1: **IEEE Internet of Things Journal**.

Exact manuscript bytes remain:
- PDF: `WellPulse_Role_Model_R9_RF9B_SubmissionReady.pdf`
- pages: **24**
- PDF SHA-256: `f8f1fc73a50049e1308e6779267e2a52d5024e3bdcaac73b82df728cfd658bd3`
- TeX: `source/wellpulse_role_model_r9_rf9b.tex`
- TeX SHA-256: `c879212140dc1f12cce840d1b08eb7740ad88fbb38d85e4f97ab33dd8884a224`
- abstract: **216 words**
- bibliography: **38 / 38 cited**
- Supplement S1: **36 groups = 19 narrowing + 17 no-impact + 0 blockers**

## RF9C package authority

Current package:

`WellPulse_ROLE_MODEL_R9_RF9C_DoctrineClean_Package_2026-08-29.zip`

- size: **4,307,774 bytes**
- SHA-256: `f4324e6c982c49b7dc5c8d37b390366ab5a3c639a5790db000092a74300587a6`
- ZIP integrity: **PASS**
- outer manifest/hash parity: **PASS**
- nested S2 manifest parity: **PASS**
- S2 executable self-check: **PASS — sanitized artifact scientific invariants and claim envelope verified**
- R9 PDF bytes vs RF9B: **IDENTICAL**
- R9 TeX bytes vs RF9B: **IDENTICAL**

ChatGPT Library checkpoint:

`/My Research Artifacts/WellPulse/WellPulse_ROLE_MODEL_R9_RF9C_DoctrineClean_Package_2026-08-29.zip`

The older RF9B package remains historical. RF9C supersedes it for current submission-package authority only; it does not supersede the R9 manuscript scientific bytes.

Important provenance boundary: RF9C has not yet been independently promoted and hash-read-back-verified in Google Drive. Do not label RF9C as Drive-durable binary authority until that operation is actually completed.

## What RF9C fixed — package only

The doctrine reflection audit found three package-level lineage defects. RF9C closed all three without touching manuscript science:

1. `ROLE_MODEL_DOCTRINE_APPLICATION.md` was rebound from stale R7 identity/counts to **R9 / RF9B**, with current **36-group / 38-reference** state.
2. `FIELD_NATIVE_GLOSSARY.md` now states **CURRENT FOR R9** while preserving the field-native vocabulary.
3. Supplement S2 now has explicit **R9 binding / NOT SUBMITTED** status. The internal `P19_submission/` directory name is retained only for historical provenance; it is not current submission status. Historical figures inside S2 are explicitly separated from current R9 main-display Figures 1–4.

RF9C also regenerated the nested S2 manifest, outer `MANIFEST.csv`, outer `SHA256SUMS.txt`, and package ZIP.

Historical R5/R6/R7/R8/RF9A receipts remain intentionally preserved as provenance. Their version labels are historical evidence, not stale current authority.

`RF9C_SCOPE=PACKAGE_LINEAGE_ONLY`
`RF9C_PACKAGE_DELTA_CLOSED=YES`
`R9_MANUSCRIPT_BYTES_UNCHANGED=YES`
`SCIENCE_CHANGED=NO`

## Frozen scientific boundaries

### FIT
- `B0/W1 × C0/C1/C2 × 3 runs = 18 cells`; 10,000 generated records/run.
- **Run/replicate is the scientific unit**; within-run records are reconciliation observations, not independent samples.
- healthy: B0/W1 = 100%; failure conditions: B0 = 80%, W1 = 100% in all three runs.
- B0 misses exactly 2,000 outage-window records/run under C1/C2.
- W1 reconciles all 10,000 IDs exactly once under tested conditions.
- reconnect ≈1.3 s; durable queue drain ≈67.7–67.9 s.
- B0 is a non-durable mechanism-isolation control, **not** the strongest durable MQTT comparator.

### POWDER
- physical-RF/LTE/MQTT characterization, not architecture treatment-effect estimation.
- 52 dB is experiment/profile-specific, not universal.
- E10-A: censored, no scalar recovery latency.
- E10-B: exact 6.063318 s first MQTT; 6.609430 s first ping; 0.060172 s publish-to-receiver receipt.
- E10-C-B: exact ≈29.248 s first ping/MQTT.
- E10-D: upper bound only `<=10.908749 s`.
- FIT and POWDER are complementary and **not statistically pooled**.

## Immutable claim prohibitions

Never claim scored P7B success; POWDER B1-vs-W1 advantage; strongest-durable-MQTT superiority; generic `WellPulse beats MQTT`; universal 52 dB; deterministic RF-only recovery; exact E10-D broker recovery latency; population reliability from three FIT runs/message counts; pooled FIT+POWDER inference; historical firstness for persistence/store-and-forward/layered recovery; or field/Siwa/pump/hydraulic/groundwater/agronomic/crop/industrial-process validation.

Historical scored state remains:

`B1=NULL_ABORTED_AFTER_Q3`
`HISTORICAL_B1=CONSUMED`
`SCORED_P7B_STATUS=UNCHANGED_NOT_PASSED`

## Residual scientific limitations — disclosed, not blockers

1. no matched durable MQTT comparator for architecture-superiority claims;
2. three FIT run-level replicates limit inferential breadth;
3. literature audit is targeted, not systematic/exhaustive;
4. POWDER is descriptive characterization;
5. no prospective probe-cadence sensitivity study;
6. no independent inter-node clock-error bound; cross-node timing remains descriptive.

None requires new evidence for the current bounded R9 claim.

## Publication identity / disclosures

- sole/corresponding author: **Ahmed Ayoub**
- affiliation: Computer Systems Engineering Department, Faculty of Engineering, October University for Modern Sciences and Arts (MSA University), 6th of October City 12451, Egypt
- institutional email: `aelsayedo@msa.edu.eg`
- ORCID: `0009-0004-7895-3191`
- external research funding: none identified
- competing interests: none identified
- CRediT, data availability, FIT/POWDER acknowledgments, and Elsevier AI-use declaration: present

## Mandatory read order for continuation

1. `HANDOVER_CURRENT.md`
2. current RF9C package from `/My Research Artifacts/WellPulse/`
3. inside RF9C, read when needed:
   - `RF9C_PACKAGE_QA.md`
   - `RF9C_PACKAGE_LINEAGE_CLEANUP.md`
   - `RF9B_SUBMISSION_READINESS_GATE.md`
   - `RF9B_EXACT_ARTIFACT_QA.md`
   - `ROLE_MODEL_DOCTRINE_APPLICATION.md`
   - `FIELD_NATIVE_GLOSSARY.md`
   - `README.md`
4. P13/P17V/P9 repository authorities only when exact claim or POWDER trace adjudication is required.

## Exact next gate — P21-R9

Prepare the internal author-authorization / portal-readiness packet against the **R9 manuscript + RF9C package**.

P21-R9 must:
1. recheck current *Internet of Things* portal/editorial requirements;
2. verify concurrent-submission state;
3. verify author/ORCID/email/affiliation/corresponding-author metadata;
4. map exact R9/RF9C files to portal roles;
5. preserve Subscription/non-OA unless explicitly changed;
6. reverify APC/EKB/STDF/institutional coverage before accepting paid OA;
7. inspect the portal-generated PDF/render before irreversible approval;
8. stop before submission unless fresh explicit authorization is given.

Do **not** infer submission authorization from `continue`, `go on`, `next`, manuscript approval, venue preference, or RF9C cleanup approval.

## Stop state

`R9_CURRENT_MANUSCRIPT_AUTHORITY=YES`
`RF9B_SCIENTIFIC_GATE=PASS`
`RF9B_EDITORIAL_GATE=PASS`
`RF9C_CURRENT_PACKAGE_AUTHORITY=YES`
`RF9C_PACKAGE_DELTA_CLOSED=YES`
`ROLE_MODEL_PAPER_GATE=PASS`
`PUBLICATION_LANE_PROGRESS=90_OF_100`
`P21_R9=NEXT_NOT_STARTED`
`P22_LOCKED=YES`
`SUBMISSION_AUTHORIZED=NO`
`PAYMENT_AUTHORIZED=NO`
`COPYRIGHT_OR_LICENSE_ACCEPTANCE_AUTHORIZED=NO`
`CURRENT_PHASE=RF9C_PACKAGE_CLEAN_P21_NEXT`
