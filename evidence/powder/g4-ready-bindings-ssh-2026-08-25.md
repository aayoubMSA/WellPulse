# POWDER G4 — READY, RF Binding, and Explicit-SSH Checkpoint — 2026-08-25

**Evidence class:** NON-SCORED INFRASTRUCTURE QUALIFICATION  
**Gate:** G4 controlled physical-RF lifecycle — IN PROGRESS  
**Experiment:** `WellPulse/WP-G4-CTRL-RF`  
**Experiment UUID:** `56e4b80d-b13a-4b2f-b9e5-f32ac6732538`  
**Scored scientific runs:** 0  
**`scored_runs_authorized`:** false

## Purpose

Preserve the reproducible, credential-free checkpoint proving that the scheduled controlled-RF experiment reached READY, exposed the expected RF-controlled topology, and accepted the canonical explicit SSH identity on both endpoint hosts. This checkpoint does **not** prove LTE attach/user-plane operation and does not close G4.

## Live state observed

Portal/status evidence showed all three requested resources ready:

- `enb1` -> physical resource `nuc1` -> `status=ready`, `nodestatus=up`, startup execute status `0`;
- `rue1` -> physical resource `nuc2` -> `status=ready`, `nodestatus=up`, startup execute status `0`;
- `rflink` -> `status=ready`.

Profile/repository identity observed in the manifest:

- profile repository: `powder-profiles/srslte-controlled-rf`;
- commit: `a6da96560b6526dc6816761282722c996418fd8c`;
- image on both endpoints: `PowderProfiles:U18LL-SRSLTE:1`;
- hardware type on both endpoints: `nuc5300`;
- UE profile parameter: `srsue`.

## RF-controlled binding observed

- `enb1:rue1_rf` -> `nuc1:rf1`, IP `10.10.1.1/24`;
- `rue1:enb1_rf` -> `nuc2:rf1`, IP `10.10.1.2/24`;
- link client id: `rflink`;
- link protocol: `P2PLTE`;
- both endpoint nodes advertise Emulab feature `rf-controlled`.

This is sufficient to accept the **resource/binding sub-gate**. It is not yet evidence that the experimental LTE user plane has operated successfully through the controlled-RF path.

## SSH endpoint validation

Portal manifest exposed:

- `enb1` SSH endpoint: `aayoub@nuc1.emulab.net:22`;
- `rue1` SSH endpoint: `aayoub@nuc2.emulab.net:22`.

The user connected from Windows PowerShell with the canonical local key `wellpulse_powder_golden` and `IdentitiesOnly=yes`.

Observed on `nuc1`:

```text
aayoub@nuc1:~$ hostname
nuc1
aayoub@nuc1:~$ whoami
aayoub
```

Observed on `nuc2`:

```text
aayoub@nuc2:~$ hostname
nuc2
aayoub@nuc2:~$ whoami
aayoub
```

Verdict: **explicit-key SSH access PASS on both controlled-RF endpoint hosts**.

## Portal graph evidence preservation

The portal Graphs view was saved as the original PDF in the canonical Drive raw-evidence workspace:

- Drive file: `POWDER_G4_CTRL_RF_Portal_Graphs_2026-08-25.pdf`
- Drive file ID: `1iTygKh_RHV3JFlDty0UsZHtFIJGyPkGo`
- parent: `02_RAW_EVIDENCE` (`11xaitxG0vkV6fCzK_JgLAacrdhjz7GBf`)

The PDF preserves the experiment header/status plus the portal-generated Load Average and Control Traffic plots. The Control Traffic plot visually shows roughly 60-70 packets/s through much of the displayed interval before declining near the end.

Evidence boundary: these portal graphs are preserved as **infrastructure/provenance evidence only**. They are not currently attributable to the experimental LTE user plane or controlled-RF impairment path. The underlying time-series samples are not present in the currently retained evidence, so an exact scientific reproduction of the portal graph is not claimed. Digitizing the image would only produce an approximation and must not replace the original PDF.

## Security sanitization

The raw portal manifest/status dump supplied during the live session contained experiment RPC credential/certificate material. That material is intentionally **not retained** in this repository. Only non-secret experiment/profile/resource identifiers and reproducibility metadata are preserved here.

Do not commit private keys, passphrases, POWDER API tokens, experiment RPC tokens, PKCS7 blocks, or raw portal credential material.

## Evidence boundary

This checkpoint proves only:

`scheduled experiment -> READY -> actual nuc1/nuc2 bindings -> rf-controlled P2PLTE link manifest -> explicit Golden-key SSH on both hosts`

It does **not** prove:

- `srsepc`/`srsenb` start success;
- `srsue` start or attach;
- LTE bearer/user-plane connectivity;
- RF impairment control;
- MQTT/WellPulse behavior;
- any scored scientific observation.

## Exact next action

Continue the same manual G4 qualification. On `nuc1` start the profile-authoritative EPC/eNB path using:

```bash
/local/repository/bin/start.sh
```

Verify EPC/eNB startup before starting the srsLTE UE on `nuc2`. Preserve only sanitized output. Do not begin scored runs.
