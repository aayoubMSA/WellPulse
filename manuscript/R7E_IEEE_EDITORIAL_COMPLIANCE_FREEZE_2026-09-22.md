# WellPulse IEEE Revival — R7e IEEE Editorial/Compliance Freeze

**Date:** 2026-09-22
**Status:** PASS
**Scientific authority:** R6 + R7c + R7d
**Scope:** editorial/compliance only; scientific claims locked

## 1. R7e source identity

`manuscript/revival_2026-09-22/WellPulse_Revival_R7e_Editorial_20260922.tex`

R7d remains preserved unchanged.

## 2. Exact author metadata recovered and applied

- Author: Ahmed Ayoub
- Affiliation: Computer Systems Engineering Department, Faculty of Engineering, October University for Modern Sciences and Arts (MSA University), 6th of October City, 12451, Egypt
- Email: aelsayedo@msa.edu.eg
- ORCID: 0009-0004-7895-3191

These values were recovered from the Sep-07 WellPulse submission title-page authority and were not inferred.

## 3. Editorial-only changes

- exact author/affiliation/correspondence/ORCID metadata;
- PDF title/author/subject/keyword metadata;
- keyword tightening;
- FIT IoT-LAB and POWDER facility citations;
- manual bibliography normalized toward IEEE reference style;
- prior-submission acknowledgment, funding, and conflict-of-interest declarations restored;
- table typography tightened only to eliminate overflow;
- long SHA-256 display split into two copy-safe 32-hex blocks.

No scientific sentence/value was altered by R7e.

## 4. Facility citation completion

FIT IoT-LAB facility reference added:
- C. Adjih et al., FIT IoT-LAB: A large scale open experimental IoT testbed;
- IEEE WF-IoT 2015, pp. 459–464;
- DOI 10.1109/WF-IoT.2015.7389098.

POWDER facility reference added:
- J. Breen et al., Powder: Platform for Open Wireless Data-driven Experimental Research;
- Computer Networks, vol. 197, 108281, 2021;
- DOI 10.1016/j.comnet.2021.108281.

## 5. Science-lock proof

Machine QA compared R7e against R7d/R7c and passed:
- title unchanged;
- abstract unchanged;
- Introduction + Related Work unchanged;
- Methods + Results identical after normalizing only two facility citations and float-format directives;
- Discussion + Threats + Reproducibility + Conclusion identical after normalizing only float typography and SHA line wrapping;
- claim firewall unchanged;
- single-author voice retained.

## 6. PDF / layout result

Compiled under IEEEtran.

- pages: 7;
- letter paper;
- PDF metadata title: Beyond Reconnection: Measuring Recovery Observables and Replay-Induced Continuity Gaps in MQTT Telemetry;
- PDF author: Ahmed Ayoub;
- undefined citations: 0;
- undefined references: 0;
- LaTeX errors: 0;
- undefined control sequences: 0;
- overfull boxes: 0.

Remaining underfull-box warnings are confined to narrow table cells and do not overflow the page.

## 7. Clean-source/privacy gate

Clean source package contains one manuscript `.tex` file only.

Secret/privacy scan excludes:
- FIT_PASSWORD;
- SSH private-key material;
- private R5 preservation Drive IDs.

## 8. Machine QA

Temporary QA PR: `#44`.

Earlier R7e QA attempts were test-harness refinements only:
- 35702181257: Discussion-table float-size normalization missing from comparator;
- 35702288948: rendered heading case sensitivity;
- 35702658442: same rendered-heading smoke after layout fix;
- 35702892399: bibliography-heading extraction was not stable under pdftotext;
- 35703155707: redundant rendered bibliography-entry smoke remained brittle.

None of those attempts changed scientific content.

Final QA run:
`35703430589` — SUCCESS.

Final artifact:
- artifact ID: `10683580970`;
- name: `wellpulse-r7e-editorial-qa-35703430589`;
- artifact ZIP digest: `sha256:efa98631a63f9634124abe6e4c75a206e13b06bcfddf42ee2c570e6ff3c9507a`;
- artifact size: 225,376 bytes;
- retention: 30 days.

File hashes from the exact successful build:
- R7e `.tex`: `b966a951d94a1c8d2d72cbd55c6680df355853a53f3577b2ed1c8f1fef369442`;
- R7e `.pdf`: `81bf29819256daebe8834d90af77cb52fd501abc56594cda33a7babadba99eed`;
- clean-source `.tar.gz`: `a55ed5cf458f6d3e4c3b5f0e0945d5e3fe2c6bcc4946b884028605b267d8f328`.

## 9. Gate

`R7e_IEEE_EDITORIAL_COMPLIANCE=PASS`

`R7e_SCIENCE_LOCK=PASS`

`R7E_MACHINE_QA=PASS`

`R7f_ENTRY=UNLOCKED`

Next:
R7f performs hostile scientific review of the complete R7e manuscript. No venue decision occurs until R8.