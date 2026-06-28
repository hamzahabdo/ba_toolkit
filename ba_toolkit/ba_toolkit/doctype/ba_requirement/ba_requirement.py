# Copyright (c) 2026, Storms Digital and contributors
# For license information, please see license.txt

import frappe
from frappe.utils.nestedset import NestedSet


class BARequirement(NestedSet):
	def validate(self):
		# super().validate()
		if self.parent_ba_requirement == self.name:
			frappe.throw("A requirement cannot be its own parent.")
