# WP2-P20E — Independent Submission-Readiness Validation

Date: 2026-08-29
Target: **IEEE Internet of Things Journal**
Route: **Traditional / non-OA**
Validated package: `WellPulse_P20D_R1_IEEE_Submission_Package_2026-08-29.zip`
Status: **PASS / SUBMISSION-READINESS VALIDATED / P21 UNLOCKED / NO SUBMISSION**

## Independence rule

P20E treated the P20D package as frozen input and initially performed no authoring. The first red-team pass found four production-only issues and returned them to a bounded P20D-R1 repair lane. P20E was then rerun from a fresh extraction of the new R1 archive.

No scientific claim, result, figure, comparator conclusion, or novelty statement was reopened.

## Current journal-policy recheck

Current IEEE IoT-J author guidance was independently rechecked on 2026-08-29.

Relevant current requirements:

- original/substantial work must not be simultaneously under consideration elsewhere;
- manuscript must use the IEEE double-column journal style;
- abstract must be one paragraph and **150–250 words**;
- **ORCID is required for all authors** to submit/review proofs;
- mandatory overlength charge is **USD 175/page beyond the first eight published pages**, and submission signifies acceptance of that requirement;
- Traditional route requires no OA APC;
- IEEE copyright form is required before publication;
- supplementary materials are uploaded as separately labeled files and should include an adequate README for collections/datasets;
- substantive AI-generated content must be disclosed in the Acknowledgment, identifying the AI system, affected sections, and level of use.

## Validation matrix

| Control | Independent result | Verdict |
|---|---|---|
| Outer archive SHA | `73b46d0b19cfd74689bdc10efb27c71a5460ca1c9ab6843503155a87696eb73c` | PASS |
| Drive raw read-back | exact same SHA | PASS |
| Root manifest | 66 entries, 0 errors | PASS |
| Root SHA list | 67 entries, 0 errors | PASS |
| Nested P19 manifest | 53 entries, 0 errors | PASS |
| PDF open/preflight | 6 pages, unencrypted, US Letter, text PDF | PASS |
| Font embedding | all listed fonts embedded | PASS |
| Visual review | no clipping, overlap, broken glyphs, or unreadable figure | PASS |
| Independent TeX rebuild | 6 pages | PASS |
| Rebuild visual diff | 0 changed pages / 0.0% pixels | PASS |
| Abstract length | 221 words | PASS |
| Publication name | `Ahmed Ayoub`; expanded variants = 0 | PASS |
| Corresponding-author identification | explicit in first footnote | PASS |
| Affiliation | MSA CSE + 6th October City 12451, Egypt | PASS |
| Funding basis | no external research funding, first-footnote placement | PASS |
| COI | no competing interests identified | PASS |
| FIT acknowledgment/citation | present | PASS |
| POWDER acknowledgment/citation | present | PASS |
| AI disclosure | OpenAI ChatGPT + affected sections + responsibility/level statement in Acknowledgment | PASS |
| CRediT | present for Ahmed Ayoub | PASS |
| P19 isolated self-check | PASS | PASS |
| `__pycache__` / `.pyc` | 0 | PASS |
| private IPv4 in reviewer corpus | 0 detected | PASS |
| credential/security text scan | no exposed credential value detected | PASS |
| forbidden generic MQTT-superiority strings | absent | PASS |
| universal 52 dB claim | absent | PASS |
| pooled FIT+POWDER inference | absent | PASS |
| P7B success relabeling | absent | PASS |
| field/industrial-process validation claim | absent | PASS |
| P20A comparators | Mohammed 2026, E-MQTT 2023, Radwan 2026 present | PASS |
| recent comparator DOI spot-check | current external records match manuscript | PASS |
| Gaspar detail use | bibliographic/scope only | PASS |
| supplementary README | IEEE collection fields present | PASS |

## Independent numerical spot-check

P20E independently recomputed key values from the included derived CSVs rather than relying only on manuscript prose.

