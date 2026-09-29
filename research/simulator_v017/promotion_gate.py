"""Fail-closed promotion gate from frozen simulator qualification to the formal 576-session plan.

Passing this gate means operational eligibility for a bounded synthetic development run.
It never establishes representativeness, human validity, or human equivalence.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

EXPECTED = {
  "qualification_cases_sha256":"6c55610b1b3ab9f6e1799ab9d9fd22edbcfa14f99fb89e7192f1aa133c4c97f0",
  "protocol_sha256":"5d40c01356e82981de5a88d4e3c5119f5468be263064488e644e8da19a024260",
  "schema_sha256":"7bba24ee306528d32b86ba08b7e5d37bb7b0b378dd27b124ccc4a1bc578fd6d9",
  "instruction_sha256":"aee25839a92f58cc71bf1324b12bd593e4779d2342d2d9f379815c185011f933",
  "model":"Qwen/Qwen3-14B-GGUF",
  "model_revision":"530227a7d994db8eca5ab5ced2fb692b614357fd",
  "weight_sha256":"500a8806e85ee9c83f3ae08420295592451379b4f8cf2d0f41c15dffeb6b81f0",
  "runtime":"llama.cpp b11146",
  "expected_model_alias":"research-sim-qwen3-14b-q4",
  "native_commit":"3633d8dab149a9482a71b024418a49ae828cc941",
  "qualification_cases":16,
  "persona_slots":6
}

def load(p): return json.loads(Path(p).read_text())
def canon(x): return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
def sha(x): return hashlib.sha256(x).hexdigest()

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument("--qualification-root",required=True)
 ap.add_argument("--persona-receipt",required=True)
 ap.add_argument("--out",required=True)
 a=ap.parse_args()
 root=Path(a.qualification_root)
 files=sorted(root.glob("**/qualification-shard.json"))
 reasons=[]; rows=[]; plans=[]
 if len(files)!=4: reasons.append(f"EXPECTED_4_SHARDS_GOT_{len(files)}")
 for f in files:
  d=load(f)
  if d.get("shard") not in (1,2,3,4): reasons.append(f"BAD_SHARD:{f}")
  if d.get("planned")!=4 or d.get("completed")!=4: reasons.append(f"INCOMPLETE_SHARD:{f}")
  if d.get("human_participants")!=0 or d.get("human_equivalence")!="NOT_ESTABLISHED": reasons.append(f"BAD_HUMAN_BOUNDARY:{f}")
  rows.extend(d.get("rows",[]))
  pf=f.parent/"pre-inference-plan.json"
  if not pf.is_file(): reasons.append(f"MISSING_PLAN:{f}")
  else: plans.append(load(pf))
 if len(rows)!=EXPECTED["qualification_cases"]: reasons.append(f"EXPECTED_16_ROWS_GOT_{len(rows)}")
 ids=[r.get("case_id") for r in rows]
 if len(set(ids))!=len(ids): reasons.append("DUPLICATE_CASE_IDS")
 for r in rows:
  result=r.get("result",{}); score=r.get("score",{})
  if result.get("status")!="valid_response": reasons.append(f"INVALID_RESPONSE:{r.get('case_id')}")
  if result.get("origin")!="ACTUAL_QUANTIZED_MODEL_INFERENCE": reasons.append(f"BAD_ORIGIN:{r.get('case_id')}")
  if result.get("model")!=EXPECTED["expected_model_alias"]: reasons.append(f"MODEL_ALIAS:{r.get('case_id')}")
  if result.get("human_participants")!=0 or result.get("human_equivalence")!="NOT_ESTABLISHED": reasons.append(f"HUMAN_BOUNDARY:{r.get('case_id')}")
  response=result.get("response") or {}
  if response.get("claims_human_validation") is not False: reasons.append(f"FABRICATED_HUMAN_CLAIM:{r.get('case_id')}")
  checks=score.get("checks") or {}
  if score.get("eligible") is not True or not checks or not all(v is True for v in checks.values()):
   reasons.append(f"QUALIFICATION_FAILURE:{r.get('case_id')}")
 for p in plans:
  checks={
   "cases_sha256":EXPECTED["qualification_cases_sha256"],
   "protocol_sha256":EXPECTED["protocol_sha256"],
   "schema_sha256":EXPECTED["schema_sha256"],
   "instruction_sha256":EXPECTED["instruction_sha256"],
   "model":EXPECTED["model"],
   "revision":EXPECTED["model_revision"],
   "weight_sha256":EXPECTED["weight_sha256"],
   "runtime":EXPECTED["runtime"],
  }
  for k,v in checks.items():
   if p.get(k)!=v: reasons.append(f"PLAN_IDENTITY_MISMATCH:{k}")
  if p.get("retries")!=0: reasons.append("RETRIES_NOT_ZERO")
 persona=load(a.persona_receipt)
 if persona.get("native_commit")!=EXPECTED["native_commit"]: reasons.append("PERSONA_NATIVE_COMMIT")
 binds=persona.get("bindings") or []
 if len(binds)!=EXPECTED["persona_slots"]: reasons.append(f"PERSONA_COUNT:{len(binds)}")
 if len({x.get("persona_id") for x in binds})!=len(binds): reasons.append("DUPLICATE_PERSONA")
 for b in binds:
  if b.get("fallback") is not False or not b.get("sha256") or not b.get("rendered_sha256"): reasons.append(f"BAD_PERSONA_BINDING:{b.get('slot')}")
 receipt={
  "schema_version":"hard-simulator-promotion/1.0",
  "qualification":"PASS" if not reasons else "FAIL",
  "formal_simulation_eligible":not reasons,
  "reason_codes":sorted(set(reasons)),
  "qualification_case_count":len(rows),
  "qualification_case_ids":sorted(ids),
  "qualification_rows_sha256":sha(canon(rows)),
  "persona_receipt_sha256":sha(canon(persona)),
  "model_identity":{k:EXPECTED[k] for k in ("model","model_revision","weight_sha256","runtime")},
  "scope":"BOUNDED_SYNTHETIC_DEVELOPMENT_ONLY",
  "human_equivalence":"NOT_ESTABLISHED",
  "human_participants":0,
  "prohibited_claims":["human-equivalent research","representative human population","validated usability effect","independent generalization"],
  "next_if_pass":"Seal a new version of the predeclared 576-session plan; do not rewrite historical qualification or Stage04B.",
  "next_if_fail":"Do not launch the 576 sessions. Freeze failure and change candidate/model architecture only in a new version."
 }
 out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
 print(json.dumps(receipt,sort_keys=True))
 return 0 if not reasons else 2
if __name__=="__main__": raise SystemExit(main())
