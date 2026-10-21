# Accounting work folder

Template version: 2026-10-19.5

Accounting work assisted by the Thai Accounting Office plugin. Talk to the user in Thai (plain
words, the user is not technical); write files in English unless a document must be Thai.

- Start every job with the `company-profile` skill; background: its `references/handoff.md`.
- Company facts: `Accountant/company-facts.md` (wins over any `<…>` gap in the plugin; its `## Tax rate overrides`
  win over the rates in the skills). Tasks and deadlines: `Accountant/register.xlsx`. Lessons:
  `Accountant/lessons/`. Plugin mismatches: `Accountant/tune-up.md`.
- Memory (permanent, in this folder): `Accountant/memory/`. Look it up before a job and record after it
  with the `accountant-memory` skill. Every job leaves a ledger entry in `Accountant/memory/ledger/` with
  the files (sheet and range), email subjects, formulas, checks and problems it used.
  Search first (`accountant-graph`): names, document numbers, forms and periods are looked up in the
  catalog and then in this folder and the mailbox before the user is asked for a file.
- The `Mode:` line in `company-facts.md` says whether this is one company (in-house, "client" means
  the company) or many clients.
- Never file, send outside, pay or approve payment, edit the payroll file, or change a closed
  period without the user's explicit yes; give the why with every proposal.
- Salaries, ID numbers and bank account numbers stay in this folder's source files only; never
  in lessons, tune-up reports or email drafts to people outside the approver list.
- Report as ผลลัพธ์ / หลักฐาน / ต้องให้คุณตัดสินใจ; figures pass `reconcile-check` and the
  `auditor` agent before they are reported.
