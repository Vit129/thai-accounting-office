---
name: accountant-graph
description: >
  This skill should be used before starting any accounting job to search for what already exists,
  and whenever the user asks "หา", "ค้นหา", "มีเอกสารของ ... ไหม", "ผู้ขายรายนี้มีอะไรบ้าง",
  "ใบกำกับเลขที่ ... อยู่ไหน", "เมลเรื่อง ... อยู่ที่ไหน", "ตัวเลขนี้สืบย้อนไปถึงไหน",
  "ถ้าเปลี่ยนอัตรานี้กระทบอะไร", "ขอดูแผนที่งาน", "ทำดัชนีเอกสาร", "find the invoice",
  "search my files and mail", "trace this", "what is connected to this vendor". It is the office's
  search and map over its own PDFs, emails, Word, Excel, CSV and notes, keyed by names, document
  numbers, accounts, forms and periods.
metadata:
  version: "0.1.2"
---

# Accountant graph (search first, then trace: a light map of the office's documents)

Like a code graph, but the things in it are an accounting office's: parties (vendors, customers),
document numbers, accounts, forms, periods, files, emails, formulas, decisions and jobs. It is two
plain tab-separated files in the memory folder, searched with the file tools; no program is needed.
Formats, relations and recipes: `references/graph-format.md`.

## Tools (use these first; the files stay readable by hand)
A standard-library Python engine (`scripts/graph.py`) does the searching, id numbering, writing and
checking, so the answers are exact and repeatable. Three ways to call it, in this order:
1. **MCP tools** (the plugin starts the server when Python is installed): `accountant_find`,
   `accountant_neighbors`, `accountant_trace`, `accountant_impact`, `accountant_path`,
   `accountant_job`, `accountant_register_doc`, `accountant_party`, `accountant_lesson`,
   `accountant_index_scan`, `accountant_usage`, `accountant_problems`, `accountant_check`,
   `accountant_map`, `accountant_init`. Pass `root` (the work folder) when it is not the current
   folder, and `client` in firm mode.
2. **Command line**, when a shell is available: `python3 <this skill's folder>/scripts/graph.py
   --root <work folder> <command> ...` (commands match the tool names: find, trace, impact, job,
   check, map, index-scan, lesson, ...; `--help` lists them).
3. **By hand**, with the file tools and the recipes in `references/graph-format.md`, when neither
   is available. Say so, because ids and the period-close check are then only as careful as you are.
The engine refuses to store a 13-digit number (personal or tax ID) and an e-mail address in a lesson.
`accountant_map` writes `map.html` next to the memory; open it in a browser or show it as an artifact. The memory folder is `Accountant/memory/`
(firm mode: `Accountant/memory/<client-slug>/`; never mix clients).

- `catalog.tsv`: one line per document seen (id `K-<n>`): kind (pdf, email, xlsx, docx, md, csv,
  image), where it is, title or subject, period, parties, numbers, topics.
- `links.tsv`: one line per relation (`from`, `relation`, `to`, `via`): a job reads a document, a
  document mentions a party, a formula is used by a job, a period carries a balance to the next.
- Names that mean the same party (Thai, English, short form) are listed once as `aka:` in
  `parties.md`, so a search by any of them finds the same party.

## Search first (before every job, before asking the user for a file)
1. Take every name, document number, form, account, period and topic in the request.
2. Look them up in `catalog.tsv`, `links.tsv`, `parties.md` (including `aka:`), `sources.md`,
   `decisions.md` and `formulas.md`. Match names after dropping company-type words (บริษัท, บจก.,
   จำกัด, Co., Ltd.) and ignoring case and spaces.
3. Nothing found, or the index is thin: search live, in this order, and stop at the first good hit:
   the work folder (file names, then readable contents), the cloud storage connector (`~~cloud
   storage`), then the mailbox (`~~email`, by sender, subject, document number). Give long PDFs and
   many files to the `doc-reader` agent.
4. Show at most five candidates: what it is, where (path, or email subject, sender organisation and
   date), period, and why it matches. Ask the user to confirm; never pick between two equally good
   candidates alone. A scanned or unreadable file is reported as such, not guessed.
5. Register what was used (below) so the next search finds it in the index.

## Register (while working; `document-intake`, `inbox-triage` and every job do this)
For each document or email a job actually reads: add or update one line in `catalog.tsv` and the
edges in `links.tsv` (`job reads K-n`, `K-n mentions P-n`, `K-n for T-yyyy-mm`). Store the
title or subject, file name and path, period, party names, document numbers and topics; never the
body, amounts, salaries, personal ID numbers or account numbers. The job ledger (`accountant-memory`)
cites the same ids.

## Index (on request: "ทำดัชนีเอกสาร")
Build the catalog for a folder or a mailbox one month at a time, oldest first, so the user can stop
at any point. For each file or email: read just enough (title, header, first page, subject) to fill
a line, skipping anything already in the catalog; hand PDFs and batches to `doc-reader`. Report the
count added, files that could not be read, and parties that look like duplicates (same name,
different spelling) so the user can merge them under one `aka:`.

## Ask the map (answers cite ids and show the path)
- **Find / neighbors:** everything linked to a party, number, period or file: documents, jobs,
  decisions, formulas, periods.
- **Trace:** follow `reads` and `carries-to` back from a figure or file to the source document,
  email and period, hop by hop.
- **Impact:** before changing a formula, rate, source or decision, list the jobs and periods that
  used it (`links.tsv`, then the ledger).
- **Path:** how two things connect, for example a vendor and a filing.
- **Map ("ขอดูแผนที่งาน"):** one artifact page, updated in place, drawn from `links.tsv`: nodes by
  kind, a search box, click a node to show its neighbors. Show one party or one period at a time
  (about 300 edges at most); say what was left out.

## Check (at every period close)
Report as open items, never fix silently: ids used in a link that are not in any file, catalog
lines no job has ever read, two parties that share a name once suffixes are dropped, and a job in
the ledger that has no edges.

## Learn and remember (every job)
- **Before:** read `Accountant/lessons/accountant-graph.md` if it exists. Search first with `accountant-graph`
  (tool `accountant_find` on the names, document numbers, forms and period in the request) and
  look up `Accountant/memory/` with `accountant-memory`.
- **During:** note what you read (file, sheet, range; email subject), each formula or rate you
  use, and every problem as it happens (a name that matched two parties, a file that could not be read, a search that found nothing).
- **After:** record the job with the tool `accountant_job` (one call writes the ledger entry, the
  catalog lines and the links; if the tool is not available, follow the manual steps in
  `accountant-memory`) and say "บันทึกงาน J-id". If the user corrected the work, a check failed
  and was fixed, or a step here was wrong or missing, save one lesson with the tool
  `accountant_lesson` (rules in `learn-and-improve`). Record verified decisions and party
  treatments. Say in one line what was saved.
