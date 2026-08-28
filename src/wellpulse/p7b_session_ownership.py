from __future__ import annotations

from typing import Iterable, Mapping

FORBIDDEN_SERVICE_SESSIONS = frozenset({"ue", "srs-ue", "enb", "srs-enb", "srs-epc"})
SERVICE_PROCESS_NAMES = frozenset({"srsue", "srsenb", "srsepc"})
ALLOWED_CONTROLLER_HOST_ROLES = frozenset({"UE", "EXTERNAL"})


def _positive_pid(value: object) -> int:
    try:
        pid = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"INVALID_PID:{value}") from exc
    if pid <= 1:
        raise ValueError(f"INVALID_PID:{pid}")
    return pid


def normalize_session(value: object) -> str:
    session = str(value or "").strip()
    if not session:
        raise ValueError("CONTROLLER_SESSION_UNKNOWN")
    return session


def evaluate_controller_identity(
    *,
    controller_pid: object,
    controller_session: object,
    controller_process_name: object,
    controller_host_role: object,
) -> dict:
    """Evaluate A1/A3 without mutating the target.

    `NONE` is the explicit value for an attached SSH/non-tmux controller.
    Any tmux session used by the service lifecycle is rejected fail-closed.
    """

    failures: list[str] = []
    try:
        pid = _positive_pid(controller_pid)
    except ValueError as exc:
        pid = -1
        failures.append(str(exc))

    try:
        session = normalize_session(controller_session)
    except ValueError as exc:
        session = "UNKNOWN"
        failures.append(str(exc))

    process_name = str(controller_process_name or "").strip()
    if not process_name:
        failures.append("CONTROLLER_PROCESS_NAME_UNKNOWN")
    elif process_name in SERVICE_PROCESS_NAMES:
        failures.append(f"CONTROLLER_PROCESS_COLLIDES_WITH_SERVICE:{process_name}")

    host_role = str(controller_host_role or "").strip().upper()
    if host_role not in ALLOWED_CONTROLLER_HOST_ROLES:
        failures.append(f"CONTROLLER_HOST_ROLE_UNSUPPORTED:{host_role or 'UNKNOWN'}")

    if session in FORBIDDEN_SERVICE_SESSIONS:
        failures.append(f"CONTROLLER_IN_SERVICE_CLEANUP_SESSION:{session}")

    passed = not failures
    return {
        "gate": "PASS" if passed else "BLOCKED",
        "controller_pid": pid,
        "controller_session": session,
        "controller_process_name": process_name,
        "controller_host_role": host_role,
        "failures": failures,
        "CONTROLLER_SERVICE_SESSION_DISJOINTNESS": "PASS" if passed else "BLOCKED",
        "CONTROLLER_RESTORE_FAILURE_DOMAIN_SEPARATION": "PASS" if passed else "BLOCKED",
    }


def evaluate_pid_ownership(
    *,
    controller_pid: object,
    controller_host_role: object,
    target_host_role: object,
    service_pids_by_name: Mapping[str, Iterable[object]],
) -> dict:
    """Evaluate the exact PID set selected for destructive service cleanup.

    This is deliberately process/PID scoped. It does not authorize tmux-session
    destruction. The caller must stop if the controller PID appears in any
    selected service PID set.
    """

    failures: list[str] = []
    try:
        cpid = _positive_pid(controller_pid)
    except ValueError as exc:
        cpid = -1
        failures.append(str(exc))

    controller_role = str(controller_host_role or "").strip().upper()
    target_role = str(target_host_role or "").strip().upper()
    if controller_role not in ALLOWED_CONTROLLER_HOST_ROLES:
        failures.append(f"CONTROLLER_HOST_ROLE_UNSUPPORTED:{controller_role or 'UNKNOWN'}")
    if target_role not in {"UE", "CORE"}:
        failures.append(f"TARGET_HOST_ROLE_UNSUPPORTED:{target_role or 'UNKNOWN'}")

    normalized: dict[str, list[int]] = {}
    for process_name, raw_pids in service_pids_by_name.items():
        name = str(process_name).strip()
        if name not in SERVICE_PROCESS_NAMES:
            failures.append(f"UNAPPROVED_SERVICE_PROCESS_TARGET:{name}")
            continue
        pids: list[int] = []
        for raw in raw_pids:
            try:
                pids.append(_positive_pid(raw))
            except ValueError as exc:
                failures.append(str(exc))
        normalized[name] = sorted(set(pids))

    if controller_role == target_role:
        for name, pids in normalized.items():
            if cpid in pids:
                failures.append(f"CONTROLLER_PID_SELECTED_FOR_SERVICE_CLEANUP:{name}:{cpid}")

    passed = not failures
    return {
        "gate": "PASS" if passed else "BLOCKED",
        "controller_pid": cpid,
        "controller_host_role": controller_role,
        "target_host_role": target_role,
        "service_pids_by_name": normalized,
        "failures": failures,
        "SERVICE_PID_OWNERSHIP_PROOF": "PASS" if passed else "BLOCKED",
        "DESTRUCTIVE_TMUX_SESSION_KILL_AUTHORIZED": False,
    }
