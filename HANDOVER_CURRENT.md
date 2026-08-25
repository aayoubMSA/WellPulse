# WellPulse — Current Handover

Last updated: 2026-08-25 late session, Africa/Cairo

## Standing handover rule

No material project state may exist only in chat. Decisions, results, artifacts, blockers, evidence boundaries, milestone percentages and the exact next action must be recoverable from GitHub and/or Drive.

## Executive state

Completed evidence/infrastructure:

- FIT IoT-LAB embedded-hardware scientific evidence layer: **FINAL PASS**.
- POWDER G0 account/project: **PASS**.
- POWDER G1 compute provisioning: **PASS**.
- POWDER G2 explicit-key SSH + teardown: **PASS**.
- POWDER G3 file-based simulated LTE stack/data path: **PASS**.
- POWDER G4 controlled physical-RF LTE lifecycle + attach + user-plane + teardown: **PASS**.

Scientific weighted completion remains **20%**.

- WP0 Novelty & Venue Lock: **8/8 complete**.
- WP1 Confirmatory Protocol & Statistics Freeze: **12/12 design work complete**, but comparator sufficiency is **OPEN FOR PRE-SCORE REVIEW**.
- WP2 RF Calibration & Measurement Validation: **0/15 — NEXT**.
- WP3 Conducted-RF Confirmatory Campaign: **0/30 — blocked by WP2 + comparator freeze + explicit scored authorization**.
- WP4 OTA External Replication: **0/15 — blocked by WP3**.
- WP5 Analysis + Artifact + Paper Closure: **0/20 scientific closure**.

`scored_runs_authorized = false`.

No POWDER G4 observation belongs to the scored scientific corpus.

## Canonical repositories and workspaces

- GitHub: `aayoubMSA/WellPulse`.
- Drive project root `P12_WellPulse`: `1eBQJ8STP-x-MaW0-2m07G7kCoF4UnLft`.
- Drive validation workspace `00_Validation_Workspace`: `1SydHCA2jlkatxdGgUtJ1P8atgyi8_ta3`.
- Drive raw evidence `02_RAW_EVIDENCE`: `11xaitxG0vkV6fCzK_JgLAacrdhjz7GBf`.
- Drive handover folder `WellPulse Handover`: `1Du4j_YkMLvQjWJCxV5zqxxK6OGG2Q0hA`.
- Drive current handover index: `1Gd4FzyJ_dW6-AK6wQc4FW7LAWVb2GNzG0t-xHaSEwn4`.

## Scientific design — frozen working baseline

Canonical protocol: `experiments/WP-PWD01/protocol.md`, v0.4.

Primary matched comparison:

- `B1_MQTT_QOS1`: Paho Python MQTT v3.1.1, QoS1, TLS scored path, automatic reconnect, `clean_session=False`, volatile client state, no application-level disk durability/reconciliation.
- `W1_OFFLINE_FIRST`: same low-level Paho Python session plus SQLite durable application queue, stable record identity/checksum, replay, idempotent receiver and reconciliation.

Frozen low-level parameters:

- `paho-mqtt==2.1.0`;
- keepalive 60 s;
- reconnect 1–8 s;
- outgoing queue 4096;
- inflight 20.

Scenarios: S0 healthy, S1 intermittent, S2 hard outage, S3 hard outage + gateway-process restart. Run is the statistical unit. Working conducted campaign remains 24–36 scored B1/W1 runs under the precision rule; OTA remains a compact 12-run S1/S2 replication if the conducted gate passes.

## FIT IoT-LAB accepted scientific evidence

Canonical result: `experiments/WP-RT01/FINAL_RESULTS_2026-08-23.md`.

- Grenoble A8 hardware.
- B0/W1 × C0/C1/C2 × 3 replicates = 18 final cells.
- exactly 10,000 records per cell.
- 18/18 final reconciliation PASS.
- W1 achieved 100% final completeness, zero permanent missing records and zero final duplicates under controlled broker outage and broker-outage + gateway restart in 3/3 replicates.
- B0 retained 80% under C1/C2.

FIT is real embedded-hardware evidence under controlled connectivity impairment. It is not physical-RF causal evidence and B0 is a historical lower-bound comparator.

## POWDER G3 accepted infrastructure evidence

Canonical evidence: `evidence/powder/g3-simstack-2026-08-24.md`.

Accepted run: `WP-G3-SIMSTACK`, UUID `3484b01d-7eca-48e7-9e34-866680057b0d`; file-based LTE simulation path PASS; cleanup/teardown PASS with `Current Usage: 0 Node Hours`. G3 has no SDR/physical-RF/scientific result.

## POWDER G4 — FINAL PASS

Canonical evidence: `evidence/powder/g4-ue-attach-2026-08-25.md`.

Successful rerun:

