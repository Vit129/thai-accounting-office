---
name: learn-and-improve
description: >
  This skill should be used at the end of every job (accountant-chief calls it), and when the user
  says "จำไว้นะ", "คราวหน้าอย่าทำแบบนี้", "ผิดนะ", "ทบทวนประจำสัปดาห์", "weekly review",
  "skill ไหนไม่ได้ใช้", "remember this", or corrects how work was done. It turns corrections into
  lessons the skills read next time, and runs the weekly curator review.
metadata:
  version: "0.3.3"
---

# Learn and improve (the office gets better every week)

Lessons live as one file per skill: `Accountant/lessons/<skill-name>.md` in the shared work folder.
Every skill in this plugin reads its lessons file before working. Full rules:
`references/learning-rules.md`.

## After every job — learning pass
0. Make sure this job's ledger entry exists (`accountant-memory`); its `problems` line is the first
   place to look for a signal.
1. Look back at this conversation for a signal: the user corrected the approach, the format,
   tone or length; a `reconcile-check` failed and was fixed; a step was missing or wrong; a
   deadline or rule turned out different from the skill.
2. No signal → say "ไม่มีบทเรียนใหม่: <why>" in one line. Do not invent lessons.
3. Signal → write ONE lesson into the lessons file of the skill that governed that step
   (patch an existing lesson if one covers it; rewrite a lesson that turned out wrong).
   No skill governs the step (a new kind of job) → write it to `Accountant/lessons/_unowned.md`:
   `- [<date>] When <situation>, do <rule>. Check: <how to confirm>. (from: <what happened, no client data>)`
4. Tell the user which lesson was saved, so they can remove it.

## Weekly review (curator) — Monday, or when asked
Use the `auditor` agent's report style. Produce proposals only; the user approves each one.
1. List lessons added this week per skill, and the problems lines the ledger (`accountant-memory`)
   recorded this week.
2. Find lessons that repeat or contradict each other → propose a merged version.
3. From the ledger, count the last use and the uses per skill: skills not used for 30+ days and
   lessons files over ~40 lines → propose cleanup. The same problem in two ledger entries with no
   lesson or decision yet → propose one. A formula or source whose authority or layout changed
   (`formulas.md`, `sources.md`) → propose updating it. Duplicate parties and documents no job has
   read, from the `accountant-graph` check → propose merging or removing them.
4. New skill: a kind of job in `_unowned.md` that happened 3+ times → draft
   `Accountant/proposals/new-skill-<slug>.md` (`references/learning-rules.md` → New skill).
5. Lessons that apply every time → propose moving them into the skill itself in the next plugin
   version (`references/learning-rules.md` → Promote).
6. Every proposal states **why** with evidence (how many times it happened, which jobs, dates).
Write the review to `Accountant/reviews/<date>.md` and show it on `accountant-dashboard`.
Use the tools instead of counting by hand: `accountant_usage` (uses and last use per skill),
`accountant_problems` (repeated problems), `accountant_check` (graph integrity) and the command
`graph.py lessons-review` (lessons near the limit, duplicates).

## Improve a skill directly
- **Lesson (immediate):** save it with the tool `accountant_lesson` (skill name and one verified,
  client-free sentence). The engine refuses e-mail addresses and 13-digit numbers, skips a lesson
  that is already saved, and stops at 40 lessons per skill (merge or promote first). Every skill reads
  its lessons file before its next job, so the improvement applies at once.
- **Promote (into the skill text):** after the user approves, in a checkout of the plugin run
  `python3 graph.py --root <work folder> promote <skill> --plugin <plugin folder> --yes`. It adds the
  lessons to the skill's `## Learned rules` section, bumps the patch version and archives the lessons.
  Without `--yes` it only previews. Then rebuild and reinstall the plugin.

## Learn and remember (every job)
- **Before:** read `Accountant/lessons/learn-and-improve.md` if it exists. Search first with `accountant-graph`
  (tool `accountant_find` on the names, document numbers, forms and period in the request) and
  look up `Accountant/memory/` with `accountant-memory`.
- **During:** note what you read (file, sheet, range; email subject), each formula or rate you
  use, and every problem as it happens (a lesson that contradicts another, a proposal the user rejected).
- **After:** record the job with the tool `accountant_job` (one call writes the ledger entry, the
  catalog lines and the links; if the tool is not available, follow the manual steps in
  `accountant-memory`) and say "บันทึกงาน J-id". If the user corrected the work, a check failed
  and was fixed, or a step here was wrong or missing, save one lesson with the tool
  `accountant_lesson` (rules in `learn-and-improve`). Record verified decisions and party
  treatments. Say in one line what was saved.
