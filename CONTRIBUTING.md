# Contributing / maintaining the plugin

- Layout: `.claude-plugin/plugin.json`, `skills/*/SKILL.md` (English content, Thai triggers), `agents/`, `hooks/hooks.json`,
  `CONNECTORS.md`, `companies/_template/` (a company-specific rules layer, used when the base is not enough).
- Test the tools: `make test` (`python3 -m unittest discover -s tests -v`).
- Build the plugin: `bash scripts/build.sh` (Windows: `powershell -ExecutionPolicy Bypass -File scripts\build.ps1`)
  produces `dist/thai-accounting-office.plugin` and `.zip`. The build fails if a `description` in a SKILL.md contains `<` or `>`
  (Claude Desktop rejects it), or if the version of `work-folder-CLAUDE.md` does not match the one embedded in `คู่มือการใช้งาน.html`.
- New skill: end the file with the `## Learn and remember (every job)` block, like every other skill.
- Release a new version: promote the lessons used on every job into `SKILL.md`, bump the skill version and the plugin version, then build.
  Users remove the old plugin and upload the new one (data in `Accountant/` is kept).
- Before publishing, `make start` runs the unit suite and package build. CI runs the unit command and build script on pull requests and pushes to `main`.
- Preview the installable package with `make preview`; inspect `dist/`. Install it only into a separate test client when reviewing runtime behavior.
- This plugin has no local web server. Its preview is the installable package artifact, followed by manual review in a separate client when needed.
- Never put client or company data into this repo.
