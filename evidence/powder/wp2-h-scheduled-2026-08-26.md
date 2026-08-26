# WP2-H Scheduled POWDER Experiment — 2026-08-26

Evidence class: **NON-SCORED INFRASTRUCTURE SCHEDULING ONLY**

Manual POWDER Portal scheduling was completed and visually verified before resource start.

- Experiment name: `WP-HCAL-A`
- State at capture: `scheduled`
- Project: `WellPulse`
- Profile: `srslte-controlled-rf`
- Profile project: `PowderProfiles`
- RefSpec: `refs/heads/master`
- Profile revision shown by Portal: `a6da9656` (matches frozen revision prefix `a6da96560b6526dc6816761282722c996418fd8c`)
- Scheduled start: `2026-08-26 14:00 Africa/Cairo`
- Scheduled expiry: `2026-08-26 16:00 Africa/Cairo`
- Manual reservation: `nuc1 x1 + nuc2 x1`, Emulab, approved for 14:00–16:00 Africa/Cairo
- Parameterized UE type: `srsLTE UE (B210)`
- Requested eNodeB Node ID: `nuc1`
- Requested UE Node ID: `nuc2`
- Nexus/ADB path selected: **NO**
- Scientific workload executed at capture: **NO**
- RF manipulation executed at capture: **NO**
- Scored run interaction: **NO**

The existing fallback reservation for `nuc1+nuc2` at 19:00–22:00 Africa/Cairo remains untouched.

Important: requested bindings are not accepted as live physical bindings until the experiment leaves `scheduled`, provisions successfully, and the live Binding/manifest view is verified. No future run may infer bindings from this scheduling request alone.
