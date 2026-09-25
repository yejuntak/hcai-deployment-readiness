"""Presentation can change without rebuilding or relabeling the protocol."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_experience import render_research_page
from hcai_readiness.guidance import criteria_catalog


def test_overview_links_to_all_canonical_rules_without_duplicating_them():
    page = render_research_page()
    assert page.count('developers#HCAI-') == 15
    assert 'class="research-criterion"' not in page
    assert '<!-- CRITERIA -->' not in page
    assert '@@HARD_' not in page
    for criterion in criteria_catalog()['criteria']:
        assert 'id="'+criterion['id']+'"' in page
        assert '/research/ai-readiness/developers#'+criterion['id'] in page
    assert 'HARD Protocol 0.2' in page
    assert 'Public Preview' in page
    assert page.count('id="hard-mcp-config"') == 1
