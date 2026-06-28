# Copyright (c) 2026, Storms Digital
#
# Creates one Jinja print format per BA Toolkit main doctype, sharing a consistent
# navy/teal style. Safe to re-run: existing print formats are skipped unless
# overwrite=True is passed.
#
# Fresh installs get these automatically via hooks.after_install.
# On an already-installed site, run:
#   bench --site your-site execute ba_toolkit.print_formats.create_all
# To refresh templates after editing this file on an existing site:
#   bench --site your-site execute ba_toolkit.print_formats.create_all --kwargs "{'overwrite': True}"

import frappe

BASE_CSS = """
<style>
  .pf-title { font-size: 20px; font-weight: bold; color: #1F3354; margin-bottom: 2px; }
  .pf-sub { color: #666; font-size: 12px; margin-bottom: 14px; }
  .pf-meta { font-size: 11px; color: #444; margin-bottom: 10px; line-height: 1.6; }
  .pf-meta b { color: #111; }
  .pf-section { background: #1F3354; color: #fff; padding: 5px 10px; font-size: 12px;
                margin-top: 18px; margin-bottom: 6px; }
  .pf-table { width: 100%; border-collapse: collapse; margin-top: 4px; margin-bottom: 4px; font-size: 11px; }
  .pf-table th, .pf-table td { border: 1px solid #ccc; padding: 5px 8px; text-align: left; vertical-align: top; }
  .pf-table th { background: #EAF1F6; color: #1F3354; }
  .pf-badge { display: inline-block; padding: 2px 8px; border-radius: 10px;
              background: #EAF1F6; color: #1F3354; font-size: 10px; }
  .pf-empty { color: #999; font-style: italic; font-size: 11px; }
  .pf-body { font-size: 12px; line-height: 1.5; }
  .pf-sign { margin-top: 50px; width: 45%; display: inline-block; }
  .pf-sign-line { border-top: 1px solid #333; margin-top: 40px; padding-top: 4px; font-size: 11px; }
</style>
"""

PROJECT_NAME = (
    '{% if doc.project %}{{ frappe.db.get_value("Project", doc.project, "project_name") '
    'or doc.project }}{% else %}\u2014{% endif %}'
)


def tpl(body):
    return BASE_CSS + body


PRINT_FORMATS = {}

# ---------------------------------------------------------------------------
# 1. BA Approach
# ---------------------------------------------------------------------------
PRINT_FORMATS["BA Approach - Print"] = {"doctype": "BA Approach", "html": tpl(f"""
<div class="pf-title">BA Approach</div>
<div class="pf-sub">{{{{ doc.name }}}} &middot; {{{{ doc.ba_approach_type or "" }}}} &middot; <span class="pf-badge">{{{{ doc.status }}}}</span></div>
<div class="pf-meta"><b>Project:</b> {PROJECT_NAME}</div>

{{% if doc.planning_notes %}}
<div class="pf-section">Planning Approach</div>
<div class="pf-body">{{{{ doc.planning_notes }}}}</div>
{{% endif %}}

{{% if doc.stakeholder_engagement_approach %}}
<div class="pf-section">Stakeholder Engagement Approach</div>
<div class="pf-body">{{{{ doc.stakeholder_engagement_approach }}}}</div>
{{% endif %}}

{{% if doc.governance_approach %}}
<div class="pf-section">Governance Approach</div>
<div class="pf-body">{{{{ doc.governance_approach }}}}</div>
{{% endif %}}

{{% if doc.information_management_approach %}}
<div class="pf-section">Information Management Approach</div>
<div class="pf-body">{{{{ doc.information_management_approach }}}}</div>
{{% endif %}}

{{% if doc.performance_improvement_notes %}}
<div class="pf-section">Performance Improvement Notes</div>
<div class="pf-body">{{{{ doc.performance_improvement_notes }}}}</div>
{{% endif %}}
""")}

