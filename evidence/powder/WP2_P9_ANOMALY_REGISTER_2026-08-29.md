# WP2-P9 Anomaly Register — 2026-08-29

No anomaly has been deleted, normalized away, or reinterpreted as a positive result.

| ID | Scope | Classification | Raw observation | Control |
|---|---|---|---|---|
| A-001 | E5 | MISSING_FROZEN_ARTIFACT | Forward UE recovery-ping was observed live but not frozen. | Do not reconstruct or quote forward recovery-ping metrics; CORE reverse recovery evidence may be used with caveat. |
| A-002 | E8 | DUPLICATE_SEND_ATTEMPT | Recovery sequence 41–60 was sent twice; sent.log has 80 lines but 60 unique IDs. | Use unique IDs for completeness; preserve 80-line diagnostic fact. |
| A-003 | E10-A | CENSORED_NO_RECOVERY | No ping recovery in 100 attempts and no MQTT recovery in 100 attempts inside the recorded window. | No exact recovery latency exists. |
| A-004 | E10-C | INVALID_ATTEMPT_A | Attempt A is incomplete/mislocated setup evidence; suffix B is the valid run. | A is SETUP_ARTIFACT; do not combine A and B. |
| A-005 | E10-D | UPPER_BOUND_TIMING | Broker-start `ACTION_BEGIN` to first manually initiated successful MQTT probe = 10.908749 s; `BROKER_START_COMMAND_COMPLETE` to the same probe = 10.872618 s. | Both are upper bounds dominated by manual probe timing; never report either as exact broker recovery latency. |
| A-006 | Departure | DOCUMENTED_POST_MANIFEST_APPEND | CAPTURE_STATUS.txt received a completion append after manifest generation on both nodes. | Expected exception; not corruption; all other files verified. |
| A-007 | Platform | RUNTIME_UHD_NOT_EXPOSED | Runtime UHD probes did not independently expose a USRP device. | Do not claim runtime B210 serial/firmware identity. |
| A-008 | RF path | UNRESOLVED_ATTENUATOR_MAPPING | Individual attenuator ID→physical-path mapping is not conclusively established. | Never infer missing mapping. |
| A-009 | E1 initial | PREREQUISITE_VIOLATION | 0 dB forward ping and MQTT prerequisite already failed, yet attenuation treatment sweep proceeded. | Run classified NULL. |
| A-010 | E1R4 | SENDER_RECEIVER_EVENT_DISAGREEMENT | Sequence 96 exists in sender log and is absent at receiver but has no matching MQTT_FAIL event. | Receiver reconciliation governs completeness; retain disagreement. |
| A-011 | E3 | SENDER_RECEIVER_EVENT_DISAGREEMENT | Sequence 150 exists in sender log and is absent at receiver but has no matching MQTT_FAIL event. | Receiver reconciliation governs completeness; retain disagreement. |
| A-012 | E10-C-B | DUPLICATE_CORE_VERIFICATION_LINE | Later CORE end-to-end verification record is duplicated. | Treat as duplicate evidence; primary timing remains publish-side. |
| A-013 | E11 | ONE_SIDED_COLLECTOR | R1-R3 collector contains nuc2/UE evidence only and no independent nuc1/CORE archive. | Limit E11 use to UE-side recovery/IP-transition replication. |
| A-014 | E7 | RTT_OUTLIER_PRESERVED | CORE reverse baseline includes a 481.046 ms maximum RTT. | Preserve as observed; do not clean or discard. |
| A-015 | Final documentation | PRIVATE_CREDENTIAL_BEARING_CAPTURE | Final profile/RSpec documentation contains credential-bearing/encrypted portal material. | Keep private or sanitize before sharing; no publication packaging in P9. |
| A-016 | Screenshots | UNCLASSIFIED_CONTEXT_EVIDENCE | 89 PNG screenshots are preserved in the private golden package with opaque UUID filenames and no defensible run mapping. | Enumerate/hash and retain; do not use for metric reconstruction or invent attribution. |
| A-017 | E5 pre-manual | PRE_SCIENCE_SETUP_ARTIFACT | `p8-e5-20260829-000402` failed at preflight with a PowerShell `System.Char.Trim` error; `p8-e5-20260829-000744` failed its MQTT gate (`53/5`). | Both remain SETUP_ARTIFACT; no treatment result is derived. |
| A-018 | Master P8 + E10/E11 archive-native manifests | DOCUMENTED_POST_MANIFEST_SELF_LOG_APPEND | Independent P9 re-audit found the stored hash for master `meta/collection.log` matches exactly the first 5611 bytes, after which the collector appended its final `creating final ZIP` line; E10/E11 `meta/collector.log` likewise matches its stored hash through byte 8570, followed only by its final `creating final ZIP` line. Outer frozen ZIP SHA256 values still match Drive exactly. | Treat the two self-logging collector files as deterministic post-manifest append exceptions, not corruption. Do not use either collector log for numeric reconstruction. All other parsed entries in the archive-native manifests verified with no mismatch. |

`P9_E_ANOMALY_REGISTER=PASS`
