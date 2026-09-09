"""Exercise the installed server through a real stdio client."""
import asyncio
import json
import sys
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def roundtrip():
    params = StdioServerParameters(command=sys.executable,args=["-m","hcai_readiness.server"])
    async with stdio_client(params) as (read,write):
        async with ClientSession(read,write) as client:
            await client.initialize()
            names={t.name for t in (await client.list_tools()).tools}
            assert names=={"assessment_template","assess_session","summarize_batch"}
            template=await client.call_tool("assessment_template",{})
            assert not template.isError
            d=json.loads((Path(__file__).resolve().parents[1]/"examples/session.json").read_text())
            result=await client.call_tool("assess_session",{"session":d})
            assert not result.isError
            payload=json.loads(result.content[0].text)
            assert payload["metrics"]["reference_set_recall_percent"]==62.5
            d["reference_defects"]=-1
            bad=await client.call_tool("assess_session",{"session":d})
            assert bad.isError
            resources=await client.list_resources()
            assert any(str(r.uri)=="hcai://protocol" for r in resources.resources)
            resource=await client.read_resource("hcai://protocol")
            assert "0.1-rc.3" in resource.contents[0].text
            prompt=await client.get_prompt("plan_handoff_review")
            assert prompt.messages

def test_stdio_roundtrip():
    asyncio.run(asyncio.wait_for(roundtrip(),timeout=30))
