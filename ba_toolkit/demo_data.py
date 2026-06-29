# Copyright (c) 2026, Company
#
# Seeds a complete, realistic BA Toolkit dataset for an "Employee Loans" project —
# documenting the BA work behind the standalone employee_loans app (EL-prefixed doctypes:
# EL Loan Application, EL Loan Type, EL Repayment Schedule, etc).
#
# Run with:
#   bench --site your-site execute ba_toolkit.demo_data.run
#
# Safe to re-run: it checks for an existing BA Approach on the project and skips if found.

import frappe

PROJECT_NAME = "Employee Loans"


def run():
	project = get_or_create_project()

	if frappe.db.exists("BA Approach", {"project": project}):
		print(f"Demo data already exists for project '{project}'. Skipping.")
		return

	user = frappe.session.user

	stakeholders = create_stakeholders(project)
	create_approach(project)
	elicitations = create_elicitation_activities(project, stakeholders, user)
	business_need = create_business_need(project)
	create_strategy_analysis(project, business_need, stakeholders)
	requirements = create_requirements(project, elicitations, business_need, stakeholders)
	create_business_rules(project, requirements)
	create_use_case(project, requirements)
	create_user_stories(project, requirements)
	create_process_model(project, requirements)
	create_glossary_terms(project, requirements)
	create_change_request(project, requirements, user)
	create_solution_evaluation(project)
	create_ba_document(project, stakeholders, requirements, business_need, user)

	frappe.db.commit()
	print(f"Demo data created for project '{project}':")
	print(f"  Stakeholders: {len(stakeholders)}")
	print(f"  Elicitation activities: {len(elicitations)}")
	print(f"  Requirements: {len(requirements)}")


def get_or_create_project():
	existing = frappe.db.get_value("Project", {"project_name": PROJECT_NAME}, "name")
	if existing:
		return existing

	company = frappe.db.get_value("Company", {}, "name")

	project = frappe.get_doc({
		"doctype": "Project",
		"project_name": PROJECT_NAME,
		"status": "Open",
		"priority": "Medium",
		"company": company,
		"notes": "Standalone Frappe app for employee loan requests, approval, and payroll-linked repayment.",
	})
	project.insert(ignore_permissions=True, ignore_mandatory=True)
	return project.name


def create_stakeholders(project):
	rows = [
		dict(stakeholder_name="Noura Al-Sahli", role_title="HR Manager", organization="Alfa",
			 stakeholder_category="Sponsor", influence_level="High", interest_level="High",
			 attitude="Champion", communication_preference="Meetings",
			 engagement_approach="Brief weekly during build; sign-off authority on policy rules.",
			 notes="Owns the loan policy; wants this live before next Ramadan advance-salary season."),
		dict(stakeholder_name="Faisal Otaibi", role_title="Payroll Officer", organization="Alfa",
			 stakeholder_category="Subject Matter Expert", influence_level="High", interest_level="High",
			 attitude="Supporter", communication_preference="Workshops",
			 engagement_approach="Deep-dive sessions on deduction rules and WPS/salary slip integration.",
			 notes="Currently tracks loans in a shared Excel sheet — main pain point owner."),
		dict(stakeholder_name="Lina Haddad", role_title="Finance Controller", organization="Alfa",
			 stakeholder_category="Business Owner", influence_level="High", interest_level="Medium",
			 attitude="Neutral", communication_preference="Written Reports",
			 engagement_approach="Monthly summary; cares about outstanding balance reporting and GL impact.",
			 notes="Wants outstanding loan balances reconcilable against the GL each month-end."),
		dict(stakeholder_name="Yousef Al-Harbi", role_title="Site Technician (employee representative)",
			 organization="Alfa", stakeholder_category="End User", influence_level="Medium",
			 interest_level="High", attitude="Supporter", communication_preference="Email",
			 engagement_approach="Represents the typical employee applying for a loan via mobile.",
			 notes="Wants a simple mobile-friendly request form with status tracking."),
		dict(stakeholder_name="Sara Qassim", role_title="ERPNext System Administrator",
			 organization="Storms Digital", stakeholder_category="Project Team", influence_level="Medium",
			 interest_level="Medium", attitude="Supporter", communication_preference="Meetings",
			 engagement_approach="Technical reviewer for the EL-prefixed doctypes and Salary Slip integration.",
			 notes="Will own the app post-go-live alongside Storms Digital support."),
	]
	created = []
	for r in rows:
		doc = frappe.get_doc({"doctype": "BA Stakeholder", "project": project, **r})
		doc.insert(ignore_permissions=True)
		created.append(doc)
	return created


