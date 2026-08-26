# Next Gate — POWDER WP2 Physical H Calibration

**Current frontier:** WP2 physical W1 H calibration  
**Scientific completion:** 20%  
**Scored authorization:** `false`

## Mandatory pre-read

Before any POWDER action, read:

1. `HANDOVER_CURRENT.md`
2. `docs/AGENT_HANDOVER_POWDER_NEXT.md`
3. `powder/PRE_EXPERIMENT_GATE_2026-08-26.md`
4. D-020 in `docs/DECISIONS.md`

## Current reservation

**2026-08-26 19:00–22:00 Africa/Cairo — `nuc1+nuc2`**.

## Entry gate

The next experiment must prove, in order:

`single instantiate -> READY -> live manifest PASS -> SSH both nodes PASS -> Q0 LTE user-plane PASS -> tun_srsue route PASS -> runtime/session-isolation PASS`

Only after all of those may physical W1 H calibration begin.

## Execution rule

- instantiate exactly one fresh `PowderProfiles/srslte-controlled-rf` experiment early in the reservation;
- verify the reservation still owns the requested resources before binding `nuc1/nuc2`;
- use the registered current automation public key through the secure Portal/API path;
- wait for READY;
- do **not** use terminate/recreate churn if provisioning stalls;
- verify fresh profile revision, manifest mapping and SSH endpoints;
- prove SSH on both nodes;
- establish EPC/eNB + UE;
- require explicit Q0 end-to-end user-plane PASS;
- require route to `172.16.0.1` via `tun_srsue`;
- verify Paho 2.1.0/runtime and first fresh MQTT `session_present=false`;
- then run only non-scored W1 H calibration.

## H rule

`30 s readiness -> Q0 60 s -> Q3 120 s -> Q0 until backlog drain`

Exactly three `VALID_W1_RECOVERY_SUCCESS` trials are required.

`H = max(120 s, ceil_to_30s(2 × p95))`

With n=3, p95 is the maximum successful drain time.

Stop if:

- a `VALID_W1_RECOVERY_FAILURE` occurs;
- H would exceed 300 s;
- Q0 user-plane fails;
- MQTT bypasses `tun_srsue`;
- runtime/session isolation differs from frozen design;
- experiment does not reach READY;
- fresh-node SSH fails after the current registered key is definitely injected.

## Frozen boundaries

- Q0 = 0 dB, Q1 = 40 dB, Q2 = 52 dB, Q3 = 55 dB.
- no RF sweep reopening.
- no scored B1/W1/B2 run.
- no WP3.
- no rerun because a scientific result is unfavorable.

The 14:00–16:00 window is operational troubleshooting history only and produced no H/scored scientific data.