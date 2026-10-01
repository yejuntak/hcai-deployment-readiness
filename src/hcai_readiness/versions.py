# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Yejun Tak
"""Public identity and exact execution versions. Historical DOI belongs only to rc.3."""
PROTOCOL_NAME = "H.A.R.D. Protocol"
PROTOCOL_FULL_NAME = "Human-centered AI Readiness and Decision Protocol"
DISPLAY_VERSION = "0.3"
RELEASE_LABEL = "Public Preview"
DISTRIBUTION_ID = "hard-0.3-preview-2"
PROTOCOL_VERSION = "0.3-preview.2"
MCP_VERSION = "0.3.0rc2"
SKILL_VERSION = "0.3.0-rc.2"
CONTRACT_VERSION = "0.3.0-rc.2"


def public_title():
    return f"{PROTOCOL_NAME} {DISPLAY_VERSION}"


def identity():
    return {"name": PROTOCOL_NAME, "full_name": PROTOCOL_FULL_NAME,
            "display_version": DISPLAY_VERSION, "release_label": RELEASE_LABEL,
            "distribution_id": DISTRIBUTION_ID}


def versions():
    return {"protocol": PROTOCOL_VERSION, "mcp": MCP_VERSION,
            "skill": SKILL_VERSION, "contract": CONTRACT_VERSION}
