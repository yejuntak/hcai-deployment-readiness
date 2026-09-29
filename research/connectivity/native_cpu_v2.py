"""Bounded real native connectivity check; no scored research or API keys.

v1 remains in commit c8030ebf9941fe07eb4973890cc5dbaba3fb9ce8 and run
36517828246. v1 generated one malformed answer and stopped. v2 corrects
namespace initialization and includes the same generic JSON instruction as
the upstream JSON client. It never repairs, retries, or scores an answer.
"""
from __future__ import annotations
import hashlib
import importlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
from datetime import datetime, timezone

PIN = '3633d8dab149a9482a71b024418a49ae828cc941'
BLOB = '0d71d61798c4eafeb4d9a0610583aefa6ef96fb1'
MODEL = 'Qwen/Qwen3-0.6B'
REVISION = 'c1899de289a04d12100db370d81485cdf75e47ca'
FORMAT_SUFFIX = '\n\nReturn only a valid JSON object. Do not include markdown.'
CONTEXTS = [
    'A box contains a blue circle and a yellow triangle. Describe one visible shape in a short sentence.\n',
    'A notice says the library opens at 09:00 and closes at 17:00. Restate one time from this notice in a short sentence.\n',
]

def now():
    return datetime.now(timezone.utc).isoformat()

def sha(data):
    return hashlib.sha256(data).hexdigest()

def emit(kind, data):
    print('HARD_REAL_EXECUTION_JSON ' + json.dumps(
        {'kind': kind, 'recorded_at': now(), 'data': data},
        ensure_ascii=False, allow_nan=False), flush=True)

