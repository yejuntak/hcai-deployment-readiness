"""Run current regression checks and record an honest candidate release assessment."""
import hashlib
import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from hcai_readiness.contracts import PilotRun
from hcai_readiness.records import release_readiness
from hcai_readiness.versions import versions

ROOT = Path(__file__).resolve().parents[1]


def main():
    out = ROOT / 'Verification'
    out.mkdir(exist_ok=True)
    suite = out / 'rc4-junit.xml'
    result = subprocess.run([sys.executable, '-m', 'pytest', '-q', '--junitxml', str(suite)], cwd=ROOT, text=True, capture_output=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    summaries = ET.parse(suite).getroot().findall('testsuite') if suite.exists() else []
    totals = {k: sum(int(s.get(k, '0')) for s in summaries) for k in ('tests', 'failures', 'errors', 'skipped')}
    inputs = {}
    for directory in ('src', 'tests', 'skills', 'protocol', 'schemas', 'evidence', 'examples'):
        for path in sorted((ROOT / directory).rglob('*')):
            if path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc':
                inputs[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
    report = {'recorded_at': datetime.now(timezone.utc).isoformat(), 'versions': versions(), 'command': 'python -m pytest -q --junitxml Verification/rc4-junit.xml',
              'exit_code': result.returncode, **totals, 'input_file_sha256': inputs,
              'interpretation': 'Software regression evidence only. No human pilot, adoption, endorsement or controlled empirical validation.'}
    (out / 'rc4-test-results.json').write_text(json.dumps(report, indent=2) + '\n')
    raw = json.loads((ROOT / 'Pilot-Kit/rc4-pilot-runs.json').read_text())
    pilots = [PilotRun.model_validate(p) for p in raw]
    release = release_readiness(pilots, regression_passed=result.returncode == 0 and totals['tests'] > 0)
    release['recorded_at'] = report['recorded_at']
    release['actual_pilot_records'] = len([p for p in pilots if p.record_kind == 'actual'])
    (out / 'rc4-release-readiness.json').write_text(json.dumps(release, indent=2) + '\n')
    print(json.dumps(release, indent=2))
    raise SystemExit(result.returncode)


if __name__ == '__main__':
    main()
