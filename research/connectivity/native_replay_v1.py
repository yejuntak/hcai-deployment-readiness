"""Replay two retained REAL model outputs through native MatrAIx; zero inference.

A separately versioned, opt-in transport adapter accepts an unambiguous single
answer object for a single-question instrument. Original schema violations and
all previous failed runs remain recorded. It cannot fill answers or use a key.
This checks interoperability, not model performance or human equivalence.
"""
from __future__ import annotations
import hashlib
import importlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from datetime import datetime, timezone
import urllib.request
import urllib.error
from urllib.parse import urlsplit

PIN = '3633d8dab149a9482a71b024418a49ae828cc941'
NATIVE_BLOB = '0d71d61798c4eafeb4d9a0610583aefa6ef96fb1'
JOBS = [(109245078772, 36518189247, 1), (109246172835, 36518547160, 2)]
RAW_HASHES = ['b6fd55ce1d96ed603c2be55a9c44c212fcf1ad2f7599e09020dbf05d2e3b20ee',
              'f6214f6bc15ff8f40f65f129be85d11061acc62f8f0146f422c053a0662a8c63']
CONTEXTS = ['A box contains a blue circle and a yellow triangle. Describe one visible shape in a short sentence.\n',
            'A notice says the library opens at 09:00 and closes at 17:00. Restate one time from this notice in a short sentence.\n']
SUFFIX = '\n\nReturn only a valid JSON object. Do not include markdown.'

def sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()

def emit(kind: str, data: dict) -> None:
    print('HARD_REPLAY_AUDIT_JSON ' + json.dumps({'kind': kind,
        'recorded_at': datetime.now(timezone.utc).isoformat(), 'data': data},
        ensure_ascii=False, allow_nan=False), flush=True)

def normalize(text: str, question_ids: list[str], *, allow_single_packet: bool = False):
    """Losslessly decode declared transports; never infer a missing question/value."""
    if not isinstance(text, str) or len(text.encode()) > 1048576:
        raise ValueError('RAW_TEXT_REQUIRED_WITHIN_BUDGET')
    if (not question_ids or any(not isinstance(q, str) or not q for q in question_ids)
            or len(set(question_ids)) != len(question_ids)):
        raise ValueError('INVALID_QUESTION_IDS')
    payload = text
    span = [0, len(text)]
    transformations = []
    if text.lstrip().startswith('```'):
        m = re.fullmatch(r'\s*```(?:json)?[ \t]*\r?\n(?P<body>[\s\S]*?)\r?\n```[ \t]*\s*', text)
        if not m:
            raise ValueError('AMBIGUOUS_FENCE')
        payload = m.group('body')
        span = list(m.span('body'))
        transformations.append('outer_code_fence_removed')
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('DUPLICATE_KEY')
            result[key] = value
        return result
    def nonfinite(value):
        raise ValueError('NONFINITE_JSON')
    obj = json.loads(payload, object_pairs_hook=unique, parse_constant=nonfinite)
    if not isinstance(obj, dict):
        raise ValueError('JSON_OBJECT_REQUIRED')
    original_shape = 'survey_envelope'
    wrapped = False
    if 'answers' not in obj:
        if not allow_single_packet or len(question_ids) != 1:
            raise ValueError('ANSWERS_ARRAY_REQUIRED')
        if (not {'questionId', 'value'} <= set(obj)
                or not set(obj) <= {'questionId', 'value', 'rationale', 'confidence'}):
            raise ValueError('AMBIGUOUS_SINGLE_PACKET')
        original_shape = 'single_answer_packet'
        obj = {'answers': [obj]}
        transformations.append('single_answer_packet_wrapped_without_value_changes')
        wrapped = True
    answers = obj['answers']
    if not isinstance(answers, list) or len(answers) != len(question_ids):
        raise ValueError('ANSWER_COUNT')
    ids = []
    for answer in answers:
        if (not isinstance(answer, dict) or 'questionId' not in answer or 'value' not in answer
                or not isinstance(answer['questionId'], str)
                or not isinstance(answer['value'], str) or not answer['value'].strip()):
            raise ValueError('MISSING_OR_INVALID_ANSWER_NO_DEFAULTS')
        ids.append(answer['questionId'])
    if len(set(ids)) != len(ids) or set(ids) != set(question_ids):
        raise ValueError('UNRESOLVED_OR_DUPLICATE_QUESTION')
    return obj, {'raw_sha256': sha(text.encode()), 'json_payload_sha256': sha(payload.encode()),
        'source_character_span': span, 'raw_strict_json': not bool(span != [0, len(text)]),
        'raw_envelope_valid': not wrapped, 'original_shape': original_shape,
        'transformations': transformations, 'answer_values_changed': False,
        'missing_answers_filled': False, 'raw_contract_promoted_to_pass': False}

