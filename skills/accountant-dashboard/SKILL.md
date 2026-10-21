---
name: accountant-dashboard
description: >
  This skill should be used when the user asks for "dashboard", "ภาพรวมงาน", "งานค้างลูกค้า",
  "อะไรใกล้ deadline", "สถานะลูกค้าทุกราย", "office overview", or after accountant-chief finishes a
  job. It builds or refreshes one artifact page that shows every client's status, upcoming
  deadlines, reconciliation results, and proposals waiting for the user.
metadata:
  version: "0.1.3"
---

# Accountant dashboard (artifact)

Read `Accountant/lessons/accountant-dashboard.md` first if it exists.

## Data
Build only from the client register (`Accountant/client-register`), each client's latest
`reconcile-check` result, open drafts from `inbox-triage`, statutory milestone trackers (monthly VAT/WHT/SSO,
half-year ภ.ง.ด.51, annual ภ.ง.ด.50, DBD ส.บช.3, บอจ.5, and audit readiness), the latest `Accountant/reviews/` file, and the job ledger (`accountant-memory`: `Accountant/memory/ledger/`).
Never invent a status; a missing value shows as "—".

## Page (one artifact, updated in place — reuse the same artifact every time)
1. **Today** — count of clients by status; unfinished jobs (`jobs/*-progress.md` with `Status: open`: client, job, next open step); deadlines in the next 7 days (monthly filings, ภ.ง.ด.51, ภ.ง.ด.50, DBD), red when ≤ 3 days.
2. **Clients table** — client, period, status, next deadline (tax/DBD/audit), last check result (pass/fail),
   waiting for (documents / approval / client reply / audit sign-off). Sortable by deadline.
3. **Statutory Cycle Status** — summary cards for Monthly Closings, Half-Year CIT (ภ.ง.ด.51), Annual CIT (ภ.ง.ด.50), and DBD e-Filing readiness.
4. **Checks** — failed reconciliation checks with the difference and the client.
5. **Waiting for your decision** — every stop-and-ask item with its why, newest first.
6. **Learning** — lessons saved this week, the weekly review's proposals, jobs run this week per
   skill from the ledger, and problems that repeated.

## Design
Thai labels, plain and readable; status colours that also carry a text label (not colour
only); works on a phone. Amounts with thousands separators and 2 decimals. Show the time the
data was last refreshed.

## Privacy
The artifact stays private unless the user shares it. Show client codes instead of full names
if the user asks for a shareable version.

## Learn and remember (every job)
- **Before:** read `Accountant/lessons/accountant-dashboard.md` if it exists. Search first with `accountant-graph`
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
