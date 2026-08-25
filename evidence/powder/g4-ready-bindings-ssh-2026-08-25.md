# POWDER G4 — READY, RF Binding, and Explicit-SSH Checkpoint — 2026-08-25

**Evidence class:** NON-SCORED INFRASTRUCTURE QUALIFICATION  
**Gate:** G4 controlled physical-RF lifecycle — IN PROGRESS  
**Experiment:** `WellPulse/WP-G4-CTRL-RF`  
**Experiment UUID:** `56e4b80d-b13a-4b2f-b9e5-f32ac6732538`  
**Scored scientific runs:** 0  
**`scored_runs_authorized`:** false

## Purpose

Preserve the reproducible, credential-free checkpoint proving that the scheduled controlled-RF experiment reached READY, exposed the expected RF-controlled topology, accepted the canonical explicit SSH identity on both endpoint hosts, and progressed into profile-authoritative LTE component startup. This checkpoint does **not** yet prove UE attach/user-plane operation and does not close G4.

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

## EPC / eNB startup checkpoint on `nuc1`

The user manually executed the profile-authoritative components on `nuc1`.

EPC command:

```bash
sudo srsepc /etc/srslte/epc.conf
```

Observed sanitized startup output included:

```text
Built in Release mode using commit c892ae56b on branch master.
Reading configuration file /etc/srslte/epc.conf...
HSS Initialized.
MME S11 Initialized
MME GTP-C Initialized
MME Initialized. MCC: 0xf998, MNC: 0xff98
SPGW GTP-U Initialized.
SPGW S11 Initialized.
SP-GW Initialized.
```

Interpretation: **EPC initialization reached the reported initialized state**. This does not by itself prove the EPC process remained alive after the captured output.

The eNB command was then executed:

```bash
sudo srsenb /etc/srslte/enb.conf
```

Observed sanitized startup output included:

```text
Built in Release mode using commit c892ae56b on branch master.
Reading configuration file /etc/srslte/enb.conf...
Force DL EARFCN for cell PCI=1 to 2175
Opening 1 channels in RF device=default with args=default
[INFO] [UHD] ... UHD_3.15.0.0-2ubuntu1emulab1
Opening USRP channels=1, args: type=b200,master_clock_rate=23.04e6
[INFO] [B200] Detected Device: B210
[INFO] [B200] Loading FPGA image: /usr/share/uhd/images/usrp_b210_fpga.bin...
```

Interpretation: **eNB startup reached the real UHD/B210 initialization path and detected a B210 device**. This is stronger than manifest-only binding evidence because it demonstrates software-level access to the physical SDR. However, the captured output does not yet prove the eNB process remained alive, completed RF bring-up, accepted a UE, or carried user-plane traffic.

Current sub-gate verdict:

- EPC reported initialization: **PASS as startup checkpoint**;
- eNB B210 detection / FPGA-load path reached: **PASS as SDR-access checkpoint**;
- sustained EPC/eNB process liveness: **NOT YET VERIFIED**;
- UE attach: **NOT STARTED / NOT VERIFIED**;
- LTE bearer/user-plane connectivity: **NOT VERIFIED**.

## Security sanitization

The raw portal manifest/status dump supplied during the live session contained experiment RPC credential/certificate material. That material is intentionally **not retained** in this repository. Only non-secret experiment/profile/resource identifiers and reproducibility metadata are preserved here.

Do not commit private keys, passphrases, POWDER API tokens, experiment RPC tokens, PKCS7 blocks, or raw portal credential material.

## Evidence boundary

This checkpoint currently proves:

`scheduled experiment -> READY -> actual nuc1/nuc2 bindings -> rf-controlled P2PLTE link manifest -> explicit Golden-key SSH on both hosts -> EPC initialization output -> eNB reaches UHD/B210 detection and FPGA-load path`

It does **not** yet prove:

- sustained `srsepc`/`srsenb` liveness;
- `srsue` start or attach;
- LTE bearer/user-plane connectivity;
- RF impairment control;
- MQTT/WellPulse behavior;
- any scored scientific observation.

## Exact next action

Before starting the UE on `nuc2`, verify that the EPC and eNB processes are actually still alive on `nuc1` using a read-only process check. Do not begin scored runs.
