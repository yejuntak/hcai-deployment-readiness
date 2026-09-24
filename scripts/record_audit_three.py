"""Record scoped audit-to-test mappings; no new practitioner testimony or validation."""
import json
from pathlib import Path
root = Path(__file__).resolve().parents[1]
rows = [
    ('C19','An altered requirement/context could retain a passing old artifact validation.','Bind checks to both artifact and requirement/context fingerprints; targets never stamp a pass.',['G4_TRACEABILITY'],['src/hcai_readiness/engine.py','src/hcai_readiness/server.py'],['test_changed_requirement_context_invalidates_validation','test_validation_targets_do_not_stamp_or_verify_evidence']),
    ('C20','Proposed state descriptions and an empty authority list could pass without a connected executable design.','Require proposed entry/transitions/exits and a nonempty authority inventory.',['G3_STATES_RECOVERY'],['src/hcai_readiness/contracts.py','src/hcai_readiness/engine.py'],['test_proposed_graph_cannot_pass_disconnected_or_unfinished','test_empty_authority_inventory_cannot_pass']),
    ('C21','All-low self-selected labels could bypass deeper review despite consequential context.','Context flags set deterministic minimum tiers; unknown prevents a quick pass.',['G6_COMMITMENT'],['schemas/context-risk-floors.json','src/hcai_readiness/engine.py'],['test_context_floors_override_self_declared_low_risk','test_unknown_context_never_means_no_and_retains_known_floor']),
    ('C22','An owner efficiency case could omit affected non-operators and human-centered concerns.','Add HCAI-1.4 applicability/affected-role/requirement coverage.',['G2_NEED_REQUIREMENTS'],['src/hcai_readiness/contracts.py','src/hcai_readiness/criteria.json'],['test_affected_people_and_applicability_cannot_be_skipped','test_human_use_and_control_cannot_be_declared_inapplicable']),
    ('C23','A structural pass could be mistaken for evidence-quality assurance.','Require recorded human evidence-quality review and explicit machine/human/authenticity claim boundaries.',['G6_COMMITMENT'],['src/hcai_readiness/engine.py','src/hcai_readiness/reporting.py'],['test_evidence_quality_needs_accountable_review','test_report_distinguishes_rule_checks_from_assurance']),
    ('C24','Pilot records could omit skipped gates and routing follow-up.','Reconcile routing status, NOT_EVALUATED gates and all follow-up reasons.',['PILOT_PROVENANCE'],['src/hcai_readiness/contracts.py','schemas/pilot-run.schema.json'],['test_pilot_preserves_routing_and_unassessed_gates']),
    ('C25','More polished packaging does not establish impact; upgrades could erase the prior candidate.','Freeze candidate.2; publish a worksheet, deep audit, falsifiable validation roadmap and claim/change-control rules.',['HISTORY_FROZEN','CLAIM_BOUNDARY'],['historical/candidate-2-manifest.json','docs/deep-audit.md','docs/claims-and-governance.md','protocol/0.1-rc.4-candidate.3/WORKSHEET.md'],['test_candidate_two_remains_byte_frozen','test_deep_audit_public_pages_and_references'])]
path=root/'evidence/change-manifest.json'
manifest=json.loads(path.read_text())
existing={x['id'] for x in manifest['changes']}
for id,problem,change,requirements,files,tests in rows:
    if id not in existing:
        manifest['changes'].append(dict(id=id, observed_problem=problem, source_theme_ids=[], change=change, requirements=requirements, files=files, acceptance_tests=tests, validation_status='software_tests_only'))
path.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
# Mechanical wording/links in current entry points only; history entries remain unchanged.
path=root/'docs/research-content.gohtml'
text=path.read_text().replace('rc.3 and the first rc.4 candidate remain available, unchanged.', 'rc.3 and both earlier rc.4 candidates remain available, unchanged.').replace('Migration notes</a>.</p>', 'Migration notes</a> · <a class="link" href="/static/research/ai-readiness/rc4-candidate-2/HCAI-v0.1-rc.4-candidate.2.zip">Candidate.2 package</a>.</p>').replace('Read the one-page starting guide','Read the starting guide')
path.write_text(text)
path=root/'docs/research-page-copy.md'
path.write_text(path.read_text().replace('Candidate.2','Candidate.3').replace('fourteen criteria','fifteen criteria').replace('Earlier /rc4-candidate/ URLs','Earlier /rc4-candidate/ and /rc4-candidate-2/ URLs'))
