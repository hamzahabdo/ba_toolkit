frappe.ui.form.on("BA Document", {
	refresh(frm) {
		if (frm.doc.project) {
			frm.add_custom_button("Pull Project Artifacts", () => {
				frappe.call({
					method: "ba_toolkit.ba_toolkit.doctype.ba_document.ba_document.get_project_artifacts",
					args: { project: frm.doc.project },
					callback(r) {
						if (!r.message) return;

						frm.clear_table("included_stakeholders");
						(r.message.stakeholders || []).forEach((s) => {
							let row = frm.add_child("included_stakeholders");
							row.stakeholder = s.name;
						});

						frm.clear_table("included_requirements");
						(r.message.requirements || []).forEach((req) => {
							let row = frm.add_child("included_requirements");
							row.requirement = req.name;
						});

						frm.clear_table("included_business_rules");
						(r.message.business_rules || []).forEach((rule) => {
							let row = frm.add_child("included_business_rules");
							row.business_rule = rule.name;
						});

						frm.refresh_fields();
						frappe.show_alert({ message: "Pulled latest project artifacts", indicator: "green" });
					},
				});
			}, "BA Toolkit");
		}
	},
});
