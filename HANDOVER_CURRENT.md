# WellPulse — Current Handover

**Last updated:** 2026-08-30 after R14/RF9H two-minor closure and P5 journal-package preparation.  
**Repository:** `aayoubMSA/WellPulse`  
**Branch:** `main`

This is the canonical operational handover. Do not create a competing current-state document.

## Current state

- **R14 / RF9H: CURRENT MANUSCRIPT AUTHORITY**
- **P4 final Scientific + Editorial Red Hat: PASS**
- **P5 journal-facing package preparation: PASS**
- **P5 portal-generated PDF inspection: NOT YET PERFORMED**
- **External submission: LOCKED / NOT EXECUTED**
- Scientific blockers for the bounded claim: **0**
- New experiment required: **NO**

## Manuscript authority

Title: **Beyond Reconnection: Failure-Domain-Aware Evaluation of Data Durability and Recovery in MQTT-Based IoT Telemetry**

Author/corresponding author: **Ahmed Ayoub**  
Affiliation: Computer Systems Engineering Department, Faculty of Engineering, October University for Modern Sciences and Arts (MSA University), 6th of October City 12451, Egypt  
Email: `aelsayedo@msa.edu.eg`  
ORCID: `0009-0004-7895-3191`

Target route:
- journal: **Internet of Things (Elsevier)**;
- article type: **Full Research Paper**;
- default publication model: **Subscription / non-OA**;
- backup: **IEEE Internet of Things Journal** only if rerouting becomes necessary.

Current R14 manuscript:
- PDF: `WellPulse_Role_Model_R14_RF9H_Two_Minor_Closure.pdf`
- pages: **28**
- PDF SHA-256: `d5f8006ecc3b0a284c7b5836ba4fee505878efe4003380d8cdbf1454a42b2f3a`
- canonical TeX SHA-256: `18b1c3579ce0e04eb4b0cc3f4c835c4ecb6c9ecdc094acd26fc2f62727b46d98`
- bibliography: **38/38 cited**
- abstract: **227 words**
- keywords: **7**

## Journal-facing submission package

Filename:
`WellPulse_Submission_Package_R14_RF9H_2026-08-30.zip`

SHA-256:
`62c79223c0bd825250f7dbf92fc9cb51c2e40678285b40d5b5432a4452bd8b33`

ChatGPT Library durable checkpoint:
`/My Research Artifacts/WellPulse/WellPulse_Submission_Package_R14_RF9H_2026-08-30.zip`

The package intentionally excludes historical internal QA/change-history clutter. It contains only the source/manuscript, front-matter submission assets, supplements, upload guidance, and integrity manifest.

### Front matter prepared

- Cover letter: **READY**
- Highlights: **READY**, 5 bullets, all <=85 characters
- Highlights were tightened for a general audience; they do not alter manuscript claims.
- Graphical abstract: **READY**, deterministic vector artwork, not AI-generated
- Portal metadata: **READY**
- Data statement: **READY**
- AI-use declaration: **READY**
- CRediT/funding/COI/acknowledgments: **in manuscript**

### Supplementary files

- S1 literature novelty audit PDF: SHA-256 `9ece93bdbba1eb4c017411ea5873c2e759dd27e74e8591497ce5a9a621f1cbc1`
- S2 reproducibility artifact ZIP: SHA-256 `f65ca67174c66513f0fbaf2ecfcb5d29b0490c3777d3d0428e08d1ca99c7da61`
- S2 executable self-check: **PASS**

## P5 executable release gate

Fresh clean-unpack validation of the final submission ZIP passed:

- package manifest/hash parity: **PASS**;
- flattened LaTeX source clean compile: **PASS**;
- compiled submission source vs frozen R14 PDF: **28/28 pages pixel-identical**;
- S2 ZIP integrity: **PASS**;
- S2 `artifact_selfcheck.py`: **PASS**;
- graphical abstract: **vector-only**, visually inspected;
- cover letter DOCX: visually inspected after metadata scrub;
- highlights DOCX: visually inspected after metadata scrub;
- no scientific data/result/reference/claim change introduced by package preparation.

Detailed gate: `/My Research Artifacts/WellPulse/P5_RELEASE_GATE_R14.md`.

