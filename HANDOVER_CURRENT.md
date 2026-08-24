# WellPulse — Current Handover

Last updated: 2026-08-25 01:42 Africa/Cairo

## Standing handover rule

No material project state may exist only in chat. Decisions, results, artifacts, blockers, evidence boundaries, milestone percentages, time estimates, and the exact next action must be recoverable from GitHub and/or Drive.

## Executive state

Completed evidence/infrastructure:

- FIT IoT-LAB embedded-hardware scientific evidence layer: **FINAL PASS**.
- POWDER G0 account/project: **PASS**.
- POWDER G1 compute provisioning: **PASS**.
- POWDER G2 explicit-key SSH + teardown: **PASS**.
- POWDER G3 file-based simulated LTE stack/data path: **PASS**.
- POWDER G4 live profile discovery: **PASS**.
- POWDER G4 required NUC5300/B210 reservation: **APPROVED**.
- POWDER G4 experiment `WP-G4-CTRL-RF`: **SCHEDULED for 2026-08-25 19:00–22:00 Africa/Cairo**.

Scientific weighted completion remains **20%**.

- WP0 Novelty & Venue Lock: **8/8 complete**, with a 2026-08-25 manuscript-grade related-work benchmark and comparator audit now attached to the lock.
- WP1 Confirmatory Protocol & Statistics Freeze: **12/12 design work complete**, but the scientific comparator interpretation is **OPEN FOR PRE-SCORE REVIEW** after the deeper survey found durable standard MQTT-client persistence that must be defended.
- WP2 RF Calibration & Measurement Validation: **0/15 — next scientific WP after G4 lifecycle/user-plane**.
- WP3 Conducted-RF Confirmatory Campaign: **0/30 — blocked by WP2 and explicit scored authorization**.
- WP4 OTA External Replication: **0/15 — blocked by WP3**.
- WP5 Analysis + Artifact + Paper Closure: **0/20 scientific closure**.

`scored_runs_authorized = false`.

No POWDER run belongs to the scored scientific corpus.

Resource-creating POWDER automation remains **FROZEN by owner mandate** until the current profile/lifecycle is manually qualified. After G4 PASS, the proven lifecycle may be automated; any new RF-control layer must itself be qualified manually once before repetitive automation.

## Canonical repositories and workspaces

- GitHub: `aayoubMSA/WellPulse`.
- Drive project root `P12_WellPulse`: `1eBQJ8STP-x-MaW0-2m07G7kCoF4UnLft`.
- Drive validation workspace `00_Validation_Workspace`: `1SydHCA2jlkatxdGgUtJ1P8atgyi8_ta3`.
- Drive raw evidence `02_RAW_EVIDENCE`: `11xaitxG0vkV6fCzK_JgLAacrdhjz7GBf`.
- Drive handover folder `WellPulse Handover`: `1Du4j_YkMLvQjWJCxV5zqxxK6OGG2Q0hA`.
- Drive current handover index: `1Gd4FzyJ_dW6-AK6wQc4FW7LAWVb2GNzG0t-xHaSEwn4`.

## Scientific design and evidence boundary

Canonical protocol: `experiments/WP-PWD01/protocol.md`, v0.4.

Working primary matched comparison:

- `B1_MQTT_QOS1`: Paho Python MQTT v3.1.1, QoS1, TLS scored path, automatic reconnect, `clean_session=False`, volatile client state, no application-level disk durability/reconciliation.
- `W1_OFFLINE_FIRST`: the same frozen low-level Paho Python session plus SQLite durable application queue, stable record identity/checksum, replay, idempotent receiver and reconciliation.

Frozen low-level parameters:

- `paho-mqtt==2.1.0`;
- keepalive 60 s;
- reconnect 1–8 s;
- outgoing queue 4096;
- inflight 20.

Scenarios:

- S0 healthy;
- S1 intermittent;
- S2 hard outage;
- S3 hard outage + one gateway-process restart.

Run is the statistical unit. The conducted primary campaign remains planned as 24–36 scored B1/W1 runs under the precision rule. OTA remains a compact 12-run S1/S2 replication if the conducted gate passes. These counts apply to the working v0.4 B1/W1 design; any additional durable-client sensitivity matrix must be separately frozen before scoring and must not be silently pooled into the primary paired inference.

Evidence supported by the current remote-testbed programme is limited to communications/radio-link resilience, telemetry integrity/completeness, recovery, reconnect, gateway-process restart and overhead. It does **not** validate pump mechanics, hydraulics, groundwater, crop/agronomic outcomes, Siwa field performance, or generic rural-field generalization.

## FIT IoT-LAB — accepted scientific evidence

Canonical result: `experiments/WP-RT01/FINAL_RESULTS_2026-08-23.md`.

Evidence class: `FINAL_WP_RT01_FIT_A8`.

- Grenoble A8 hardware.
- B0/W1 × C0/C1/C2 × 3 replicates = 18 final cells.
- exactly 10,000 records per cell.
- 18/18 final reconciliation PASS.
- W1 achieved 100% final completeness, zero permanent missing records and zero final duplicates under both controlled broker outage and broker-outage + gateway-process restart in 3/3 replicates.
- B0 retained 80% under C1/C2.

