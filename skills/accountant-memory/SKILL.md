---
name: accountant-memory
description: >
  This skill should be used at the start of every accounting job (to look up what this company
  already decided and where its numbers come from), at the end of every job (to write the job
  ledger and record what was decided), and when the user says "จำไว้ว่าบริษัทนี้",
  "ครั้งก่อนเราทำยังไง", "เคยตัดสินใจเรื่องนี้ยังไง", "ตัวเลขนี้มาจากไหน", "ใช้ไฟล์ไหน", "ใช้สูตรไหน",
  "เมลเรื่องอะไร", "งานนี้ทำเมื่อไหร่", "ผู้ขายรายนี้หัก ณ ที่จ่ายยังไง", "ยอดยกมา", "สถานะงวดนี้",
  "what did we decide", "where did this number come from", "trace this figure". It keeps the
  company's permanent record of decisions, sources, formulas and every job in the work folder.
metadata:
  version: "0.3.3"
---

# Accountant memory (a permanent, searchable record of the work, kept in the work folder)

The memory belongs to one company and lives only in its work folder; nothing from it is written
into this plugin. Talk to the user in Thai; write the files in English (party names, file names and
email subjects stay as they are). Formats and empty templates: `references/memory-format.md`.

## Where it lives
- **in-house** (`Mode:` in `Accountant/company-facts.md`): `Accountant/memory/`
- **firm**: `Accountant/memory/<client-slug>/`, one folder per client. Open only the folder of the
  client of this job and never copy a fact from one client's folder into another's.

| File | Holds |
|---|---|
| `index.md` | one line per entry below, the map to open first |
| `parties.md` | how a vendor, customer or payee is treated (WHT, VAT, account) |
| `decisions.md` | judgment calls and approved treatments, with basis and approver |
| `recurring.md` | monthly entries and their usual amounts |
| `periods.md` | status and carried-forward balances per period |
| `sources.md` | files, sheets, ranges and email senders/subjects that jobs read from, and their quirks |
| `formulas.md` | formulas and rates in use: expression, authority, where used |
| `catalog.tsv`, `links.tsv` | the document catalog and the relations between jobs, documents, parties, formulas and periods (`accountant-graph`) |
| `jobs/<job-slug>-progress.md` | a Medium/Large job that may span sessions: one `- [ ]` line per step, ticked as it is done, `Status: open` → `Status: done` when the ledger entry is written |
| `ledger/<YYYY-MM>.md` | one entry per job, written every time: when, what it read, what it used, what it made, what went wrong |

## Which store holds what
| Question | Store |
|---|---|
| A standing rule or policy of the company (conventions, tax scheme, approvers) | `Accountant/company-facts.md` |
| A task and its deadline | `Accountant/register.xlsx` |
| How to do a kind of job better (no company data) | `Accountant/lessons/<skill>.md` (`learn-and-improve`) |
| What this company decided, where numbers come from, what each job did | this memory |

## Look up (before the work)
0. Search first with `accountant-graph`: every name, document number, form and period in the request,
   in the index and then live in the folder and mailbox, before asking the user for a file.
1. Open `index.md`. Pick only the entries that match this job's party, topic, source or period;
   open those sections, not the whole files. No index yet: say so and carry on.
2. Apply a matching entry and say which one ("ตามบันทึก D-7"). A matching entry saves a question to
   the user; a missing one means ask, as usual.
3. An entry never outranks the source document, the law, `## Tax rate overrides` in
   `company-facts.md` or what the user says now. On a conflict say so, use the higher source, and
   fix the entry after the user confirms.
4. Starting a period close: read the previous month's section in `periods.md` and compare its
   carried-forward balances with this month's opening balances. A difference is an open item for the
   report, not something to adjust silently.
5. Reuse known sources and formulas: a recurring source in `sources.md` tells which sheet and range
   to read; `formulas.md` gives the expression and its authority. Do not re-derive them.

