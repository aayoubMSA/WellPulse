import json
import sqlite3
from pathlib import Path
from .records import Record

class DurableQueue:
    def __init__(self, path):
        self.path = Path(path)
        self.conn = sqlite3.connect(self.path)
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA synchronous=FULL")
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS queue (
                record_id TEXT PRIMARY KEY,
                payload_json TEXT NOT NULL,
                checksum_sha256 TEXT NOT NULL,
                state TEXT NOT NULL DEFAULT 'PENDING'
            )"""
        )
        self.conn.commit()

    def enqueue(self, record: Record) -> None:
        self.conn.execute(
            "INSERT OR IGNORE INTO queue(record_id,payload_json,checksum_sha256,state) VALUES(?,?,?,'PENDING')",
            (record.record_id, record.canonical_payload(), record.checksum_sha256),
        )
        self.conn.commit()

    def rows(self):
        return list(self.conn.execute("SELECT record_id,payload_json,checksum_sha256,state FROM queue ORDER BY record_id"))

    def pending_rows(self):
        return list(self.conn.execute(
            "SELECT record_id,payload_json,checksum_sha256,state FROM queue WHERE state='PENDING' ORDER BY record_id"
        ))

    def mark_sent(self, record_id: str, *, commit: bool = True) -> None:
        self.conn.execute("UPDATE queue SET state='SENT' WHERE record_id=?", (record_id,))
        if commit:
            self.conn.commit()

    def commit_state(self) -> None:
        self.conn.commit()

    def count(self) -> int:
        return self.conn.execute("SELECT COUNT(*) FROM queue").fetchone()[0]

    def close(self):
        self.conn.close()
