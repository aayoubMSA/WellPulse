# WP2-P8 E2 — Live Handover

Date: 2026-08-28
Repository: `aayoubMSA/WellPulse`
Branch: `main`
Platform: POWDER / srsLTE controlled RF
Campaign: `WP2-P8 — Modular Manual RF Experiment Campaign`
Current experiment: `P8-E2 — RF Hysteresis / Spontaneous Recovery`

## 1. Scientific boundary

This campaign is manual, exploratory, non-scored reference work. It does not alter the frozen historical scored P7B state.

`SCORED_P7B_STATUS=UNCHANGED_NOT_PASSED`
`P8_CAMPAIGN_CLASS=NON_SCORED_MANUAL_REFERENCE`

## 2. Live topology

- `nuc1 / CORE`: EPC, eNB, Mosquitto broker, MQTT receiver, reverse-path monitor.
- `nuc2 / UE`: srsUE, RF attenuation control, UE->CORE ping, MQTT publisher.
- Attenuators: `[1,33,2,34]`.
- Known healthy UE tunnel address during clean baseline: `172.16.0.2/24`.
- CORE LTE endpoint: `172.16.0.1`.

## 3. Three-screen operating layout

- `nuc1-A` top-left: visible MQTT receiver only.
- `nuc1-B` top-right: CORE->UE ping monitor and CORE-side evidence commands.
- `nuc2` bottom-right: RF treatment, UE->CORE ping, MQTT publisher, UE evidence.

All instructions must identify one of these roles explicitly. Do not collapse the experiment into a one-node B1-style script.

## 4. Completed campaign evidence

### P8-E0 — Stable baseline qualification

Clean two-node baseline was established before the valid threshold work:

- CORE->UE ping: 10/10, 0% loss.
- UE->CORE ping: 10/10, 0% loss.
- UE tunnel stable at `172.16.0.2/24`.
- `srsepc`, `srsenb`, `srsue` stable.
- 10/10 MQTT messages visibly delivered from nuc2 to nuc1-A.

`P8_E0_BASELINE_QUALIFIED=PASS`

### P8-E1 initial attempt

Initial E1 raw evidence was preserved but analysis showed the nominal baseline was already unhealthy before treatment. It is diagnostic only and is not valid for RF-threshold inference.

`P8_E1=NULL_ABORTED_INVALID_PRETREATMENT_BASELINE`
`EVIDENCE_INTEGRITY=PASS`
`DIAGNOSTIC_VALUE=HIGH`

### P8-E1R2 — 0 to 30 dB

Clean run with bidirectional connectivity and MQTT completeness through 30 dB.

- MQTT generated/received: 65/65.
- missing: 0.
- duplicates: 0.
- packet loss: 0% at every tested point through 30 dB.

Off-platform archive hashes:

- CORE: `A8DBA3B486FA9E86CCD80E8704DA2AE277BACC6998C5B4292B53C52BBBD62B4A`
- UE: `7A1C2F2F32DF22E6C0B2E0F3A4480C8A7D7B64C290129AE84FC5E47F181E348B`

`P8_E1R2_OFFPLATFORM_PRESERVATION=PASS`

### P8-E1R3 — 30 to 50 dB

Clean extension located the first degraded region.

- 48 dB: known-good.
- 50 dB: first confirmed packet-loss degradation.
- 50 dB confirmation: 20 transmitted / 19 received / 5% loss; RTT min/avg/max approximately 28.142/43.581/90.091 ms.

Off-platform archive hashes:

- CORE: `00699132F302018585972A81503E464272B2BACE3E85DDA9A94D224C844B13E5`
- UE: `0C32700B3A4751EFFA7B7109614E64A9425AB874068E372AC365B5CE3AB4E837`

`P8_E1R3_OFFPLATFORM_PRESERVATION=PASS`

### P8-E1R4 — 48 to 52 dB micro-sweep

Raw archives were preserved off-platform and analyzed. Derived profile:

| Attenuation | UE->CORE ping loss | CORE->UE ping loss | MQTT received | Mean app delay |
|---:|---:|---:|---:|---:|
| 48 dB | 0% | 0% | 20/20 | ~98 ms |
| 49 dB | 0% | 0% | 20/20 | ~92 ms |
| 50 dB | 0% | ~3.3% | 20/20 | ~170 ms |
| 51 dB | ~30% | ~30% | 20/20 | ~448 ms |
| 52 dB | ~60% | ~64% | 13/20 | ~8.0 s |

Independent 52 dB confirmation: 30 transmitted / 6 received / 80% loss.

Missing MQTT sequences at 52 dB: `82,84,90,91,92,96,97`.

After restoring RF to 0 dB without service restart:

- 20/20 ping, 0% loss.
- mean RTT approximately 22.6 ms.
- 10/10 recovery MQTT messages received.

Interpretation frozen for exploratory use:

