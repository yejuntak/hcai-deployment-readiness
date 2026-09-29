"""Explicitly instructed synthetic decision instrument qualification.

Twelve exposed regression cases and four new transfer cases, all preregistered
for this revision. This is development qualification, not hidden validation.
"""
import argparse
from pathlib import Path
import simulator as s
import qualify as old
import qualification_base as base

def make_cases():
 cases=base.make_cases()
 extra=[
 ('Reviewer comparison reference','not_applicable','independent_evaluation','Compare two reviewer conditions and report measured reviewer performance.',
  'This comparison requires a frozen independent reference before reviewers answer. A training answer key produced after seeing their answers is not eligible.',
  'Reviewer answers are recorded, but no frozen independent reference exists. No reference was evaluated and no protocol execution failure is asserted.',
  'insufficient_evidence','request_evidence'),
 ('Resolved historic defect','implementation_review','artifact_review','Review the current revision B4 only under its stated evidence contract.',
  'The sole requirement is preserving accents in exported names. A code record and test on exactly current revision B4 are required.',
  'Revision B3 previously lost accents. B4 has a changed code record intended to fix that defect but no B4 execution was performed. No observed failure on B4 is available.',
  'insufficient_evidence','request_evidence'),
 ('Defensible scope exclusion','prototype_handoff','artifact_review','Review prototype handoff for the current one-path contract, not future planned features.',
  'The current contract contains only password reset and requires a specification and prototype walkthrough. A proposed future color theme is explicitly excluded with a rationale and has no dependency on password reset.',
  'Reset is specified and its retained walkthrough conforms for revision P9. An obsolete future-theme mockup failed a color check, but it is not part of the current scope or dependencies.',
  'sufficient_for_declared_scope','continue_declared_review'),
 ('Concurrent operation review','runtime_release_review','artifact_review','Inspect both concurrency and recovery requirements on current revision Z5; no release authority is requested.',
  'The two in-scope requirements are single-application of each update and recovery after interruption. Each needs a retained runtime test on Z5.',
  'A retained Z5 concurrency test applies one update twice, contrary to its requirement. Recovery is specified but has never been executed on Z5. Both requirements remain in scope.',
  'mixed_failure_and_missing','revise')]
 for title,stage,route,request,contract,evidence,state,rec in extra:
  case={'schema_version':'1.0','case_id':'K'+s.sha((title+'qualification-v5-defined').encode())[:12],
   'instructions':'Constructed qualification vignette. Use only the supplied records; absent evidence must not be invented.',
   'title':title,'request':request,'artifact_stage':stage,'records':[
    {'id':'R01','title':'Declared review contract','text':contract},
    {'id':'R02','title':'Available evidence','text':evidence},
    {'id':'R03','title':'Origin and authority','text':'These are authored synthetic records, not a human participant study. No owner or deployment authorization has been granted.'}]}
  cases.append({'case':case,'expected':{'review_route':route,'evidence_state':state,'recommendation':rec}})
 return cases

def main():
 a=argparse.ArgumentParser();a.add_argument('--protocol',required=True);a.add_argument('--out',required=True);a.add_argument('--native');a.add_argument('--shard',type=int,required=True);v=a.parse_args()
 if v.shard not in (1,2,3,4):raise ValueError('UNKNOWN_SHARD')
 out=Path(v.out);out.mkdir(parents=True,exist_ok=False);material=Path(v.protocol).read_text()
 if s.sha(material.encode())!=s.PROTOCOL_SHA256:raise ValueError('PROTOCOL_DRIFT')
 cases=make_cases();s.write_json(out/'cases.controller.json',cases)
 plan={'version':'operational-qualification-v5-defined','model':s.MODEL,'revision':s.REVISION,'weight_sha256':s.WEIGHT_SHA256,
  'runtime':'llama.cpp b11146','protocol_sha256':s.PROTOCOL_SHA256,'cases_sha256':s.sha(s.canonical(cases)),
  'floor':'16/16 categorical, source-reference, no-fabricated-human and no-authority-overreach checks; NOT human validation',
  'max_calls':18,'shards':4,'call_timeout_seconds':240,'retries':0,
  'grammar':'same allowed values and bounded prose; explicit field definitions in the response instrument',
  'instruction_sha256':s.sha(s.INSTRUCTION.encode()),'schema_sha256':s.sha(s.canonical(s.schema())),
  'prior_results_preserved':True,'development_adaptation':'Field definitions added after observed ambiguity; these are regression tests, not held-out evidence.',
  'selection':'12 exposed cases and 4 new authored transfer cases before v013 inference; no formal pilot outcomes inspected',
  'estimand_boundary':'Judgments under shared field definitions; not unguided human understanding of protocol wording.'}
 s.write_json(out/'pre-inference-plan.json',plan);client=s.ModelClient();rows=[]
 if v.shard==1:
  old.personas(v.native,out)
  for i,text in enumerate(['A green square is beside a red circle. Restate one shape.','A room opens at 08:00 and closes at 16:00. Restate one time.']):
   case={'schema_version':'1.0','case_id':'K'+str(i+1)*12,'instructions':'Neutral connectivity only. A review judgment is not requested.','title':'Neutral note','request':text,'artifact_stage':'not_applicable','records':[{'id':'R01','title':'Note','text':text}]}
   result=client.call(s.request_for(case,'',seed=20260928+i),out/f'smoke-{i+1}')
   print('SIM_NEUTRAL '+s.canonical({'id':i+1,'status':result['status']}).decode(),flush=True)
   if result['status']=='transport_error':raise RuntimeError('NEUTRAL_TRANSPORT_FAILURE')
 for index in range((v.shard-1)*4,v.shard*4):
  item=cases[index];result=s.session(client,item['case'],material,s.PROFILES[0],20261000+index,out/f'qualification-{index+1}',persona='')
  score=old.evaluate(result,item['case'],item['expected']);row={'case_id':item['case']['case_id'],'score':score,'result':result};rows.append(row)
  print('SIM_QUAL_RESULT '+s.canonical(row).decode(),flush=True)
  if result['status']=='transport_error':break
 summary={'planned':4,'completed':len(rows),'model_calls':client.calls,'shard':v.shard,'shard_passed':len(rows)==4 and all(x['score']['eligible'] for x in rows),
  'rows':rows,'human_participants':0,'human_equivalence':'NOT_ESTABLISHED','use_scope':'BOUNDED_INSTRUCTED_SYNTHETIC_DEVELOPMENT',
  'qualification_does_not_establish_representativeness':True}
 s.write_json(out/'qualification-shard.json',summary);print('SIM_QUAL_TERMINAL '+s.canonical(summary).decode(),flush=True)
 return 0
if __name__=='__main__':raise SystemExit(main())