FIT:
- C0 B0/W1 = 100% in all runs;
- C1 B0 = 80%, W1 = 100%;
- C2 B0 = 80%, W1 = 100%;
- 2,000 permanent B0 missing records per C1/C2 run;
- W1 C1 mean reconnect `1.317088 s`, backlog drain `67.731246 s`;
- W1 C2 mean reconnect `1.3448697 s`, backlog drain `67.870252 s`;
- B0 reconnect means `1.325412 s` (C1) and `1.3621213 s` (C2).

POWDER spot-checks:
- E1R4 @51 dB: ICMP loss 30%, MQTT 20/20;
- E1R4 @52 dB: ICMP loss 60%, MQTT 13/20 = 65%;
- E2 @52 dB: ICMP loss 65%, MQTT 11/20 = 55%;
- E2 @51 dB: ICMP loss 10%, MQTT 20/20;
- E3 @52 dB MQTT completeness: 60%, 25%, 55% across cycles.

All match the submission-facing manuscript and frozen scientific doctrine.

## Literature / DOI spot-check

Independent current-source spot-check confirmed:

- Mohammed et al. 2026: DOI `10.48084/etasr.16945`, volume 16 issue 3, pages 36014–36024;
- Im and Lim 2023: DOI `10.3390/app132212419`, Applied Sciences 13(22), 12419;
- Radwan et al. 2026: DOI `10.1038/s41598-026-66865-8`, published 17 Aug 2026;
- POWDER reference: DOI `10.1016/j.comnet.2021.108281`;
- FIT IoT-LAB reference DOI `10.1109/WF-IoT.2015.7389098`;
- Gaspar bibliographic DOI `10.1109/MIOT.2026.3681190` independently exists; detailed method/result attribution remains prohibited unless full text is directly recovered.

## Visual/accessibility review

All six manuscript pages were rendered at 180 dpi and inspected. Main F1–F4 remain readable in the two-column build. Figures preserve the P18RC grayscale/semantic encoding. The separate alt-text file remains mapped to F1–F4. No visual defect requiring P20D reopening remains.

## Residual portal controls — P21/P22, not P20E defects

1. **ORCID portal gate:** IoT-J requires ORCID for every author. P21 must verify the exact ORCID linked to Ahmed Ayoub before authorization; the manuscript does not need to print ORCID in the byline.
2. **No concurrent submission:** P21 must explicitly confirm the manuscript is not under active consideration elsewhere at the authorization moment.
3. **Traditional route selection:** the portal must remain Traditional/non-OA unless the author explicitly changes route.
4. **Page-charge acceptance:** although the author build is 6 pages, IoT-J states that submission itself signifies acceptance of mandatory overlength charges if the published article exceeds eight pages. P21 must surface this exact residual condition for explicit author authorization.
5. **Supplement upload mapping:** the R1 outer ZIP is an archival authority, not a single portal upload. P21 should map the main manuscript and supplementary files to their portal roles and label supplements separately.
6. **Graphics upload naming:** if the portal requests separate production graphics, P21/P22 should use IEEE-compatible upload copies/names; this must not change figure content or authority.
7. **Graphical abstract:** optional, not required; none is needed to pass readiness.
8. **Copyright form:** downstream pre-publication action, not authorized by P20E.

## P20E verdict

There are **no remaining manuscript-science, evidence, production-layout, privacy/security, identity, acknowledgment, AI-disclosure, or supplementary-readiness blockers** in the validated R1 package.

`WP2_P20E=PASS_INDEPENDENT_SUBMISSION_READINESS_VALIDATION`

`VALIDATED_ARCHIVE_SHA256=73b46d0b19cfd74689bdc10efb27c71a5460ca1c9ab6843503155a87696eb73c`

`VALIDATED_PDF_SHA256=95917105f9d03fce155b9cc2a579d2e0e6f567a30557f87f82382db193597fa1`

`SCIENTIFIC_BLOCKERS=0`

`PRODUCTION_BLOCKERS=0`

`P21_UNLOCKED=YES`

`SUBMISSION_AUTHORIZED=NO`
