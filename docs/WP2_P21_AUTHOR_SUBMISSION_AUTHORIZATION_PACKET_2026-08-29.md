# WP2-P21 — Author Submission Authorization Packet

Date: 2026-08-29
Status: **PACKET READY / AUTHOR DECISION REQUIRED / NO SUBMISSION**

Target venue: **IEEE Internet of Things Journal**  
Selected route: **Traditional / non-OA**  
Publication name: **Ahmed Ayoub**

## Purpose

This is the final internal authorization packet before any external submission action. It does not submit the manuscript, accept IEEE copyright terms, or authorize payment.

P20E has independently validated the exact P20D-R1 package with zero scientific or production blockers.

## 1. Exact validated submission authority

Current archival/source authority:

`WellPulse_P20D_R1_IEEE_Submission_Package_2026-08-29.zip`

- Drive ID: `1j61flpHqrVlR_c-Hu1ueUjl5p2RQwhGG`
- Size: `3,601,271 bytes`
- Archive SHA-256: `73b46d0b19cfd74689bdc10efb27c71a5460ca1c9ab6843503155a87696eb73c`
- Drive raw read-back: exact match / PASS

Main manuscript:

`WellPulse_IEEE_IoTJ_P20D_R1_SubmissionDraft.pdf`

- SHA-256: `95917105f9d03fce155b9cc2a579d2e0e6f567a30557f87f82382db193597fa1`
- IEEEtran author build: **6 pages**
- Abstract: **221 words**
- Publication name: **Ahmed Ayoub**

Source TeX:

`source/wellpulse_ieee_iotj_p20d.tex`

- SHA-256: `0e0c64ba0552f2e71e8a00e4cc29a35da908b7f0996a5a94db34e36d2ef644ef`

Reviewer/supplement package:

`supplement/WellPulse_P19_SUBMISSION_SAFE_R1.zip`

- SHA-256: `99ed7c4dfc42c1f0f4b659489abf7ad328584f413c0318210dace29b4912b48d`

## 2. Publication identity / portal metadata

Author:
**Ahmed Ayoub**

Corresponding author:
**Ahmed Ayoub**

Affiliation:
**Computer Systems Engineering Department, Faculty of Engineering, October University for Modern Sciences and Arts (MSA University), 6th of October City 12451, Egypt**

Institutional email expected for submission:
`aelsayedo@msa.edu.eg`

Canonical ORCID held in the Research & Grants profile:
`0009-0004-7895-3191`

IEEE IoT-J currently requires ORCID for every author. The exact ORCID must be confirmed as linked to the IEEE Author Portal account before P22 submits.

`ORCID_EXPECTED=0009-0004-7895-3191`

`IEEE_PORTAL_ORCID_LINKAGE=VERIFY_AT_P22_LOGIN`

## 3. Authorship / disclosure metadata

- Author count: 1.
- Research funding: **This work received no external research funding.**
- Competing interests: **none currently identified**.
- FIT IoT-LAB acknowledgment/citation: present.
- POWDER acknowledgment/citation: present.
- CRediT roles: present.
- IEEE generative-AI disclosure: present in `Acknowledgment`.
- Patent/IP hold: none established; current verdict remains `NO_IP_ACTION -> PUBLISH`.
- Repository software licence: not activated; not required for article submission.

## 4. Concurrent-submission gate

Current IEEE IoT-J guidance requires original/substantial work not currently under consideration elsewhere and prohibits multiple submission.

P21 evidence check:

- canonical WellPulse repository contains no submission-receipt state;
- Gmail search for WellPulse/title terms plus `IEEE IoT-J`, `Internet of Things Journal`, `Manuscript Central`, and `ScholarOne` returned **no journal-submission record**;
- existing WellPulse mail concerns student GP work, GitHub/testbed operations, and experiment infrastructure, not manuscript submission.

Therefore:

`CONCURRENT_SUBMISSION_EVIDENCE_FOUND=NO`