- experiment `WP-G4-CTRL-RF`;
- UUID `0e4269fb-06dd-432b-abec-4bca685a05af`;
- profile `srslte-controlled-rf`;
- RefSpec `refs/heads/master (a6da9656)`;
- live role binding: `enb1 -> nuc2`, `rue1 -> nuc1`;
- explicit Golden-key SSH PASS on both nodes;
- physical B210 EPC/eNodeB startup PASS;
- physical B210 srsUE startup PASS;
- LTE attach PASS;
- UE IP `172.16.0.2`;
- E-RAB/bearer establishment PASS;
- UE interface `tun_srsue 172.16.0.2/24`;
- EPC interface `srs_spgw_sgi 172.16.0.1/24`;
- bounded LTE user-plane command `ping -I tun_srsue -c 5 172.16.0.1`;
- result **5/5 replies, 0% packet loss**;
- manual termination PASS;
- final portal **no active experiments; Current Usage 0 Node Hours**.

Accepted G4 chain:

`READY -> actual live binding -> SSH -> physical B210 network startup -> physical B210 UE startup -> LTE attach -> bearer -> user-plane IP transfer -> terminate -> zero usage`

G4 is **non-scored infrastructure qualification** and contributes 0% scientific completion.

Raw evidence in Drive includes final teardown screenshot `POWDER_G4_TEARDOWN_ZERO_USAGE_PASS_2026-08-25.png`, id `1lbgnFuesXbjd13WxJUPQY6zjvRCWQMLb`.

## Comparator gate — still open

The serious related-work/comparator audit remains authoritative in `docs/WP0_COMPARATOR_AUDIT_2026-08-25.md`.

Key finding: current Paho Python B1 is the clean matched same-implementation comparator but is not the strongest durable MQTT client generally. Other standard Paho implementations can provide durable persistence/offline buffering.

Preferred route remains:

- retain B1 for the matched B1/W1 primary campaign;
- locally qualify candidate `B2_MQTT_DURABLE_CLIENT`;
- if valid, freeze a compact S2/S3 B2 sensitivity comparison rather than inflate the full primary matrix;
- keep B2 separate from primary paired inference.

No scored run may begin until the comparator review and exact amendment are explicitly frozen.

## Automation / security state

Canonical manual key remains `WellPulse-POWDER-Golden`, fingerprint `SHA256:fLOBcEmuJ/ozS3Zyo1kRimvbnOm4Fb1yzP0f5X5TOgs`. Never expose/commit/copy the private key or passphrase.

G4 manual qualification is now complete, so the **proven G4 lifecycle may be automated**. Do not rediscover the resource lifecycle by trial and error. Any new RF-control/impairment layer must receive one bounded manual qualification before repetitive automation.

The GitHub `POWDER_SSH_PRIVATE_KEY` path remains known-bad and must be repaired before trusting automated SSH or scored execution.

## Immediate next gate

**G5 / WP2 — RF impairment and measurement calibration.**

Do not repeat G4. Reuse the proven lifecycle and add only the minimum RF-control/measurement layer needed to qualify controlled impairment.

An approved fallback reservation still exists for `nuc1+nuc2` on **2026-08-26 19:00–22:00 Africa/Cairo**. Highest-ROI use is G5/WP2, provided its new RF-control procedure is prepared and manually bounded first.

## Scientific critical path

```text
G4 controlled physical-RF lifecycle PASS
        ↓
G5 / WP2 RF impairment + measurement calibration
        ↓
close B2 durable-client comparator gate before scoring
        ↓
freeze Q0-Q3 + H + exact protocol amendment if needed
        ↓
WP3 conducted scored campaign
        ↓
WP4 compact OTA replication
        ↓
WP5 deterministic analysis + artifact + manuscript closure
```

## Evidence boundary

Current remote-testbed evidence supports communications/radio-link resilience, telemetry integrity/completeness, recovery, reconnect, gateway-process restart and controlled LTE connectivity. It does **not** validate pump mechanics, hydraulics, groundwater, crop/agronomic outcomes, Siwa field performance or generic rural-field generalization.

## Reproducibility read order for a new agent

1. `HANDOVER_CURRENT.md`
2. `docs/MILESTONE_STATUS.md`
3. `docs/STATUS.md`
4. `docs/DECISIONS.md`
5. `evidence/powder/g4-ue-attach-2026-08-25.md`
6. `docs/WP0_COMPARATOR_AUDIT_2026-08-25.md`
7. `experiments/WP-PWD01/protocol.md`
8. `experiments/WP-PWD01/analysis-plan.md`
9. `experiments/WP-PWD01/evidence-schema.md`
10. `experiments/WP-PWD01/randomization-plan.csv`
11. `experiments/WP-PWD01/run-matrix.yaml`
12. `powder/MANUAL_GOLDEN_PATH.md`

Do not infer current live bindings from past node numbers; roles can reverse between runs. Verify live bindings each time.