"""Public identity and exact execution versions. Historical DOI belongs only to rc.3."""
PROTOCOL_NAME = "HARD Protocol"
PROTOCOL_FULL_NAME = "Human-centered AI Readiness Deployment Protocol"
DISPLAY_VERSION = "0.2"
RELEASE_LABEL = "Public Preview"
DISTRIBUTION_ID = "hard-0.2-preview-1"
PROTOCOL_VERSION = "0.2-preview.1"
MCP_VERSION = "0.2.0rc7"
SKILL_VERSION = "0.2.0-rc.7"
CONTRACT_VERSION = "0.2.0-rc.7"


def public_title():
    return f"{PROTOCOL_NAME} {DISPLAY_VERSION}"


def identity():
    return {"name": PROTOCOL_NAME, "full_name": PROTOCOL_FULL_NAME,
            "display_version": DISPLAY_VERSION, "release_label": RELEASE_LABEL,
            "distribution_id": DISTRIBUTION_ID}


def versions():
    return {"protocol": PROTOCOL_VERSION, "mcp": MCP_VERSION,
            "skill": SKILL_VERSION, "contract": CONTRACT_VERSION}
