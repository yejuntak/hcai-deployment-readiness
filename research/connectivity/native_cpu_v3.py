"""Connectivity v3: one retained real response + one new CPU inference.

No scored research, answer repair, automatic retries, API inference key, or
model-weight uploads. Prior v1/v2 failures remain failures. A code fence is
transport-normalized without changing JSON values; strict_json stays false.
"""
import hashlib
import importlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
import urllib.request
import urllib.error
from urllib.parse import urlsplit

PIN='3633d8dab149a9482a71b024418a49ae828cc941'
BLOB='0d71d61798c4eafeb4d9a0610583aefa6ef96fb1'
MODEL='Qwen/Qwen3-0.6B'
REV='c1899de289a04d12100db370d81485cdf75e47ca'
PREVIOUS_JOB=109245078772
PREVIOUS_RUN=36518189247
SUFFIX='\n\nReturn only a valid JSON object. Do not include markdown.'
CONTEXTS=['A box contains a blue circle and a yellow triangle. Describe one visible shape in a short sentence.\n','A notice says the library opens at 09:00 and closes at 17:00. Restate one time from this notice in a short sentence.\n']

def now(): return datetime.now(timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def emit(k,d): print('HARD_REAL_EXECUTION_JSON '+json.dumps({'kind':k,'recorded_at':now(),'data':d},ensure_ascii=False,allow_nan=False),flush=True)

def decode(text):
    payload=text; start,end=0,len(text); strict=True
    if text.lstrip().startswith('```'):
        m=re.fullmatch(r'\s*```(?:json)?[ \t]*\r?\n(?P<body>[\s\S]*?)\r?\n```[ \t]*\s*',text)
        if not m: raise ValueError('AMBIGUOUS_OR_INCOMPLETE_FENCE')
        payload=m.group('body'); start,end=m.span('body'); strict=False
    def unique(pairs):
        obj={}
        for k,v in pairs:
            if k in obj: raise ValueError('DUPLICATE_KEY')
            obj[k]=v
        return obj
    obj=json.loads(payload,object_pairs_hook=unique,parse_constant=lambda s: (_ for _ in ()).throw(ValueError('NONFINITE_JSON')))
    if not isinstance(obj,dict): raise ValueError('OBJECT_REQUIRED')
    return obj,{'strict_json':strict,'transformation':'none' if strict else 'remove_outer_code_fence_only','raw_sha256':sha(text.encode()),'json_payload_sha256':sha(payload.encode()),'source_character_span':[start,end],'answer_repair':False}

def previous_records():
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self,*a,**k): return None
    url=f'https://api.github.com/repos/yejuntak/hcai-deployment-readiness/actions/jobs/{PREVIOUS_JOB}/logs'
    req=urllib.request.Request(url,headers={'Authorization':'Bearer '+os.environ['GH_LOG_READ_TOKEN'],'Accept':'application/vnd.github+json'})
    try:
        with urllib.request.build_opener(NoRedirect).open(req,timeout=30) as r: b=r.read(2000001)
    except urllib.error.HTTPError as e:
        if e.code not in (301,302,303,307,308): raise
        target=e.headers.get('Location',''); parsed=urlsplit(target)
        if parsed.scheme!='https' or parsed.username or parsed.password: raise ValueError('UNSAFE_LOG_REDIRECT')
        # Deliberately do not forward the GitHub authorization header.
        with urllib.request.urlopen(target,timeout=30) as r: b=r.read(2000001)
    if len(b)>2000000: raise ValueError('LOG_TOO_LARGE')
    records=[]
    for line in b.decode('utf-8-sig').splitlines():
        line=re.sub(r'^\d{4}-\d\d-\d\dT\S+\s+','',line).strip()
        if line.startswith('HARD_REAL_EXECUTION_JSON {'):
            records.append(json.loads(line[len('HARD_REAL_EXECUTION_JSON '):]))
    def one(kind):
        values=[r for r in records if r['kind']==kind]
        if len(values)!=1: raise ValueError('PREVIOUS_RECORD_COUNT:'+kind)
        return values[0]
    lock=one('PRE_INFERENCE_LOCK')['data']; model=one('MODEL_LOADED')['data']
    request=one('RAW_REQUEST')['data']; response=one('RAW_MODEL_RESPONSE'); terminal=one('TERMINAL')['data']
    assert lock['native_commit']==PIN and lock['native_module_blob']==BLOB
    assert lock['model_revision']==REV and lock['persona_fallback'] is False
    assert terminal['actual_model_generate_calls']==1 and terminal['native_completed']==0
    assert response['data']['native_fake_client'] is False
    assert sha(response['data']['raw_text'].encode())=='b6fd55ce1d96ed603c2be55a9c44c212fcf1ad2f7599e09020dbf05d2e3b20ee'
    emit('RETAINED_SOURCE',{'source_job':PREVIOUS_JOB,'source_run':PREVIOUS_RUN,'complete_job_log_sha256':sha(b),'previous_lock':lock,'previous_response':response,'previous_terminal':terminal,'new_inference':False})
    return lock,model,request,response['data']

