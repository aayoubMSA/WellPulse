class PublishOnlyBaseline:
    """Non-durable baseline: a record is permanently lost when delivery is unavailable."""

    def __init__(self, receiver):
        self.receiver = receiver

    def submit(self, record, link_up: bool) -> bool:
        if not link_up:
            return False
        return self.receiver.ingest(record.record_id, record.canonical_payload(), record.checksum_sha256)
