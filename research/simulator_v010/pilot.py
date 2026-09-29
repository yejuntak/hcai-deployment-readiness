"""Reserved, bounded pilot runner. Receives actor-only precomputed requests.

Never imports evaluator keys. The model has no filesystem or tool access.
This adapter sends exact planned HTTP bytes without changing model parameters.
"""
from pathlib import Path
import argparse,json,sys,time,urllib.request,hashlib
import recorder as runner
import simulator as s

class ExactTransport:
 origin='MODEL_HTTP_NOT_NATIVE_MATRAIX'
 def __init__(self,raw_root):self.raw_root=Path(raw_root);self.calls=0;self.deadline=time.monotonic()+1100
 def call(self,request,trial):
  tid=trial['trial_id'];d=self.raw_root/tid;d.mkdir(parents=True,exist_ok=False)
  req=urllib.request.Request('http://127.0.0.1:8765/v1/chat/completions',data=s.canonical(request),headers={'Content-Type':'application/json'},method='POST')
  self.calls+=1;s.write_json(d/'attempt.json',{'at':s.now(),'request_sha256':s.sha(s.canonical(request)),'actual_http_attempt':self.calls})
  class NoRedirect(urllib.request.HTTPRedirectHandler):
   def redirect_request(self,*a,**kw):raise runner.Blocked('REDIRECT_REJECTED')
  try:
   remaining=self.deadline-time.monotonic()
   if remaining<=1:raise TimeoutError('CAMPAIGN_TIME_RESERVE')
   with urllib.request.build_opener(urllib.request.ProxyHandler({}),NoRedirect()).open(req,timeout=min(240,remaining)) as r:b=r.read(2000001)
   (d/'provider.raw.json').write_bytes(b)
   if len(b)>2000000:raise runner.Blocked('RESPONSE_SIZE_LIMIT')
   env=s.strict_json(b)
   if env.get('model')!='research-sim-4b-q4':raise runner.Blocked('MODEL_ALIAS_CHANGED')
   choices=env.get('choices')
   if not isinstance(choices,list) or len(choices)!=1:raise runner.Blocked('CHOICES_CHANGED')
   text=choices[0]['message']['content']
   (d/'model.raw.txt').write_text(text)
   if choices[0]['finish_reason']!='stop':raise runner.Blocked('OUTPUT_TRUNCATION')
   return {'raw_envelope':env,'response_text':text,'observed_model':env['model'],'usage':env.get('usage'),
    'native_matraix':False,'provider_revision_verification':'OPERATOR_CHECKED_WEIGHT_SHA256'}
  except Exception as e:
   s.write_json(d/'failure.json',{'type':type(e).__name__,'message':str(e)[:250],'at':s.now()});raise

def main():
 a=argparse.ArgumentParser();a.add_argument('--inputs',required=True);a.add_argument('--out',required=True);v=a.parse_args()
 inputs=Path(v.inputs);out=Path(v.out);out.mkdir(parents=True,exist_ok=False)
 actor=s.strict_json((inputs/'actor-inputs.json').read_bytes());reservation=s.strict_json((inputs/'reservation.json').read_bytes());cfg=s.strict_json((inputs/'config.json').read_bytes())
 expected=s.strict_json((inputs/'input-files.sha256.json').read_bytes())
 for p,h in expected.items():
  path=(inputs/p).resolve()
  if not path.is_relative_to(inputs.resolve()) or s.sha(path.read_bytes())!=h:raise ValueError('INPUT_MANIFEST_DRIFT')
 if s.sha((inputs/'config.json').read_bytes())!=reservation['config_digest'].split(':')[1]:raise ValueError('CONFIG_NOT_RESERVED')
 from datetime import datetime,timezone
 if datetime.fromisoformat(reservation['reserved_at'])>datetime.now(timezone.utc):raise ValueError('RESERVATION_FROM_FUTURE')
 s.write_json(out/'execution-context.json',{'reserved':reservation,'actual_started_at':s.now(),'origin':'MODEL_HTTP_NOT_NATIVE_MATRAIX','model_weights_sha256':s.WEIGHT_SHA256,'post_outcome_adaptation':False})
 transport=ExactTransport(out/'provider-raw')
 def factory(t):
  row=actor['requests'][t['trial_id']]
  return row['case'],row['request']
 report=runner.run_sessions(actor['trials'],factory,transport,out/'bundle',cfg['budget'],reservation['config_digest'],response_schema=s.strict_json((inputs/'response.schema.json').read_bytes()))
 runner.audit_journal(out/'bundle')
 s.write_json(out/'actual-calls.json',{'provider_call_count':transport.calls,'automatic_retries':0,'at':s.now(),'human_participants':0})
 # Record true duplicate app submissions without another inference request.
 # These are in-memory simulator state operations, not production product writes.
 behavior=s.strict_json((inputs/'behavior-plan.json').read_bytes());submissions=[]
 for row in report['rows']:
  policy=behavior[row['trial_id']];store=s.SubmissionStore();one=store.submit(row['trial_id'],row);events=[one]
  if policy['behavior_profile']['repeat_submit'] or policy['chaos']=='duplicate_submit':events.append(store.submit(row['trial_id'],row))
  submissions.append({'trial_id':row['trial_id'],'events':events,'context':'SIMULATOR_IN_MEMORY_STORE_NOT_PRODUCTION'})
 s.write_json(out/'submission-events.json',submissions)
 print('PILOT_TERMINAL '+s.canonical({'assigned':report['assigned'],'attempts':transport.calls,'terminal_counts':report['terminal_counts'],'human_participants':0,'human_equivalence':'NOT_ESTABLISHED'}).decode(),flush=True)
 return 0
if __name__=='__main__':raise SystemExit(main())
