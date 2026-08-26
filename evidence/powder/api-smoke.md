# POWDER Portal API smoke — current reservation state

- Checked UTC: 2026-08-26T09:48:40Z
- WellPulse SHA: 0194208c19d21325ea82c9883aeb1ca2ebfd1f53
- Authentication gate: **PASS**
- Resource mutation attempted: **NONE**
- Visible WellPulse experiments: **0**
- Visible WellPulse reservation groups: **1**
- Token content recorded: **NO**

## WellPulse reservation groups — sanitized

```json
[
  {
    "creator": "aayoub",
    "expires_at": "2026-08-26T19:00:00+00:00",
    "group": "WellPulse",
    "id": "a921c17b-08fb-47dc-a7cf-d8033c35f8a2",
    "nodetypes": {
      "nodetypes": [
        {
          "approved_at": "2026-08-25T19:10:06+00:00",
          "canceled_at": null,
          "count": 1,
          "deleted_at": null,
          "error": null,
          "errorCode": null,
          "nodetype": "nuc1",
          "reservation_id": "947f7470-a0b8-11f1-90d9-e4434b2381fc",
          "resgroup_id": "a921c17b-08fb-47dc-a7cf-d8033c35f8a2",
          "urn": "urn:publicid:IDN+emulab.net+authority+cm"
        },
        {
          "approved_at": "2026-08-25T19:10:06+00:00",
          "canceled_at": null,
          "count": 1,
          "deleted_at": null,
          "error": null,
          "errorCode": null,
          "nodetype": "nuc2",
          "reservation_id": "91e76f90-a0b8-11f1-90d9-e4434b2381fc",
          "resgroup_id": "a921c17b-08fb-47dc-a7cf-d8033c35f8a2",
          "urn": "urn:publicid:IDN+emulab.net+authority+cm"
        }
      ]
    },
    "powder_zones": null,
    "project": "WellPulse",
    "ranges": null,
    "reason": "Continuation of an approved WellPulse controlled-RF qualification experiment using the srslte-controlled-rf profile. The previous session successfully validated EPC/eNodeB startup and B210 operation; this reservation is required to complete the non-scored UE attach and LTE user-plane qualification.",
    "routes": null,
    "start_at": "2026-08-26T16:00:00+00:00"
  }
]
```

## Experiment scheduling options

```text
│ *  --name                   TEXT                    A human readable name    │
│ *  --project                TEXT                    The project the          │
│ *  --profile-name           TEXT                    The name of the profile. │
│ *  --profile-project        TEXT                    The name of the profile  │
│                                                     project                  │
│    --group                  STR                     The project subgroup the │
│    --start-at               [%Y-%m-%dT%H:%M:%S%z|%  Schedule experiment to   │
│                             Y-%m-%dT%H:%M:%S.%f%z|  start at a future time   │
│    --stop-at                [%Y-%m-%dT%H:%M:%S%z|%  Schedule experiment to   │
│                             Y-%m-%dT%H:%M:%S.%f%z|  stop at a future time    │
│    --duration               INT                     Initial experiment       │
│                                                     duration in hours        │
│    --paramset-name          STR                     Optional name of a       │
│                                                     to the profile           │
│    --bindings               ANYOBJECT               [default: Unset]         │
│                                                     profile, optionally      │
```

## Resgroup CLI

```text
                                                                                
 Usage: portal-cli resgroup [OPTIONS] COMMAND [ARGS]...                         
                                                                                
╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                  │
╰──────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────╮
│ create        A cloudlab reservation group                                   │
│ create_raw    Create a new reservation group                                 │
│ delete        Delete a reservation group                                     │
│ get           Retrieve a specific reservation group                          │
│ list          Get reservation group list                                     │
│ modify        A cloudlab reservation group                                   │
│ modify_raw    Modify a reservation group                                     │
│ search        A cloudlab reservation group search request                    │
│ search_raw    Search for a free time slot where a resgroup can be scheduled  │
│ reservation                                                                  │
╰──────────────────────────────────────────────────────────────────────────────╯

```
