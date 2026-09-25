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
                           "assess_engineering_commitment", "validate_pilot_run", "export_public_feedback",
                           "new_review_record", "review_next_step", "get_gate_guide", "assessment_report",
                           "get_review_criterion", "validate_study_review", "get_validation_targets"}
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
            assert "0.1-rc.4-candidate.6" in resource.contents[0].text
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
            empty=await client.call_tool("new_review_record",{"run_id":"NEW-STDIO","recorded_at":"2026-09-24T12:00:00Z","evaluator_kind":"human"})
            draft=json.loads(empty.content[0].text)
            assert draft["evidence"] == []
            guided=await client.call_tool("review_next_step",{"draft":draft})
            assert json.loads(guided.content[0].text)["decision_card"]["next_step"]["stage"] == "SCOPE"
            criterion=await client.call_tool("get_review_criterion",{"criterion_id":"HCAI-2.2"})
            assert json.loads(criterion.content[0].text)["found"]
            guide=await client.call_tool("get_gate_guide",{"gate_id":"G1_BASELINE"})
            assert "question" in json.loads(guide.content[0].text)
            data=json.loads((Path(__file__).resolve().parents[1]/"examples/rc4/low-risk-quick.json").read_text())
            report=await client.call_tool("assessment_report",{"assessment":data,"format":"html"})
            assert not report.isError and "<details><summary>" in report.content[0].text
            targets=await client.call_tool('get_validation_targets',{'assessment':data})
            assert not targets.isError
            payload=json.loads(targets.content[0].text)
            assert payload['requirement_digests']==data['workflow']['validations'][0]['tested_requirement_digests']
            assert not payload['evidence_verified']
            catalog=await client.read_resource("hcai://criteria")
            assert "HCAI-4.5" in catalog.contents[0].text
            from test_experience import study
            study_result=await client.call_tool("validate_study_review",{"review":study()})
            assert not study_result.isError and json.loads(study_result.content[0].text)["decision"] is None

def test_stdio_roundtrip():
    asyncio.run(asyncio.wait_for(roundtrip(),timeout=30))
