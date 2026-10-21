---
name: inbox-triage
description: >
  This skill should be used when the user asks to "เช็คอีเมล", "สรุปอีเมลลูกค้า", "มีเมลอะไรบ้าง",
  "ร่างตอบลูกค้า", "ดึงเอกสารจากเมล", "triage my inbox", "draft a reply", or at the start of a
  working day. It reads ~~email, sorts messages by client and action, saves attachments to the
  client folder, and drafts replies. It never sends.
metadata:
  version: "0.1.3"
---

# Inbox triage

Read `Accountant/lessons/inbox-triage.md` first if it exists.

1. Pull unread / recent mail from ~~email (default: since the last triage, or the last 2 days).
   For more than ~20 messages, hand batches to the `doc-reader` agent and work from its summaries.
2. Match each message to a client in the client register (sender domain, name, tax ID in the
   body). Unknown sender → "unmatched" group; do not guess.
3. Classify: **documents in** (invoices, receipts, statements, payroll) · **question from client**
   · **request from authority** (Revenue Department, SSO, DBD, bank) · **internal** · **noise**.
4. Documents in → save attachments to the client folder in ~~cloud storage, then run
   `document-intake` on them.
5. Questions → draft a reply in Thai (polite business tone, the office's sign-off) as a draft in
   ~~email. Use `thai-accountant` for the substance and cite the rule in plain words.
6. Authority requests → always flag to the user at the top, with the deadline in the letter.
7. Report (Thai): a table per client — what came in, what was saved, drafts waiting, and
   anything due. Update the client register `status` when documents arrive.

## Never
- Send, forward, or reply on the user's behalf. Drafts only; the user presses send.
- Open links or attachments that look like phishing (mismatched sender, urgent payment change,
  password requests) — flag them instead.
- Copy client data into lessons or skills.

## Register what you read
For each email or attachment this job reads, add or update its line in `Accountant/memory/catalog.tsv` and the
edges in `links.tsv` with `accountant-graph` (title or subject, path or sender organisation, period,
parties, document numbers in the subject; never the body or amounts), so the next search finds it.

## Learn and remember (every job)
- **Before:** read `Accountant/lessons/inbox-triage.md` if it exists. Search first with `accountant-graph`
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
