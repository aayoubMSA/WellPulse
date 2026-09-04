"""CL-WP-01: minimal CloudLab repository-based profile.

Allocates two bare-metal nodes (edge, cloud) joined by one isolated LAN.
No startup services are executed in this first profile revision; the initial live
allocation is intentionally a bounded infrastructure smoke test.
"""

import geni.portal as portal
import geni.rspec.pg as rspec

request = portal.context.makeRequestRSpec()

edge = request.RawPC("edge")
edge_if = edge.addInterface("if1")
edge_if.addAddress(rspec.IPv4Address("10.10.0.1", "255.255.255.0"))

cloud = request.RawPC("cloud")
cloud_if = cloud.addInterface("if1")
cloud_if.addAddress(rspec.IPv4Address("10.10.0.2", "255.255.255.0"))

lan = request.LAN("lan")
lan.addInterface(edge_if)
lan.addInterface(cloud_if)

portal.context.printRequestRSpec()
