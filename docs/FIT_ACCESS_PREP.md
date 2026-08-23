# FIT IoT-LAB access and smoke preparation — WellPulse

Status: prepared, not executed. Account creation/reservation requires Dr. Ahmed's explicit approval.

## Verified platform facts
- FIT IoT-LAB remains an open-access remote IoT testbed.
- A8-M3 nodes run embedded Linux and are reached through an IoT-LAB SSH frontend, then by root SSH to the allocated A8 node.
- The public FIT MQTT broker is `mqtt4.iot-lab.info:8883`, TLS only.
- Authenticated users are restricted to `iotlab/<login>` topics and subtopics.
- On shared SSH frontends, credentials should be stored in protected mosquitto config files rather than exposed on command lines.

## Minimum reservation plan
Use one A8-M3 node at Saclay for the first smoke test. Do not reserve multiple nodes until the single-node capability gate passes.

Illustrative official CLI sequence after account/SSH configuration:

```bash
iotlab-auth -u <login>
iotlab-experiment submit -n wellpulse-fit-smoke -d 30 -l 1,archi=a8:at86rf231+site=saclay
iotlab-experiment wait
iotlab-experiment get -i <exp_id> -n
ssh <login>@saclay.iot-lab.info
ssh root@node-a8-<n>.saclay.iot-lab.info
```

Exact node identifier must come from the live reservation result; never hard-code it.

## Smoke objectives
1. SSH access and boot success.
2. OS/Python/runtime inventory.
3. writable storage and identification of any experiment-persistent/shared mount.
4. free disk space and UTC clock behavior.
5. outbound DNS/TCP/TLS reachability to `mqtt4.iot-lab.info:8883`.
6. authenticated MQTT publish/receive on `iotlab/<login>/wellpulse/smoke` without placing credentials in logs.
7. probe whether `tc`/`netem` exists and is permitted; do not assume it.
8. copy all smoke logs off the node and checksum them.

## Kill rule
If the A8 environment cannot run the minimal WellPulse Python stack, cannot make the required authenticated TLS MQTT connection, or requires substantial custom platform work, stop FIT integration and reassess NITOS/POWDER rather than over-engineering WellPulse.

## Evidence boundary
This smoke test is capability evidence only. It is not a final WP-RT01 run and must not be included as publication performance data.