def fetch_prior(job_id: int):
    """Read an authorized job log; never forward the GitHub token on redirect."""
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *args, **kwargs):
            return None
    url = f'https://api.github.com/repos/yejuntak/hcai-deployment-readiness/actions/jobs/{job_id}/logs'
    req = urllib.request.Request(url, headers={'Authorization': 'Bearer ' + os.environ['GH_LOG_READ_TOKEN'],
                                              'Accept': 'application/vnd.github+json'})
    try:
        with urllib.request.build_opener(NoRedirect).open(req, timeout=30) as r:
            data = r.read(2000001)
    except urllib.error.HTTPError as error:
        if error.code not in (301, 302, 303, 307, 308):
            raise
        target = error.headers.get('Location', '')
        parsed = urlsplit(target)
        if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password:
            raise ValueError('UNSAFE_LOG_REDIRECT')
        with urllib.request.urlopen(target, timeout=30) as r:
            data = r.read(2000001)
    if len(data) > 2000000:
        raise ValueError('LOG_BUDGET')
    records = []
    for line in data.decode('utf-8-sig').splitlines():
        line = re.sub(r'^\d{4}-\d\d-\d\dT\S+\s+', '', line).strip()
        if line.startswith('HARD_REAL_EXECUTION_JSON {'):
            records.append(json.loads(line[len('HARD_REAL_EXECUTION_JSON '):]))
    return records, sha(data)

