# WellPulse — Current Handover

**Last updated:** 2026-09-09 after IEEE TNSM SUB02 submission and confirmation verification  
**Repository:** `aayoubMSA/WellPulse`  
**Branch:** `main`

This is the canonical operational handover. Do not reconstruct current state from older Elsevier/IoT handovers or chat memory.

## Current state

- **Venue:** IEEE Transactions on Network and Service Management (TNSM)
- **Article type:** Regular Issue submission
- **Lifecycle:** **SUBMITTED / WAITING — OFFICIAL SCHOLARONE MANUSCRIPT ID PENDING**
- **Submission date:** 2026-09-09
- **Author Portal / ReX submission ID:** `cac73869-ae6f-416c-8a36-7d82afeff8eb`
- **IEEE confirmation email:** Gmail message `1a0864e91a440449`
- **Confirmation status:** verified — manuscript successfully submitted and being delivered to the TNSM Editorial Office
- **Official TNSM Manuscript ID:** **PENDING**; IEEE states ScholarOne will send it in the next several days
- **External submission:** **EXECUTED / VERIFIED**
- **Reviewer-PDF QA:** **PASS**
- **New experiment required:** **NO**
- **Active scientific work:** **CLOSED while waiting for external response**

## Submitted manuscript authority

**Title:** *Beyond Reconnection: Receiver-Verified Service Recovery in MQTT Telemetry Across Failure Domains*

**Author/corresponding author:** Ahmed Ayoub  
**Affiliation:** Computer Systems Engineering Department, Faculty of Engineering, October University for Modern Sciences and Arts (MSA University), 6th of October City 12451, Egypt  
**Email:** `aelsayedo@msa.edu.eg`  
**ORCID:** `0009-0004-7895-3191`

The IEEE account UI currently greets the user as `Ahemd`, but the manuscript and submission author metadata were verified as **Ahmed Ayoub**. Do not treat the UI-profile typo as manuscript metadata.

### Final controlled package

- package: `WellPulse_TNSM_SUB02_Submission_Package_20260909.zip`
- SHA-256: `7945ccbd58b85aa128bf8163436f0a289d53a80fc8b743e5cc7e0cdae3e32802`
- main LaTeX upload archive: `WellPulse_TNSM_Main_Manuscript_LaTeX_20260909.zip`
- main LaTeX upload SHA-256: `803a92148b6239ea61fc04770df315390814441fd4680fec727c101640e84466`
- reproducibility supplement: `WellPulse_TNSM_Supplement_Reproducibility_20260909_FRESH.zip`
- supplement SHA-256: `3b6ede7ba4b73dd19767eff531eab05058e9220c95c873fb540cfad28677d5d9`

### IEEE-generated Reviewer PDF

- portal file / submission ID: `cac73869-ae6f-416c-8a36-7d82afeff8eb.pdf`
- pages: **12 total** = 3-page IEEE submission wrapper + 9-page manuscript
- SHA-256: `3f73ab4c7f3280f27debb215320614d6e926c46d9465a18a0a860863510dfec9`
- visual/render QA: **PASS**
- title/byline/ORCID/affiliation: **PASS**
- equations/tables/figures/references: **PASS**
- supplement binding: **PASS** (`Supplementary Zip Bundle`, accessible online to reviewers)
- cover letter correctly excluded from reviewer bundle

## Frozen TNSM contribution architecture

The paper is a **network/service-management recovery-assurance study**, not a new MQTT persistence-mechanism paper.

Primary contribution wedge:

> Connectivity restoration is an insufficient service-assurance criterion for stateful MQTT telemetry. Recovery closure should preserve failure-domain identity, declared endpoint, receiver-confirmed application state, and timing semantics.

Primary evidence:

1. **FIT IoT-LAB receiver-state closure**
   - B0 non-durable negative control: `8,000/10,000` under C1/C2
   - W1 durable application-buffered path: `10,000/10,000` under C1/C2
   - three run-level replicates per cell
   - B0 is **not** a durable MQTT comparator

