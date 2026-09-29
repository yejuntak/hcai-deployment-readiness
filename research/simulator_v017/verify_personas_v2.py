"""Verify v2 frozen maximin persona binding with pinned MatrAIx native loader.

No model inference. This proves exact bytes load and render without fallback.
Selection was outcome-blinded and excluded declared sensitive dimensions.
"""
from __future__ import annotations
import hashlib, json, os, sys
from pathlib import Path

PIN="3633d8dab149a9482a71b024418a49ae828cc941"
SELECTION_RUN=36568697079
BINDINGS={
 "P01":("0162","b0fe41c35355091592b13ed3228b480b39e66bff15424bd1d4d4ba8fb88137d0"),
 "P02":("0054","7d64b99e18ea33b31d629aa4d60c7a274ec6c5b2d78ce3035057701fa2119cad"),
 "P03":("0177","1591feea9a3c16e0ba1d4e27d8dd0f48c5b40580bcaf33dfd3c2e1df70e06503"),
 "P04":("0163","bac86a27c50b7233995606d870bcca085f3353c4ad548648e4078728eee78a82"),
 "P05":("0158","d157d6245671a4ab390032cac86ed684c2a5be9512c972b368da31ce260ba54c"),
 "P06":("0094","ca8253939b5b6dcaa26af24986a0a47c0ca3c8341534ed6a1a4d036ec9ce32ae"),
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
    raw=p.read_bytes(); actual=hashlib.sha256(raw).hexdigest()
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
receipt={
  "schema_version":"hard-persona-binding/2.0",
  "native_commit":PIN,
  "selection_workflow_run":SELECTION_RUN,
  "selection_method":"deterministic maximin categorical distance over declared non-sensitive behavioral/cognitive fields",
  "selection_outcome_blinded":True,
  "model_calls":0,"human_participants":0,
  "representativeness":"NOT_ESTABLISHED",
  "human_equivalence":"NOT_ESTABLISHED",
  "bindings":out
}
Path(os.environ["OUT"]).write_text(json.dumps(receipt,sort_keys=True,indent=2)+"\n")
print(json.dumps(receipt,sort_keys=True))
