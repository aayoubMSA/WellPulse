# Next Gate — FIT IoT-LAB Readiness

Do not book remote hardware until the local validation harness is ready to execute unchanged on a FIT A8 node.

## Required before booking

- local unit tests pass
- 10,000-record local W1 dry run completes
- B0 and W1 execution paths are both implemented
- MQTT/TLS publisher and idempotent receiver are implemented
- run manifest captures Git commit and configuration
- raw/derived evidence paths are fixed

## FIT smoke checks after account access

- SSH access to reserved A8 node
- runtime/dependency availability
- persistent storage path
- outbound MQTT/TLS connectivity
- clock/timezone behavior
- available disk
- `tc/netem` availability; if absent, record deterministic fallback before final runs

No final experiment begins until this gate is documented as passed.
