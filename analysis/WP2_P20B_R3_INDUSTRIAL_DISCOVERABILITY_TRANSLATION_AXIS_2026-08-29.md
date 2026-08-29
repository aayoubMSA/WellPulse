# WP2-P20B-R3 — Industrial Discoverability & Translation Axis

Date: 2026-08-29  
Repository: `aayoubMSA/WellPulse`  
Branch: `main`  
Status: **COMPLETE / INDUSTRIAL-PULL AXIS ADDED / NO SCIENTIFIC CHANGE**

## 1. Trigger

The author identified a missing venue-selection objective: papers are not read only by academic peers. Corporate R&D engineers, technology scouts, innovation teams, standards engineers, patent teams, venture builders, technology-transfer offices and potential licensees also search technical literature for deployable ideas.

This introduces a distinct venue-selection dimension:

**Industrial Pull / Translational Discoverability** — the probability that the published work is encountered, understood and considered by actors capable of converting it into products, licenses, standards input, sponsored research or commercial partnerships.

## 2. Why this is not the same as scientific impact

Scientific citation impact and commercial discoverability are correlated but not identical.

A venue can be:

- scientifically prestigious but weakly read by engineering practitioners;
- broad and highly visible but not searched routinely by technical product teams;
- specialist and heavily used by corporate R&D/standards teams;
- accessible but difficult to translate because the article/artifact is not implementation-facing.

Therefore venue selection should not use impact factor, CiteScore, indexing, APC or editorial speed as proxies for industrial pull.

## 3. Industrial-pull dimensions

| Dimension | Question |
|---|---|
| Practitioner density | Are engineers, product developers and corporate researchers part of the normal readership? |
| Corporate search infrastructure | Is the platform sold/used explicitly for corporate R&D and technology discovery? |
| Patent/innovation adjacency | Is the literature demonstrably used in patents or invention workflows? |
| Standards adjacency | Does the ecosystem connect directly to standards bodies, SDO activity or implementation guidance? |
| Applied-method readability | Can a practitioner understand what was built/tested without reconstructing the science from scratch? |
| Artifact/code availability | Can a scout or engineer inspect reproducible material and estimate implementation effort? |
| Open discoverability | Can non-subscribers access enough of the work to identify commercial relevance? |
| Translation pathway | Is the ecosystem connected to industry partnerships, practitioner communities or technology-transfer activity? |

## 4. Current publisher/ecosystem evidence

### IEEE — VERY HIGH industrial-pull evidence

Current IEEE material explicitly positions IEEE Xplore as a resource for researchers in academia, industry and government and as a platform used by industry professionals for design/application research and standards work. IEEE reports that its publications receive more than three times the patent citations of competing publishers in US and European new-technology patents and specifically identifies IoT among fields in which IEEE is the most referenced publisher in patents.

For WellPulse this matters because the work is engineering-facing, IoT-specific, implementation/testbed-driven and potentially relevant to reliability architectures, middleware/gateway products and telemetry systems.

Additional structural advantage: IEEE IoT Journal explicitly includes IoT standardization activity and SDOs such as IEEE, IETF, ITU, 3GPP and ETSI in its scope.

**Industrial Pull: VERY HIGH.**

### Elsevier / ScienceDirect — HIGH corporate-R&D discoverability

Elsevier explicitly markets ScienceDirect, Scopus and related products to industrial R&D teams and describes scientific literature as a source used to make innovation decisions. ScienceDirect for R&D is positioned for corporate innovation and engineering/technology organizations, with full-text literature integrated into R&D discovery workflows.

For WellPulse, *Internet of Things* therefore has meaningful industrial-search value in addition to academic fit.

**Industrial Pull: HIGH.**

### ACM — HIGH computing-practitioner discoverability

ACM describes its Digital Library as serving researchers, practitioners and corporate users across telecommunications, electronics, internet, defense, energy and manufacturing. Beginning in 2026 ACM publications are open access, improving discoverability and reuse. ACM's ecosystem is strongly computing-specialist, although available evidence suggests IEEE remains stronger in corporate/patent penetration.

**Industrial Pull: HIGH / SPECIALIST.**

### Nature Portfolio / Scientific Reports — HIGH broad visibility, MEDIUM targeted engineering pull

Nature Portfolio emphasizes global, cross-disciplinary readership and open access. This is strong for broad visibility and serendipitous discovery, and the confirmed STDF/EKB agreement can make Scientific Reports economically attractive. However, it is less directly integrated with engineering standards/practitioner workflows than IEEE and less explicitly corporate-R&D-search focused than Elsevier's industry products.

**Industrial Pull: HIGH BROAD / MEDIUM TARGETED.**

## 5. WellPulse industrial-readiness profile

WellPulse has potentially interesting applied elements beyond the paper's scientific contribution:

