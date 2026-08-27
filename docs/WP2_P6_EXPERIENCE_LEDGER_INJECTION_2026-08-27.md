# WP2-P6 — Experience-Ledger Injection — 2026-08-27

## Sources reviewed

1. Google Drive `Physical Validation Asset Ledger`:
   - `REMOTE_TESTBEDS`, row `RPT-006` — POWDER;
   - `POWDER_HARDWARE`, especially `PWD-004` — conducted B210 + Intel NUC resources.
2. Google Drive `Research Operating Doctrine — Evidence-First Execution v2.1`.

## Material transferable lessons

### EL-1 — node-local home is not archival storage

POWDER support-confirmed lesson already recorded in `RPT-006`:

- experiment home directories are node-local;
- they may be reloaded immediately after experiment termination;
- raw evidence left only in node-local home can become unrecoverable;
- `/proj` is the persistent experiment-independent storage path.

P6 consequence:

`node raw -> verified /proj escrow -> controller pull -> GitHub artifact -> independent read-back/hash -> teardown`

No teardown may occur from node-side success alone.

### EL-2 — resource catalog is capability evidence, not availability evidence

`POWDER_HARDWARE` records the conducted B210+NUC pool and states that dynamic free/busy availability must be checked at reservation time.

P6 consequence:

- advisory resource preflight is recorded as `PASS|DEFER|UNKNOWN`;
- no hardware/profile/binding substitution is permitted to chase availability;
- authoritative acceptance requires Portal READY plus exact manifest identity for the frozen `nuc1/nuc2` binding, `nuc5300` hardware, image, and profile revision.

### EL-3 — preserve identity and failure evidence

Research Operating Doctrine v2.1 requires preservation of failures, exact evidence identity, hashes, run logs and excluded-run rationale. Missing measurements may not be regenerated or silently repaired after the fact. Automation failures must be handled from the earliest actionable failure, then the required gate is rerun rather than inferred from neighboring passes.

P6 consequence:

- experiment UUID/name/run ID must survive fail-closed workflow paths;
- if protected science has started and evidence closure has not passed, the experiment remains live;
- negative/null scientific outcome is retained and does not authorize a rerun;
- a technical failure is recorded exactly rather than converted into a scientific result.

The P6 workflow was hardened before trigger so `result.env` identity fields are exported to workflow status even when the execution step returns non-zero.

### EL-4 — remote physical evidence has a claim ceiling

A remote physical testbed can strongly support wireless/network/edge claims, but does not establish field/agronomic/physiological validity.

P6/P7 consequence:

- Golden is a non-scored measurement-system qualification rehearsal;
- later POWDER scored evidence supports conducted-RF communications/resilience claims only;
- FIT/POWDER evidence must not be relabeled as Siwa field validation.

## Injected P6 invariant

`EVIDENCE_SURVIVAL_BEFORE_TEARDOWN > EXPERIMENT_CLEANUP_CONVENIENCE`

If evidence and cleanup goals conflict after protected science begins, preserve the live experiment and recover evidence first.

## Verdict

`P6_EXPERIENCE_LEDGER_INJECTION=PASS`

No scientific parameter, comparator, RF state, horizon, endpoint, or scored authorization was changed by this review.
