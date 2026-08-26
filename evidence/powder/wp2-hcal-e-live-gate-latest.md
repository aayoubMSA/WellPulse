# WP2 H-Cal E Live Manifest + SSH Gate — latest

- Checked UTC: 2026-08-26T17:19:18Z
- Git SHA: 0b59c0b6d34c14b3701e836a005c14e7c2774e02
- Evidence class: **READ_ONLY INFRASTRUCTURE PRE-SCIENCE GATE**
- Resource mutation: **NONE**
- RF/LTE/MQTT/scientific workload: **NONE**
- Experiment state: **ready**
- SSH both live nodes gate: **FAIL**

## Sanitized experiment state
~~~json
{
  "bindings": {
    "enb_node": "nuc1",
    "ue_node": "nuc2",
    "ue_type": "srsue"
  },
  "created_at": "2026-08-26T17:13:15+00:00",
  "expires_at": "2026-08-26T19:00:00+00:00",
  "id": "9153e16a-1eb1-45f5-88bf-303636a9d1ec",
  "name": "WP-HCAL-E",
  "profile_name": "srslte-controlled-rf",
  "profile_project": "PowderProfiles",
  "project": "WellPulse",
  "started_at": "2026-08-26T17:13:18+00:00",
  "status": "ready"
}
~~~

## Live manifest mapping
~~~json
{
  "endpoints": {
    "enb1": [
      "aayoub",
      "nuc1.emulab.net",
      "22"
    ],
    "rue1": [
      "aayoub",
      "nuc2.emulab.net",
      "22"
    ]
  },
  "physical": {
    "enb1": "urn:publicid:IDN+emulab.net+node+nuc1",
    "rue1": "urn:publicid:IDN+emulab.net+node+nuc2"
  }
}
~~~

## SSH results
~~~json
[
  {
    "host": "nuc1.emulab.net",
    "logical_node": "enb1",
    "port": "22",
    "ssh_rc": 0,
    "stderr_tail": "debug2: channel 0: rcvd eow\ndebug2: channel 0: rcvd close\ndebug2: channel 0: almost dead\ndebug2: channel 0: gc: notify user\ndebug2: channel 0: gc: user detached\ndebug2: channel 0: send close\ndebug2: channel 0: is dead\ndebug2: channel 0: garbage collecting\ndebug1: channel 0: free: client-session, nchannels 1\nTransferred: sent 2432, received 2412 bytes, in 0.4 seconds\nBytes per second: sent 6049.3, received 5999.5\ndebug1: Exit status 0",
    "user": "aayoub"
  }
]
~~~

- Credentials recorded: **NO**