def main() -> int:
    root = Path(os.environ['NATIVE']).resolve()
    assert subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip() == PIN
    sys.path[:0] = [str(root / p) for p in ('.', 'src', 'environment/runtime', 'environment/agents',
                                         'packages/playground/src', 'application/playground')]
    os.chdir(root)
    from matraix.agents.persona.loader import load_persona
    from matraix.agents.persona.templating import PERSONA_SYSTEM_TEMPLATE, resolve_persona_template, render_persona_template
    from playground.user_sim.prompt import render_persona_block
    from playground.types import Persona
    from backend.service.survey_types import SurveyEvalConfig
    from playground.inprocess.survey_eval import InprocessSurveyEvalRunner
    from playground.survey_task_content import load_survey_task_content_for_task_path
    import yaml
    module = importlib.import_module('playground.inprocess.survey_eval')
    mp = root / 'packages/playground/src/playground/inprocess/survey_eval.py'
    b = mp.read_bytes()
    assert Path(module.__file__).resolve() == mp
    assert hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest() == NATIVE_BLOB
    pp = root / 'persona/datasets/matraix-persona-dev-sample/persona_0042.yaml'
    p = yaml.safe_load(pp.read_text())
    persona = Persona(id=str(p['persona_id']), name=str(p['display_name']), source=str(p['source']))
    loaded = load_persona(str(pp))
    rendered = render_persona_template(resolve_persona_template(loaded, None, PERSONA_SYSTEM_TEMPLATE), loaded).strip()
    assert render_persona_block(persona, persona_yaml_path=str(pp)).strip() == rendered
    assert sha(rendered.encode()) == '7e574e7375debba321249a866762f455cb24b27a7470e39e6f6fa574671f8608'
    emit('REPLAY_POLICY_LOCK', {'adapter': 'lossless-transport-replay-v1', 'new_model_calls': 0,
        'native_commit': PIN, 'native_module_blob': NATIVE_BLOB, 'source_jobs': JOBS,
        'expected_raw_sha256': RAW_HASHES, 'allow_single_packet': True,
        'applies_to_future_study': False, 'prior_failures_preserved': True})
    completed = []
    for index, (job, run, trial) in enumerate(JOBS):
        records, loghash = fetch_prior(job)
        requests = [r['data'] for r in records if r['kind'] == 'RAW_REQUEST' and r['data'].get('trial') == trial]
        responses = [r['data'] for r in records if r['kind'] == 'RAW_MODEL_RESPONSE' and r['data'].get('trial') == trial]
        assert len(requests) == len(responses) == 1
        request, response = requests[0], responses[0]
        assert sha(response['raw_text'].encode()) == RAW_HASHES[index]
        assert response['origin'] == 'ACTUAL_LOCAL_MODEL_GENERATION' and response['native_fake_client'] is False
        task = root / 'application/tasks' / f'hard-neutral-{trial:02d}-connectivity-v2'
        (task / 'input').mkdir(parents=True, exist_ok=False)
        instrument = {'askConfidence': False, 'askRationale': False,
            'id': f'hard_neutral_{trial:02d}_connectivity_v2', 'questions': [{
                'construct': 'connection_check_only', 'id': 'neutral_answer',
                'prompt': 'Reply with one short sentence about the notice.', 'required': True, 'type': 'free_text'}],
            'schemaVersion': '1.0', 'title': 'Neutral connection check'}
        (task / 'task.toml').write_text('version = "1.0"\n[task]\nname = "neutral"\n[metadata]\ntype = "survey"\n[agent]\ntimeout_sec = 120.0\n[environment]\ndefinition = "application/shared-survey-form"\n')
        (task / 'instruction.md').write_text('Read the short notice. Answer the one question briefly. This is a connectivity check, not a scored research task.\n')
        (task / 'input/context.md').write_text(CONTEXTS[index])
        (task / 'input/questionnaire.yaml').write_text(json.dumps(instrument, sort_keys=True, separators=(',', ':')))
        os.environ['MATRIX_SURVEY_TASK_PATH'] = str(task)
        content = load_survey_task_content_for_task_path(str(task), repo_root=root)
        class ReplayClient:
            called = False
            raw = None
            audit = None
            def complete_json(self, system, user):
                if self.called:
                    raise ValueError('REPLAY_DUPLICATION')
                self.called = True
                assert [{'role': 'system', 'content': system}, {'role': 'user', 'content': user + SUFFIX}] == request['messages']
                self.raw, self.audit = normalize(response['raw_text'], ['neutral_answer'], allow_single_packet=True)
                return self.raw
        client = ReplayClient()
        result = InprocessSurveyEvalRunner()(persona, content.instrument,
            config=SurveyEvalConfig(persona_model='local/Qwen3-0.6B'),
            created_at=datetime.now(timezone.utc).isoformat(), persona_yaml_path=str(pp), job_dir=None, client=client)
        assert [a.value for a in result.answers] == [a['value'] for a in client.raw['answers']]
        evidence = {'trial': trial, 'source_job': job, 'source_run': run, 'full_log_sha256': loghash,
            'raw_response': response, 'audit': client.audit, 'native_answer_values': [a.value for a in result.answers],
            'new_inference': False, 'replay_completed': True, 'generated_trajectory_not_human_behavior': True}
        completed.append(evidence)
        emit('NATIVE_REPLAY_RESULT', evidence)
    emit('TERMINAL', {'status': 'TWO_PRIOR_REAL_RESPONSES_REPLAYED_LOSSLESSLY',
        'native_replays_completed': len(completed), 'fresh_model_calls': 0,
        'raw_strict_json_passes': 0, 'original_raw_contract_failures_preserved': True,
        'scored_research_sessions': 0, 'human_participants': 0, 'human_equivalence': 'NOT_ESTABLISHED',
        'original_stage04c_changed': False, 'ready_for_formal_research': False})
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
