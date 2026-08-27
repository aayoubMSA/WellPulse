# K1 — Offline Supply-Chain / Runtime Pin Closure — 2026-08-27

## Verdict

`K1=PASS`

`POWDER_CONTACT=NO`

`SCIENTIFIC_RUN=NO`

`PRE_INTEGRATION_COMPATIBILITY_GATE=BLOCKED`

`REBOOK_GOLDEN=false`

K1 has now closed the supply-chain/runtime pinning items required before later compatibility patches. The final blocker, the immutable revision of the supported Emulab/POWDER Portal API client, was resolved through K1-P2 and is now frozen and statically enforced.

## Closed items

### 1. GitHub checkout action used by the pre-integration path

Pinned to immutable commit:

`actions/checkout@11d5960a326750d5838078e36cf38b85af677262`

The active pre-integration workflow uses explicit runner label `ubuntu-24.04`, not `ubuntu-latest`.

### 2. uv bootstrap

Pinned to:

- uv version: `0.12.1`
- asset: `uv-x86_64-unknown-linux-gnu.tar.gz`
- SHA-256: `90b2f223fb69d19db49e117da601f64978593417988530aa733d456141b4bcbb`
- upstream release target commit: `329541a503de8a4d9bb021814f9c0875efe033c8`

The mutable `https://astral.sh/uv/install.sh` path is prohibited in the accepted runtime bootstrap. The archive is hash-verified before extraction/install and the exact runtime version is checked afterward.

Implementation commit:

`353be59fa222150fbedf731ae45bbac9026ba543`

### 3. rclone bootstrap

Frozen contract:

- rclone version: `1.75.0`
- Linux amd64 ZIP SHA-256: `aa2804e08f48250e71009c727124b6341cd0288465804a9a09d14663cabafbaa`
- moving `rclone-current-linux-amd64.zip` path prohibited
- SHA-256 verified before extraction/install
- exact installed version checked after install

### 4. Portal API client

Authoritative repository:

`https://gitlab.flux.utah.edu/emulab/portal-api.git`

Frozen authoritative revision:

`01be03b2f60c067815a7654437320dd981ca3617`

Capture archive provenance:

- archive: `portal-api-01be03b2f60c067815a7654437320dd981ca3617.tar`
- SHA-256: `3e9f0073b2df6840801baa38333f1f04debd02a2eaa57997939b6f7ee678d4c8`
- bytes: `1003520`

Canonical K1-P2 record:

`docs/K1P2_PORTAL_API_PIN_CLOSURE_2026-08-27.md`

Accepted future bootstrap:

`scripts/wp2_portal_client_bootstrap.sh`

Implementation commit:

`4a88d439b4084f0f0155a94166304150018e2fac`

The bootstrap fetches the exact revision, checks out detached state, verifies `git rev-parse HEAD` equals the frozen SHA, and fails closed before installing the CLI if any mismatch occurs.

### 5. Static fail-close enforcement

`.github/workflows/wp2-preintegration-static.yml` checks:

- exact uv version/archive/hash and absence of mutable installer;
- exact rclone version/hash and absence of moving download;
- immutable checkout action and explicit `ubuntu-24.04` runner;
- exact Portal API repository/revision/capture hash and checked-out-SHA equality contract;
- existing receiver-launch, TLS-diagnostic, rclone-runtime and prelaunch-time fail-close checks.

Portal-pin static implementation commit:

`76aa56c202d66b12ec7bf9239b2177c2007da73e`

Offline validation trigger commit:

`479459d801e4b08e438eb1aa793a5c747121fe3b`

Validation workflow run:

- `WP2 Pre-Integration Static Acceptance`
- run ID `33081196297`
- conclusion `success`

## Workstation-independence rule

Home and work PCs are operator terminals only. No future Golden/scored execution may depend on workstation-local history, downloads, tokens, or unique filesystem state. Canonical execution authority remains GitHub + frozen repository state + GitHub Actions/secrets.

## Scope boundary

K1 does **not** close:

- Google Drive dedicated OAuth and transport verification;
- Portal lifecycle/status/error semantics;
- receiver live detach proof;
- authoritative live reservation budget validation;
- `/proj/WellPulse` live write/read/hash validation;
- live observation semantics proof;
- the full C1–C14 compatibility gate.

These remain later K-series patches or live-only gates.

## Scientific consequence

None. K1 is infrastructure/reproducibility hardening only.

Scientific weighted completion remains `20%`.

`scored_runs_authorized=false`

`REBOOK_GOLDEN=false`

## Exact next patch

`K2 — Auth / Drive transport contract closure`

K2 must be executed as a separate bounded patch under the project patch discipline.