def s(stakeholders, name):
	return next(d for d in stakeholders if d.stakeholder_name == name)


def create_approach(project):
	doc = frappe.get_doc({
		"doctype": "BA Approach",
		"project": project,
		"ba_approach_type": "Hybrid",
		"status": "Active",
		"planning_notes": (
			"Plan-driven for the payroll-integration and policy-rule pieces (fixed, regulated scope); "
			"adaptive for the employee-facing request portal, iterated with HR and a small pilot group."
		),
		"stakeholder_engagement_approach": (
			"Weekly check-in with HR Manager and Payroll Officer during build. Finance Controller reviewed "
			"at the strategy analysis and BRD sign-off milestones only, given lower day-to-day interest."
		),
		"governance_approach": (
			"HR Manager has final approval on policy-rule requirements (loan caps, deduction limits). "
			"Change requests against approved requirements go through Finance Controller sign-off if they "
			"affect payroll deduction logic."
		),
		"information_management_approach": (
			"All BA artifacts tracked in BA Toolkit against the Employee Loans project. Requirements use the "
			"BA-REQ traceability tree; design artifacts (rules, stories, process model) link back via "
			"Related Requirement so the BRD can be regenerated at any time from current data."
		),
		"performance_improvement_notes": (
			"Retro after pilot: elicitation with Payroll Officer ran long because deduction edge cases "
			"(partial month, mid-cycle resignation) weren't scoped up front — added a dedicated interview "
			"for exception handling before finalizing requirements next time."
		),
	})
	doc.insert(ignore_permissions=True)
	return doc


