"""Verify frozen practitioner-like persona binding with pinned MatrAIx native loader.

No model inference. This only proves exact bytes load and render without fallback.
"""
from __future__ import annotations
import hashlib, json, os, sys
from pathlib import Path

PIN="3633d8dab149a9482a71b024418a49ae828cc941"
BINDINGS={
 "P01":("0174","d9d013ae541b7624fa0cbbcaf9b3b5f499f3602980652bfe45ddc557bc8964ea"),
 "P02":("0098","46b450ea7a3052463aed61cd25037002ffd357a2598a3f1c7ba3e940b7fb5f90"),
 "P03":("0025","0225fcf828fb490bbb42075b52848d3e81b356b99350081dd74786acf671dfae"),
 "P04":("0088","54f0dc12fb4230c1371cfe93d541ea75bdb6afac535d97bf79f8b490a9517adf"),
 "P05":("0157","d1db5d05d309bf378c2d6f69e93525dff311b632f7ac599f8bdc2e0e88d984a5"),
 "P06":("0095","ad66b8ac1e97d8b52e127389531bf03cb54ed427fa488dc9fe63472a7748d660"),
}
root=Path(os.environ["NATIVE"]).resolve()
paths=[str(root/p) for p in (".","src","environment/runtime","environment/agents","packages/playground/src","application/playground")]
sys.path[:0]=paths
os.chdir(root)
from matraix.agents.persona.loader import load_persona
from matraix.agents.persona.templating import PERSONA_SYSTEM_TEMPLATE, render_persona_template, resolve_persona_template

out=[]
for slot,(pid,expected_sha) in BINDINGS.items():
    p=root/"persona/datasets/matraix-persona-dev-sample"/f"persona_{pid}.yaml"
    raw=p.read_bytes()
    actual=hashlib.sha256(raw).hexdigest()
    assert actual==expected_sha,(slot,actual,expected_sha)
    loaded=load_persona(str(p))
    template=resolve_persona_template(loaded,None,PERSONA_SYSTEM_TEMPLATE)
    rendered=render_persona_template(template,loaded).strip()
    assert rendered and "(a typical user)" not in rendered
    out.append({
      "slot":slot,"persona_id":pid,"file":p.name,"sha256":actual,
      "rendered_sha256":hashlib.sha256(rendered.encode()).hexdigest(),
      "rendered_bytes":len(rendered.encode()),"fallback":False
    })
Path(os.environ["OUT"]).write_text(json.dumps({
  "native_commit":PIN,"model_calls":0,"human_participants":0,
  "human_equivalence":"NOT_ESTABLISHED","bindings":out
},sort_keys=True,indent=2)+"\n")
print(json.dumps(out,sort_keys=True))
