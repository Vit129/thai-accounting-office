# Graph format

Plain text, tab-separated, UTF-8, one record per line; the first line of each file is the header.
Ids are shared with `accountant-memory`: `P-` party, `D-` decision, `R-` recurring entry, `T-yyyy-mm`
period, `S-` source, `F-` formula, `J-yyyymmdd-n` job, and `K-n` for a document or email.

## catalog.tsv
```
id	kind	where	title	period	parties	numbers	topics	first_seen
```
- `kind`: pdf, email, xlsx, docx, md, csv, image, other
- `where`: a path in the work folder, or for an email `mail: <sender organisation or role>, <date>`
- `title`: the file's own title or the email subject, unchanged so a search finds it
- `parties`: `P-` ids, or the name as written until a party entry exists
- `numbers`: document numbers (tax invoice, voucher, receipt, 50 tawi certificate, filing reference)
- `topics`: a few words (WHT, VAT, bank statement, payroll file, audit confirmation)
- `first_seen`: the job id or date it was first read
One line per document; a re-read updates the line. Never: bodies, amounts, salaries, personal ID
numbers, bank account numbers.

## links.tsv
```
from	relation	to	via
```
| relation | from -> to |
|---|---|
| `reads` | job -> document, source or period |
| `makes` | job -> file, sheet and range, or draft |
| `uses` | job -> formula |
| `applies` | job -> party, decision, recurring entry |
| `mentions` | document -> party, number, form |
| `for` | document or job -> period |
| `carries-to` | period -> next period (balances) |
| `supersedes` | entry -> older entry |
| `alias-of` | name -> party |
`via` is the job id (or date) that established the edge. Write edges when the job's ledger entry is
written; never edit a line, add a `supersedes` line instead.

## aka: in parties.md
```
- aka: <Thai name>; <English name>; <short form>; <old name>
```
Matching drops บริษัท, บจก., จำกัด, Co., Ltd., Company, Limited, ignores case, spaces and dots.

## Recipes (open only what can match)
- Find a party: grep the name in `parties.md` (aka), then its id in `links.tsv`, then each `K-` in `catalog.tsv`.
- Find a document by number: grep the number in `catalog.tsv`, then its `K-` in `links.tsv` for the jobs that read it.
- Trace a figure: ledger entry (`accountant-memory`) -> its `reads` edges -> `catalog.tsv` -> if the document is a period
  balance, follow `carries-to` backwards.
- Impact of a formula: grep `F-n` in `links.tsv` (jobs), then those jobs' months in `ledger/`.
- Path: expand both ends one hop at a time (neighbors) until a node appears on both sides; stop at four hops.

## The job record (what `accountant_job` takes)
```json
{"skill": "payment-prep", "summary": "monthly vouchers", "client": "-", "period": "2026-10", "status": "done",
 "read": [{"kind": "xlsx", "where": "Payments/2026-10.xlsx", "title": "Payments Oct", "sheet": "Sheet1", "range": "A2:F80",
           "supplied": "vendor lines", "parties": ["P-3"], "numbers": ["INV-2026-0042"]},
          {"kind": "email", "sender": "cloud vendor (organisation)", "subject": "Invoice October", "supplied": "amount due"},
          "S-2: bank movements"],
 "used": ["F-3", "P-3", {"formula": "base x rate, 2 decimals", "where": "Sheet1!H2:H80"}],
 "made": ["Vouchers/PV-2026-10.xlsx!A1:H24"],
 "checks": "reconcile-check pass; auditor pass; approved by the approver on 2026-10-31",
 "problems": [{"problem": "bank file uses Buddhist years", "resolution": "converted", "saved": "lessons/payment-prep.md"}],
 "decisions": ["D-7"], "carries_to": "2026-11"}
```
One call numbers the job (`J-yyyymmdd-n`), writes the ledger entry, registers each document in `catalog.tsv`
(reusing the line when the same file or mail is read again), and adds the links. `status` is done, blocked
or partial. Anything with a 13-digit number is refused.

## Command line summary
`init` · `job FILE|-` · `register-doc` · `link` · `party` · `find QUERY [--files DIR]` · `neighbors|trace|impact REF` ·
`path A B` · `usage [--plugin DIR]` · `problems [--skill S] [--party P]` · `check [--strict]` · `map [--party P|--period YYYY-MM]` ·
`index-scan DIR [--month YYYY-MM] [--max N]` · `lesson SKILL TEXT` · `lessons-review` · `promote SKILL --plugin DIR [--yes]`.
`find --files` also reads the text of md, txt, csv, tsv, html, docx and xlsx files; pdf and image files are matched by name
only and listed as needing `doc-reader`.
