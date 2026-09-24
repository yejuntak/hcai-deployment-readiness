"""Exercise the installed server through a real stdio client."""
import asyncio
import json
import sys
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from hcai_readiness.contracts import Assessment
from hcai_readiness.engine import assess

async def roundtrip():
    params = StdioServerParameters(command=sys.executable,args=["-m","hcai_readiness.server"])
    async with stdio_client(params) as (read,write):
        async with ClientSession(read,write) as client:
            await client.initialize()
            names={t.name for t in (await client.list_tools()).tools}
            assert names=={"assessment_template","assess_legacy_session","summarize_legacy_batch",
                           "assess_engineering_commitment", "validate_pilot_run", "export_public_feedback"}
            template=await client.call_tool("assessment_template",{})
            assert not template.isError
            d=json.loads((Path(__file__).resolve().parents[1]/"examples/session.json").read_text())
            result=await client.call_tool("assess_legacy_session",{"session":d})
            assert not result.isError
            payload=json.loads(result.content[0].text)
            assert payload["metrics"]["reference_set_recall_percent"]==62.5
            d["reference_defects"]=-1
            bad=await client.call_tool("assess_legacy_session",{"session":d})
            assert bad.isError
            resources=await client.list_resources()
            assert any(str(r.uri)=="hcai://protocol" for r in resources.resources)
            resource=await client.read_resource("hcai://protocol")
            assert "0.1-rc.4-candidate" in resource.contents[0].text
            for path in (Path(__file__).resolve().parents[1]/"examples/rc4").glob("*.json"):
                data=json.loads(path.read_text())
                if path.stem=="pilot-synthetic":
                    pilot_result=await client.call_tool("validate_pilot_run",{"pilot":data})
                    assert not pilot_result.isError
                    continue
                actual=await client.call_tool("assess_engineering_commitment",{"assessment":data})
                assert not actual.isError
                assert json.loads(actual.content[0].text)==assess(Assessment.model_validate(data))
            prompt=await client.get_prompt("plan_handoff_review")
            assert prompt.messages

def test_stdio_roundtrip():
    asyncio.run(asyncio.wait_for(roundtrip(),timeout=30))