def main():
    root = Path(os.environ['NATIVE']).resolve()
    assert subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip() == PIN
    # Set every namespace contributor BEFORE the first import of matraix.
    paths = [str(root / p) for p in ('.', 'src', 'environment/runtime',
             'environment/agents', 'packages/playground/src', 'application/playground')]
    sys.path[:0] = paths
    os.chdir(root)
    from matraix.launch_env import required_pythonpath_entries
    assert paths == required_pythonpath_entries(root)
    from matraix.agents.persona.loader import load_persona
    from matraix.agents.persona.templating import (
        PERSONA_SYSTEM_TEMPLATE, render_persona_template, resolve_persona_template)
    from playground.user_sim.prompt import render_persona_block
    from playground.types import Persona
    from backend.service.survey_types import SurveyEvalConfig
    from playground.inprocess.survey_eval import InprocessSurveyEvalRunner
    from playground.survey_task_content import load_survey_task_content_for_task_path
    import yaml
    import torch
    import transformers
    from huggingface_hub import snapshot_download
    from transformers import AutoTokenizer, AutoModelForCausalLM

    module = importlib.import_module('playground.inprocess.survey_eval')
    module_path = root / 'packages/playground/src/playground/inprocess/survey_eval.py'
    assert Path(module.__file__).resolve() == module_path
    b = module_path.read_bytes()
    assert hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest() == BLOB
    persona_path = root / 'persona/datasets/matraix-persona-dev-sample/persona_0042.yaml'
    payload = yaml.safe_load(persona_path.read_text())
    persona = Persona(id=str(payload['persona_id']), name=str(payload['display_name']), source=str(payload['source']))
    # Direct loading propagates errors; never accept the upstream fallback silently.
    loaded = load_persona(str(persona_path))
    template = resolve_persona_template(loaded, None, PERSONA_SYSTEM_TEMPLATE)
    expected_persona = render_persona_template(template, loaded).strip()
    actual_persona = render_persona_block(persona, persona_yaml_path=str(persona_path)).strip()
    assert actual_persona == expected_persona and len(actual_persona) > 300
    assert '(a typical user)' not in actual_persona
    emit('PRE_INFERENCE_LOCK', {
        'adapter_version': 'native-cpu-v2', 'native_commit': PIN, 'native_module_blob': BLOB,
        'persona_sha256': sha(persona_path.read_bytes()), 'persona_template_sha256': sha(template.read_bytes()),
        'persona_prompt_sha256': sha(actual_persona.encode()), 'persona_fallback': False,
        'model_id': MODEL, 'model_revision': REVISION, 'engine': 'transformers CPU, injected native client',
        'torch': torch.__version__, 'transformers': transformers.__version__, 'python': platform.python_version(),
        'format_suffix': FORMAT_SUFFIX, 'max_new_tokens': 192, 'do_sample': False,
        'enable_thinking': False, 'max_calls': 2, 'paid_provider_calls': 0,
        'human_participants': 0, 'scope': 'CONNECTIVITY_ONLY_NOT_RESEARCH',
        'github_run_id': os.environ.get('GITHUB_RUN_ID'), 'github_sha': os.environ.get('GITHUB_SHA'),
        'previous_failed_run': 36517828246,
    })
    model_dir = Path(snapshot_download(MODEL, revision=REVISION, token=False,
        allow_patterns=['*.json', '*.safetensors', '*.jinja', '*.txt', 'LICENSE']))
    weights = {f.name: sha(f.read_bytes()) for f in model_dir.glob('*.safetensors')}
    assert weights.get('model.safetensors') == 'f47f71177f32bcd101b7573ec9171e6a57f4f4d31148d38e382306f42996874b'
    tokenizer = AutoTokenizer.from_pretrained(str(model_dir), local_files_only=True, trust_remote_code=False)
    torch.set_num_threads(4)
    torch.set_num_interop_threads(1)
    model = AutoModelForCausalLM.from_pretrained(str(model_dir), local_files_only=True,
        trust_remote_code=False, torch_dtype=torch.float32, attn_implementation='eager').eval()
    emit('MODEL_LOADED', {'weight_sha256': weights, 'device': str(model.device),
        'parameters': sum(v.numel() for v in model.parameters()),
        'tokenizer_files': {f.name: sha(f.read_bytes()) for f in model_dir.iterdir()
                            if f.is_file() and f.suffix in ('.json', '.jinja', '.txt')}})
    counters = {'generate': 0, 'native_started': 0, 'native_completed': 0}

    class CPUClient:
        def __init__(self, trial):
            self.trial, self.calls, self.raw = trial, 0, None

        def complete_json(self, system, user):
            if self.calls or counters['generate'] >= 2:
                raise RuntimeError('NO_AUTOMATIC_RETRY')
            assert system.strip() == actual_persona
            self.calls += 1
            messages = [{'role': 'system', 'content': system},
                        {'role': 'user', 'content': user + FORMAT_SUFFIX}]
            prompt = tokenizer.apply_chat_template(messages, tokenize=False,
                add_generation_prompt=True, enable_thinking=False)
            inputs = tokenizer(prompt, return_tensors='pt')
            n = inputs['input_ids'].shape[1]
            if n > 4096:
                raise RuntimeError('CONNECTIVITY_INPUT_BUDGET')
            emit('RAW_REQUEST', {'trial': self.trial, 'messages': messages,
                'native_user_prompt_sha256': sha(user.encode()),
                'rendered_prompt_sha256': sha(prompt.encode()), 'input_tokens': n})
            started = now()
            before = time.monotonic()
            counters['generate'] += 1
            with torch.inference_mode():
                output = model.generate(**inputs, max_new_tokens=192,
                    do_sample=False, pad_token_id=tokenizer.eos_token_id)
            ids = output[0, n:].tolist()
            text = tokenizer.decode(ids, skip_special_tokens=True)
            emit('RAW_MODEL_RESPONSE', {'trial': self.trial, 'started_at': started,
                'elapsed_seconds': time.monotonic() - before, 'generated_token_ids': ids,
                'raw_text': text, 'origin': 'ACTUAL_LOCAL_MODEL_GENERATION', 'native_fake_client': False})
            raw = json.loads(text)  # No markdown stripping, repair or default insertion.
            if not isinstance(raw, dict) or not isinstance(raw.get('answers'), list):
                raise ValueError('RAW_INVALID_ENVELOPE')
            entries = raw['answers']
            if (len(entries) != 1 or not isinstance(entries[0], dict)
                    or entries[0].get('questionId') != 'neutral_answer'
                    or not isinstance(entries[0].get('value'), str) or not entries[0]['value'].strip()):
                raise ValueError('RAW_MISSING_OR_INVALID_ANSWER')
            self.raw = raw
            return raw

    failure = None
    for i, context in enumerate(CONTEXTS, 1):
        try:
            task = root / 'application/tasks' / f'hard-neutral-{i:02d}-connectivity-v2'
            (task / 'input').mkdir(parents=True, exist_ok=False)
            instrument = {'askConfidence': False, 'askRationale': False,
                'id': f'hard_neutral_{i:02d}_connectivity_v2', 'questions': [{
                    'construct': 'connection_check_only', 'id': 'neutral_answer',
                    'prompt': 'Reply with one short sentence about the notice.',
                    'required': True, 'type': 'free_text'}],
                'schemaVersion': '1.0', 'title': 'Neutral connection check'}
            (task / 'task.toml').write_text('version = "1.0"\n[task]\nname = "neutral"\n[metadata]\ntype = "survey"\n[agent]\ntimeout_sec = 120.0\n[environment]\ndefinition = "application/shared-survey-form"\n')
            (task / 'instruction.md').write_text('Read the short notice. Answer the one question briefly. This is a connectivity check, not a scored research task.\n')
            (task / 'input/context.md').write_text(context)
            (task / 'input/questionnaire.yaml').write_text(json.dumps(instrument, sort_keys=True, separators=(',', ':')))
            os.environ['MATRIX_SURVEY_TASK_PATH'] = str(task)
            content = load_survey_task_content_for_task_path(str(task), repo_root=root)
            assert content is not None and content.instrument is not None
            emit('TASK_LOCK', {'trial': i, 'files': {str(f.relative_to(task)): sha(f.read_bytes()) for f in task.rglob('*') if f.is_file()}})
            client = CPUClient(i)
            counters['native_started'] += 1
            result = InprocessSurveyEvalRunner()(persona, content.instrument,
                config=SurveyEvalConfig(persona_model='local/Qwen3-0.6B'), created_at=now(),
                persona_yaml_path=str(persona_path), job_dir=None, client=client)
            assert client.calls == 1
            assert [a.value for a in result.answers] == [a['value'] for a in client.raw['answers']]
            counters['native_completed'] += 1
            emit('NATIVE_DERIVED_RESULT', {'trial': i, 'result': result.to_dict(),
                'raw_answer_values': client.raw['answers'], 'trajectory_is_derived_not_observed_behavior': True})
        except Exception as error:
            failure = {'trial': i, 'type': type(error).__name__, 'message': str(error)}
            emit('CONNECTIVITY_FAILURE', failure)
            break
    emit('TERMINAL', {'status': 'TWO_REAL_NATIVE_NEUTRAL_CALLS_RECORDED' if failure is None else 'CONNECTION_FORMAT_OR_RUNTIME_FAILED',
        'actual_model_generate_calls': counters['generate'], 'native_runner_calls': counters['native_started'],
        'native_completed': counters['native_completed'], 'human_participants': 0,
        'paid_model_api_calls': 0, 'research_sessions': 0, 'human_equivalence': 'NOT_ESTABLISHED',
        'stage04c_modified': False, 'stage04c_imported': False, 'failure': failure})
    return 0 if failure is None else 1

if __name__ == '__main__':
    raise SystemExit(main())
