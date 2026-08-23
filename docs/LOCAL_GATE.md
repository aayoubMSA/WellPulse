# Local readiness gate

The required pre-FIT local gate is deliberately bounded to the minimum high-value checks:

1. **W1 / C2 / 10,000 records** — durable offline-first queue under outage plus process restart. Expected: 10,000/10,000 unique final records, zero missing, zero duplicates.
2. **B0 / C1 / 10,000 records** — publish-only/non-durable baseline under the deterministic outage window. Expected: records 3001–5000 are permanently missing (2,000 records).

The full B0/W1 × C0/C1/C2 matrix remains a final experiment requirement on the selected testbed.

The queue commits each newly acquired record durably. Delivery acknowledgements may be committed in batches because a crash before an acknowledgement commit only causes safe retransmission; the receiver is idempotent on `record_id`.

This gate validates software plumbing only. It is not real-hardware, wireless, rural, pump, hydraulic, or Siwa evidence.
