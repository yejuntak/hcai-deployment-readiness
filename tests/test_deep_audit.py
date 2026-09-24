"""Adversarial candidate.3 regressions: file presence is not assurance."""
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path
import pytest
from pydantic import ValidationError
from hcai_readiness.contracts import Assessment, PilotRun
from hcai_readiness.engine import assess, validation_targets, CONTEXT_FLOORS
from hcai_readiness.reporting import render_report

ROOT = Path(__file__).resolve().parents[1]

def case():
    return json.loads((ROOT/'examples/rc4/low-risk-quick.json').read_text())

def result(d):
    return assess(Assessment.model_validate(d))

@pytest.mark.parametrize('target', ['acceptance', 'scope', 'state', 'reference', 'dependencies', 'authority'])
def test_changed_requirement_context_invalidates_validation(target):
    d = case()
    if target == 'acceptance':
        d['workflow']['requirements'][0]['acceptance_criteria'] = 'A newly changed success condition'
    elif target == 'scope':
        d['scope']['environment'] = 'New live multi-tenant environment'
    elif target == 'state':
        d['workflow']['states'][0]['behavior'] = 'New behavior not walked through'
    elif target == 'reference':
        d['evidence'][0]['version'] = 'different-reference-revision'
    elif target == 'dependencies':
        d['workflow']['dependencies'].append('New untested integration')
    else:
        d['workflow']['action_boundaries'] = ['Now allowed to send externally']
    r = result(d)
    assert r['decision'] == 'REVISE'
    assert any('context changed' in reason for reason in r['gates'][3]['reasons'])

def test_missing_requirement_fingerprint_is_missing_not_a_pass():
    d = case()
    d['workflow']['validations'][0]['tested_requirement_digests'] = {}
    assert result(d)['decision'] == 'INSUFFICIENT_EVIDENCE'

def test_validation_targets_do_not_stamp_or_verify_evidence():
    d = case()
    d['workflow']['requirements'][0]['acceptance_criteria'] = 'Changed criterion'
    a = Assessment.model_validate(d)
    before = a.model_dump()
    t = validation_targets(a)
    assert a.model_dump() == before and not t['evidence_verified']
    assert 'decision' not in t and result(d)['decision'] == 'REVISE'
    assert t['requirement_digests'] != d['workflow']['validations'][0]['tested_requirement_digests']

@pytest.mark.parametrize('mutation', ['no_entry','orphan','no_exit','no_endpoint_flag'])
def test_proposed_graph_cannot_pass_disconnected_or_unfinished(mutation):
    d = case()
    if mutation == 'no_entry':
        d['workflow']['entry_state_id'] = None
    elif mutation == 'orphan':
        d['workflow']['states'][0]['next_state_ids'] = ['S4']
    elif mutation == 'no_exit':
        for row in d['workflow']['states']:
            row.update(terminal=False, next_state_ids=['S1'])
    else:
        d['workflow']['states'][3]['terminal'] = None
    r = result(d)
    assert r['stop_at_gate'] == 'G3_STATES_RECOVERY'
    assert r['gates'][2]['status'] == 'MISSING'

def test_dangling_proposed_transition_is_invalid():
    d = case()
    d['workflow']['states'][0]['next_state_ids'] = ['UNKNOWN']
    with pytest.raises(ValidationError):
        Assessment.model_validate(d)

def test_empty_authority_inventory_cannot_pass():
    d = case()
    d['workflow']['action_boundaries'] = []
    assert result(d)['stop_at_gate'] == 'G3_STATES_RECOVERY'

@pytest.mark.parametrize('field,floor', list(CONTEXT_FLOORS.items()))
def test_context_floors_override_self_declared_low_risk(field, floor):
    d = case()
    d['risk']['context'][field] = True
    r = result(d)
    assert r['risk_tier'] == floor
    assert r['required_profile'] == 'FULL'
    assert r['routing']['known_risk_floor'] == floor
    assert r['decision'] != 'PROCEED_TO_ENGINEERING'
    assert all(g['status'] == 'NOT_EVALUATED' for g in r['gates'])

def test_unknown_context_never_means_no_and_retains_known_floor():
    d = case()
    d['risk']['context'].update(safety_or_rights_impact=True, sensitive_data=None)
    r = result(d)
    assert r['risk_tier'] == 'unknown' and r['routing']['known_risk_floor'] == 'high'

