#!/usr/bin/env python3
"""Fail-closed structural checks for the CL-WP-01 generated request RSpec."""

from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from pathlib import Path

EXPECTED_NODES = {"edge", "cloud"}
EXPECTED_LINK = "lan"
EXPECTED_IPS = {"10.10.0.1", "10.10.0.2"}
EXPECTED_SLIVER_TYPE = "raw-pc"


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_profile.py REQUEST_RSPEC.xml", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    root = ET.parse(path).getroot()

    nodes = [e for e in root.iter() if local_name(e.tag) == "node"]
    links = [e for e in root.iter() if local_name(e.tag) == "link"]
    node_ids = {e.attrib.get("client_id") for e in nodes}
    link_ids = {e.attrib.get("client_id") for e in links}

    ips = {
        e.attrib.get("address")
        for e in root.iter()
        if local_name(e.tag) == "ip" and e.attrib.get("address")
    }

    errors: list[str] = []
    if node_ids != EXPECTED_NODES:
        errors.append(f"nodes={sorted(node_ids)} expected={sorted(EXPECTED_NODES)}")
    if len(nodes) != 2:
        errors.append(f"node_count={len(nodes)} expected=2")
    if EXPECTED_LINK not in link_ids:
        errors.append(f"link_ids={sorted(link_ids)} missing={EXPECTED_LINK}")
    if not EXPECTED_IPS.issubset(ips):
        errors.append(f"ips={sorted(ips)} missing={sorted(EXPECTED_IPS - ips)}")

    for node in nodes:
        sliver_types = [
            e.attrib.get("name")
            for e in node.iter()
            if local_name(e.tag) == "sliver_type"
        ]
        if sliver_types != [EXPECTED_SLIVER_TYPE]:
            errors.append(
                f"node {node.attrib.get('client_id')} sliver_types={sliver_types} "
                f"expected={[EXPECTED_SLIVER_TYPE]}"
            )
        if node.attrib.get("exclusive") != "true":
            errors.append(
                f"node {node.attrib.get('client_id')} exclusive={node.attrib.get('exclusive')} expected=true"
            )

    if errors:
        print("CLWP01_STATIC_PROFILE_GATE=FAIL")
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("CLWP01_STATIC_PROFILE_GATE=PASS")
    print("nodes=edge,cloud")
    print("sliver_type=raw-pc")
    print("exclusive=true")
    print("lan=lan")
    print("data_plane_ips=10.10.0.1,10.10.0.2")
    print("live_resource_mutation=NO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
