# Client register (one sheet, one row per client)

The single source of truth for who the office works for, their accounting policies, and what is due.
Keep it in ~~spreadsheet as `Accountant/client-register`. Never copy client figures into a skill or lesson.

## Standard Columns & Configuration

| Column | Example | Default (if blank) | Notes & Workflow Impact |
|---|---|---|---|
| `client_code` | C001 | *(Required)* | Short code used in file names; no tax ID in file names |
| `client_name` | บริษัท ตัวอย่าง จำกัด | *(Required)* | Legal registered entity name |
| `entity_type` | company / partnership / individual | `company` | Drives legal forms and compliance calendar |
| `workflow_scope` | `full` / `tax-only` / `annual-only` | `full` | **Workflow selector** (see below) |
| `tax_scheme` | `sme` / `general` / `boi` | `sme` if capital ≤ 5M & rev ≤ 30M, else `general` | Drives CIT rate (0-15-20% vs flat 20% vs BOI exemption) |
| `inventory_method` | `none` / `fifo` / `weighted_average` | `none` | If `none`, skip inventory-cogs; if set, requires stock valuation & Sec 87(3) report |
| `asset_threshold` | 5000 / 10000 | `5000` | Capitalization threshold (THB) for fixed assets vs immediate expensing |
| `vat_registered` | yes / no | `yes` | ภ.พ.30 monthly if yes |
| `wht_forms` | PND1, PND3, PND53 | `PND1, PND3, PND53` | Which withholding returns apply |
| `sso` | yes / no | `yes` | สปส.1-10 monthly if they have employees |
| `e_filing` | yes / no | `yes` | Changes statutory deadlines (+8 days extension) |
| `fiscal_year_end` | 12-31 | `12-31` | For ภ.ง.ด.50/51, DBD ส.บช.3, and annual audit schedule |
| `auditor_type` | CPA / TA / pending | `CPA` | Independent auditor tier |
| `folder` | link to client cloud folder | `Accountant/clients/<client_code>` | Working directory link |
| `period` | 2026-10 | Current month | The period currently being worked |
| `status` | not started / docs in / booked / reconciled / waiting approval / filed | `not started` | Current operational state |
| `next_deadline` | 2026-11-15 | Earliest open deadline | Trigger for dashboard alerts |
| `notes` | free text | `—` | Client preferences, special instructions |

---

## Workflow Scope Options (`workflow_scope`)

Clients differ in their engagement contracts. Accountant-chief adapts its workflow based on `workflow_scope`:

1. **`full` (Default - งานบัญชีเต็มรูปแบบ):**
   - Collect documents → Book GL/VAT/WHT → Run `adjusting-entries` (accruals, prepayments, depreciation) → Run `inventory-cogs` (if inventory_method ≠ none) → Run `reconcile-check` (all 15 checks) → `auditor` review → Report.
2. **`tax-only` (งานยื่นภาษีประจำเดือนเท่านั้น):**
   - Collect tax invoices & WHT slips → Book VAT reports and WHT lists → Skip adjusting entries and inventory → Run `reconcile-check` (VAT, WHT, documents only) → Report filing figures.
3. **`annual-only` (งานปิดงบการเงินประจำปีและตรวจสอบบัญชี):**
   - Receives 12-month trial balance → Run `year-end-close` (tax reconciliation Sec 65 Ter) → Prepare ภ.ง.ด.50 → Draft `financial-statements` (ส.บช.3 & notes) → Assemble `audit-readiness` pack.

---

## Fallback Philosophy (ไม่ครบก็ไม่สะดุด)
If a client row does not specify policy columns (`tax_scheme`, `inventory_method`, `asset_threshold`),
the plugin automatically assumes the **Standard Defaults**:
- Tax rate: SME tiered rates if eligible, otherwise 20% general corporate tax.
- Inventory: None (Service model).
- Asset threshold: 5,000 THB.
- Workflow: Full cycle.
