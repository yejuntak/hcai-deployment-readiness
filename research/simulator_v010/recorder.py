"""Minimal multiaxis-run/1.0 recorder; controller independently audits every event."""
import json,hashlib,time,os
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
from jsonschema import Draft202012Validator
from simulator import strict_json as load,canonical,schema
class Blocked(ValueError):pass
def digest(b):return 'sha256:'+hashlib.sha256(b).hexdigest()
def now():return datetime.now(timezone.utc).isoformat()
def write(p,obj):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(canonical(obj))
class Journal:
 def __init__(self,p):self.path=p;self.prev='GENESIS';self.seq=0
 def append(self,kind,data):
  d={'seq':self.seq+1,'at':now(),'kind':kind,'data':data,'prev':self.prev};d['hash']=digest(canonical(d))
  with self.path.open('ab') as f:f.write(canonical(d)+b'\n');f.flush();os.fsync(f.fileno())
  self.prev=d['hash'];self.seq+=1

def run_sessions(schedule,request_factory,transport,output,budget,manifest_digest,response_schema=None):
 output=Path(output);output.mkdir(parents=True,exist_ok=False)
 if len({x['trial_id'] for x in schedule})!=len(schedule) or len(schedule)!=budget['planned_sessions']:raise Blocked('ASSIGNMENT_COUNT')
 sc=response_schema or schema();validator=Draft202012Validator(sc)
 write(output/'run.json',{'version':'0.1.0-direct','origin':transport.origin,'manifest_digest':manifest_digest,'schedule':schedule,'budget':budget,'at':now(),'human_participants':0,'human_equivalence':'NOT_ESTABLISHED'})
 journal=Journal(output/'journal.jsonl');journal.append('RUN_RESERVED',{'planned':len(schedule),'origin':transport.origin})
 rows=[];errors=0;attempts=0;stop=None;start=time.monotonic()
 for t in schedule:
  row={**t,'origin':transport.origin,'status':'not_launched','reason':None,'response':None,'usage':None,'elapsed_seconds':None,'model_calls':None}
  if stop is None and time.monotonic()-start>budget['max_campaign_wall_seconds']:stop='WALL_BUDGET'
  if stop is None and attempts>=budget['max_total_attempts']:stop='REQUEST_BUDGET'
  if stop:row['reason']=stop;rows.append(row);journal.append('TRIAL_TERMINAL',row);continue
  try:
   observation,request=request_factory(t)
   if observation['case_id']!=t['case_id'] or not isinstance(observation['records'],list):raise Blocked('CASE_IDENTITY')
   if len(canonical(request))>budget['max_request_utf8_bytes']:raise Blocked('INPUT_TOO_LARGE')
  except Exception as e:
   stop='INPUT_CONTRACT_OR_DRIFT';row['reason']=type(e).__name__;rows.append(row);journal.append('TRIAL_TERMINAL',row);continue
  write(output/(t['trial_id']+'.request.json'),request)
  journal.append('ATTEMPT_RESERVED',{'trial_id':t['trial_id'],'request_sha256':digest(canonical(request))})
  attempts+=1;t0=time.monotonic()
  try:
   env=transport.call(request,t);write(output/(t['trial_id']+'.envelope.json'),env)
   text=env['response_text'];row['usage']=env.get('usage');row['raw_response_sha256']=digest(text.encode())
   try:
    parsed=load(text)
    if parsed=={'event':'abandon','case_id':observation['case_id']}:
     row['status']='abandoned';row['reason']='ACTOR_DECLINED'
    else:
     validator.validate(parsed)
     if parsed['case_id']!=t['case_id']:raise ValueError('WRONG_CASE')
     known={r['id'] for r in observation['records']}
     if not set(parsed['evidence_record_ids']).issubset(known):raise ValueError('UNKNOWN_REFERENCE')
     normalized=dict(parsed)
     for k,v in sc.get('properties',{}).items():
      if k not in normalized and 'default' in v:normalized[k]=v['default']
     row['response']=normalized;row['status']='valid_response'
   except Exception as e:row['status']='invalid_response';row['reason']=type(e).__name__
   errors=0
  except Blocked as e:row['status']='identity_error';row['reason']=str(e);stop='IDENTITY_OR_CONTRACT';errors+=1
  except Exception as e:
   row['status']='timeout' if isinstance(e,TimeoutError) else 'transport_error';row['reason']=type(e).__name__;errors+=1
  row['elapsed_seconds']=time.monotonic()-t0
  if errors>=budget['max_consecutive_transport_errors']:stop='CONSECUTIVE_TRANSPORT_ERRORS'
  rows.append(row);journal.append('TRIAL_TERMINAL',row)
 report={'schema_version':'multiaxis-run/1.0','origin':transport.origin,'assigned':len(schedule),'attempted_requests':attempts,'terminal_counts':dict(Counter(r['status'] for r in rows)),'rows':rows,'human_participants':0,'human_equivalence':'NOT_ESTABLISHED','native_matraix_execution':False,'model_calls':None,'model_call_count_note':'See retained actual HTTP attempts and provider responses. Timeout does not establish whether a provider finished.','scientific_status':'NOT_EVALUATED','automatic_promotion':False,'parent_harness_receipt':'NOT_IMPORTED','stop_reason':stop}
 write(output/'report.json',report);journal.append('RUN_FINISHED',{'report_sha256':digest(canonical(report))});return report

def audit_journal(path):
 path=Path(path);previous='GENESIS';terminal=[];finished=None
 for i,line in enumerate((path/'journal.jsonl').read_bytes().splitlines(),1):
  d=load(line);h=d.pop('hash')
  if d['seq']!=i or d['prev']!=previous or digest(canonical(d))!=h:raise Blocked('JOURNAL_TAMPERED')
  previous=h
  if d['kind']=='TRIAL_TERMINAL':terminal.append(d['data'])
  if d['kind']=='RUN_FINISHED':finished=d['data']['report_sha256']
 report=load((path/'report.json').read_bytes())
 if terminal!=report['rows'] or digest(canonical(report))!=finished:raise Blocked('REPORT_NOT_RECONCILED')
 return {'status':'COMPLETE','rows':len(terminal),'controller_full_audit_still_required':True}
