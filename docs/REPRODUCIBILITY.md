# Reproducibility Rules

Every final remote run must preserve:

- experiment/run identifier
- Git commit SHA
- platform/site/node identifiers
- start/end timestamps in UTC
- experiment configuration
- package/system versions
- generated record ledger
- edge events and queue events
- impairment log
- cloud received ledger
- reconciliation output
- stdout/stderr
- machine-readable metrics
- SHA-256 manifest

Raw logs are immutable evidence. Derived files must be reproducible from raw evidence plus a specific Git commit. Never regenerate missing measurements.
