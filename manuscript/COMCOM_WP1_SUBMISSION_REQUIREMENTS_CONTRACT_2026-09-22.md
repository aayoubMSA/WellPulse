# WellPulse → Computer Communications — WP1 Submission Requirements Contract

**Date:** 2026-09-22  
**Target:** Computer Communications (Elsevier)  
**Article type:** Research Article  
**Scientific authority:** R7g / R7f-R4 final manuscript  
**Submission action in WP1:** NONE  
**Scientific-content edits in WP1:** NONE

## 1. Governing decision

The R7g scientific source remains frozen:

`manuscript/revival_2026-09-22/WellPulse_Revival_R7fR4_EvidencePresentation_20260922.tex`

Accepted source SHA-256:

`14c29c0d693bc696ae042b291b0528ab68c62ebfdb91e7c4d461bce8f05756eb`

Current source metadata:
- abstract = 174 words;
- keywords = 7;
- Acknowledgment present;
- Funding present;
- Conflict of Interest present;
- Reproducibility and Data Availability section present;
- Generative-AI declaration absent;
- CRediT statement absent.

## 2. Current official venue/scope authority

Computer Communications currently states that it publishes scientific articles covering future computer communication networks, with topics including:
- Internet of Things;
- experimental test-beds and research platforms;
- future Internet architecture, protocols and services;
- modeling, measurement, and simulation of computer communication networks.

This remains consistent with the R8 venue decision.

## 3. Highest-ROI submission-format decision

**Do not perform a wholesale IEEEtran→Elsevier rewrite merely for initial submission unless the live journal guide or portal explicitly requires it.**

Current Elsevier author guidance states that most new submissions may be supplied as a single review-ready PDF/Word file under the Your Paper Your Way workflow, while editable source is required for production/revision. Elsevier recommends `elsarticle.cls` for LaTeX but does not make template conversion universally mandatory at initial submission.

Therefore the package program is:

1. preserve the frozen R7g PDF as the review manuscript unless Computer Communications explicitly rejects that layout;
2. separately prepare an Elsevier-safe flattened LaTeX source archive;
3. only convert the full manuscript to `elsarticle` if the Computer Communications portal/Guide for Authors makes this mandatory.

This avoids unnecessary scientific/layout churn before submission.

## 4. Confirmed Elsevier submission requirements relevant to this paper

### 4.1 LaTeX / Editorial Manager
Elsevier current LaTeX guidance:
- a compiled manuscript PDF can be uploaded as the Manuscript when PDF submission is allowed;
- source files can be bundled as a single archive under the LaTeX/source-file item type when requested;
- Editorial Manager LaTeX source must not depend on subfolders;
- figures, bibliography/style/class material required by the source must be available at one folder level when source compilation is requested.

Package consequence:
**the sanitized supplement may remain a separate supplementary file, but the manuscript LaTeX compilation bundle must be flat.**

### 4.2 Highlights
Elsevier's current Highlights standard:
- 3–5 bullet points;
- each bullet ≤85 characters including spaces;
- supplied as a separate editable file when requested.

Computer Communications current published articles display Highlights, and current third-party journal templates identify Highlights as expected.

Package consequence:
**prepare a 3–5 bullet Highlights file now.**

### 4.3 Data availability / research data
Elsevier supports integrated Data Availability Statements and encourages transparent disclosure of availability or restrictions.

Computer Communications 2026 papers routinely contain a Data availability section.

Package consequence:
**prepare a standalone portal-ready Data Availability Statement in addition to the manuscript's Reproducibility and Data Availability section.**

### 4.4 Competing interests
The current manuscript already contains the standard no-competing-interest statement.

Package consequence:
**retain the existing statement exactly unless the portal requires a separate declaration file/form.**

### 4.5 Funding
The current manuscript states:
`This work received no external research funding.`

Package consequence:
**retain unchanged unless the portal requires entry in a separate funding field.**

### 4.6 Author metadata
Frozen authority:
- Ahmed Ayoub
- Computer Systems Engineering Department, Faculty of Engineering
- October University for Modern Sciences and Arts (MSA University)
- 6th of October City, 12451, Egypt
- aelsayedo@msa.edu.eg
- ORCID 0009-0004-7895-3191

Package consequence:
**reuse exactly.**

## 5. Mandatory 2026 Elsevier AI-disclosure delta

Elsevier's updated August 2026 journal policy requires disclosure when generative AI or AI-assisted tools made substantive changes to manuscript wording, sentence structure, organization, literature synthesis, or similar preparation tasks. Grammar/spelling-only use is exempt.

This revival used OpenAI ChatGPT substantially for literature organization, claim-boundary review, manuscript restructuring, language refinement, and consistency checking.

Therefore a new declaration is mandatory before the references.

Frozen proposed disclosure text for the next package WP:

**Declaration of generative AI and AI-assisted technologies in the manuscript preparation process**

