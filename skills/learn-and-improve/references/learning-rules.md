# Learning rules

How this office's skills stay useful: they learn from corrections and from the job ledger.

1. **Verified only.** Save a lesson only after the corrected way worked: the check passed, the
   user confirmed, or the authority's document says so.
2. **General, not this client.** Replace names, tax IDs and amounts with placeholders
   (`<client>`, `<amount>`). A lesson must never contain client data.
3. **Fix, don't stack.** If an existing lesson caused the mistake, rewrite or delete it; never
   leave two lessons that disagree.
4. **One place.** The lesson goes into the lessons file of the skill that governed the step —
   not a general notes file.
5. **Bounded.** Keep each lessons file under ~40 lines; merge similar lessons.
6. **Say it.** Every saved lesson is announced in one line so the user can undo it.
7. **A problem that repeats becomes a lesson.** The same problem in two ledger entries needs a
   lesson (this file) or a decision (`accountant-memory`); do not leave it as a note.
8. **The user decides changes to the plugin itself.** The weekly review proposes; nothing in the
   plugin is changed without approval.

## Promote (monthly)
Lessons that apply in every job are folded into the skill text in the next plugin version:
export the lessons folder, ask Claude (in Claude Code or Desktop) to update the matching
`SKILL.md` files, bump the plugin version, reinstall, then clear the promoted lessons.

## New skill (from the weekly review)
When `Accountant/lessons/_unowned.md` shows the same kind of job 3+ times with no skill for it, draft
`Accountant/proposals/new-skill-<slug>.md`: a name, a description with Thai trigger phrases (no `<`
or `>`), when to use it, the steps that worked, the checks, and the evidence (dates, how many
times). No client data. The user approves; at the next build it goes into `skills/` (generic) or
`companies/<slug>/overrides/` (company-specific), and its lessons move out of `_unowned.md`.
