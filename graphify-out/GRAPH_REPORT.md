# Graph Report - delivery-workflow-completion  (2026-10-31)

## Corpus Check
- 70 files · ~44,330 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 741 nodes · 999 edges · 64 communities (59 shown, 5 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `1ec1279f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## God Nodes (most connected - your core abstractions)
1. `register_doc()` - 22 edges
2. `run()` - 22 edges
3. `find()` - 19 edges
4. `write_job()` - 18 edges
5. `call()` - 18 edges
6. `catalog()` - 17 edges
7. `add_entry()` - 16 edges
8. `Thai Accounting Office` - 16 edges
9. `ledger_entries()` - 15 edges
10. `index_scan()` - 15 edges

## Cross-Cutting Nodes (span the most distinct areas of the codebase)
A high-degree node isn't always architecturally central - a widely-used
utility/config file can rack up more edges than a real coupler while only
ever touching one area. This ranks by how many DIFFERENT communities a
node's neighbors span, not by raw edge count.
1. `Base` - bridges 3 areas (14 edges)
2. `call()` - bridges 2 areas (18 edges)
3. `register_doc()` - bridges 1 areas (22 edges)
4. `run()` - bridges 1 areas (22 edges)
5. `find()` - bridges 1 areas (19 edges)
6. `write_job()` - bridges 1 areas (18 edges)
7. `catalog()` - bridges 1 areas (17 edges)
8. `add_entry()` - bridges 1 areas (16 edges)
9. `ledger_entries()` - bridges 1 areas (15 edges)
10. `read_text()` - bridges 1 areas (14 edges)

## Surprising Connections (you probably didn't know these)
- `parties_aka()` --calls--> `parties()`  [EXTRACTED]
  tests/test_graph.py → skills/accountant-graph/scripts/graph.py
- `call()` --calls--> `check()`  [EXTRACTED]
  skills/accountant-graph/scripts/mcp_server.py → skills/accountant-graph/scripts/graph.py
- `call()` --calls--> `init()`  [EXTRACTED]
  skills/accountant-graph/scripts/mcp_server.py → skills/accountant-graph/scripts/graph.py
- `call()` --calls--> `register_doc()`  [EXTRACTED]
  skills/accountant-graph/scripts/mcp_server.py → skills/accountant-graph/scripts/graph.py
- `call()` --calls--> `write_job()`  [EXTRACTED]
  skills/accountant-graph/scripts/mcp_server.py → skills/accountant-graph/scripts/graph.py

## Import Cycles
- None detected.

## Communities (64 total, 5 thin omitted)

### Community 0 - "graph.py"
Cohesion: 0.07
Nodes (79): Exception, add_entry(), add_link(), append_text(), append_tsv(), build_map(), build_parser(), catalog() (+71 more)

### Community 1 - "test_graph.py"
Cohesion: 0.11
Nodes (13): check(), lessons_review(), Return a list of findings; empty means the memory is consistent., read_text(), Base, parties_aka(), Tests for the accountant graph engine, the Stop gate and the MCP server (standar, TestCheck (+5 more)

### Community 2 - "Thai Accounting Office"
Cohesion: 0.05
Nodes (40): [0.4.0] - 2026-10-21, [0.5.0] - 2026-10-21, Added, Added, Changelog, Contributing / maintaining the plugin, Claude จะไม่ทำเองเด็ดขาด (ต้องให้คุณกดยืนยัน), Contributors (+32 more)

### Community 3 - "Reference: Thai Accounting Compliance (กฎหมายบัญชีไทย)"
Cohesion: 0.08
Nodes (23): 1. กฎหมายหลัก, 2. มาตรฐานบัญชีไทย, 3. หน่วยงานกำกับดูแล, 4. จรรยาวิชาชีพบัญชี (FAP Code of Ethics), 5. การรายงานต่อหน่วยงาน, 6. บทลงโทษ, DBD, Reference: Thai Accounting Compliance (กฎหมายบัญชีไทย) (+15 more)

### Community 4 - "1. ภาษีเงินได้นิติบุคคล (Corporate Income Tax - CIT)"
Cohesion: 0.09
Nodes (22): 1. ภาษีเงินได้นิติบุคคล (Corporate Income Tax - CIT), 2. ภาษีมูลค่าเพิ่ม (VAT), 3. ภาษีหัก ณ ที่จ่าย (Withholding Tax - WHT), 4. ภาษีเงินได้บุคคลธรรมชาติ (PIT), 5. ภาษีอื่นๆ, Input VAT ที่ไม่สามารถเครดิตได้, Reference: Tax Accounting (บัญชีภาษี), การคำนวณ (+14 more)

### Community 5 - "Reference: Working Capital & Internal Controls"
Cohesion: 0.09
Nodes (22): 1. การจัดการเงินสด (Cash Management), 2. บัญชีลูกหนี้ (Accounts Receivable), 3. บัญชีสินค้าคงคลัง (Inventory), 4. บัญชีเจ้าหนี้ (Accounts Payable), 5. Internal Controls (COSO Framework), 5 องค์ประกอบ, 6. Fraud Prevention, Aging Analysis (+14 more)

### Community 6 - "Reference: Digital Tax Systems (ระบบภาษีดิจิทัล)"
Cohesion: 0.09
Nodes (21): 1. e-Tax Invoice & e-Receipt, 2. e-Withholding Tax (e-WHT), 3. e-Filing (การยื่นแบบออนไลน์), 4. Digital Services Tax, 5. การเตรียมความพร้อมสำหรับ e-Tax, 6. แหล่งข้อมูล, Reference: Digital Tax Systems (ระบบภาษีดิจิทัล), ขั้นตอน (+13 more)

### Community 7 - "Thai Accounting Office"
Cohesion: 0.29
Nodes (4): handle(), main(), One JSON-RPC message -> a response dict, or None for a notification., TestMcp

### Community 8 - "Reference: Advanced Accounting (บัญชีขั้นสูง)"
Cohesion: 0.10
Nodes (19): 1. TFRS 15 — Revenue Recognition (5-Step Model), 2. TFRS 9 — Financial Instruments, 3. TFRS 16 — Leases, 4. Business Combination (TFRS 3), 5. Consolidated Financial Statements, 6. Foreign Currency (TAS 21), Acquisition Method, ECL (Expected Credit Loss) (+11 more)

### Community 9 - "Reference: BOI Tax Incentives (สิทธิประโยชน์ BOI)"
Cohesion: 0.10
Nodes (19): 1. ภาพรวม BOI, 2. การบัญชีสำหรับกิจการ BOI, 3. เงื่อนไขการรักษาสิทธิ์, 4. การบัญชีเมื่อสิทธิ์หมดอายุ, 5. การรายงานต่อ BOI, 6. ประเภทกิจการที่ได้รับส่งเสริม (2025), Deferred Tax สำหรับกิจการ BOI, Reference: BOI Tax Incentives (สิทธิประโยชน์ BOI) (+11 more)

### Community 10 - "Reference: Cost Accounting (บัญชีต้นทุน)"
Cohesion: 0.11
Nodes (18): 1. Job Order Costing, 2. Process Costing, 3. Activity-Based Costing (ABC), 4. Standard Costing & Variance Analysis, 5. Target Costing, 6. Throughput Accounting (Theory of Constraints), Equivalent Units, Joint Products & By-Products (+10 more)

### Community 11 - "Reference: Financial Planning & Capital Budgeting"
Cohesion: 0.12
Nodes (16): 1. งบประมาณประจำปี (Annual Budget), 2. Capital Budgeting, 3. Cost-Volume-Profit Analysis, 4. Relevant Costing for Decisions, 5. Risk Management, Discontinuance Decision, Hedging, Make or Buy (+8 more)

### Community 12 - "Reference: Financial Reporting & Disclosure"
Cohesion: 0.13
Nodes (14): 1. องค์ประกอบงบการเงินฉบับเต็ม, 2. งบกระแสเงินสด (Cash Flow Statement), 3 กิจกรรม, 3. หมายเหตุประกอบงบการเงิน, 4. Segment Reporting (TFRS 8), 5. ประเภทความเห็นผู้สอบบัญชี, 6. Deferred Tax (TAS 12), Key Audit Matters (KAM) (+6 more)

### Community 13 - "decide"
Cohesion: 0.26
Nodes (7): decide(), has_work_folder(), is_prompt(), last_turn(), main(), Return the block reason, or None to allow., TestStopGate

### Community 14 - "Reference: Financial Analysis (วิเคราะห์งบการเงิน)"
Cohesion: 0.14
Nodes (13): 1. อัตราส่วนสภาพคล่อง (Liquidity Ratios), 2. อัตราส่วนประสิทธิภาพ (Efficiency Ratios), 3. อัตราส่วนความสามารถชำระหนี้ (Solvency Ratios), 4. อัตราส่วนความสามารถทำกำไร (Profitability Ratios), 5. DuPont Analysis, 6. Trend Analysis, 7. EVA (Economic Value Added), 8. WACC (+5 more)

### Community 15 - "Reference: Transfer Pricing (ราคาโอน)"
Cohesion: 0.15
Nodes (12): 1. กฎหมายและข้อบังคับ, 2. หลักการ Arm's Length, 3. เอกสารที่ต้องจัดทำ, 4. Global Minimum Tax (Pillar Two), 5. Related Party Transactions, 6. บทลงโทษ, Local File Documentation, Master File (สำหรับ MNE ขนาดใหญ่) (+4 more)

### Community 16 - "1. Core Adjusting Cycles"
Cohesion: 0.17
Nodes (11): 1. Core Adjusting Cycles, 2. Steps to Execute Adjusting Entries, 3. Output, A. Accrued Expenses (ค่าใช้จ่ายค้างจ่าย), Adjusting Entries & Asset Schedules (เกณฑ์คงค้างและรายการปรับปรุงสิ้นงวด), B. Accrued Income (รายได้ค้างรับ), C. Prepaid Expenses & Amortization (ค่าใช้จ่ายจ่ายล่วงหน้าและตารางตัดจำหน่าย), D. Deferred / Unearned Revenue (รายได้รับล่วงหน้า) (+3 more)

### Community 17 - "Payment Voucher & Bank Transfer Preparation"
Cohesion: 0.17
Nodes (11): 1. 3-Way Matching & Document Verification, 2. Domestic Withholding Tax (WHT) Rates (มาตรา 3 เตรส), 3. Calculation & Payment Voucher (PV) Structure, 4. Withholding Tax Certificate (หนังสือรับรอง 50 ทวิ), 5. Online Banking Payment Schedule, 6. Execution Steps & Stop-and-Ask, 7. Output, Calculation Formula: (+3 more)

### Community 18 - "Accountant memory (a permanent, searchable record of the work, kept in the work folder)"
Cohesion: 0.18
Nodes (10): Accountant memory (a permanent, searchable record of the work, kept in the work folder), Job ledger (after every job, even when nothing went wrong), Keep it small, Learn and remember (every job), Look up (before the work), Never store, Record decisions (with the job), Trace and review (ask the memory, like a graph) (+2 more)

### Community 19 - "Company profile (works for any company; the answers live in the user's work folder)"
Cohesion: 0.18
Nodes (10): Company profile (works for any company; the answers live in the user's work folder), Confidentiality and backups, Duty → skill, Extending for one company, Facts to collect (saved to `Accountant/company-facts.md`, one line each, shown before saving), Learn and remember (every job), Mode (asked once at setup, stored as `Mode:` in company-facts), Setup (+2 more)

### Community 20 - "Statutory Financial Statements & DBD Compliance (การจัดทำงบการเงินและ DBD e-Filing)"
Cohesion: 0.18
Nodes (10): 1. Statutory Corporate Calendar (รอบปีสิ้นสุด 31 ธันวาคม), 2. Structure of Financial Statements (แบบ ส.บช.3), 3. Preparation & Filing Package, 4. Output, A. Statement of Financial Position (งบแสดงฐานะการเงิน), B. Statement of Income (งบกำไรขาดทุน), C. Statement of Changes in Equity (งบแสดงการเปลี่ยนแปลงส่วนของเจ้าของ), D. Notes to Financial Statements (หมายเหตุประกอบงบการเงิน) (+2 more)

### Community 21 - "Half-Year Corporate Income Tax: ภ.ง.ด.51 (ภาษีเงินได้นิติบุคคลครึ่งปี)"
Cohesion: 0.18
Nodes (10): 1. Deadlines & Statutory Basis, 2. Estimation Methods, 3. The 25% Underestimation Penalty (มาตรา 67 ตรี), 4. Tax Rate Computation, 5. Execution Steps, 6. Output, Formula for Shortfall Percentage:, Half-Year Corporate Income Tax: ภ.ง.ด.51 (ภาษีเงินได้นิติบุคคลครึ่งปี) (+2 more)

### Community 22 - "Reference: General Accounting (บัญชีทั่วไป)"
Cohesion: 0.18
Nodes (10): 1. การบันทึกรายการ (Journal Entries), 2. การจัดสรรค่าใช้จ่าย (Cost Allocation), 3. Bank Reconciliation, 4. ระบบเอกสาร, 5. Period-End Procedures, Reference: General Accounting (บัญชีทั่วไป), รายการพิเศษ, รายได้และค่าใช้จ่าย (+2 more)

### Community 23 - "Memory format"
Cohesion: 0.20
Nodes (9): decisions.md, formulas.md, index.md, ledger/<YYYY-MM>.md, Memory format, parties.md, periods.md, recurring.md (+1 more)

### Community 24 - "Foreign SaaS & Cloud Tax Compliance: ภ.พ.36 & ภ.ง.ด.54"
Cohesion: 0.20
Nodes (9): 1. Statutory Deadlines & Forms, 2. Form ภ.พ.36 (Reverse-Charge VAT 7%) vs VAT e-Service, 3. Form ภ.ง.ด.54 (Cross-Border Withholding Tax & DTA), 4. Monthly Execution Steps, 5. Output, Classification of Common Tech Expenses:, Crucial Inspection: Did the Vendor Already Charge Thai VAT? (กฎหมาย VAT e-Service), Foreign SaaS & Cloud Tax Compliance: ภ.พ.36 & ภ.ง.ด.54 (+1 more)

### Community 25 - "Inventory & Cost of Goods Sold (สินค้าคงเหลือและต้นทุนขาย)"
Cohesion: 0.20
Nodes (9): 1. Inventory Valuation & Cost Flow Methods, 2. Accounting Systems (Perpetual vs Periodic), 3. Lower of Cost or Net Realizable Value (LCNRV), 4. Statutory VAT Inventory Report (รายงานสินค้าและวัตถุดิบ ม.87(3)), 5. Physical Stock Count & Reconciliation Steps, 6. Output, Approved Methods under TFRS & Thai Tax Law, Inventory & Cost of Goods Sold (สินค้าคงเหลือและต้นทุนขาย) (+1 more)

### Community 26 - "TestPlugin"
Cohesion: 0.33
Nodes (3): The plugin files agree with the engine: tools named in skills exist, the hook an, read(), TestPlugin

### Community 27 - "Accountant Chief (the user decides, Claude runs the job)"
Cohesion: 0.22
Nodes (8): 0. Before anything, 1. Brief — ask once, 2. Task Sizing & Model Routing (การจัดสรรขนาดงานและระดับโมเดล), 3. Stop and ask the user — never decide these alone, 4. Check, then report, 5. Close: learning pass (every job), Accountant Chief (the user decides, Claude runs the job), Learn and remember (every job)

### Community 28 - "Accountant graph (search first, then trace: a light map of the office's documents)"
Cohesion: 0.22
Nodes (8): Accountant graph (search first, then trace: a light map of the office's documents), Ask the map (answers cite ids and show the path), Check (at every period close), Index (on request: "ทำดัชนีเอกสาร"), Learn and remember (every job), Register (while working; `document-intake`, `inbox-triage` and every job do this), Search first (before every job, before asking the user for a file), Tools (use these first; the files stay readable by hand)

### Community 29 - "Document intake"
Cohesion: 0.22
Nodes (8): Bank statements, Dates, numbers and encoding (Thai Windows / Excel), Document intake, Extract (one row per document), Learn and remember (every job), Register what you read, Tax invoice check (full tax invoice, Revenue Code s.86/4), Write

### Community 30 - "Thai Accountant Skills — Local Instructions"
Cohesion: 0.22
Nodes (8): Input Conventions, Output Conventions, Professional Boundaries, Recommended Composition, Routing Guide, Scope, Thai Accountant Skills — Local Instructions, Which Markdown To Use

### Community 31 - "Thai Accountant Skills — Local Instructions"
Cohesion: 0.22
Nodes (8): Input Conventions, Output Conventions, Professional Boundaries, Recommended Composition, Routing Guide, Scope, Thai Accountant Skills — Local Instructions, Which Markdown To Use

### Community 32 - "Thai Accountant Skills — Local Instructions"
Cohesion: 0.22
Nodes (8): Input Conventions, Output Conventions, Professional Boundaries, Recommended Composition, Routing Guide, Scope, Thai Accountant Skills — Local Instructions, Which Markdown To Use

### Community 33 - "Year-End Close & Annual Corporate Tax: ภ.ง.ด.50 (ปิดบัญชีสิ้นปีและภาษีนิติบุคคล)"
Cohesion: 0.22
Nodes (8): 1. Statutory Deadlines, 2. Year-End Closing Workflow, 3. Tax Reconciliation (กระทบยอดกำไรทางบัญชีสู่กำไรสุทธิทางภาษี), 4. CIT Computation & Tax Credits, 5. Year-End Closing Journal Entries, 6. Output, Learn and remember (every job), Year-End Close & Annual Corporate Tax: ภ.ง.ด.50 (ปิดบัญชีสิ้นปีและภาษีนิติบุคคล)

### Community 34 - "คู่มือการใช้งาน.html"
Cohesion: 0.25
Nodes (8): copy(), #cp, #dl, flash(), G, #md, #out, #q

### Community 35 - "Graph format"
Cohesion: 0.25
Nodes (7): aka: in parties.md, catalog.tsv, Command line summary, Graph format, links.tsv, Recipes (open only what can match), The job record (what `accountant_job` takes)

### Community 36 - "External Audit Readiness & Working Papers (การเตรียมเอกสารและกระดาษทำการส่งผู้สอบบัญชี)"
Cohesion: 0.25
Nodes (7): 1. Audit Lead Schedules (ผังกระดาษทำการตามหมวดบัญชี), 2. External Confirmation Letters (หนังสือยืนยันยอดภายนอก), 3. Mandatory Statutory Compliance Package, 4. Execution Steps, 5. Output, External Audit Readiness & Working Papers (การเตรียมเอกสารและกระดาษทำการส่งผู้สอบบัญชี), Learn and remember (every job)

### Community 37 - "Budget Tracking & Financial Forecasts"
Cohesion: 0.25
Nodes (7): 1. Operating Budget Cost Categories (defaults for a tech company; replace with the company's own categories in `company-profile`), 2. Monthly Variance Analysis Rules, 3. Rolling 3-Month Cash Flow & Runway Forecast, 4. Execution Steps, 5. Output, Budget Tracking & Financial Forecasts, Learn and remember (every job)

### Community 38 - "Handoff — for the Claude working with an accountant"
Cohesion: 0.25
Nodes (7): Data rules, Getting changes into the plugin, Handoff — for the Claude working with an accountant, How the plugin works (the boss loop), Open on day one, Where things live (the user's work folder), Who and why

### Community 39 - "<COMPANY_NAME> — office profile"
Cohesion: 0.29
Nodes (6): Accounting conventions, <COMPANY_NAME> — office profile, Office, People and approvals, Tools, Writing to clients

### Community 40 - "tests.yml"
Cohesion: 0.29
Nodes (6): jobs, test, name, on, pull_request, push

### Community 41 - "Accountant dashboard (artifact)"
Cohesion: 0.29
Nodes (6): Accountant dashboard (artifact), Data, Design, Learn and remember (every job), Page (one artifact, updated in place — reuse the same artifact every time), Privacy

### Community 42 - "Company tune-up: calibrate the assistant to the company"
Cohesion: 0.29
Nodes (6): After the first two months, Company tune-up: calibrate the assistant to the company, End of each day or on-demand tuning ("สรุปวันนี้"), End of each week ("สรุปสัปดาห์"), Flexible tuning triggers, Learn and remember (every job)

### Community 43 - "Thai Accountant & Finance — Senior/Manager Level"
Cohesion: 0.29
Nodes (6): Learn and remember (every job), Lessons, Persona & Principles, Quick Decision Framework, Reference Loading Guide, Thai Accountant & Finance — Senior/Manager Level

### Community 44 - "Independent Auditor (ผู้ตรวจอิสระประจำสำนักงานบัญชี)"
Cohesion: 0.33
Nodes (5): Checklist (PASS / FAIL with concrete evidence), Core Mandate: True Independence (หลักการตรวจสอบอิสระ), Execution & Model Tiering Protocol (การแยก Session และระดับโมเดล), Independent Auditor (ผู้ตรวจอิสระประจำสำนักงานบัญชี), Output Format

### Community 45 - "Learn and improve (the office gets better every week)"
Cohesion: 0.33
Nodes (5): After every job — learning pass, Improve a skill directly, Learn and improve (the office gets better every week), Learn and remember (every job), Weekly review (curator) — Monday, or when asked

### Community 46 - "Monthly close for one client (repeat per client)"
Cohesion: 0.33
Nodes (5): Deadlines (day of the following month), Learn and remember (every job), Monthly close for one client (repeat per client), Output, Steps

### Community 47 - "test_no_company_data.py"
Cohesion: 0.40
Nodes (3): NoCompanyData, Company data never lives in this repo (NDA): no work-folder files, tracked or no, repo_files()

### Community 48 - "Client register (one sheet, one row per client)"
Cohesion: 0.40
Nodes (4): Client register (one sheet, one row per client), Fallback Philosophy (ไม่ครบก็ไม่สะดุด), Standard Columns & Configuration, Workflow Scope Options (`workflow_scope`)

### Community 49 - "Ctx"
Cohesion: 0.40
Nodes (4): Architecture, Build and checks, Data boundary, Package layout

### Community 50 - "Inbox triage"
Cohesion: 0.40
Nodes (4): Inbox triage, Learn and remember (every job), Never, Register what you read

### Community 51 - "Payroll check (before executive approval)"
Cohesion: 0.40
Nodes (4): Checks (each one pass / fail with the figures), Learn and remember (every job), Output, Payroll check (before executive approval)

### Community 52 - "Connectors"
Cohesion: 0.50
Nodes (3): Connectors, Connectors for this plugin, How tool references work

### Community 53 - "Learning rules"
Cohesion: 0.50
Nodes (3): Learning rules, New skill (from the weekly review), Promote (monthly)

### Community 54 - "Reconciliation checks (the "tests" of the office)"
Cohesion: 0.50
Nodes (3): Learn and remember (every job), Reconciliation checks (the "tests" of the office), Rules

### Community 61 - "Design"
Cohesion: 0.40
Nodes (4): Design, Interaction model, Interaction principles, Preview

### Community 62 - "Product"
Cohesion: 0.40
Nodes (4): Delivery, Product, Safety boundaries, Users and interface

## Knowledge Gaps
- **396 isolated node(s):** `name`, `pull_request`, `push`, `test`, `python3` (+391 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.
- **4 possibly unreachable function(s):** `find_root()`, `parties_aka()`, `read()`, `repo_files()`
  Not reached from any recognized entry point - could be dead code, or dynamically dispatched/decorator-registered.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `TestStopGate` connect `decide` to `test_graph.py`?**
  _High betweenness centrality (0.003) - this node is a cross-community bridge._
- **Why does `TestPlugin` connect `TestPlugin` to `test_graph.py`?**
  _High betweenness centrality (0.003) - this node is a cross-community bridge._
- **Why does `Base` connect `test_graph.py` to `graph.py`, `decide`, `Thai Accounting Office`?**
  _High betweenness centrality (0.003) - this node is a cross-community bridge._
- **What connects `name`, `pull_request`, `push` to the rest of the system?**
  _422 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `graph.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07445141065830721 - nodes in this community are weakly interconnected._
- **Should `test_graph.py` be split into smaller, more focused modules?**
  _Cohesion score 0.1066066066066066 - nodes in this community are weakly interconnected._
- **Should `Thai Accounting Office` be split into smaller, more focused modules?**
  _Cohesion score 0.045454545454545456 - nodes in this community are weakly interconnected._