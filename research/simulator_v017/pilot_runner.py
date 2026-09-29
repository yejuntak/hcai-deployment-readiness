"""Run the predeclared 24-session HARD pipeline pilot.

This is an integrity/runtime pilot, not an A/B efficacy analysis.
Evaluator keys are intentionally absent from this process.
"""
from __future__ import annotations
import argparse, hashlib, json, os, re, sys
from pathlib import Path

import simulator as sim

ARM_A_SHA="5d40c01356e82981de5a88d4e3c5119f5468be263064488e644e8da19a024260"
ARM_B_SHA="32757344f7152fabe3a6e638e889a7e8c22ff8fad5630e262aae9f8e3c255829"
ACTOR_SHA="6d0ee9f701e4197556a61c3bd05a763cfc030508f200e07a51a0d27316752c02"
PLAN_SHA="90bda8d93763b2de76449c8efc13119db6f7bde11cc94e5228d2e6d73272ecaf"
PIN="3633d8dab149a9482a71b024418a49ae828cc941"
SLOT_BINDING={
 "P01":("0162","b0fe41c35355091592b13ed3228b480b39e66bff15424bd1d4d4ba8fb88137d0"),
 "P02":("0054","7d64b99e18ea33b31d629aa4d60c7a274ec6c5b2d78ce3035057701fa2119cad"),
 "P03":("0177","1591feea9a3c16e0ba1d4e27d8dd0f48c5b40580bcaf33dfd3c2e1df70e06503"),
 "P04":("0163","bac86a27c50b7233995606d870bcca085f3353c4ad548648e4078728eee78a82"),
 "P05":("0158","d157d6245671a4ab390032cac86ed684c2a5be9512c972b368da31ce260ba54c"),
 "P06":("0094","ca8253939b5b6dcaa26af24986a0a47c0ca3c8341534ed6a1a4d036ec9ce32ae"),
}
REORDER=[1,2,4,6,0,3,5,7]

def sha_bytes(b): return hashlib.sha256(b).hexdigest()
def load_json(p): return json.loads(Path(p).read_text())
def write_json(p,x):
 p=Path(p); p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(x,sort_keys=True,indent=2,ensure_ascii=False)+"\n")

def materials(protocol_bytes):
 if sha_bytes(protocol_bytes)!=ARM_A_SHA: raise ValueError("ARM_A_IDENTITY")
 text=protocol_bytes.decode()
 m=list(re.finditer(r"(?m)^## ",text))
 if len(m)!=8: raise ValueError(f"EXPECTED_8_H2_GOT_{len(m)}")
 pre=text[:m[0].start()]
 secs=[]
 for i,x in enumerate(m):
  end=m[i+1].start() if i+1<len(m) else len(text)
  secs.append(text[x.start():end])
 b=(pre+"".join(secs[i] for i in REORDER)).encode()
 if len(b)!=len(protocol_bytes): raise ValueError("ARM_LENGTH")
 if sorted(sha_bytes(x.encode()) for x in secs)!=sorted(sha_bytes(secs[i].encode()) for i in REORDER): raise ValueError("SECTION_MULTISET")
 if sha_bytes(b)!=ARM_B_SHA: raise ValueError("ARM_B_IDENTITY")
 return {"A":protocol_bytes.decode(),"B":b.decode()}

def render_personas(native_root):
 root=Path(native_root).resolve()
 paths=[str(root/p) for p in (".","src","environment/runtime","environment/agents","packages/playground/src","application/playground")]
 sys.path[:0]=paths
 os.chdir(root)
 from matraix.agents.persona.loader import load_persona
 from matraix.agents.persona.templating import PERSONA_SYSTEM_TEMPLATE, render_persona_template, resolve_persona_template
 out={}
 for slot,(pid,expected) in SLOT_BINDING.items():
  p=root/"persona/datasets/matraix-persona-dev-sample"/f"persona_{pid}.yaml"
  raw=p.read_bytes()
  if sha_bytes(raw)!=expected: raise ValueError(f"PERSONA_BYTES:{slot}")
  loaded=load_persona(str(p))
  tmpl=resolve_persona_template(loaded,None,PERSONA_SYSTEM_TEMPLATE)
  rendered=render_persona_template(tmpl,loaded).strip()
  if not rendered or "(a typical user)" in rendered: raise ValueError(f"PERSONA_FALLBACK:{slot}")
  out[slot]={"persona_id":pid,"sha256":expected,"rendered":rendered,"rendered_sha256":sha_bytes(rendered.encode())}
 return out

