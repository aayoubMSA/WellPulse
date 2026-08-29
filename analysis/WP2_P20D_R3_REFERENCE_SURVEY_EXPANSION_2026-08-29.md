# WP2-P20D-R3 — Reference / Survey Expansion for Elsevier Internet of Things

Date: 2026-08-29
Status: **PASS / R3-R2 CURRENT PRODUCTION AUTHORITY / NOT SUBMITTED**

## Trigger

The author rejected the 17-reference version as too short for the amount of literature-survey effort completed and required that the paper visibly demonstrate that work.

This patch reopened **literature presentation and production only**. It did not reopen experiments, empirical results, statistical units, P13 claims, P17V conclusions, P18RC figure science, or FIT/POWDER inferential roles.

## Expanded literature backbone

The current targeted submission-date novelty audit contains **32 source/axis groups**:

- **25 peer-reviewed scholarly articles**;
- **1 normative MQTT standard**;
- **6 official technical/platform documentation sources**.

The retained sources span the frozen seven search axes plus the direct subthemes needed to expose the prior-art boundary: persistent MQTT state, retransmission/store-and-forward, offline-first continuity, downstream acknowledgment/receiver confirmation, broker distribution/scalability, QoS/timeliness/freshness, robustness/stress testing, and repeatable testbed methodology.

Current audit classification:

- wording narrowing: **17** groups;
- contextual/no-impact: **15** groups;
- scientific blockers: **0**.

All 32 bibliography entries are cited in the manuscript; no uncited or unresolved bibliography keys remain.

## Important newly surfaced comparators

The expansion adds materially relevant work rather than citation padding, including:

- OASIS MQTT Version 5.0 normative semantics;
- Detti et al. 2020 MQTT cluster scalability;
- Longo et al. 2022 BORDER distributed-broker benchmarking;
- Longo & Redondi 2023 distributed MQTT broker design;
- Cho et al. 2024 multi-broker delay;
- Kim & Kyung 2024 Age-of-Information-aware MQTT retained messages;
- Palmese et al. 2022 adaptive MQTT-SN QoS;
- Roy et al. 2018 application-aware MQTT-SN delay/loss;
- Saavedra et al. 2022 universal wireless-IoT testbed;
- Islam et al. 2026 STGen scalable protocol testbed;
- Akshatha et al. 2024 priority/timeliness MQTT;
- Bozorgi et al. 2026, `Internet of Things` 37, 101900, a particularly relevant same-journal store-and-forward / acknowledgment comparator under intermittent NB-IoT conditions;
- current Azure IoT Edge, HiveMQ Edge, and Azure MQTT Broker engineering capabilities.

The expansion **narrows mechanism novelty**; it does not add a new empirical claim.

Gaspar et al. 2026 remains included only as current practical MQTT stress-testing context. The manuscript does not attribute detailed method/results to it.

## Survey presentation doctrine

The paper now makes the survey work visible in the main text through a dedicated **Structured Literature Survey and Novelty Control** section and synthesis table, while Supplementary Material S1 preserves the full source-by-source collision matrix.

To avoid pseudo-systematic-review overclaiming, the manuscript explicitly states that this is a **targeted, claim-bounding submission-date novelty audit**, not:

- a PRISMA systematic review;
- a meta-analysis;
- an exhaustive bibliographic census;
- a prevalence estimate of the literature.

The audit exists to determine what the experimental paper may and may not claim.

## Red-hat finite repairs incorporated in R3-R2

Before final R3 freeze, the adversarial review found and corrected production-only defects:

1. a stale manuscript sentence saying Supplement S1 contained the earlier 17-group audit; corrected to **32 groups**;
2. survey composition and non-exhaustive claim-bounding purpose made explicit to prevent a reviewer from treating the counts as a pseudo-systematic-review claim;
3. internal retrieval-process wording around Gaspar et al. removed from the main research narrative while preserving conservative scope-only treatment;
4. the reproducibility ZIP renamed to `Supplement_S2_Reproducibility_Artifact.zip` to match the manuscript's S2 label.

No scientific result changed.

## Current exact production authority

Archive:
`WellPulse_P20D_R3R2_Elsevier_IoT_Submission_Package_2026-08-29.zip`

Drive ID:
`1Th-aO9_2wOnhD6EWyh5b6qml4fPmGDSb`

Archive size:
`2,157,349 bytes`

Archive SHA-256:
`6ca12912711f9f7b9f255bb161399244fac4572c7d902db0ad2270741b38496d`

Drive raw read-back: **exact hash match / PASS**.

Main PDF:
`WellPulse_Elsevier_IoT_P20D_R3R2_SubmissionDraft.pdf`

- pages: **19**;
- references: **32**;
- PDF SHA-256: `d68c7b19a0785a4c8527156e93213ee4ac0582cccaccd95c28f815da6641c768`;
- author metadata: **Ahmed Ayoub**;
- fonts: embedded;
- private IPv4 addresses: none found;
- unresolved citation markers: none found.

Supplement S1:
- PDF + CSV;
- CSV rows: **32**;
- classifications reproduce 17 narrowing / 15 no-impact / 0 blockers.

Supplement S2:
`Supplement_S2_Reproducibility_Artifact.zip`

SHA-256:
`99ed7c4dfc42c1f0f4b659489abf7ad328584f413c0318210dace29b4912b48d`

Isolated `python -I artifact_selfcheck.py`: **PASS**.

## Claim state

`P20D_R3_REFERENCES=32`

`P20D_R3_WORDING_NARROWING=17`

`P20D_R3_NO_IMPACT=15`

`P20D_R3_SCIENTIFIC_BLOCKERS=0`

`P20D_R3_NEW_EXPERIMENT_REQUIRED=NO`

`P20D_R3_NEW_EMPIRICAL_CLAIM_REQUIRED=NO`

`SUBMISSION_AUTHORIZED=NO`
