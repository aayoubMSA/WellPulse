# WellPulse IEEE Revival — R8 Venue Requalification and Submission Decision

**Date:** 2026-09-22
**Status:** PASS
**Scientific authority:** R7g final candidate / R7f-R4 manuscript
**Manuscript edits in R8:** NONE
**Submission action in R8:** NONE

## 1. Frozen manuscript object

Title:
**Beyond Reconnection: Measuring Recovery Observables and Replay-Induced Continuity Gaps in MQTT Telemetry**

The manuscript is now an experimental network/IoT measurement paper, not a new recovery architecture.

Surviving contribution:
- operational recovery-measurement discipline over M0–M5;
- implementation-specific, repeatedly measured W1 serialized-replay continuity cost;
- prospective negative/bounded M2→M3 adjudication;
- complementary non-pooled POWDER stale-carryover/failure-domain evidence;
- reproducibility and evidence-preservation discipline.

Primary venue risk:
the strongest empirical result is a measured consequence of the frozen serialized replay code path, not a new general recovery mechanism.

## 2. Candidate requalification

### A. Computer Communications — Elsevier
**Disposition: PRIMARY TARGET**

Current official scope explicitly includes:
- Internet of Things;
- experimental test-beds and research platforms;
- modeling, measurement, and simulation of computer communication networks;
- protocols, services, and applications;
- practical as well as theoretical research.

Recent scope evidence includes:
- *A methodology for reproducible and portable experiment workflows* (Computer Communications, 2025), centered on reproducible networking testbed workflows;
- 2026 IoT/reliability papers in the journal, including state-change consistency validation and reliable communication services.

Fit to WellPulse:
- strongest match to the paper's experimental/testbed identity;
- the M0–M5 measurement discipline is directly within measurement/evaluation scope;
- FIT IoT-LAB + POWDER are natural experimental-platform evidence;
- MQTT/IoT context is explicitly in scope;
- the journal does not require the paper to be a new network-management architecture.

Residual risk:
- novelty must remain framed as measurement discipline + evidence adjudication, not as a new MQTT mechanism;
- the paper should not be rewritten to claim a broader system contribution merely to fit the venue.

Decision:
**GO.**

### B. Computer Networks — Elsevier
**Disposition: QUALIFIED BACKUP / HIGHER NOVELTY RISK**

Current official scope covers:
- communication protocols and their performance evaluation;
- network operation/management;
- reliability;
- network performance measurement and analysis;
- experimental networking.

Recent 2026 papers confirm appetite for:
- reproducible experimental testbeds;
- large-scale empirical network measurement;
- MQTT and publish-subscribe performance studies.

Why not primary:
Computer Networks' own scope language emphasizes novel solutions and analyses, and recent empirical papers often pair measurement with a broader method, tool, large-scale dataset, or mechanism. WellPulse is scientifically sound but intentionally does not claim a new recovery mechanism.

Decision:
**BACKUP, not first submission.**

### C. Internet of Things — Elsevier
**Disposition: STRONG TOPICAL BACKUP, OVERLAP RISK**

Official scope spans IoT reliability, enabling technologies, software/engineering, and full research papers.

A directly relevant 2025 article, *An approach to assess robustness of MQTT-based IoT systems*, confirms that MQTT fault-injection/robustness methodology is squarely within scope.

Why not primary:
- that close topical precedent also raises novelty-overlap scrutiny;
- WellPulse's strongest identity is now network recovery measurement semantics rather than a broad IoT application or new IoT robustness method;
- Computer Communications provides a cleaner home for the experimental-networking/testbed emphasis.

Decision:
**BACKUP.**

### D. Journal of Network and Systems Management — Springer
**Disposition: SCOPE-POSSIBLE, NOT PREFERRED**

The journal publishes network/system management, monitoring, performance, orchestration, reliability and experimental measurement work. Recent papers include experimental network performance/monitoring studies.

Why not primary:
- the revived manuscript deliberately moved away from a network/service-management mechanism;
- after the TNSM rejection and R6 pivot, forcing the work back into a management-journal frame risks recreating the same contribution-depth objection;
- the paper now reads more naturally as experimental communications/network measurement.

Decision:
**DO NOT TARGET FIRST.**

### E. Journal of Network and Computer Applications — Elsevier
**Disposition: BROAD BACKUP**

The journal covers computer networks, IoT, sensor networks, protocols and network applications.

Why not primary:
its scope is broad but less specifically aligned than Computer Communications with experimental testbeds and network measurement. The manuscript would compete against papers with more application novelty.

Decision:
**BACKUP ONLY.**

## 3. Final submission decision

**Primary venue: Computer Communications (Elsevier).**

Article type:
**Research Article / regular scientific article.**

The manuscript should be submitted as:
- an experimental computer-communications/network measurement study;
- not a new MQTT recovery architecture;
- not a network-management mechanism paper;
- not a generic durability-vs-freshness paper.

Venue-facing positioning:
**measurement semantics + reproducible experimental evidence + bounded claim adjudication.**

## 4. Required venue-specific delta before submission

Scientific content is frozen.

Only submission engineering is required:
1. convert IEEEtran source to the current Computer Communications/Elsevier submission format;
2. preserve title, abstract, contribution boundaries, tables, figure, numbers and references unless a venue rule requires a purely editorial change;
3. prepare Elsevier-required highlights if requested;
4. prepare cover letter centered on measurement/reproducibility fit;
5. include the sanitized reproducibility supplement;
6. keep private raw archives private while retaining hash authority;
7. select the non-open-access/subscription route if available unless the author explicitly chooses an APC/open-access option;
8. do not make any payment, copyright/licence, APC, or irreversible submission commitment without explicit author approval.

## 5. R8 gate

`R8_VENUE_REQUALIFICATION=PASS`

`R8_PRIMARY_TARGET=COMPUTER_COMMUNICATIONS`

`R8_ARTICLE_TYPE=RESEARCH_ARTICLE`

`R8_SCIENTIFIC_CONTENT_CHANGE=NONE`

`R8_SUBMISSION_EXECUTED=NO`

`NEXT=COMPUTER_COMMUNICATIONS_SUBMISSION_PACKAGE_PREPARATION`
