# WP4 — Double-Anonymous Live-Portal Bundle Closure

Date: 2026-08-30  
Status: **PASS / DOUBLE-ANONYMOUS PORTAL BUNDLE BUILT / DRIVE READ-BACK VERIFIED / NOT SUBMITTED**

## Trigger

The live *Internet of Things* (Elsevier) submission flow exposed two portal-specific requirements that were not visible from the earlier static author guidance:

- article type wording: **Full Length Article**;
- main file role: **Manuscript without author details**, with a separate title page carrying author information.

This WP4 closure is a bounded submission-engineering derivative only. It does not reopen or change experiments, results, references, figures, inferential boundaries, novelty conclusions, authorship, venue route, or the credited R14/RF9H scientific authority.

## Double-anonymous main manuscript

File: `01_Manuscript_Anonymous_R14_RF9H.pdf`  
Pages: **26**  
SHA-256: `39068eb989432f5d7918b1fdf5c8c5227717b4d8af4aef84feca9782e7876b89`

Acceptance:

- openable / unencrypted / non-scanned: **PASS**;
- 26/26-page render review: **PASS**;
- fonts embedded: **PASS**;
- 38 bibliography entries retained: **PASS**;
- author/institution/email/ORCID/project-name scan: **ZERO HITS**;
- PDF Author metadata: blank;
- acknowledgments and CRediT removed from the blinded manuscript and retained on the separate title page;
- funding, generic competing-interest statement, data availability, and Generative-AI declaration retained.

Figure production remains scientifically invariant. Figure 1 uses the canonical deterministic TikZ source; Figures 2–4 remain vector reproductions at the frozen publication width using the frozen R14 values, labels, endpoint semantics, and captions.

## Front matter

- `02_Title_Page_R14_IOT.docx`: one-page visual QA **PASS**; author identity, affiliation, ORCID, acknowledgments, CRediT, funding and COI intentionally present.
- `03_Highlights_R14_IOT.docx`: one-page visual QA **PASS**; five substantive bullets, each <=85 characters; identity/project scan **ZERO HITS**.
- `04_Portal_Metadata_R14_IOT.txt`: live portal copy/paste authority for the current upload flow; article type wording = **Full Length Article**.

The previously accepted signed P5 cover letter and deterministic vector graphical abstract are unchanged by this anonymity patch and were not reconstructed from secondary copies. If the live portal presents those upload roles, use their canonical P5 versions. Recorded signed-cover-letter SHA-256: `d37d3f383bdc30ab498818987b435ae4227396b208ec59e071450ea8d97f0894`.

## Anonymous supplementary material

### S1 literature / novelty audit

File: `05_Supplement_S1_Literature_Novelty_Audit_ANONYMOUS.pdf`  
Pages: **3**  
SHA-256: `8bea48b978274960258399ec33bb5821ae0a8b062b30cce4e4fe1f7a0eee2925`

Acceptance:

- 36 source/axis groups: **PASS**;
- 29 peer-reviewed + 1 normative standard + 6 official technical/platform sources: **PASS**;
- wording-narrowing / no-impact / blocker state remains inside frozen R14 novelty envelope;
- visual review 3/3 pages: **PASS**;
- identity/project-name scan: **ZERO HITS**;
- PDF Author metadata blank.

### S2 reproducibility artifact

File: `06_Supplement_S2_Reproducibility_Artifact_ANONYMOUS.zip`  
SHA-256: `dc7827e1df1185efb698ba701ea900f3b2d73c75c21ea1ee7738ed9efd18b589`

Acceptance:

- ZIP integrity: **PASS**;
- standard-library `artifact_selfcheck.py`: **PASS — sanitized artifact scientific invariants and claim envelope verified**;
- filenames + text/code identity/project-name scan: **ZERO HITS**.

## Final portal bundle

File: `WellPulse_IOT_DoubleAnonymous_Portal_Bundle_R14_WP4_2026-08-30.zip`  
SHA-256: `e4c1452771add93b5682c6764285e7f50cd9e2259f46b39676d5ebea0857618d`  
Drive ID: `1DUWkRXOtoeX_6YnMvNelH9yVFHsP0zln`  
Drive parent: `P12_WellPulse` / `1eBQJ8STP-x-MaW0-2m07G7kCoF4UnLft`

Final clean-unpack validation:

- package ZIP integrity: **PASS**;
- internal SHA-256 manifest: **PASS**;
- reviewer-visible manuscript/S1 identity scan: **ZERO HITS**;
- highlights XML identity scan: **ZERO HITS**;
- S2 executable self-check after clean unpack: **PASS**;
- Drive raw-file read-back SHA-256: exact match / **PASS**.

## Authority and stop state

The credited scientific authority remains:

- R14 PDF SHA-256: `d5f8006ecc3b0a284c7b5836ba4fee505878efe4003380d8cdbf1454a42b2f3a`;
- canonical TeX SHA-256: `18b1c3579ce0e04eb4b0cc3f4c835c4ecb6c9ecdc094acd26fc2f62727b46d98`.

No new experiment or scientific claim was introduced.

`WP4_DOUBLE_ANONYMOUS_PORTAL_BUNDLE=PASS`  
`WP4_DRIVE_ARCHIVE=PASS`  
`WP4_DRIVE_READBACK_HASH=PASS`  
`CURRENT_SCIENTIFIC_BLOCKERS=0`  
`NEW_EXPERIMENT_REQUIRED=NO`  
`SCIENTIFIC_CONTENT_CHANGED=NO`  
`PORTAL_GENERATED_PDF_INSPECTION=PENDING`  
`SUBMISSION_AUTHORIZED=NO`  
`SUBMISSION_EXECUTED=NO`  
`PAYMENT_AUTHORIZED=NO`  
`COPYRIGHT_OR_LICENSE_ACCEPTANCE_AUTHORIZED=NO`

## Exact next action

Resume at the live Elsevier portal **preview only**:

1. select **Full Length Article**;
2. upload `01_Manuscript_Anonymous_R14_RF9H.pdf` as **Manuscript without author details**;
3. upload the separate title page, highlights, anonymous S1 and anonymous S2 according to the portal file roles;
4. use `04_Portal_Metadata_R14_IOT.txt` for copy/paste metadata;
5. if cover-letter or graphical-abstract roles appear, use the unchanged canonical P5 versions;
6. build and inspect the portal-generated PDF and supplementary links;
7. if suggested reviewers are mandatory, stop for a conflict-screened shortlist;
8. stop before final Submit, copyright/license acceptance, or payment unless the author explicitly authorizes it.
