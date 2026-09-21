# WellPulse IEEE Revival — Q0 Instrumentation Qualification Status

## Authority / scope
This record belongs to the post-rejection R4/Q0 revival path. It does not reopen the historical submitted manuscript as authority. No scored experiment has been executed.

## Critical R4 correction discovered during Q0
Static inspection of the frozen FIT runner `experiments/WP-RT01/fit_runner_py35.py` shows that source generation is not driven by a configured periodic interval. Therefore the earlier R4 rule using a nominal `tau0` was invalid. The canonical Drive revival record now supersedes that rule with semantic endpoint misclassification:

- M2 = final publisher-side PUBACK coverage for H.
- M3 = receiver-side completion of H.
- POSITIVE requires a clock-resolved M3 > M2 and receiver incompleteness at M2.
- Timing magnitude is reported; no arbitrary source-cycle threshold is imposed.

## Frozen implementation facts recovered
- Frozen FIT runner: `experiments/WP-RT01/fit_runner_py35.py`.
- W1 persists records in SQLite, then serially drains the historical queue after reconnect.
- `Publisher._on_connect` previously stored only a Boolean and did not preserve the CONNACK event timestamp.
- `Publisher.publish` waited for QoS-1 completion but did not persist record_id <-> packet-id <-> PUBACK attribution.
- Receiver uses record_id primary-key deduplication.
- C1 has no process restart; outage is iptables REJECT on broker TCP/8883 and is explicitly socket-verified.

## Q0 sidecar implementation
Branch: `revival-r4-q0-instrumentation`

File:
`experiments/WP-RT01/fit_runner_q0_instrumented_py35.py`

Latest commit:
`c2b724b59577f4d9f6d2eb7c81dd9e80a3d2d83a`

Local SHA-256 of the verified wrapper:
`f231fc8a8c689836d99ec0fd809022723daad1d428b76e794566cb82cfd928f0`

Design:
- imports and reuses frozen `main()`, queue semantics, outage sequencing, payload generation, and inherited `Publisher.publish()`;
- adds sidecar logs only;
- captures CONNACK directly through the existing paho callback;
- maps record_id <-> MQTT packet id <-> publish attempt before PUBACK callback attribution;
- retains unmatched PUBACKs explicitly as UNRESOLVED;
- logs source-generation events without modifying wire payload bytes;
- logs OUTAGE_CONFIRMED and a fixed 250 ms retry user-plane restoration probe;
- remains Python-3.5-syntax compatible.

## Local qualification evidence
- PY35 syntax gate: PASS.
- Q0-1 frozen Publisher.publish method reused: PASS.
- Q0-2 CONNACK event capture logic: LOCAL PASS; live paho/FIT confirmation still required.
- Q0-3 packet-id reuse mapping: LOCAL PASS using deliberate packet-id reuse.
- Q0-4 receiver duplicate reconciliation: PASS; deliberate duplicate input produced 2 unique records from 3 arrivals.
- Q0-5 local logging-overhead precheck: PASS.
  - baseline 5000-record mock generation: 0.014039 s
  - instrumented: 0.041357 s
  - incremental overhead: ~5.464 us/record
  - instrumented p99 inter-call interval: ~20.380 us
  - maximum observed local interval: ~617.700 us
  - this does not replace the required live FIT healthy-connectivity qualification.
- Q0-7 treatment event logic: LOCAL PASS; live FIT outage/restoration confirmation still required.

## Gate state
Q0-1: PASS
Q0-2: PREQUALIFIED — LIVE FIT confirmation required
Q0-3: PREQUALIFIED — LIVE FIT confirmation required
Q0-4: PASS
Q0-5: PREQUALIFIED — LIVE FIT qualification required
Q0-6: WAITING — live clock-bound evidence required
Q0-7: PREQUALIFIED — LIVE FIT qualification required

Overall:
`Q0_GATE=WAITING_LIVE_FIT_QUALIFICATION`

## Remaining delta
One bounded, non-scored FIT qualification session should close Q0-2/Q0-3/Q0-5/Q0-6/Q0-7 together. It must:
1. run healthy connectivity with frozen and instrumented code to compare cadence/total runtime;
2. demonstrate real CONNACK and mapped PUBACK events;
3. collect pre/post clock-bound evidence for source and receiver;
4. execute one non-scored C1 outage/restoration with no process restart;
5. preserve and hash raw sidecar and receiver evidence.

No C0/T1 scientific R5 run is authorized until this Q0 live gate passes.
