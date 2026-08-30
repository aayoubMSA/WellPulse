# WellPulse — Current Handover

**Last updated:** 2026-08-30 after R14/RF9H closure, P5 package preparation, and WP4 double-anonymous live-portal bundle closure.  
**Repository:** `aayoubMSA/WellPulse`  
**Branch:** `main`

This is the canonical operational handover. Do not create a competing current-state document.

## Current state

- **R14 / RF9H: CURRENT MANUSCRIPT AUTHORITY**
- **P4 final Scientific + Editorial Red Hat: PASS**
- **P5 journal-facing package preparation: PASS**
- **WP3 anonymized-manuscript gate: PASS**
- **WP4 double-anonymous live-portal bundle: PASS**
- **WP4 Drive archive + read-back hash: PASS**
- **Portal-generated PDF inspection: NOT YET PERFORMED**
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
- article class: **Full Research Paper**;
- live portal article-type wording: **Full Length Article**;
- default publication model: **Subscription / non-OA**;
- backup: **IEEE Internet of Things Journal** only if rerouting becomes necessary.

Current credited R14 manuscript:
- PDF: `WellPulse_Role_Model_R14_RF9H_Two_Minor_Closure.pdf`
- pages: **28**
- PDF SHA-256: `d5f8006ecc3b0a284c7b5836ba4fee505878efe4003380d8cdbf1454a42b2f3a`
- canonical TeX SHA-256: `18b1c3579ce0e04eb4b0cc3f4c835c4ecb6c9ecdc094acd26fc2f62727b46d98`
- bibliography: **38/38 cited**
- abstract: **227 words**
- keywords: **7**

The credited R14 manuscript remains the scientific authority. The anonymous manuscript below is a portal derivative only.

## Original journal-facing P5 package

Filename:
`WellPulse_Submission_Package_R14_RF9H_2026-08-30.zip`

Original P5 SHA-256:
`62c79223c0bd825250f7dbf92fc9cb51c2e40678285b40d5b5432a4452bd8b33`

A later bounded patch replaced only the cover letter with the signed version. Recorded signed-cover-letter SHA-256:
`d37d3f383bdc30ab498818987b435ae4227396b208ec59e071450ea8d97f0894`

ChatGPT Library durable checkpoint for the original package:
`/My Research Artifacts/WellPulse/WellPulse_Submission_Package_R14_RF9H_2026-08-30.zip`

The P5 package contains the credited manuscript/source, signed cover letter, highlights, deterministic vector graphical abstract, portal metadata, and the credited supplementary materials. The cover letter and graphical abstract remain valid unchanged canonical assets; do not reconstruct them from secondary copies.

### P5 executable release gate

Fresh clean-unpack validation of the credited P5 package passed:

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

## Live-portal double-anonymous requirement

The live Elsevier submission flow exposed the file role **Manuscript without author details** and a separate title-page role. This live portal requirement supersedes the earlier assumption that the credited manuscript PDF could be uploaded directly for initial review.

### Anonymous main manuscript — WP3 PASS

File: `01_Manuscript_Anonymous_R14_RF9H.pdf`  
Pages: **26**  
SHA-256: `39068eb989432f5d7918b1fdf5c8c5227717b4d8af4aef84feca9782e7876b89`

Gate:
- openable, unencrypted, non-scanned: **PASS**;
- 26/26-page final render review: **PASS**;
- fonts embedded: **PASS**;
- 38 bibliography entries retained: **PASS**;
- `Ahmed`, `Ayoub`, `MSA`, `Modern Sciences and Arts`, corresponding email, ORCID, and `WellPulse`: **ZERO HITS** in reviewer-visible text;
- PDF Author metadata: blank;
- author command, affiliation, corresponding-author email, CRediT statement, and acknowledgments removed from the blinded manuscript;
- funding, generic COI, data availability, and Generative-AI declaration retained.

Detailed gate: `WellPulse_WP3_ANONYMIZED_MANUSCRIPT_GATE_R14_2026-08-30.txt` in the durable artifact set.

### Double-anonymous portal bundle — WP4 PASS

Filename:
`WellPulse_IOT_DoubleAnonymous_Portal_Bundle_R14_WP4_2026-08-30.zip`

SHA-256:
`e4c1452771add93b5682c6764285e7f50cd9e2259f46b39676d5ebea0857618d`

Drive archive:
- file ID: `1DUWkRXOtoeX_6YnMvNelH9yVFHsP0zln`;
- parent: `P12_WellPulse` / `1eBQJ8STP-x-MaW0-2m07G7kCoF4UnLft`;
- raw-file read-back SHA-256: exact match / **PASS**.

