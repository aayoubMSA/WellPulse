class PublishOnlyBaseline:
    """Legacy non-durable lower bound: records generated while unavailable are lost."""

    def __init__(self, receiver):
        self.receiver = receiver

    def submit(self, record, link_up: bool) -> bool:
        if not link_up:
            return False
        return self.receiver.ingest(record.record_id, record.canonical_payload(), record.checksum_sha256)


class VolatileReconnectBaseline:
    """Strong baseline model: volatile in-memory QoS1/reconnect-style buffering.

    This models the scientific comparator planned for POWDER: standard MQTT QoS1
    with automatic reconnect and volatile client state, but no application-level
    disk durability or reconciliation. Records can survive a network-only outage
    while the process remains alive, but pending records are lost if the gateway
    process restarts.

    The scored POWDER implementation must still freeze and record the exact Paho
    MQTT client/session/queue semantics. This class is a deterministic local
    semantics model; it is not itself evidence of Paho behavior on POWDER.
    """

    def __init__(self, receiver):
        self.receiver = receiver
        self._pending = []
        self.restart_dropped = 0

    def _deliver(self, record) -> bool:
        return self.receiver.ingest(
            record.record_id,
            record.canonical_payload(),
            record.checksum_sha256,
        )

    def flush(self) -> int:
        pending = self._pending
        self._pending = []
        delivered = 0
        for record in pending:
            if self._deliver(record):
                delivered += 1
        return delivered

    def submit(self, record, link_up: bool) -> bool:
        if not link_up:
            self._pending.append(record)
            return False
        self.flush()
        return self._deliver(record)

    def restart(self) -> int:
        """Drop volatile pending state, as a process restart would."""
        dropped = len(self._pending)
        self.restart_dropped += dropped
        self._pending = []
        return dropped

    @property
    def pending_count(self) -> int:
        return len(self._pending)
