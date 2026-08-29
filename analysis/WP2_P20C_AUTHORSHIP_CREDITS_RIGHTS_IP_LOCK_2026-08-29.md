# WP2-P20C — Authorship / Credits / Rights / IP-Translation Lock

Date: 2026-08-29
Venue: **IEEE Internet of Things Journal**
Route: **Traditional / non-OA initial route**
Status: **PASS WITH EXPLICIT RELEASE CONDITIONS / NO SUBMISSION**

## 1. Purpose

Freeze manuscript identity, authorship, credits, funding/COI basis, testbed acknowledgments, AI disclosure basis, rights boundaries and pre-publication IP/commercialization state before venue-specific manuscript integration.

P20C does not perform IEEE formatting, copyright-form acceptance, payment, public DOI release or submission.

## 2. Author lock

### Canonical publication identity

**Publication name: Ahmed Ayoub.**

This exact form is mandatory across manuscript bylines, IEEE submission metadata, CRediT, citation metadata, ORCID/Scopus/Google Scholar-facing records, repositories and publication-related correspondence. Expanded variants such as `Ahmed Elsayed Ayoub` or `Ahmed El-Sayed Ayoub` are not permitted in publication-facing metadata unless the author explicitly overrides this rule for a specific legal/administrative form.

### Author list and order

**Sole author:** Ahmed Ayoub.

No second author is currently supported by manuscript/repository evidence.

The active WellPulse graduation-project students, Nadeem Abdelhamid and Mohamed Waleed, are not added to this manuscript because no verified substantial contribution to the frozen FIT/POWDER experiment, analysis or manuscript science has been established in the current publication record. Future work can create future authorship; it does not retroactively create authorship on this frozen study.

`AUTHOR_COUNT=1`

`AUTHOR_ORDER=AHMED_AYOUB`

### Corresponding author

Ahmed Ayoub is the corresponding author.

Repository commit metadata identifies the current MSA email as `aelsayedo@msa.edu.eg`. P20D/P21 must recheck the address immediately before portal submission.

`CORRESPONDING_AUTHOR=AHMED_AYOUB`

## 3. Canonical affiliation

Current official institutional wording supports:

**Computer Systems Engineering Department, Faculty of Engineering, October University for Modern Sciences and Arts (MSA University), 6th of October City, Egypt.**

The author's academic title should not be embedded inside the affiliation line unless the selected IEEE template/portal explicitly requests it.

`AFFILIATION_LOCK=MSA_CSE_ENGINEERING`

## 4. CRediT contribution lock

For the sole-author paper, the current evidence supports the following roles:

- Conceptualization
- Methodology
- Software
- Validation
- Formal analysis
- Investigation
- Data curation
- Visualization
- Writing — original draft
- Writing — review & editing
- Project administration

Not claimed without separate evidence:

- Funding acquisition
- Resources as personal ownership of FIT/POWDER infrastructure

`CREDIT_ROLES=LOCKED`

## 5. Research funding and publication funding

Author decision/current record: **no external research funding** for the WellPulse study.

Submission-facing research-funding statement:

> This research received no external funding.

This is separate from publication-fee support. The selected IEEE Traditional route currently requires no OA APC. No SCU/EKB/STDF publication-payment claim applies to the selected route.

If the route later changes to a covered Springer Nature OA venue, publication-fee support must be recorded separately and must never be described as funding the research itself.

`RESEARCH_FUNDING=NO_EXTERNAL_FUNDING`

`PUBLICATION_FUNDING=NONE_FOR_SELECTED_TRADITIONAL_IEEE_ROUTE`

## 6. Competing interests

Author decision/current record: **no competing interests identified**.

Submission-facing basis:

> The author declares no competing interests.

This statement must be rechecked at P21 in case a commercial partnership, patent filing, licence negotiation or financial interest arises before submission.

`COI=CURRENTLY_NONE`

## 7. Testbed and institutional acknowledgments

### FIT IoT-LAB — mandatory acknowledgment

Current FIT IoT-LAB terms require publications based on its experiments to:

1. acknowledge FIT IoT-LAB in the publication;
2. cite the FIT IoT-LAB reference paper;
3. notify the platform after acceptance.

The manuscript already cites the reference article as [8]. An explicit acknowledgment must be added during P20D.

### POWDER

Current POWDER guidance asks publications using the facility to name POWDER in the text and cite its reference article. The manuscript does both and cites Breen et al. as [10]. An acknowledgment is recommended for clarity but no unverified funder/grant number will be invented.

### Frozen acknowledgment basis

P20D should include a concise statement such as:

> The author acknowledges FIT IoT-LAB for access to its experimental IoT infrastructure and POWDER for access to its wireless experimentation platform.

Do not acknowledge or attribute funding to FIT, POWDER, NSF, STDF, EKB, MSA, students or collaborators unless the specific basis is independently verified.

`FIT_ACK_REQUIRED=YES`

`POWDER_CITATION_REQUIRED=YES`

## 8. AI disclosure basis for IEEE