# ---------------------------------------------------------------------------
# 2. BA Stakeholder
# ---------------------------------------------------------------------------
PRINT_FORMATS["BA Stakeholder - Print"] = {"doctype": "BA Stakeholder", "html": tpl(f"""
<div class="pf-title">{{{{ doc.stakeholder_name }}}}</div>
<div class="pf-sub">{{{{ doc.name }}}} &middot; {{{{ doc.role_title or "" }}}}{{% if doc.organization %}}, {{{{ doc.organization }}}}{{% endif %}}</div>
<div class="pf-meta"><b>Project:</b> {PROJECT_NAME}</div>

<div class="pf-section">Engagement Profile</div>
<table class="pf-table">
  <tr><th>Category</th><th>Influence</th><th>Interest</th><th>Attitude</th></tr>
  <tr>
    <td>{{{{ doc.stakeholder_category or "\u2014" }}}}</td>
    <td>{{{{ doc.influence_level or "\u2014" }}}}</td>
    <td>{{{{ doc.interest_level or "\u2014" }}}}</td>
    <td>{{{{ doc.attitude or "\u2014" }}}}</td>
  </tr>
</table>

{{% if doc.communication_preference %}}
<div class="pf-section">Communication</div>
<div class="pf-body">Preferred channel: {{{{ doc.communication_preference }}}}</div>
{{% endif %}}

{{% if doc.engagement_approach %}}
<div class="pf-section">Engagement Approach</div>
<div class="pf-body">{{{{ doc.engagement_approach }}}}</div>
{{% endif %}}

{{% if doc.notes %}}
<div class="pf-section">Notes</div>
<div class="pf-body">{{{{ doc.notes }}}}</div>
{{% endif %}}
""")}

# ---------------------------------------------------------------------------
# 3. BA Elicitation Activity
# ---------------------------------------------------------------------------
PRINT_FORMATS["BA Elicitation Activity - Print"] = {"doctype": "BA Elicitation Activity", "html": tpl(f"""
<div class="pf-title">{{{{ doc.activity_title }}}}</div>
<div class="pf-sub">{{{{ doc.name }}}} &middot; {{{{ doc.technique or "" }}}} &middot; <span class="pf-badge">{{{{ doc.status }}}}</span></div>
<div class="pf-meta">
  <b>Project:</b> {PROJECT_NAME}<br>
  <b>Date:</b> {{{{ frappe.utils.formatdate(doc.activity_date) if doc.activity_date else "\u2014" }}}}<br>
  <b>Facilitator:</b> {{{{ frappe.db.get_value("User", doc.facilitator, "full_name") or doc.facilitator or "\u2014" }}}}
</div>

{{% if doc.objective %}}
<div class="pf-section">Objective</div>
<div class="pf-body">{{{{ doc.objective }}}}</div>
{{% endif %}}

{{% if doc.agenda %}}
<div class="pf-section">Agenda</div>
<div class="pf-body">{{{{ doc.agenda }}}}</div>
{{% endif %}}

<div class="pf-section">Participants</div>
{{% if doc.participants %}}
<table class="pf-table">
  <tr><th>Stakeholder</th><th>Role in Session</th><th>Attended</th></tr>
  {{% for row in doc.participants %}}
  {{% set sh = frappe.db.get_value("BA Stakeholder", row.stakeholder, "stakeholder_name") %}}
  <tr>
    <td>{{{{ sh or row.stakeholder }}}}</td>
    <td>{{{{ row.role_in_session or "\u2014" }}}}</td>
    <td>{{{{ "Yes" if row.attended else "No" }}}}</td>
  </tr>
  {{% endfor %}}
</table>
{{% else %}}
<div class="pf-empty">No participants recorded.</div>
{{% endif %}}

{{% if doc.key_findings %}}
<div class="pf-section">Key Findings</div>
<div class="pf-body">{{{{ doc.key_findings }}}}</div>
{{% endif %}}

{{% if doc.follow_up_actions %}}
<div class="pf-section">Follow-up Actions</div>
<div class="pf-body">{{{{ doc.follow_up_actions }}}}</div>
{{% endif %}}
""")}

