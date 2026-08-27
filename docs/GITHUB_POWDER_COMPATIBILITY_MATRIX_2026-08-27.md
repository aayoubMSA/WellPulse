# GitHub Actions ↔ POWDER Compatibility Matrix — 2026-08-27

**Gate:** `PRE_INTEGRATION_COMPATIBILITY_GATE=BLOCKED`  
**Rebook:** `REBOOK_GOLDEN=false`  
**Purpose:** freeze verified interface facts and material unknowns before a new non-scored Golden reservation.

## Decision summary

The integration is not yet ready to rebook. K1 closed the uv and rclone bootstrap pinning contract and the immutable checkout reference used by the active pre-integration path, but K1 remains fail-closed because the exact immutable upstream revision of the supported Portal API client is unresolved. The next reservation may be requested only after all blocking rows below are closed or explicitly bounded by a fail-closed design.

| Boundary | GitHub / automation side | POWDER / remote side | Exact verified contract/version | Risk | Acceptance evidence | Status |
|---|---|---|---|---|---|---|
| Repository state | `aayoubMSA/WellPulse` | deployed copy on both nodes | Attempt 6 audited SHA `42a25cc7331cb484445eb7ef61ddfb8917af3d1c`; adopter verified same SHA on both nodes before science | stale/mismatched code | Attempt 6 adopter logs | PASS pattern; reverify next reservation |
| Runner OS | GitHub-hosted runner | n/a | pre-integration path uses explicit `ubuntu-24.04`; prior observed runner `2.336.0`, Ubuntu `24.04.4`, image version `20260816.277.1` | hosted image content can still drift under fixed major image label | Attempt 6 log + active static workflow | PARTIAL: moving `ubuntu-latest` removed from pre-integration path; runtime image fingerprint must still be captured/reverified |
| Checkout action | active pre-integration path | n/a | `actions/checkout@11d5960a326750d5838078e36cf38b85af677262` | moving major tag/runtime drift | active `wp2-preintegration-static.yml` + authoritative tag resolution | PASS for pre-integration/future integration contract; local-only workflows are outside live authority |
| Portal API | client must be installed from immutable source | Emulab/POWDER Portal API | supported repository identity is `https://gitlab.flux.utah.edu/emulab/portal-api`; Portal API is under active development | exact upstream client revision unresolved; mutable HEAD unacceptable | POWDER/Emulab manual + K1 closure record | **BLOCKED: `PORTAL_API_REVISION=UNRESOLVED`** |
| Experiment identity | workflow request JSON | Portal experiment | A3 UUID `357f3275-403d-491a-906f-99677bdf454f`; was `ready` during Attempt 6; later `404 No such experiment` at 2026-08-27T11:55:56Z | stale experiment ID / expiry or removal | Attempt 6 + Attempt 7 logs | PASS fail-close behavior; new reservation must rebind dynamically |
| Node role identity | orchestration expects core/UE | profile dispatch | `/local/repository/bin/start.sh` dispatches by `geni-get client_id`: `enb1 -> start-enb.sh`, `rue1 -> start-ue.sh` | hostname is not authoritative role identity | run `33067176463` | PASS; reverify profile revision |
| Hardware type | manifest parser requires `nuc5300` | both A3 nodes | `enb1=nuc5300`, `rue1=nuc5300` | wrong hardware binding | Attempt 6 manifest | PASS for A3; reverify new reservation |
| Disk image | n/a | both A3 nodes | `urn:publicid:IDN+emulab.net+image+PowderProfiles:U18LL-SRSLTE:1` | image/package drift | Attempt 6 manifest | PASS identity only; package fingerprint incomplete |
| Base Python | runner Python separate | both A3 nodes | system `python3=3.6.9` | too old for scientific runtime | Attempt 6 runtime inspection | PASS because not used after bootstrap |
| Scientific Python | bootstrap orchestration | both A3 nodes | isolated Python `3.11.13` at `~/.wp2-golden-venv/bin/python` | runtime mismatch | bootstrap evidence | PASS |
| MQTT library | package install | both A3 nodes | `paho-mqtt=2.1.0`; enforced before Golden | API/callback drift | bootstrap + G0 contract | PASS |
| `uv` binary | verified immutable release archive | installed on nodes | uv `0.12.1`; `uv-x86_64-unknown-linux-gnu.tar.gz`; SHA-256 `90b2f223fb69d19db49e117da601f64978593417988530aa733d456141b4bcbb`; release target commit `329541a503de8a4d9bb021814f9c0875efe033c8` | bootstrap behavior drift | K1 implementation commit `353be59fa222150fbedf731ae45bbac9026ba543` + static checks | **PASS / PINNED** |
| rclone binary | verified exact archive | UE uses rclone for off-POWDER escrow | rclone `v1.75.0`; Linux amd64 ZIP SHA-256 `aa2804e08f48250e71009c727124b6341cd0288465804a9a09d14663cabafbaa` | binary drift | bootstrap + K1 static acceptance | **PASS / PINNED** |
| Google Drive OAuth | encrypted rclone config transported from repo secret-derived material | UE writes off-POWDER evidence | current remote uses rclone shared Google Drive client ID; rclone states shared ID will stop working during 2026 | evidence escrow can fail after scientific run | Attempt 6 warning + official rclone Drive docs | BLOCKED: dedicated OAuth client required and must pass write/read/hash test |
| Persistent storage | GitHub has no authority | `/proj/WellPulse` | path existed and was writable on A3; dual-copy design requires persistent `/proj` before teardown | evidence loss at experiment destruction | adopter precheck + escrow design | PASS design; reverify write/read/hash on new reservation |
| RF command semantics | workflow/status probes | `tmcc attenuator` | a call used as a status probe printed `changing attenuation` during Attempt 6 | observation can mutate experiment state | Attempt 6 targeted fail-close evidence | BLOCKED/UNSAFE for observation: never use as live status query unless authoritative read-only syntax is proven |
| Scientific-window observability | GitHub can launch independent SSH probes | running Golden | unqualified independent probes can contaminate timing/state | invalid run | Attempt 6 | PASS policy: prohibit independent unqualified probes during G3–G10 |
| TLS endpoint | orchestration | broker `172.16.0.1:8883` | TLS identity verified for IP; Mosquitto config requires TLS 1.2; future diagnostics use `openssl s_client -brief` | exact runtime versions still need live verification | Attempt 6 + hardening + static contract | PARTIAL: verbose session-material exposure fixed; exact OpenSSL/Mosquitto versions still required |
| Network route | runner reaches external nodes by SSH | UE route to broker | A3 UE: `172.16.0.1 dev tun_srsue src 172.16.0.2`; Q0 5/5 ICMP, 0% loss | stale tunnel/route | Attempt 6 Q0 gate | PASS pattern; reverify |
| Receiver process lifecycle | SSH launches core receiver | long-lived Python receiver | orchestration now contains bounded SSH launch timeout/stdin detach instrumentation, but no fresh live proof after hardening | previous Attempt 6 spent ~13m44s between G2 and G3 | script/static acceptance + Attempt 6 timestamps | PARTIAL: implementation hardened; live deterministic-return proof still required |
| Fixed observation | workflow waits on sender | UE sender | G7 horizon fixed at 300 s from `t_service_ready` | cannot truncate due reservation pressure | frozen protocol | PASS invariant |
| Reservation time budget | workflow prelaunch guard | experiment has finite reservation/lifecycle | fail-closed `wp2_prelaunch_time_guard.py`; static tests require PASS at 2700 s and BLOCK at 2699 s/invalid timestamp | runtime may still supply stale/unknown expiry semantics | K1 static workflow + Attempt 6/7 evidence | PARTIAL: guard implementation PASS; authoritative lifecycle time source semantics still coupled to Portal closure |
| Evidence teardown guard | workflow | `/proj` + Drive | `EVIDENCE_ESCROW_GATE=PASS` required before teardown | loss of raw evidence | frozen handover/protocol | PASS invariant; transport dependencies remain blocked |

