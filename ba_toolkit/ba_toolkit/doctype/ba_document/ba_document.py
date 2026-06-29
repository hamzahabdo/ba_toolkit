# Copyright (c) 2026, Company and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class BADocument(Document):
	pass

@frappe.whitelist()
def get_project_artifacts(project):
	"""Bulk-fetch all BA artifacts for a project in one query per doctype,
	so a BA Document can be populated without N+1 lookups."""
	if not project:
		frappe.throw("Project is required")

	stakeholders = frappe.get_all(
		"BA Stakeholder",
		filters={"project": project},
		fields=["name", "stakeholder_name", "stakeholder_category"],
	)
	requirements = frappe.get_all(
		"BA Requirement",
		filters={"project": project},
		fields=["name", "title", "requirement_type", "status"],
	)
	business_rules = frappe.get_all(
		"BA Business Rule",
		filters={"project": project},
		fields=["name", "rule_name", "rule_type"],
	)

	return {
		"stakeholders": stakeholders,
		"requirements": requirements,
		"business_rules": business_rules,
	}
