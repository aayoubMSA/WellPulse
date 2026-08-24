# POWDER G4 live controlled-RF discovery — 2026-08-25

Status: **DISCOVERY PASS / ALLOCATION NOT YET ATTEMPTED**

Evidence class: **INFRASTRUCTURE_DISCOVERY_ONLY_NON_SCORED**

## Live profile discovery

Using the authenticated POWDER Portal UI, the current profile search for `controlled` exposed `srslte-controlled-rf` under project `PowderProfiles`.

Observed live metadata:

- Profile: `srslte-controlled-rf`
- Project: `PowderProfiles`
- Created by: `dmaas`
- Latest version: `0`
- Repo based: `Yes`
- Repo hash: `a6da9656` (`refs/heads/master`)
- Last updated: `2020-06-03 16:14:23`

The profile description states that it instantiates an end-to-end LTE network in a controlled RF environment with wired connections between UE and eNB.

## Parameterization

Observed UE choices:

- `srsLTE UE (B210)`
- `COTS UE (Nexus 5)`

For the WellPulse controlled-RF lane, `srsLTE UE (B210)` is the preferred candidate because it keeps both UE and eNB sides programmable and reproducible.

No experiment was created during this discovery step.

## Live resource-availability snapshot

The authenticated POWDER Resource Availability view at approximately 2026-08-25 00:10 Africa/Cairo showed:

- multiple attenuator-matrix nodes available (`Yes`), including several `nuc*` resources and `x310-1`;
- generic server availability including `d430: 5`, `d710: 115`, and others;
- the Indoor OTA Lab resources were currently unavailable and showed the next free interval beginning 2026-08-27 06:00;
- Paired Radio Workbenches showed `oai-wb-b1` and `oai-wb-b2` available;
- several rooftop/dense-deployment resources were also available.

This availability page is a global/current resource snapshot. It does **not** by itself prove that project `WellPulse` is entitled to, or can successfully allocate, the exact NUC5300/B210 pair required by `srslte-controlled-rf`.

## Interpretation

**G4 discovery sub-gate: PASS.**

A current controlled physical-RF candidate has been identified in the live Portal and its parameterization has been inspected. The next step is a single manual, non-scored allocation attempt using `srsLTE UE (B210)` followed by READY -> manifest/topology verification -> explicit-key SSH -> clean terminate.

G4 overall remains **PENDING** until that lifecycle passes.

No scientific claim is supported by this discovery step. Scientific completion remains **20%** and `scored_runs_authorized=false`.
