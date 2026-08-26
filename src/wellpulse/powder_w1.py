from __future__ import annotations

from dataclasses import dataclass
from threading import Lock

from .store import DurableQueue
from .transport import PahoQoS1Session


@dataclass(frozen=True)
class ReplaySnapshot:
    connected: bool
    pending_count: int
    app_inflight_count: int
    published_calls: int
    puback_callbacks: int


class DurablePahoReplay:
    """Non-blocking W1 durable replay layer above the frozen Paho session.

    The telemetry generator writes every record durably before this object sees
    it. The replay layer only submits records while the MQTT session reports a
    live connection, keeps at most the frozen MQTT inflight limit active, and
    marks a durable record SENT only after Paho reports that its QoS1 publish was
    acknowledged. Generation therefore never waits for PUBACK.
    """

    def __init__(self, queue: DurableQueue, session: PahoQoS1Session):
        self.queue = queue
        self.session = session
        self._lock = Lock()
        self._active: dict[str, object] = {}

    def pump_once(self) -> ReplaySnapshot:
        with self._lock:
            completed = [rid for rid, info in self._active.items() if info.is_published()]
            for rid in completed:
                self.queue.mark_sent(rid, commit=False)
                self._active.pop(rid, None)
            if completed:
                self.queue.commit_state()

            transport = self.session.snapshot()
            if transport["connected"]:
                capacity = max(0, self.session.config.max_inflight_messages - len(self._active))
                if capacity:
                    for rid, payload_json, _checksum, _state in self.queue.pending_rows():
                        if capacity <= 0:
                            break
                        if rid in self._active:
                            continue
                        info = self.session.publish_async(payload_json)
                        self._active[rid] = info
                        capacity -= 1

            transport = self.session.snapshot()
            return ReplaySnapshot(
                connected=bool(transport["connected"]),
                pending_count=len(self.queue.pending_rows()),
                app_inflight_count=len(self._active),
                published_calls=int(transport["published_calls"]),
                puback_callbacks=int(transport["puback_callbacks"]),
            )

    def pending_record_ids(self) -> set[str]:
        with self._lock:
            return {row[0] for row in self.queue.pending_rows()}

    def close_at_horizon(self) -> None:
        self.session.close_at_horizon()
