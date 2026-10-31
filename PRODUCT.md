# Product

Thai Accounting Office is an installable Claude plugin for accounting-office workflows. It supports document intake, bookkeeping preparation, reconciliation, period close, tax work, and review while keeping company records in the user's work folder.

## Users and interface

The users are accounting professionals using Claude Desktop or Claude Code. The product interface is the plugin's skills, agents, hooks, and Markdown handouts. It is not a standalone web application and has no local development server.

## Safety boundaries

The plugin prepares and checks work. It does not submit tax or statutory filings, send messages, make payments, or change a closed accounting period without user confirmation. Company data must not be committed to this repository.

## Delivery

`make test` runs the unit suite. `make build` packages the plugin. `make start` runs both in order, and `make preview` creates the installable artifact for review under `dist/`.
