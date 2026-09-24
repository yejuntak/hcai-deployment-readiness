import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path
import pytest
from pydantic import ValidationError
from hcai_readiness.contracts import Assessment, StudyReview, PilotRun
from hcai_readiness.engine import assess, validation_targets
from hcai_readiness.guidance import new_review, guided_review, criteria_catalog, criterion_guide
from hcai_readiness.reporting import render_report
from hcai_readiness.server import review_next_step, validate_study_review

ROOT = Path(__file__).resolve().parents[1]

def case(name='low-risk-quick'):
    return json.loads((ROOT / 'examples/rc4' / (name+'.json')).read_text())

def result(d):
    return assess(Assessment.model_validate(d))

def test_current_map_is_required_and_connected():
    d = case()
    d['baseline'].update(steps=[], entry_step_id=None)
    assert result(d)['stop_at_gate'] == 'G1_BASELINE'
    d = case()
    d['baseline']['steps'][0]['next_step_ids'] = ['C4']
    assert any('reachable' in r for r in result(d)['gates'][0]['reasons'])

def test_current_map_requires_exit_and_observed_normal():
    d = case()
    for step in d['baseline']['steps']:
        step.update(terminal=False, next_step_ids=['C1'], observation_status='reported')
    reasons = result(d)['gates'][0]['reasons']
    assert any('endpoint' in r for r in reasons)
    assert any('observed' in r for r in reasons)

@pytest.mark.parametrize('mutation', ['same_origin', 'general_reference', 'assumed_discussion'])
def test_need_sources_are_actual_distinct_origins(mutation):
    d = case('high-risk-full')
    if mutation == 'same_origin':
        d['evidence'][2]['origin_id'] = d['evidence'][1]['origin_id']
    elif mutation == 'general_reference':
        d['evidence'][2]['source_type'] = 'reference'
    else:
        d['evidence'][2]['kind'] = 'assumption'
    assert result(d)['gates'][1]['status'] == 'MISSING'

def test_stale_or_missing_tested_revision_never_passes():
    d = case()
    d['workflow']['validations'][0]['tested_artifact_digests']['E1'] = 'a'*64
    assert result(d)['decision'] == 'REVISE'
    d['workflow']['validations'][0]['tested_artifact_digests'] = {}
    assert result(d)['decision'] == 'INSUFFICIENT_EVIDENCE'

def test_simulated_behavior_is_not_implemented_test():
    d = case()
    d['workflow']['validations'][0]['level'] = 'implemented_test'
    assert result(d)['decision'] == 'REVISE'
    d['workflow']['requirements'][0]['behavior_status'] = 'implemented'
    # Stipulate a NEW synthetic execution against the changed requirement, not an old pass.
    d['workflow']['validations'][0]['tested_requirement_digests'] = validation_targets(Assessment.model_validate(d))['requirement_digests']
    assert result(d)['decision'] == 'PROCEED_TO_ENGINEERING'
    assert result(d)['operational_performance']['deployment_decision'] == 'NOT_ASSESSED'

def test_human_action_boundaries_required():
    d = case()
    d['workflow']['human_control_review'] = {}
    d['workflow']['action_boundaries'] = None
    assert result(d)['stop_at_gate'] == 'G3_STATES_RECOVERY'

def test_preparation_is_costed_not_hidden_or_double_counted():
    d = case()
    before = result(d)
    d['evaluator_burden'].update(preparation_person_minutes=60, preparation_elapsed_minutes=30)
    after = result(d)
    rate = d['evaluator_burden']['labor_cost_per_hour']
    assert after['evaluator_burden']['protocol_evaluation_cost'] == before['evaluator_burden']['protocol_evaluation_cost']+rate
    assert after['roi'] == before['roi']
    d['evaluator_burden']['preparation_person_minutes'] = None
    assert result(d)['evaluator_burden']['protocol_evaluation_cost'] is None
    assert result(d)['decision'] == 'INSUFFICIENT_EVIDENCE'
    d['evaluator_burden']['capture_reporting_minutes'] = 16
    with pytest.raises(ValidationError):
        Assessment.model_validate(d)

def test_routing_is_early_and_known_floor_retained():
    d = case('high-risk-quick')
    d['risk']['complexity'] = None
    r = result(d)
    assert r['routing']['known_risk_floor'] == 'high'
    assert r['stop_at_gate'] == 'PROFILE_ROUTING'
    assert all(g['status'] == 'NOT_EVALUATED' for g in r['gates'])

def test_early_stop_does_not_hide_known_critical_findings():
    d = case('polished-no-baseline')
    d['handoff']['reviewer_findings'] = [{'id':'F1','severity':'critical','status':'accepted','description':'Known unsafe action','evidence_ids':['E1']}]
    r = result(d)
    assert r['decision'] == 'REVISE'
    assert r['stop_at_gate'] == 'G1_BASELINE'
    assert r['attention_items'][0]['id'] == 'F1'

def test_nonpositive_benefit_requires_rationale_and_stays_visible():
    d = case('savings-erased')
    assert result(d)['decision'] == 'INSUFFICIENT_EVIDENCE'
    d['handoff']['investment_rationale'] = 'Bounded learning experiment, not a savings investment.'
    r = result(d)
    assert r['decision'] == 'PROCEED_TO_ENGINEERING'
    assert r['roi']['net_operational_benefit_per_period'] < 0
    assert any(x['kind'] == 'nonpositive_benefit' for x in r['attention_items'])

