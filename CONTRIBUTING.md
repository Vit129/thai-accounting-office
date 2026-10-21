# Contributing / maintaining the plugin

- Layout: `.claude-plugin/plugin.json`, `skills/*/SKILL.md` (English content, Thai triggers), `agents/`, `hooks/hooks.json`,
  `CONNECTORS.md`, `companies/_template/` (a company-specific rules layer, used when the base is not enough).
- Test the tools: `python3 -m unittest discover -s tests -v` (`build.sh` compiles the scripts and runs the tests itself when Python is available, and fails if they fail).
- Build the plugin: `bash scripts/build.sh` (Windows: `powershell -ExecutionPolicy Bypass -File scripts\build.ps1`)
  produces `dist/thai-accounting-office.plugin` and `.zip`. The build fails if a `description` in a SKILL.md contains `<` or `>`
  (Claude Desktop rejects it), or if the version of `work-folder-CLAUDE.md` does not match the one embedded in `คู่มือการใช้งาน.html`.
- New skill: end the file with the `## Learn and remember (every job)` block, like every other skill.
- Release a new version: promote the lessons used on every job into `SKILL.md`, bump the skill version and the plugin version, then build.
  Users remove the old plugin and upload the new one (data in `Accountant/` is kept).
- Never put client or company data into this repo.
