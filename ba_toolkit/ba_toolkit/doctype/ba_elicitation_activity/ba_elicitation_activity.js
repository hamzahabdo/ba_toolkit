frappe.ui.form.on("BA Elicitation Activity", {
	refresh(frm) {
		if (!frm.is_new() && frm.doc.project) {
			frm.add_custom_button("New Requirement from this Session", () => {
				frappe.new_doc("BA Requirement", {
					project: frm.doc.project,
					source_elicitation: frm.doc.name,
				});
			});
		}
	},
});
