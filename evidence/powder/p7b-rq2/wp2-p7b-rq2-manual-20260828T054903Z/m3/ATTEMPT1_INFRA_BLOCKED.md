# M3 attempt 1 — infrastructure block before Q0

- GitHub Actions run: `33146108383`
- Job: `98767406896`
- Manual precheck run ID: `wp2-p7b-rq2-manual-20260828T054903Z`
- Result: `BLOCKED_BEFORE_Q0`
- First cause: `RuntimeError:EVIDENCE_ROOT_ALREADY_EXISTS`
- RF mutation: `NO`
- LTE/service mutation: `NO`
- Scientific cell execution: `NO`
- B1/W1/B2: `NOT_STARTED`
- Teardown: `NO`
- Automatic scientific retry: `NOT_APPLICABLE`

The pre-science gate intentionally created an evidence root containing `PRE_SCIENCE_IDENTITY.txt`; the frozen RQ2 adapter requires the M3 evidence root to not exist before `prepare_session()`. The attempt stopped at that guard before Q0 attenuation or service restore. The precheck evidence root is retained and not deleted.