def neutral_smokes(client,out_dir):
 fixtures=[
  {
   "schema_version":"1.0","case_id":"SMOKE00000001","title":"Neutral connectivity fixture 1",
   "instructions":"This is an unscored format/connectivity fixture. Do not claim human validation.",
   "request":"Return a bounded review judgment using the response schema; this fixture is excluded from research outcomes.",
   "artifact_stage":"not_applicable",
   "records":[{"id":"R01","title":"Fixture","text":"This fixture contains no real organization, user study, implementation, or deployment authority."}]
  },
  {
   "schema_version":"1.0","case_id":"SMOKE00000002","title":"Neutral connectivity fixture 2",
   "instructions":"This is an unscored format/connectivity fixture. Do not claim human validation.",
   "request":"Return a bounded review judgment using the response schema; this fixture is excluded from research outcomes.",
   "artifact_stage":"not_applicable",
   "records":[{"id":"R01","title":"Fixture","text":"No human participants or real operational evidence are present in this fixture."}]
  }
 ]
 rows=[]
 for i,c in enumerate(fixtures,1):
  req=sim.request_for(c,"Neutral execution smoke. No scientific claims are scored.",metadata={"smoke":True,"timing_is_human":False},seed=20260928+i)
  r=client.call(req,Path(out_dir)/f"smoke-{i}")
  rows.append({"id":c["case_id"],"status":r.get("status"),"claims_human_validation":(r.get("response") or {}).get("claims_human_validation"),"origin":r.get("origin")})
 return rows

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--actor",required=True)
 ap.add_argument("--plan",required=True)
 ap.add_argument("--protocol",required=True)
 ap.add_argument("--native",required=True)
 ap.add_argument("--shard",type=int,choices=[1,2,3,4],required=True)
 ap.add_argument("--out",required=True)
 ap.add_argument("--smoke",action="store_true")
 args=ap.parse_args()

 actor_b=Path(args.actor).read_bytes(); plan_b=Path(args.plan).read_bytes()
 if sha_bytes(actor_b)!=ACTOR_SHA: raise SystemExit("ACTOR_SHA_MISMATCH")
 if sha_bytes(plan_b)!=PLAN_SHA: raise SystemExit("PLAN_SHA_MISMATCH")
 actor=json.loads(actor_b); plan=json.loads(plan_b)
 if plan.get("sessions")!=24 or plan.get("retries")!=0: raise SystemExit("BAD_PLAN")
 if actor.get("pilot_session_count")!=24 or actor.get("semantic_outcomes_blinded_until_full_plan_lock") is not True: raise SystemExit("BAD_ACTOR_PLAN")

 mats=materials(Path(args.protocol).read_bytes())
 personas=render_personas(args.native)
 cases={c["case_id"]:c for c in actor["cases"]}
 trials=actor["trials"]
 if len(trials)!=24 or len(cases)!=12: raise SystemExit("BAD_COUNTS")

 # three lineages per shard; both paired arms stay in one shard
 lineage_nums={f"L{i:02d}" for i in range((args.shard-1)*3+1,args.shard*3+1)}
 mine=[t for t in trials if t["lineage_id"] in lineage_nums]
 if len(mine)!=6: raise SystemExit(f"EXPECTED_6_TRIALS_GOT_{len(mine)}")
 mine=sorted(mine,key=lambda x:(int(x["lineage_id"][1:]),x["within_pair_order"]))

 out=Path(args.out); out.mkdir(parents=True,exist_ok=False)
 client=sim.ModelClient(timeout=900)
 smoke_rows=neutral_smokes(client,out/"smoke") if args.smoke else []
 profile=next(p for p in sim.PROFILES if p["id"]=="full")
 rows=[]; consecutive_transport=0; stopped=False
 for idx,t in enumerate(mine):
  if stopped:
   rows.append({**t,"status":"not_launched","reason":"CONSECUTIVE_TRANSPORT_ERRORS"})
   continue
  case=cases[t["case_id"]]
  slot=t["persona_slot"]
  if slot not in personas or t["persona_id"]!=personas[slot]["persona_id"]: raise SystemExit(f"PERSONA_BINDING:{t['trial_id']}")
  trial_dir=out/"trials"/t["trial_id"]
  result=sim.session(client,case,mats[t["arm_id"]],profile,int(t["seed"]),trial_dir,persona=personas[slot]["rendered"],chaos="none")
  status=result.get("status")
  consecutive_transport=consecutive_transport+1 if status=="transport_error" else 0
  if consecutive_transport>=3: stopped=True
  row={
   **t,
   "status":status,
   "model_origin":result.get("origin"),
   "case_identity_valid":result.get("case_identity_valid"),
   "unseen_citations":result.get("unseen_citations"),
   "claims_human_validation":(result.get("response") or {}).get("claims_human_validation"),
   "material_sha256":ARM_A_SHA if t["arm_id"]=="A" else ARM_B_SHA,
   "persona_sha256":personas[slot]["sha256"],
   "persona_rendered_sha256":personas[slot]["rendered_sha256"],
   "response_present":result.get("response") is not None,
   "semantic_scored":False
  }
  rows.append(row)

 receipt={
  "schema_version":"hard-execution-pilot-shard/1.0",
  "shard":args.shard,
  "lineages":sorted(lineage_nums),
  "planned":6,"rows":rows,
  "smoke_rows":smoke_rows,
  "model_calls":client.calls,
  "retries":0,
  "semantic_scoring":"NOT_PERFORMED",
  "human_participants":0,
  "human_equivalence":"NOT_ESTABLISHED",
  "evidence_class":"SIMULATION_ONLY"
 }
 write_json(out/"pilot-shard.json",receipt)
 print(json.dumps(receipt,sort_keys=True))
 return 0

if __name__=="__main__": raise SystemExit(main())
