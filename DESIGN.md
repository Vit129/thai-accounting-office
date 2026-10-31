# Design

## Interaction model

This is a conversational Claude plugin rather than a graphical application. Its user-facing design is expressed through skill instructions, confirmation points, review steps, and generated documents. A visual layout specification does not apply.

## Interaction principles

- Ask for confirmation before consequential actions.
- Keep source documents and company records in the user's work folder.
- Present prepared work for professional review before filing or sending.
- Distinguish extracted facts, calculations, assumptions, and unresolved questions.
- Keep the plugin package independent from company-specific data.

## Preview

`make preview` builds the installable package under `dist/`. To review runtime behavior, install that artifact into a separate test client and use synthetic data.
