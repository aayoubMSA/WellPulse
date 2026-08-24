# WP0 — Durable MQTT Comparator Audit — 2026-08-25

**Status:** MATERIAL PRE-SCORE FINDING / PROTOCOL REVIEW REQUIRED

**Scope:** This note supersedes the earlier conclusion in `WP0_RELATED_WORK_BENCHMARK_2026-08-25.md` that no further comparator review was required. It does **not** block G4 infrastructure qualification. It **does** block any move into scored POWDER execution until the comparator decision below is resolved and frozen.

## 1. Why this audit was triggered

The first WellPulse novelty audit correctly replaced the FIT `B0_PUBLISH_ONLY` lower-bound with `B1_MQTT_QOS1`: Paho Python MQTT v3.1.1, QoS1, automatic reconnect, `clean_session=False`, bounded volatile outgoing state, and no application-level disk durability/reconciliation.

A deeper pre-G4 survey then tested a stronger reviewer question:

> Is a volatile Paho Python client actually the strongest defensible representation of standard MQTT client reliability across process restarts?

The answer is **no**. Other standard Eclipse Paho client implementations provide durable client-side persistence, and Paho Java also exposes persistent disconnected buffering.

## 2. Authoritative client-library evidence

### 2.1 Paho Python — the current B1 implementation

Official Eclipse Paho Python documentation states that with `clean_session=False`, the client session is stored only in memory and is not persisted. When the client process is restarted/recreated, this state is lost; unacknowledged QoS1/QoS2 publications may therefore be lost.

This remains a valid and common Python implementation baseline, but it must be described precisely as a **matched volatile Paho Python baseline**, not as the strongest durability standard available in the MQTT ecosystem.

### 2.2 Paho Java — file-backed persistence across client restarts

Official Eclipse Paho Java documentation states:

- `MqttDefaultFilePersistence` is the default persistence mechanism unless another store is supplied;
- reliable QoS1/QoS2 delivery across network/client restart requires messages to be safely stored;
- the persistence package explicitly distinguishes file persistence from memory persistence, with memory persistence described as unsuitable when reliability across client/device restarts is required;
- `MqttAsyncClient` documents the default file-based persistence and recommends persistent storage with `cleanSession=false` for reliable delivery.

Therefore, client-process durability is not unique to a custom WellPulse queue at the MQTT transport implementation level.

### 2.3 Paho Java — disconnected/offline buffering can itself be persisted

`DisconnectedBufferOptions` exposes:

- buffer enable/disable;
- buffer size;
- `setPersistBuffer(boolean)` / `isPersistBuffer()`;
- delete-oldest policy.

The default disconnected buffer is disabled and non-persistent, but persistence can be enabled.

Current Eclipse Paho Java source shows that, when the disconnected buffer is configured as persistent, a publish submitted while disconnected is passed to `persistBufferedMessage(...)` before it is inserted into the disconnected message buffer. The persistence state uses a dedicated buffered-message namespace. Earlier Paho source also shows restoration logic for these buffered outgoing messages from the persistence store.

This is a material comparator fact: a standard open-source MQTT client can be configured to persist outbound messages that arise while disconnected, not only messages already in flight.

### 2.4 This does not make WellPulse equivalent to Paho persistence

Transport-level persistence is not automatically the same architecture as WellPulse.

WellPulse additionally defines application-level semantics:

- stable telemetry record identity independent of MQTT packet/message IDs;
- SHA-256 payload integrity checks;
- explicit durable pending/sent application state;
- application-controlled replay;
- idempotent receiver keyed by record identity;
- deterministic end-to-end reconciliation against the generated ledger;
- evidence sufficient to distinguish duplicates, corruption, unexpected records, permanent missing records, and late delivery.

MQTT QoS1 remains an at-least-once transport guarantee; duplicate delivery is permissible. Durable transport state therefore does not eliminate the scientific relevance of application-level identity/idempotence/reconciliation. But it can reduce or eliminate a simplistic claim that WellPulse wins merely because the alternative forgets outbound records when its process restarts.

## 3. Reviewer attack now considered credible

A reviewer could state:

> The paper compares an application-level disk queue to Paho Python, whose own documentation says persistent client state is not implemented. Eclipse Paho Java provides file-backed persistence and persistent disconnected buffering. Why was a durable standard client not evaluated?

This attack is strong enough that it must be addressed **before scored runs**, not left for discussion after data collection.

## 4. Comparator options considered

### Option A — keep B1 only

Keep `B1_MQTT_QOS1` as the sole comparator and clarify that it is a matched Paho Python baseline.

**Advantage:** cleanest controlled B1/W1 comparison because both use identical low-level code.

**Problem:** insufficient protection against the durable-client reviewer attack.

