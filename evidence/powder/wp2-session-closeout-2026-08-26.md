# WP2 POWDER session closeout — 2026-08-26

Experiment: `WP-HCAL-E`
Experiment UUID: `9153e16a-1eb1-45f5-88bf-303636a9d1ec`
Profile: `PowderProfiles/srslte-controlled-rf`
Profile revision: `a6da96560b6526dc6816761282722c996418fd8c`
Nodes: `enb1 -> nuc1`, `rue1 -> nuc2`
H1 run ID: `wp2h1-a1-20260826-001`

## Frozen scientific state

- H1 Trial #1 classification: `VALID_W1_RECOVERY_FAILURE`.
- H remains **UNFROZEN**.
- No replacement H-calibration trials are authorized under the frozen rule.
- Scored B1/W1/B2 runs remain unauthorized.
- The H1 failure is preserved as a real recovery failure, not reclassified as technically invalid.

## Recovery characterization

The observed long-outage failure was localized below the WellPulse application layer. UE-only restart failed; EPC/eNB reset while leaving the UE running also failed. A coordinated clean-order LTE restart succeeded when executed as:

`stop UE -> EPC -> eNB -> fresh UE`

After that recovery, Q0 returned with `tun_srsue` source IP `172.16.0.2`, and a 10-packet user-plane confirmation completed with 0% loss.

The restored application path was then verified end-to-end with the exact frozen application prerequisites: Paho 2.1.0, MQTT 3.1.1, TLS, QoS1 SUBACK/PUBACK, broker round-trip receive, fresh-session evidence, and payload SHA-256 equality. Three independent fresh application sessions passed (`3/3`).

This supports the clean-order restart as an operational testbed recovery primitive only. It does not retroactively repair H1 or authorize scored runs. Any future use of an explicit LTE-stack restart inside calibration would be a prospective protocol change that must be frozen before use.

## Preserved evidence archives

Original H1 raw evidence:

- nuc1 H1 archive SHA-256: `3e3d4c44847bfb7e6304de89d8c1cc05ff9722b6a54d93dd08ce0acfa7418210`
- nuc2 H1 archive SHA-256: `c5d3b212af015061c092c79025258a7f3378e3351051eef48318f12964af2593`

Recovery-characterization archives:

- nuc1 SHA-256: `71aaea25a50ad955fa797a358b14cce4efc0e76ec0861468b3b99dd224c7dd55`
- nuc2 SHA-256: `431855c8662fa46a82f7baca60b5f3deeda4fd849cf4d90bfc4889800be3e71d`

Reproducibility fingerprints:

- nuc1 runtime record SHA-256: `1ef8b04a8d3a634c1cc3ded2b84c80a7140d877758a0d63010411971eab8607f`
- nuc1 fingerprint archive SHA-256: `af601716237082be410be3680f1e33b36240beae77e7b644f0f5bef811c1b647`
- nuc2 runtime record SHA-256: `fc1c131602c49b8376733ad8e190c4fc5d8d1976b62fe59c1e5becbe41cf8d5a`
- nuc2 fingerprint archive SHA-256: `ada35310a2dd46dba6c28a26604d41f28884799e0fc27c0846a7bf66421935bc`

## Node-local final chain-of-custody manifests

The final manifest script was run independently on both nodes. The differing hashes and file counts are preserved as node-local evidence inventories; they are not treated as an expectation of byte-identical cross-node manifests.

- `nuc2`: 34 files hashed; manifest SHA-256 `343a9deb1e432c0f5d30cbf55def3d133726a214a595d9f7f0723a5e87d8ec2e`
- `nuc1`: 22 files hashed; manifest SHA-256 `9596f23f4e9359d3395f29f6e0081d5acdec05dc6a986c0e0b0f19ac5fa35811`

This GitHub closeout record is the session-level aggregate linking both node-local manifests and the preserved archive/fingerprint hashes.

## Closeout decision

1. End live scientific experimentation for this reservation.
2. Preserve H1 exactly as `VALID_W1_RECOVERY_FAILURE`.
3. Keep H undefined and scored runs unauthorized.
4. Treat the demonstrated `EPC -> eNB -> UE` clean-order restart as testbed recovery knowledge to inform the next protocol design/rehearsal.
5. Before the next reservation, decide scientifically whether an explicit LTE-stack restart is admissible inside the outage/recovery semantics. If yes, freeze it prospectively and validate it in a non-scored Golden E2E rehearsal before any scored run.

No credentials or private keys are intentionally recorded in this closeout file.