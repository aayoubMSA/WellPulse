# CL-WP-01 GitHub ↔ CloudLab Compatibility Matrix

**Scope:** first CloudLab activation path for WellPulse.  
**Authority:** root `AGENTS.md` and `docs/PRE_INTEGRATION_COMPATIBILITY_GATE.md`.  
**Live CloudLab mutation:** **NOT AUTHORIZED BY THIS RECORD YET**.

## Frozen known contract

| Boundary | GitHub / WellPulse side | CloudLab side | Exact contract / version | Risk | Acceptance evidence | Status |
|---|---|---|---|---|---|---|
| Profile source | public `aayoubMSA/WellPulse` repository | repository-based profile | CloudLab manual 2026-02-02: public HTTP(S) git repo; top-level `profile.py`; repo cloned to `/local/repository` on experiment nodes | low | static repo/file inspection | PASS |
| Profile language | dependency-free source gate | CloudLab-supported geni-lib runtime | official current docs identify geni-lib `0.9.7.9`; CloudLab portal is authoritative for actual profile evaluation/RSpec generation | medium | GitHub source-contract gate + portal profile evaluation | STATIC PENDING CI / PORTAL PENDING |
| Hardware | `RawPC("edge")`, `RawPC("cloud")` | physical allocatable nodes | no hardware type pinned in revision 1; scheduler chooses compatible bare metal | medium | live manifest required | PENDING LIVE |
| Data network | one LAN; `10.10.0.1/24`, `10.10.0.2/24` | experiment data plane | CloudLab LAN profile semantics | low | source-contract check + portal render + live ping | STATIC PENDING / LIVE PENDING |
| Startup mutation | none | none beyond normal provisioning | no `Install`/`Execute`/`addService` in revision 1 | low | fail-closed source scan | PENDING CI |
| Persistence | Git commit is durable | node-local files are ephemeral on experiment termination | CloudLab documentation warns local experiment storage is lost on termination | high | evidence escrow plan before scientific runs | BOUNDED |
| Profile registration | Git repo URL | CloudLab portal profile object | one-time manual registration may be used as shortest path | low | profile page screenshot / identifier | MANUAL PENDING |
| Experiment lifecycle API | GitHub Actions planned | current CloudLab Portal API | official Portal API can instantiate/interact/terminate; legacy XMLRPC API is deprecated | high | exact client revision, auth, endpoints, retry/idempotency semantics still to be frozen | BLOCKED |
| Authentication/secrets | GitHub Actions Secrets planned | CloudLab Portal API auth TBD from current client/account | no credential may enter repo, artifact, raw evidence, or logs | high | credential type + injection/redaction test | BLOCKED |
| Teardown | GitHub orchestration planned | CloudLab terminate operation | exact API command and idempotency semantics must be verified before automation | high | dry-run/controlled smoke test | BLOCKED |
| Evidence | GitHub artifact/off-platform archive planned | live manifest + node/run logs | raw evidence must be hashed and copied off nodes before teardown | medium | bounded first-run evidence receipt | PENDING LIVE |

## First bounded acceptance sequence

1. Compile and source-validate `profile.py` offline in GitHub Actions without importing CloudLab libraries or contacting CloudLab.
2. Verify exactly two `RawPC` declarations, one LAN, the two declared data-plane IPs, and absence of startup services/external-runtime calls.
3. Merge only after the static gate passes.
4. **Manual shortest-path step:** register the public GitHub repository as a CloudLab repository-based profile and record the resulting profile identity.
5. Treat successful portal evaluation/rendering of the repository profile as the first authoritative CloudLab-runtime compatibility test.
6. Instantiate one non-scientific smoke experiment manually if that remains faster than completing API auth discovery.
7. Verify both nodes reach Ready, record the manifest/hardware binding, SSH to each node, and test data-plane ping.
8. Terminate the smoke experiment manually after preserving the small evidence bundle.
9. Only then freeze current Portal API client/auth/lifecycle semantics and add GitHub Actions live orchestration.

## Gate state

`CLWP01_STATIC_PROFILE_CONTRACT=READY_FOR_CI`

`PRE_INTEGRATION_COMPATIBILITY_GATE=BLOCKED_FOR_LIVE_API_AUTOMATION`

Reason: exact current Portal API authentication, client revision, endpoint/command semantics, retry/idempotency, and teardown behavior have not yet been verified against the account. This block does **not** prevent the bounded manual CloudLab profile-registration/smoke-test path after the static profile gate passes.