def create_elicitation_activities(project, stakeholders, user):
	acts = []

	a1 = frappe.get_doc({
		"doctype": "BA Elicitation Activity",
		"project": project,
		"activity_title": "Employee Loans kickoff workshop",
		"technique": "Workshop",
		"activity_date": "2026-05-18",
		"facilitator": user,
		"status": "Completed",
		"objective": "Align HR, Payroll and Finance on scope and current pain points before requirements work starts.",
		"agenda": "1) Current process walkthrough 2) Pain points 3) Must-have vs nice-to-have scope 4) Next steps",
		"key_findings": (
			"Loan requests currently move via email + a shared Excel tracker. No visibility for employees into "
			"their own outstanding balance. Payroll manually edits each Salary Slip to apply deductions, which "
			"has caused at least two repayment errors in the last six months."
		),
		"follow_up_actions": "Schedule a dedicated payroll interview to map deduction and repayment mechanics.",
	})
	a1.append("participants", {"stakeholder": s(stakeholders, "Noura Al-Sahli").name,
							 "role_in_session": "Sponsor", "attended": 1})
	a1.append("participants", {"stakeholder": s(stakeholders, "Faisal Otaibi").name,
							 "role_in_session": "SME", "attended": 1})
	a1.append("participants", {"stakeholder": s(stakeholders, "Lina Haddad").name,
							 "role_in_session": "Business owner", "attended": 1})
	a1.insert(ignore_permissions=True)
	acts.append(a1)

	a2 = frappe.get_doc({
		"doctype": "BA Elicitation Activity",
		"project": project,
		"activity_title": "Payroll deduction & repayment mechanics interview",
		"technique": "Interview",
		"activity_date": "2026-05-25",
		"facilitator": user,
		"status": "Completed",
		"objective": "Understand exactly how loan deductions should interact with Salary Slip, GOSI, and net pay.",
		"agenda": "Walk through 3 real loan cases: full-term repayment, early settlement, mid-cycle resignation.",
		"key_findings": (
			"Deduction must be capped so net pay after deduction never drops below a configurable minimum "
			"(currently informal practice: never below 70% of net salary). On resignation, outstanding balance "
			"should auto-offset against final settlement / EOSB before payout."
		),
		"follow_up_actions": "Draft the deduction-cap business rule and validate the wording with Faisal before sign-off.",
	})
	a2.append("participants", {"stakeholder": s(stakeholders, "Faisal Otaibi").name,
							 "role_in_session": "SME", "attended": 1})
	a2.insert(ignore_permissions=True)
	acts.append(a2)

	a3 = frappe.get_doc({
		"doctype": "BA Elicitation Activity",
		"project": project,
		"activity_title": "Existing loan request form & tracker review",
		"technique": "Document Analysis",
		"activity_date": "2026-06-02",
		"facilitator": user,
		"status": "Completed",
		"objective": "Review the current Excel tracker and email-based request form to identify required data fields.",
		"agenda": "Field-by-field review of the existing tracker against what HR actually uses for decisions.",
		"key_findings": (
			"Current tracker has no audit trail of approvals — just a status column anyone can edit. "
			"Loan type (advance vs personal loan) is recorded inconsistently, which affects whether interest-free "
			"rules apply."
		),
		"follow_up_actions": "Carry the loan-type distinction into the EL Loan Type doctype design.",
	})
	a3.append("participants", {"stakeholder": s(stakeholders, "Yousef Al-Harbi").name,
							 "role_in_session": "End-user perspective", "attended": 1})
	a3.insert(ignore_permissions=True)
	acts.append(a3)

	return acts


def create_business_need(project):
	doc = frappe.get_doc({
		"doctype": "BA Business Need",
		"project": project,
		"need_title": "Replace manual, spreadsheet-based employee loan tracking",
		"status": "Validated",
		"problem_or_opportunity": (
			"Employee loan requests, approvals, and repayment deductions are currently managed through email "
			"and a shared Excel tracker maintained by Payroll. This has caused repayment calculation errors, "
			"gives employees no visibility into their own balance, and leaves no auditable approval trail. "
			"As headcount grows, the manual process will not scale and the error rate will increase."
		),
		"business_goals": "Reduce payroll deduction errors to zero; cut loan-request turnaround from ~5 days to under 2.",
		"desired_outcomes": (
			"Employees self-serve loan requests and see live balances. Payroll deductions calculate automatically "
			"from each approved loan with no manual Salary Slip edits. HR has a full, auditable approval history."
		),
	})
	doc.insert(ignore_permissions=True)
	return doc


