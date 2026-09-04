#!/usr/bin/env python3
"""Fail-closed, dependency-free source checks for the CL-WP-01 profile.

This gate intentionally does not import geni-lib or contact CloudLab. The
CloudLab portal remains authoritative for compiling the repository profile into
an RSpec in its own supported runtime.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

EXPECTED_RAWPCS = {"edge", "cloud"}
EXPECTED_LAN = "lan"
EXPECTED_IPS = {"10.10.0.1", "10.10.0.2"}
FORBIDDEN_CALL_ATTRS = {"addService", "Install", "Execute"}
FORBIDDEN_IMPORT_ROOTS = {"os", "subprocess", "socket", "requests", "urllib"}


def literal_first_arg(call: ast.Call) -> str | None:
    if not call.args:
        return None
    arg = call.args[0]
    return arg.value if isinstance(arg, ast.Constant) and isinstance(arg.value, str) else None


def call_attr_name(call: ast.Call) -> str | None:
    func = call.func
    if isinstance(func, ast.Attribute):
        return func.attr
    if isinstance(func, ast.Name):
        return func.id
    return None


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_profile.py PROFILE.py", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))

    rawpcs: set[str] = set()
    lans: set[str] = set()
    ips: set[str] = set()
    forbidden_calls: list[str] = []
    forbidden_imports: list[str] = []
    print_rspec_calls = 0

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            name = call_attr_name(node)
            if name == "RawPC":
                value = literal_first_arg(node)
                if value:
                    rawpcs.add(value)
            elif name == "LAN":
                value = literal_first_arg(node)
                if value:
                    lans.add(value)
            elif name == "IPv4Address":
                value = literal_first_arg(node)
                if value:
                    ips.add(value)
            elif name == "printRequestRSpec":
                print_rspec_calls += 1
            elif name in FORBIDDEN_CALL_ATTRS:
                forbidden_calls.append(name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".", 1)[0]
                if root in FORBIDDEN_IMPORT_ROOTS:
                    forbidden_imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            root = node.module.split(".", 1)[0]
            if root in FORBIDDEN_IMPORT_ROOTS:
                forbidden_imports.append(node.module)

    errors: list[str] = []
    if rawpcs != EXPECTED_RAWPCS:
        errors.append(f"RawPCs={sorted(rawpcs)} expected={sorted(EXPECTED_RAWPCS)}")
    if lans != {EXPECTED_LAN}:
        errors.append(f"LANs={sorted(lans)} expected={[EXPECTED_LAN]}")
    if ips != EXPECTED_IPS:
        errors.append(f"IPv4Address={sorted(ips)} expected={sorted(EXPECTED_IPS)}")
    if print_rspec_calls != 1:
        errors.append(f"printRequestRSpec_calls={print_rspec_calls} expected=1")
    if forbidden_calls:
        errors.append(f"forbidden_startup_calls={sorted(forbidden_calls)}")
    if forbidden_imports:
        errors.append(f"forbidden_runtime_imports={sorted(forbidden_imports)}")
    if "lan.addInterface(edge_if)" not in source or "lan.addInterface(cloud_if)" not in source:
        errors.append("LAN must explicitly attach edge_if and cloud_if")

    if errors:
        print("CLWP01_STATIC_PROFILE_GATE=FAIL")
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("CLWP01_STATIC_PROFILE_GATE=PASS")
    print("rawpcs=edge,cloud")
    print("lan=lan")
    print("data_plane_ips=10.10.0.1,10.10.0.2")
    print("startup_services=NONE")
    print("external_runtime_calls=NONE")
    print("live_resource_mutation=NO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