2. **Post-reconnect incomplete-state interval**
   - durable-path connectivity recovery: about `1.3 s`
   - durable backlog reconciliation: about `67.7–67.9 s`
   - this W1-internal result is the principal TNSM service-management result and does not depend on generic B0-vs-W1 superiority

3. **POWDER failure-domain observability**
   - RF/client/core-network/broker-service failure domains
   - exact, censored, and upper-bound timing semantics retained
   - lower-layer health and MQTT service state can disagree
   - FIT and POWDER remain complementary evidence tracks and are never statistically pooled

## Immutable claim prohibitions

Do not claim:
- generic or strongest-durable-MQTT superiority;
- `WellPulse beats MQTT`;
- population reliability from three FIT replicates or from message counts;
- a universal `52 dB` threshold;
- deterministic RF-only recovery;
- exact broker-restart recovery when only an upper bound exists;
- pooled FIT+POWDER inference;
- firstness for persistence, store-and-forward, layered recovery, or generic recovery-layer separation;
- a universal recovery model.

Comparator scope remains the principal limitation and must stay visible in any revision.

## Portal declarations frozen at submission

- previously submitted to TNSM: **No**
- previously presented/published: **No**
- related to prior rejected manuscript: **Yes** — historical Internet of Things desk rejection `IOT-D-26-03494` disclosed; no peer review occurred
- conference extension: **No**
- related uncited author papers: **No**
- preprint: **No**
- human subjects: **No**
- animal subjects: **None**
- conflict of interest: **None disclosed**
- external research funding: **None**
- code associated: **Yes**
- separately linked/repository-hosted data to share: **No**
- reproducibility material: uploaded as reviewer supplementary ZIP
- opposed reviewers: none provided

Reviewer-routing keywords:
- Internet of Things Services
- Service Assurance
- Fault Management
- Performance Management

## Historical route

The earlier manuscript version was submitted to Elsevier *Internet of Things* as `IOT-D-26-03494` and desk-rejected on 2026-09-08 for insufficient novelty / quality threshold while explicitly considered in scope. No peer-review reports were issued. No appeal and no Elsevier transfer were executed.

That route is historical. Do not revert to the older title or IoT-journal positioning unless the owner explicitly reopens it.

## Exact next action

**WAIT. Do not perform new experiments, manuscript rewriting, venue shopping, or portal edits.**

Reopen only on one of these material triggers:
1. ScholarOne sends the official TNSM Manuscript ID;
2. TNSM technical check or administrative query;
3. editor/reviewer assignment or request;
4. editorial decision;
5. explicit owner instruction.

On receipt of the ScholarOne ID, update the Master Submission Tracker from `SUBMITTED — ID PENDING` to `SUBMITTED — WAITING`, record the exact ID and confirmation source, then return to waiting state.

## Stop state

`TNSM_SUB02_QA=PASS`
`TNSM_REVIEWER_PDF_QA=PASS`
`TNSM_SUBMISSION_EXECUTED=YES`
`TNSM_SUBMISSION_CONFIRMED=YES`
`TNSM_REX_SUBMISSION_ID=cac73869-ae6f-416c-8a36-7d82afeff8eb`
`TNSM_MANUSCRIPT_ID=PENDING`
`ACTIVE_SCIENTIFIC_EXECUTION=CLOSED`
`CURRENT_PHASE=WAIT_FOR_SCHOLARONE_ID_OR_MATERIAL_EXTERNAL_RESPONSE`

## NEXT CHAT PROMPT

```text
Resume WellPulse from the canonical repository HANDOVER_CURRENT.md only.
The paper "Beyond Reconnection: Receiver-Verified Service Recovery in MQTT Telemetry Across Failure Domains" was successfully submitted to IEEE Transactions on Network and Service Management (TNSM) on 2026-09-09 via IEEE Author Portal/ReX submission ID cac73869-ae6f-416c-8a36-7d82afeff8eb. Reviewer-PDF QA passed. The official ScholarOne Manuscript ID was still pending at handover freeze. Read the current EAS/Research Operating Doctrine and current repository handover first. Check for the exact external trigger; do not reopen experiments or manuscript work unless a material TNSM response requires it.
```
