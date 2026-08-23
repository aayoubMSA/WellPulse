# WellPulse RF Platform Adapters

Purpose: keep the WellPulse workload, receiver, reconciliation, and evidence semantics platform-neutral while isolating testbed-specific resource and RF-control logic.

## Common adapter contract
Each adapter must expose equivalent operations conceptually:

1. `describe_resources()`
   - platform name
   - experiment/project ID
   - node/container/UE/RAN identifiers
   - RF path type: conducted / OTA / outdoor OTA

2. `reference_state()`
   - establish R0
   - return/log platform-native RF state and available metrics

3. `degraded_connected_state()`
   - establish R1 using genuine RF-layer control
   - log requested and observed control values
   - confirm user-plane traffic remains connected

4. `loss_state()`
   - establish R2 using genuine RF-layer control or OTA detach mechanism
   - log transition timestamp and link state

5. `restore_state()`
   - restore RF path
   - log restoration timestamp
   - confirm user-plane traffic recovers

6. `sample_metrics()`
   - emit timestamped records compatible with `rf_event_schema.json`

7. `capture_manifest()`
   - preserve platform/resource IDs, config, commit SHA, timestamps, and evidence locations

## Hard boundary
Adapters must not contain WellPulse buffering/reconciliation logic. They only manipulate/observe the testbed environment and emit synchronized RF events.

No adapter may substitute application-layer blocking (`iptables`, broker ACLs, synthetic packet drops) for the intended RF impairment.

## POWDER adapter target
Preferred first resource: `srs-rf-matrix`.

Expected responsibilities:
- identify radios/endpoints and matrix resources;
- set/read programmable attenuation or equivalent RF controls;
- establish R0/R1/R2;
- preserve exact profile/resource identifiers and settings;
- emit available link/RF metrics.

Do not freeze attenuation values until the capability smoke demonstrates a stable connected-degradation region and a reproducible loss/recovery boundary.

## COSMOS/ORBIT adapter target
Preferred first resource: ORBIT `sb4` RF Attenuator Matrix.

Expected responsibilities:
- identify sender/receiver/radio nodes and matrix paths;
- manipulate programmable attenuation using the platform-supported mechanism;
- establish R0/R1/R2;
- log exact node and reservation identifiers;
- emit available RF/link metrics.

Outdoor ORBIT or COSMOS 5G OTA is optional and only justified if it adds a distinct claim after controlled-RF evidence.

## ARA adapter target
Preferred first resource: field-deployed COTS 5G UE with corresponding RAN/core path where permitted.

Expected responsibilities:
- identify UE/RAN/core resources;
- preserve field-site/resource IDs;
- emit timestamped RSRP/RSRQ/SINR and attach/detach state where available;
- use only permitted RF/RAN controls for R1/R2;
- prove end-to-end traffic traverses the real field UE path.

ARA should not be reduced to an application-layer outage test; FIT already established that claim.

## Adapter acceptance gate
An adapter is acceptable only when:
- it controls or observes the real intended RF path;
- R0/R1/R2 are repeatable;
- timestamps align with WellPulse application events;
- the workload runs without architecture redesign;
- evidence is durable and reproducible enough for later audit.
