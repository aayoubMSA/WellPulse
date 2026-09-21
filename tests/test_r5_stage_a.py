from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[1]


def load_module(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, REPO / rel)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


runmod = load_module("r5_run", "scripts/analyze_r5_stage_a_run.py")
stagemod = load_module("r5_stage", "scripts/adjudicate_r5_stage_a.py")


class R5PrimaryRuleTests(unittest.TestCase):
    def test_invalidity_dominates(self):
        self.assertEqual(
            runmod.adjudicate_primary(
                invalid=["x"], causal_positive=True, clock_positive=True,
                censored_positive=True, m3_observed=True, reversal=False
            ),
            "INVALID",
        )

    def test_causal_positive_without_clock_resolution(self):
        self.assertEqual(
            runmod.adjudicate_primary(
                invalid=[], causal_positive=True, clock_positive=False,
                censored_positive=False, m3_observed=True, reversal=False
            ),
            "POSITIVE_CAUSAL",
        )

    def test_censored_causal_positive(self):
        self.assertEqual(
            runmod.adjudicate_primary(
                invalid=[], causal_positive=True, clock_positive=False,
                censored_positive=False, m3_observed=False, reversal=False
            ),
            "CENSORED_POSITIVE_CAUSAL",
        )

    def test_clock_positive(self):
        self.assertEqual(
            runmod.adjudicate_primary(
                invalid=[], causal_positive=False, clock_positive=True,
                censored_positive=False, m3_observed=True, reversal=False
            ),
            "POSITIVE_CLOCK",
        )

    def test_reversal(self):
        self.assertEqual(
            runmod.adjudicate_primary(
                invalid=[], causal_positive=False, clock_positive=False,
                censored_positive=False, m3_observed=True, reversal=True
            ),
            "REVERSAL",
        )


class R5ClockRuleTests(unittest.TestCase):
    @staticmethod
    def _clock(source_est, source_bound, receiver_est, receiver_bound):
        return {
            "source": {"best": {
                "offset_remote_minus_controller_s": source_est,
                "midpoint_bound_s": source_bound,
            }},
            "receiver": {"best": {
                "offset_remote_minus_controller_s": receiver_est,
                "midpoint_bound_s": receiver_bound,
            }},
        }

    def test_relative_interval_uses_pre_post_hull(self):
        pre = self._clock(1.0, 0.1, 4.0, 0.2)
        post = self._clock(1.2, 0.1, 4.1, 0.2)
        lo, hi = runmod.relative_receiver_minus_source_interval(pre, post)
        self.assertAlmostEqual(lo, 2.5)
        self.assertAlmostEqual(hi, 3.4)


class R5StageDecisionTests(unittest.TestCase):
    @staticmethod
    def r(run_id, valid=True, positive=False, cls="UNRESOLVED"):
        return {
            "run_id": run_id,
            "valid": valid,
            "positive_for_stage_rule": positive,
            "primary_class": cls,
        }

    def test_two_of_three_confirms_and_stops(self):
        out = stagemod.adjudicate([
            self.r("R1", positive=True, cls="POSITIVE_CAUSAL"),
            self.r("R2", positive=True, cls="POSITIVE_CLOCK"),
            self.r("R3"),
        ])
        self.assertEqual(out["decision"], "CONFIRM_REPEAT_OCCURRENCE_STOP")
        self.assertEqual(out["positive_run_count"], 2)

    def test_zero_of_three_not_confirmed(self):
        out = stagemod.adjudicate([self.r("R1"), self.r("R2"), self.r("R3")])
        self.assertEqual(out["decision"], "NOT_CONFIRMED_STOP")

    def test_one_of_three_requires_exactly_two_more(self):
        out = stagemod.adjudicate([
            self.r("R1", positive=True, cls="POSITIVE_CAUSAL"),
            self.r("R2"), self.r("R3"),
        ])
        self.assertEqual(out["decision"], "STAGE_B_REQUIRED_TWO_ADDITIONAL_VALID_RUNS")

    def test_invalid_run_blocks_stage_adjudication(self):
        out = stagemod.adjudicate([
            self.r("R1", valid=False, cls="INVALID"),
            self.r("R2", positive=True, cls="POSITIVE_CAUSAL"),
            self.r("R3", positive=True, cls="POSITIVE_CLOCK"),
        ])
        self.assertFalse(out["stage_complete"])
        self.assertEqual(out["decision"], "STAGE_A_INCOMPLETE_INVALID_RUN")


