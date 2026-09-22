# WellPulse IEEE Revival — R7f-R4 Evidence-Presentation Repair Freeze

**Date:** 2026-09-22
**Status:** PASS
**Parent authority:** R7f-R3 + R7f hostile review
**Scope:** evidence presentation only; no new experiment and no raw-data change

## 1. New source identity

`manuscript/revival_2026-09-22/WellPulse_Revival_R7fR4_EvidencePresentation_20260922.tex`

R7f-R3 remains preserved unchanged.

## 2. M0–M5 × campaign observability matrix

A new campaign-by-observable coverage matrix now states explicitly that not every campaign observes every recovery endpoint.

Historical FIT:
- M0: not directly instrumented by a dedicated post-restoration user-plane probe;
- M1: direct publisher reconnect/session-restoration measurement;
- M2: direct sender-side replay/QoS-1 closure, retrospectively reclassified as broker-hop rather than receiver completion;
- M3: end-state reconciliation only; exact completion timestamp absent;
- M4: direct seq5000→seq5001 source-generation gap;
- M5: no historical FIT ordering claim retained.

Prospective FIT Stage A:
- M0: direct post-restoration probe;
- M1: direct CONNACK;
- M2: direct record-attributed final PUBACK over H;
- M3: direct complete-H receiver timestamp, but relation to M2 unresolved in 3/3 runs;
- M4: direct source-generation gap;
- M5: arrival-order monitoring; no stale-arrival event and no causal witness in 3/3.

POWDER:
- M0: related path/ping restoration evidence, not the frozen FIT probe rule;
- M1: no isolated publisher CONNACK endpoint retained;
- M2: no frozen-H PUBACK-closure endpoint;
- M3: selected end-state/batch receiver completeness, not a timed frozen-H completion endpoint;
- M4: no W1 serialized-replay source-continuity metric;
- M5: direct same-receiver stale-carryover event in E3 cycle 3.

The matrix makes the historical endpoint correction visible: historical sender-side replay evidence can support M2/M4, but cannot be promoted to exact M3 timing.

## 3. Historical C1/C2 descriptive split

The six historical W1 generation-gap observations are now separated by treatment.

C1 — connectivity interruption without process restart:
- gaps: 68.992, 69.466, 68.944 s;
- mean: 69.134 s;
- range: 68.944–69.466 s;
- W1 final receiver: 10,000/10,000 in 3/3;
- B0 final receiver: 8,000/10,000 in 3/3;
- W1 publisher reconnect mean: 1.317 s.

C2 — connectivity interruption plus one gateway-process exec restart:
- gaps: 68.785, 70.264, 68.852 s;
- mean: 69.300 s;
- range: 68.785–70.264 s;
- W1 final receiver: 10,000/10,000 in 3/3;
- B0 final receiver: 8,000/10,000 in 3/3;
- W1 publisher reconnect mean: 1.345 s.

These are descriptive run summaries only. C1 and C2 remain distinct treatments and are not pooled for condition-level inference.

## 4. Evidence-faithful recovery figure

A new black-and-white vector figure was added with two panels.

Panel (a):
- frozen W1 source-side program order only;
- outage-period H generation;
- transport restoration;
- M0 prospective probe;
- M1 CONNACK;
- serialized H replay;
- M2 final PUBACK(H);
- seq5001 generation;
- M4 seq5000→seq5001 gap;
- historical C1 mean 69.134 s;
- historical C2 mean 69.300 s;
- prospective C1 range 74.798–76.308 s.

Panel (b):
- prospective D23=M3−M2 conservative intervals;
- R1 [-5.038,+4.801] s;
- R2 [-4.857,+4.932] s;
- R3 [-4.858,+4.815] s;
- all three cross zero;
- 0/3 causal witnesses;
- 3/3 UNRESOLVED.

Critical visual firewall:
M3 is deliberately not placed after M2 on the source-side timeline. The figure explicitly states that prospective evidence does not resolve that ordering.

## 5. Visual QA