FIT is real embedded-hardware evidence under controlled connectivity impairment. It is not physical-RF causal evidence and its B0 comparator is a historical lower-bound rather than the primary POWDER inferential baseline.

## POWDER G3 — accepted infrastructure evidence

Canonical evidence: `evidence/powder/g3-simstack-2026-08-24.md`.

Accepted run:

- experiment `WP-G3-SIMSTACK`;
- UUID `3484b01d-7eca-48e7-9e34-866680057b0d`;
- profile `srsLTE-SIM:9`;
- one d430, allocated node `pc757`;
- Golden-key explicit SSH PASS;
- `pdsch_enodeb -> IQ file -> pdsch_ue` PASS;
- multiple `TB decoded OK`;
- `RX_RC=0`;
- waveform 2,304,000 bytes;
- SHA-256 `103de59d52e75252e916d7ed62c5c9b76401e817ffec3178363879e0bed71678`;
- cleanup PASS;
- teardown PASS with `Current Usage: 0 Node Hours`.

G3 is file-based LTE simulation only: no SDR, no physical RF, no attenuation, no OTA and no scientific WellPulse result.

## POWDER G4 — current scheduled state

Canonical discovery/reservation evidence:

`evidence/powder/g4-live-discovery-2026-08-25.md`

Live qualified candidate:

- profile `srslte-controlled-rf`;
- project/owner namespace `PowderProfiles`;
- profile version 0;
- repo hash `a6da9656` on `refs/heads/master`;
- UE option `srsLTE UE (B210)`;
- visible controlled topology `enb1` + `rue1`.

The live POWDER scheduler exposed the hidden required resource type `nuc5300`. A manual reservation was created and approved for project `WellPulse`:

- `Emulab / nuc1 / 1`;
- `Emulab / nuc2 / 1`;
- no OTA Lab selection;
- no separate frequency range requested for this conducted-RF qualification;
- class reservation: No;
- approved window: **2026-08-25 19:00–22:00 Africa/Cairo**.

Scheduled experiment:

- name `WP-G4-CTRL-RF`;
- project `WellPulse`;
- profile `srslte-controlled-rf`;
- RefSpec `refs/heads/master (a6da9656)`;
- state at scheduling: `scheduled`;
- current usage at scheduling: `0 Node Hours`.

### Exact G4 action at 19:00 Cairo

1. Open the existing scheduled experiment; do not create another experiment.
2. Refresh and wait for `READY`.
3. Capture actual allocated node/radio bindings from the live manifest/list view; do not assume reservation node IDs are the final manifest until observed.
4. Verify B210/controlled-RF topology and exact current endpoints.
5. SSH with the canonical explicit Golden key using the live endpoint.
6. Validate the controlled LTE physical-RF lifecycle/data path without using the POWDER control network as the experimental path.
7. Preserve credential-free evidence only.
8. Terminate manually and verify zero active usage / `0 Node Hours`.
9. Record G4 PASS/FAIL before moving into G5/WP2.

G4 remains **non-scored infrastructure qualification** and adds 0% scientific completion.

## 2026-08-25 serious related-work / comparator survey

The pre-G4 interval is being used for a manuscript-grade rapid structured benchmark rather than a casual literature scan.

Canonical artifacts:

- `docs/WP0_RELATED_WORK_BENCHMARK_2026-08-25.md`
- `docs/WP0_RELATED_WORK_MATRIX_2026-08-25.csv`
- `docs/WP0_COMPARATOR_AUDIT_2026-08-25.md`
- updated `docs/WP0_NOVELTY_VENUE_LOCK_2026-08-24.md`

### Survey conclusion so far

The literature is crowded enough that WellPulse must **not** claim standalone novelty for:

- MQTT reliability testing;
- buffering/store-and-forward;
- SQLite/database-backed retransmission;
- offline-first operation;
- application identifiers/sequence numbers;
- checksum or idempotency as isolated concepts;
- edge/cloud reconciliation;
- cellular/5G/NB-IoT for IoT;
- agricultural/solar monitoring using MQTT;
- real-hardware/testbed validation itself.

The defensible paper story is therefore a **compound empirical and methodological contribution**: matched transport comparison, explicit network-vs-process-restart decomposition, record-level integrity/reconciliation, causal controlled physical RF, FIT -> conducted RF -> OTA transportability, run-level randomized/precision-based inference, and complete reproducibility/evidence reconstruction.

### Material comparator finding

The deeper audit found an important reviewer risk that the earlier survey had not fully resolved:

- Eclipse Paho Python, which underlies current B1/W1, does not durably persist its MQTT client session across process restart.
- Other standard Eclipse Paho implementations, especially Java, provide file-backed persistence and can configure persistent disconnected buffering.

Therefore B1 remains valuable as the **matched same-implementation causal comparator**, but it must not be represented as the strongest durable MQTT-client configuration available generally.

