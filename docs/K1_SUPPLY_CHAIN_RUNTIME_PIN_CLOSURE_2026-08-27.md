# K1 — Offline Supply-Chain / Runtime Pin Closure — 2026-08-27

## Verdict

`K1=BLOCKED_PORTAL_API_REVISION`

`POWDER_CONTACT=NO`

`SCIENTIFIC_RUN=NO`

`PRE_INTEGRATION_COMPATIBILITY_GATE=BLOCKED`

`REBOOK_GOLDEN=false`

K1 closed every supply-chain/runtime item that can be resolved reproducibly from the current repository and authoritative public release metadata without contacting POWDER. One material blocker remains: the exact immutable upstream revision of the supported Emulab/POWDER Portal API client cannot yet be established from an authoritative accessible source, so K1 must fail closed rather than pin an invented or mutable revision.

## Closed items

### 1. GitHub checkout action used by the pre-integration path

Pinned to immutable commit:

`actions/checkout@11d5960a326750d5838078e36cf38b85af677262`

The active pre-integration workflow uses explicit runner label `ubuntu-24.04`, not `ubuntu-latest`.

### 2. uv bootstrap

The previous runtime bootstrap fetched and executed the mutable installer:

`https://astral.sh/uv/install.sh`

That path is no longer used by `scripts/wp2_a3_runtime_bootstrap.sh`.

The bootstrap is now pinned to:

- uv version: `0.12.1`
- asset: `uv-x86_64-unknown-linux-gnu.tar.gz`
- SHA-256: `90b2f223fb69d19db49e117da601f64978593417988530aa733d456141b4bcbb`
- upstream release target commit recorded from the immutable GitHub release: `329541a503de8a4d9bb021814f9c0875efe033c8`

The archive SHA-256 is verified before extraction/install, the exact runtime version is checked after install, and the archive hash is written to the runtime fingerprint.

Implementation commit:

`353be59fa222150fbedf731ae45bbac9026ba543`

### 3. rclone bootstrap

The existing bootstrap already satisfied the exact-version/checksum contract:

- rclone version: `1.75.0`
- Linux amd64 ZIP SHA-256: `aa2804e08f48250e71009c727124b6341cd0288465804a9a09d14663cabafbaa`
- moving `rclone-current-linux-amd64.zip` path prohibited
- SHA-256 verified before extraction/install
- exact installed version checked after install

No weaker moving reference was introduced.

### 4. Static fail-close enforcement

`.github/workflows/wp2-preintegration-static.yml` now checks that:

- uv is exactly `0.12.1`;
- the exact uv archive SHA-256 is present;
- the mutable `astral.sh/uv/install.sh` reference is absent;
- rclone remains exactly `1.75.0` with the frozen checksum;
- the integration checkout action is the immutable SHA;
- `ubuntu-latest` is not used by this pre-integration path;
- the archived Attempt-6 status workflow is checked at its actual archived path;
- existing receiver-launch, TLS-diagnostic, rclone-runtime and prelaunch-time fail-close checks remain active.

Implementation commit:

`421eb314b7210c646dfc19405b2fd6a867a5bfd6`

## Remaining material blocker

### Portal API client immutable revision

Authoritative POWDER/Emulab documentation identifies the supported current client repository as:

`https://gitlab.flux.utah.edu/emulab/portal-api`

and explicitly states that the Portal API is under active development. Therefore cloning or installing repository HEAD is not acceptable for a reproducibility-critical Golden path.

During this K1 patch, the environment could verify the authoritative repository identity and active-development warning, but could not resolve an authoritative immutable Git commit for the client. Direct GitLab repository access was not available through the current execution path, and no canonical WellPulse artifact contains a previously frozen Portal API revision.

Accordingly:

`PORTAL_API_REVISION=UNRESOLVED`

No placeholder SHA, guessed commit, tag-as-commit substitute, or mutable branch name is accepted.

## Scope boundary

K1 does **not** close:

- Google Drive dedicated OAuth and transport verification;
- Portal lifecycle/status/error semantics;
- receiver live detach proof;
- live reservation budget validation;
- `/proj/WellPulse` live write/read/hash validation;
- live observation semantics proof;
- the full C1–C14 compatibility gate.

These remain later K patches or live-only gates.

## Scientific consequence

None. K1 is infrastructure/reproducibility hardening only.

Scientific weighted completion remains `20%`.

`scored_runs_authorized=false`

`REBOOK_GOLDEN=false`

## Exact next patch

Because K1 is blocked, do **not** advance to K2 yet.

Next bounded patch:

`K1-P — Resolve and freeze the exact Portal API upstream revision from an authoritative source, then re-run K1 static acceptance.`

If an authoritative immutable revision cannot be established, the future Golden automation must use a different fully versioned Portal interaction path or remain blocked.
