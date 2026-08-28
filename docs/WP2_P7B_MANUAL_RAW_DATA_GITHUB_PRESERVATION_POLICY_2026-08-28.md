# WP2-P7B Manual Execution — GitHub Raw-Data Preservation Policy — 2026-08-28

## Mandatory rule

For the manual P7B-RQ2 execution lane, experiment completion and teardown are prohibited until all available raw evidence has been copied off POWDER to GitHub, hashed, and read back.

Required evidence chain:

`node_raw -> /proj escrow -> controller pull -> GitHub Actions artifact -> readback -> SHA-256 manifest in repository`

If the compressed raw bundle is small enough for normal Git repository storage, the raw archive may additionally be committed under `evidence/powder/`. Otherwise the GitHub Actions artifact is the raw payload and the repository stores its artifact identity, byte size, SHA-256, provenance, and reconstruction metadata.

## Raw evidence scope

Preserve, when generated:

- complete UE raw tree;
- complete CORE raw tree;
- orchestration/module/frontier JSON/JSONL files;
- RF attenuation command evidence;
- LTE/EPC/eNB/UE logs;
- gateway/generator/receiver logs;
- MQTT raw receive/transmit records;
- restart transition and restoration frontier evidence;
- timestamps and run metadata;
- reconstruction inputs and outputs;
- preservation/readback manifests and SHA-256 files.

No raw file may be silently discarded because a cell, service, or reconstruction failed.

## Teardown gate

`TEARDOWN_READY=YES` requires all of:

1. node evidence roots frozen;
2. /proj escrow copy completed;
3. controller/off-node pull completed;
4. GitHub raw artifact uploaded;
5. artifact readback completed;
6. SHA-256 manifest verified;
7. repository evidence index updated.

Until then:

`TEARDOWN_AUTHORIZED=NO`

## HCI rule

During manual execution, each node should expose a simple human-readable status surface in the POWDER SSH browser. Human command blocks must identify `nuc1 / CORE` or `nuc2 / UE`. The HCI is observational only and never substitutes for raw evidence.

## Current lane

Experiment ID: `41d64b85-e743-4d06-a81d-687c28c58e52`

Experiment name: `WP-05-C`

Evidence class: `NON_SCORED_PRE_SCORE_PHYSICAL_QUALIFICATION`

Scored execution: `NO`
