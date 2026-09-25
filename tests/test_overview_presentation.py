"""Presentation can change without rebuilding or relabeling the protocol."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_experience import render_research_page
from hcai_readiness.guidance import criteria_catalog


def test_overview_links_to_all_canonical_rules_without_duplicating_them():
    page = render_research_page()
    assert page.count('href="/research/ai-readiness/developers"') == 1
    assert page.count('data-primary-task') == 4
    assert page.split('</section>')[0].count('data-primary-task') == 2
    assert 'class="research-criterion"' not in page
    assert '<!-- CRITERIA -->' not in page
    assert '@@HARD_' not in page
    for criterion in criteria_catalog()['criteria']:
        assert 'id="'+criterion['id']+'"' in page
        assert criterion['requirement'] not in page
    assert 'H.A.R.D. Protocol 0.2' in page
    assert 'Public Preview' in page
    assert 'id="hard-mcp-config"' not in page
    assert 'class="hard-legacy-anchors" aria-hidden="true"' in page


def test_overview_explains_the_missing_layer_without_claiming_a_result():
    page = render_research_page()
    assert 'A polished result can still be unfinished.' in page
    assert 'origin anecdote, not evidence of a measured effect' in page
    assert 'Payment taken. No booking. Now what?' in page
    assert 'Do not blur labels or remove information people need' in page
    for label in ('Experience and information', 'Workflow and architecture',
                  'Implementation and evidence', 'People and operation'):
        assert label in page
    protocol = (ROOT/'protocol/0.2-preview.2/PROTOCOL.md').read_text()
    assert 'not four scores or additional gates' in protocol
    skill = (ROOT/'skills/ai-ready/SKILL.md').read_text()
    assert 'Never introduce this view into a research session' in skill
