"""Enforce the requested punctuation style without changing historical artifacts."""
import hashlib
import html
import json
from pathlib import Path

from hcai_readiness.contracts import Assessment
from hcai_readiness.guidance import GUIDES, criteria_catalog
from hcai_readiness.reporting import render_report
from hcai_readiness.versions import versions

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN = (chr(0x2013), chr(0x2014))


def test_current_reader_text_has_no_em_or_en_dash():
    paths = list((ROOT/'protocol'/versions()['protocol']).glob('*.md'))
    paths += list((ROOT/'docs').glob('*.md'))
    paths += list((ROOT/'docs/web').glob('*.html'))
    paths += list((ROOT/'skills/ai-ready/references').glob('*.md'))
    paths += [ROOT/name for name in ('README.md', 'CHANGELOG.md', 'docs/research-content.gohtml',
                                     'skills/ai-ready/SKILL.md', 'schemas/README.md', 'index.html',
                                     'docs/index.html', 'Pilot-Kit/rc4-candidate-5-external-packet.md')]
    failures = [str(p.relative_to(ROOT)) for p in paths if any(c in html.unescape(p.read_text()) for c in FORBIDDEN)]
    assert not failures, failures
    assert all(c not in json.dumps(GUIDES, ensure_ascii=False) for c in FORBIDDEN)
    assert all(c not in json.dumps(criteria_catalog(), ensure_ascii=False) for c in FORBIDDEN)
    for path in (ROOT/'examples/rc4').glob('*.json'):
        if path.name == 'pilot-synthetic.json':
            continue
        record = Assessment.model_validate_json(path.read_text())
        for format in ('markdown', 'html'):
            assert all(c not in html.unescape(render_report(record, format)) for c in FORBIDDEN)


def test_candidate_four_remains_byte_frozen():
    manifest = json.loads((ROOT/'historical/candidate-4-manifest.json').read_text())
    assert len(manifest['files']) == 15
    for name, digest in manifest['files'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest
    site = ROOT.parent/'readiness-site'
    if site.is_dir():
        assets = json.loads((ROOT/'historical/candidate-4-site-manifest.json').read_text())
        assert len(assets['files']) == 28
        for name, digest in assets['files'].items():
            assert hashlib.sha256((site/name).read_bytes()).hexdigest() == digest
