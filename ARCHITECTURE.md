# Architecture

## Package layout

- `.claude-plugin/` declares the plugin and marketplace metadata.
- `skills/` contains task workflows and references.
- `agents/` defines review roles.
- `hooks/` supplies lifecycle checks and state handling.
- `scripts/` validates, builds, and packages the plugin.
- `tests/` covers Python tools and repository constraints.
- `companies/_template/` contains a sanitized company-specific starting point.

## Build and checks

`make test` runs `python3 -m unittest discover -s tests -v`. `make build` runs `bash scripts/build.sh`, which compiles graph scripts, runs tests, validates package content, and writes `.plugin` and `.zip` artifacts under ignored `dist/`. `make start` runs test then build. Pull request CI runs the tests and build script.

## Data boundary

Accounting records and customer-specific lessons belong in the user's work folder. The repository contains generic plugin content and a sanitized template only.
