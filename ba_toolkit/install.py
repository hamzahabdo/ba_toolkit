import frappe


def after_install():
	create_roles()
	create_print_format()
	frappe.db.commit()


def create_roles():
	for role_name in ("Business Analyst", "Business Analyst Manager"):
		if not frappe.db.exists("Role", role_name):
			frappe.get_doc({
				"doctype": "Role",
				"role_name": role_name,
				"desk_access": 1,
			}).insert(ignore_permissions=True)


def create_print_format():
	if frappe.db.exists("Print Format", "BA Document - BRD"):
		return

	frappe.get_doc({
		"doctype": "Print Format",
		"name": "BA Document - BRD",
		"doc_type": "BA Document",
		"module": "BA Toolkit",
		"print_format_type": "Jinja",
		"standard": "Yes",
		"disabled": 0,
		"html": BRD_TEMPLATE,
	}).insert(ignore_permissions=True)


BRD_TEMPLATE = r"""
<style>
  .brd-title { text-align: center; margin-bottom: 4px; }
  .brd-subtitle { text-align: center; color: #666; margin-bottom: 30px; }
  .brd-section-title { background: #2e3f6e; color: #fff; padding: 6px 10px; margin-top: 24px; font-size: 13px; }
  .brd-table { width: 100%; border-collapse: collapse; margin-top: 8px; font-size: 11px; }
  .brd-table th, .brd-table td { border: 1px solid #ccc; padding: 5px 8px; text-align: left; vertical-align: top; }
  .brd-table th { background: #f2f2f2; }
  .brd-meta { font-size: 11px; color: #555; margin-bottom: 16px; }
  .sign-block { margin-top: 50px; width: 45%; display: inline-block; }
  .sign-line { border-top: 1px solid #333; margin-top: 40px; padding-top: 4px; font-size: 11px; }
</style>

<h1 class="brd-title">{{ doc.document_title }}</h1>
<div class="brd-subtitle">{{ doc.document_type }} &middot; Version {{ doc.version }} &middot; {{ doc.status }}</div>

<div class="brd-meta">
  <strong>Project:</strong> {{ frappe.db.get_value("Project", doc.project, "project_name") or doc.project }}<br>
  <strong>Prepared by:</strong> {{ frappe.db.get_value("User", doc.prepared_by, "full_name") or doc.prepared_by }}<br>
  <strong>Date:</strong> {{ frappe.utils.formatdate(doc.modified) }}
</div>

{% if doc.executive_summary %}
<div class="brd-section-title">Executive Summary</div>
<div>{{ doc.executive_summary }}</div>
{% endif %}

{% if doc.business_need %}
<div class="brd-section-title">Business Need</div>
<div>{{ frappe.db.get_value("BA Business Need", doc.business_need, "problem_or_opportunity") or "" }}</div>
{% endif %}

{% if doc.included_stakeholders %}
<div class="brd-section-title">Stakeholders</div>
<table class="brd-table">
  <tr><th>Name</th><th>Category</th><th>Influence</th><th>Interest</th></tr>
  {% for row in doc.included_stakeholders %}
  {% set s = frappe.get_doc("BA Stakeholder", row.stakeholder) %}
  <tr>
    <td>{{ s.stakeholder_name }}</td>
    <td>{{ s.stakeholder_category or "" }}</td>
    <td>{{ s.influence_level or "" }}</td>
    <td>{{ s.interest_level or "" }}</td>
  </tr>
  {% endfor %}
</table>
{% endif %}

{% if doc.included_requirements %}
<div class="brd-section-title">Requirements</div>
<table class="brd-table">
  <tr><th>ID</th><th>Title</th><th>Type</th><th>Priority</th><th>Status</th><th>Description</th></tr>
  {% for row in doc.included_requirements %}
  {% set r = frappe.get_doc("BA Requirement", row.requirement) %}
  <tr>
    <td>{{ r.name }}</td>
    <td>{{ r.title }}</td>
    <td>{{ r.requirement_type or "" }}</td>
    <td>{{ r.priority or "" }}</td>
    <td>{{ r.status or "" }}</td>
    <td>{{ r.description or "" }}</td>
  </tr>
  {% endfor %}
</table>
{% endif %}

{% if doc.included_business_rules %}
<div class="brd-section-title">Business Rules</div>
<table class="brd-table">
  <tr><th>Name</th><th>Type</th><th>Statement</th></tr>
  {% for row in doc.included_business_rules %}
  {% set br = frappe.get_doc("BA Business Rule", row.business_rule) %}
  <tr>
    <td>{{ br.rule_name }}</td>
    <td>{{ br.rule_type or "" }}</td>
    <td>{{ br.rule_statement or "" }}</td>
  </tr>
  {% endfor %}
</table>
{% endif %}

{% if doc.approval_notes %}
<div class="brd-section-title">Approval Notes</div>
<div>{{ doc.approval_notes }}</div>
{% endif %}

<div class="sign-block">
  <div class="sign-line">Prepared by &mdash; {{ frappe.db.get_value("User", doc.prepared_by, "full_name") or doc.prepared_by }}</div>
</div>
<div class="sign-block" style="float:right;">
  <div class="sign-line">Approved by</div>
</div>
"""
