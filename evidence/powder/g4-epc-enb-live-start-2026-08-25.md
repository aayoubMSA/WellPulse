# POWDER G4 — EPC/eNB Live Startup Checkpoint — 2026-08-25

**Evidence class:** NON-SCORED INFRASTRUCTURE QUALIFICATION  
**Experiment:** `WellPulse/WP-G4-CTRL-RF`  
**Experiment UUID:** `56e4b80d-b13a-4b2f-b9e5-f32ac6732538`  
**Gate:** G4 controlled physical-RF lifecycle — IN PROGRESS  
**Scored scientific runs:** 0  
**`scored_runs_authorized`:** false

## Context

After an earlier manual-component attempt, the user intentionally reset only the process state while keeping the same POWDER experiment alive. On `nuc1`, old `srsepc`/`srsenb` processes were terminated and a read-only process check returned `CLEAN`. `nuc2` had no `srsue` process. The profile-authoritative startup script was then used on `nuc1`:

```bash
/local/repository/bin/start.sh
```

## Observed live output

The profile-created tmux session showed the EPC receiving the eNB S1 setup request and replying:

```text
Received S1 Setup Request.
S1 Setup Request - eNB Name: srsenb01, eNB id: 0x19b
S1 Setup Request - MCC:998, MNC:98, PLMN: 10090633
S1 Setup Request - TAC 0, B-PLMN 0
S1 Setup Request - Paging DRX v128
Sending S1 Setup Response
```

The eNB pane showed successful B210 initialization and RF clock setup:

```text
[INFO] [B200] Initialized CODEC control...
[INFO] [B200] Initialized Radio control...
[INFO] [B200] Performing register loopback test...
[INFO] [B200] Register loopback test passed
[INFO] [B200] Asking for clock rate 23.040000 MHz...
[INFO] [B200] Actually got clock rate 23.040000 MHz.
Setting frequency: DL=2132.5 MHz, UL=1732.5 MHz for cc_idx=0
==== eNodeB started ===
Type <t> to view trace
```

## Raw screenshot preservation

The user-supplied screenshot of the live tmux session was preserved in the canonical Drive raw-evidence workspace:

- Drive file: `POWDER_G4_EPC_eNB_S1_B210_PASS_2026-08-25.png`
- Drive file ID: `1IG9goNqSuCmXpB_zMJdrEsZ6CZrZS4R0`
- parent: `02_RAW_EVIDENCE` (`11xaitxG0vkV6fCzK_JgLAacrdhjz7GBf`)

## Verdict

This checkpoint supports the following claims:

- profile-authoritative `nuc1` startup path executed;
- EPC initialized and accepted the eNB S1 setup exchange;
- eNB obtained software-level access to the physical B210;
- B210 register loopback tests passed;
- requested/actual 23.04 MHz clock agreed;
- eNB configured DL/UL frequencies and reported `eNodeB started`.

Therefore the **EPC/eNB live-start sub-gate = PASS**.

## Evidence boundary

This does **not** yet prove:

- `srsue` startup on `nuc2`;
- UE attach/authentication;
- LTE bearer establishment;
- user-plane packet flow over the experimental LTE path;
- RF impairment control;
- MQTT/WellPulse behavior;
- any scored scientific observation.

## Exact next action

Keep `nuc1` tmux services running. On the already-connected `nuc2` session, execute the profile-authoritative UE startup script:

```bash
/local/repository/bin/start.sh
```

Then inspect the UE/eNB/EPC outputs for successful attach and assigned LTE connectivity before any ping/iperf test. Preserve only credential-free evidence.
