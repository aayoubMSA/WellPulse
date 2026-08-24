# POWDER G4 live controlled-RF discovery — 2026-08-25

Status: **DISCOVERY PASS / RESERVATION APPROVED / EXPERIMENT SCHEDULED / LIFECYCLE PENDING**

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

## Reservation result

A manual reservation request was created under project `WellPulse` for two NUC5300/B210 resources represented by individual nodes:

- `Emulab / nuc1 / 1`
- `Emulab / nuc2 / 1`

Reservation settings:

- OTA Lab: **not selected**
- frequency-range fields: left blank for this conducted-RF qualification request
- class reservation: **No**
- requested window: **2026-08-25 19:00 to 22:00** (Africa/Cairo operator context)
- purpose: non-scored G4 infrastructure qualification only

The POWDER Schedule page showed the reservation row with status **Approved** and the same start/end window.

## Scheduled G4 experiment

After the approved reservation was visible, the manual G4 experiment was scheduled against the same window.

Observed live Portal state:

- Name: `WP-G4-CTRL-RF`
- State: `scheduled`
- Profile: `srslte-controlled-rf`
- RefSpec: `refs/heads/master (a6da9656)`
- Creator: `aayoub`
- Project: `WellPulse`
- Created: `Aug 25, 2026 12:39 AM`
- Scheduled: `Aug 25, 2026 7:00 PM`
- Expires: `Aug 25, 2026 10:00 PM`
- Current Usage at scheduling time: `0 Node Hours`

The Portal also displayed the banner that the experiment is scheduled to start later and that a reservation group is starting soon in project `WellPulse`.

No resources are active yet. No RF workload, WellPulse workload, or scored scientific run has executed.

## Interpretation

**G4 discovery sub-gate: PASS.**

**Required controlled-RF reservation: APPROVED for 2026-08-25 19:00–22:00.**

**Manual G4 qualification experiment: SCHEDULED for the approved reservation window.**

G4 overall remains **PENDING** until the scheduled experiment reaches READY and passes exact topology/resource binding verification, explicit-key SSH, controlled-LTE lifecycle sanity, clean termination, and zero active usage.

Exact next action: at or just after **2026-08-25 19:00 Africa/Cairo**, open `WP-G4-CTRL-RF`, wait for READY, and verify the actual allocated `rue1`/`enb1` NUC/B210 bindings before any SSH or LTE command is executed.

No scientific claim is supported by this discovery/reservation/scheduling step. Scientific completion remains **20%** and `scored_runs_authorized=false`.
