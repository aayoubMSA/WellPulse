# GitHub Actions ↔ POWDER Compatibility Matrix — 2026-08-27

**Gate:** `PRE_INTEGRATION_COMPATIBILITY_GATE=PASS`  
**Golden rebook:** `REBOOK_GOLDEN=false`  
**Separate blocker:** `LIVE_HCI_AND_RAW_EVIDENCE_GATE=BLOCKED`

## Decision summary

K1–K8 are now closed from combined immutable supply-chain, offline fail-close, and bounded live compatibility evidence.

The decisive live evidence is compatibility run `33085406598`, experiment `fc7c2187-2376-4a92-8de1-4665a06ea943`, classified `INFRASTRUCTURE_ONLY_NON_SCORED`. It reached READY, verified exact profile/hardware/image/SSH/runtime identity, passed live expiry/time-budget binding, passed bounded detached-process return, passed cross-node `/proj/WellPulse` persistence, passed controller pull + GitHub artifact + independent read-back/hash verification, and requested mandatory termination.

Golden remains blocked only because the separate HCI/raw-evidence gate has not yet passed.

| Boundary | Exact verified contract/version | Acceptance evidence | Status |
|---|---|---|---|
| Repository/controller authority | `aayoubMSA/WellPulse`, immutable workflow state | K1/K8 records | PASS |
| Runner | `ubuntu-24.04`; live image `20260823.283.1`; runner `2.336.0` | run `33085406598` | PASS / REVERIFY PER RUN |
| Controller actions | checkout `fbc6f3992d24b796d5a048ff273f7fcc4a7b6c09`; upload-artifact `b7c566a772e6b6bfb58ed0dc250532a479d7789f`; download-artifact `37930b1c2abaa49bbe596cd826c3c89aef350131` | static acceptance + live run | PASS / PINNED |
| Portal API client | Flux GitLab `emulab/portal-api`, revision `01be03b2f60c067815a7654437320dd981ca3617`, source capture SHA-256 `3e9f0073b2df6840801baa38333f1f04debd02a2eaa57997939b6f7ee678d4c8` | K1-P2 + K3 QA | PASS / PINNED |
| Portal lifecycle/status | create/get/manifests/terminate; fail closed on invalid/unknown state | K3 QA `33087174307`; live run | PASS |
| Experiment status/expiry | `ready`; exact ID match; unique `$.expires_at=2026-08-27T16:00:53Z` | run `33085406598` | PASS |
| Reservation budget | remaining `3283 s`; minimum `2700 s` | `PRELAUNCH_TIME_GATE=PASS` | PASS |
| Profile revision | `a6da96560b6526dc6816761282722c996418fd8c` | live node fingerprints | PASS / FROZEN |
| Bindings | `enb1 -> nuc1`, `rue1 -> nuc2`, `ue_type=srsue` | Portal bindings + manifests | PASS |
| Hardware | both `nuc5300` | live manifest | PASS |
| Image | `urn:publicid:IDN+emulab.net+image+PowderProfiles:U18LL-SRSLTE:1` | live manifest | PASS |
| Base node runtime | Linux `4.15.0-91-lowlatency`; Python `3.6.9`; OpenSSL `1.1.1 11 Sep 2018`; base `mosquitto` absent | live fingerprints | PASS AS BASELINE |
| Scientific runtime contract | uv `0.12.1`; isolated Python `3.11.13`; `paho-mqtt=2.1.0`; rclone `1.75.0`, all frozen/hash-verified | frozen bootstrap + prior qualified path + static acceptance | PASS / PINNED |
| Receiver/process detach | bounded `ssh -n` + `nohup` + stdin detach; live return `1 s <= 15 s` | K4 live step | PASS |
| Persistent evidence path | `/proj/WellPulse` writable on both nodes; cross-node write/read/hash | K6 live step | PASS |
| Controller off-POWDER transport | `/proj -> controller tar -> GitHub artifact -> independent download -> outer+internal hash` | bundle SHA `f5464e08b41e2bcb81facd26daa2ee11ad115fa06554d40eea9bc01e0b0e6616`; artifact ID `9652138428` | PASS |
| Evidence teardown authority | `CONTROLLER_OFFPOWDER_GATE=PASS`; `EVIDENCE_ESCROW_GATE=PASS`; `TEARDOWN_AUTHORIZED=YES` only after verified read-back | live run | PASS |
| RF observation | `tmcc attenuator` classified mutating/unsafe for observation; no independent unqualified RF probe | K7 semantic guard `33087181821`; integrated static `33087199247` | PASS POLICY |
| HCI control | protected-window HCI must be passive/one-way | frozen policy | PASS POLICY; LIVE HCI GATE OPEN |
| Cleanup | terminate path accepted in successful run; same path independently verified absent on earlier compatibility experiment | successful run + post-cleanup diagnosis `33086065236` | PASS / BOUNDED |
| Google Drive | optional secondary mirror only; not teardown-critical | K-fastlane evidence architecture | OUTSIDE CRITICAL PATH |

## K-series closure

- `K1=PASS`
- `K2=PASS`
- `K3=PASS`
- `K4=PASS`
- `K5=PASS`
- `K6=PASS`
- `K7=PASS`
- `K8=PASS`

Canonical closure record:

`docs/K8_PREINTEGRATION_COMPATIBILITY_CLOSURE_2026-08-27.md`

## Gate decision

`PRE_INTEGRATION_COMPATIBILITY_GATE=PASS`

The following remains independently required before a new non-scored Golden:

`LIVE_HCI_AND_RAW_EVIDENCE_GATE=PASS`

Therefore:

`REBOOK_GOLDEN=false`

`scored_runs_authorized=false`

Next mission step:

`HCI/raw-evidence gate -> clean non-scored Golden -> freeze H -> WP2 close -> WP3 -> WP4 -> WP5`
