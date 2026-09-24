"""Exact candidate identities. Historical DOI belongs only to rc.3."""
PROTOCOL_VERSION = "0.1-rc.4-candidate.4"
MCP_VERSION = "0.2.0rc4"
SKILL_VERSION = "0.2.0-rc.4"
CONTRACT_VERSION = "0.2.0-rc.4"


def versions():
    return {"protocol": PROTOCOL_VERSION, "mcp": MCP_VERSION,
            "skill": SKILL_VERSION, "contract": CONTRACT_VERSION}
