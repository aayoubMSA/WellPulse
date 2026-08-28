# WellPulse — Current Handover

Last updated: 2026-08-28 during **WP2-P8 P8-E2 RF Hysteresis / Spontaneous Recovery** live manual-reference campaign.

## Canonical authority

Repository: `aayoubMSA/WellPulse`  
Branch: `main`

This file is the current operational retrieval point. Do not reconstruct current state from chat memory.

## Executive scientific state

- WP0: **PASS**
- WP1: **PASS / FROZEN**
- WP2: **ACTIVE**
- WP2-P8 manual RF campaign: **ACTIVE / NON-SCORED MANUAL REFERENCE**
- WP3: **BLOCKED ON WP2**
- WP4: **BLOCKED**
- WP5: **PREPARED / NOT EXECUTED**
- P6 Golden baseline: **VALID / FROZEN**
- P7B scored physical qualification: **NOT PASSED**
- scored execution: **NOT AUTHORIZED**

Historical P7B state remains unchanged:

`B1=NULL_ABORTED_AFTER_Q3`

`HISTORICAL_B1=CONSUMED`

`SCORED_P7B_STATUS=UNCHANGED_NOT_PASSED`

No P8 exploratory/manual result may be promoted into scored P7B.

## Current live lane

Current campaign:

`WP2-P8 — Modular Manual RF Experiment Campaign`

Current experiment:

`P8-E2 — RF Hysteresis / Spontaneous Recovery`

Current run:

`CURRENT_RUN_ID=p8-e2-20260828A`

Live topology:

- `nuc1-A / CORE`: visible MQTT receiver.
- `nuc1-B / CORE`: reverse CORE->UE ping monitor and CORE evidence.
- `nuc2 / UE`: RF treatment, UE->CORE ping, MQTT publisher and UE evidence.

Treatment sequence:

`0 -> 52 -> 51 -> 50 -> 49 -> 48 -> 46 -> 0 dB`

No `srsue`, `srsepc`, `srsenb` or Mosquitto restart is allowed during E2.

`P8_E2_STATE=LIVE_RUNNING`

## Completed P8 evidence

### P8-E0

Stable two-node baseline qualification passed:

- bidirectional ping healthy;
- UE tunnel stable at `172.16.0.2/24`;
- LTE services stable;
- 10/10 MQTT messages visibly delivered nuc2 -> nuc1-A.

`P8_E0_BASELINE_QUALIFIED=PASS`

### P8-E1 initial attempt

Evidence preserved but baseline was invalid before treatment.

`P8_E1=NULL_ABORTED_INVALID_PRETREATMENT_BASELINE`

### P8-E1R2

Clean 0-30 dB run; 65/65 MQTT records received, no missing/duplicates, 0% ping loss at all tested points.

Off-platform hashes:

- CORE `A8DBA3B486FA9E86CCD80E8704DA2AE277BACC6998C5B4292B53C52BBBD62B4A`
- UE `7A1C2F2F32DF22E6C0B2E0F3A4480C8A7D7B64C290129AE84FC5E47F181E348B`

### P8-E1R3

Clean 30-50 dB extension. 48 dB remained known-good; 50 dB showed first confirmed degradation. Independent 50 dB confirmation: 20 transmitted / 19 received / 5% loss.

Off-platform hashes:

- CORE `00699132F302018585972A81503E464272B2BACE3E85DDA9A94D224C844B13E5`
- UE `0C32700B3A4751EFFA7B7109614E64A9425AB874068E372AC365B5CE3AB4E837`

### P8-E1R4

48-52 dB micro-sweep result:

| Attenuation | UE->CORE ping loss | CORE->UE ping loss | MQTT received | Mean app delay |
|---:|---:|---:|---:|---:|
| 48 dB | 0% | 0% | 20/20 | ~98 ms |
| 49 dB | 0% | 0% | 20/20 | ~92 ms |
| 50 dB | 0% | ~3.3% | 20/20 | ~170 ms |
| 51 dB | ~30% | ~30% | 20/20 | ~448 ms |
| 52 dB | ~60% | ~64% | 13/20 | ~8.0 s |

Independent 52 dB confirmation: 30 transmitted / 6 received / 80% loss.

After RF restore to 0 dB with no service restart: 20/20 ping, 0% loss and 10/10 recovery MQTT messages.

Exploratory interpretation:

- `<=49 dB`: healthy;
- `50-51 dB`: degrading but application-resilient;
- `>=52 dB`: severe intermittent region with application loss.

Off-platform hashes:

- CORE `70F3CF784517ABB32D98F33118634FD48B736DB5EC5F46C54556E57A2237DD25`
- UE `4CE3CEBEF0292E8276B46B1249A95E4766CE6E0E060843346E772D811AB8838F`

## Evidence storage policy

Use a three-layer evidence model:

1. **Google Drive = primary durable raw-evidence store** for immutable CORE/UE archives, hashes, manifests and publication evidence bundles.
2. **GitHub = canonical control/scientific record** for experiment contracts, run manifests, SHA256 values, analysis scripts, derived small tables, reconciliation outputs, result/closure docs, Drive pointer/ID and handovers.
3. **Home PC = independent temporary third copy** until Drive upload/read-back verification is complete.

Do not commit large `.tgz` raw archives directly into ordinary Git history unless a deliberate Git LFS/release policy is later adopted.

Required preservation chain:

`POWDER node-local raw -> node SHA256 -> home-PC pull -> PC SHA256 match -> Drive upload -> Drive read-back/hash verification -> GitHub manifest/pointer/results`

## Mandatory current read order

1. `HANDOVER_CURRENT.md`
2. `docs/WP2_P8_E2_LIVE_HANDOVER_2026-08-28.md`
3. `experiments/WP-PWD01/WP2_P8_MANUAL_RF_EXPERIMENT_CAMPAIGN_2026-08-28.md`
4. current `Research & Grants — Lessons Learned Ledger`
5. historical P7B handover/closures only if working on scored P7B rather than P8.

## Immediate next action

Wait for nuc2 to print:

`=== P8-E2 COMPLETE ===`

Then:

1. capture the three-screen final state;
2. stop nuc1-A receiver and nuc1-B monitor;
3. freeze independent CORE and UE raw evidence;
4. hash and archive each node separately;
5. pull both archives to home PC and verify hashes;
6. upload to Drive and verify read-back before reservation release;
7. reconcile/ analyze E2 before beginning E3.

## Stop state

`WP2_P8_STATUS=ACTIVE`

`CURRENT_EXPERIMENT=P8-E2`

`CURRENT_RUN_ID=p8-e2-20260828A`

`RAW_STORAGE_POLICY=DRIVE_PRIMARY_GITHUB_MANIFEST`

`LIVE_TEARDOWN=NOT_YET`
