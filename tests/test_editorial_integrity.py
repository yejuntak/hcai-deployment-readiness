"""Frozen editorial evidence and established decision/economic behavior survive new releases."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import zipfile

import pytest
from hcai_readiness.contracts import Assessment
from hcai_readiness.engine import assess
from hcai_readiness.guidance import criteria_catalog
from hcai_readiness.versions import versions

ROOT = Path(__file__).resolve().parents[1]
OLD_PREFIX = 'HCAI-v0.1-rc.4-candidate.3/'
OLD_ZIP = ROOT/'release/HCAI-v0.1-rc.4-candidate.3.zip'
OLD_WHEEL = ROOT/'release/hcai_readiness_mcp-0.2.0rc3-py3-none-any.whl'


def previous(name):
    with zipfile.ZipFile(OLD_ZIP) as archive:
        return archive.read(OLD_PREFIX+name)


def test_candidate_three_remains_byte_frozen():
    manifest = json.loads((ROOT/'historical/candidate-3-manifest.json').read_text())
    assert len(manifest['files']) == 15
    for name, digest in manifest['files'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest
    site = ROOT.parent/'readiness-site'
    if site.is_dir():
        assets = json.loads((ROOT/'historical/candidate-3-site-manifest.json').read_text())
        assert len(assets['files']) == 27
        for name, digest in assets['files'].items():
            assert hashlib.sha256((site/name).read_bytes()).hexdigest() == digest


def test_editorial_release_preserves_core_logic():
    # The frozen executable must still contain the exact published source used
    # in the regression comparison below. Current feature work may change it.
    with zipfile.ZipFile(OLD_WHEEL) as wheel:
        for name in ('engine.py', 'contracts.py', 'records.py', 'assessment.py'):
            assert wheel.read('hcai_readiness/'+name) == previous('src/hcai_readiness/'+name)


@pytest.mark.parametrize('name', [
    'low-risk-quick', 'polished-no-baseline', 'documentation-no-operational-evidence',
    'prototype-no-traceability', 'high-risk-quick', 'high-risk-full', 'savings-erased',
    'expensive-evaluation', 'missing-recovery',
])
def test_editorial_release_preserves_fixture_decisions(name, tmp_path):
    record = json.loads((ROOT/'examples/rc4'/f'{name}.json').read_text())
    current = assess(Assessment.model_validate(record))
    old_record = json.loads(previous('examples/rc4/'+name+'.json'))
    # Execute the actual frozen wheel, not a rewritten approximation of its logic.
    program = 'import json,sys; from hcai_readiness.contracts import Assessment; from hcai_readiness.engine import assess; print(json.dumps(assess(Assessment.model_validate(json.load(sys.stdin)))))'
    env = {**os.environ, 'PYTHONPATH': str(OLD_WHEEL)}
    old = json.loads(subprocess.check_output([sys.executable, '-c', program],
                                            input=json.dumps(old_record), text=True, cwd=tmp_path, env=env))
    # Compare the entire historical result, including empty metric/evidence
    # dictionaries. Only these three explicit top-level additions are allowed;
    # a generic subset comparison could hide invented operational results.
    added_fields = {'mode', 'artifact_population', 'choice_review'}
    assert set(current) - set(old) == added_fields
    assert not set(old) - set(current)
    def historical_result(value):
        output = json.loads(json.dumps(value))
        for field in added_fields | {'versions'}:
            output.pop(field, None)
        output['provenance'].pop('input_sha256')
        return output
    assert historical_result(current) == historical_result(old)
    assert current['versions'] == versions()
    assert current['mode'] == 'engineering_commitment'
    assert current['artifact_population'] == record['artifact_population']


def test_editorial_release_preserves_criterion_identity():
    old = json.loads(previous('src/hcai_readiness/criteria.json'))
    current = criteria_catalog()
    assert [(c['id'], c['gate']) for c in current['criteria']] == [(c['id'], c['gate']) for c in old['criteria']]
    assert current['principles'] == old['principles']
    assert current['version'] == versions()['protocol']


def test_editorial_release_preserves_risk_tables_and_formulas():
    old = previous('protocol/0.1-rc.4-candidate.3/FULL-PROFILE.md').decode()
    current = (ROOT/'protocol'/versions()['protocol']/'FULL-PROFILE.md').read_text()
    def numerical_contract(text):
        return [line for line in text.splitlines() if line.startswith(('|', '- Gross', '- Net', '- Baseline', '- Proposed', '- Recurring', '- Payback'))]
    assert numerical_contract(current) == numerical_contract(old)


def test_editorial_release_preserves_external_citations():
    # Candidate.6 explicitly removes these unrelated references at the author's request.
    removed = {
        'https://www.w3.org/TR/WCAG20/#intro-layers-guidance',
        'https://www.w3.org/TR/WCAG22/',
        'https://www.w3.org/WAI/WCAG22/Understanding/understanding-act-rules.html',
        'https://www.w3.org/WAI/WCAG22/Understanding/conformance',
    }
    def citations(text):
        urls = re.findall(r'https://[^\s)"<>]+', text)
        return {url for url in urls if any(domain in url for domain in ('w3.org/', 'nist.gov/', 'microsoft.com/', 'doi.org/'))}
    for name in ('docs/deep-audit.md', 'docs/research-boundary.md', 'README.md', 'docs/research-content.gohtml'):
        assert citations((ROOT/name).read_text()) == citations(previous(name).decode()) - removed
    assert citations((ROOT/'protocol'/versions()['protocol']/'PROTOCOL.md').read_text()) == citations(previous('protocol/0.1-rc.4-candidate.3/PROTOCOL.md').decode()) - removed


def test_editorial_audit_is_linked_and_candidate_only():
    page = (ROOT/'docs/web/editorial-review.html').read_text()
    assert '<html lang="en">' in page and '<h1>' in page
    assert versions()['protocol'] in page
    assert 'editorial-review.html' in (ROOT/'docs/research-content.gohtml').read_text()
    assert json.loads((ROOT/'Pilot-Kit/rc4-pilot-runs.json').read_text()) == []
