# Company layer

Copy `_template` to `companies/<company-slug>/` for each company that uses the plugin.

- `company-profile/SKILL.md` — replaces the generic base `skills/company-profile` (state check, setup questions); keep its Step 0 and Setup if you replace it (replace every `<…>`).
- `overrides/` — mirrors the plugin root. Any file here replaces the base file of the same path
  when building, e.g. `overrides/skills/monthly-close/SKILL.md`, `overrides/hooks/hooks.json`,
  `overrides/agents/auditor.md`. Add a new skill by adding `overrides/skills/<name>/SKILL.md`.

Build: `bash scripts/build.sh <company-slug>` (Mac/Linux) or `powershell -ExecutionPolicy Bypass -File scripts\build.ps1 <company-slug>` (Windows) → `dist/thai-accounting-office-<company-slug>.plugin`.
Keep base fixes in the base folders; keep office-specific choices here.
