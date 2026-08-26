# WellPulse — RS-2 LTE Recovery Mechanism Review

**Date:** 2026-08-26  
**Stage:** POST-H1 / PRE-AMENDMENT / PRE-SCORE  
**Scientific completion:** 20%  
**H:** `UNFROZEN`  
**Scored runs:** `NOT AUTHORIZED`  
**Raw H1 record-level bundles:** unavailable from user-accessible persistent storage; backend recovery pending.

## 1. RS-2 question

Determine whether the H1 non-recovery can be removed by a **bounded, architecture-neutral LTE configuration/runtime repair** that preserves the frozen RF protocol, or whether the study must prospectively separate RF restoration from usable network-service restoration.

RS-2 does not authorize a new POWDER reservation, does not alter Q0–Q3, does not reclassify H1, and does not amend H.

## 2. Evidence basis

### Project evidence admitted

- H1 run `wp2h1-a1-20260826-001` classified `VALID_W1_RECOVERY_FAILURE`.
- Q3 held at 55 dB for `120.000117905 s` and Q0 was restored.
- Pre-outage LTE user plane passed through `tun_srsue`.
- After RF restoration, `tun_srsue` remained present at `172.16.0.2/24` and routing still pointed to `172.16.0.1`, but packets did not traverse.
- eNB later recovered usable uplink decoding, including CRC-OK PUSCH with strong SNR; therefore the eNB/radio process had not simply crashed.
- EPC/MME/SPGW diagnostics showed repeated attach/context churn, including `UE Context already exists`, active GTP-C conflicts, failed old-tunnel deletion, and successive SPGW UE address allocations `.3` through `.7` while the UE tunnel remained `.2`.
- UE-only restart failed after 96 s despite cell discovery, random access and RRC connection.
- EPC/eNB reset while UE stayed live failed to restore a usable user plane after 61 s.
- Coordinated clean-order restart (`stop UE -> EPC -> eNB -> fresh UE`) restored the original `.2` UE address, route and 10/10 Q0 ping.
- The recovered path then passed the exact LTE/TLS/MQTTv3.1.1/QoS1/SHA-256 application-path qualification in 3/3 fresh sessions.

### External implementation/specification evidence

The srsRAN 4G EPC implementation stores NAS contexts keyed by IMSI and explicitly logs `UE Context already exists` when an IMSI context is already present. Current srsRAN source also contains explicit logic for service requests and for releasing a prior ECM context when appropriate. Historical srsEPC issue #154 documents that after radio-link failure or RRC inactivity the UE attempts NAS service recovery, and incomplete service-request handling can trap recovery in a loop. Later srsRAN issue reports demonstrate that repeated connect/disconnect operation can produce stale SPGW/GTP-C state and repeated address allocation behavior closely resembling the H1 symptoms.

3GPP TS 24.301 identifies EMM cause #9 as `UE identity cannot be derived by the network`; among the triggering conditions is a service request whose temporary identity/context or integrity state cannot be validated. H1 UE diagnostics included `Received service reject with EMM cause=0x9`, which is therefore consistent with a stale/mismatched NAS/MME context rather than with an application-layer transport failure.

## 3. Layer-by-layer failure chain

| Layer | H1 observation | RS-2 interpretation |
|---|---|---|
| RF attenuation | Q3 applied and later Q0 restored | Treatment executed correctly |
| PHY/eNB | uplink decoding later recovered, eNB alive | RF/RAN process not the dominant persistent blocker |
| RRC | cell discovery/random access/RRC connection repeatedly possible | radio access partially recovered |
| NAS/MME | service reject cause 0x9; repeated attach/context churn | stale/mismatched UE security/identity/session context likely |
| GTP-C/SPGW | active-context conflict, failed old-tunnel deletion, successive IP allocations | bearer/session cleanup and IP-state consistency failed |
| UE IP/tunnel | UE retained `172.16.0.2` while core allocated `.3`–`.7` | control-plane/user-plane state diverged |
| IP user plane | Q0 post-restore ping failed | usable service not restored |
| MQTT/WellPulse | disconnected and backlog remained | downstream consequence, not demonstrated root cause |

The strongest causal interpretation supported by current evidence is therefore:

`long RF outage -> RLF/NAS recovery -> stale or inconsistent EPC/session context -> UE/core address/tunnel divergence -> no usable user plane -> MQTT cannot reconnect -> WellPulse backlog cannot drain`.

## 4. Candidate repair hypotheses

### HYP-A1 — RF/RAN tuning problem

