# Project Validation Status

## Current state — 2026-08-25 late session, Africa/Cairo

- Canonical GitHub repository and Drive validation workspace: established.
- FIT IoT-LAB WP-RT01: **COMPLETE / FINAL EVIDENCE PASS**; Grenoble A8; 18/18 final cells reconciled.
- POWDER G0 account/project: **PASS**.
- POWDER G1 compute provisioning: **PASS**.
- POWDER G2 explicit-key SSH + teardown: **PASS**.
- POWDER G3 simulated LTE stack/data path: **PASS**.
- POWDER G4 controlled physical-RF lifecycle and user-plane: **PASS**.
- Scientific weighted completion: **20%**.
- `scored_runs_authorized = false`.

## POWDER G4 accepted evidence

Canonical file: `evidence/powder/g4-ue-attach-2026-08-25.md`.

Accepted successful chain:

`READY -> explicit-key SSH -> physical B210 EPC/eNodeB -> physical B210 srsUE -> LTE attach -> E-RAB/bearer -> UE tunnel 172.16.0.2 -> EPC SGi 172.16.0.1 -> 5/5 LTE user-plane ping -> terminate -> 0 Node Hours`

Successful rerun metadata:

- experiment `WP-G4-CTRL-RF`;
- UUID `0e4269fb-06dd-432b-abec-4bca685a05af`;
- profile `srslte-controlled-rf`;
- RefSpec `refs/heads/master (a6da9656)`;
- `enb1 -> nuc2`, `rue1 -> nuc1`;
- user-plane command: `ping -I tun_srsue -c 5 172.16.0.1`;
- result: **5 transmitted, 5 received, 0% loss**;
- final portal: **no active experiments; Current Usage 0 Node Hours**.

G4 is non-scored infrastructure qualification and adds no scientific percentage.

## Scientific programme state

- WP0 Novelty & Venue Lock: **8/8 complete**.
- WP1 Confirmatory Protocol & Statistics Freeze: **12/12 design work complete**, but comparator sufficiency remains **OPEN FOR PRE-SCORE REVIEW**.
- WP2 RF Calibration & Measurement Validation: **0/15 — NEXT**.
- WP3 Conducted-RF Confirmatory Campaign: **0/30 — BLOCKED BY WP2 + comparator freeze + scored authorization**.
- WP4 OTA External Replication: **0/15 — BLOCKED BY WP3**.
- WP5 Analysis + Artifact + Paper Closure: **0/20 scientific closure**.

## Comparator gate

B1 remains the same-implementation Paho-Python matched comparator but must not be described as the strongest durable MQTT client generally. Candidate `B2_MQTT_DURABLE_CLIENT` remains under review. Exact B2 semantics and any compact S2/S3 sensitivity amendment remain unfrozen.

No scored run may begin until this comparator gate is explicitly closed and WP2 is passed.

## Automation/security state

- The proven G4 lifecycle may now be automated rather than rediscovered manually.
- Any new RF-control/impairment layer still requires one bounded manual qualification before repetitive automation.
- The known-bad GitHub `POWDER_SSH_PRIVATE_KEY` path must be repaired before trusting automated SSH/scored execution.
- Never expose or commit the Golden private key/passphrase.

## Immediate next stage

**G5 / WP2 — RF impairment and measurement calibration.**

An approved `nuc1+nuc2` reservation remains available for **2026-08-26 19:00–22:00 Africa/Cairo**. Use it for G5/WP2 only if the bounded RF-control procedure is ready; do not repeat G4 merely for confirmation.

## Evidence boundary

Accepted G4 evidence proves controlled physical-RF LTE lifecycle, attach/bearer establishment and bounded user-plane IP connectivity. It does not prove calibrated RF impairment, MQTT/WellPulse scientific effects, pump mechanics, hydraulics, groundwater, agronomy, Siwa field performance or generic rural-field generalization.