"""Accessible, offline decision report. Supplied content is always escaped, never executed."""
import html
from .engine import assess, requirement_digest
from .guidance import decision_card


def traceability(a):
    evidence = {e.id: e for e in a.evidence}
    validations = {v.id: v for v in a.workflow.validations}
    rows = []
    for requirement in a.workflow.requirements:
        pairs = []
        for artifact_id in requirement.artifact_ids:
            artifact = evidence[artifact_id]
            checks = [v for v in validations.values() if v.id in requirement.validation_ids and
                      requirement.id in v.requirement_ids and artifact_id in v.artifact_ids]
            pairs.append({"artifact": artifact.model_dump(), "checks": [{**v.model_dump(),
                          "tested_revision_matches": v.tested_artifact_digests.get(artifact_id) == artifact.sha256,
                          "tested_requirement_matches": v.tested_requirement_digests.get(requirement.id) == requirement_digest(a, requirement)} for v in checks]})
        rows.append({"requirement": requirement.model_dump(), "pairs": pairs})
    return rows


def display(value):
    return "Not recorded" if value is None else str(value)


def render_report(a, format="markdown"):
    if format not in ("markdown", "html"):
        raise ValueError("Report format must be markdown or html")
    r = assess(a)
    card = decision_card(a, r)
    # Escape raw HTML and Markdown metacharacters so reports cannot create active links/images.
    def esc(value):
        value = html.escape(display(value), quote=True)
        if format == "markdown":
            for char in ("\\", "`", "*", "_", "[", "]", "|", "#", "!"):
                value = value.replace(char, "\\" + char)
        return value
    sections = []
    def heading(text, level=2):
        sections.append(f'<h{level}>{esc(text)}</h{level}>' if format == 'html' else '#' * level + ' ' + esc(text))
    def paragraph(text):
        sections.append(f'<p>{esc(text)}</p>' if format == 'html' else esc(text))
    def table(headers, rows):
        if format == 'html':
            sections.append('<div class="table-scroll" tabindex="0" role="region" aria-label="'+esc('Table: '+', '.join(headers))+'"><table><thead><tr>' + ''.join('<th scope="col">'+esc(h)+'</th>' for h in headers) + '</tr></thead><tbody>' + ''.join('<tr>'+''.join('<td>'+esc(c)+'</td>' for c in row)+'</tr>' for row in rows) + '</tbody></table></div>')
        else:
            sections.append('\n'.join(['| '+' | '.join(esc(h) for h in headers)+' |', '| '+' | '.join('---' for _ in headers)+' |', *['| '+' | '.join(esc(c) for c in row)+' |' for row in rows]]))
    heading(card['headline'], 1)
    paragraph(card['record_privacy'])
    paragraph(f"{a.run_id} · {a.scope.workflow_name or 'Workflow not yet named'} · {a.versions.protocol}")
    paragraph(card['boundary'])
    table(['Decision', 'Profile needed', 'Risk', 'First stop'], [[card['decision'], card['required_profile'], card['risk'], card['stop_at'] or 'No gate stop']])
    paragraph('Machine checks: structure and decision rules only. Human evidence-quality review: '+r['assurance']['human_quality_review']+'. Evidence authenticity is not independently verified; no criterion certification is issued.')
    heading('Do next')
    step = card['next_step']
    paragraph(step['question'])
    paragraph(f"Owner: {step['owner']}. {step['action']}")
    for attention in card['attention_items']:
        paragraph(f"ATTENTION - {attention['message']} {attention['action']}")
    heading('Six gates - no combined score')
    table(['Gate and criteria', 'Result', 'What is missing or failed'], [[g['title']+' ('+', '.join(g['criteria_ids'])+')', g['status'], '; '.join(g['reasons']) or 'Required checks passed'] for g in card['gates']])
    paragraph('PASS means the structural rules and supplied review judgments satisfy this gate. It does not prove the evidence is true or sufficient in practice. MISSING means gather evidence; FAIL means repair a known problem; NOT_EVALUATED means no conclusion was drawn.')
    heading('Keep these results separate')
    roi, burden = r['roi'], r['evaluator_burden']
    table(['Result', 'Value', 'Interpretation'], [
        ['Gross labor minutes saved / case', roi['gross_minutes_saved_per_case'], 'Before AI-output oversight'],
        ['Oversight minutes / case', roi['oversight_minutes_per_case'], 'Review + correction + escalation + rework'],
        ['Net labor minutes saved / case', roi['net_minutes_saved_per_case'], 'Projected; not measured performance'],
        ['Net operating benefit / period', roi['net_operational_benefit_per_period'], f"{roi['currency'] or 'Currency unknown'} / {roi['period'] or 'period unknown'}; {roi['status']}"],
        ['Preparation elapsed minutes', burden['preparation_elapsed_minutes'], 'Outside the short session, never hidden'],
        ['Review session elapsed minutes', burden['elapsed_minutes'], 'Includes capture/reporting'],
        ['Total evaluation person-minutes', burden['total_person_minutes'], 'Disjoint preparation + evaluator + participant + adjudication'],
        ['Protocol evaluation cost', burden['protocol_evaluation_cost'], burden['currency'] or 'Currency unknown'],
        ['Operational system performance', r['operational_performance']['status'], 'No deployment decision is made by this instrument']])
    paragraph('Missing values are not zero. Money and time are scenario estimates unless separately observed. Evaluation expense is not workflow operating cost.')
    heading('Current workflow - observed versus reported')
    table(['Step', 'Role and action', 'Next / endpoint', 'Basis'], [[s.id, f'{s.actor_role}: {s.action}', ', '.join(s.next_step_ids) or 'Endpoint', s.observation_status] for s in a.baseline.steps])
    heading('People and consequences')
    paragraph('Affected roles: '+', '.join(a.scope.affected_roles or []))
    table(['Review area', 'Applicability and reason', 'Requirements / owner'], [[i.domain, i.applicability+': '+i.rationale, ', '.join(i.requirement_ids)+' / '+display(i.owner_role)] for i in a.workflow.impact_reviews])
    for trigger in r['routing']['context_triggers']:
        paragraph('Risk floor: '+trigger['field']+' requires at least '+trigger['minimum_tier']+' depth.')
    heading('Proposed workflow - connected paths')
    table(['State', 'Behavior', 'Next / endpoint'], [[s.id, s.behavior, ', '.join(s.next_state_ids) or ('Endpoint' if s.terminal else 'Unresolved')] for s in a.workflow.states])
    heading('Inspect requirement -> artifact -> check')
    for row in traceability(a):
        req = row['requirement']
        if format == 'html':
            sections.append('<details><summary>'+esc(req['id']+': '+req['description'])+'</summary>')
        else:
            heading(req['id']+': '+req['description'], 3)
        paragraph('Success condition: '+req['acceptance_criteria'])
        paragraph('Behavior shown: '+req['behavior_status']+'; this label is not inferred from visual fidelity.')
        paragraph(f"Form: {req['form']} | Fit: {req['fit']} | Function: {req['function']}")
        paragraph('Reference records: '+', '.join(req['reference_material_ids']))
        for pair in row['pairs']:
            artifact = pair['artifact']
            paragraph(f"Artifact {artifact['id']} · version {artifact['version']} · SHA-256 {artifact['sha256']}")
            if not pair['checks']:
                paragraph('No linked executed check. Repair this chain.')
            for check in pair['checks']:
                paragraph(f"Check {check['id']}: {check['method']} | {check['level']} | {check['status']} | tested revision matches: {check['tested_revision_matches']} | requirement/context matches: {check['tested_requirement_matches']}")
        if format == 'html':
            sections.append('</details>')
    heading('Bounded owner decision')
    for label, value in [('Owner', card['owner']), ('Engineering step', card['engineering_scope']), ('Resource cap', card['resource_limit']), ('Revisit trigger', card['revisit_when'])]:
        paragraph(label+': '+display(value))
    paragraph('Owner authorization: pending separate dated record. A recommendation alone does not permit deployment.')
    heading('Provenance and limits')
    paragraph('Versions: '+'; '.join(k+' '+v for k,v in a.versions.model_dump().items()))
    paragraph('Input SHA-256: '+card['input_sha256'])
    paragraph('Previous run: '+display(a.previous_run_id)+'; revision: '+display(a.revision_summary))
    paragraph('Evidence digests are supplied and structurally checked, not independently fetched or authenticated. Practitioner correspondence and software tests do not establish empirical effectiveness.')
    if format == 'markdown':
        return '\n\n'.join(sections)+'\n'
    css = 'body{font:17px/1.6 system-ui,sans-serif;color:#172b43;background:#faf9f6;margin:0}main{max-width:1040px;margin:auto;padding:36px 24px}h1{font-size:36px;line-height:1.15;max-width:850px}h2{margin-top:38px;border-top:1px solid #ccd6df;padding-top:20px}p{max-width:80ch;overflow-wrap:anywhere}table{width:100%;border-collapse:collapse;min-width:540px;font-size:15px}th,td{text-align:left;vertical-align:top;padding:12px;border-bottom:1px solid #ccd6df;overflow-wrap:anywhere}th{background:#e8eef4}.table-scroll{overflow:auto}details{border:1px solid #ccd6df;border-radius:8px;padding:16px;margin:12px 0;background:white}summary{cursor:pointer;font-weight:650}summary:focus-visible{outline:3px solid #94580c;outline-offset:4px}@media print{body{background:white}details{break-inside:avoid}.table-scroll{overflow:visible}table{min-width:0;font-size:11px}}'
    return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Private engineering decision record</title><style>'+css+'</style></head><body><main>'+''.join(sections)+'</main></body></html>'
