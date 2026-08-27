# Independent P7B Preflight Scope Guard

This patch is intentionally offline-only. No workflow, trigger, POWDER API call, SSH session, reservation action, RF command, scientific cell, or teardown is authorized during implementation/QA.

The only deliverables are an orthogonal probe script, its contract, and offline regression tests. Live execution requires a separate explicit authorization after QA closure.
