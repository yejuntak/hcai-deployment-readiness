#!/usr/bin/env python3
"""Frozen generalization holdout for H.A.R.D. simulator qualification.

Full factorial over 3 review routes x 4 evidence states x 2 contexts = 24 cases.
No prior model outputs are inputs. Actor packets and controller keys are emitted
separately. This is an operational generalization gate, not human validation.
"""
from __future__ import annotations
import hashlib,json,argparse,pathlib,random
SEED=20260929
ROUTES=('artifact_review','engineering_commitment','independent_evaluation')
STATES=('sufficient_for_declared_scope','insufficient_evidence','demonstrated_failure','mixed_failure_and_missing')
CONTEXTS=(
 ('document_export','A document export preserves a pending annotation across reconnect.'),
 ('inventory_sync','An inventory sync preserves an accepted quantity across retry.'),
)
def cid(route,state,ctx): return 'H'+hashlib.sha256(f'{SEED}|{route}|{state}|{ctx}'.encode()).hexdigest()[:12]
def canon(x): return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def records(route,state,domain):
 base=[{'id':'R01','title':'Declared scope','text':f'This constructed case concerns {domain}. The declared review question and required evidence are limited to the named route. No production deployment authority is supplied.'}]
 if route=='artifact_review':
  base.append({'id':'R02','title':'Stage contract','text':'The artifact is at prototype handoff. A checkable requirement and retained walkthrough are required for the two named paths. Implementation and runtime evidence are outside this declared artifact-review stage.'})
  if state=='sufficient_for_declared_scope': base.append({'id':'R03','title':'Review evidence','text':'Both named paths are specified and the retained walkthrough records both matching the prototype requirement. No implementation or runtime claim is made.'})
  elif state=='insufficient_evidence': base.append({'id':'R03','title':'Review evidence','text':'Both paths are specified, but no retained walkthrough exists for one named path. No observed failure is reported.'})
  elif state=='demonstrated_failure': base.append({'id':'R03','title':'Review evidence','text':'Both paths are specified and walked through. One walkthrough records behavior contrary to the stated prototype requirement.'})
  else: base.append({'id':'R03','title':'Review evidence','text':'One named path is walked through and fails its stated requirement; the other named path has no retained walkthrough.'})
 elif route=='engineering_commitment':
  base.append({'id':'R02','title':'Engineering gate contract','text':'All required engineering-commitment gates must be supported for the bounded next engineering step. A demonstrated gate failure requires revision; missing required evidence remains insufficient. Owner authorization is separate.'})
  if state=='sufficient_for_declared_scope': base.append({'id':'R03','title':'Gate evidence','text':'The bounded baseline, affected need, failure/recovery path, executed validation, residual human work and owner/limits records are all retained and each required gate is recorded as passing. No deployment approval is supplied.'})
  elif state=='insufficient_evidence': base.append({'id':'R03','title':'Gate evidence','text':'No baseline measurement is retained for a required gate. No required gate is reported as failed.'})
  elif state=='demonstrated_failure': base.append({'id':'R03','title':'Gate evidence','text':'Executed validation for a required recovery path is retained and demonstrates failure against the requirement. Other required evidence is present.'})
  else: base.append({'id':'R03','title':'Gate evidence','text':'Executed validation demonstrates failure of one required recovery path, and a separate required baseline record is missing.'})
 else:
  base.append({'id':'R02','title':'Evaluation contract','text':'The request is only to measure reviewer performance against a frozen independent reference. This route grants no engineering or deployment permission. Required reference and response records must be available to compute the declared comparison.'})
  if state=='sufficient_for_declared_scope': base.append({'id':'R03','title':'Evaluation evidence','text':'A frozen independent reference and the reviewer response set are retained and version matched; the declared performance comparison can be computed. The records are synthetic, not human validation.'})
  elif state=='insufficient_evidence': base.append({'id':'R03','title':'Evaluation evidence','text':'Reviewer responses are retained but the required frozen independent reference is absent. No comparison result is claimed.'})
  elif state=='demonstrated_failure': base.append({'id':'R03','title':'Evaluation evidence','text':'The frozen independent reference and reviewer responses are retained; the executed comparison demonstrates the reviewer missed a required reference finding.'})
  else: base.append({'id':'R03','title':'Evaluation evidence','text':'The executed comparison demonstrates one missed reference finding, while a second required response record is absent and therefore cannot be evaluated.'})
 return base
def expected(route,state):
 if state=='sufficient_for_declared_scope':
  rec={'artifact_review':'continue_declared_review','engineering_commitment':'propose_engineering','independent_evaluation':'evaluate_performance'}[route]
 else:
  rec='request_evidence' if state=='insufficient_evidence' else 'revise'
 return {'review_route':route,'evidence_state':state,'recommendation':rec,
   'permission_claim':'engineering_recommendation' if route=='engineering_commitment' and state=='sufficient_for_declared_scope' else 'review_only',
   'claims_human_validation':False}
def build():
 actor=[];keys=[]
 for route in ROUTES:
  for state in STATES:
   for ctx,domain in CONTEXTS:
    case_id=cid(route,state,ctx)
    stage='not_applicable' if route!='artifact_review' else 'prototype_handoff'
    req={'artifact_review':'Decide the bounded next action for this prototype artifact review.',
         'engineering_commitment':'Decide whether the retained evidence supports the bounded next engineering commitment.',
         'independent_evaluation':'Decide the bounded next action for this performance-evaluation request.'}[route]
    actor.append({'schema_version':'1.0','case_id':case_id,'title':f'{ctx} {route} holdout','artifact_stage':stage,
      'instructions':'Constructed holdout case. Use only supplied records and protocol. Cite record IDs. Do not infer missing evidence or authority.',
      'request':req,'records':records(route,state,domain)})
    keys.append({'case_id':case_id,'route':route,'state':state,'context':ctx,'expected':expected(route,state)})
 random.Random(SEED).shuffle(actor)
 return {'schema_version':'hard-generalization-holdout-actor/1.0','seed':SEED,'cases':actor,'human_equivalence':'NOT_ESTABLISHED'}, {'schema_version':'hard-generalization-holdout-key/1.0','seed':SEED,'keys':keys,'human_equivalence':'NOT_ESTABLISHED'}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--actor',required=True);ap.add_argument('--keys',required=True);a=ap.parse_args()
 actor,keys=build();pathlib.Path(a.actor).write_text(json.dumps(actor,indent=2,sort_keys=True)+'\n');pathlib.Path(a.keys).write_text(json.dumps(keys,indent=2,sort_keys=True)+'\n')
 print(canon({'cases':len(actor['cases']),'unique':len({x['case_id'] for x in actor['cases']}),'routes':{r:sum(1 for x in keys['keys'] if x['route']==r) for r in ROUTES},'states':{s:sum(1 for x in keys['keys'] if x['state']==s) for s in STATES}}))
if __name__=='__main__':main()