- `<=49 dB`: healthy region.
- `50-51 dB`: degrading but application-resilient region.
- `>=52 dB`: severe intermittent region with application loss.

Off-platform archive hashes:

- CORE: `70F3CF784517ABB32D98F33118634FD48B736DB5EC5F46C54556E57A2237DD25`
- UE: `4CE3CEBEF0292E8276B46B1249A95E4766CE6E0E060843346E772D811AB8838F`

`P8_E1R4_OFFPLATFORM_PRESERVATION=PASS`
`P8_E1R4=FROZEN`

## 5. Current live experiment: P8-E2

Scientific question: does recovery occur at the same RF condition at which degradation appears, or is there hysteresis/state dependence; can the stack recover autonomously without service restart?

Shared run ID:

`p8-e2-20260828A`

Treatment sequence:

`0 -> 52 -> 51 -> 50 -> 49 -> 48 -> 46 -> 0 dB`

No service restarts are allowed during E2:

- no `srsue` restart;
- no `srsepc` restart;
- no `srsenb` restart;
- no Mosquitto restart.

Live node roles:

- `nuc1-A`: `mosquitto_sub` on topic `wellpulse/p8/e2`, timestamping and writing `received.log`.
- `nuc1-B`: repeated CORE->UE ping monitor writing `core_monitor.log`.
- `nuc2`: attenuation sequence, 20 UE->CORE ping probes per level, 20 sequenced MQTT sends per level, `events.log`, `sent.log`, per-level ping logs.

At handover creation time, E2 is running. Do not infer results until the loop is complete and raw evidence is frozen.

`P8_E2_STATE=LIVE_RUNNING`
`NEXT_ACTION=WAIT_FOR_E2_COMPLETE_THEN_FREEZE_BOTH_NODES`

## 6. Mandatory post-E2 closure

When nuc2 prints `=== P8-E2 COMPLETE ===`:

1. do not change treatment before taking a final visible three-screen snapshot;
2. stop nuc1-A receiver with one Ctrl+C;
3. stop nuc1-B monitor with one Ctrl+C;
4. capture final process/network state on both nodes;
5. create `SHA256_CORE.txt` and `SHA256_UE.txt` independently;
6. create separate CORE and UE `.tgz` archives;
7. print node-side archive SHA256 values;
8. pull both archives to the home PC using the explicit POWDER key;
9. independently compute PC SHA256 values and require exact match;
10. only then classify `P8_E2_OFFPLATFORM_PRESERVATION=PASS`;
11. upload both archives for reconciliation and analysis before E3.

## 7. Evidence storage doctrine

Raw experiment archives should NOT be committed directly to normal Git history as the primary store.

Recommended split:

### Google Drive = durable raw evidence store

Store immutable per-run CORE/UE archives, hashes, manifests, and later publication-ready raw-evidence packages under the WellPulse validation/evidence workspace. Drive is preferred for binary raw archives because it avoids repository bloat and preserves the original bundles separately from code.

### GitHub = canonical scientific control plane

Commit only:

- experiment contracts/plans;
- run manifests and SHA256 values;
- analysis scripts;
- derived CSV/JSON tables small enough for review;
- reconciliation outputs;
- concise results/closure documents;
- Drive artifact pointer/ID and digest;
- handovers.

Do not duplicate large raw archives into Git unless there is a deliberate Git LFS release policy.

### Home PC = temporary independent third copy

Keep the verified local copy until Drive upload/read-back verification is complete. Do not treat PC-only storage as canonical.

Recommended preservation chain:

`POWDER node-local raw -> independent per-node hash -> home-PC pull -> PC hash match -> Drive immutable upload -> Drive read-back/hash verification -> GitHub manifest/pointer/results`

Do not release a reservation while unique raw evidence exists only on POWDER.

## 8. Current next experiment order

After E2 analysis, remain inside the existing P8 WP. Do not drift.

Planned remaining experiments:

1. `P8-E3` near-threshold repeatability;
2. `P8-E4` RF-only recovery;
3. `P8-E5` UE-restart recovery;
4. `P8-E6` CORE-restart recovery;
5. `P8-E8` broker-only fault control;
6. `P8-E9` duration-matched no-fault control;
7. `P8-E7` combined recovery stress case, only if time/value remains.

E2 may provide some evidence relevant to E4, but do not silently collapse experiment identities; decide after E2 reconciliation whether E4 remains necessary or can be narrowed.

## 9. Stop state

`WP2_P8_STATUS=ACTIVE`
`CURRENT_EXPERIMENT=P8-E2`
`CURRENT_RUN_ID=p8-e2-20260828A`
`SCORED_P7B_STATUS=UNCHANGED`
`RAW_STORAGE_POLICY=DRIVE_PRIMARY_GITHUB_MANIFEST`
`LIVE_TEARDOWN=NOT_YET`
