---
name: reconcile-check
description: >
  This skill should be used before any figure is filed, sent to a client, or reported — when the
  user says "กระทบยอด", "เช็คตัวเลข", "งบทดลองตรงมั้ย", "reconcile", "check the numbers",
  "ยอด VAT ตรงมั้ย", or when another skill reaches its check step. It is the accounting office's
  equivalent of a test suite: work is not done until these checks pass.
metadata:
  version: "0.1.2"
---

# Reconciliation checks (the "tests" of the office)

Read `Accountant/lessons/reconcile-check.md` first if it exists. Run every check that applies, then
report a table: check | expected | actual | difference | pass/fail. A difference of 0.00 passes;
anything else fails unless the user accepted a documented reason.

| # | Check | How |
|---|---|---|
| 1 | Trial balance | total debits = total credits for the period and year to date |
| 2 | Bank | book balance ± outstanding items = bank statement closing balance, per account |
| 3 | Output VAT | sales VAT report = VAT on sales in GL = ภ.พ.30 output figure |
| 4 | Input VAT | purchase VAT report = claimable input VAT in GL = ภ.พ.30 input figure; every line backed by a valid tax invoice |
| 5 | WHT | sum of 50 ทวิ per form = WHT payable in GL = ภ.ง.ด. figure |
| 6 | Payroll / SSO | contributions = rate × capped wage per employee; total = สปส.1-10 |
| 7 | Sub-ledgers | AR and AP ageing totals = control accounts |
| 8 | Spreadsheet health | no `#REF!`, `#VALUE!`, `#DIV/0!`, `#N/A`; no hard-coded totals where a formula is expected; totals use the full range |
| 9 | Documents | every booked line links a source document; none counted twice (same tax invoice number + seller) |
| 10 | Dates | no B.E. years stored as C.E. (or the reverse); every date in the period being closed |
| 11 | Fixed Assets & Depr | asset register cost & acc. depr = GL balances; depr expense matches schedule; tax vs book depr differences identified |
| 12 | Accruals & Prepayments | accrual schedules = GL accrued accounts; prepayments amortized for expired periods; unearned revenues recognized |
| 13 | Inventory & COGS | physical count / perpetual sub-ledger = GL inventory; beginning + purchases - ending = COGS; VAT assessed on missing stock |
| 14 | Tax Reconciliation | accounting profit ± Section 65 Ter & 65 Bis items = taxable net profit; ภ.ง.ด.50 credits match 50 ทวิ & ภ.ง.ด.51 |
| 15 | Half-year Forecast | projected ภ.ง.ด.51 taxable net profit tested against Section 67 Ter 25% threshold or meets Ruling Paw. 50/2537 safe harbor |

## Rules
- Compute every figure from the source rows yourself; never trust a total typed in a cell.
- For Excel files use the xlsx skill to read values and formulas; for Google Sheets read the
  ranges through ~~spreadsheet.
- A failed check is reported with the rows that cause it, not just the difference.
- Never "fix" a failing check by editing the expected figure. Find the wrong entry.

## Learn and remember (every job)
- **Before:** read `Accountant/lessons/reconcile-check.md` if it exists. Search first with `accountant-graph`
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
