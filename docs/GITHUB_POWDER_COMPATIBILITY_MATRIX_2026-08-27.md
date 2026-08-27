# GitHub Actions ↔ POWDER Compatibility Matrix — 2026-08-27

**Gate:** `PRE_INTEGRATION_COMPATIBILITY_GATE=BLOCKED`  
**Rebook:** `REBOOK_GOLDEN=false`  
**Purpose:** freeze verified interface facts and material unknowns before a new non-scored Golden reservation.

## Decision summary

The integration is not yet ready to rebook. The previous A3 run established that implementation-first debugging is too costly inside a reservation window. The next reservation may be requested only after all blocking rows below are closed or explicitly bounded by a fail-closed design.

| Boundary | GitHub / automation side | POWDER / remote side | Exact verified contract/version | Risk | Acceptance evidence | Status |
|---|---|---|---|---|---|---|
| Repository state | `aayoubMSA/WellPulse` | deployed copy on both nodes | Attempt 6 audited SHA `42a25cc7331cb484445eb7ef61ddfb8917af3d1c`; adopter verified same SHA on both nodes before science | stale/mismatched code | Attempt 6 adopter logs | PASS pattern; reverify next reservation |
| Runner OS | GitHub-hosted runner | n/a | runner `2.336.0`; Ubuntu `24.04.4`; image `ubuntu-24.04`; image version observed `20260816.277.1` | `ubuntu-latest` / hosted image drift | Attempt 6 workflow log | BLOCKED: capture/pin policy required |
| Checkout action | `actions/checkout@v4` | n/a | resolved SHA `11d5960a326750d5838078e36cf38b85af677262`; Node 24 execution warning observed | moving major tag/runtime drift | Attempt 6 workflow log | BLOCKED: pin immutable SHA in Golden path |
| Portal API | clone/install client at job runtime | Emulab/POWDER Portal API | official current Portal API is the supported programmatic interface; project is under active development | current script clones repository HEAD with no immutable revision | Emulab manual + `powder/wp2_a3_adopt.sh` | BLOCKED: pin source revision and log it |
| Experiment identity | workflow request JSON | Portal experiment | A3 UUID `357f3275-403d-491a-906f-99677bdf454f`; was `ready` during Attempt 6; later `404 No such experiment` at 2026-08-27T11:55:56Z | stale experiment ID / expiry or removal | Attempt 6 + Attempt 7 logs | PASS fail-close behavior; new reservation must rebind dynamically |
| Node role identity | orchestration expects core/UE | profile dispatch | `/local/repository/bin/start.sh` dispatches by `geni-get client_id`: `enb1 -> start-enb.sh`, `rue1 -> start-ue.sh` | hostname is not authoritative role identity | run `33067176463` | PASS; reverify profile revision |
| Hardware type | manifest parser requires `nuc5300` | both A3 nodes | `enb1=nuc5300`, `rue1=nuc5300` | wrong hardware binding | Attempt 6 manifest | PASS for A3; reverify new reservation |
| Disk image | n/a | both A3 nodes | `urn:publicid:IDN+emulab.net+image+PowderProfiles:U18LL-SRSLTE:1` | image/package drift | Attempt 6 manifest | PASS identity only; package fingerprint incomplete |
| Base Python | runner Python separate | both A3 nodes | system `python3=3.6.9` | too old for scientific runtime | Attempt 6 runtime inspection | PASS because not used after bootstrap |
| Scientific Python | bootstrap orchestration | both A3 nodes | isolated Python `3.11.13` at `~/.wp2-golden-venv/bin/python` | runtime mismatch | bootstrap evidence | PASS |
| MQTT library | package install | both A3 nodes | `paho-mqtt=2.1.0`; enforced before Golden | API/callback drift | bootstrap + G0 contract | PASS |
| `uv` installer | fetched live from `astral.sh/uv/install.sh` | installed on nodes | exact version recorded only after installation; installer URL currently unpinned | bootstrap behavior drift | `scripts/wp2_a3_runtime_bootstrap.sh` | BLOCKED: pin uv version before rebook |
| rclone binary | GitHub precheck installs current; node bootstrap downloads current if missing | UE uses rclone for off-POWDER escrow | latest stable verified externally on 2026-08-27 is `v1.75.0`; official SHA-256 for Linux amd64 ZIP `aa2804e08f48250e71009c727124b6341cd0288465804a9a09d14663cabafbaa` | moving download / binary drift | rclone release/download checksums | BLOCKED until scripts use pinned binary + checksum |
| Google Drive OAuth | encrypted rclone config transported from repo secret-derived material | UE writes off-POWDER evidence | current remote uses rclone shared Google Drive client ID; rclone states shared ID will stop working during 2026 | evidence escrow can fail after scientific run | Attempt 6 warning + official rclone Drive docs | BLOCKED: dedicated OAuth client required and must pass write/read/hash test |
| Persistent storage | GitHub has no authority | `/proj/WellPulse` | path existed and was writable on A3; dual-copy design requires persistent `/proj` before teardown | evidence loss at experiment destruction | adopter precheck + escrow design | PASS design; reverify new reservation |
| RF command semantics | workflow/status probes | `tmcc attenuator` | a call used as a status probe printed `changing attenuation` during Attempt 6 | observation can mutate experiment state | Attempt 6 targeted fail-close evidence | BLOCKED/UNSAFE: never use as live status query unless authoritative read-only syntax is proven |
| Scientific-window observability | GitHub can launch independent SSH probes | running Golden | unqualified independent probes can contaminate timing/state | invalid run | Attempt 6 | PASS policy: prohibit independent unqualified probes during G3–G10 |
| TLS endpoint | orchestration | broker `172.16.0.1:8883` | TLS identity verified for IP; Mosquitto config requires TLS 1.2; future diagnostics use `openssl s_client -brief` | verbose diagnostics previously persisted TLS session material | Attempt 6 + hardening commits | PARTIAL: redaction fixed; exact OpenSSL/Mosquitto versions still required |
| Network route | runner reaches external nodes by SSH | UE route to broker | A3 UE: `172.16.0.1 dev tun_srsue src 172.16.0.2`; Q0 5/5 ICMP, 0% loss | stale tunnel/route | Attempt 6 Q0 gate | PASS pattern; reverify |
| Receiver process lifecycle | SSH launches core receiver | long-lived Python receiver | Attempt 6 spent ~13m44s between G2 receiver launch and G3 despite receiver being intended as background process | reservation-window waste / SSH session not fully detached | Attempt 6 timestamps | BLOCKED: detach stdin/session and bound launch return time |
| Fixed observation | workflow waits on sender | UE sender | G7 horizon fixed at 300 s from `t_service_ready` | cannot truncate due reservation pressure | frozen protocol | PASS invariant |
| Reservation time budget | workflow previously checked experiment status only | experiment has finite reservation/lifecycle | A3 disappeared before Attempt 7; Attempt 6 lost ~14 min at G2 | run can start too late to reach G9 safely | Attempt 6/7 empirical evidence | BLOCKED: pre-launch minimum remaining-time guard required |
| Evidence teardown guard | workflow | `/proj` + Drive | `EVIDENCE_ESCROW_GATE=PASS` required before teardown | loss of raw evidence | frozen handover/protocol | PASS invariant; dependencies above must close |