## Authoritative-source notes

1. Emulab/POWDER documentation describes the Portal API as the supported API for programmatically instantiating, interacting with, and terminating experiments, and states that it is under active development. Therefore a mutable HEAD install is not acceptable for a reproducibility-critical Golden path.
2. rclone's Google Drive documentation states that its shared Google Drive client ID is being retired during 2026; a dedicated client ID is therefore a precondition for reliable G9 escrow.
3. K1 froze uv `0.12.1` to the immutable x86_64 Linux GNU release archive SHA-256 `90b2f223fb69d19db49e117da601f64978593417988530aa733d456141b4bcbb`.
4. K1 retained the already frozen rclone `v1.75.0` Linux amd64 ZIP SHA-256 `aa2804e08f48250e71009c727124b6341cd0288465804a9a09d14663cabafbaa`.

## Required closures before rebooking

### Software/version closure

- [x] Pin `actions/checkout` to an immutable verified SHA for the pre-integration/future integration path.
- [ ] Pin the Portal API client to a verified upstream revision and record the revision at runtime.
- [x] Pin `uv` to exact release `0.12.1` and verify archive SHA-256.
- [x] Pin rclone `v1.75.0` and verify SHA-256 before install.
- [ ] Record OpenSSL and Mosquitto exact versions on POWDER nodes.
- [~] Use explicit GitHub runner major image label and capture/reverify exact runtime image fingerprint.

### Contract closure

- [x] Treat `tmcc attenuator` as mutating/unsafe for observation.
- [x] Prohibit independent unqualified live probes during G3–G10.
- [ ] Establish the allowed Portal API lifecycle/status calls and their error semantics from authoritative docs/source or conservatively bound unknowns.
- [ ] Verify future profile revision/start scripts and exact hardware bindings before science.

### Lifecycle closure

- [~] Receiver-launch implementation is bounded/detached statically; fresh live proof remains required.
- [~] Pre-launch reservation-time guard implementation is fail-closed; authoritative expiry/source semantics remain to be qualified.
- [ ] Do not launch if the time budget cannot complete evidence escrow before reservation expiry.

### Evidence closure

- [ ] Replace the shared rclone Google OAuth client with a dedicated client ID/secret and refreshed token.
- [ ] Verify off-POWDER escrow by disposable write → read/list → content/hash comparison → delete test before requesting the next reservation.
- [ ] Verify `/proj/WellPulse` write/read/hash on the new reservation before science.

## K1 status

Canonical K1 record:

`docs/K1_SUPPLY_CHAIN_RUNTIME_PIN_CLOSURE_2026-08-27.md`

Current K1 verdict:

`K1=BLOCKED_PORTAL_API_REVISION`

Closed in K1: immutable checkout SHA for pre-integration path, uv exact binary/version/hash, rclone exact binary/version/hash, static fail-close enforcement.

Remaining K1 blocker: authoritative immutable Portal API client revision.

## Gate

Current decision:

`PRE_INTEGRATION_COMPATIBILITY_GATE=BLOCKED`

`REBOOK_GOLDEN=false`

A new reservation is not authorized until the material BLOCKED rows are closed.