Current IEEE policy requires disclosure in the acknowledgments section when AI-generated content is used in an article; grammar/editing-only assistance is generally outside the mandatory disclosure intent but disclosure is recommended.

The manuscript-development record includes substantive generative-AI assistance during drafting/editorial preparation. Therefore a disclosure is required; omission would not be compliant with the current IEEE policy.

Minimum compliant P20D disclosure basis:

> OpenAI ChatGPT was used during manuscript preparation to assist with editorial drafting and language refinement across selected textual sections. All scientific analyses, numerical results, claims, citations, and final wording were reviewed and approved by the author, who takes full responsibility for the content.

P20D should preserve this as concise as policy allows and must not imply that AI is an author.

`IEEE_AI_DISCLOSURE=REQUIRED`

## 9. Figure/data/software rights

### Figures

P18RC main figures are project-generated from the WellPulse evidence pipeline. No externally reproduced third-party figure has been identified in the current main display.

`THIRD_PARTY_FIGURE_PERMISSION_REQUIRED=NO_IDENTIFIED`

### Data / testbed evidence

FIT and POWDER evidence is experimental output generated through authorized testbed use. Publication must preserve the existing privacy/security sanitization from P19. Testbed platform source papers are cited; infrastructure ownership is not claimed.

### Software / repository

The GitHub repository `aayoubMSA/WellPulse` is currently **public**. `CITATION.cff` currently names Ahmed Ayoub as the software author and says publication-ready citation metadata will be finalized later.

No root `LICENSE` file is currently present. A prior author decision favored MIT licensing for original WellPulse code only, with third-party material handled separately, but institutional/student ownership authority has not been independently established in the current P20C record.

Therefore:

- do **not** add a public software licence during P20C;
- do **not** represent the repository as MIT-licensed until authority to license the relevant code is verified;
- third-party code/data/testbed infrastructure retains its own rights;
- IEEE article copyright does not itself create a software licence for the repository.

`SOFTWARE_LICENSE_DECISION=MIT_INTENT_RECORDED`

`SOFTWARE_LICENSE_ACTIVATED=NO`

`LICENSE_RELEASE_CONDITION=VERIFY_AUTHORITY_TO_LICENSE_ORIGINAL_CODE`

## 10. Pre-publication IP / commercialization screen

### Public-disclosure state

The WellPulse GitHub repository is already public. Public code/docs therefore constitute prior public disclosure of at least some software/architecture material. P20C does not attempt a legal patentability opinion and does not assume that patent novelty remains available in any jurisdiction.

`PRIOR_PUBLIC_DISCLOSURE=YES`

`PATENTABILITY=NOT_ASSESSED_NO_CLAIM`

### Ownership

Formal institutional/student IP ownership or assignment rules have not been independently verified in the current record.

`IP_OWNERSHIP=UNRESOLVED_FOR_NEW_PROTECTIVE_ACTION`

### Commercial demand

No validated customer, licensee, investor, commercial partner or revenue evidence is currently established.

`COMMERCIAL_DEMAND=UNVALIDATED`

### Finite commercialization verdict

Because public disclosure already exists, no unverified patent-right claim should delay publication. The current bounded verdict is:

**`NO_IP_ACTION -> PUBLISH`**

This does not prohibit future:

- industrial partnership;
- implementation services;
- sponsored validation;
- standards engagement;
- licensing of rights the author/institution actually controls;
- a future patent on genuinely new, undisclosed subject matter after proper ownership/legal review.

It only means the current paper will not be held while assuming patent protection that has not been established.

## 11. IEEE route rights boundary

Current IoT-J policy states:

- Traditional publication has no OA APC;
- IEEE requires its copyright form before publication;
- mandatory overlength charges apply beyond the first 8 published pages;
- author is responsible for prior consent/permissions required for disclosure.

P20C does not authorize copyright-form acceptance. It verifies that no identified third-party figure permission or patent hold currently prevents manuscript integration.

`IEEE_COPYRIGHT_FORM=NOT_AUTHORIZED_YET`

`IEEE_OVERLENGTH_PAYMENT=NOT_AUTHORIZED`

## 12. Acceptance gate

- exact publication name: **PASS — Ahmed Ayoub**
- exact author list/order: **PASS**
- corresponding author: **PASS**
- affiliation: **PASS**
- CRediT: **PASS**
- research funding basis: **PASS**
- COI basis: **PASS**
- FIT/POWDER acknowledgment/citation obligations: **PASS / P20D insertion required**
- AI disclosure basis: **PASS / P20D insertion required**
- third-party figure rights: **PASS / none identified**
- software licence state: **CONTROLLED / no licence activated**
- IP screen: **PASS / prior public disclosure exists / no patent hold**
- commercialization verdict: **NO_IP_ACTION -> PUBLISH**
- payment authorized: **NO**
- copyright form authorized: **NO**
- submission authorized: **NO**

`WP2_P20C=PASS_AUTHORSHIP_CREDITS_RIGHTS_IP_LOCK`

`PUBLICATION_NAME=AHMED_AYOUB`

`P20D_UNLOCKED=YES`

`SUBMISSION_AUTHORIZED=NO`
