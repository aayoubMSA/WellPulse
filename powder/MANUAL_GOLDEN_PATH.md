# POWDER Manual Golden Path Runbook

This runbook is the canonical reproducibility procedure for proving basic POWDER access before any radio or scientific workload is attempted.

## Scope

This gate proves only:

`manual instantiate -> READY -> explicit SSH key login -> basic metadata -> manual terminate -> zero active usage`

It is deliberately narrower than WP-PWD01 and must not be cited as RF or scientific evidence.

## Security boundary

- Canonical SSH key label: `WellPulse-POWDER-Golden`.
- Canonical public-key fingerprint: `SHA256:fLOBcEmuJ/ozS3Zyo1kRimvbnOm4Fb1yzP0f5X5TOgs`.
- The private key remains local and is protected by a user-held passphrase.
- Never commit the private key, passphrase, POWDER API token, experiment RPC token, raw certificate material, or full portal logs containing credential-like fields.
- Public-key fingerprints, experiment UUIDs, profile IDs, node IDs, non-secret manifests, and sanitized logs may be recorded.

## Prerequisites

1. POWDER project `WellPulse` is approved.
2. User account `aayoub` can instantiate experiments in the project.
3. `WellPulse-POWDER-Golden` is present under POWDER SSH keys before the experiment is instantiated.
4. Local private key exists at:

```text
%USERPROFILE%\.ssh\wellpulse_powder_golden
```

## Canonical profile

Use the POWDER profile:

```text
srsLTE-SIM:9
```

Profile UUID:

```text
80dda605-7e5f-11e9-8006-e4434b2381fc
```

Expected topology:

- one exclusive compute node;
- hardware type `d430`;
- image `PowderProfiles:gnuradio-srslte`;
- no SDR;
- no RF.

## Procedure

### 1. Confirm clean baseline

Before instantiation, verify the portal header shows:

```text
Current Usage: 0 Node Hours
```

Do not create a reservation if the required `d430` node is available.

### 2. Instantiate manually

Select `srsLTE-SIM:9` and use:

```text
Project: WellPulse
Name: WP-G1-SIM
Hardware: d430
Start: ASAP
Reservation: none
```

Use the portal-provided default expiration; the experiment will be terminated manually after the gate.

### 3. Wait for READY

Do not proceed while state is `provisioning`.

PASS condition:

```text
State: ready
```

Open **List View** and record the actual SSH hostname. Never guess or reuse a hostname from an earlier run.

### 4. SSH with the explicit Golden key

From Windows PowerShell, use the exact hostname shown by POWDER:

```powershell
ssh -o IdentitiesOnly=yes `
  -i "$HOME\.ssh\wellpulse_powder_golden" `
  aayoub@ACTUAL_HOSTNAME_FROM_LIST_VIEW
```

Enter the local key passphrase when prompted.

Do not use a bare `ssh aayoub@host` as the acceptance test because Windows may select a different default identity.

### 5. Execute only the metadata checks

After login:

```bash
hostname
whoami
uname -a
date -u
cat /etc/os-release
```

Do not run srsLTE, install packages, upgrade the OS, alter SSH configuration, or start any radio/scientific workload in this gate.

### 6. Exit and terminate

```bash
exit
```

Then terminate the experiment manually in the POWDER portal.

PASS condition after teardown:

```text
Current Usage: 0 Node Hours
```

## Acceptance criteria

The gate is PASS only if all are true:

- experiment reaches `ready`;
- List View exposes a real SSH endpoint;
- explicit `wellpulse_powder_golden` authentication succeeds;
- `whoami` returns `aayoub`;
- canonical remote hostname can be read;
- OS/kernel/UTC metadata can be read;
- experiment is destroyed cleanly;
- active usage returns to zero;
- no radio or scientific workload was executed.

## Verified reference run — 2026-08-24

The first accepted reference run is documented in:

`evidence/powder/manual-golden-path-2026-08-24.md`

Reference allocation:

```text
experiment UUID: 0dc233d7-44a0-4e6c-9734-6d4c8ea0e2ad
node:            pc734
SSH endpoint:    pc734.emulab.net:22
remote hostname: node.wp-g1-sim.wellpulse.emulab.net
```

These node identifiers are historical evidence only. Future reproductions must use the endpoint assigned by their own List View.

## Same-resource terminate/recreate guard

Do **not** assume that a successful terminate request means the just-released node can be immediately reused by a replacement experiment in the same reservation.

Observed on 2026-08-26: `WP-HCAL-A` was terminated and `WP-HCAL-B` was created immediately with the same reserved `nuc1+nuc2` bindings. The replacement entered a transient `pending/booting` state with a reservation-allocation warning while the project still held the reservation.

Operational rule:

1. terminate the old experiment;
2. verify the old experiment no longer resolves/owns the resources;
3. wait for allocator/resource state to converge;
4. only then instantiate the replacement;
5. if the new experiment enters `pending` with a reservation conflict, preserve the state and allow the allocator to recover rather than repeatedly terminating/recreating.

This is a defensive scheduling rule based on an observed allocator/release lag. It is not a claim that every immediate recreate will fail.

## Failure rule

If any step fails:

1. stop;
2. preserve the portal state/log evidence;
3. do not retry from assumptions;
4. diagnose the exact failed layer;
5. rerun only after the cause is resolved;
6. retain failed attempts as troubleshooting history, never as successful evidence.

Resource-creating automation remains frozen until the relevant manual path has first passed.
