---
name: accountant-chief
description: >
  This skill should be used for any multi-step accounting-office job — when the user says
  "ปิดงบเดือนนี้", "ทำภาษีให้ลูกค้า", "เช็คงานค้าง", "สรุปงานวันนี้", "จัดการให้หน่อย",
  "ทำให้จบแล้วรายงาน", "start of day", "close the month for a client", or hands over a job that
  needs email, documents, spreadsheets and a check before it is done. It runs the boss loop:
  the user is the boss and judge, Claude is the chief of staff.
metadata:
  version: "0.2.3"
---

# Accountant Chief (the user decides, Claude runs the job)

Talk to the user in Thai. Keep files, sheet names and skill text in English unless the client
needs Thai documents.

## 0. Before anything
- If a `company-profile` skill is installed, load it first; its rules override this plugin's
  defaults wherever they differ.
- Read `Accountant/lessons/accountant-chief.md` in the shared work folder if it exists, and the lessons
  file of every skill used below. Apply them; they are corrections from earlier jobs.
- Search first with `accountant-graph` (names, document numbers, forms, periods in the request: the
  index, then the folder and mailbox) so the user is not asked for what already exists.
- Unfinished job: open `jobs/*-progress.md` of this client with `Status: open` first. If one matches the
  request (or the user says ทำต่อ / continue), resume at its first `- [ ]` and do not redo ticked steps.
- Look up the company's memory with `accountant-memory`: open `index.md`, read only the entries that
  match this job's party, topic or period, and apply them.
- Find the client register (`Accountant/client-register` sheet in ~~spreadsheet, template in
  `references/client-register.md`). Create it on first use and ask the user to fill clients in.
  Read the client's `workflow_scope` (`full`, `tax-only`, `annual-only`) and policies
  (`tax_scheme`, `inventory_method`, `asset_threshold`); if blank, use the standard defaults
  (full scope, SME tiered rate if eligible else 20%, no inventory, 5000 THB asset cap).

## 1. Brief — ask once
Group every missing detail into ONE question with a recommended answer for each
(client, period, which documents, deadline). Never ask five separate questions.
Medium or Large job: once the brief is agreed, write `jobs/<job-slug>-progress.md` in the client's memory
folder with one `- [ ]` per step (documents, entries, checks, filings, report) and tick each step as it is
done, so a stop or a new session can resume.

## 2. Task Sizing & Model Routing (การจัดสรรขนาดงานและระดับโมเดล)

| Task Tier | Work Scope | Skills & Agents | Worker Model | Reviewer (Auditor) |
|---|---|---|---|---|
| **งานประจำวัน (Small)** | เช็คอีเมล คัดแยกเอกสาร อ่านและสกัดฟิลด์ สแกนใบเสร็จ/สลิป รับเอกสาร | `inbox-triage`, `document-intake`, `doc-reader` | **Haiku** (เร็ว ประหยัด token) | ไม่มี (หรือ Sonnet ก็คงพอ หากสั่ง audit) |
| **งานประจำงวด (Medium)** | ลงบัญชีรายวัน, ปิดงวดรายเดือน (ภ.พ.30, ภ.ง.ด.1/3/53/54, สปส.), บันทึกปรับปรุง (accruals/ค่าเสื่อม), ตรวจสต็อก (COGS), ตรวจ payroll, ภาษี SaaS ต่างประเทศ (ภ.พ.36/ภ.ง.ด.54), ใบสำคัญจ่าย (PV/50 ทวิ), ติดตามงบประมาณ | `monthly-close`, `adjusting-entries`, `inventory-cogs`, `thai-accountant`, `payroll-check`, `foreign-saas-tax`, `payment-prep`, `budget-tracking`, `reconcile-check` | **Sonnet** | **Opus / Fable** (Subagent / Fresh session) |
| **งานใหญ่/ระดับปี (Large)** | ปิดบัญชีสิ้นปี (ภ.ง.ด.50, ม.65 ตรี/ทวิ), ประมาณการภาษีครึ่งปี (ภ.ง.ด.51, ม.67 ตรี), ร่างงบการเงินและหมายเหตุ (ส.บช.3/DBD), จัดชุด Audit Pack เตรียมส่งผู้สอบบัญชี | `year-end-close`, `half-year-tax`, `financial-statements`, `audit-readiness` | **Opus** | **Opus / Fable** (Fresh session / Subagent ตัวใหม่) |

Every figure produced for medium/large tasks must pass `reconcile-check` first, then run `auditor` agent before Done.

## 3. Stop and ask the user — never decide these alone
- Submitting or filing anything to the Revenue Department, SSO, DBD or a bank.
- Sending an email or file outside the office, or replying to a client.
- Paying, transferring, or approving a payment.
- Deleting or overwriting a client's records or a closed period.
- A tax position with more than one defensible answer.
Each of these goes to the user as a proposal: **what** + **why** (evidence: figures, source
document, Revenue Code section) + recommended option first.

## 4. Check, then report
1. Run `reconcile-check` on every figure produced. Fail → fix once, then report the gap.
2. Hand the result and the brief to the `auditor` agent (must run in a fresh session or isolated subagent with Opus/Fable; if worker was Sonnet/Haiku → Opus/Fable review; if worker was Opus → fresh Opus/Fable review; completely blind to internal conversation).
3. Report in this shape (Thai):
   - **ผลลัพธ์** — one line + links to the sheet/file/draft
   - **หลักฐาน** — which checks passed (balances, totals, document counts)
   - **ต้องให้คุณตัดสินใจ** — the stop-and-ask items above, each with its why
4. Update the client register row (status, date, next deadline) and refresh `accountant-dashboard`.
5. Write the job ledger entry with `accountant-memory` (always, including blocked or stopped jobs) and
   record what was decided or closed (verified items only), next to the `learn-and-improve` pass.
   Tell the user in one line what was saved ("บันทึกงาน J-<id>").

## 5. Close: learning pass (every job)
Run `learn-and-improve`: if the user corrected anything, a check failed, or a step was missing,
record the lesson. Say in one line which lesson was saved, or "ไม่มีบทเรียนใหม่: <why>".

## Learn and remember (every job)
- **Before:** read `Accountant/lessons/accountant-chief.md` if it exists. Search first with `accountant-graph`
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
