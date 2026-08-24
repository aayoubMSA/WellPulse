# POWDER Manual Golden Path — Verified Evidence

**Date:** 2026-08-24  
**Project:** `WellPulse`  
**Purpose:** infrastructure/reproducibility gate only — **not scientific evidence** and **not a scored run**.

## Verdict

**PASS — manual provision -> SSH -> node identity verification -> clean teardown completed.**

This is the first POWDER run in this project accepted as the canonical manual infrastructure baseline.

## Canonical successful run

- Experiment name: `WP-G1-SIM`
- Experiment UUID: `0dc233d7-44a0-4e6c-9734-6d4c8ea0e2ad`
- Profile: `srsLTE-SIM:9`
- Profile UUID: `80dda605-7e5f-11e9-8006-e4434b2381fc`
- Project: `WellPulse`
- Aggregate/cluster: Emulab / POWDER
- Requested hardware: `d430`
- Allocated node: `pc734`
- Disk image: `PowderProfiles:gnuradio-srslte`
- SSH endpoint: `pc734.emulab.net:22`
- SSH username: `aayoub`
- Canonical hostname observed after login: `node.wp-g1-sim.wellpulse.emulab.net`
- SSH authentication mode in manifest: `ssh-keys`
- Start shown in portal history: 2026-08-24 22:07 local portal time
- Destroyed shown in portal history: 2026-08-24 22:17 local portal time
- Portal history PHours for this run: `0.16`
- Teardown check: `Current Usage: 0 Node Hours`

## SSH key used

Canonical manual key label:

`WellPulse-POWDER-Golden`

Public-key fingerprint:

`SHA256:fLOBcEmuJ/ozS3Zyo1kRimvbnOm4Fb1yzP0f5X5TOgs`

The private key and its passphrase are **not** stored in this repository.

## Remote verification output

The following commands were executed after successful SSH authentication:

```text
hostname
whoami
uname -a
date -u
cat /etc/os-release
```

Observed values:

```text
hostname: node.wp-g1-sim.wellpulse.emulab.net
whoami:   aayoub
kernel:   Linux 4.15.0-33-generic x86_64
UTC:      Mon Aug 24 19:15:48 UTC 2026
OS:       Ubuntu 18.04.1 LTS (Bionic Beaver)
```

## Portal-log evidence retained in sanitized form

The portal log established:

- operation `create_instance`;
- profile `srsLTE-SIM:9`;
- one exclusive `d430` node;
- image `PowderProfiles:gnuradio-srslte`;
- node allocation `pc734`;
- final node state `ready`, raw state `ISUP`, node status `up`;
- SSH service `pc734.emulab.net:22`, username `aayoub`, authentication `ssh-keys`;
- successful manifest resolution and provisioning (`WaitForSlivers ... code:0`).

The raw portal log is intentionally **not committed** because it contains certificate/token-like encrypted material and account metadata that are unnecessary for reproducibility.

## Evidence boundary

The profile description explicitly states that it runs srsLTE eNodeB/UE interaction **without SDR hardware**, using file-based simulated interaction.

Therefore this PASS establishes only:

1. WellPulse project resource allocation works on POWDER;
2. a `d430` compute node can be provisioned manually;
3. the registered SSH key can be injected and used from the local Windows workstation;
4. remote node identity/OS/time metadata can be collected;
5. the experiment can be destroyed cleanly with zero active node usage.

It does **not** establish:

- LTE/5G user-plane correctness;
- SDR or RF operation;
- conducted attenuation control;
- OTA behavior;
- WellPulse telemetry behavior;
- MQTT resilience;
- any scientific endpoint in WP-PWD01.

## Prior attempts — excluded from the canonical baseline

Portal history on 2026-08-24 contained five experiments in total. The relevant earlier attempts are retained as troubleshooting history, not evidence of scientific validation:

- `wpplmb6787317` / `srs-rf-matrix` — failed; hidden/unavailable `n310` dependency; no scored work.
- `wphnd8201533` / `srsran-handover` — exploratory/invalid feasibility attempt; excluded from scientific evidence.
- `WP-G1-SIM` started 21:06 — provisioned but SSH failed because the intended local public key was not the registered key; destroyed 21:42.
- `WP-G1-SIM` started 21:45 — troubleshooting rerun before the canonical Golden key reset; destroyed 22:04.
- `WP-G1-SIM` started 22:07 — **canonical PASS** recorded above; destroyed 22:17.

No prior attempt is to be silently promoted into the scored corpus.

## Gate state after this record

- G0 account/project baseline: **PASS**
- G1 simple compute provisioning: **PASS**
- G2 manual SSH + node verification: **PASS**
- clean teardown: **PASS**
- G3 simulated radio/data-path validation: **NOT STARTED**
- controlled physical-RF gate: **NOT STARTED**
- scored POWDER campaign: **NOT AUTHORIZED**
