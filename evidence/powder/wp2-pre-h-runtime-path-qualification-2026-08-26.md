# WP2 Pre-H Runtime and Experimental-Path Qualification — 2026-08-26

## Classification

- Evidence class: **NON-SCORED PRE-SCORE VALIDATION / REPRODUCIBILITY**
- Scientific result contribution: **none**
- Purpose: qualify the physical POWDER execution chain before H calibration and later scored B1/W1/B2 runs.
- Scored runs authorized: **false**
- H calibration started in this artifact: **no**
- Secret/credential material preserved: **no**
- Raw experiment RPC token preserved: **no**

This artifact validates experimental setup, execution path, runtime identity, and session isolation. It must not be cited as evidence that WellPulse outperforms a comparator.

## Live experiment identity

- Experiment: `WP-HCAL-E`
- Project: `WellPulse`
- Profile: `PowderProfiles/srslte-controlled-rf`
- Profile revision: `a6da96560b6526dc6816761282722c996418fd8c`
- UE type: `srsue`
- Logical/physical mapping:
  - `enb1 -> nuc1`
  - `rue1 -> nuc2`
- Image: `PowderProfiles:U18LL-SRSLTE:1`
- Controlled RF link: profile-provided `P2PLTE`

The user-provided manifest also exposed an encrypted experiment RPC credential block. That block is intentionally excluded from this evidence file under the raw-log minimization rule.

## Gate 1 — EPC/eNB bring-up on nuc1

Observed UTC: `2026-08-26T17:29:49Z`

Sanitized terminal result:

```text
HOST=nuc1
USER=aayoub
1601 sudo nohup srsepc /etc/srslte/epc.conf
1603 srsepc /etc/srslte/epc.conf
1634 sudo nohup srsenb /etc/srslte/enb.conf
1636 srsenb /etc/srslte/enb.conf
WP2_NUC1_EPC_ENB=PASS
```

Result: **PASS**.

## Gate 2 — LTE attach and bearer establishment

Initial UE-side readiness script observed `srsue` running but timed out before `tun_srsue` appeared. This was investigated rather than classified as LTE failure.

UE startup evidence included:

```text
Built in Release mode using commit c892ae56b on branch master.
Detected Device: B210
Operating over USB 3.
Waiting PHY to initialize ... done!
Attaching UE...
```

EPC/eNB diagnostic then proved successful radio access, authentication, session creation, UE IP allocation, and attach completion:

```text
RACH: ... temp_crnti=0x46
User 0x46 connected
Received S1 Setup Request.
Initial UE message: LIBLTE_MME_MSG_TYPE_ATTACH_REQUEST
Attach request -- IMSI: 001010123456789
UE Authentication Accepted.
Sending Create Session Request.
SPGW: Allocate UE IP 172.16.0.2
Sent Initial Context Setup Request. E-RAB id 5
UL NAS: Received Attach Complete
Received GTP-C PDU. Message type: GTPC_MSG_TYPE_MODIFY_BEARER_REQUEST
```

Interpretation: the earlier `tun_srsue` timeout was a readiness/timing race in the first script, not a failed LTE attach.

Result: **PASS**.

## Gate 3 — Q0 end-to-end user-plane through experimental tunnel

The UE held `172.16.0.2`; the EPC/SGi endpoint was `172.16.0.1`.

Verified path:

```text
172.16.0.1 dev tun_srsue src 172.16.0.2
```

Explicit Q0 user-plane test through `tun_srsue`:

```text
PING 172.16.0.1 from 172.16.0.2 tun_srsue
10 packets transmitted, 10 received, 0% packet loss
rtt min/avg/max/mdev = 16.861/72.649/528.746/152.067 ms
WP2_Q0_USERPLANE=PASS
```

The first 528 ms response is treated as startup/transient behavior; delivery was 10/10 and subsequent RTTs settled to approximately 17–28 ms.

Result: **PASS**.

## Gate 4 — MQTT broker endpoint and TLS compatibility

### Initial legacy-broker observation

The base Ubuntu image provided:

- Mosquitto `1.4.15`
- OpenSSL `1.1.1`

The TLS endpoint was structurally correct:

- listener `172.16.0.1:8883`
- certificate `CN=172.16.0.1`
- SAN `IP Address:172.16.0.1`
- certificate/key modulus match
- connection arrived from UE IP `172.16.0.2`

However the legacy broker reset both OpenSSL and Python/Paho TLS handshakes. This was classified as a legacy runtime compatibility issue, not a radio-path failure.

### Isolated broker repair

A reversible isolated broker runtime was created under `/tmp` using conda-forge:

- Mosquitto `2.0.20`
- OpenSSL `3.6.4` in the isolated environment
- no system-image upgrade
- no RF-state change

TLS self-test result:

```text
LISTEN ... 172.16.0.1:8883
CONNECTION ESTABLISHED
Protocol version: TLSv1.2
Ciphersuite: ECDHE-RSA-AES256-GCM-SHA384
Peer certificate: CN = 172.16.0.1
Verification: OK
MOSQUITTO_VERSION=2.0.20
MODERN_MQTT_TLS=PASS
WP2_G_BROKER_COMPATIBILITY=PASS
```

Result: **PASS**.

## Gate 5 — Frozen remote Paho runtime and experimental MQTT path

The base node Python was `3.6.9`, which cannot host the frozen `paho-mqtt==2.1.0` requirement. A reversible isolated Python runtime was therefore created under `/tmp`, without modifying system Python.

Qualified runtime:

- Python `3.11.16`
- `paho-mqtt==2.1.0`
- protocol: MQTT v3.1.1
- QoS: 1
- TLS: enabled
- broker: `172.16.0.1:8883`
- route: `172.16.0.1 dev tun_srsue src 172.16.0.2`

The public CA certificate was fetched from `172.16.0.1` over the live LTE-routed endpoint before the MQTT test.

Final sanitized result:

```text
Q0_USERPLANE=PASS
PYTHON=Python 3.11.16
PAHO_VERSION=2.1.0
CA_FETCH_OVER_LTE=PASS
CLIENT_ID=wp2g-wp2g-20260826T175243Z-1939
TOPIC=wellpulse/wp2g/wp2g-20260826T175243Z-1939
SESSION_PRESENT=false
MQTT_TLS_CONNECT=PASS
MQTT_QOS1_PUBACK=PASS
PAYLOAD_SHA256=bed8a6601664c865c48ad8dd0342ddf0b6aa956b9ed7c1213a9774ce86cf811c
RUN_UNIQUE_ISOLATION=PASS
WP2_G_MQTT_RUNTIME_PATH_SESSION=PASS
```

Result: **PASS**.

The Paho callback API v1 deprecation warning is non-blocking; the frozen package version and required MQTT/session semantics were reproduced.

## Reproducibility value

This qualification establishes, before any H calibration or scored outcome exists, that:

1. the frozen POWDER profile revision and physical binding are known;
2. EPC/eNB and srsUE can establish a real LTE bearer;
3. the application endpoint is reachable through `tun_srsue`, not merely over the POWDER control network;
4. Q0 has explicit end-to-end user-plane health;
5. the frozen Python/Paho runtime is reproducible on the legacy POWDER image using an isolated runtime;
6. TLS MQTT QoS1 works end-to-end over the LTE path;
7. the first fresh MQTT connection reports `session_present=false`;
8. client ID and topic namespace are run-unique;
9. compatibility fixes are reversible and isolated from the testbed base image and RF configuration.

## Paper-validity role

This artifact supports **internal validity, methods reproducibility, and execution-path validation**. In a manuscript, it can support the Experimental Setup / Reproducibility / Threats-to-Validity narrative that later B1/W1 differences are not artifacts of an unverified control-network bypass, stale MQTT session, mismatched runtime, or failed LTE bearer.

It does **not** validate the paper's primary performance claim by itself. Scientific evidence begins only after the common recovery horizon H is frozen from the predeclared non-scored calibration and the scored matrix is explicitly authorized.

## Current frontier after this artifact

`WP-HCAL-E READY -> EPC/eNB PASS -> UE attach PASS -> Q0 user-plane PASS -> MQTT TLS/runtime/path/session isolation PASS`

Next gate: **WP2-H1 — non-scored W1 H-calibration trial #1**.