Provisional preferred defense:

- keep B1 for the full matched primary B1/W1 campaign;
- qualify a candidate `B2_MQTT_DURABLE_CLIENT` locally using authoritative durable-client settings;
- if B2 demonstrably survives offline generation + client-process restart, freeze a compact B2 sensitivity comparison focused on S2/S3 rather than inflate the whole study into a three-arm matrix;
- do not change the primary scientific matrix until B2 semantics and the exact amendment are explicitly frozen.

`docs/WP0_COMPARATOR_AUDIT_2026-08-25.md` is authoritative for this pre-score issue.

One high-priority direct competitor still needs full-text recovery before final manuscript novelty freeze:

Gaspar et al., *The Price of Reliability: Stress-Testing MQTT in Practical IoT Communications*, IEEE Internet of Things Magazine (2026), DOI `10.1109/MIOT.2026.3681190`.

Metadata is confirmed. Methods/results must not be inferred until the paper is obtained/read.

### Comparator gate

**G4 is not blocked by this finding.** G4 contains no scored B1/W1/B2 science.

**Scored execution is blocked until the comparator review is explicitly closed.**

After G4, G5/WP2 non-scored RF/user-plane calibration may proceed while the comparator sensitivity decision is finalized, but no scored B1/W1/B2 run is authorized by a G4 PASS alone.

## Automation / security state

Canonical manual acceptance SSH key:

- label `WellPulse-POWDER-Golden`;
- fingerprint `SHA256:fLOBcEmuJ/ozS3Zyo1kRimvbnOm4Fb1yzP0f5X5TOgs`;
- local private key `%USERPROFILE%\.ssh\wellpulse_powder_golden`.

Never request, echo, commit or copy the private key or passphrase.

The GitHub repository secret `POWDER_SSH_PRIVATE_KEY` is known to contain a public key rather than a usable private key. Failed attach attempts are troubleshooting only. Do not rerun them merely to reproduce an already accepted G3 result. Repair this credential path before trusting automated SSH/scored execution.

The full resource-creating G3 workflow remains frozen. After G4 passes manually, build automation by cloning the proven current G4 lifecycle rather than trial-and-error resource creation.

## Troubleshooting history — quarantined

Do not promote these into scientific evidence:

- `wpplmb6787317` / `srs-rf-matrix`: failed before READY because it requested `n310` while WellPulse entitlement was 0; never resubmit unchanged.
- `wphnd8201533` / `srsran-handover`: exploratory/invalid feasibility attempt.
- earlier pre-Golden G1 attempts.
- failed G3 GitHub attach attempts caused by the bad repository SSH secret.

## Scientific critical path

```text
G4 manual controlled-RF lifecycle qualification
        ↓
G5 / WP2 real user-plane + RF impairment calibration
        ↓
close B2 durable-client comparator gate before scoring
        ↓
freeze Q0-Q3 + H + exact scored protocol amendment if needed
        ↓
WP3 conducted scored campaign
        ↓
WP4 compact OTA replication
        ↓
WP5 deterministic analysis + artifact + manuscript closure
```

Planning estimate remains approximately 27–48 active hours from the pre-G4 state to a paper-ready package, excluding resource wait time and any small additional B2 sensitivity experiment created by the comparator audit.

## Reproducibility read order for a new agent

Read in this order before acting:

1. `HANDOVER_CURRENT.md`
2. `docs/MILESTONE_STATUS.md`
3. `docs/STATUS.md`
4. `docs/DECISIONS.md`
5. `docs/WP0_NOVELTY_VENUE_LOCK_2026-08-24.md`
6. `docs/WP0_RELATED_WORK_BENCHMARK_2026-08-25.md`
7. `docs/WP0_COMPARATOR_AUDIT_2026-08-25.md`
8. `evidence/powder/g4-live-discovery-2026-08-25.md`
9. `evidence/powder/g3-simstack-2026-08-24.md`
10. `powder/MANUAL_GOLDEN_PATH.md`
11. `experiments/WP-PWD01/protocol.md`
12. `experiments/WP-PWD01/analysis-plan.md`
13. `experiments/WP-PWD01/evidence-schema.md`
14. `experiments/WP-PWD01/randomization-plan.csv`
15. `experiments/WP-PWD01/run-matrix.yaml`

Do not infer current profile availability, actual resource binding, or comparator semantics from historical assumptions. Verify the live POWDER lifecycle and locally validate any proposed B2 durable-client behavior before freezing scored science.

## Handover completion checklist

Before ending any material WellPulse work block:

1. Update this file.
2. Update `docs/MILESTONE_STATUS.md` when a WP/gate/progress/time estimate changes.
3. Update `docs/STATUS.md`.
4. Update `docs/DECISIONS.md` only if a decision changed.
5. Update relevant sanitized evidence.
6. Update the Drive Current Handover Index and `MILESTONES` tab.
7. Preserve exact PASS/FAIL, exclusions, evidence boundary, teardown state and next action.
8. Ensure a new agent can resume without reading chat history.