Because absence of an email cannot prove absence of every possible external portal action, the author must confirm at authorization time:

> I confirm that this WellPulse manuscript is not currently under consideration at another journal or conference.

## 5. Route / financial condition

Selected route:

**Traditional / non-OA**

Current IoT-J guidance states:

- no OA fee is required for Traditional submission;
- mandatory overlength charge = **USD 175 per published page beyond the first eight pages**;
- submission of the manuscript signifies acceptance of that mandatory page-charge requirement.

The independently validated author build is **6 pages**, providing two pages of author-build headroom, but final IEEE production pagination can change.

No page-charge payment has been authorized or incurred.

Authorization therefore requires explicit awareness of this residual condition:

> I understand that IEEE IoT-J states that submission signifies acceptance of mandatory overlength charges if the final published article exceeds eight pages, even though the current validated author build is six pages.

`OVERLENGTH_PAYMENT_AUTHORIZED_NOW=NO`

## 6. Portal upload map

The outer P20D-R1 ZIP is an **archival authority**, not a single submission upload.

### Primary manuscript

Upload as main manuscript:

`WellPulse_IEEE_IoTJ_P20D_R1_SubmissionDraft.pdf`

### Supplementary material

Upload and label separately as supplementary/reviewer material:

`WellPulse_P19_SUBMISSION_SAFE_R1.zip`

The supplement includes its IEEE-complete `SUPPLEMENT_README.txt`, experiment atlas, sanitized derived data, reproducibility code, privacy/security notes, alt text, manifests, and self-check.

### Source / production files

Retain for portal requests and downstream production:

- `source/wellpulse_ieee_iotj_p20d.tex`
- `figures/Figure01_system_evidence_architecture.pdf`
- `figures/Figure02_FIT_effect_and_recovery_cost.pdf`
- `figures/Figure03_POWDER_transition_and_repeatability.pdf`
- `figures/Figure04_failure_domain_and_recovery_semantics.pdf`
- `figures/ALT_TEXT.md`

If IEEE requests separate source/graphics at initial submission, P22 may upload byte-identical or format-compatible copies without changing scientific content. The exact portal UI determines the final file-role labels.

### Graphical abstract

Not required for submission readiness; none is authorized/needed.

## 7. P20E assurance summary

Independent P20E PASS established:

- science blockers: 0;
- production blockers: 0;
- 6-page independent rebuild;
- 0 changed pages / 0.0% rendered-pixel difference between packaged PDF and independent rebuild;
- all fonts embedded;
- manifests and SHA lists valid;
- P19 isolated self-check PASS;
- no cache files;
- publication-name consistency PASS;
- privacy/security scans PASS;
- key FIT and POWDER values independently recomputed and matched;
- P20A novelty boundaries preserved;
- forbidden claim families absent.

## 8. Downstream copyright control

IEEE copyright-form acceptance is a separate post-acceptance/pre-publication action. P21 does not authorize it.

`COPYRIGHT_ACCEPTANCE_AUTHORIZED=NO`

## 9. Author decision gate

To unlock P22, the author must explicitly authorize submission while confirming the two statements below:

1. **Concurrent-submission confirmation** — the WellPulse manuscript is not under consideration elsewhere.
2. **IoT-J page-charge awareness** — submission signifies acceptance of the mandatory overlength rule if the final published article exceeds eight pages.

The requested decision is:

`AUTHORIZE_SUBMISSION=YES`

or

`AUTHORIZE_SUBMISSION=NO`

Until the author explicitly chooses YES:

`P22_LOCKED=YES`

`SUBMISSION_AUTHORIZED=NO`

## P21 state

`WP2_P21=PASS_PACKET_READY_AUTHOR_DECISION_PENDING`

`PUBLICATION_LANE_PROGRESS=95_OF_100`

`P22_LOCKED=YES`

`SUBMISSION_AUTHORIZED=NO`
