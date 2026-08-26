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

For the current interactive/manual reservation, the access path is now:

`single instantiate -> READY -> live manifest/bindings PASS -> POWDER browser shell on both nodes PASS -> Q0 LTE user-plane PASS -> tun_srsue route PASS -> runtime/session-isolation PASS`

Direct SSH from the Home PC or GitHub Actions is **not a blocking gate for this reservation**. POWDER's browser-based shell is the preferred access mechanism because it is portal-authenticated and does not depend on a local SSH keypair. The GitHub SSH ownership gate remains a future automation-qualification task only; do not spend reservation time repairing it unless remote automation becomes materially necessary.

Only after the access/path gates above may physical W1 H calibration begin.

## Execution rule

- instantiate exactly one fresh `PowderProfiles/srslte-controlled-rf` experiment early in the reservation;
- verify the reservation still owns the requested resources before binding `nuc1/nuc2`;
- wait for READY;
- do **not** use terminate/recreate churn if provisioning stalls;
- verify fresh profile revision and physical mapping (`enb1 -> nuc1`, `rue1 -> nuc2`);
- use the POWDER **Web-based Shell** from the node action menu as the default interactive access path;
- prove browser-shell access on both `nuc1` and `nuc2` before LTE actions;
- do not block current science on Home-PC/GitHub SSH-key troubleshooting;
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
- browser-shell access to either allocated node fails.

## Frozen boundaries

- Q0 = 0 dB, Q1 = 40 dB, Q2 = 52 dB, Q3 = 55 dB.
- no RF sweep reopening.
- no scored B1/W1/B2 run.
- no WP3.
- no rerun because a scientific result is unfavorable.

The 14:00–16:00 window is operational troubleshooting history only and produced no H/scored scientific data.

## Operational simplification freeze — 2026-08-26

For this reservation and future interactive POWDER recovery work, prefer the shortest portal-native path:

`Portal READY -> List View/Actions -> Shell`

Do not route ordinary interactive access through Home-PC SSH keys or GitHub Actions merely because those automation paths exist. Use GitHub SSH only when unattended remote automation itself is the object being qualified.