@pytest.mark.parametrize('mutation',['missing_domain','unknown','unjustified_na','uncovered_role','missing_requirement'])
def test_affected_people_and_applicability_cannot_be_skipped(mutation):
    d = case()
    if mutation == 'missing_domain':
        d['workflow']['impact_reviews'].pop()
    elif mutation == 'unknown':
        d['workflow']['impact_reviews'][1]['applicability'] = 'unknown'
    elif mutation == 'unjustified_na':
        d['workflow']['impact_reviews'][1].update(applicability='not_applicable',rationale='')
    elif mutation == 'uncovered_role':
        d['scope']['affected_roles'].append('bystander')
    else:
        d['workflow']['impact_reviews'][0]['requirement_ids'] = []
    assert result(d)['stop_at_gate'] == 'G2_NEED_REQUIREMENTS'

def test_human_use_and_control_cannot_be_declared_inapplicable():
    d = case()
    d['workflow']['impact_reviews'][0]['applicability'] = 'not_applicable'
    assert result(d)['decision'] == 'REVISE'

@pytest.mark.parametrize('field',['sensitive_data','untrusted_input_to_actions'])
def test_context_and_applicability_cannot_contradict(field):
    d = case()
    d['requested_profile'] = 'FULL'
    d['risk']['context'][field] = True
    d['workflow']['impact_reviews'][1]['applicability'] = 'not_applicable'
    r = result(d)
    assert r['gates'][1]['status'] == 'FAIL'
    assert r['decision'] == 'REVISE'

@pytest.mark.parametrize('mutation',['missing','agent','no_role','estimated_record'])
def test_evidence_quality_needs_accountable_review(mutation):
    d = case()
    review = d['handoff']['evidence_quality_review']
    if mutation == 'missing':
        review['status'] = 'missing'
    elif mutation == 'agent':
        review['reviewer_kind'] = 'agent'
    elif mutation == 'no_role':
        review['reviewer_role'] = None
    else:
        # Keep all other synthetic records valid; only the review record is an estimate.
        d['evidence'].append({**d['evidence'][0], 'id':'REVIEW', 'kind':'estimate'})
        review['evidence_ids'] = ['REVIEW']
    r = result(d)
    assert r['decision'] == 'INSUFFICIENT_EVIDENCE'
    assert r['stop_at_gate'] == 'G6_COMMITMENT'

def test_pilot_preserves_routing_and_unassessed_gates():
    d = json.loads((ROOT/'examples/rc4/pilot-synthetic.json').read_text())
    d['assessment']['risk']['context']['sensitive_data'] = True
    r = result(d['assessment'])
    d.update(gates_passed=[], gates_not_evaluated=[g['id'] for g in r['gates']],
             risk_tier='moderate', decision_after=r['decision'], routing_status='USE_FULL',
             follow_up_reasons=sorted({reason for g in r['gates'] for reason in g['reasons']}))
    assert PilotRun.model_validate(d).gates_not_evaluated
    d['follow_up_reasons'] = []
    with pytest.raises(ValidationError):
        PilotRun.model_validate(d)

def test_report_distinguishes_rule_checks_from_assurance():
    a = Assessment.model_validate(case())
    r = assess(a)
    assert r['assurance']['criterion_conformance'] == 'NOT_CERTIFIED'
    assert r['assurance']['evidence_authenticity'] == 'NOT_INDEPENDENTLY_VERIFIED'
    report = render_report(a,'html')
    assert 'No gate stop' in report and 'People and consequences' in report
    assert 'requirement/context matches: True' in report

def test_candidate_two_remains_byte_frozen():
    manifest = json.loads((ROOT/'historical/candidate-2-manifest.json').read_text())
    assert len(manifest['files']) == 14
    for name, digest in manifest['files'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest

def test_cli_targets_match_shared_engine():
    output = subprocess.check_output([sys.executable,'-m','hcai_readiness.cli',str(ROOT/'examples/rc4/low-risk-quick.json'),'--validation-targets'],text=True)
    assert json.loads(output) == validation_targets(Assessment.model_validate(case()))

def test_deep_audit_public_pages_and_references():
    from hcai_readiness.guidance import criteria_catalog
    assert criteria_catalog()['version'] == case()['versions']['protocol']
    for name in ('deep-audit','claims-and-governance','WORKSHEET'):
        page = (ROOT/'docs/web'/f'{name}.html').read_text()
        assert '<html lang="en">' in page
        assert '<h1>' in page and '<title>' in page
        assert '0.1-rc.4-candidate.3' in page
    protocol = (ROOT/'protocol/0.1-rc.4-candidate.3/PROTOCOL.md').read_text()
    assert '15 review criteria' in protocol and 'not a W3C standard' in protocol
    assert (ROOT/'docs/claims-and-governance.md').read_bytes() == (ROOT/'skills/ai-ready/references/claims-and-governance.md').read_bytes()

def test_worksheet_writing_spaces_remain_literal_and_tables_focusable():
    page = (ROOT/'docs/web/WORKSHEET.html').read_text()
    assert 'Workflow / one completed case: ______' in page
    assert '<em>' not in page
    assert 'tabindex="0" role="region"' in page
