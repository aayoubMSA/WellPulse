# Architecture Baseline

The frozen conceptual path is:

`read-only industrial inputs -> acquisition/quality -> durable local queue -> network/MQTT/TLS -> idempotent cloud ingestion -> storage/rules/dashboard`

WP-RT01 isolates the resilience spine. Synthetic Modbus-like payloads are acceptable because WP-RT01 does not claim pump-sensor validity; it tests record persistence, transport interruption, restart recovery, and reconciliation.
