from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import hashlib
import json

@dataclass(frozen=True)
class Record:
    run_id: str
    boot_id: str
    sequence: int
    generated_at_utc: str
    source: str
    payload: dict
    quality_flag: str = "OK"

    @property
    def record_id(self) -> str:
        return f"{self.run_id}:{self.boot_id}:{self.sequence:08d}"

    def canonical_payload(self) -> str:
        body = {**asdict(self), "record_id": self.record_id}
        return json.dumps(body, sort_keys=True, separators=(",", ":"))

    @property
    def checksum_sha256(self) -> str:
        return hashlib.sha256(self.canonical_payload().encode("utf-8")).hexdigest()

def make_record(run_id: str, boot_id: str, sequence: int) -> Record:
    return Record(
        run_id=run_id,
        boot_id=boot_id,
        sequence=sequence,
        generated_at_utc=datetime.now(timezone.utc).isoformat(),
        source="synthetic_modbus_like",
        payload={"register_1": 1000 + sequence, "status": sequence % 4},
    )
