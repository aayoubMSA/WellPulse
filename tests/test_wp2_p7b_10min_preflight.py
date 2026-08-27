from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROBE = ROOT / "scripts" / "wp2_p7b_target_preflight_probe.sh"
CONTRACT = ROOT / "experiments" / "WP-PWD01" / "P7B_10MIN_PREFLIGHT_CONTRACT_v1.md"


def test_probe_and_contract_exist():
    assert PROBE.is_file()
    assert CONTRACT.is_file()


def test_probe_is_read_only_and_non_scored():
    text = PROBE.read_text(encoding="utf-8")
    forbidden = [
        "experiment create",
        "experiment terminate",
        "experiment extend",
        "tmcc attenuator set",
        "scored_runs_authorized=true",
        "start_broker(",
        "run_cell(",
    ]
    for token in forbidden:
        assert token not in text
    assert "RF_MUTATION NO" in text
    assert "CELL_EXECUTION NO" in text
    assert "TEARDOWN NO" in text
    assert "SCORED NO" in text


def test_probe_covers_accumulated_failure_classes():
    text = PROBE.read_text(encoding="utf-8")
    required = [
        "SYSTEM_PYTHON_VERSION",
        "SYSTEM_PYTHON3_VERSION",
        "APP_PYTHON_VERSION",
        "TMCC_ATTENUATOR_RAW_BEGIN",
        "UNRESOLVED_PATH_TOKEN_GATE",
        "SHELL_ONLY_PRESERVATION_GATE",
        "PROJECT_ESCROW_DIR",
        "PROJECT_ESCROW_WRITABLE",
        "sha256sum",
        "tar",
        "find",
        "ssh",
        "scp",
    ]
    for token in required:
        assert token in text


def test_contract_has_hard_timebox_and_fail_closed_verdict():
    text = CONTRACT.read_text(encoding="utf-8")
    assert "Target wall time <= 4 minutes" in text
    assert "Hard stop 8 minutes" in text
    assert "WP2_P7B_10MIN_PREFLIGHT=PASS" in text
    assert "WP2_P7B_10MIN_PREFLIGHT=BLOCKED:<first_actionable_failure>" in text
    assert "scored_runs_authorized=false" in text