# ---------------------------------------------------------------------------
# 4. BA Requirement
# ---------------------------------------------------------------------------
PRINT_FORMATS["BA Requirement - Print"] = {"doctype": "BA Requirement", "html": tpl(f"""
<div class="pf-title">{{{{ doc.title }}}}</div>
<div class="pf-sub">{{{{ doc.name }}}} &middot; {{{{ doc.requirement_type or "" }}}} &middot; <span class="pf-badge">{{{{ doc.status }}}}</span></div>
<div class="pf-meta">
  <b>Project:</b> {PROJECT_NAME}<br>
  <b>Priority:</b> {{{{ doc.priority or "\u2014" }}}} &nbsp;&nbsp; <b>Version:</b> {{{{ doc.version or "1.0" }}}}<br>
  {{% if doc.parent_ba_requirement %}}<b>Parent requirement:</b> {{{{ frappe.db.get_value("BA Requirement", doc.parent_ba_requirement, "title") or doc.parent_ba_requirement }}}}<br>{{% endif %}}
  {{% if doc.owner_stakeholder %}}<b>Owning stakeholder:</b> {{{{ frappe.db.get_value("BA Stakeholder", doc.owner_stakeholder, "stakeholder_name") or doc.owner_stakeholder }}}}<br>{{% endif %}}
  {{% if doc.source_elicitation %}}<b>Source:</b> {{{{ frappe.db.get_value("BA Elicitation Activity", doc.source_elicitation, "activity_title") or doc.source_elicitation }}}}<br>{{% endif %}}
  {{% if doc.business_need %}}<b>Business need:</b> {{{{ frappe.db.get_value("BA Business Need", doc.business_need, "need_title") or doc.business_need }}}}{{% endif %}}
</div>

{{% if doc.description %}}
<div class="pf-section">Description</div>
<div class="pf-body">{{{{ doc.description }}}}</div>
{{% endif %}}

<div class="pf-section">Acceptance Criteria</div>
{{% if doc.acceptance_criteria %}}
<table class="pf-table">
  <tr><th>Criterion</th><th>Status</th></tr>
  {{% for row in doc.acceptance_criteria %}}
  <tr><td>{{{{ row.criterion }}}}</td><td>{{{{ row.status }}}}</td></tr>
  {{% endfor %}}
</table>
{{% else %}}
<div class="pf-empty">No acceptance criteria recorded.</div>
{{% endif %}}
""")}

# ---------------------------------------------------------------------------
# 5. BA Requirement Change Request
# ---------------------------------------------------------------------------
PRINT_FORMATS["BA Requirement Change Request - Print"] = {"doctype": "BA Requirement Change Request", "html": tpl(f"""
<div class="pf-title">Change Request {{{{ doc.name }}}}</div>
<div class="pf-sub">Against: {{{{ frappe.db.get_value("BA Requirement", doc.requirement, "title") or doc.requirement }}}} &middot; <span class="pf-badge">{{{{ doc.status }}}}</span></div>
<div class="pf-meta">
  <b>Project:</b> {PROJECT_NAME}<br>
  <b>Requested by:</b> {{{{ frappe.db.get_value("User", doc.requested_by, "full_name") or doc.requested_by or "\u2014" }}}} &nbsp;&nbsp;
  <b>Date:</b> {{{{ frappe.utils.formatdate(doc.request_date) if doc.request_date else "\u2014" }}}}
</div>

{{% if doc.change_description %}}
<div class="pf-section">Change Description</div>
<div class="pf-body">{{{{ doc.change_description }}}}</div>
{{% endif %}}

{{% if doc.justification %}}
<div class="pf-section">Justification</div>
<div class="pf-body">{{{{ doc.justification }}}}</div>
{{% endif %}}

{{% if doc.impact_analysis %}}
<div class="pf-section">Impact Analysis</div>
<div class="pf-body">{{{{ doc.impact_analysis }}}}</div>
{{% endif %}}

<div class="pf-section">Decision</div>
<div class="pf-body">{{{{ doc.decision_notes or "Pending." }}}}</div>

<div class="pf-sign">
  <div class="pf-sign-line">Approved by</div>
</div>
""")}

# ---------------------------------------------------------------------------
# 6. BA Business Need
# ---------------------------------------------------------------------------
PRINT_FORMATS["BA Business Need - Print"] = {"doctype": "BA Business Need", "html": tpl(f"""
<div class="pf-title">{{{{ doc.need_title }}}}</div>
<div class="pf-sub">{{{{ doc.name }}}} &middot; <span class="pf-badge">{{{{ doc.status }}}}</span></div>
<div class="pf-meta"><b>Project:</b> {PROJECT_NAME}</div>

{{% if doc.problem_or_opportunity %}}
<div class="pf-section">Problem or Opportunity Statement</div>
<div class="pf-body">{{{{ doc.problem_or_opportunity }}}}</div>
{{% endif %}}

{{% if doc.business_goals %}}
<div class="pf-section">Business Goals</div>
<div class="pf-body">{{{{ doc.business_goals }}}}</div>
{{% endif %}}

{{% if doc.desired_outcomes %}}
<div class="pf-section">Desired Outcomes</div>
<div class="pf-body">{{{{ doc.desired_outcomes }}}}</div>
{{% endif %}}
""")}