Bundle upload map:
- `01_Manuscript_Anonymous_R14_RF9H.pdf` — **Manuscript without author details**;
- `02_Title_Page_R14_IOT.docx` — separate author/title page;
- `03_Highlights_R14_IOT.docx` — 5 bullets, all <=85 characters;
- `04_Portal_Metadata_R14_IOT.txt` — live portal copy/paste authority;
- `05_Supplement_S1_Literature_Novelty_Audit_ANONYMOUS.pdf` — anonymous reviewer supplement;
- `06_Supplement_S2_Reproducibility_Artifact_ANONYMOUS.zip` — anonymous exercisable artifact;
- `README_FIRST.txt`, `SHA256SUMS.txt`, `WP4_ACCEPTANCE_GATE.txt` — control files, not journal upload files unless needed internally.

Anonymous S1:
- pages: **3**;
- SHA-256: `8bea48b978274960258399ec33bb5821ae0a8b062b30cce4e4fe1f7a0eee2925`;
- 36 source/axis groups = 29 peer-reviewed + 1 normative + 6 official technical/platform;
- identity/project-name scan: **ZERO HITS**;
- visual QA: **3/3 PASS**.

Anonymous S2:
- SHA-256: `dc7827e1df1185efb698ba701ea900f3b2d73c75c21ea1ee7738ed9efd18b589`;
- ZIP integrity: **PASS**;
- `artifact_selfcheck.py`: **PASS**;
- filenames/text/code identity/project-name scan: **ZERO HITS**.

WP4 closure record:
`docs/WP4_DOUBLE_ANONYMOUS_PORTAL_BUNDLE_CLOSURE_2026-08-30.md`

## Figure-production authority

R13/RF9G permanently fixed the figure-compression failure mode:

- Figure 1 is native TikZ at manuscript width;
- Figures 2–4 are vector PDFs generated at the final 390-pt production width;
- rule: **redesign / split / reflow — never shrink-to-fit**;
- any venue/layout change requires fresh width/font preflight.

The anonymous derivative preserves the frozen values, labels, endpoint semantics, and captions. It does not introduce a scientific-figure change.

The existing Research Operating Doctrine v2.2 remains strengthened in place with this rule.

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

Current official Elsevier resources and the live portal establish the working submission state:
- the paper remains within *Internet of Things* scope;
- live article-type wording is **Full Length Article**;
- main initial-review file role is **Manuscript without author details**;
- a separate title page carries the author identity;
- highlights: 3–5 bullets, <=85 characters — **PASS**;
- graphical abstract: separate optional/encouraged asset — canonical P5 vector asset already prepared;
- current AI declaration requirements — **MET**;
- data availability — **MET**.

The live portal is the final authority for additional upload fields/file roles.

## Exact next action

**Resume at the live Elsevier portal preview only; do not submit yet.**

1. Select **Full Length Article**.
2. Upload `01_Manuscript_Anonymous_R14_RF9H.pdf` as **Manuscript without author details**.
3. Upload `02_Title_Page_R14_IOT.docx` as the separate title page.
4. Upload `03_Highlights_R14_IOT.docx`.
5. Upload anonymous S1 and S2 under the portal's supplementary-material roles.
6. Use `04_Portal_Metadata_R14_IOT.txt` for copy/paste fields.
7. If the portal exposes cover-letter or graphical-abstract roles, use the unchanged canonical P5 signed cover letter and graphical abstract.
8. Preserve **Subscription / non-OA** unless explicitly changed by the author.
9. Build and inspect the portal-generated PDF, file roles, and supplementary links.
10. Check author identity on the title page/metadata, equations, references, Tables 1–3, Figures 1–4, and supplementary links.
11. If suggested reviewers are mandatory, **STOP** and prepare a conflict-screened shortlist; do not invent names.
12. Stop before final irreversible Submit, copyright/license acceptance, or payment unless explicit author authority is given.

## Stop state

`R14_CURRENT_MANUSCRIPT_AUTHORITY=YES`
`P4_DOUBLE_RED_HAT=PASS`
`P5_PACKAGE_PREPARATION=PASS`
`P5_EXECUTABLE_RELEASE_GATE=PASS`
`WP3_ANONYMIZED_MANUSCRIPT=PASS`
`WP4_DOUBLE_ANONYMOUS_PORTAL_BUNDLE=PASS`
`WP4_DRIVE_ARCHIVE=PASS`
`WP4_DRIVE_READBACK_HASH=PASS`
`P5_PORTAL_RENDER=NOT_DONE`
`SUBMISSION_AUTHORIZED=NO`
`SUBMISSION_EXECUTED=NO`
`PAYMENT_AUTHORIZED=NO`
`COPYRIGHT_OR_LICENSE_ACCEPTANCE_AUTHORIZED=NO`
`CURRENT_PHASE=P5_DOUBLE_ANONYMOUS_BUNDLE_READY_PORTAL_RENDER_NEXT`