def create_strategy_analysis(project, business_need, stakeholders):
	doc = frappe.get_doc({
		"doctype": "BA Strategy Analysis",
		"project": project,
		"business_need": business_need.name,
		"current_state_description": (
			"Employees email HR to request a loan. HR checks eligibility informally and replies by email. "
			"Payroll manually edits the employee's Salary Slip each pay run to apply a deduction, tracking "
			"running balances in a shared Excel file with no version history."
		),
		"future_state_description": (
			"A standalone employee_loans Frappe app (EL-prefixed doctypes) lets employees submit requests "
			"through the portal, routes them through a configurable approval flow, and automatically generates "
			"a repayment schedule that feeds Salary Slip deductions each pay run with no manual editing."
		),
		"new_capabilities_required": (
			"Self-service loan request portal; configurable approval workflow; automatic repayment schedule "
			"generation; Salary Slip deduction integration; employee-facing balance visibility."
		),
		"scope_statement": (
			"In scope: loan request, approval, repayment schedule, Salary Slip deduction integration, balance "
			"reporting. Out of scope for v1: interest-bearing loans, third-party lender integration."
		),
		"constraints": "Must integrate with existing HR/Payroll module without modifying core Salary Slip code.",
		"assumptions": "Employee and Salary Slip doctypes are already in active use across all client sites.",
		"change_strategy": (
			"Phased rollout: pilot with Alfa HR/Payroll for one pay cycle before extending to other "
			"client sites running the Storms Digital ERPNext implementation."
		),
		"solution_scope": "A standalone employee_loans app installed alongside HR/Payroll, not a core HR module change.",
	})
	doc.append("capability_gaps", {
		"capability_area": "Approval audit trail",
		"current_state": "Status tracked in an editable spreadsheet cell",
		"desired_state": "System-enforced workflow with timestamped approval history",
		"gap_description": "No tamper-proof record of who approved what, and when.",
	})
	doc.append("capability_gaps", {
		"capability_area": "Payroll deduction accuracy",
		"current_state": "Manual Salary Slip edits each pay run",
		"desired_state": "Deduction auto-calculated from an active repayment schedule",
		"gap_description": "Manual edits are the direct cause of recent repayment errors.",
	})
	doc.append("risks", {
		"risk_description": "Incorrect deduction calculation causes employee net-pay disputes",
		"likelihood": "Medium", "impact": "High",
		"mitigation_strategy": "Parallel-run the new deduction logic against manual figures for one full pay cycle before cutover.",
	})
	doc.append("risks", {
		"risk_description": "Outstanding balances at resignation aren't offset against final settlement correctly",
		"likelihood": "Medium", "impact": "High",
		"mitigation_strategy": "Build and test the final-settlement offset rule against at least 3 historical resignation cases.",
	})
	doc.insert(ignore_permissions=True)
	return doc