# ---------------------------------------------------------------------------
# 7. BA Strategy Analysis
# ---------------------------------------------------------------------------
PRINT_FORMATS["BA Strategy Analysis - Print"] = {"doctype": "BA Strategy Analysis", "html": tpl(f"""
<div class="pf-title">Strategy Analysis</div>
<div class="pf-sub">{{{{ doc.name }}}}</div>
<div class="pf-meta">
  <b>Project:</b> {PROJECT_NAME}<br>
  {{% if doc.business_need %}}<b>Business need:</b> {{{{ frappe.db.get_value("BA Business Need", doc.business_need, "need_title") or doc.business_need }}}}{{% endif %}}
</div>

{{% if doc.current_state_description %}}
<div class="pf-section">Current State</div>
<div class="pf-body">{{{{ doc.current_state_description }}}}</div>
{{% endif %}}

{{% if doc.capability_gaps %}}
<table class="pf-table">
  <tr><th>Capability Area</th><th>Current State</th><th>Desired State</th><th>Gap</th></tr>
  {{% for row in doc.capability_gaps %}}
  <tr>
    <td>{{{{ row.capability_area or "\u2014" }}}}</td>
    <td>{{{{ row.current_state or "\u2014" }}}}</td>
    <td>{{{{ row.desired_state or "\u2014" }}}}</td>
    <td>{{{{ row.gap_description or "\u2014" }}}}</td>
  </tr>
  {{% endfor %}}
</table>
{{% endif %}}

{{% if doc.future_state_description %}}
<div class="pf-section">Future State</div>
<div class="pf-body">{{{{ doc.future_state_description }}}}</div>
{{% endif %}}
{{% if doc.new_capabilities_required %}}
<div class="pf-body"><b>New capabilities required:</b> {{{{ doc.new_capabilities_required }}}}</div>
{{% endif %}}

{{% if doc.scope_statement or doc.constraints or doc.assumptions %}}
<div class="pf-section">Scope</div>
{{% if doc.scope_statement %}}<div class="pf-body">{{{{ doc.scope_statement }}}}</div>{{% endif %}}
{{% if doc.constraints %}}<div class="pf-body"><b>Constraints:</b> {{{{ doc.constraints }}}}</div>{{% endif %}}
{{% if doc.assumptions %}}<div class="pf-body"><b>Assumptions:</b> {{{{ doc.assumptions }}}}</div>{{% endif %}}
{{% endif %}}

{{% if doc.risks %}}
<div class="pf-section">Risks</div>
<table class="pf-table">
  <tr><th>Risk</th><th>Likelihood</th><th>Impact</th><th>Rating</th><th>Mitigation</th></tr>
  {{% for row in doc.risks %}}
  <tr>
    <td>{{{{ row.risk_description }}}}</td>
    <td>{{{{ row.likelihood or "\u2014" }}}}</td>
    <td>{{{{ row.impact or "\u2014" }}}}</td>
    <td>{{{{ row.risk_rating or "\u2014" }}}}</td>
    <td>{{{{ row.mitigation_strategy or "\u2014" }}}}</td>
  </tr>
  {{% endfor %}}
</table>
{{% endif %}}

{{% if doc.change_strategy %}}
<div class="pf-section">Change Strategy</div>
<div class="pf-body">{{{{ doc.change_strategy }}}}</div>
{{% endif %}}
""")}

# ---------------------------------------------------------------------------
# 8. BA Business Rule
# ---------------------------------------------------------------------------
PRINT_FORMATS["BA Business Rule - Print"] = {"doctype": "BA Business Rule", "html": tpl(f"""
<div class="pf-title">{{{{ doc.rule_name }}}}</div>
<div class="pf-sub">{{{{ doc.name }}}} &middot; {{{{ doc.rule_type or "" }}}} &middot; <span class="pf-badge">{{{{ doc.status }}}}</span></div>
<div class="pf-meta">
  <b>Project:</b> {PROJECT_NAME}<br>
  {{% if doc.source %}}<b>Source:</b> {{{{ doc.source }}}}<br>{{% endif %}}
  {{% if doc.related_requirement %}}<b>Related requirement:</b> {{{{ frappe.db.get_value("BA Requirement", doc.related_requirement, "title") or doc.related_requirement }}}}{{% endif %}}
</div>

<div class="pf-section">Rule Statement</div>
<div class="pf-body">{{{{ doc.rule_statement }}}}</div>
""")}

