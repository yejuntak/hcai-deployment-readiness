"""Exact candidate identities. Historical DOI belongs only to rc.3."""
PROTOCOL_VERSION = "0.1-rc.4-candidate.6"
MCP_VERSION = "0.2.0rc6"
SKILL_VERSION = "0.2.0-rc.6"
CONTRACT_VERSION = "0.2.0-rc.6"


def versions():
    return {"protocol": PROTOCOL_VERSION, "mcp": MCP_VERSION,
            "skill": SKILL_VERSION, "contract": CONTRACT_VERSION}
