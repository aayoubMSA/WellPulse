import sqlite3
from pathlib import Path
from datetime import datetime, timezone


class IdempotentReceiver:
    """SQLite-backed idempotent sink keyed by WellPulse record_id."""

    def __init__(self, path):
        self.path = Path(path)
        self.conn = sqlite3.connect(self.path)
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS received (
                record_id TEXT PRIMARY KEY,
                payload_json TEXT NOT NULL,
                checksum_sha256 TEXT NOT NULL,
                first_seen_utc TEXT NOT NULL
            )"""
        )
        self.conn.commit()

    def ingest(self, record_id: str, payload_json: str, checksum_sha256: str) -> bool:
        cur = self.conn.execute(
            "INSERT OR IGNORE INTO received(record_id,payload_json,checksum_sha256,first_seen_utc) VALUES(?,?,?,?)",
            (record_id, payload_json, checksum_sha256, datetime.now(timezone.utc).isoformat()),
        )
        self.conn.commit()
        return cur.rowcount == 1

    def ids(self):
        return [r[0] for r in self.conn.execute("SELECT record_id FROM received ORDER BY record_id")]

    def count(self) -> int:
        return self.conn.execute("SELECT COUNT(*) FROM received").fetchone()[0]

    def close(self):
        self.conn.close()
