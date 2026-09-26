"""Keep naming-only releases frozen while the current contract evolves explicitly."""
import copy
import hashlib
import json
from pathlib import Path
import zipfile

import pytest
from pydantic import ValidationError
from hcai_readiness.contracts import Assessment
from hcai_readiness.engine import assess
from hcai_readiness.versions import identity, versions

ROOT = Path(__file__).resolve().parents[1]


def test_first_hard_preview_and_all_published_assets_remain_frozen():
    for base, filename in [(ROOT, 'hard-preview-1-manifest.json'),
                           (ROOT.parent/'readiness-site', 'hard-preview-1-site-manifest.json')]:
        if not base.exists():
            continue
        manifest = json.loads((ROOT/'historical'/filename).read_text())
        assert manifest['files']
        for name, digest in manifest['files'].items():
            assert hashlib.sha256((base/name).read_bytes()).hexdigest() == digest, name


def test_second_hard_preview_remains_byte_frozen():
    manifest = json.loads((ROOT/'historical/hard-preview-2-manifest.json').read_text())
    assert manifest['protocol_version'] == '0.2-preview.2'
    assert manifest['files']
    for name, digest in manifest['files'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest, name


def test_decision_name_preserves_first_preview_method_and_fixtures():
    # This is a claim about the two published naming-only releases, not a rule
    # prohibiting an explicitly versioned subsequent feature release.
    with zipfile.ZipFile(ROOT/'release/HARD-Protocol-0.2-preview.1.zip') as archive, \
         zipfile.ZipFile(ROOT/'release/HARD-Protocol-0.2-preview.2.zip') as renamed:
        prefix = 'HARD-Protocol-0.2-preview.1/'
        renamed_prefix = 'HARD-Protocol-0.2-preview.2/'
        for name in ('engine.py', 'contracts.py', 'records.py', 'assessment.py'):
            assert archive.read(prefix+'src/hcai_readiness/'+name) == renamed.read(renamed_prefix+'src/hcai_readiness/'+name)
        old_catalog = json.loads(archive.read(prefix+'src/hcai_readiness/criteria.json'))
        new_catalog = json.loads(renamed.read(renamed_prefix+'src/hcai_readiness/criteria.json'))
        old_catalog['version'] = new_catalog['version']
        assert old_catalog == new_catalog
        for path in (ROOT/'examples/rc4').glob('*.json'):
            if path.name == 'pilot-synthetic.json':
                continue
            old = json.loads(archive.read(prefix+'examples/rc4/'+path.name))
            original = json.dumps(old, sort_keys=True)
            with pytest.raises(ValidationError):
                Assessment.model_validate(old)
            assert json.dumps(old, sort_keys=True) == original
            renamed_record = json.loads(renamed.read(renamed_prefix+'examples/rc4/'+path.name))
            comparison = copy.deepcopy(old)
            comparison['versions'] = renamed_record['versions']
            assert comparison == renamed_record
            # Adding the new population field cannot silently authorize old versions.
            legacy_with_population = {**old, 'artifact_population': 'ai_generated'}
            with pytest.raises(ValidationError, match='Exact protocol/MCP/Skill/contract'):
                Assessment.model_validate(legacy_with_population)
            current = json.loads(path.read_text())
            assert assess(Assessment.model_validate(current))['operational_performance']['deployment_decision'] == 'NOT_ASSESSED'


def test_decision_identity_scope_and_versioned_guides():
    assert identity()['full_name'] == 'Human-centered AI Readiness and Decision Protocol'
    for path in (ROOT/'protocol'/versions()['protocol']).glob('*.md'):
        text = path.read_text()
        assert 'Public Preview' in text and versions()['protocol'] in text
        assert 'The name includes deployment' not in text
        assert 'Readiness Deployment Protocol' not in text
    for name in ('README.md', 'skills/ai-ready/SKILL.md', 'docs/agent-tools.md',
                 'src/hcai_readiness/protocol.md', 'CITATION.cff', 'docs/decision-naming-migration.md'):
        assert identity()['full_name'] in (ROOT/name).read_text(), name
    assert json.loads((ROOT/'Pilot-Kit/rc4-pilot-runs.json').read_text()) == []