The accepted PDF was rendered page-by-page at 160 dpi and visually inspected after machine QA.

Inspection focused on:
- Page 4: observable taxonomy + campaign coverage matrix;
- Page 6: historical C1/C2 split table;
- Page 7: prospective table + new recovery figure.

Visual result:
- no clipping;
- no table overflow;
- no figure overlap;
- no broken glyphs;
- matrix is legible;
- C1/C2 table is legible;
- recovery figure is legible in black/white;
- figure does not visually assert M2-before-M3.

`R7FR4_VISUAL_QA=PASS`

## 6. Machine QA

Temporary QA PR: `#48`.

Superseded attempts:
- 35710987881: failed only because the first C1/C2 table and figure exceeded IEEE width;
- later repair commits narrowed the table, scaled the figure, and removed figure-label overlap;
- 35711852418 and 35712369275 were intermediate successful machine passes followed by further visual polishing.

Final accepted run:
`35712778308` — SUCCESS.

Passed:
- exact R7f-R4 authority checkout;
- coverage-matrix assertions;
- frozen C1/C2 arithmetic and values;
- evidence-figure semantic assertions;
- R7f-R3 science locks;
- 14-reference bibliography lock;
- claim firewall;
- IEEEtran compile;
- undefined citations = 0;
- undefined references = 0;
- LaTeX errors = 0;
- overfull boxes = 0;
- rendered-text smoke = PASS.

Final compiled PDF:
- pages: 10;
- letter paper;
- file size: 230,412 bytes.

Accepted-build SHA-256:
- R7f-R4 TEX:
  `14c29c0d693bc696ae042b291b0528ab68c62ebfdb91e7c4d461bce8f05756eb`;
- R7f-R4 PDF:
  `6278b4d8de668acdd8c336bce846eaf47054bc2ac940e14e49ac126e00129d49`.

Final Actions artifact:
- artifact ID: `10688475323`;
- size: 245,146 bytes;
- digest:
  `sha256:a222858c6cde863ec155e9e9930593d13a370076b9ce0d9187fd627fb7bd6612`;
- retention: 30 days.

## 7. Durable preservation

Drive folder:
`P12_WellPulse / R7fR4_Evidence_Presentation_2026-09-22`

Drive folder ID:
`19DOuiWtQtr04wd38fenrlRZ-FaUw25sY`

Drive package:
`WellPulse_R7fR4_Evidence_QA_35712778308.zip`

Drive file ID:
`1dw9nOYWi4K1LYW_TeWmq-DEKCFaKK91r`

Drive read-back:
- size: 245,146 bytes;
- SHA-256:
  `a222858c6cde863ec155e9e9930593d13a370076b9ce0d9187fd627fb7bd6612`;
- exact match to the GitHub Actions artifact digest.

## 8. Repository authority

- accepted manuscript source blob:
  `167355aa580fbcaf19a1cc306d6053feae7db1cd`;
- accepted source commit:
  `ef2902e545668516ad30e1cd95751aecad314281`.

## 9. R7f repair-package closure

R7f-R1 SOTA + claim-boundary repair: PASS.
R7f-R2 contribution + evidence framing: PASS.
R7f-R3 reproducibility surface: PASS.
R7f-R4 evidence presentation: PASS.

The major repair package raised by the hostile R7f review is therefore closed without new scored experiments.

## 10. Gate

`R7f_R4_EVIDENCE_PRESENTATION=PASS`

`R7f_R4_COVERAGE_MATRIX=PASS`

`R7f_R4_C1_C2_SPLIT=PASS`

`R7f_R4_EVIDENCE_FIGURE=PASS`

`R7FR4_MACHINE_QA=PASS`

`R7FR4_VISUAL_QA=PASS`

`R7f_MAJOR_REPAIR_PACKAGE=CLOSED`

`R7g_ENTRY=UNLOCKED`

Next:
R7g performs the final integrated compile / visual / evidence QA of the complete revived manuscript. No venue decision occurs until R8.