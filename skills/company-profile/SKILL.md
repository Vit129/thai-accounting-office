---
name: company-profile
description: >
  This skill should be used at the start of every job, before accountant-chief, monthly-close,
  inbox-triage or any other skill in this plugin — and when the user asks "กฎของบริษัท",
  "กฎของออฟฟิศ", "หน้าที่เรามีอะไรบ้าง", "ใช้ format ไหน", "ลงชื่อท้ายเมลยังไง", "ผังบัญชี",
  "company rules", "เริ่มตั้งค่างานบัญชี", "first-time setup", "เริ่มงาน", "ตั้งค่า", or starts in an
  uninitialized folder. It holds the rules of this company or office, which override the general
  skills wherever they differ.
metadata:
  version: "0.10.1"
  last_improved: "2026-10-19"
---

# Company profile (works for any company; the answers live in the user's work folder)

These rules win over every other skill in this plugin. Background for a new session:
`references/handoff.md`. Company facts and "how this company does it" rules go into
`Accountant/company-facts.md`; lessons about how to do a task go through `learn-and-improve`.
Nothing about one company is written into this plugin: the plugin stays the same for everyone.

## Mode (asked once at setup, stored as `Mode:` in company-facts)
- **in-house**: the user keeps the books of ONE company. Wherever another skill says "client",
  read the company; ignore the multi-client register in `accountant-chief` and track jobs per period
  in `Accountant/register.xlsx` (one row per task and deadline). `accountant-dashboard` and `inbox-triage`
  use that register wherever they say client register.
- **firm**: the user serves many clients; use the client register in `accountant-chief`.

## Step 0 — which state is this folder in? (every job; the user never needs a magic phrase)
Tell the user the state in one line before working.
- **Old folder name**: no `Accountant/` folder but `Office/` or `AODD/` exists with a
  `company-facts.md`. This is a folder set up by an earlier version. Say so, show what is in it,
  and ask before renaming it to `Accountant/` (a rename, never a copy and never a delete); after
  the yes, rename it, then continue with the state it is in. Do not run setup over it.
- **New**: no `Accountant/company-facts.md` and no old folder. Run setup from step 1.
- **Setup unfinished**: `company-facts.md` exists but lacks a `Setup: done <date>` first line, or
  `CLAUDE.md`, `Accountant/register.xlsx`, `Accountant/lessons/` or `Accountant/memory/` is missing. Say what is missing and resume
  from that step; do not redo finished steps or re-ask answered gaps.
- **Plugin updated**: the `Template version` line in the folder's `CLAUDE.md` differs from
  `references/work-folder-CLAUDE.md`. Show the difference and ask before updating it.
- **Working**: everything is present. Do the job.

"เริ่มตั้งค่า", "เริ่มงาน", "ตั้งค่า" or "ตั้งค่าใหม่" on a Working folder: show the current facts
and ask which to change. Never wipe `Accountant/`.

## Setup
1. Read `references/handoff.md`. Copy `references/work-folder-CLAUDE.md` to `CLAUDE.md` at the
   work folder root; if one exists, show the difference and ask before changing it.
2. In the work folder create `Accountant/` (the tool `accountant_init` creates the memory files in one call; do the rest by hand) with `lessons/`, `reviews/`, `memory/` (an `index.md` from the
   templates in `accountant-memory`'s `references/memory-format.md`, plus empty `parties.md`,
   `decisions.md`, `recurring.md`, `periods.md`, `sources.md`, `formulas.md`, `ledger/`, and
  `catalog.tsv` and `links.tsv` with the header lines in `accountant-graph`'s `references/graph-format.md`; in firm
   mode one subfolder per client when a client is added), `register.xlsx` (sheet `Tasks`: task, period, deadline, status, waiting on)
   and `company-facts.md`.
3. Ask in ONE message for the facts below, with a recommended answer for each; accept "ไม่รู้" and
   leave that line as `<unknown>` for `company-tune-up` to ask later.
4. Fill `register.xlsx` with this month's deadlines from `monthly-close` (ภ.ง.ด.1, 3, 53, 54,
   ภ.พ.30, ภ.พ.36, สปส.1-10) and the payroll date. Then write `Setup: done <YYYY-MM-DD>` as the
   first line of `company-facts.md`; that line marks the folder as Working.
5. Tell the user the assistant can be tuned at any time ("ปรับได้ตลอดเวลา"): `company-tune-up`
   runs for the first two months from the setup date.

## Facts to collect (saved to `Accountant/company-facts.md`, one line each, shown before saving)
- Company or office name (Thai / English), Mode (in-house / firm), fiscal year
- Executive who approves payroll, payments and filings; who reviews before anything goes out
- Outside parties: accounting service for payroll (firm, contact, payroll date), external auditor
  (firm, contact, year-end date), banks
- Tools: email, files, spreadsheets, accounting software; file naming
- Writing: language and tone, sign-off block
- Accounting conventions: chart of accounts, tax scheme (sme / general / boi), inventory method,
  capitalization threshold, depreciation method, rounding, cut-off and accrual rules
- Foreign SaaS accounts (check the Tax ID is entered in each vendor's billing profile to avoid
  double VAT)

## Duty → skill
| Duty | Use |
|---|---|
| Day-to-day transactions, ledger, bank payments | `payment-prep` (a payment is prepared, never released), `document-intake`, `thai-accountant` |
| Monthly, quarterly, annual closing; financial statements | `monthly-close`, `adjusting-entries`, `year-end-close`, `financial-statements`, `half-year-tax` |
| Budget forecasts, tracking performance | `budget-tracking` |
| Reconcile AP and AR | `reconcile-check` |
| WHT and tax filings | `monthly-close` (domestic), `foreign-saas-tax` (foreign cloud and SaaS) |
| Audit documents, company policy | `audit-readiness`, `auditor` agent before anything is reported or filed |
| Verify payroll before executive approval | `payroll-check` |
| Coordinate with teams and outside parties | `inbox-triage` (drafts only, the user sends) |
| Look up or record what this company decided, party treatments, recurring entries, period balances | `accountant-memory` |

## Confidentiality and backups
- Salaries, ID numbers and bank accounts stay in the work folder; never paste them into email
  drafts to people outside the approver list, and never into lessons or tune-up reports.
- Never enter or store banking passwords anywhere.
- At every month-end close confirm the books and `Accountant/` exist in a second place and note the
  backup date in the close summary. No backup this month: say so as an open item.

## Tax rate overrides
Rates in the skills (WHT, treaty, depreciation) are defaults with their source. The company's own
rate goes under `## Tax rate overrides` in `Accountant/company-facts.md` as
`- <item>: <rate> (source: <ruling / auditor / date>)` and wins over the skill. When the user
states a different rate, ask once whether to record it. `adjusting-entries`, `inventory-cogs`,
`half-year-tax` and `year-end-close` read these policies from that file.

## Extending for one company
Company-specific rules are data, not plugin code: add a line to `company-facts.md`. A rule that
changes how a skill works goes to `Accountant/lessons/<skill>.md` through `learn-and-improve`, or to
`Accountant/tune-up.md` when it needs a plugin change.

## Learn and remember (every job)
- **Before:** read `Accountant/lessons/company-profile.md` if it exists. Search first with `accountant-graph`
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
