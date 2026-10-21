---
name: document-intake
description: >
  This skill should be used when the user shares or receives accounting documents — "อ่านใบกำกับภาษี",
  "ลงบัญชีจากเอกสารนี้", "สแกนใบเสร็จ", "ดึงข้อมูลจาก PDF", "bank statement", "50 ทวิ", "invoice",
  "receipt", "import this statement" — and the data has to go into a client workbook. It extracts
  fields, checks tax-invoice validity, and writes rows with a link back to the source file.
metadata:
  version: "0.1.3"
---

# Document intake

Read `Accountant/lessons/document-intake.md` first if it exists. Use the pdf / xlsx / docx skills to
read files; for many documents, give batches to the `doc-reader` agent.

## Extract (one row per document)
date · document type · document number · counterparty name · counterparty tax ID + branch ·
description · amount before VAT · VAT · WHT (if any) · total · currency · source file link.

## Tax invoice check (full tax invoice, Revenue Code s.86/4)
The words "ใบกำกับภาษี" · seller name, address, 13-digit tax ID (and branch) · buyer name and
address (and tax ID + branch when the buyer is VAT registered) · invoice number · description,
quantity and value · VAT shown separately · issue date. Missing items → mark the row
`input VAT not claimable` with the reason, and list it for the user.

## Bank statements
Import every line with date, description, debit, credit, running balance. Check that opening
balance + movements = closing balance before using the data.

## Dates, numbers and encoding (Thai Windows / Excel)
- Thai-locale Windows and Excel often show Buddhist-era years (2569 = 2026). A year above 2400 is
  B.E.: subtract 543. Store real date values (or ISO `YYYY-MM-DD`), never date-looking text.
- Amounts: strip thousands separators and "บาท"; a trailing or bracketed minus is negative.
- Prefer `.xlsx`. If a CSV is needed for Excel on Windows, write it as UTF-8 **with BOM** so Thai
  text opens correctly; read CSVs as UTF-8 first, then TIS-620 / Windows-874 if Thai is garbled.
- File and folder names: no `\ / : * ? " < > |`; keep full paths short (OneDrive / SharePoint
  paths over ~250 characters fail on Windows).

## Write
- Append to the client workbook sheet (`Purchase-VAT`, `Sales-VAT`, `Bank`, `WHT`) in
  ~~spreadsheet; never overwrite existing rows.
- Skip a document whose (number + seller tax ID) already exists — report it as a duplicate.
- Report counts: read, written, duplicates, failed tax-invoice checks, unreadable files.

## Register what you read
For each document this job reads, add or update its line in `Accountant/memory/catalog.tsv` and the
edges in `links.tsv` with `accountant-graph` (title or subject, path or sender organisation, period,
parties, document numbers; never the body or amounts), so the next search finds it.

## Learn and remember (every job)
- **Before:** read `Accountant/lessons/document-intake.md` if it exists. Search first with `accountant-graph`
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
