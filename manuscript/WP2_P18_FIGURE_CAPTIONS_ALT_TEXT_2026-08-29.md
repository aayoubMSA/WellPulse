# P18 publication captions and accessibility text

## Figure 1 — Architecture and evidence roles
**Caption.** WellPulse W1 record lifecycle and non-overlapping experimental evidence roles. Panel A summarizes the evaluated record path: generated telemetry receives a stable identity and SHA-256 checksum, enters durable PENDING state, is published when delivery is available, and is reconciled from independent receiver identities; unavailable delivery returns to durable state rather than being treated as final loss. Panel B separates the inferential roles of the two testbeds: FIT IoT-LAB supports the B0-versus-W1 record-survival comparison, whereas POWDER supports communication-path degradation and recovery characterization. The two evidence classes are integrated through structured failure-domain-aware triangulation only and are not statistically pooled.

**Alt text.** Two-panel diagram. The upper panel shows Generate → Identity/hash → Durable queue → MQTT publish → Receiver → Reconciliation, with failed delivery returning to the durable queue and successful delivery reaching SENT state. The lower panel shows FIT leading to record-state survival and POWDER leading to path degradation/recovery; both point to structured synthesis, with a note that no cross-platform reliability statistic or POWDER W1-versus-baseline effect is claimed.

## Figure 2 — FIT final completeness
**Caption.** Final receiver-reconciled unique-record completeness in the FIT IoT-LAB experiment. Each architecture-condition combination contains three run-level replicates. B0 and W1 are both complete under healthy C0. Under C1 broker outage and C2 broker outage plus gateway-process restart, B0 ends at 80% and W1 at 100% in every run. B0 is a non-durable publish-only baseline; the figure does not establish superiority over durable MQTT persistence or a population reliability probability.

**Alt text.** Three condition groups on a 0–100% scale. Both B0 circles and W1 squares are at 100% in C0. In C1 and C2, three B0 circles are at 80% and three W1 squares are at 100%.

## Figure 3 — POWDER transition and direction
**Caption.** Cross-layer response during the accepted ascending E1R4 and descending E2 programmed-attenuation sweeps. ICMP is shown as response success (100 minus packet-loss percentage) so that it shares a truthful percentage scale with MQTT unique-record completeness. In E1R4, ICMP response falls to 70% at 51 dB while MQTT remains complete; at 52 dB both layers degrade. The attenuation values describe the tested POWDER profile and do not define a universal failure threshold.

**Alt text.** Four line series on a 0–100% vertical scale. Ascending ICMP and MQTT remain at 100% through 50 dB; at 51 dB ICMP is 70% and MQTT 100%; at 52 dB they are 40% and 65%. Descending E2 begins at 52 dB with 35% ICMP response and 55% MQTT completeness, then recovers strongly by 51 dB.

## Figure 4 — POWDER E3 repeatability
**Caption.** Near-transition MQTT unique-record completeness across the three accepted E3 cycles. All cycles are complete at 49–50 dB, remain 95–100% at 51 dB, and diverge at 52 dB to 60%, 25%, and 55%. The full 0–100% percentage scale is retained to avoid visually exaggerating the cycle differences.

**Alt text.** Three cycle lines are at 100% for 49 and 50 dB. At 51 dB two cycles are 100% and one is 95%. At 52 dB the three values are 60%, 25%, and 55%.