def create_requirements(project, elicitations, business_need, stakeholders):
	reqs = {}

	parent = frappe.get_doc({
		"doctype": "BA Requirement",
		"project": project,
		"title": "Employee loan management",
		"requirement_type": "Business",
		"priority": "Must Have",
		"status": "Approved",
		"is_group": 1,
		"description": "Top-level capability covering loan request through repayment, replacing the manual Excel process.",
		"business_need": business_need.name,
		"owner_stakeholder": s(stakeholders, "Noura Al-Sahli").name,
	})
	parent.insert(ignore_permissions=True)
	reqs["parent"] = parent

	def child(title, rtype, priority, desc, source=None, owner=None, criteria=None):
		doc = frappe.get_doc({
			"doctype": "BA Requirement",
			"project": project,
			"title": title,
			"requirement_type": rtype,
			"priority": priority,
			"status": "Approved",
			"parent_ba_requirement": parent.name,
			"description": desc,
			"source_elicitation": source,
			"business_need": business_need.name,
			"owner_stakeholder": owner,
		})
		for c in (criteria or []):
			doc.append("acceptance_criteria", {"criterion": c, "status": "Pending"})
		doc.insert(ignore_permissions=True)
		return doc

	reqs["submit"] = child(
		"Submit a loan request online", "Stakeholder", "Must Have",
		"Employees submit a loan request through a self-service form instead of email.",
		source=elicitations[0].name, owner=s(stakeholders, "Yousef Al-Harbi").name,
		criteria=["Employee can select loan type and amount",
				  "Employee can attach supporting documents",
				  "Employee receives a confirmation on submission"],
	)
	reqs["approval"] = child(
		"Route requests through an approval workflow", "Solution - Functional", "Must Have",
		"Loan requests are routed to the configured approver(s) with a full, timestamped decision history.",
		source=elicitations[0].name, owner=s(stakeholders, "Noura Al-Sahli").name,
		criteria=["Each approval/rejection is timestamped and attributed to a user",
				  "Rejected requests show a reason to the employee"],
	)
	reqs["deduction"] = child(
		"Automatically calculate payroll deductions", "Solution - Functional", "Must Have",
		"An approved loan generates a repayment schedule that feeds the employee's Salary Slip deduction "
		"each pay run without manual editing.",
		source=elicitations[1].name, owner=s(stakeholders, "Faisal Otaibi").name,
		criteria=["Deduction amount matches the active repayment schedule line for that period",
				  "Net pay after deduction never falls below the configured minimum percentage"],
	)
	reqs["settlement"] = child(
		"Offset outstanding balance on final settlement", "Solution - Functional", "Should Have",
		"On resignation or termination, any outstanding loan balance is automatically offset against the "
		"employee's final settlement before payout.",
		source=elicitations[1].name, owner=s(stakeholders, "Faisal Otaibi").name,
		criteria=["Final settlement calculation includes outstanding loan balance as a deduction line"],
	)
	reqs["balance_visibility"] = child(
		"Show employees their live loan balance", "Solution - Functional", "Should Have",
		"Employees can view their current outstanding balance and remaining repayment schedule at any time.",
		source=elicitations[2].name, owner=s(stakeholders, "Yousef Al-Harbi").name,
	)
	reqs["audit_trail"] = child(
		"Maintain a full audit trail of loan records", "Solution - Non-Functional", "Must Have",
		"All loan record changes (submission, approval, schedule edits) are tracked with user and timestamp, "
		"replacing the untracked spreadsheet edits in the current process.",
		source=elicitations[2].name, owner=s(stakeholders, "Lina Haddad").name,
	)
	reqs["migration"] = child(
		"Migrate existing open loans from the spreadsheet", "Transition", "Must Have",
		"All currently open loans tracked in the Excel sheet are migrated into the new system with correct "
		"outstanding balances before go-live.",
		source=elicitations[2].name, owner=s(stakeholders, "Faisal Otaibi").name,
	)

	return reqs


def create_business_rules(project, requirements):
	rules = [
		dict(rule_name="Maximum loan amount cap", rule_type="Constraint",
			 rule_statement="An employee's total outstanding loan balance may not exceed 3x their monthly basic salary.",
			 source="Kickoff workshop, 2026-05-18", related_requirement=requirements["approval"].name),
		dict(rule_name="Minimum net pay after deduction", rule_type="Constraint",
			 rule_statement="Loan deduction for a pay period may not reduce the employee's net pay below 70% of "
							 "their standard net salary for that period.",
			 source="Payroll deduction interview, 2026-05-25", related_requirement=requirements["deduction"].name),
		dict(rule_name="Interest-free threshold", rule_type="Action Enabler",
			 rule_statement="Loans of SAR 5,000 or less are interest-free by default, consistent with current "
							 "company policy; larger amounts require Finance Controller sign-off on terms.",
			 source="Kickoff workshop, 2026-05-18", related_requirement=requirements["approval"].name),
	]
	for r in rules:
		doc = frappe.get_doc({"doctype": "BA Business Rule", "project": project, "status": "Approved", **r})
		doc.insert(ignore_permissions=True)


def create_use_case(project, requirements):
	doc = frappe.get_doc({
		"doctype": "BA Use Case",
		"project": project,
		"use_case_name": "Employee submits a loan request",
		"primary_actor": "Employee",
		"related_requirement": requirements["submit"].name,
		"description": "An employee requests a loan through the self-service portal.",
		"preconditions": "Employee is logged in and has no pending request awaiting decision.",
		"alternate_flows": (
			"3a. Requested amount exceeds the maximum loan cap: system blocks submission and shows the cap. "
			"5a. Approver rejects: employee is notified with the stated reason."
		),
		"postconditions": "A BA-tracked EL Loan Application exists with status Pending Approval, or the request "
						   "is blocked with a clear validation message.",
	})
	steps = [
		("Employee opens the loan request form", "System pre-fills employee details and shows current balance"),
		("Employee selects loan type and enters amount", "System validates amount against the maximum loan cap"),
		("Employee attaches supporting documents (optional)", "System stores attachments against the request"),
		("Employee submits the request", "System creates the request with status Pending Approval"),
		("Approver reviews and decides", "System notifies the employee of the approval or rejection"),
	]
	for i, (action, response) in enumerate(steps, start=1):
		doc.append("main_flow", {"step_no": i, "actor_action": action, "system_response": response})
	doc.insert(ignore_permissions=True)