**Evidence against:** Q0 was physically restored; eNB later decoded uplink successfully; random access/RRC connection was repeatedly possible; clean-order restart restored the same RF path without changing Q0/Q3 values.

**Verdict:** `REJECT as dominant cause`.

### HYP-A2 — MQTT/TLS/application problem

**Evidence against:** user-plane ping already failed below MQTT; after clean-order LTE recovery the unchanged TLS/MQTT/QoS1 application path passed 3/3.

**Verdict:** `REJECT as dominant cause`.

### HYP-A3 — UE-only transient state

**Evidence against:** a fresh UE process still failed while the old EPC/eNB state remained.

**Verdict:** `REJECT as sufficient repair`.

### HYP-A4 — EPC/eNB-only stale state

**Evidence against:** resetting EPC/eNB while leaving the UE live did not recover service. This implies that both sides must be brought back to a mutually clean state, not only the core/RAN.

**Verdict:** `REJECT as sufficient repair`.

### HYP-A5 — cross-node LTE session-context consistency failure

**Evidence for:** stale UE/MME/GTP-C warnings, EMM cause #9, successive SPGW IP allocations, preserved stale UE tunnel address, failure of one-sided resets, and success of a clean ordered reset of both endpoints.

**Verdict:** `SUPPORTED / dominant working diagnosis`.

## 5. Can Strategy A be closed as a bounded configuration repair?

**No. Not from current evidence.**

A configuration-only fix (timer, RLF threshold, paging timer, attach timer, APN parameter, etc.) has not been demonstrated or uniquely identified. Changing such parameters without a discriminating mechanism would be speculative and could alter the outage treatment itself.

The demonstrated clean-order restart is deterministic operationally, but it is not an autonomous LTE recovery fix. It changes service state by explicitly reinitializing UE, EPC and eNB.

Upgrading the old srsLTE/srsRAN runtime may plausibly improve context-management behavior, but this would change a major experimental substrate and would require a new qualification campaign. It is therefore **not the shortest scientifically defensible route** for this paper unless a very specific source-level defect/fix can be tied to the exact deployed commit and reproduced in a non-scored comparison.

## 6. RS-2 time-box rule

Do not turn WellPulse into an srsLTE core-repair project.

Strategy A may remain alive only for **one bounded offline source/config review round**. It passes only if that review identifies all three:

1. a specific defect or configuration mechanism that directly explains the observed H1 state divergence;
2. a deterministic pre-trial fix that requires no architecture/outcome inspection during a run;
3. a minimal non-scored test capable of falsifying the fix without reopening Q0–Q3.

If any of these are absent, Strategy A is closed for this paper and RS-3 must proceed using Strategy B semantics.

## 7. RS-2 verdict

### `PASS — MECHANISM CHARACTERIZED; NO PROVEN BOUNDED AUTONOMOUS REPAIR`

The LTE substrate failure has been localized sufficiently for the scientific decision gate:

- persistent RF failure is not supported;
- MQTT/WellPulse failure is not supported as the cause of service non-recovery;
- one-sided UE or EPC/eNB restart is insufficient;
- mutually stale/inconsistent LTE session context is the dominant diagnosis;
- clean-order full LTE reinitialization is the only demonstrated deterministic restoration primitive;
- no specific configuration-only or autonomous-recovery repair has been demonstrated.

**RS-2 recommendation:** do not spend another reservation searching broadly for LTE fixes. Carry one bounded offline source/config check only; absent a specific verified fix, move to **Strategy B — standardized service-restoration boundary** and make RS-3 separate substrate-recovery and application-recovery clocks prospectively.

## 8. Implication for RS-3

RS-3 must treat these as distinct observable events:

- `t_rf_restore`: physical RF attenuation returns to Q0;
- `t_service_ready`: end-to-end Q0 user plane and broker reachability are proven after the prospectively defined, architecture-neutral service-restoration procedure;
- `t_app_complete`: the primary application cohort reaches the frozen completion criterion.

The fairness constraint is mandatory: any restoration procedure must be scheduled/triggered solely from substrate/testbed state, must be identical across B1/W1/B2, and may not inspect architecture identity, queue depth, delivery success, or emerging outcomes.

## 9. Remaining uncertainty

Because the H1 raw node bundles are currently unavailable, RS-2 cannot reconstruct every NAS/GTP event from original timestamps. This limits forensic precision but does not overturn the mechanism-level conclusion above, which is based on preserved live diagnostics, recovery interventions and the 3/3 post-recovery application qualification.

If POWDER support recovers the raw archives, RS-2 should be rechecked against the complete logs; the verdict changes only if those logs materially contradict the preserved diagnosis.
