---
name: monthly-close
description: >
  This skill should be used when the user asks to "ปิดงวด", "ปิดบัญชีเดือนนี้", "ทำ ภ.พ.30",
  "ยื่น ภ.ง.ด.1/3/53/54", "ภาษีหัก ณ ที่จ่าย", "ประกันสังคม สปส.1-10", "month-end close",
  "what is due this month", or checks filing deadlines for one or all clients. Not for annual
  statements or ภ.ง.ด.50 planning — use thai-accountant for those.
metadata:
  version: "0.1.3"
---

# Monthly close for one client (repeat per client)

Read `Accountant/lessons/monthly-close.md` first if it exists. Use `thai-accountant`
(`skills/thai-accountant/references/tax-accounting.md`, `skills/thai-accountant/references/general-accounting.md`) for treatment questions.

## Deadlines (day of the following month)
| Return | Paper | e-Filing | Applies when |
|---|---|---|---|
| ภ.ง.ด.1, 3, 53 (WHT) | 7 | 15 | paid salary / individuals / companies with WHT |
| ภ.ง.ด.54 (WHT on payments abroad) | 7 | 15 | paid a foreign company (service fees, royalties, licences, interest) — usually filed with ภ.พ.36 |
| ภ.พ.36 (VAT on foreign services) | 7 | 15 | paid a foreign provider |
| ภ.พ.30 (VAT) | 15 | 23 | VAT registered |
| สปส.1-10 (social security) | 15 | 15 | has employees |
Before every filing, check the Revenue Department / SSO announcements for the current year —
e-filing extensions and holiday shifts change these dates. If a date moved, record it as a
lesson.

## Steps
1. **Collect** — from the client folder and `inbox-triage`: sales and purchase tax invoices,
   receipts, bank statements, payroll, WHT certificates (50 ทวิ) issued and received.
   Missing documents → list them for the user to request from the client (draft, never send).
2. **Book** — post the period into the client workbook in ~~spreadsheet (sheets: `GL`,
   `Sales-VAT`, `Purchase-VAT`, `WHT`, `Bank`). One row per document; keep the document link.
3. **Adjust** — run `adjusting-entries`: record recurring accruals (utilities, rent, interest),
   amortize prepayments, update fixed asset depreciation, and if trading/manufacturing, run
   `inventory-cogs` for month-end stock and COGS.
4. **VAT** — output VAT from the sales report, input VAT only from valid tax invoices dated in a
   period still claimable; flag invoices that fail `document-intake`'s tax-invoice check.
5. **WHT** — every payment that needs withholding has a 50 ทวิ; totals per form match the WHT sheet.
6. **Reconcile** — run `reconcile-check` (trial balance, bank, VAT, WHT, fixed assets, accruals). Do not continue on a fail.
7. **Prepare** — fill the return figures into a `Filing-<period>` sheet with each figure's
   source formula visible. Filing itself is the user's action (stop-and-ask).
8. **Close** — update the client register status and next deadline; refresh `accountant-dashboard`.

## Output
A short Thai summary per client: figures per return, checks passed, what is waiting for the
user (approval to file, documents to request), and the next deadline.

## Learn and remember (every job)
- **Before:** read `Accountant/lessons/monthly-close.md` if it exists. Search first with `accountant-graph`
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