def create_user_stories(project, requirements):
	stories = [
		dict(story_title="Self-service loan request", as_a="employee",
			 i_want="to submit a loan request from my phone",
			 so_that="I don't have to email HR and wait days for a reply",
			 story_points=5, priority="Must Have", status="Backlog",
			 related_requirement=requirements["submit"].name,
			 criteria=["Form is usable on a mobile screen", "Confirmation is shown immediately on submit"]),
		dict(story_title="Automatic deduction calculation", as_a="payroll officer",
			 i_want="loan deductions to be calculated automatically from the repayment schedule",
			 so_that="I no longer have to manually edit each Salary Slip and risk errors",
			 story_points=8, priority="Must Have", status="Backlog",
			 related_requirement=requirements["deduction"].name,
			 criteria=["Deduction line appears on the Salary Slip without manual entry"]),
		dict(story_title="One-click approval", as_a="HR manager",
			 i_want="to approve or reject a loan request in one click with an optional comment",
			 so_that="processing time drops from days to minutes",
			 story_points=3, priority="Should Have", status="Backlog",
			 related_requirement=requirements["approval"].name,
			 criteria=["Approve/Reject actions are visible directly on the request list view"]),
	]
	for st in stories:
		criteria = st.pop("criteria", [])
		doc = frappe.get_doc({"doctype": "BA User Story", "project": project, **st})
		for c in criteria:
			doc.append("acceptance_criteria", {"criterion": c, "status": "Pending"})
		doc.insert(ignore_permissions=True)


def create_process_model(project, requirements):
	doc = frappe.get_doc({
		"doctype": "BA Process Model",
		"project": project,
		"process_name": "Loan request to repayment",
		"related_requirement": requirements["parent"].name,
		"as_is_description": (
			"Employee emails HR -> HR manually checks eligibility and replies by email -> Payroll manually "
			"edits each Salary Slip every pay run -> running balance tracked in a shared Excel file."
		),
		"to_be_description": (
			"Employee submits via self-service form -> system validates against loan cap -> routed to approver "
			"with timestamped decision -> approved loan generates a repayment schedule -> Salary Slip deduction "
			"applies automatically each pay run -> balance visible to employee in real time -> on resignation, "
			"outstanding balance auto-offsets against final settlement."
		),
		"swimlane_notes": "Lanes: Employee, HR/Approver, Payroll, System. Hand-off points: submission (Employee->System), "
						   "decision (System->Approver->System), deduction (System->Payroll Salary Slip).",
	})
	doc.insert(ignore_permissions=True)


def create_glossary_terms(project, requirements):
	terms = [
		dict(term="EL", synonyms="Employee Loans module prefix",
			 definition="Naming prefix used for all doctypes in the standalone employee_loans app, "
						 "e.g. EL Loan Application, EL Loan Type, EL Repayment Schedule."),
		dict(term="Repayment schedule", synonyms="Deduction schedule",
			 definition="The set of dated, amount-specific lines generated from an approved loan that drive "
						 "each pay run's Salary Slip deduction until the balance reaches zero.",
			 related_requirement=requirements["deduction"].name),
		dict(term="Final settlement", synonyms="End of service settlement, EOSB payout",
			 definition="The final payment made to an employee on resignation or termination, against which "
						 "any outstanding loan balance must be offset before payout.",
			 related_requirement=requirements["settlement"].name),
		dict(term="Loan cap", synonyms="Maximum loan amount",
			 definition="The maximum total outstanding loan balance an employee may hold, expressed as a "
						 "multiple of monthly basic salary.",
			 related_requirement=requirements["approval"].name),
	]
	for t in terms:
		doc = frappe.get_doc({"doctype": "BA Glossary Term", "project": project, **t})
		doc.insert(ignore_permissions=True)


