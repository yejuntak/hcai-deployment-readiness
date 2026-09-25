"""Synchronize the overview without changing releases or the home component."""
import argparse
from pathlib import Path
from build_experience import render_research_page

parser = argparse.ArgumentParser()
parser.add_argument('--site-root', type=Path, required=True)
parser.add_argument('--check', action='store_true')
args = parser.parse_args()
path = args.site_root/'templates/research.gohtml'
current = path.read_text()
marker = '{{define "research-preview"}}'
assert current.count(marker) == 1, 'Expected one preserved home-page component'
expected = render_research_page().rstrip()+'\n\n'+marker+current.split(marker, 1)[1]
if args.check:
    assert current == expected, 'Overview and canonical source differ'
else:
    path.write_text(expected)
print('Overview synchronized; home component and release downloads preserved')
