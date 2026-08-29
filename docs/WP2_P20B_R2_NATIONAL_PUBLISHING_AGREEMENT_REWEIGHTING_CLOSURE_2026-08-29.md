# WP2-P20B-R2 — National Publishing Agreement Reweighting Closure

Date: 2026-08-29  
Repository: `aayoubMSA/WellPulse`  
Branch: `main`  
Status: **PASS / AGREEMENT-AWARE VENUE AUTHORITY / SCIENCE UNCHANGED**

## Trigger

The author recalled national publisher agreements available through the Egyptian higher-education / EKB ecosystem that can cover open-access publishing charges. This created a new bounded venue-selection risk class: **institutional/national publishing-agreement omission**.

P20B-R2 reopened only the economic/route-weighting portion of P20B-R1.

## Verified finding

A current Springer Nature–STDF–EKB transformative plus fully OA agreement is active through **31 December 2029**.

**October University for Modern Sciences and Arts** is explicitly listed as a participating institution.

For eligible articles, a corresponding author affiliated with the participating Egyptian institution may receive OA publication-fee coverage, subject to STDF/EKB verification and approval after editorial acceptance. The agreement information explicitly includes **Scientific Reports** among covered Springer Nature routes.

Recent 2025–2026 Springer Nature publications by MSA-affiliated researchers provide operational evidence that STDF/EKB publication funding is being applied in practice.

`MSA_SPRINGER_NATURE_AGREEMENT=VERIFIED_ACTIVE`

`AGREEMENT_EXPIRY=2029-12-31`

`ARTICLE_LEVEL_COVERAGE=SUBJECT_TO_APPROVAL`

## Corrected venue strategy

P20B should no longer be represented as one unconditional total order. The correct decision depends on the author's publication objective.

### Best specialist scholarly home

**IEEE Internet of Things Journal** remains the preferred specialist target.

Reason: strongest domain/readership fit and IEEE visibility. No national APC waiver was verified for MSA; traditional publication avoids an OA APC, but final IEEE page count may create mandatory overlength charges.

### Best agreement-advantaged route

**Scientific Reports** is promoted to a co-primary strategic route.

Reason:

- engineering is in scope;
- technical soundness/validity rather than subjective significance drives publication criteria;
- first-decision target is around 45 days in current official guidance;
- a directly relevant MQTT experimental paper was published on 17 August 2026;
- Scientific Reports is covered by the Springer Nature STDF/EKB agreement;
- MSA is explicitly eligible;
- recent MSA publications demonstrate the national OA funding mechanism is operational.

This is the strongest current route if optimization emphasizes:

`acceptance plausibility × legitimacy × speed × zero expected APC × reuse of validated package`.

### Specialist fallback

**Internet of Things (Elsevier)** remains a strong specialist fallback because it is directly in scope and does not require the paper to change scientific identity. A current national Elsevier APC-free publishing agreement for MSA was not verified.

### Agreement-advantaged specialist fallback

**Telecommunication Systems (Springer Nature)** is promoted as the best currently identified Springer specialist fallback because its scope includes performance evaluation, networking protocols, reliability and availability, and it publishes current IoT/resilience work. Its readership fit remains less direct than IEEE IoT-J or Elsevier Internet of Things.

### Journal of Network and Systems Management

Economically attractive under the Springer agreement, but its official scope requires a network/systems management emphasis. It remains conditional; no artificial management framing is permitted solely to obtain free OA.

## Other publisher agreements

Current Taylor & Francis guidance lists Egyptian Knowledge Bank among its MENA open-access agreements. Exact MSA/article/journal coverage was not sufficiently resolved from the accessible public evidence to treat it as a guaranteed APC waiver.

Current Elsevier–EKB partnership evidence confirms access/research-tool collaboration, but not a broad national APC-free publishing guarantee for MSA.

No current public evidence recovered in R2 established a national MSA/SCU/EKB IEEE APC waiver.

## Decision state

**Two legitimate co-primary routes now exist:**

1. `IEEE_INTERNET_OF_THINGS_JOURNAL` — specialist/IEEE route;
2. `SCIENTIFIC_REPORTS` — agreement-advantaged speed/zero-APC route.

The author has **not** selected between these routes yet.

P20C can still proceed venue-neutrally on authorship/credits/rights facts, but no venue-specific rights/license commitment is permitted until author venue choice is made.

## Acceptance gate

- national publisher-agreement check: **PASS**;
- MSA Springer Nature eligibility: **VERIFIED**;
- agreement end date: **2029-12-31**;
- Scientific Reports coverage: **VERIFIED**;
- actual MSA use evidence: **VERIFIED**;
- IEEE national APC waiver: **NOT VERIFIED**;
- Taylor & Francis EKB agreement existence: **VERIFIED / ARTICLE-LEVEL DETAILS UNRESOLVED**;
- science reopened: **NO**;
- new experiment required: **NO**;
- author venue commitment: **NO**;
- payment authorized: **NO**;
- submission authorized: **NO**.

## Authority transition

P20B-R1 remains the publisher-neutral scope authority.

P20B-R2 is the current **agreement-aware economic/route authority** and must be read after R1.

`WP2_P20B_R2=PASS_NATIONAL_PUBLISHING_AGREEMENT_REWEIGHTING`

`CO_PRIMARY_SPECIALIST=IEEE_INTERNET_OF_THINGS_JOURNAL`

`CO_PRIMARY_ZERO_APC_SPEED=SCIENTIFIC_REPORTS`

`SPECIALIST_BACKUP=ELSEVIER_INTERNET_OF_THINGS`

`SPRINGER_SPECIALIST_BACKUP=TELECOMMUNICATION_SYSTEMS`

`P20B_AUTHOR_COMMITMENT=NO`

`P20C_LOCK_RELEASED=YES`

`SUBMISSION_AUTHORIZED=NO`