class R5EndToEndSyntheticTests(unittest.TestCase):
    def setUp(self):
        self.saved = (
            runmod.H_FIRST, runmod.H_LAST, runmod.LIVE_WITNESS_SEQ,
            runmod.EXPECTED_RECORDS, runmod.EXPECTED_H,
        )
        runmod.H_FIRST = 3
        runmod.H_LAST = 4
        runmod.LIVE_WITNESS_SEQ = 5
        runmod.EXPECTED_RECORDS = 6
        runmod.EXPECTED_H = 2

    def tearDown(self):
        (
            runmod.H_FIRST, runmod.H_LAST, runmod.LIVE_WITNESS_SEQ,
            runmod.EXPECTED_RECORDS, runmod.EXPECTED_H,
        ) = self.saved

    @staticmethod
    def _clock(source_est=0.0, receiver_est=100.0, bound=0.01):
        return {
            "source": {"best": {
                "offset_remote_minus_controller_s": source_est,
                "midpoint_bound_s": bound,
            }},
            "receiver": {"best": {
                "offset_remote_minus_controller_s": receiver_est,
                "midpoint_bound_s": bound,
            }},
        }

    def test_causal_witness_is_detected_end_to_end(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "source"
            source.mkdir()
            run_id = "SYN-R1"

            wires = {}
            with (source / "generated.jsonl").open("w", encoding="utf-8") as fh:
                for seq in range(1, 7):
                    obj = {
                        "run_id": run_id,
                        "boot_id": "BOOT-001",
                        "sequence": seq,
                        "record_id": f"{run_id}:BOOT-001:{seq:08d}",
                    }
                    wire = json.dumps(obj, sort_keys=True, separators=(",", ":"))
                    wires[seq] = wire
                    fh.write(wire + "\n")

            with (source / "q0_source_generation.ndjson").open("w", encoding="utf-8") as fh:
                for seq in range(1, 7):
                    mono = float(seq)
                    if seq == 5:
                        mono = 6.0
                    elif seq == 6:
                        mono = 7.0
                    fh.write(json.dumps({
                        "event_type": "SOURCE_GENERATED",
                        "run_id": run_id,
                        "sequence": seq,
                        "record_id": f"{run_id}:BOOT-001:{seq:08d}",
                        "utc_epoch_s": mono,
                        "mono_s": mono,
                    }) + "\n")

            mqtt = [
                {"event_type": "CONNACK_OK", "utc_epoch_s": 1.0, "mono_s": 1.0},
                {"event_type": "CONNACK_OK", "utc_epoch_s": 4.7, "mono_s": 4.7},
                {"event_type": "PUBACK", "record_id": f"{run_id}:BOOT-001:{3:08d}",
                 "utc_epoch_s": 4.9, "mono_s": 4.9},
                {"event_type": "PUBACK", "record_id": f"{run_id}:BOOT-001:{4:08d}",
                 "utc_epoch_s": 5.0, "mono_s": 5.0},
            ]
            (source / "q0_mqtt_events.ndjson").write_text(
                "".join(json.dumps(x) + "\n" for x in mqtt), encoding="utf-8"
            )

            transport = [
                {"event_type": "OUTAGE_CONFIRMED", "utc_epoch_s": 2.5, "mono_s": 2.5},
                {"event_type": "RESTORE_APPLY", "utc_epoch_s": 4.5, "mono_s": 4.5},
                {"event_type": "PROBE_SUCCESS", "utc_epoch_s": 4.6, "mono_s": 4.6},
            ]
            (source / "q0_transport_events.ndjson").write_text(
                "".join(json.dumps(x) + "\n" for x in transport), encoding="utf-8"
            )
            (source / "edge_metrics.json").write_text(json.dumps({
                "architecture": "W1",
                "condition": "C1",
                "restart_count": 0,
                "queue_pending": 0,
                "evidence_class": "R5_SCORED_STAGE_A",
            }), encoding="utf-8")

            # seq 5 is observed before historical seq 3 and 4.
            order = [1, 2, 5, 3, 4, 6]
            with (root / "receiver_raw.tsv").open("w", encoding="utf-8") as fh:
                for i, seq in enumerate(order, 1):
                    fh.write(f"{100.0 + i * 0.1:.6f}\t{wires[seq]}\n")

            (root / "clock_pre.json").write_text(
                json.dumps(self._clock()), encoding="utf-8"
            )
            (root / "clock_post.json").write_text(
                json.dumps(self._clock()), encoding="utf-8"
            )

            result, _ = runmod.classify_run(root, run_id)
            self.assertTrue(result["valid"], result["invalid_reasons"])
            self.assertTrue(result["receiver_causal_positive"])
            self.assertTrue(result["positive_for_stage_rule"])
            self.assertGreaterEqual(result["historical_records_after_causal_witness"], 1)


if __name__ == "__main__":
    unittest.main()
