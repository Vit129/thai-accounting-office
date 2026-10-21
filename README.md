English | [ภาษาไทย](README.th.md)

# Thai Accounting Office

A plugin for Claude (Claude Desktop / Claude Code) that acts as the "chief of staff" of an accounting office:
**you are the boss who gives orders and makes decisions.** Claude reads email and documents, posts entries in
Excel / Google Sheets, closes periods, prepares taxes, checks every number before it goes out, and then reports back.
Three things make it better over time:

1. **Permanent memory.** Every finished or blocked job is written to a job ledger: which file, sheet and cell range,
   which email subject, which formula, which checks passed, which problems came up. You can ask later "where does this number come from?".
2. **It gets better with every job.** Every skill reads its lessons before it works and learns each time you correct it or a check fails.
3. **Your data stays in your folder.** All memory lives in your work folder (`Accountant/`), never inside the plugin.

You write in Thai. Skills are written in English with Thai trigger phrases.

## Key capabilities

- Inbox triage by client, saving attachments, drafting replies (never sends): `inbox-triage`
- Reading tax invoices, receipts, bank statements and 50 ทวิ, and posting them to the workbook: `document-intake`
- Payment voucher preparation (never pays): `payment-prep`
- Month-end close, VAT and withholding tax, adjusting entries, depreciation, inventory and COGS: `monthly-close`, `adjusting-entries`, `inventory-cogs`
- Foreign SaaS / cloud tax (ภ.พ.36, ภ.ง.ด.54), payroll checks: `foreign-saas-tax`, `payroll-check`
- Half-year tax (ภ.ง.ด.51) and year-end close (ภ.ง.ด.50): `half-year-tax`, `year-end-close`
- Financial statements (TFRS for NPAEs, DBD), audit pack, budget tracking: `financial-statements`, `audit-readiness`, `budget-tracking`
- Reconciliation of trial balance, bank, VAT, WHT, assets, and broken Excel formulas: `reconcile-check`
- Search and map over your own PDFs, emails, Word, Excel and CSV; trace a number to its source: `accountant-graph`, `accountant-memory`
- Dashboard of all clients, deadlines and decisions waiting for you: `accountant-dashboard`
- Weekly review and lessons: `learn-and-improve`; first-time setup and fine-tuning: `company-profile`, `company-tune-up`
- An independent `auditor` agent checks each result against your instruction before it is reported.

Claude never files taxes / social security / DBD, sends email or files, pays money, or edits closed periods
without your explicit confirmation. Salaries, national ID numbers, bank account numbers and passwords are never stored in memory or lessons.

## Install

### Claude Desktop

1. Download `thai-accounting-office.zip` from the [latest release](https://github.com/Vit129/thai-accounting-office/releases/latest).
2. In Claude Desktop go to **Customize → Plugins → Add → Upload plugin** and choose the zip.

### Claude Code (auto-updating)

```
/plugin marketplace add Vit129/thai-accounting-office
/plugin install thai-accounting-office@thai-accounting-office
```

Then turn on auto-update for this marketplace in `/plugin` → Marketplaces. If you previously uploaded the zip, remove that copy first, otherwise the hooks run twice.

## Update

- Claude Desktop: remove the old plugin and upload the new zip. Your data in `Accountant/` is kept.
- Claude Code: automatic when auto-update is on.

## First run

1. Create a work folder for your accounting files (a short path on Google Drive or OneDrive works well).
2. Copy [`skills/company-profile/references/work-folder-CLAUDE.md`](skills/company-profile/references/work-folder-CLAUDE.md) into it and rename the copy to `CLAUDE.md`. (The repo-root `CLAUDE.md` is maintainer notes, not this file.)
3. Open a chat in the work folder and type **`เริ่มงาน`**. Claude asks for the company details in one message and creates the `Accountant/` folder.

## Data & privacy

Memory, lessons, the job ledger and the document map are plain text files in your work folder under `Accountant/`.
You can read, edit or delete them. Nothing is written into the plugin, and no client data belongs in this repository.
Tax rates and deadlines in the skills are defaults: check the current Revenue Department announcements before filing.
Claude prepares the work; professional responsibility stays with the bookkeeper and the auditor.

## Documentation

- [README.th.md](README.th.md): this page in Thai
- [docs/user-guide.th.md](docs/user-guide.th.md): the full user manual (Thai)
- [CONTRIBUTING.md](CONTRIBUTING.md): building and maintaining the plugin
- [CHANGELOG.md](CHANGELOG.md)

## License

Apache License 2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
