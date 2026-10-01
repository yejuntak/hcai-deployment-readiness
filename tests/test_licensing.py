"""Distribution-level licensing and historical preservation regression checks."""
import hashlib
import json
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_license_metadata_and_skill_notices_agree():
    project = tomllib.loads((ROOT / 'pyproject.toml').read_text())['project']
    assert project['license'] == 'Apache-2.0'
    assert project['license-files'] == ['LICENSE', 'NOTICE']
    assert json.loads((ROOT / '.zenodo.json').read_text())['license'] == 'apache-2.0'
    assert '\nlicense: Apache-2.0\n' in (ROOT / 'CITATION.cff').read_text()
    for name in ('LICENSE', 'NOTICE'):
        assert (ROOT / name).read_bytes() == (ROOT / 'skills/ai-ready/references' / name).read_bytes()
    for name in ('README.md', 'skills/ai-ready/SKILL.md', 'docs/claims-and-governance.md', 'docs/research-content.gohtml'):
        text = (ROOT / name).read_text()
        assert 'Apache-2.0' in text
        assert 'CC BY 4.0' not in text
        assert 'engine code MIT' not in text


def test_preserved_license_baseline_bytes():
    baseline = json.loads((ROOT / 'historical/apache-license-baseline.json').read_text())
    assert baseline['source_commit'] == 'f6c61a2137c482e85c6562cf28afd9f72f320738'
    for name, expected in baseline['files'].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected, name


def test_packager_refuses_frozen_version_before_writes(tmp_path, monkeypatch):
    import importlib.util
    spec = importlib.util.spec_from_file_location('license_packager', ROOT / 'scripts/package_candidate.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    (tmp_path / 'Verification').mkdir()
    (tmp_path / 'Verification/current-test-results.json').write_text(json.dumps(
        {'exit_code': 0, 'failures': 0, 'errors': 0, 'tests': 1, 'input_file_sha256': {}}))
    (tmp_path / 'historical').mkdir()
    (tmp_path / 'historical/apache-license-baseline.json').write_text(json.dumps(
        {'files': {'release/frozen.zip': 'example'}}))
    monkeypatch.setattr(module, 'ROOT', tmp_path)
    monkeypatch.setattr(module, 'RELEASE', tmp_path / 'release')
    monkeypatch.setattr(module, 'ZIP_NAME', 'frozen.zip')
    monkeypatch.setattr('sys.argv', ['package_candidate.py'])
    import pytest
    with pytest.raises(SystemExit, match='Refusing to overwrite a frozen distribution'):
        module.main()
    assert not (tmp_path / 'release').exists()
