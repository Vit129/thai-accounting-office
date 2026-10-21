---
name: audit-readiness
description: >
  This skill should be used to assemble external audit working papers, lead schedules, bank and
  receivable confirmation requests, and the statutory audit pack for CPA or TA review — when the
  user says "เตรียมตรวจบัญชี", "ส่งผู้สอบบัญชี", "กระดาษทำการผู้สอบ", "หนังสือยืนยันยอด", "audit pack",
  "bank confirmation", "AR confirmation", "working papers", or "lead schedule".
metadata:
  version: "0.1.2"
---

# External Audit Readiness & Working Papers (การเตรียมเอกสารและกระดาษทำการส่งผู้สอบบัญชี)

Read `Accountant/lessons/audit-readiness.md` first if it exists. Consult `thai-accountant`
(`skills/thai-accountant/references/compliance.md`, `skills/thai-accountant/references/reporting-disclosure.md`) for auditing standards.

In Thailand, all private companies and registered partnerships must have their financial statements
audited by an independent Certified Public Accountant (CPA) or Tax Auditor (TA for small partnerships).
This skill organizes client accounts into a standardized audit package to minimize audit queries and
ensure smooth sign-off.

---

## 1. Audit Lead Schedules (ผังกระดาษทำการตามหมวดบัญชี)

Every balance sheet and income statement account must trace to a Lead Schedule indexed by standard code:

| Index | Section | Components & Required Supporting Docs |
|---|---|---|
| **A** | Cash & Cash Equivalents | Bank reconciliation for all accounts at year-end, 12 months of bank statements, year-end bank confirmation letters, petty cash count certificates |
| **B** | Trade & Other Receivables | AR ageing report (0-30, 31-60, 61-90, >90 days), subsequent collection receipts, sample sales invoices, AR confirmation replies, doubtful debt calculations |
| **C** | Inventories | Physical stock count sheets signed by witnesses, unit cost verification schedules, lower of cost or net realizable value (LCNRV) assessment |
| **D** | Property, Plant & Equipment | Fixed asset register, capital additions invoices, disposal calculations and scrap sales invoices, depreciation computation schedules |
| **E** | Other Assets | Prepaid expense amortization schedules, deposit contracts, withholding tax certificates pending refund |
| **F** | Trade & Other Payables | AP ageing, supplier statements, AP confirmation letters, search for unrecorded liabilities (invoices dated post-period) |
| **G** | Loans & Borrowings | Bank loan agreements, director loan contracts with board approval, debt repayment schedules, year-end loan balance confirmations |
| **H** | Accruals & Provisions | Computation of accrued expenses (bonus, utilities, audit fee), employee benefit obligations valuation |
| **I** | Equity | Shareholder register (บอจ.5), share certificates, board and AGM minutes approving dividends or capital increases |
| **J** | Profit & Loss | Monthly revenue and expense trend analysis, gross margin variance explanations, 12 months of ภ.พ.30, ภ.ง.ด.1/3/53/54, ภ.ง.ด.51 |

---

## 2. External Confirmation Letters (หนังสือยืนยันยอดภายนอก)

Prepare formal confirmation request letters on client letterhead for management signature:
1. **Bank Confirmation (หนังสือยืนยันยอดธนาคาร)**: Standard Thai Bankers' Association format
   requesting balances, credit facilities, guarantees, contingent liabilities, and authorized signatories.
2. **Trade Receivable / Payable Confirmation (หนังสือยืนยันยอดลูกหนี้และเจ้าหนี้)**:
   - Positive confirmation: Requesting customer/vendor to confirm balance directly to the auditor.
   - List customer name, tax ID, outstanding invoice numbers, and total balance as of fiscal year-end.
3. **Legal Counsel Inquiry Letter (หนังสือยืนยันภาระผูกพันคดีความ)**:
   - For pending litigation, labour claims, or disputes handled by external legal advisors.

---

## 3. Mandatory Statutory Compliance Package

Collect and index corporate governance files for auditor inspection:
- Certificate of Incorporation (หนังสือรับรองนิติบุคคล) dated within 1 month.
- Memorandum and Articles of Association (หนังสือบริคณห์สนธิ และข้อบังคับบริษัท).
- Minutes of Board of Directors meetings and Shareholder meetings held during the fiscal year.
- Copy of prior year's audited financial statements and CPA management letter.
- Annual summary reports: ภ.ง.ด.1ก (annual payroll WHT summary), social security contribution cards.

---

## 4. Execution Steps

1. **Verify Trial Balance**: Run `year-end-close` and confirm post-closing Trial Balance is final.
2. **Populate Lead Schedules**: Link GL balances into standardized A to J audit schedules.
3. **Draft Confirmations**: Generate bank and debtor confirmation letters; present to user for client signing.
4. **Compile Audit Pack**:
   - Create organized folder `Accountant/audit-pack/<fiscal-year>/` with standardized indexing.
5. **Pre-Audit Review**: Hand over the full pack to `auditor` agent to cross-check numbers against the trial balance.
6. **Stop-and-Ask**: Present completed audit pack to the user for formal handover to the external CPA/TA.

---

## 5. Output

Thai summary report:
- Audit readiness scorecard (Readiness percentage, missing documents, unconfirmed accounts).
- Links to Lead Schedules (A to J) with formulas visible.
- Confirmation tracking table (Sent date, Response received, Discrepancies noted).

## Learn and remember (every job)
- **Before:** read `Accountant/lessons/audit-readiness.md` if it exists. Search first with `accountant-graph`
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
