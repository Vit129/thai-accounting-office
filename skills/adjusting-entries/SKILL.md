---
name: adjusting-entries
description: >
  This skill should be used for month-end and year-end adjusting journal entries (AJE),
  prepayments, accruals, fixed asset registers, depreciation schedules, and allowance for doubtful
  accounts under TFRS for NPAEs and the Thai Revenue Code — when the user says "รายการปรับปรุงบัญชี",
  "ปรับปรุงสิ้นงวด", "บันทึกค้างจ่าย", "รายได้ค้างรับ", "ตัดจ่ายล่วงหน้า", "ทะเบียนทรัพย์สิน",
  "คิดค่าเสื่อมราคา", "accrual", "prepayment", "depreciation schedule", or "fixed asset register".
metadata:
  version: "0.1.3"
  last_improved: "2026-10-16"
---

# Adjusting Entries & Asset Schedules (เกณฑ์คงค้างและรายการปรับปรุงสิ้นงวด)

Read `Accountant/lessons/adjusting-entries.md` first if it exists. Consult `thai-accountant`
(`skills/thai-accountant/references/general-accounting.md`, `skills/thai-accountant/references/compliance.md`) for treatment decisions.

Under the Thai Accounting Act B.E. 2543 and TFRS for NPAEs, financial statements must follow
the **accrual basis (เกณฑ์คงค้าง)**. This skill manages the recurring and period-end adjusting
entries that ensure income and expenses reflect economic reality, not just cash flows.

---

## 1. Core Adjusting Cycles

### A. Accrued Expenses (ค่าใช้จ่ายค้างจ่าย)
Incurred in the period but invoice not yet received or payment not yet made:
- Common items: Utility bills (electricity, water, telephone), audit fees, accounting fees,
  office rent, staff bonuses, interest on loans.
- Entry: `Dr. Expense / Cr. Accrued Expense (หนี้สินหมุนเวียน)`
- Reverse on payment or first day of next period depending on client accounting policy.

### B. Accrued Income (รายได้ค้างรับ)
Goods delivered or services rendered in the period but billing occurs in a later period:
- Common items: Service revenue earned under contract milestones, interest receivable.
- Entry: `Dr. Accrued Income (สินทรัพย์หมุนเวียน) / Cr. Revenue`
- Note for Thai VAT: For service businesses, VAT liability arises upon receipt of payment or
  issuance of tax invoice (whichever is earlier), so accrued service income generally does not
  trigger VAT output until invoiced/paid.

### C. Prepaid Expenses & Amortization (ค่าใช้จ่ายจ่ายล่วงหน้าและตารางตัดจำหน่าย)
Payments made covering future periods:
- Common items: Annual insurance premiums, prepaid rent, software subscriptions, domain names.
- Track in an **Amortization Schedule** sheet: Contract start/end date, total cost, monthly charge,
  accumulated amortization, remaining net book value.
- Monthly Entry: `Dr. Expense / Cr. Prepaid Expense (สินทรัพย์หมุนเวียน)`

### D. Deferred / Unearned Revenue (รายได้รับล่วงหน้า)
Cash received before services are performed or goods delivered:
- Common items: Customer deposits, advance service retainers, annual maintenance fees.
- Monthly Entry: `Dr. Unearned Revenue (หนี้สินหมุนเวียน) / Cr. Revenue`

### E. Fixed Asset Register & Depreciation (ทะเบียนสินทรัพย์ถาวรและค่าเสื่อมราคา)
Every capital expenditure above the capitalization threshold (commonly 5,000 THB or per company policy)
must be entered into the **Fixed Asset Register**:
- Columns required: Asset Code, Description, Serial No., Location, Purchase Date, Invoice No.,
  Supplier, Initial Cost, Useful Life (years), Salvage Value, Depreciation Method.
- **Accounting vs Tax Depreciation:**
  - Standard method: Straight-line `(Cost - Residual Value) / Useful Life`
  - Tax maximum rates under Royal Decree No. 145 (พ.ร.ฎ. 145) — defaults; a rate in
    `Accountant/company-facts.md` → `## Tax rate overrides` wins (ask the user to record any change there):
    - Buildings: Permanent 5% (20 years), Temporary 100%
    - Machinery / Equipment: 20% (5 years)
    - Computer hardware & peripherals: 33.33% (3 years)
    - Vehicles: 20% (5 years) — passenger cars capped at 1,000,000 THB depreciable cost for tax
    - Computer software (cost of copyright): over the licence term when limited; 10% a year when
      unlimited (RD rulings — confirm)
  - SME Special Incentives: Royal Decree grants initial allowances (e.g. 40% initial allowance
    on machinery/computers for eligible SMEs with paid-up capital not exceeding 5M and revenue not
    exceeding 30M THB).
- Monthly Entry: `Dr. Depreciation Expense / Cr. Accumulated Depreciation`

### F. Allowance for Impairment of Receivables (ค่าเผื่อหนี้สงสัยจะสูญ)
- Review AR ageing at period end.
- TFRS for NPAEs allows percentage of outstanding balance or specific identification based on
  collection history.
- Entry: `Dr. Bad Debt Expense / Cr. Allowance for Doubtful Accounts (หักจากลูกหนี้การค้า)`
- Note: For tax purposes (Revenue Code Section 65 Bis (9) and Ministerial Regulation No. 186),
  provisions are non-deductible until actual write-off conditions are satisfied. Flag the tax difference.

---

## 2. Steps to Execute Adjusting Entries

1. **Review Sub-ledgers & Contracts**: Examine loan agreements, insurance policies, lease contracts,
   and open supplier purchase orders.
2. **Update Schedules**:
   - Update `Fixed-Assets` sheet (additions, disposals, monthly depreciation).
   - Update `Prepayments` sheet (monthly amortization).
   - Update `Accruals` sheet (new accruals, reversals).
3. **Generate General Journal Entries (GJ)**:
   - Prepare journal vouchers with explanation and calculation breakdown.
4. **Post to GL and Trial Balance**:
   - Verify post-adjustment debits equal credits.
5. **Reconcile**:
   - Run `reconcile-check` to confirm asset sub-ledgers agree with GL balance sheet accounts.

---

## 3. Output

A structured Thai summary:
- Table of adjusting entries made (Account code, Account name, Debit, Credit, Description).
- Updated Asset & Prepayment schedule links.
- Flagged differences between Accounting treatment and Thai Tax treatment (for year-end tax reconciliation).

## Learn and remember (every job)
- **Before:** read `Accountant/lessons/adjusting-entries.md` if it exists. Search first with `accountant-graph`
  (tool `accountant_find` on the names, document numbers, forms and period in the request) and
  look up `Accountant/memory/` with `accountant-memory`.
- **During:** note what you read (file, sheet, range; email subject), each formula or rate you
  use, and every problem as it happens.
- **After:** record the job with the tool `accountant_job` (one call writes the ledger entry, the
  catalog lines and the links; if the tool is not available, follow the manual steps in
  `accountant-memory`) and say "บันทึกงาน J-id". If the user corrected the work, a check failed
  and was fixed, or a step here was wrong or missing, save one lesson with the tool
  `accountant_lesson` (rules in `learn-and-improve`). Record verified decisions and party
  treatments. Say in one line what was saved.
