# K1-P2 — Authoritative Portal API Pin Closure — 2026-08-27

## Verdict

`K1P2=PASS`

`PORTAL_API_PIN_GATE=PASS`

`K1=PASS`

`POWDER_CONTACT=NO`

`DRIVE_CONTACT=NO`

`SCIENTIFIC_RUN=NO`

## Authoritative capture

The official Emulab/POWDER Portal API repository was resolved from a user-accessible shell directly against:

`https://gitlab.flux.utah.edu/emulab/portal-api.git`

Frozen authoritative revision:

`01be03b2f60c067815a7654437320dd981ca3617`

A source archive was generated from that exact checked-out revision during the capture step.

- archive: `portal-api-01be03b2f60c067815a7654437320dd981ca3617.tar`
- SHA-256: `3e9f0073b2df6840801baa38333f1f04debd02a2eaa57997939b6f7ee678d4c8`
- bytes: `1003520`

The capture script explicitly reported:

- `POWDER_CONTACT=NO`
- `RESERVATION_CREATED=NO`
- `SCIENTIFIC_RUN=NO`

## Runtime integration contract

Created:

`scripts/wp2_portal_client_bootstrap.sh`

Implementation commit:

`4a88d439b4084f0f0155a94166304150018e2fac`

The bootstrap:

1. references only the authoritative repository;
2. fetches the exact 40-character immutable revision;
3. checks out detached `FETCH_HEAD`;
4. verifies `git rev-parse HEAD` equals the frozen revision exactly;
5. fails closed on any mismatch;
6. installs the CLI only after revision verification;
7. records the capture archive hash/size as provenance constants.

This removes moving-HEAD authority from the future integration contract.

## Static fail-close enforcement

Updated:

`.github/workflows/wp2-preintegration-static.yml`

Implementation commit:

`76aa56c202d66b12ec7bf9239b2177c2007da73e`

The static gate now requires the exact Portal repository, revision, capture archive hash, revision fetch, and checked-out SHA equality check. It rejects a mutable `git clone ... portal-api.git` pattern in the accepted future bootstrap.

Offline CI trigger commit:

`479459d801e4b08e438eb1aa793a5c747121fe3b`

GitHub Actions validation:

- workflow: `WP2 Pre-Integration Static Acceptance`
- run ID: `33081196297`
- event: `push`
- status: `completed`
- conclusion: `success`
- created: `2026-08-27T14:15:08Z`
- updated: `2026-08-27T14:15:20Z`

No POWDER or Drive contact is performed by that workflow.

## Workstation independence

The authoritative revision capture was a one-time bootstrap only. Normal future experiment control must not depend on the home PC or work PC. The frozen revision and acceptance contract now live in the canonical WellPulse repository and are therefore available to GitHub Actions independent of the operator workstation.

## K1 consequence

The only remaining K1 blocker was the unresolved immutable Portal API revision. It is now resolved and statically enforced.

Therefore:

`K1=PASS`

This does **not** imply the complete compatibility gate passes. Portal lifecycle/error semantics, Drive OAuth/transport, receiver detach proof, reservation-expiry semantics, `/proj/WellPulse` live validation, and observation semantics remain later K-series work.

Scientific weighted completion remains `20%`.

`scored_runs_authorized=false`

`REBOOK_GOLDEN=false`
