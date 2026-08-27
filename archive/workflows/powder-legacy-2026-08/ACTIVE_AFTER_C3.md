# Active workflow set after Cleanup Patch C3

The active `.github/workflows/` set is intentionally restricted to non-POWDER execution paths:

- `local-gate-once.yml`
- `local-unit-tests.yml`
- `wp2-b2-semantics.yml` — local broker semantics only; POWDER interaction NONE
- `wp2-golden-offline-qa.yml` — offline Golden QA only
- `wp2-h-preflight.yml` — local preflight only; POWDER resource interaction NONE
- `wp2-preintegration-static.yml` — static pre-integration checks only

Any future live POWDER workflow must be introduced only after the current compatibility and HCI/raw-evidence gates pass and must be purpose-specific, reviewed, and free of unqualified independent probes.
