frappe.ui.form.on("BA Requirement", {
	refresh(frm) {
		frm.add_custom_button("Traceability Tree", () => {
			frappe.set_route("Tree", "BA Requirement");
		});
		if (!frm.is_new()) {
			frm.add_custom_button("New Change Request", () => {
				frappe.new_doc("BA Requirement Change Request", {
					project: frm.doc.project,
					requirement: frm.doc.name,
				});
			});
		}
	},
});
