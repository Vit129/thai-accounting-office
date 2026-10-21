# Memory format

All files are plain Markdown in the memory folder (see `SKILL.md`). Dates are `YYYY-MM-DD`.
`<…>` below is a placeholder to fill in. Copy these templates when the folder is first created.

## index.md
```markdown
# Memory index
One line per entry: `- [<id>] <topic> -> <file> (<status>, <date>)`. Status: active or replaced.
```
Entry ids: `P-<n>` party, `D-<n>` decision, `R-<n>` recurring entry, `T-<YYYY-MM>` period,
`S-<n>` source, `F-<n>` formula. Job ids in the ledger: `J-<YYYYMMDD>-<n>`.
Example line: `- [P-3] Cloud hosting vendor, withholding -> parties.md (active, 2026-03-02)`

## parties.md
```markdown
# Parties
## P-<n> <party name>
- role: vendor | customer | payee group
- aka: <Thai name>; <English name>; <short form>
- treatment: <WHT type and rate, VAT yes/no, usual account>
- basis: <source document, Revenue Code section, or "user decision">
- confirmed: <date> by <who>
- replaced by: <id, only if replaced>
```

## decisions.md
```markdown
# Decisions
## D-<n> <topic>
- situation: <what came up>
- decision: <what was decided>
- basis: <source document, section, auditor or ruling>
- approved: <date> by <who>
- applies to: all periods | <period> | until <event>
- revisit when: <condition, or "never">
- replaced by: <id, only if replaced>
```

## recurring.md
```markdown
# Recurring entries
## R-<n> <entry name>
- schedule: monthly | quarterly | yearly (day <d>)
- usual amount: <low>–<high> THB
- accounts: <debit> / <credit>
- source: <where the document arrives>
- last seen: <period>
```
An amount outside the usual range, or a missing entry in its period, goes into the report as a
question, not into the books silently.

## periods.md
```markdown
# Periods
## T-<YYYY-MM>
- status: open | closed <date> approved by <who>
- filed: <form> on <date>, ref <number>   (one line per form)
- carried forward: AR <amount>; AP <amount>; inventory <amount>; VAT credit <amount>; WHT payable <amount>
- open adjustments: <list, or none>
- backup noted: <date>, <where>
```
Next month's close compares its opening balances with `carried forward`.

## sources.md
```markdown
# Sources
## S-<n> <name of the source>
- kind: file | email | portal export
- where: <path, sheet, range>  or  <sender organisation or role, subject pattern, folder it is saved to>
- holds: <what figures or documents it supplies>
- cadence: monthly | quarterly | yearly | on request
- quirks: <thing that went wrong before: merged cells, Buddhist-era dates, late arrival, ...>
- last used: <job id>
```

## formulas.md
```markdown
# Formulas and rates
## F-<n> <name>
- expression: <for example: withholding = base x rate, rounded to 2 decimals>  or the spreadsheet formula text
- parameters: <rate, base, rounding, source cell or range>
- authority: <Revenue Code section, ruling, auditor, or "company convention">
- used by: <skills and where it sits in the sheet>
- verified: <date> by <check or person>
- replaced by: <id, only if replaced>
```

## ledger/<YYYY-MM>.md
One file per month, entries appended in time order and never rewritten.
```markdown
# Ledger <YYYY-MM>
## J-<YYYYMMDD>-<n> <HH:MM> <skill> - <one-line job>
- client / period: <client or company> / <period>
- status: done | blocked | partial
- read: <S-id or file path, sheet, range> -> <what it supplied>; email "<subject>" from <organisation or role>, <date> -> <what it supplied>
- used: <F-ids or formula text, where in the sheet>; <P-/D-/R-/T- ids applied>
- made: <file, sheet, range, draft>
- checks: reconcile-check <pass/fail, difference>; auditor <verdict>; approved by <who> on <date>
- problems: <what went wrong> -> <how resolved> (saved: <lesson file / memory id / none>)
```
A job that read nothing new still gets an entry with `read: -`. Subjects and file names are kept
as they are so a search finds them; bodies, salaries, personal ID numbers and account numbers never go in.
