# POWDER G4 live controlled-RF discovery — 2026-08-25

Status: **DISCOVERY PASS / ALLOCATION BLOCKED AT CURRENT TIME**

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

The B210 selection exposes a topology with `rue1` and `enb1`, corresponding to the controlled-RF NUC5300/B210 path.

No experiment has yet been created during this G4 qualification attempt.

## Live resource-availability snapshot

The authenticated POWDER Resource Availability view at approximately 2026-08-25 00:10 Africa/Cairo showed:

- multiple attenuator-matrix nodes available (`Yes`), including several `nuc*` resources and `x310-1`;
- generic server availability including `d430: 5`, `d710: 115`, and others;
- the Indoor OTA Lab resources were currently unavailable and showed the next free interval beginning 2026-08-27 06:00;
- Paired Radio Workbenches showed `oai-wb-b1` and `oai-wb-b2` available;
- several rooftop/dense-deployment resources were also available.

This availability page is a global/current resource snapshot. It does **not** by itself prove that project `WellPulse` is entitled to, or can successfully allocate, the exact NUC5300/B210 pair required by `srslte-controlled-rf`.

## Schedule/admission-control result

After selecting:

- profile `srslte-controlled-rf`;
- UE type `srsLTE UE (B210)`;
- project `WellPulse`;
- experiment name `WP-G4-CTRL-RF`;

and advancing to the Schedule step, the live Portal displayed this admission-control warning:

> Unable to start at this time; other projects are using, or have reservations for, node/type `nuc5300`.

The Portal therefore exposed an actual hidden/late-bound dependency relevant to this profile: **`nuc5300` availability/admission control**.

No `Finish` action was taken and no G4 experiment/resource allocation was created.

## Interpretation

**G4 discovery sub-gate: PASS.**

**Immediate allocation at the observed time: BLOCKED by `nuc5300` usage/reservations.**

This is not an entitlement failure and not a scientific failure. The next defensible action is to use the POWDER reservation/scheduling mechanism to identify and reserve a future window for the required `nuc5300` resources under project `WellPulse`, then instantiate exactly one manual non-scored G4 lifecycle qualification inside that reservation.

G4 overall remains **PENDING** until READY -> topology/manifest verification -> explicit-key SSH -> controlled-RF lifecycle sanity -> clean termination -> zero active usage all pass.

No scientific claim is supported by this discovery step. Scientific completion remains **20%** and `scored_runs_authorized=false`.
