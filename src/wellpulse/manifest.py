from datetime import datetime, timezone
from hashlib import sha256
import platform
import subprocess
from pathlib import Path


def git_commit(root: Path) -> str:
    try:
        return subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return "UNRESOLVED"


def file_sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def build_run_manifest(*, root: Path, run_id: str, experiment_version: str, config_path: Path,
                       architecture: str, condition: str, raw_path: str, derived_path: str) -> dict:
    return {
        "run_id": run_id,
        "experiment_version": experiment_version,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": git_commit(root),
        "config_path": str(config_path.relative_to(root)),
        "config_sha256": file_sha256(config_path),
        "architecture": architecture,
        "condition": condition,
        "raw_evidence_path": raw_path,
        "derived_results_path": derived_path,
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "evidence_class": "LOCAL_SOFTWARE_GATE_NOT_PUBLICATION_EVIDENCE",
    }
