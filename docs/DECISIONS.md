# Decision Register

## D-001 — Validation order
FIT IoT-LAB is the first completed remote-testbed layer. POWDER is the next controlled real-RF layer; compact indoor OTA follows only after the conducted-RF gate. Outdoor/rural validation remains a later distinct layer rather than an automatic extension.

## D-002 — Smallest publishable experiment
Keep the paper focused on durable telemetry resilience. Do not expand into GPU, massive MIMO, O-RAN/RIC, mobility, multi-rate sweeps, or unrelated networking features merely because POWDER exposes them.

## D-003 — Baseline evolution
The publish-only/non-durable baseline remains valid historical evidence for FIT WP-RT01 and as a lower-bound sanity reference. For POWDER and the Q1-oriented manuscript, the **primary comparator is upgraded to a stronger standard MQTT QoS 1 + automatic reconnect baseline with volatile client state and no application-level disk durability/reconciliation**. This avoids a strawman comparison and separates network-only resilience from restart durability.

## D-004 — No evidence inflation
Remote networking evidence is not pump, hydraulic, groundwater, agronomic, Siwa field, or rural-generalization evidence.

## D-005 — No unnecessary BYOD initially
Use existing testbed compute/radio resources first. Custom hardware shipping is deferred unless it becomes necessary for a material claim.

## D-006 — Publication novelty position
Do not claim novelty for generic MQTT, buffering, store-and-forward, offline-first operation, or 5G. The publication contribution is the combination of lightweight durable record semantics, idempotent reconciliation, a strong matched MQTT baseline, a cross-layer FIT -> controlled real-RF -> OTA validation ladder, and publication-grade reproducibility.

## D-007 — Primary venue-fit target
Design the manuscript first for **Internet of Things (Elsevier)**, with **Computer Networks** and **Computer Communications** as backups depending on final network-measurement emphasis. Re-verify current Q1/indexing/APC/author guidance immediately before submission; do not freeze a static quartile claim months in advance.

## D-008 — Statistical unit and anti-pseudoreplication
The run is the statistical unit. Telemetry messages within a run are repeated observations, not thousands of independent replicates. Use paired run-level comparisons and effect-size-first reporting.

## D-009 — Precision-based replication
POWDER impairment scenarios start at three paired B1/W1 blocks and may extend to five pairs only under the frozen precision rule. Stopping may not depend on p-values, effect direction, or whether the result favors WellPulse.

## D-010 — Manual-first POWDER execution
No resource-creating POWDER automation is trusted merely because API syntax or a workflow appears to work. Each lifecycle layer must first pass manually through the live POWDER UI and be captured as reproducible evidence. Automation may clone a proven manual path later; it may not define the path by trial and error.

The first accepted baseline is the 2026-08-24 manual `srsLTE-SIM:9` run documented in `evidence/powder/manual-golden-path-2026-08-24.md`.

## D-011 — Canonical POWDER SSH key
The canonical manual acceptance key is `WellPulse-POWDER-Golden`, fingerprint `SHA256:fLOBcEmuJ/ozS3Zyo1kRimvbnOm4Fb1yzP0f5X5TOgs`.

Its private key and passphrase remain local and must never enter Git, evidence bundles, chat-derived repository files, or raw portal exports. Older registered keys may remain temporarily for historical plumbing but are not assumed to be acceptance keys unless explicitly re-qualified.

## D-012 — POWDER raw-log minimization
Do not commit raw POWDER portal logs when they contain experiment RPC tokens, certificate blocks, account metadata, or other credential-like material. Preserve only the minimum sanitized fields needed to reproduce and audit an experiment: experiment/profile identifiers, resource bindings, software/image identity, SSH endpoint/auth mode, state transitions, timestamps, and acceptance results.

## D-013 — Troubleshooting runs are not evidence
Failed or exploratory POWDER experiments remain visible in history and may be cited for troubleshooting provenance, but they are never silently promoted into the scientific corpus. The failed `srs-rf-matrix`, exploratory `srsran-handover`, and pre-Golden-key `WP-G1-SIM` attempts are explicitly excluded. Only a run that passes its frozen gate may become the canonical baseline for the next layer.

## D-014 — G3 attach automation without resource-creation automation
For the current G3 gate, manual resource creation remains mandatory. After a fresh `srsLTE-SIM:9` experiment is created manually and reaches READY, `.github/workflows/powder-g3-attach.yml` may attach to that exact experiment UUID and automate target validation, manifest/SSH discovery, the profile-authoritative file-based `pdsch_enodeb -> file -> pdsch_ue` check, sanitized evidence capture, and fail-safe termination.

This does **not** unfreeze resource-creating automation. `.github/workflows/powder-g3-simstack.yml` remains unapproved for execution until the equivalent G3 manual gate has passed and the canonical handover explicitly changes that state. G3 remains non-scored/no-RF and adds no scientific percentage.
