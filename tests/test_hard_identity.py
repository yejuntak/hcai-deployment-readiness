"""Public branding is separate from exact execution provenance and decision logic."""
import hashlib
import json
from pathlib import Path
import re
import tomllib
import zipfile

import pytest
from pydantic import ValidationError

from hcai_readiness.contracts import Assessment
from hcai_readiness.guidance import new_review
from hcai_readiness.records import release_readiness
from hcai_readiness.reporting import render_report
from hcai_readiness.versions import identity, public_title, versions

ROOT = Path(__file__).resolve().parents[1]


def test_hard_public_identity_and_generated_surfaces():
    assert identity() == {
        'name': 'H.A.R.D. Protocol',
        'full_name': 'Human-centered AI Readiness and Decision Protocol',
        'display_version': '0.3', 'release_label': 'Public Preview',
        'distribution_id': 'hard-'+versions()['protocol'].replace('preview.', 'preview-'),
    }
    assert json.loads((ROOT/'identity.json').read_text()) == identity()
    assert public_title() == 'H.A.R.D. Protocol 0.3'
    surfaces = list((ROOT/'protocol'/versions()['protocol']).glob('*.md'))
    surfaces += [ROOT/p for p in ('README.md', 'skills/ai-ready/SKILL.md',
                  f"Pilot-Kit/{identity()['distribution_id']}-external-packet.md")]
    for path in surfaces:
        text = path.read_text()
        assert public_title() in text and 'Public Preview' in text, path
        assert versions()['protocol'] in text, path
    assert 'display_name: "H.A.R.D. Protocol"' in (ROOT/'skills/ai-ready/agents/openai.yaml').read_text()
    assert 'name: ai-ready' in (ROOT/'skills/ai-ready/SKILL.md').read_text()
    for path in (ROOT/'index.html', ROOT/'docs/index.html'):
        text = path.read_text()
        assert '<h1' in text and public_title() in text and identity()['full_name'] in text
        assert '@@HARD_' not in text
    assert tomllib.loads((ROOT/'pyproject.toml').read_text())['project']['version'] == versions()['mcp']
    record = Assessment.model_validate_json((ROOT/'examples/rc4/low-risk-quick.json').read_text())
    for kind in ('markdown', 'html'):
        report = render_report(record, kind)
        for label in (public_title(), identity()['full_name'], 'Public Preview', versions()['protocol']):
            assert label in report


def test_hard_execution_versions_and_legacy_record_boundary():
    exact = versions()
    assert exact == json.loads((ROOT/'versions.json').read_text())
    assert re.fullmatch(r'0\.3-preview\.\d+', exact['protocol'])
    release = re.fullmatch(r'0\.3\.0rc(\d+)', exact['mcp'])
    assert release
    assert exact['skill'] == exact['contract'] == '0.3.0-rc.'+release[1]
    assert new_review('HARD-NEW', '2026-09-24T12:00:00Z', 'human')['versions'] == exact
    archive_path = ROOT/'release/HCAI-v0.1-rc.4-candidate.6.zip'
    before = hashlib.sha256(archive_path.read_bytes()).hexdigest()
    with zipfile.ZipFile(archive_path) as archive:
        legacy = json.loads(archive.read('HCAI-v0.1-rc.4-candidate.6/examples/rc4/low-risk-quick.json'))
    original = json.dumps(legacy, sort_keys=True)
    with pytest.raises(ValidationError):
        Assessment.model_validate(legacy)
    with pytest.raises(ValidationError, match='Exact protocol/MCP/Skill/contract'):
        Assessment.model_validate({**legacy, 'artifact_population': 'ai_generated'})
    assert json.dumps(legacy, sort_keys=True) == original
    assert legacy['versions']['protocol'] == '0.1-rc.4-candidate.6'
    assert hashlib.sha256(archive_path.read_bytes()).hexdigest() == before
    current = json.loads((ROOT/'examples/rc4/low-risk-quick.json').read_text())
    current['versions']['protocol'] = '0.3'
    with pytest.raises(ValidationError, match='Exact protocol/MCP/Skill/contract'):
        Assessment.model_validate(current)


def test_hard_preview_does_not_promote_without_actual_use():
    assert json.loads((ROOT/'Pilot-Kit/rc4-pilot-runs.json').read_text()) == []
    result = release_readiness([], regression_passed=True)
    assert result['status'] == 'REMAIN_CANDIDATE'
    assert identity()['release_label'] == 'Public Preview'


def test_candidate_six_remains_byte_frozen():
    manifest = json.loads((ROOT/'historical/candidate-6-manifest.json').read_text())
    assert len(manifest['files']) == 15
    for name, digest in manifest['files'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest, name
    site = ROOT.parent/'readiness-site'
    if site.is_dir():
        assets = json.loads((ROOT/'historical/candidate-6-site-manifest.json').read_text())
        assert len(assets['files']) == 28
        for name, digest in assets['files'].items():
            assert hashlib.sha256((site/name).read_bytes()).hexdigest() == digest, name
