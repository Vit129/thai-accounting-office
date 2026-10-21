---
name: company-tune-up
description: >
  This skill should be used during the first two months after setup (counted from the
  "Setup: done" date in Accountant/company-facts.md), or any time fine-tuning is needed — when the user
  says "สรุปวันนี้", "จบวัน", "วันแรก", "สัปดาห์แรก", "สรุปสัปดาห์", "ปรับผู้ช่วยให้เข้ากับบริษัท",
  "จูนระบบ", "ปรับระบบ", "ที่นี่ทำแบบนี้", "ยังไม่ตรง", "fine-tune", "end of day", or when
  company-facts.md still has open gaps. It tunes the plugin to match how the company really works.
metadata:
  version: "0.3.2"
  last_improved: "2026-10-19"
---

# Company tune-up: calibrate the assistant to the company

The plugin was built before anyone saw this company. For the **first two months after setup**
the assistant can be tuned at any time ("ปรับได้ตลอดเวลา") so it matches how the company really
works. Talk in Thai, keep it under five minutes for the user.

## Flexible tuning triggers
The user needs no magic phrase. Activate this skill when:
- the user says one of the phrases in the description;
- the user says a workflow differs from company practice;
- a task finishes within the calibration window and `Accountant/company-facts.md` still has `<unknown>` gaps.

## End of each day or on-demand tuning ("สรุปวันนี้")
1. **What happened** — list today's jobs from the conversation and `Accountant/register.xlsx`
   (one line each: job, done / waiting, on whom).
2. **Ask at most 3 questions**, picked from the facts list in `company-profile` that are still
   `<unknown>`, most useful first (approver, accounting software, chart of accounts, payroll
   date, banks, fiscal year, file locations, sign-off). Offer a recommended answer when the
   day's work suggests one.
3. **Write** the answers into `Accountant/company-facts.md` (show each line before saving).
4. **Mismatches** — where today's work did not fit a skill (a step that does not exist here, a
   form or report the skill does not know, a different approval flow), write one line each to
   `Accountant/tune-up.md`: date · skill · what the company does instead · example (no salaries, ID
   numbers or bank accounts).
5. Tell the user in one line what was saved and what is still unknown.

## End of each week ("สรุปสัปดาห์")
Read `Accountant/tune-up.md`, `Accountant/company-facts.md` and `Accountant/lessons/`, then write
`Accountant/tune-up-week-<n>.md` in English for the plugin's maintainer:
- **Facts still missing** (from `company-profile`).
- **Skill changes needed** — per skill: what to change, why (the dated examples), proposed text.
- **New skills needed** — recurring work no skill covers, with how often it happens.
- **Working well** — skills used without corrections (keep as is).
Tell the user: "ส่งไฟล์ `Accountant/tune-up-week-<n>.md` ให้คนที่ทำผู้ช่วยนี้ เพื่อทำเวอร์ชันใหม่".
Check the file holds no client, salary or personal data before saying it can be sent.

## After the first two months
Stop prompting daily. Keep `tune-up.md` for mismatches found later; the weekly
`learn-and-improve` review takes over.

## Learn and remember (every job)
- **Before:** read `Accountant/lessons/company-tune-up.md` if it exists. Search first with `accountant-graph`
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