## Authoritative-source notes

1. Emulab's current manual describes the Portal API as the supported API for programmatically instantiating, interacting with, and terminating experiments, and states that it is under active development. Therefore a mutable HEAD install is not acceptable for a reproducibility-critical Golden path.
2. rclone's current Google Drive documentation states that its shared Google Drive client ID is being retired and will stop working during 2026; a dedicated client ID is therefore a precondition for reliable G9 escrow.
3. The official rclone download archive identifies `v1.75.0` as the current stable release on 2026-08-27 and publishes SHA-256 checksums for its binaries.

## Required closures before rebooking

### Software/version closure

- [ ] Pin `actions/checkout` to an immutable verified SHA for the Golden workflow path.
- [ ] Pin the Portal API client to a verified upstream revision and record the revision at runtime.
- [ ] Pin `uv` to an exact tested release.
- [ ] Pin rclone `v1.75.0` and verify SHA-256 before install.
- [ ] Record OpenSSL and Mosquitto exact versions on POWDER nodes.
- [ ] Record runner image/version and fail if the selected execution contract changes materially.

### Contract closure

- [x] Treat `tmcc attenuator` as mutating/unsafe for observation.
- [x] Prohibit independent unqualified live probes during G3–G10.
- [ ] Establish the allowed Portal API lifecycle/status calls and their error semantics from authoritative docs/source or conservatively bound unknowns.
- [ ] Verify future profile revision/start scripts and exact hardware bindings before science.

### Lifecycle closure

- [ ] Fix receiver startup so the SSH launch returns promptly after a fully detached process is confirmed alive.
- [ ] Add a pre-launch reservation-time budget guard covering setup + worst-case recovery + 300 s G7 + G8 + G9 + safe shutdown margin.
- [ ] Do not launch if the time budget cannot complete evidence escrow before reservation expiry.

### Evidence closure

- [ ] Replace the shared rclone Google OAuth client with a dedicated client ID/secret and refreshed token.
- [ ] Verify off-POWDER escrow by disposable write → read/list → content/hash comparison → delete test before requesting the next reservation.
- [ ] Verify `/proj/WellPulse` write/read/hash on the new reservation before science.

## Gate

Current decision:

`PRE_INTEGRATION_COMPATIBILITY_GATE=BLOCKED`

`REBOOK_GOLDEN=false`

A new reservation is not authorized until the material BLOCKED rows are closed.
