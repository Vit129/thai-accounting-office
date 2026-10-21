---
name: payroll-check
description: >
  This skill should be used when the payroll file from the payroll preparer (an outsourced accounting service or HR) arrives,
  or the user says "เช็คเงินเดือน", "ตรวจ payroll", "สรุปเงินเดือนให้ผู้บริหาร", "ภ.ง.ด.1 เดือนนี้",
  "สปส. เดือนนี้", "check payroll". It verifies the payroll before the executive approves it.
metadata:
  version: "0.1.3"
---

# Payroll check (before executive approval)

Read `Accountant/lessons/payroll-check.md` first if it exists. The payroll preparer prepares payroll;
this skill checks it. Never change the payroll file itself and never release a payment.

## Checks (each one pass / fail with the figures)
1. **Headcount** — employees paid = last month ± joiners and leavers the user confirms (HR email
   or list). Anyone new or missing is named.
2. **Gross pay** — each person's base matches last month unless a raise, bonus, OT or unpaid leave
   is documented. List every change with its reason or "no document".
3. **Social security** — 5% of wages capped at the current monthly ceiling (check the SSO rate for
   this year; it changes) for employee and employer; totals match the สปส.1-10 figures.
4. **WHT (ภ.ง.ด.1)** — tax per person is plausible against annualized income and last month;
   the ภ.ง.ด.1 total equals the payroll WHT total.
5. **Net pay** — gross − SSO − WHT − other deductions = net, per person and in total; the total
   equals the bank transfer file amount.
6. **GL** — the payroll journal (salary expense, SSO payable, WHT payable, accrued salary) balances
   and ties to the trial balance (`reconcile-check`).

## Output
A one-page Thai summary for the executive: totals (gross, SSO, WHT, net), headcount, changes from
last month with reasons, and failed checks as questions for the accounting service (draft email,
not sent). Show salaries only to the user and the approver named in `company-profile`.

## Learn and remember (every job)
- **Before:** read `Accountant/lessons/payroll-check.md` if it exists. Search first with `accountant-graph`
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
