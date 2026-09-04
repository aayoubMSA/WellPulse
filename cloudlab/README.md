# CloudLab — CL-WP-01

Purpose: turn CloudLab into a reusable **real bare-metal systems validation asset** for WellPulse and later edge/distributed-system studies.

## Revision 1 scope

`profile.py` at the repository root defines the smallest useful physical topology:

- `edge` — one bare-metal node;
- `cloud` — one bare-metal node;
- `lan` — one isolated experiment LAN;
- data-plane addresses: `10.10.0.1/24` and `10.10.0.2/24`.

There are intentionally **no startup services or experiment scripts** in the first live allocation. This keeps the first CloudLab use a bounded infrastructure smoke test and avoids discovering automation-side effects during a scarce physical allocation.

## Why `profile.py` is at repository root

CloudLab repository-based profiles require a public HTTP(S) git repository with a top-level `profile.py`. When instantiated, CloudLab clones the repository to `/local/repository` on each experiment node. This makes the Git commit the profile source of truth while allowing later experiment scripts to live under `cloudlab/`.

## Static gate

GitHub Actions runs only a **dependency-free offline source-contract check** in this revision:

1. compile the Python source without importing CloudLab libraries;
2. validate exactly two `RawPC` declarations, one LAN, and the two declared IPs;
3. reject startup services or external-runtime/network imports;
4. freeze the profile, validator hashes, and runner fingerprint as a GitHub artifact.

The CloudLab portal remains authoritative for evaluating the repository profile with its supported geni-lib runtime and producing the actual request topology/RSpec. The workflow does **not** contact CloudLab, allocate hardware, expose credentials, or terminate resources.

## Shortest next manual step after merge

In CloudLab:

1. create a new **repository-based profile**;
2. provide `https://github.com/aayoubMSA/WellPulse` as the repository URL;
3. confirm CloudLab successfully evaluates `profile.py` and renders two raw PCs joined by one LAN;
4. record the CloudLab profile identity before instantiation.

If a one-time manual smoke allocation is faster than completing Portal API authentication setup, use it. Manual intervention is preferred whenever it reduces total path length without weakening evidence or safety controls.

## Target first smoke experiment

Name: `clwp01`

Acceptance evidence:

- experiment reaches **Ready**;
- manifest identifies two physical nodes;
- SSH succeeds to both;
- `edge` can ping `10.10.0.2` over the experiment data plane;
- `cloud` can ping `10.10.0.1`;
- profile commit SHA and live manifest are preserved off the nodes;
- experiment is terminated only after evidence read-back.

This first allocation is **not** a scored scientific run. Controlled outage/buffering/recovery automation follows only after the GitHub ↔ CloudLab live API compatibility gate passes.

See `cloudlab/COMPATIBILITY_MATRIX.md`.
