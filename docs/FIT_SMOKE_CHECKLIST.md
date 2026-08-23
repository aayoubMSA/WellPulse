# FIT IoT-LAB capability smoke checklist

Run only after account/access approval. No final WP-RT01 evidence is collected during this checklist.

- Record FIT experiment ID, site, node ID/type, and UTC start/end.
- Confirm SSH to the reserved A8 node.
- Record OS/runtime and Python version.
- Confirm writable/persistent path intended for log recovery.
- Confirm free disk space.
- Confirm UTC clock and note synchronization behavior.
- Confirm outbound TLS connection to the chosen MQTT broker.
- Confirm MQTT publish/receive with a non-evidentiary smoke topic.
- Probe `tc qdisc` / `netem` availability without assuming support.
- If unavailable, document deterministic transport-blocking fallback before any final run.
- Copy all smoke logs off the testbed and checksum them.

Passing this checklist authorizes final WP-RT01 scheduling; it does not count as a final run.