## Figure-production authority

R13/RF9G permanently fixed the figure-compression failure mode:

- Figure 1 is native TikZ at manuscript width;
- Figures 2–4 are vector PDFs generated at the final 390-pt production width;
- rule: **redesign / split / reflow — never shrink-to-fit**;
- any venue/layout change requires fresh width/font preflight.

The existing Research Operating Doctrine v2.2 was strengthened in place with this rule.

## Frozen scientific boundaries

### FIT IoT-LAB
- B0/W1 × C0/C1/C2 × 3 run-level replicates = 18 cells.
- 10,000 generated records/run; the **run** is the scientific unit.
- healthy: B0/W1 complete at the declared endpoint.
- failure cells: B0 8,000/10,000 vs W1 10,000/10,000 in every replicate.
- +20 percentage points is a **bounded mechanism-isolation contrast**, not generic MQTT superiority.
- reconnect ~1.3 s; durable queue drain ~67.7–67.9 s.
- receiver count termination bounds the claim to the declared capture endpoint.

### POWDER
- physical RF/LTE/MQTT characterization; not architecture treatment-effect estimation.
- programmed attenuation thresholds are profile-specific, not universal.
- recovery endpoints remain exact, censored, or upper-bound as preserved.
- E10 publish-to-receipt 0.0602 s is an exact preserved-timestamp difference but remains descriptive because no independent inter-node clock-synchronization error bound was established.
- FIT and POWDER are **not statistically pooled**.

## Immutable claim prohibitions

Do not claim:
- strongest-durable-MQTT superiority;
- generic `WellPulse beats MQTT`;
- population reliability from three FIT runs or from message counts;
- universal 52 dB behavior;
- deterministic RF-only recovery;
- exact broker-restart recovery when only an upper bound is preserved;
- pooled FIT+POWDER inference;
- historical firstness for persistence/store-and-forward/layered recovery;
- field, agronomic, pump, hydraulic, groundwater, rural, crop, or industrial-process validation.

Historical scored state remains:
`B1=NULL_ABORTED_AFTER_Q3`
`HISTORICAL_B1=CONSUMED`
`SCORED_P7B_STATUS=UNCHANGED_NOT_PASSED`

## Current Elsevier readiness

Checked 2026-08-30 against current official Elsevier author resources and the current *Internet of Things* journal scope:
- Full Research Papers remain in scope;
- reliability is explicitly within the journal's IoT research interests;
- highlights rule: 3–5 bullets, <=85 characters, Word file — **PASS**;
- graphical abstract: separate optional/encouraged visual asset — **PREPARED**;
- current AI declaration requirements — **MET**;
- data availability — **MET**.

The journal-specific ScienceDirect Guide-for-Authors page returned HTTP 403 to the retrieval environment. Therefore the live submission portal is the final authority for any additional field/file role.

## Exact next action

**Portal preview only; do not submit yet.**

1. Open the Elsevier *Internet of Things* submission flow.
2. Select Full Research Paper.
3. Use `Portal_Metadata.txt` for copy/paste fields.
4. Upload files according to `READ_ME_FIRST.txt`.
5. Preserve Subscription/non-OA unless explicitly changed.
6. Build and inspect the portal-generated PDF and supplementary links.
7. If the portal requires suggested reviewers, stop and prepare a conflict-screened shortlist rather than inventing names.
8. Stop before final irreversible submission, license/copyright acceptance, or any payment unless explicit authority is given.

## Stop state

`R14_CURRENT_MANUSCRIPT_AUTHORITY=YES`
`P4_DOUBLE_RED_HAT=PASS`
`P5_PACKAGE_PREPARATION=PASS`
`P5_EXECUTABLE_RELEASE_GATE=PASS`
`P5_PORTAL_RENDER=NOT_DONE`
`SUBMISSION_AUTHORIZED=NO`
`SUBMISSION_EXECUTED=NO`
`PAYMENT_AUTHORIZED=NO`
`COPYRIGHT_OR_LICENSE_ACCEPTANCE_AUTHORIZED=NO`
`CURRENT_PHASE=P5_PACKAGE_READY_PORTAL_PREVIEW_NEXT`
