# Copyright (c) 2026, Company and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class BAStrategyAnalysis(Document):
	def validate(self):
		self.calculate_risk_ratings()

	def calculate_risk_ratings(self):
		rating_matrix = {
			("High", "High"): "Critical",
			("High", "Medium"): "High",
			("High", "Low"): "Medium",
			("Medium", "High"): "High",
			("Medium", "Medium"): "Medium",
			("Medium", "Low"): "Low",
			("Low", "High"): "Medium",
			("Low", "Medium"): "Low",
			("Low", "Low"): "Low",
		}
		for row in self.risks:
			row.risk_rating = rating_matrix.get((row.likelihood, row.impact), "")