def create_change_request(project, requirements, user):
	doc = frappe.get_doc({
		"doctype": "BA Requirement Change Request",
		"project": project,
		"requirement": requirements["deduction"].name,
		"status": "Approved",
		"requested_by": user,
		"request_date": "2026-06-20",
		"change_description": (
			"Add support for early/full settlement of a loan ahead of schedule, triggered by the employee "
			"rather than only on resignation."
		),
		"justification": "Two employees asked Payroll directly during the pilot whether they could pay off a "
						  "loan early; there was no way to do this without manually zeroing the schedule.",
		"impact_analysis": (
			"Affects the deduction requirement and the repayment schedule generation logic. No impact on the "
			"approval workflow or loan cap rule."
		),
		"decision_notes": "Approved by HR Manager and Finance Controller; scoped into v1 given low build cost.",
	})
	doc.insert(ignore_permissions=True)


def create_solution_evaluation(project):
	doc = frappe.get_doc({
		"doctype": "BA Solution Evaluation",
		"project": project,
		"solution_name": "Employee Loans app — pilot pay cycle",
		"status": "In Progress",
		"evaluation_date": "2026-06-25",
		"evaluation_method": "KPI Review",
		"findings": (
			"First pilot pay run with automatic deductions completed with zero manual Salary Slip edits, "
			"versus a baseline of 2-3 manual corrections per cycle. Average loan request turnaround dropped "
			"from 5 days to 1.5 days during the pilot week."
		),
		"recommendations": "Proceed to full rollout across remaining client sites after one more pay cycle "
							"of parallel-run validation on the deduction calculation.",
	})
	doc.append("performance_measures", {
		"metric_name": "Manual Salary Slip corrections per pay run",
		"target_value": "0", "actual_value": "0",
		"variance_notes": "Met target in pilot run 1.",
	})
	doc.append("performance_measures", {
		"metric_name": "Average loan request turnaround (days)",
		"target_value": "2", "actual_value": "1.5",
		"variance_notes": "Ahead of target.",
	})
	doc.insert(ignore_permissions=True)


def create_ba_document(project, stakeholders, requirements, business_need, user):
	doc = frappe.get_doc({
		"doctype": "BA Document",
		"project": project,
		"document_title": "Employee Loans — Business Requirements Document",
		"document_type": "Business Requirements Document (BRD)",
		"prepared_by": user,
		"version": "1.0",
		"status": "In Review",
		"executive_summary": (
			"This BRD documents the requirements for replacing Alfa's manual, spreadsheet-based "
			"employee loan process with a standalone employee_loans Frappe app, integrated with the existing "
			"HR/Payroll module. It covers loan requests, approval, automatic payroll deduction, and final "
			"settlement offsetting."
		),
		"business_need": business_need.name,
		"approval_notes": "Pending Finance Controller sign-off on the deduction-cap business rule wording.",
	})
	for st in stakeholders:
		doc.append("included_stakeholders", {"stakeholder": st.name})
	for key in ("parent", "submit", "approval", "deduction", "settlement", "audit_trail", "migration"):
		doc.append("included_requirements", {"requirement": requirements[key].name})
	for rule_name in frappe.get_all("BA Business Rule", filters={"project": project}, pluck="name"):
		doc.append("included_business_rules", {"business_rule": rule_name})
	doc.insert(ignore_permissions=True)
