# POWDER generic NUC5300 early-window search

- Checked UTC: 2026-08-26T09:52:35Z
- WellPulse SHA: 2bfaf4b91911a63f7282abb57118f986243a23b7
- Request: `nuc5300 x2`, Emulab, project `WellPulse`
- Resource mutation attempted: **NONE**
- Existing 19:00–22:00 fallback reservation modified: **NO**

## 3-hour result

- Exit: `150`

```json
null
```

```text
{
    "code": 406,
    "error": "Prediction Info is stale: 2026-08-25 14:38:48\n/usr/testbed/bin/manage_reservations -t 0ad774cdae778d1d1cb3eacce6fa00c29098eea5   prediction -a 'urn:publicid:IDN+emulab.net+authority+cm' WellPulse/WellPulse\nNo fit, could not find a start time\n$VAR1 = {\n          'type' => 'nuc5300',\n          'uuid' => '14f62568-a9f1-4f84-bebf-14ab8ef8c479',\n          'cluster' => 'urn:publicid:IDN+emulab.net+authority+cm',\n          'count' => 2\n        };\n*** manage_resgroup:\n    Could not fit this reservation request into the schedule: could not fit 2 nuc5300 at the Emulab cluster\n",
    "errors": null
}


```

## 2-hour result

- Exit: `150`

```json
null
```

```text
{
    "code": 406,
    "error": "Prediction Info is stale: 2026-08-25 14:38:48\n/usr/testbed/bin/manage_reservations -t 68b9c377c243eb993bf06c4354aff6393347218d   prediction -a 'urn:publicid:IDN+emulab.net+authority+cm' WellPulse/WellPulse\nNo fit, could not find a start time\n$VAR1 = {\n          'type' => 'nuc5300',\n          'count' => 2,\n          'uuid' => 'f5cb50b5-1065-42e7-a6d5-ce3d42d9c0e1',\n          'cluster' => 'urn:publicid:IDN+emulab.net+authority+cm'\n        };\n*** manage_resgroup:\n    Could not fit this reservation request into the schedule: could not fit 2 nuc5300 at the Emulab cluster\n",
    "errors": null
}


```

## 1-hour result

- Exit: `150`

```json
null
```

```text
{
    "code": 406,
    "error": "Prediction Info is stale: 2026-08-25 14:38:48\n/usr/testbed/bin/manage_reservations -t ae8a50e4aa92b2440fd5d4aa3d4cef362bb345a1   prediction -a 'urn:publicid:IDN+emulab.net+authority+cm' WellPulse/WellPulse\nNo fit, could not find a start time\n$VAR1 = {\n          'uuid' => '312c2b4f-4411-4c0f-878b-c97f14df88ff',\n          'cluster' => 'urn:publicid:IDN+emulab.net+authority+cm',\n          'type' => 'nuc5300',\n          'count' => 2\n        };\n*** manage_resgroup:\n    Could not fit this reservation request into the schedule: could not fit 2 nuc5300 at the Emulab cluster\n",
    "errors": null
}


```

- Token content recorded: **NO**