# ---------------------------------------------------------------------------
# 9. BA Use Case
# ---------------------------------------------------------------------------
PRINT_FORMATS["BA Use Case - Print"] = {"doctype": "BA Use Case", "html": tpl(f"""
<div class="pf-title">{{{{ doc.use_case_name }}}}</div>
<div class="pf-sub">{{{{ doc.name }}}}{{% if doc.primary_actor %}} &middot; Actor: {{{{ doc.primary_actor }}}}{{% endif %}}</div>
<div class="pf-meta">
  <b>Project:</b> {PROJECT_NAME}<br>
  {{% if doc.related_requirement %}}<b>Related requirement:</b> {{{{ frappe.db.get_value("BA Requirement", doc.related_requirement, "title") or doc.related_requirement }}}}{{% endif %}}
</div>

{{% if doc.description %}}<div class="pf-body">{{{{ doc.description }}}}</div>{{% endif %}}
{{% if doc.preconditions %}}<div class="pf-body"><b>Preconditions:</b> {{{{ doc.preconditions }}}}</div>{{% endif %}}

<div class="pf-section">Main Flow</div>
{{% if doc.main_flow %}}
<table class="pf-table">
  <tr><th style="width:8%">#</th><th>Actor Action</th><th>System Response</th></tr>
  {{% for row in doc.main_flow %}}
  <tr><td>{{{{ row.step_no }}}}</td><td>{{{{ row.actor_action }}}}</td><td>{{{{ row.system_response }}}}</td></tr>
  {{% endfor %}}
</table>
{{% else %}}
<div class="pf-empty">No flow steps recorded.</div>
{{% endif %}}

{{% if doc.alternate_flows %}}
<div class="pf-section">Alternate / Exception Flows</div>
<div class="pf-body">{{{{ doc.alternate_flows }}}}</div>
{{% endif %}}

{{% if doc.postconditions %}}
<div class="pf-section">Postconditions</div>
<div class="pf-body">{{{{ doc.postconditions }}}}</div>
{{% endif %}}
""")}

# ---------------------------------------------------------------------------
# 10. BA User Story
# ---------------------------------------------------------------------------
PRINT_FORMATS["BA User Story - Print"] = {"doctype": "BA User Story", "html": tpl(f"""
<div class="pf-title">{{{{ doc.story_title }}}}</div>
<div class="pf-sub">{{{{ doc.name }}}} &middot; {{{{ doc.priority or "" }}}} &middot; <span class="pf-badge">{{{{ doc.status }}}}</span>{{% if doc.story_points %}} &middot; {{{{ doc.story_points }}}} pts{{% endif %}}</div>
<div class="pf-meta">
  <b>Project:</b> {PROJECT_NAME}<br>
  {{% if doc.related_requirement %}}<b>Related requirement:</b> {{{{ frappe.db.get_value("BA Requirement", doc.related_requirement, "title") or doc.related_requirement }}}}{{% endif %}}
</div>

<div class="pf-section">Story</div>
<div class="pf-body">
  <b>As a</b> {{{{ doc.as_a }}}}<br>
  <b>I want</b> {{{{ doc.i_want }}}}<br>
  <b>So that</b> {{{{ doc.so_that }}}}
</div>

<div class="pf-section">Acceptance Criteria</div>
{{% if doc.acceptance_criteria %}}
<table class="pf-table">
  <tr><th>Criterion</th><th>Status</th></tr>
  {{% for row in doc.acceptance_criteria %}}
  <tr><td>{{{{ row.criterion }}}}</td><td>{{{{ row.status }}}}</td></tr>
  {{% endfor %}}
</table>
{{% else %}}
<div class="pf-empty">No acceptance criteria recorded.</div>
{{% endif %}}
""")}