During the preparation of this work, the author used OpenAI ChatGPT to assist with literature organization, manuscript structuring, language refinement, and consistency checking. The author independently reviewed and verified the scientific claims, source records, calculations, experimental evidence, and citations, edited the content as needed, and takes full responsibility for the content of the publication.

This is an editorial/transparency addition; it does not change the scientific claims or evidence.

## 6. CRediT authorship statement

Recent Computer Communications papers routinely publish a CRediT authorship contribution statement. Elsevier generally encourages CRediT transparency.

Because this is a single-author manuscript, a CRediT statement should be prepared, but **roles must not be invented**.

Status:
`CREDIT_EXACT_ROLES=UNRESOLVED_FROM_CURRENT_AUTHORITY`

Next-package rule:
- recover the exact author-role authority from the WellPulse project record if available;
- otherwise stop for author confirmation before asserting roles such as Software, Data curation, Resources, or Supervision.

## 7. Graphical abstract

Elsevier provides current graphical-abstract specifications, and recent Computer Communications papers often include graphical abstracts. However, the journal-specific Guide for Authors could not be directly retrieved in this WP, so mandatory status is not established.

Status:
`GRAPHICAL_ABSTRACT_REQUIREMENT=PORTAL_DEPENDENT`

Rule:
- do not generate one merely speculatively;
- if the live portal marks it mandatory, derive it mechanically from the already validated recovery-observable/vector evidence;
- do not introduce any new scientific relationship or imply M2>M3.

## 8. Cover letter

A concise journal-specific cover letter should be prepared.

Required positioning:
- experimental network/IoT measurement study;
- measurement semantics and evidence adjudication;
- FIT IoT-LAB + POWDER experimental platforms;
- prospective negative/unresolved endpoint result retained;
- no new MQTT architecture claim;
- no universal durability/freshness claim;
- fit to Computer Communications' experimental test-bed and network-measurement scope.

No claim of editor preference, novelty firstness, or guaranteed fit is allowed.

## 9. Public/supplementary reproducibility pointer

Current sanitized supplement:
`manuscript/revival_2026-09-22/supplement_r7fr3/`

Current R7g package already preserves:
- sanitized execution configuration;
- exact code-authority manifest;
- clock-bound procedure;
- private-data boundary;
- deterministic self-check.

Before submission, one of the following must be frozen:
1. a public GitHub tag/release pointing to sanitized reproduction materials; or
2. a DOI-backed public archive; or
3. an explicit Data Availability Statement explaining what is public and what protected raw evidence can only be shared under access constraints.

No repository/DOI identifier may be invented.

## 10. Reference-format decision

Elsevier's current Your Paper Your Way guidance does not require strict journal reference formatting at initial submission as long as references are complete and consistent.

The current 14-reference bibliography has passed:
- 14 unique keys;
- all citations resolved;
- 13/13 DOI-bearing references independently matched;
- 0 retractions;
- OASIS MQTT v5 retained as the non-DOI standard.

Decision:
**do not spend another WP on cosmetic reference reformatting before portal evidence requires it.**

## 11. Portal-dependent items to resolve only at live submission

Do not guess these before opening the Computer Communications submission workflow:
- exact file-item labels;
- whether source is mandatory at first submission;
- whether graphical abstract is mandatory;
- exact reviewer-suggestion count;
- any mandatory classification/topic selections;
- any live data-policy option;
- open-access/APC choice;
- copyright/licence terms;
- optional transfer-service consent.

Any APC, open-access, copyright/licence, payment, or irreversible publication commitment requires author confirmation.

## 12. Submission package contract

Prepare in the next package WP:

1. `WellPulse_COMCOM_Manuscript.pdf` — frozen science plus required editorial declarations only.
2. `WellPulse_COMCOM_LaTeX_Source.zip` — flat, compilable source bundle.
3. `WellPulse_COMCOM_Highlights.txt` — 3–5 bullets, each ≤85 chars.
4. `WellPulse_COMCOM_Cover_Letter.pdf` or editable source.
5. `WellPulse_COMCOM_Reproducibility_Supplement.zip` — sanitized R7f-R3 materials.
6. `WellPulse_COMCOM_Data_Availability.txt` — portal-ready statement.
7. `WellPulse_COMCOM_CRediT.txt` — only after exact role authority is recovered/confirmed.
8. Graphical abstract — only if the live portal/guide confirms it is required.

## 13. Gate

`COMCOM_WP1_CURRENT_REQUIREMENTS=PASS`

`COMCOM_WP1_HIGHEST_ROI_FORMAT_DECISION=KEEP_REVIEW_PDF_UNLESS_PORTAL_REQUIRES_TEMPLATE`

`COMCOM_WP1_AI_DISCLOSURE_REQUIRED=YES`

`COMCOM_WP1_CREDIT_ROLES=UNRESOLVED`

`COMCOM_WP1_GRAPHICAL_ABSTRACT=PORTAL_DEPENDENT`

`COMCOM_WP1_SUBMISSION_EXECUTED=NO`

`NEXT=COMCOM_WP2_PACKAGE_ASSEMBLY_AND_EDITORIAL_DECLARATIONS`
