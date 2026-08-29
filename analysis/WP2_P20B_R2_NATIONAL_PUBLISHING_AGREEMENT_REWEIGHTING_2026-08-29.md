# WP2-P20B-R2 — National Publishing Agreement Reweighting

Date: 2026-08-29  
Repository: `aayoubMSA/WellPulse`  
Branch: `main`  
Status: **COMPLETE / COST-AND-AGREEMENT REWEIGHTING / SCIENCE UNCHANGED**

## Trigger

The author recalled national publisher agreements available to Egyptian universities through the Supreme Council of Universities / Egyptian Knowledge Bank ecosystem. This is a material venue-selection variable because a valid read-and-publish / transformative agreement can remove or substantially reduce APC exposure and alter the utility ranking between otherwise comparable venues.

P20B-R2 therefore reweights the publisher-neutral P20B-R1 ranking using only currently verifiable national/institutional publishing-agreement evidence. It does not change any scientific claim, experiment, figure, table, author, affiliation, funding statement, rights statement, or submission state.

## Verified national agreement — Springer Nature / STDF / EKB

Current official Springer Nature guidance confirms a transformative plus fully open-access agreement between Springer Nature and the Science, Technology & Innovation Funding Authority (STDF) in cooperation with the Egyptian Knowledge Bank (EKB).

Verified properties as of 2026-08-29:

- the agreement runs through **31 December 2029**;
- more than 150 Egyptian institutions participate;
- **October University for Modern Sciences and Arts** is explicitly listed as a participating institution;
- eligible corresponding authors at participating Egyptian institutions may publish OA with fees covered, subject to STDF/EKB eligibility review and approval;
- eligible article types include Original Paper, Review Paper, Brief Communication and Continuing Education;
- the author must identify the participating Egyptian institution as primary affiliation and be the corresponding author;
- the majority of the research must be carried out at a participating Egyptian institution;
- both hybrid and fully OA Springer Nature routes are covered according to the detailed institution/journal-family matrix, with family-specific exceptions;
- Scientific Reports is explicitly included in the Egypt OA agreement information;
- approval is handled after editorial acceptance; funding is **not** to be presumed before formal eligibility confirmation.

Operational proof that the agreement is active for MSA exists in recent Springer Nature publications by MSA-affiliated authors carrying the statement that open-access funding was provided by STDF in cooperation with EKB, including 2025–2026 papers in Scientific Reports, AAPS PharmSciTech, BMC Chemistry and Clinical Oral Investigations.

Therefore:

`MSA_SPRINGER_NATURE_NATIONAL_OA_AGREEMENT=VERIFIED_ACTIVE`

`AGREEMENT_END_DATE=2029-12-31`

`MSA_INSTITUTION_ELIGIBILITY=VERIFIED_LISTED`

`ARTICLE_LEVEL_FUNDING=SUBJECT_TO_STDF_EKB_APPROVAL_AFTER_ACCEPTANCE`

## Other publisher agreements

### Taylor & Francis / EKB

Current Taylor & Francis MENA guidance explicitly lists **Egyptian Knowledge Bank** under its Middle East & North Africa open-access agreements.

However, the publicly accessible evidence reviewed during R2 did not expose a sufficiently specific institution-by-journal eligibility table or APC-coverage rule for MSA comparable to the Springer Nature evidence.

Therefore:

`TAYLOR_FRANCIS_EKB_OA_AGREEMENT_EXISTENCE=VERIFIED`

`TAYLOR_FRANCIS_MSA_ARTICLE_LEVEL_COVERAGE=UNRESOLVED_REQUIRES_DIRECT_EKB_TF_CHECK`

No T&F venue is promoted solely because the agreement exists.

### Elsevier / EKB

A current Elsevier–EKB partnership is verified for access/research tools, including Scopus AI, ScienceDirect AI and related services. No current publisher-level evidence was recovered establishing a national Egyptian transformative agreement that guarantees APC-free publication across Elsevier journals.

Therefore:

`ELSEVIER_EKB_ACCESS_PARTNERSHIP=VERIFIED`

`ELSEVIER_NATIONAL_APC_FREE_PUBLISHING_FOR_MSA=NOT_VERIFIED`

### IEEE

No current evidence was recovered for a national SCU/EKB agreement that guarantees APC-free IEEE publication for MSA. IEEE remains viable through traditional non-OA publication where allowed, but journal-specific mandatory overlength charges remain a separate economic risk.

Therefore:

`IEEE_MSA_NATIONAL_APC_WAIVER=NOT_VERIFIED`

Do not interpret an IEEE subscription/access arrangement as a publication-fee waiver.

## Agreement-aware venue reweighting

The agreement changes the economic dimension but must not override scientific/editorial fit.

### Route A — strongest specialist target

**IEEE Internet of Things Journal** remains the preferred specialist target because its domain fit, readership and prestige are stronger than the currently identified Springer alternatives.

Economic position:

- traditional publication can avoid an OA APC;
- mandatory overlength charges may still apply depending on final IEEE formatted length;
- P20D must run a page-count simulation before venue commitment.