# ---------------------------------------------------------------------------
# 11. BA Process Model
# ---------------------------------------------------------------------------
PRINT_FORMATS["BA Process Model - Print"] = {"doctype": "BA Process Model", "html": tpl(f"""
<div class="pf-title">{{{{ doc.process_name }}}}</div>
<div class="pf-sub">{{{{ doc.name }}}}</div>
<div class="pf-meta">
  <b>Project:</b> {PROJECT_NAME}<br>
  {{% if doc.related_requirement %}}<b>Related requirement:</b> {{{{ frappe.db.get_value("BA Requirement", doc.related_requirement, "title") or doc.related_requirement }}}}{{% endif %}}
</div>

{{% if doc.as_is_description %}}
<div class="pf-section">As-Is</div>
<div class="pf-body">{{{{ doc.as_is_description }}}}</div>
{{% endif %}}

{{% if doc.to_be_description %}}
<div class="pf-section">To-Be</div>
<div class="pf-body">{{{{ doc.to_be_description }}}}</div>
{{% endif %}}

{{% if doc.diagram %}}
<div class="pf-section">Diagram</div>
<img src="{{{{ doc.diagram }}}}" style="max-width: 100%; border: 1px solid #ccc;">
{{% endif %}}

{{% if doc.swimlane_notes %}}
<div class="pf-section">Swimlane / RACI Notes</div>
<div class="pf-body">{{{{ doc.swimlane_notes }}}}</div>
{{% endif %}}
""")}

# ---------------------------------------------------------------------------
# 12. BA Glossary Term
# ---------------------------------------------------------------------------
PRINT_FORMATS["BA Glossary Term - Print"] = {"doctype": "BA Glossary Term", "html": tpl(f"""
<div class="pf-title">{{{{ doc.term }}}}</div>
<div class="pf-sub">{{{{ doc.name }}}}{{% if doc.synonyms %}} &middot; Also known as: {{{{ doc.synonyms }}}}{{% endif %}}</div>
<div class="pf-meta">
  {{% if doc.project %}}<b>Project:</b> {PROJECT_NAME}<br>{{% else %}}<b>Scope:</b> Organization-wide<br>{{% endif %}}
  {{% if doc.related_requirement %}}<b>Related requirement:</b> {{{{ frappe.db.get_value("BA Requirement", doc.related_requirement, "title") or doc.related_requirement }}}}{{% endif %}}
</div>

<div class="pf-section">Definition</div>
<div class="pf-body">{{{{ doc.definition }}}}</div>
""")}

# ---------------------------------------------------------------------------
# 13. BA Solution Evaluation
# ---------------------------------------------------------------------------
PRINT_FORMATS["BA Solution Evaluation - Print"] = {"doctype": "BA Solution Evaluation", "html": tpl(f"""
<div class="pf-title">{{{{ doc.solution_name }}}}</div>
<div class="pf-sub">{{{{ doc.name }}}} &middot; <span class="pf-badge">{{{{ doc.status }}}}</span></div>
<div class="pf-meta">
  <b>Project:</b> {PROJECT_NAME}<br>
  <b>Evaluation date:</b> {{{{ frappe.utils.formatdate(doc.evaluation_date) if doc.evaluation_date else "\u2014" }}}} &nbsp;&nbsp;
  <b>Method:</b> {{{{ doc.evaluation_method or "\u2014" }}}}
</div>

<div class="pf-section">Performance Measures</div>
{{% if doc.performance_measures %}}
<table class="pf-table">
  <tr><th>Metric</th><th>Target</th><th>Actual</th><th>Notes</th></tr>
  {{% for row in doc.performance_measures %}}
  <tr>
    <td>{{{{ row.metric_name }}}}</td>
    <td>{{{{ row.target_value or "\u2014" }}}}</td>
    <td>{{{{ row.actual_value or "\u2014" }}}}</td>
    <td>{{{{ row.variance_notes or "\u2014" }}}}</td>
  </tr>
  {{% endfor %}}
</table>
{{% else %}}
<div class="pf-empty">No performance measures recorded.</div>
{{% endif %}}

{{% if doc.findings %}}
<div class="pf-section">Findings</div>
<div class="pf-body">{{{{ doc.findings }}}}</div>
{{% endif %}}

{{% if doc.recommendations %}}
<div class="pf-section">Recommendations</div>
<div class="pf-body">{{{{ doc.recommendations }}}}</div>
{{% endif %}}
""")}