def main():
    oldlock,oldmodel,oldrequest,oldresponse=previous_records()
    root=Path(os.environ['NATIVE']).resolve()
    assert subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()==PIN
    sys.path[:0]=[str(root/p) for p in ('.','src','environment/runtime','environment/agents','packages/playground/src','application/playground')]
    os.chdir(root)
    from matraix.agents.persona.loader import load_persona
    from matraix.agents.persona.templating import PERSONA_SYSTEM_TEMPLATE,render_persona_template,resolve_persona_template
    from playground.user_sim.prompt import render_persona_block
    from playground.types import Persona
    from backend.service.survey_types import SurveyEvalConfig
    from playground.inprocess.survey_eval import InprocessSurveyEvalRunner
    from playground.survey_task_content import load_survey_task_content_for_task_path
    import yaml,torch,transformers
    from huggingface_hub import snapshot_download
    from transformers import AutoTokenizer,AutoModelForCausalLM
    mod=importlib.import_module('playground.inprocess.survey_eval')
    fp=root/'packages/playground/src/playground/inprocess/survey_eval.py'; b=fp.read_bytes()
    assert Path(mod.__file__).resolve()==fp
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==BLOB
    pp=root/'persona/datasets/matraix-persona-dev-sample/persona_0042.yaml'; p=yaml.safe_load(pp.read_text())
    persona=Persona(id=str(p['persona_id']),name=str(p['display_name']),source=str(p['source']))
    loaded=load_persona(str(pp)); template=resolve_persona_template(loaded,None,PERSONA_SYSTEM_TEMPLATE)
    expected=render_persona_template(template,loaded).strip()
    assert render_persona_block(persona,persona_yaml_path=str(pp)).strip()==expected
    assert sha(expected.encode())==oldlock['persona_prompt_sha256']
    emit('PRE_INFERENCE_LOCK',{'adapter_version':'native-cpu-v3-lossless-transport','native_commit':PIN,'native_module_blob':BLOB,'model_id':MODEL,'model_revision':REV,'persona_sha256':sha(pp.read_bytes()),'persona_prompt_sha256':sha(expected.encode()),'max_new_tokens':192,'do_sample':False,'enable_thinking':False,'max_new_generate_calls':1,'replay_trial':1,'fresh_trial':2,'prior_source_run':PREVIOUS_RUN,'paid_model_api_calls':0,'scope':'CONNECTIVITY_ONLY_NOT_RESEARCH','github_run_id':os.environ['GITHUB_RUN_ID'],'github_sha':os.environ['GITHUB_SHA'],'torch':torch.__version__,'transformers':transformers.__version__})
    model_dir=Path(snapshot_download(MODEL,revision=REV,token=False,allow_patterns=['*.json','*.safetensors','*.jinja','*.txt','LICENSE']))
    weights={f.name:sha(f.read_bytes()) for f in model_dir.glob('*.safetensors')}
    assert weights==oldmodel['weight_sha256']
    tokenizer=AutoTokenizer.from_pretrained(str(model_dir),local_files_only=True,trust_remote_code=False)
    torch.set_num_threads(4); torch.set_num_interop_threads(1)
    model=AutoModelForCausalLM.from_pretrained(str(model_dir),local_files_only=True,trust_remote_code=False,torch_dtype=torch.float32,attn_implementation='eager').eval()
    emit('MODEL_LOADED',{'device':str(model.device),'weight_sha256':weights,'tokenizer_sha256':sha((model_dir/'tokenizer.json').read_bytes())})
    counts={'fresh':0,'replays':0,'completed':0}; formats=[]; failure=None
    class Client:
        def __init__(self,trial): self.trial=trial; self.called=False; self.raw=None
        def complete_json(self,system,user):
            if self.called: raise RuntimeError('NO_RETRY')
            self.called=True
            assert system.strip()==expected
            messages=[{'role':'system','content':system},{'role':'user','content':user+SUFFIX}]
            if self.trial==1:
                assert messages==oldrequest['messages'], 'REPLAY_INPUT_CHANGED'
                text=oldresponse['raw_text']; counts['replays']+=1
                emit('REPLAYED_MODEL_RESPONSE',{'trial':1,'source_job':PREVIOUS_JOB,'source_run':PREVIOUS_RUN,'raw_text':text,'raw_sha256':sha(text.encode()),'new_inference':False})
            else:
                if counts['fresh']: raise RuntimeError('NEW_CALL_CAP')
                prompt=tokenizer.apply_chat_template(messages,tokenize=False,add_generation_prompt=True,enable_thinking=False)
                inputs=tokenizer(prompt,return_tensors='pt'); n=inputs['input_ids'].shape[1]
                if n>4096: raise RuntimeError('INPUT_BUDGET')
                emit('RAW_REQUEST',{'trial':2,'messages':messages,'input_tokens':n,'rendered_prompt_sha256':sha(prompt.encode())})
                start=now(); before=time.monotonic(); counts['fresh']+=1
                with torch.inference_mode(): output=model.generate(**inputs,max_new_tokens=192,do_sample=False,pad_token_id=tokenizer.eos_token_id)
                ids=output[0,n:].tolist(); text=tokenizer.decode(ids,skip_special_tokens=True)
                emit('RAW_MODEL_RESPONSE',{'trial':2,'started_at':start,'elapsed_seconds':time.monotonic()-before,'generated_token_ids':ids,'raw_text':text,'origin':'ACTUAL_LOCAL_MODEL_GENERATION','native_fake_client':False})
            raw,audit=decode(text)
            entries=raw.get('answers')
            if not isinstance(entries,list) or len(entries)!=1 or not isinstance(entries[0],dict) or entries[0].get('questionId')!='neutral_answer' or not isinstance(entries[0].get('value'),str) or not entries[0]['value'].strip(): raise ValueError('INVALID_ENVELOPE_NO_DEFAULTS')
            self.raw=raw; formats.append(audit)
            emit('LOSSLESS_TRANSPORT_DECODE',{'trial':self.trial,'audit':audit,'decoded':raw})
            return raw
    for i,context in enumerate(CONTEXTS,1):
        try:
            task=root/'application/tasks'/f'hard-neutral-{i:02d}-connectivity-v2'
            (task/'input').mkdir(parents=True,exist_ok=False)
            instrument={'askConfidence':False,'askRationale':False,'id':f'hard_neutral_{i:02d}_connectivity_v2','questions':[{'construct':'connection_check_only','id':'neutral_answer','prompt':'Reply with one short sentence about the notice.','required':True,'type':'free_text'}],'schemaVersion':'1.0','title':'Neutral connection check'}
            (task/'task.toml').write_text('version = "1.0"\n[task]\nname = "neutral"\n[metadata]\ntype = "survey"\n[agent]\ntimeout_sec = 120.0\n[environment]\ndefinition = "application/shared-survey-form"\n')
            (task/'instruction.md').write_text('Read the short notice. Answer the one question briefly. This is a connectivity check, not a scored research task.\n')
            (task/'input/context.md').write_text(context)
            (task/'input/questionnaire.yaml').write_text(json.dumps(instrument,sort_keys=True,separators=(',',':')))
            os.environ['MATRIX_SURVEY_TASK_PATH']=str(task)
            content=load_survey_task_content_for_task_path(str(task),repo_root=root)
            client=Client(i)
            result=InprocessSurveyEvalRunner()(persona,content.instrument,config=SurveyEvalConfig(persona_model='local/Qwen3-0.6B'),created_at=now(),persona_yaml_path=str(pp),job_dir=None,client=client)
            assert [a.value for a in result.answers]==[a['value'] for a in client.raw['answers']]
            counts['completed']+=1
            emit('NATIVE_DERIVED_RESULT',{'trial':i,'new_inference':i==2,'raw_answer_values':client.raw['answers'],'result':result.to_dict(),'trajectory_is_derived_not_observed_behavior':True})
        except Exception as e:
            failure={'trial':i,'type':type(e).__name__,'message':str(e)}; emit('CONNECTIVITY_FAILURE',failure); break
    emit('TERMINAL',{'status':'ACTUAL_NATIVE_CONNECTIVITY_WITH_RECORDED_TRANSPORT_NORMALIZATION' if failure is None else 'FAILED','fresh_generate_calls':counts['fresh'],'replayed_prior_real_responses':counts['replays'],'native_completed':counts['completed'],'raw_format_violations':sum(not a['strict_json'] for a in formats),'strict_json_not_claimed':True,'research_sessions':0,'human_participants':0,'human_equivalence':'NOT_ESTABLISHED','paid_model_api_calls':0,'stage04c_modified':False,'stage04c_imported':False,'failure':failure})
    return int(failure is not None)

if __name__=='__main__': raise SystemExit(main())