### Route B — strongest zero-APC / broad-validity route

**Scientific Reports** is materially upgraded.

Reasons:

- Nature Portfolio engineering scope is active;
- the journal evaluates technical validity/robustness rather than subjective perceived significance;
- official guidance aims for first decisions within about 45 days;
- a directly relevant MQTT experimental paper was published on 17 August 2026;
- MSA is explicitly eligible under the STDF/EKB Springer Nature agreement;
- Scientific Reports is explicitly covered by the agreement;
- prior MSA papers demonstrate real operation of the funding mechanism.

This creates a defensible high-value route when optimization emphasizes:

**acceptance plausibility × legitimacy × speed × zero author APC × package reuse**.

### Route C — strongest specialist Springer route

**Telecommunication Systems (Springer Nature)** is promoted as the best currently identified Springer specialist candidate.

Fit reasons:

- covers modeling, analysis, design and management of telecommunication systems;
- explicitly includes performance evaluation, networking protocols, reliability and availability;
- recent 2025–2026 publications include IoT, resilience, survivability and LPWAN work;
- as a Springer hybrid journal, the national agreement can materially reduce APC exposure if the article passes eligibility approval.

Its editorial/readership fit is still less directly centered on IoT resilience than IEEE IoT-J or Elsevier Internet of Things.

### Journal of Network and Systems Management

The Springer Nature agreement improves its economics, and recent MQTT-SN real-hardware work demonstrates technical proximity. However, its official scope explicitly requires a network/systems **management** emphasis. WellPulse is broader resilience/evidence work rather than a management solution paper.

Therefore it remains conditional and should not be artificially reframed merely to exploit free OA.

## Corrected multi-objective ranking

| Role | Venue | Publisher | Agreement/economic state | Decision |
|---|---|---|---|---|
| **Specialist primary** | **IEEE Internet of Things Journal** | IEEE | Traditional route avoids OA APC; page-charge risk remains | **GO / PRIMARY SPECIALIST** |
| **Zero-APC broad/fast route** | **Scientific Reports** | Springer Nature | **MSA/STDF/EKB OA coverage verified, approval required** | **GO / CO-PRIMARY ECONOMIC-SPEED ROUTE** |
| **Specialist fallback** | **Internet of Things** | Elsevier | No mandatory OA needed on subscription route; national APC waiver not verified | **GO / BACKUP** |
| **Springer specialist fallback** | **Telecommunication Systems** | Springer Nature | **MSA/STDF/EKB OA coverage applicable subject to approval** | **GO / AGREEMENT-ADVANTAGED BACKUP** |
| Strong science, cost gate | ACM Transactions on Internet of Things | ACM | No MSA national waiver verified | GO / cost gate |
| Network-management conditional | IEEE TNSM | IEEE | Traditional route possible; page-charge risk | CONDITIONAL GO |
| Management-heavy Springer route | Journal of Network and Systems Management | Springer Nature | MSA/STDF/EKB coverage advantage | CONDITIONAL / scope-framing risk |

## Decision doctrine after R2

Do **not** compress the decision into one scalar ranking without stating the objective.

If the objective is **best specialist scholarly home / IEEE visibility**, choose:

`IEEE Internet of Things Journal`.

If the objective is **shortest defensible path with strong legitimacy, high acceptance plausibility, and zero expected APC under verified national coverage**, choose:

`Scientific Reports`, subject to formal STDF/EKB eligibility confirmation after acceptance.

If the objective is **specialist IoT venue with lower formatting distortion and no need to buy OA**, retain:

`Internet of Things (Elsevier)`.

## Guardrails

- National agreements affect economics, not scientific truth.
- Do not select a weaker-scope venue solely because OA is free.
- Do not state that STDF/EKB funding is guaranteed before approval.
- Do not list STDF/EKB as research funding unless that statement is factually required by the publisher's OA funding metadata; distinguish **publication funding** from **research funding**.
- Corresponding-author and primary-affiliation eligibility must be verified during P20C.
- Journal-level inclusion must be rechecked at submission/acceptance because agreement lists can change.
- No license, OA choice, payment, or submission is authorized by P20B-R2.

## Result

`WP2_P20B_R2=COMPLETE_NATIONAL_PUBLISHING_AGREEMENT_REWEIGHTING`

`MSA_SPRINGER_NATURE_OA=VERIFIED_ACTIVE_TO_2029_12_31`

`SPECIALIST_PRIMARY=IEEE_INTERNET_OF_THINGS_JOURNAL`

`ZERO_APC_SPEED_ROUTE=SCIENTIFIC_REPORTS_SPRINGER_NATURE`

`SPECIALIST_BACKUP=ELSEVIER_INTERNET_OF_THINGS`

`SPRINGER_SPECIALIST_BACKUP=TELECOMMUNICATION_SYSTEMS`

`P20B_AUTHOR_COMMITMENT=NO`

`PAYMENT_AUTHORIZED=NO`

`SUBMISSION_AUTHORIZED=NO`
