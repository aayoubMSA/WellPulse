from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PROBE = ROOT / "scripts/wp2_powder_ssh_environment_inventory_v2.sh"


def test_inventory_v2_shell_syntax():
    q = subprocess.run(["bash", "-n", str(PROBE)], capture_output=True, text=True)
    assert q.returncode == 0, q.stdout + q.stderr


def test_inventory_v2_is_read_only_by_construction():
    text = PROBE.read_text(encoding="utf-8")
    forbidden = (
        "portal-cli experiment create",
        "portal-cli experiment terminate",
        "tmcc attenuator",
        "wp2_p7b_c_node",
        "systemctl restart",
        "service restart",
    )
    for token in forbidden:
        assert token not in text


def test_inventory_v2_avoids_known_runtime_qa_escapes():
    text = PROBE.read_text(encoding="utf-8")
    assert 'PINNED="$HOME/.wp2-golden-venv/bin/python"' in text
    assert "importlib.metadata as md" in text
    assert "pkg_resources" not in text
    assert "third_party_imports.txt" in text
    assert "SOURCE|MISSING|" in text
    assert "SOURCE|SYNTAX_FAIL|" in text
    assert "REPO_PRESENT=yes" in text
    assert 'git -C "$REPO" rev-parse HEAD' in text
    assert "openssl version" in text
    assert "paho-mqtt" in text
