# BA Toolkit

A Frappe/ERPNext app for business analysts to document BA work, structured around the **BABOK v3 knowledge areas**. Every artifact links back to a core ERPNext **Project**, so BA documentation lives alongside the engagements it supports.

## What's inside

| Knowledge Area | Doctypes |
|---|---|
| 1. Business Analysis Planning & Monitoring | **BA Approach**, **BA Stakeholder** |
| 2. Elicitation & Collaboration | **BA Elicitation Activity** (with participants child table) |
| 3. Requirements Life Cycle Management | **BA Requirement** (tree/traceability), **BA Requirement Change Request** |
| 4. Strategy Analysis | **BA Business Need**, **BA Strategy Analysis** (current/future state, gaps, risks) |
| 5. Requirements Analysis & Design Definition | **BA Business Rule**, **BA Use Case**, **BA User Story**, **BA Process Model**, **BA Glossary Term** |
| 6. Solution Evaluation | **BA Solution Evaluation** (with performance measures) |
| Cross-cutting | **BA Document** — compiles a BRD/FRD from linked stakeholders, requirements, and business rules, with a print format |

23 doctypes total (14 main + 9 child tables).

### A few things worth knowing before you migrate

- **BA Requirement** is a tree doctype (`is_tree: 1`), so you get a native Frappe traceability tree (parent/child requirement decomposition) via **Tree > BA Requirement**.
- **BA Strategy Analysis** auto-computes a `risk_rating` (Critical/High/Medium/Low) on each risk row from likelihood × impact in `validate()` — no manual rating needed.
- **BA Document** has a "Pull Project Artifacts" button that bulk-fetches all stakeholders/requirements/business rules for the linked project in three queries (not N+1), via a module-level whitelisted function — same pattern you've used elsewhere (`gicore`, `construction_pm`).
- Two roles are created automatically on install: **Business Analyst** (create/read/write, no delete) and **Business Analyst Manager** (full CRUD). Assign these to users via User > Roles.
- A Jinja print format **"BA Document - BRD"** is created automatically, rendering a cover, executive summary, stakeholder table, requirements table, business rules, and a sign-off block.

### What's *not* automated (by design, to keep this safe to install)

I didn't hand-write a Workspace fixture — Frappe's Workspace JSON schema has shifted across v13/v14/v15 and a malformed one can be more annoying to debug than it's worth. Setting one up manually takes about 2 minutes:

1. Desk > Create New Workspace > "Business Analysis"
2. Add shortcut blocks for each doctype above, grouped under headers per knowledge area (the table above is already in that order)

If you tell me your exact `bench version`, I can generate the workspace JSON precisely for it next time.

## Installation

```bash
# from your bench directory
bench get-app ba_toolkit /path/to/ba_toolkit   # or push this to a git repo first and use the URL
bench --site your-site install-app ba_toolkit
bench --site your-site migrate
```

Then:
1. Go to **User** for each BA, add the **Business Analyst** role (or **Business Analyst Manager** for whoever approves change requests / publishes documents).
2. Open any doctype above from **Awesome Bar** (e.g. type "BA Stakeholder") to start using it, or build the workspace as described above.

## Typical workflow

1. **BA Approach** — one per project, captures planning/governance/stakeholder-engagement approach.
2. **BA Stakeholder** — build the stakeholder register, rate influence/interest/attitude.
3. **BA Elicitation Activity** — log each interview/workshop; use "New Requirement from this Session" to spin up requirements straight from session notes.
4. **BA Business Need → BA Strategy Analysis** — capture the problem/opportunity, then current/future state, gaps, and risks.
5. **BA Requirement** — the core artifact; type it as Business/Stakeholder/Solution-Functional/Solution-Non-Functional/Transition, set MoSCoW priority, decompose into children via the tree.
6. **BA Business Rule / BA Use Case / BA User Story / BA Process Model / BA Glossary Term** — design-level detail, each linkable back to a requirement.
7. **BA Requirement Change Request** — raised straight from a requirement via "New Change Request".
8. **BA Solution Evaluation** — after delivery, track performance measures against targets.
9. **BA Document** — pull everything together into a BRD, generate the PDF via Print.

## Extending later

- Add Frappe **Workflows** on `status` fields (e.g. Change Request: Submitted → Under Review → Approved → Implemented) if you want enforced approval gates rather than free-text status.
- If this needs to go bilingual later, the doctypes are plain English labels for now (kept simple since this is an internal tool) — Frappe's Translation tool can localize labels without touching the schema.
