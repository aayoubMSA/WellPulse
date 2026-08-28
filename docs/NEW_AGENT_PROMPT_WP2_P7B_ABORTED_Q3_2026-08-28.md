# New Agent Prompt — WellPulse WP2 P7B after aborted Q3 attempt

Take ownership of the WellPulse WP2 execution lane from the canonical private repository `aayoubMSA/WellPulse`, branch `main`.

Do **not** reconstruct current state from conversation memory.

First read, completely:

1. `docs/WP2_P7B_MANUAL_ABORT_HANDOVER_2026-08-28.md`
2. `HANDOVER_CURRENT.md`

Then follow the complete mandatory read order in the new live handover document before taking action.

Resume exactly at:

**`WP2-P7B-H1 — ABORTED-Q3 EVIDENCE FREEZE + OFFLINE ROOT-CAUSE HANDOVER`**

Critical frozen state:

- latest authoritative run ID: `wp2-p7b-manual-20260828T024433Z`;
- current/last reservation: `wp7brq2609012`, UUID `f6de95cb-a13a-421e-bd0e-766dfc1d3fb3`;
- CORE = `nuc1`; UE = `nuc2`;
- Q0 path had passed before the scientific attempt;
- B1 entered Q3 scientific impairment;
- `Q3_STARTED=YES`;
- `attenuator_q3_set.txt=EXISTS`;
- `t_rf_restore.txt=EXISTS`;
- `restart_proof.json=MISSING`;
- completed cells = none;
- B1 scientific verdict = NULL / aborted after Q3;
- W1 and B2 were not started;
- automatic retry is prohibited;
- manual B1 retry is prohibited under the current frozen contract;
- scored execution remains prohibited.

Raw evidence root to preserve first, if still accessible:

`/proj/WellPulse/evidence/p7b-live-wp2-p7b-manual-20260828T024433Z`

Latest abrupt-exit RCA:

`/proj/WellPulse/evidence/p7b-live-wp2-p7b-manual-20260828T024433Z/abrupt-exit-rca`

Do not contact POWDER, alter RF, restart services, rerun B1, run W1/B2, create a reservation, or teardown anything until you first report the retrieved canonical state and the exact finite H1 patches you will own.

The first live-capable action, if later explicitly authorized, must prioritize evidence freeze/pull before any other mutation.

Manual-operation constraint: every command block must explicitly say **`nuc1 / CORE`** or **`nuc2 / UE`**. Do not add diagnostic `sleep`/wait delays to human-operated scripts; preserve only the scientific timing already frozen inside the authoritative runner.

H1 terminal verdict must be exactly one of:

`WP2_P7B_H1=PASS_ABORT_EVIDENCE_FROZEN_ROOT_CAUSE_CLASSIFIED`

or

`WP2_P7B_H1=BLOCKED:<first_named_reason>`

Then STOP.