# WellPulse Sprint Handover — RF Approval Readiness

Date: 2026-08-23
Sprint status: COMPLETE

## Sprint objective
Use the account-approval waiting window to make WellPulse executable on the first approved real-RF platform without opening additional testbed-registration queues.

## Entering state
- WP-RT01 FIT: publication-class validation complete.
- ARA: access approval pending.
- POWDER: account/project approval pending.
- COSMOS/ORBIT: group activation email received for `msa-university`, PI username `aayoub`; activation/approval/login not yet proven.
- Decision: do not register NITOS/AERPAW now; parallelize access, not redundant experiments.

## Sprint outputs
Created a platform-agnostic RF capability-smoke package:

1. `experiments/RF_COMMON/RF_CAPABILITY_SMOKE_v1.0.md`
   - frozen R0/R1/R2 capability sequence;
   - smoke evidence class `CAPABILITY_SMOKE_RF`;
   - synchronized application/RF evidence requirements;
   - explicit GO/PIVOT/KILL rules;
   - final-matrix freeze gate;
   - prohibition on using application-layer blocking as RF evidence.

2. `experiments/RF_COMMON/rf_event_schema.json`
   - common machine-readable event structure for RF state, RF metrics, application events, reconnect, and backlog drain;
   - supports POWDER, COSMOS/ORBIT, ARA;
   - UTC plus monotonic-time alignment.

3. `experiments/RF_COMMON/PLATFORM_ADAPTERS.md`
   - thin platform adapter boundary;
   - POWDER target: `srs-rf-matrix`;
   - COSMOS/ORBIT target: `sb4` RF Attenuator Matrix;
   - ARA target: field COTS UE / RAN path with timestamped radio state;
   - WellPulse workload/reconciliation logic remains platform-neutral.

Relevant commits:
- RF smoke contract: `3fac17ae3ab656ae80e8e8514b8e48d0c5f10266`
- RF event schema: `6a045ee268822815617b0893d4b63bd51a49cf9b`
- adapter contract: `ac7983de651b72b8aa7afe321f2035220690bbc2`

## Reuse baseline
Existing WP-RT01 components remain the implementation baseline rather than being rewritten:
- `scripts/wp_rt01_a8_runner.py`
- `scripts/wp_rt01_receiver.py`
- `scripts/analyze_fit_rt01.py`
- existing FIT evidence/reconciliation scripts

The next implementation step, once one platform is accessible, is a thin adapter around these semantics—not a new WellPulse architecture.

## Frozen decision rule
Whichever of POWDER or COSMOS/ORBIT clears access first gets the controlled-RF capability smoke. ARA remains the rural-OTA lane. Do not execute redundant final matrices merely because multiple platforms become accessible.

## Exact next action
1. Complete COSMOS/ORBIT activation/approval/login gate.
2. Continue waiting for POWDER and ARA approvals.
3. On first usable controlled-RF platform, implement only its thin adapter and run the bounded R0/R1/R2 capability smoke.
4. Decide GO/PIVOT/KILL before freezing any publication-final RF experiment.
5. No hardware reservation or paid action until explicitly authorized.

## Evidence boundary
This sprint creates experiment readiness only. It adds no new publication result and must not be cited as experimental evidence.

## Handover cadence rule adopted
Atomic actions belong in GitHub issues, run logs, commits, and evidence registers. Sprint handovers are written only at meaningful boundaries such as access-gate resolution, capability-smoke completion, protocol/claim freeze, material experiment completion/failure, pivot/kill, or agent transfer. The canonical project handover should roll up sprint outcomes rather than narrating every operational action.