def test_guided_journey_starts_small_and_never_seeds_facts():
    d = new_review('NEW', '2026-09-24T12:00:00Z', 'human')
    assert d['evidence'] == [] and d['baseline']['steps'] == []
    assert all(v is None for v in d['scope'].values())
    guide = guided_review(Assessment.model_validate(d))
    assert set(guide) == {'decision_card'}
    assert guide['decision_card']['next_step']['stage'] == 'SCOPE'
    d['scope'].update(workflow_name='Intake', unit_of_work='One request')
    assert guided_review(Assessment.model_validate(d))['decision_card']['next_step']['stage'] == 'PROFILE_ROUTING'
    d['risk'] = case()['risk']
    d['evidence'] = case()['evidence']
    d['evaluator_kind'] = 'synthetic'
    assert guided_review(Assessment.model_validate(d))['decision_card']['next_step']['stage'] == 'G1_BASELINE'

def test_stopped_run_revision_requires_trace():
    d = case()
    d['previous_run_id'] = 'PRIOR'
    with pytest.raises(ValidationError):
        Assessment.model_validate(d)
    d['revision_summary'] = 'Added retained observation evidence'
    assert Assessment.model_validate(d).previous_run_id == 'PRIOR'

def test_report_escapes_artifacts_and_has_drilldown():
    d = case()
    d['scope']['workflow_name'] = '<script>alert(1)</script> ![x](https://private.invalid)'
    a = Assessment.model_validate(d)
    html = render_report(a, 'html')
    assert '<script>' not in html and '&lt;script&gt;' in html
    assert '<details><summary>' in html and 'tested revision matches: True' in html
    assert 'PRIVATE working record' in html
    md = render_report(a)
    assert '\\!\\[x\\]' in md
    assert '| --- | --- | --- | --- |\n|' in md
    assert '## Next action' in md

def test_invalid_draft_does_not_echo_private_values():
    d = case()
    d['baseline']['sample_size'] = 'PRIVATE_SECRET_SENTINEL'
    r = review_next_step(d)
    assert not r['valid'] and r['decision'] is None
    assert 'PRIVATE_SECRET_SENTINEL' not in json.dumps(r)

def test_criteria_have_stable_ids_examples_and_gate_mapping():
    catalog = criteria_catalog()
    assert len(catalog['principles']) == 4 and len(catalog['criteria']) == 15
    ids = [c['id'] for c in catalog['criteria']]
    assert len(set(ids)) == 15
    gates = {g['id'] for g in result(case())['gates']}
    for c in catalog['criteria']:
        assert c['gate'] in gates
        assert all(c[k] for k in ['requirement','check','pass_example','failure_example','verification'])
        assert criterion_guide(c['id'])['found']
    assert not criterion_guide('UNKNOWN')['found']

def study():
    return dict(study_version='unvalidated-design-example', participant_id='SYNTHETIC', scenario_id='S1', artifact_version='v1', artifact_sha256='a'*64, requirement_ids=['R1','R2'], judgments=[dict(requirement_id='R1',judgment='defect',confidence_correct=.7),dict(requirement_id='R2',judgment='abstain')], review_minutes=2, perceived_handoff_readiness=4, global_confidence=.5, locked_at='2026-09-24T12:00:00Z',reference_answers_disclosed=False)

def test_study_judgments_are_not_engineering_decisions_or_answer_keys():
    d = study()
    assert validate_study_review(StudyReview.model_validate(d))['decision'] is None
    for field, value in [('reference_answers',{'R1':'defect'}),('reference_answers_disclosed',True),('decision','PROCEED_TO_ENGINEERING')]:
        bad = {**d,field:value}
        with pytest.raises(ValidationError):
            StudyReview.model_validate(bad)
    d['judgments'][0]['confidence_correct'] = 1.1
    with pytest.raises(ValidationError):
        StudyReview.model_validate(d)

def test_pilot_usability_records_are_optional_not_fabricated():
    d = case('pilot-synthetic')
    p = PilotRun.model_validate(d)
    assert p.usability.next_action_understood is None
    assert p.usability.participant_explanation_of_decision is None

def test_first_candidate_is_byte_frozen():
    manifest = json.loads((ROOT/'historical/candidate-1-manifest.json').read_text())
    for name, digest in manifest['files'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest, name

def test_cli_guide_report_and_empty_start():
    command = [sys.executable, '-m', 'hcai_readiness.cli']
    path = str(ROOT/'examples/rc4/low-risk-quick.json')
    guide = subprocess.check_output(command+[path,'--guide'],text=True)
    assert json.loads(guide)['decision_card']['next_step']['stage'] == 'OWNER_DECISION'
    report = subprocess.check_output(command+[path,'--format','html'],text=True)
    assert '<details><summary>' in report
    new = subprocess.check_output(command+['--new','--run-id','CLI-NEW','--recorded-at','2026-09-24T12:00:00Z','--evaluator-kind','human'],text=True)
    assert json.loads(new)['evidence'] == []
