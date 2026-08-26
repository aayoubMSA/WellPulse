# WP-PWD01 — B2 Durable MQTT Client Semantics Gate v1

**Date:** 2026-08-26  
**Evidence class:** LOCAL NON-SCORED PRE-SCORE COMPARATOR QUALIFICATION  
**Status:** FROZEN FOR LOCAL EXECUTION  
**Scored runs authorized:** **NO**

## Purpose

Qualify or reject `B2_MQTT_DURABLE_CLIENT` before any scored POWDER campaign. The gate tests the exact reviewer-relevant semantic claim: can a standard Eclipse Paho client preserve QoS1 records generated while disconnected across destruction/restart of the client process, then deliver them after connectivity returns?

This gate does not compare B2 against WellPulse scientifically, does not estimate an effect, does not touch POWDER, and does not authorize WP3.

## Candidate B2 configuration

- client: Eclipse Paho Java MQTT v3 client;
- pinned library: `org.eclipse.paho.client.mqttv3:1.2.5`;
- MQTT protocol: v3.1.1;
- QoS: 1;
- stable client identity within one trial/restart;
- `cleanSession=false`;
- file-backed client persistence: `MqttDefaultFilePersistence`;
- disconnected buffering: enabled;
- disconnected buffer size: 4096;
- disconnected buffer persistence: enabled via `setPersistBuffer(true)`;
- delete-oldest on full buffer: disabled;
- local broker only for this semantics gate.

The B2 runtime/language difference from B1/W1 is explicit and is why B2 remains a sensitivity comparator rather than replacing the matched primary B1 arm.

## Frozen local failure sequence

Run exactly three independent semantics trials. Each trial uses a fresh client ID, topic and persistence directory:

1. start a local MQTT broker;
2. start B2 and connect with the frozen options;
3. terminate the broker to create an actual network-service outage;
4. confirm the client detects disconnection;
5. generate exactly five identifiable QoS1 records while disconnected;
6. confirm the records enter the persistent disconnected buffer;
7. terminate the B2 process without a graceful MQTT disconnect;
8. verify file-backed persistence exists before recovery;
9. restart the broker and a receiver;
10. recreate B2 with the same client ID and persistence directory;
11. reconnect with `cleanSession=false`;
12. verify all five pre-restart records arrive at the receiver;
13. verify five unique identities, no permanent loss, and the disconnected buffer drains.

## PASS rule

`PASS` only if all three independent trials demonstrate:

- 5/5 unique pre-restart records delivered after process restart;
- zero permanently missing records;
- persistent store present before recovery;
- no manual replay logic outside the standard Paho client;
- the same pinned client/options are used in all three trials.

Duplicates, if any, are preserved and reported rather than hidden. Any missing record or failure to restore the persistent disconnected buffer is `B2_SEMANTICS_FAIL` and blocks inclusion of B2 in the scored sensitivity matrix pending investigation.

## Decision after PASS

A PASS qualifies B2 semantically but does not yet create scored B2 cells. The smallest intended scientific amendment remains compact B2 sensitivity in `S2_HARD_OUTAGE` and `S3_OUTAGE_RESTART`; exact replication and analysis must be frozen separately before any scored B2 execution.