## Job ledger (after every job, even when nothing went wrong)
Use the tool `accountant_job` (see `accountant-graph`): one call numbers the job, writes the entry below, registers the
documents and adds the links. The manual steps below apply when the tool is not available.
Write one entry in `ledger/<YYYY-MM>.md` when a job finishes, is blocked, or is stopped. Take the
facts from what this job actually did, not from memory:
- **when and what:** date and time, the skill, one line on the job, the client and period;
- **read:** each file (path, sheet, range) and each email (subject, sender organisation or role,
  date) it took figures from, and what each supplied;
- **used:** the formulas and rates (an `F-` id from `formulas.md`, or the expression and where it
  sits in the sheet) and the party/decision/period entries applied;
- **made:** files, sheets, ranges and drafts it produced;
- **checks:** `reconcile-check` result, `auditor` verdict, what the user approved;
- **links:** add the job's edges to `links.tsv` and register each document it read in
  `catalog.tsv` (`accountant-graph`), citing the same ids;
- **problems:** what went wrong or surprised, how it was resolved, and which lesson or memory entry
  was saved because of it (or none).
When the entry is written, say "บันทึกงาน J-<id>" in one line so the user can see it.
A source or formula that is used again goes into `sources.md` or `formulas.md` the second time it
appears, with its id, so the next entry can cite `S-2` or `F-4` instead of repeating it.

## Trace and review (ask the memory, like a graph)
Answer from the files, citing the job id and entry ids; open only the months that can match.
- **Where did this figure or file come from?** Search the ledger for the sheet, range, label or
  email subject. Report the job, its inputs with sheet and range, the email subject, the formula and
  the checks.
- **When was this kind of job done, and how often?** Scan `ledger/` by month for the skill; give the
  last date and the count. `learn-and-improve` uses this for its weekly review.
- **What went wrong before?** Search the ledger's problems lines by skill, party or period; two or
  more of the same problem means a lesson (`learn-and-improve`) or a decision should exist.
- **What depends on this source or formula?** Search the ledger for its id before changing it.

## Record decisions (with the job)
1. Save only what is verified: a source document, a filing receipt, or the user's explicit yes.
   Anything guessed stays out. A one-line reason and the source go with every entry.
2. Write to the matching file using the template, add its line to `index.md`, and tell the user in
   one line what was saved so they can remove it ("บันทึก D-8: ...").
3. One truth per question: if a new entry changes an old one, edit the old entry and mark it
   `replaced by <id>`; never leave two entries that disagree.
4. When a job closes a period, write that period's section in `periods.md`: status, forms filed
   with dates and reference numbers, balances carried forward, adjustments still open, and the
   backup date (`company-profile` asks for it at every close).
5. The user says an entry is wrong → correct or delete it at once and confirm in one line.

## Never store
Salaries, personal ID numbers, bank account numbers, passwords, or a document's full text and the
body of an email. Refer to the file name, sheet and range instead. An email subject is kept;
strip any figure or personal name from it that is not needed to find the mail. A tax ID of a
vendor stays in the vendor master or the source document; `parties.md` holds the name and the
treatment.

## Keep it small
A memory file stays under about 40 entries; a ledger month grows with the work and is never
rewritten. At month end, if a file is longer, propose to merge duplicates and move closed periods
older than two years to `archive/`. Propose only; the user approves.

## Learn and remember (every job)
- **Before:** read `Accountant/lessons/accountant-memory.md` if it exists. Search first with `accountant-graph`
  (tool `accountant_find` on the names, document numbers, forms and period in the request) and
  look up `Accountant/memory/` with `accountant-memory`.
- **During:** note what you read (file, sheet, range; email subject), each formula or rate you
  use, and every problem as it happens (an entry that conflicted with a source document, a duplicate party).
- **After:** record the job with the tool `accountant_job` (one call writes the ledger entry, the
  catalog lines and the links; if the tool is not available, follow the manual steps in
  `accountant-memory`) and say "บันทึกงาน J-id". If the user corrected the work, a check failed
  and was fixed, or a step here was wrong or missing, save one lesson with the tool
  `accountant_lesson` (rules in `learn-and-improve`). Record verified decisions and party
  treatments. Say in one line what was saved.
