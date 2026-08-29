# WP2-P18R — Scientific Figure Requirements Specification (FRS)

Date: 2026-08-29  
Status: **FROZEN / AUTHOR-REQUESTED HIGH-CREDIBILITY FIGURE ENGINEERING**

## 1. Authority hierarchy

1. P13 claim–evidence matrix;
2. P11 reconstructed FIT/POWDER metrics;
3. P9 forensic validity/anomaly authorities;
4. canonical `records.py` / `store.py` implementation semantics;
5. P17/P17V manuscript framing;
6. this FRS for display implementation only.

## 2. Main-figure functional requirements

### F1 — System and evidence architecture

Must expose:
- stable record identity and SHA-256;
- durable SQLite WAL/PENDING state;
- publish/retry behavior;
- receiver reconciliation;
- FIT design/treatment/endpoints;
- POWDER transition/recovery/control families;
- claim mapping;
- explicit non-pooling.

### F2 — FIT effect + recovery cost

Must expose:
- all three run-level B0/W1 observations for C0/C1/C2;
- full 0–100% completeness scale;
- +20 pp observed C1/C2 differences;
- exact 2,000-record B0 outage-block loss;
- reconnect observations;
- W1 backlog-drain observations;
- separation of final integrity, reconnect, and catch-up.

### F3 — POWDER transition + repeatability

Must expose:
- E1R4 ascending ICMP response;
- E2 descending ICMP response;
- E1R4/E2 MQTT completeness;
- E3 ICMP cycle variability;
- E3 MQTT cycle variability;
- experiment-specific attenuation only;
- no fitted threshold.

### F4 — Failure-domain + recovery semantics

Must expose:
- RF/UE/CORE/broker/no-fault intervention identity for E4–E10;
- E10-A censored non-recovery;
- E10-B exact endpoints;
- E10-C-B exact endpoints;
- E10-D upper-bound semantics;
- no generic pooled recovery latency.

## 3. Non-functional requirements

- deterministic code generation;
- zero AI image dependency;
- no manual raster editing in the canonical production path;
- full-width composite publication figures;
- vector PDF/SVG masters;
- 600-dpi PNG fallback;
- embedded PDF fonts;
- no clipped/overlapping text at final rendered size;
- no decorative icons in quantitative figures;
- no dual y-axis quantitative plots;
- marker/linestyle redundancy for multiple series;
- captions carry interpretive caveats instead of crowding data regions.

## 4. Scientific safety requirements

- B0 remains a non-durable publish-only comparator;
- no generic MQTT superiority;
- no universal 52 dB threshold;
- no message-count pseudoreplication;
- no unsupported CI or p-value;
- no scalar E10-A latency;
- E10-D remains upper bound;
- no pooled FIT+POWDER inferential statistic.

## 5. Verification requirements

Build must assert frozen source-data values before rendering.

Post-build V&V must verify:
- four figure families exist in PDF/SVG/PNG;
- PDF width is at or below full publication width;
- PDF fonts embedded;
- source-data receipt exists;
- hashes exist;
- render-first visual inspection complete;
- figure-to-claim mapping preserved.

## 6. Change-control rule

Any later change to numerical data, aggregation, axis semantics, fit/smoothing, treatment grouping, endpoint definition, or claim implication **reopens P18R scientific V&V**.

Pure venue transformations such as font normalization, filename normalization, or equivalent line-weight changes may proceed under P20 production QA if the data encoding and claim meaning are unchanged.

`P18R_FRS=FROZEN`
