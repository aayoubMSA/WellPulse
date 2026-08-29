# WP2-P14 — Figure Captions and Accessibility Text

## Figure 1

**Caption:** Final unique-record completeness for the FIT IoT-LAB architecture experiment. Each condition contains three replicate-level B0 and W1 observations; small horizontal offsets reveal coincident replicate values without altering the measured y values. Both architectures achieved 100% under C0. Under C1 and C2, B0 retained 80% while W1 retained 100% in all three replicates. Results are bounded to the tested FIT workload and B0 non-durable baseline.

**Alt text:** Three condition groups. Healthy has both B0 and W1 at 100%. Broker outage and outage plus gateway restart show B0 at 80% and W1 at 100% for each of three replicates.

## Figure 2

**Caption:** W1 post-outage backlog-drain time in the FIT IoT-LAB experiment. Symbols show individual replicates and the horizontal segment shows the arithmetic mean. Backlog drain is reported separately from transport reconnect time because they are distinct recovery constructs.

**Alt text:** Two groups of three replicate points around 67.3–68.9 seconds, with means near 67.73 seconds for C1 and 67.87 seconds for C2.

## Figure 3

**Caption:** Cross-layer response during ascending (E1R4) and descending (E2) POWDER attenuation sweeps. ICMP is shown as response success (100 minus packet-loss percentage) so that it shares a common 0–100% scale with MQTT unique-record completeness. At 51 dB in E1R4, ICMP response had fallen to 70% while MQTT remained complete; at 52 dB both layers degraded. The attenuation values are experiment-specific and do not define a universal failure threshold.

**Alt text:** Four line series across attenuation. Ascending ICMP and MQTT are complete through 50 dB; at 51 dB ICMP falls to 70% while MQTT stays 100%; at 52 dB they fall to 40% and 65%. Descending data recover from 35% ICMP and 55% MQTT at 52 dB to 90% and 100% at 51 dB.

## Figure 4

**Caption:** Near-transition MQTT repeatability in POWDER E3. All three cycles remain complete through 50 dB, remain 95–100% at 51 dB, and diverge sharply at 52 dB (60%, 25%, and 55%), demonstrating severe but variable impairment rather than a single deterministic transition.

**Alt text:** Three cycle lines overlap at 100% for 49 and 50 dB, remain near 100% at 51 dB, then separate to 60%, 25%, and 55% at 52 dB.