# ---------------------------------------------------------------------------
# 14. BA Document (BRD / FRD / Vision & Scope / Business Case)
# ---------------------------------------------------------------------------
PRINT_FORMATS["BA Document - BRD"] = {"doctype": "BA Document", "html": tpl(f"""
<div class="pf-title">{{{{ doc.document_title }}}}</div>
<div class="pf-sub">{{{{ doc.document_type }}}} &middot; Version {{{{ doc.version }}}} &middot; <span class="pf-badge">{{{{ doc.status }}}}</span></div>
<div class="pf-meta">
  <b>Project:</b> {PROJECT_NAME}<br>
  <b>Prepared by:</b> {{{{ frappe.db.get_value("User", doc.prepared_by, "full_name") or doc.prepared_by }}}} &nbsp;&nbsp;
  <b>Date:</b> {{{{ frappe.utils.formatdate(doc.modified) }}}}
</div>

{{% if doc.executive_summary %}}
<div class="pf-section">Executive Summary</div>
<div class="pf-body">{{{{ doc.executive_summary }}}}</div>
{{% endif %}}

{{% if doc.business_need %}}
<div class="pf-section">Business Need</div>
<div class="pf-body">{{{{ frappe.db.get_value("BA Business Need", doc.business_need, "problem_or_opportunity") or "" }}}}</div>
{{% endif %}}

{{% if doc.included_stakeholders %}}
<div class="pf-section">Stakeholders</div>
<table class="pf-table">
  <tr><th>Name</th><th>Category</th><th>Influence</th><th>Interest</th></tr>
  {{% for row in doc.included_stakeholders %}}
  {{% set sd = frappe.get_doc("BA Stakeholder", row.stakeholder) %}}
  <tr>
    <td>{{{{ sd.stakeholder_name }}}}</td>
    <td>{{{{ sd.stakeholder_category or "" }}}}</td>
    <td>{{{{ sd.influence_level or "" }}}}</td>
    <td>{{{{ sd.interest_level or "" }}}}</td>
  </tr>
  {{% endfor %}}
</table>
{{% endif %}}

{{% if doc.included_requirements %}}
<div class="pf-section">Requirements</div>
<table class="pf-table">
  <tr><th>ID</th><th>Title</th><th>Type</th><th>Priority</th><th>Status</th><th>Description</th></tr>
  {{% for row in doc.included_requirements %}}
  {{% set rd = frappe.get_doc("BA Requirement", row.requirement) %}}
  <tr>
    <td>{{{{ rd.name }}}}</td>
    <td>{{{{ rd.title }}}}</td>
    <td>{{{{ rd.requirement_type or "" }}}}</td>
    <td>{{{{ rd.priority or "" }}}}</td>
    <td>{{{{ rd.status or "" }}}}</td>
    <td>{{{{ rd.description or "" }}}}</td>
  </tr>
  {{% endfor %}}
</table>
{{% endif %}}

{{% if doc.included_business_rules %}}
<div class="pf-section">Business Rules</div>
<table class="pf-table">
  <tr><th>Name</th><th>Type</th><th>Statement</th></tr>
  {{% for row in doc.included_business_rules %}}
  {{% set brd = frappe.get_doc("BA Business Rule", row.business_rule) %}}
  <tr>
    <td>{{{{ brd.rule_name }}}}</td>
    <td>{{{{ brd.rule_type or "" }}}}</td>
    <td>{{{{ brd.rule_statement or "" }}}}</td>
  </tr>
  {{% endfor %}}
</table>
{{% endif %}}

{{% if doc.approval_notes %}}
<div class="pf-section">Approval Notes</div>
<div class="pf-body">{{{{ doc.approval_notes }}}}</div>
{{% endif %}}

<div class="pf-sign">
  <div class="pf-sign-line">Prepared by &mdash; {{{{ frappe.db.get_value("User", doc.prepared_by, "full_name") or doc.prepared_by }}}}</div>
</div>
<div class="pf-sign" style="float:right;">
  <div class="pf-sign-line">Approved by</div>
</div>
""")}


def create_all(overwrite=False):
	created, skipped, updated = 0, 0, 0
	for name, spec in PRINT_FORMATS.items():
		if frappe.db.exists("Print Format", name):
			if overwrite:
				pf = frappe.get_doc("Print Format", name)
				pf.html = spec["html"]
				pf.save(ignore_permissions=True)
				updated += 1
			else:
				skipped += 1
			continue

		frappe.get_doc({
			"doctype": "Print Format",
			"name": name,
			"doc_type": spec["doctype"],
			"module": "BA Toolkit",
			"print_format_type": "Jinja",
			"standard": "Yes",
			"disabled": 0,
			"html": spec["html"],
		}).insert(ignore_permissions=True)
		created += 1

	frappe.db.commit()
	print(f"Print formats: {created} created, {updated} updated, {skipped} skipped (already existed).")


def run():
	create_all()