**Verdict:** not preferred as the final paper design without an external durable-client sensitivity check.

### Option B — replace B1 with a durable Java/C MQTT client as primary comparator

Use Paho Java/C durable persistence as the primary baseline.

**Advantage:** very strong practical comparator.

**Problem:** changes language/runtime/client implementation at the same time as durability semantics, introducing a major confound into the primary paired experiment.

**Verdict:** not preferred as the primary inferential comparator.

### Option C — retain matched B1 and add a targeted durable MQTT comparator B2

Recommended route.

- retain `B1_MQTT_QOS1` as the matched same-implementation comparator for the full controlled campaign;
- add `B2_MQTT_DURABLE_CLIENT` as an external strong comparator/sensitivity analysis focused on the scenarios where persistence matters most, especially hard outage and process restart;
- implement B2 using an authoritative standard client configuration with documented file persistence and persistent disconnected buffering;
- treat B2 as a secondary/sensitivity comparator rather than pool it into the B1/W1 paired primary inference;
- record runtime/language/client differences explicitly.

This preserves causal cleanliness while answering the strongest practical reviewer objection.

**Provisional preference:** Option C.

## 5. Minimal decision experiment before protocol amendment

Before changing the scored matrix, run a small **local, non-scored comparator semantics gate** that proves the exact candidate B2 behavior:

1. stable client identity;
2. QoS1;
3. persistent session / clean-session setting appropriate to the client version;
4. file-backed client persistence;
5. persistent disconnected buffer enabled;
6. generate records while network is unavailable;
7. kill/restart the client process during the outage;
8. restore connectivity;
9. verify which pre-restart/offline records are actually delivered;
10. capture duplicates and any loss;
11. repeat enough times only to validate semantics, not to estimate a scientific effect.

If B2 does not demonstrably preserve the required offline/process-restart state, do not include it merely because documentation suggests it should. If it does, freeze its exact version/options and determine the smallest non-inflated B2 sensitivity matrix.

## 6. Provisional smallest B2 scientific matrix

Do **not** add B2 to every condition by default.

If the local semantics gate passes, the highest-value compact comparison is likely:

- `S2_HARD_OUTAGE`: B2 vs W1, small fixed replication;
- `S3_OUTAGE_RESTART`: B2 vs W1, small fixed replication.

The objective is not another fully powered three-arm study. It is a reviewer-defense sensitivity check answering:

> Does WellPulse's record-level integrity/reconciliation provide measurable value beyond a standard MQTT client configured with durable transport persistence?

Exact replication and analysis must be frozen before any scored B2 execution.

## 7. Impact on G4 and current schedule

**G4 is unaffected.**

G4 asks whether the selected POWDER profile can provide a valid controlled physical-RF lifecycle:

`scheduled -> READY -> manifest/resource binding -> SSH -> controlled LTE sanity -> clean teardown -> 0 Node Hours`

No B1/W1/B2 scientific result is generated during G4.

Therefore:

- keep the approved/scheduled G4 window;
- do not alter tonight's infrastructure qualification;
- do not authorize scored runs after G4 merely because G4 passes;
- insert this comparator review plus B2 local semantics gate before the scored campaign is frozen.

## 8. Revised gate decision

**Related-work/benchmark status:** PASS FOR G4, **REVIEW REQUIRED FOR SCIENTIFIC COMPARATOR FREEZE**.

**Scientific completion:** unchanged at 20%.

`scored_runs_authorized = false`

The current protocol v0.4 remains the working design for infrastructure and calibration planning, but its claim that B1 is the sufficient strong standard comparator is now **under review**. No scored run may begin until the comparator decision is explicitly frozen.

## 9. Source trail

Authoritative sources reviewed 2026-08-25:

- Eclipse Paho MQTT Python documentation — known limitation: MQTT v3 persistent client session is in-memory only and is lost across client-process restart.
- Eclipse Paho Java `MqttClient`, `MqttAsyncClient`, persistence package and `MqttDefaultFilePersistence` documentation — file-backed persistence across client/network restarts.
- Eclipse Paho Java `DisconnectedBufferOptions` documentation — optional persistent disconnected buffering.
- Eclipse Paho Java current source (`ClientComms`) — persistent disconnected buffer invokes `persistBufferedMessage(...)` before buffering; reconnect logic drains the buffer.
- Eclipse Paho Java source history (`ClientState`) — persisted `sb-` buffered outbound messages are restored into outbound state.

This audit should be read together with:

- `docs/WP0_NOVELTY_VENUE_LOCK_2026-08-24.md`
- `docs/WP0_RELATED_WORK_BENCHMARK_2026-08-25.md`
- `experiments/WP-PWD01/protocol.md`