- durable record-state survival under bounded failure conditions;
- explicit gateway-side state semantics;
- receiver-side identity reconciliation;
- separation of record-state survival from path recovery;
- failure-domain-specific recovery semantics;
- deployable evidence/reproducibility artifacts.

These could be relevant to:

- industrial IoT telemetry platforms;
- remote monitoring gateways;
- energy/water/agriculture monitoring systems;
- field sensors with intermittent backhaul;
- edge middleware vendors;
- reliability testing and validation services;
- device-management / fleet-observability vendors;
- standards or best-practice work around evidence-aware IoT resilience.

This is **commercial hypothesis space**, not a validated market claim. No revenue, market size, customer demand or patentability is currently claimed.

## 6. Venue impact after adding industrial pull

### IEEE Internet of Things Journal

Remains **PRIMARY** and becomes stronger.

Reason: it performs well simultaneously on:

1. scientific fit;
2. specialist IoT readership;
3. corporate/industry discoverability;
4. patent adjacency;
5. standards adjacency;
6. current publication speed.

Its main risk remains page/overlength economics and possible destructive compression. That is a P20D simulation issue, not a reason to demote it now.

### Internet of Things (Elsevier)

Remains **strong backup** and gains explicit recognition as a corporate-R&D-discoverable route through ScienceDirect/Scopus industry workflows.

### ACM Transactions on Internet of Things

Remains scientifically strong and becomes more attractive under 2026 open access because practitioners can discover/read the final work without subscription barriers. Cost/institutional-coverage status remains a separate gate.

### Scientific Reports

Remains a powerful broad-reach/economically advantaged route because of the confirmed MSA Springer Nature–STDF–EKB agreement. Its industrial visibility is broad rather than engineering-specialist; therefore it does not replace IEEE IoT-J as the specialist industrial-pull leader.

## 7. New decision doctrine

Venue selection for applied engineering research should now evaluate at least four independent objectives:

1. **Scientific Fit / Editorial Plausibility**
2. **Publication Economics / Speed**
3. **Industrial Pull / Translational Discoverability**
4. **Evidence-Package Preservation / Reproducibility**

A single scalar journal metric must not substitute for these dimensions.

For WellPulse current objective profile:

- **Best specialist scientific + industrial route:** IEEE Internet of Things Journal.
- **Best corporate-R&D-search fallback with lower transformation risk:** Elsevier Internet of Things.
- **Best broad/open/economically advantaged route:** Scientific Reports under verified STDF/EKB eligibility.
- **Best computing-specialist OA alternative:** ACM Transactions on Internet of Things, subject to institutional/APC confirmation.

## 8. Commercialization/IP pre-publication safeguard

Industrial pull creates a new rights risk: if WellPulse contains potentially patentable foreground IP, public disclosure can affect patent novelty.

WIPO states that public disclosure before patent filing can become prior art and can prevent valid patent protection in many jurisdictions; grace periods vary and should not be assumed. Therefore a bounded IP/commercialization screen must occur before any external submission/public release if protectable subject matter may exist.

This does **not** mean WellPulse is patentable. Current state is:

`PATENTABILITY=UNKNOWN_NOT_ASSESSED`

`COMMERCIAL_DEMAND=UNKNOWN_NOT_VALIDATED`

`IP_OWNERSHIP=TO_BE_VERIFIED_IN_P20C`

P20C must now include a pre-publication IP/translation check alongside authorship, rights and acknowledgments.

## 9. Scientific impact

None.

No experiment, statistic, result, claim, comparator or figure is changed.

`P13_UNSUPPORTED_MANUSCRIPT_CLAIMS=0`

`P20A_SCIENTIFIC_BLOCKERS=0`

`NEW_EXPERIMENT_REQUIRED=NO`

## 10. Current venue authority after R3

R1 remains authority for publisher-neutral scientific/editorial fit.

R2 remains authority for national/institutional publishing-agreement economics.

R3 is authority for industrial-pull/translation weighting and the pre-publication commercialization/IP safeguard.

No venue commitment is made.

`P20B_R3=PASS_INDUSTRIAL_DISCOVERABILITY_TRANSLATION_AXIS`

`P20B_SPECIALIST_PRIMARY=IEEE_INTERNET_OF_THINGS_JOURNAL`

`P20B_CORPORATE_RD_BACKUP=ELSEVIER_INTERNET_OF_THINGS`

`P20B_BROAD_ZERO_APC_ROUTE=SCIENTIFIC_REPORTS_CONDITIONAL_ON_ARTICLE_ELIGIBILITY`

`P20B_ACM_SPECIALIST_OA=ACM_TRANSACTIONS_ON_INTERNET_OF_THINGS_COST_GATE`

`P20C_MUST_INCLUDE_IP_TRANSLATION_SCREEN=YES`

`SUBMISSION_AUTHORIZED=NO`
