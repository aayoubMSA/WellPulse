# WP2-P8 Golden Evidence Index — 2026-08-29

## Classification

`P8_CLASS=MANUAL_NON_SCORED_REFERENCE`

This index records immutable evidence anchors for the completed POWDER manual-reference campaign. It does not change historical scored P7B status.

## Primary evidence bundles

| Artifact | SHA256 | Notes |
|---|---|---|
| `WellPulse-P8-Evidence-ALL-20260829-004254.zip` | `6952565D8ED630496EB7A801DB90583F2FED2EFCDC81FEACD1A2072F18FA8878` | Master P8 evidence available in handover runtime; 403 ZIP entries |
| `WellPulse-P8-E10-E11-20260829-015817-FROZEN.zip` | `A6CEBA5107610639E62709F0041FB463CACBC45AA07847AFFE6600008B77C8F6` | E10/E11 collector bundle; all discovered runs collected with no partials |
| `WellPulse-POWDER-Platform-Specs-FROZEN.zip` | `5537947B03373FB6869C3E154CCCECAC387FF12481D74634AFB192CA03F26E18` | Two-node HW/OS/SW/runtime specification capture |
| `WellPulse-POWDER-Final-Documentation-FROZEN.zip` | `2B015A8FD4655F5615D570230C8989E54A4BD6EEB6E727D04D219B9013320C19` | Final profile/RSpec/radio/attenuation documentation; **PRIVATE** because captured manifest contains credential-bearing/encrypted portal material |
| `WellPulse-p8-e6-manual-20260829A-FROZEN.zip` | `93AC4E0BE040B3A3FF7815BA7A43354C4F69971DF1468A0BD55C75DD97C01539` | E6 standalone frozen run |
| `WellPulse-p8-e7-manual-20260829A-FROZEN.zip` | `886676778C667CB9B368456364972C91C4BF494DCC5FB1DA87D6EB14858DD22D` | E7 standalone frozen run |
| `WellPulse-p8-e8-manual-20260829A-FROZEN.zip` | `CA71214B12392C7349511B4400E288D59E6DE3A1507C043DB876E4642C227AFA` | E8 standalone frozen run |
| `WellPulse-p8-e9-manual-20260829A-FROZEN.zip` | `B89906139DD87EC2AF18CEF15072EFC065C8DA104C433F7FFAA431B41DCF0118` | E9 standalone frozen run |

## Departure archives currently anchored by home-PC hash

These were created and verified locally but were not available as uploaded runtime bytes when this index was written:

| Artifact | SHA256 | Policy |
|---|---|---|
| `WellPulse-POWDER-Departure-Capture-PRIVATE-FROZEN.zip` | `7DBA8CE95CF06B254939C692915325E369FFA114080AE10BACA446D4BF62A66E` | PRIVATE / access controlled |
| `WellPulse-POWDER-Departure-Capture-SANITIZED-FROZEN.zip` | `236C6E269CDA6F7814B50415917D277CD7D0ED78D7D9DB0C3C4D1FE185EAE7A4` | Shareable research preservation archive |

## Integrity observations

Departure per-node verification:

- `nuc1 VERIFIED=31 BAD=0 EXPECTED_EXCEPTION=1`
- `nuc2 VERIFIED=17 BAD=0 EXPECTED_EXCEPTION=1`

The expected exception is `CAPTURE_STATUS.txt`, whose final completion line was appended after `SHA256_MANIFEST.txt` was generated. This is documented as `DOCUMENTED_POST_MANIFEST_APPEND`, not evidence corruption.

## Platform / profile provenance

- reservation `WP-07-C`
- profile `srslte-controlled-rf`
- `enb1 -> nuc1 / CORE`
- `rue1 -> nuc2 / UE`
- profile repository commit `a6da96560b6526dc6816761282722c996418fd8c`
- final RF state reasserted to `0 dB`
- profile/RSpec identifies Intel NUC5300/B210 topology
- final runtime UHD probes returned no independently visible UHD device; do not claim a runtime USRP serial/firmware identity
- exact individual attenuator ID -> physical path mapping is not established

## Golden handover package

Local handover bundle assembled from all evidence bytes available in the ChatGPT runtime plus tooling and manifests:

- `WellPulse_POWDER_Golden_Handover_2026-08-29.zip`
- SHA256 `F94951A42C2DF429297CEC888EA81D3DC374B6E47F34D71AA2F3BCE7898642B4`

The Drive copy must additionally include the two departure archives listed above from the home PC.

## Storage policy

Raw/frozen binaries belong in Google Drive, with home-PC third copy retained until read-back verification. GitHub stores this index, hashes, handover, scripts, derived tables and analysis outputs only.
