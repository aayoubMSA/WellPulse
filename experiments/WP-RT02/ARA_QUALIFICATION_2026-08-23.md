# WP-RT02 — ARA Rural OTA Validation Qualification

Date: 2026-08-23
Status: **QUALIFIED FOR ACCESS/CAPABILITY GATE — NOT YET EXECUTED**

## Purpose

WP-RT01 established controlled outage/recovery behavior on real FIT IoT-LAB A8 hardware. WP-RT02 is intended to add a distinct evidence layer: **real over-the-air rural wireless conditions with measured radio state**.

This is not pump, hydraulic, groundwater, motor, bearing, agronomic, or Siwa field validation.

## Platform decision

Primary follow-on: **ARA Wireless Living Lab, COTS 5G path**.

Why:

- ARA is an at-scale real-world living lab across rural/agricultural settings in central Iowa.
- ARA exposes field-deployed COTS 5G UEs and remote experiment containers.
- COTS UE APIs expose channel state such as RSRP, SINR, and RSRQ.
- RAN APIs expose configurable coverage-related parameters such as SSB power, configured maximum transmit power, UE pMAX, and RACH/cell-range controls.
- Current ARA material documents outdoor, kilometer-scale 5G experiments and per-packet measurements including throughput, delivery reliability, latency, jitter, and interference effects.
- ARA supports remote experimentation through its portal.
- The COTS path minimizes implementation burden compared with a first-pass SDR/O-RAN/BYOD experiment.

Official sources checked 2026-08-23:

- https://arawireless.org/about-ara/
- https://arawireless.org/cots-5g/
- https://arawireless.org/at-scale-real-world-srsran-experiments-in-ara/
- https://arawireless.org/open-nextg/
- https://arawireless.org/research/
- https://portal.arawireless.org/auth/login/

## Access status

- ARA portal currently exposes user-account registration.
- ARA documentation/training shows username/password and federated login workflows and remote resource reservation.
- Published ARA overview material shows users from multiple international universities.
- No Egypt-specific prohibition was found in the public material reviewed.
- **Actual account/project approval for MSA/Egypt remains unverified and is an explicit gate.**
- No ARA account, project, lease, or reservation has been created as part of this qualification.

## Candidate scientific claim

> A durable offline-first edge gateway preserves monitoring records across measured degradation and recovery of a real rural over-the-air wireless link.

This claim may only be used after WP-RT02 executes successfully.

## Proposed experimental architecture

Preferred resources, subject to portal availability and capability smoke:

1. A field-deployed ARA COTS 5G UE / UE Experiment Container.
2. A corresponding RAN Experiment Container if controlled radio degradation is permitted.
3. OS-CN / data-center endpoint as required for an end-to-end user-plane path.
4. WellPulse-compatible traffic generator / gateway workload in the experiment container.
5. Independent receiver/reconciliation endpoint.
6. ARA channel measurements synchronized with application records.

## Frozen workload skeleton

Preserve comparability with WP-RT01:

- Architectures: B0 non-durable baseline vs W1 WellPulse durable offline-first.
- Exactly 10,000 uniquely identified monitoring records per final cell unless a capability smoke demonstrates a scientifically necessary change.
- Three replicates per final condition/architecture cell.
- Record identity remains `run_id + boot_id + sequence`.
- Independent cloud reconciliation remains mandatory.
- Final duplicates must be measured independently, not inferred from publisher counters.

## Radio-condition skeleton — mechanism NOT YET FROZEN

The scientific conditions are:

- `R0_REFERENCE`: connected rural OTA reference condition.
- `R1_DEGRADED_CONNECTED`: reproducible degraded-but-connected radio condition.
- `R2_DETACH_RECOVERY`: reproducible connectivity-loss and recovery condition over the OTA path.

The exact mechanism for R1/R2 is deliberately **not frozen yet**. It must be selected only after an ARA capability smoke confirms which user-accessible RAN/UE controls are safe, isolated, repeatable, and permitted. Candidate controls include documented SSB-power / configured-max-transmit-power / UE-pMAX / cell-range parameters, but none is assumed to cause a specific RF state until measured.

Do not substitute an application-layer firewall outage for R2; WP-RT01 already supplies that evidence. WP-RT02 must add a materially distinct real-radio layer.

## Required synchronized measurements

Application layer:

- generated records
- local committed records for W1
- cloud unique records
- permanent missing records
- final duplicates
- completeness
- reconnect/recovery time
- backlog-drain time
- queue high-water / oldest queued age if available

Radio/network layer:

- RSRP
- SINR
- RSRQ
- UE attach/detach/recovery timestamps where available
- packet delivery reliability / loss
- latency and jitter where the ARA path exposes defensible measurements
- throughput as context, not a primary WellPulse success metric

## Final success rule

The strongest desired W1 result under `R2_DETACH_RECOVERY` is:

- 10,000 generated
- 10,000 unique final cloud records
- 0 permanent missing
- 0 final duplicates
- successful recovery after measured radio connectivity restoration

No fixed expected loss is predeclared for B0 because the exact duration and severity of the real-radio impairment will be determined by the frozen ARA mechanism after capability smoke.

## Access/capability gates before any final matrix

1. Account/project eligibility for the MSA researcher is approved.
2. COTS UE Experiment Container is accessible remotely.
3. End-to-end user-plane traffic from the field UE path to an independent endpoint is proven.
4. RSRP/SINR/RSRQ can be logged with timestamps.
5. At least one permitted RAN/UE control can reproducibly create `R1_DEGRADED_CONNECTED`.
6. A permitted control can create a bounded `R2_DETACH_RECOVERY` without contaminating other users/resources.
7. WellPulse workload can run without redesigning the application architecture.
8. Raw evidence, environment metadata, resource IDs, code commit, and checksums can be preserved.

If gates 5–6 cannot be satisfied, do not force the ARA route. Reframe ARA as an observational rural-radio evidence layer or move the controlled real-radio experiment to another suitable testbed.

## Kill / pivot rules

Kill or pivot the COTS-ARA path if any of the following holds:

- access requires unacceptable coordination or on-site handling;
- only synthetic/application-layer network impairment is available;
- no timestamped radio metrics can be paired with WellPulse records;
- custom application traffic cannot traverse the real field UE path;
- R1/R2 cannot be created reproducibly and safely;
- the experiment requires major 5G stack development unrelated to WellPulse.

In those cases, evaluate NITOS/POWDER or a different ARA modality; do not add wireless-stack research for its own sake.

## Evidence boundary

A successful WP-RT02 would support wording such as **“real rural over-the-air wireless validation in the ARA living lab”** for the communications/resilience layer.

It would still not support wording implying:

- validation at the Siwa well;
- solar-pump mechanical/hydraulic validation;
- groundwater validation;
- real inverter/Modbus hardware compatibility unless separately tested;
- real pump fault diagnosis.
