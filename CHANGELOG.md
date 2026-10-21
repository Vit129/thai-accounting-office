# Changelog

All notable changes to **thai-accounting-office** are documented here. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and it follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2026-10-21

### Added
- **Complete Thai Accounting Cycle Skills:**
  - `monthly-close`: Monthly closing cycle and tax preparation (PND 1, 3, 53, PP 30).
  - `adjusting-entries`: Accruals, prepayments, depreciation schedules, and asset registers.
  - `inventory-cogs`: Cost of Goods Sold (COGS) calculation and physical inventory reconciliation.
  - `half-year-tax`: Mid-year corporate income tax estimation and PND 51 preparation.
  - `year-end-close`: Year-end closing, CIT calculation (PND 50), and tax net profit reconciliation.
  - `financial-statements`: Financial statements and notes drafting for DBD filing (SorBorChor 3).
  - `audit-readiness`: Audit pack preparation, lead schedules, and balance confirmation requests.
- **Compliance & In-House Skills:**
  - `foreign-saas-tax`: Cross-border SaaS and cloud service tax withholding and remittance (PND 54 & PP 36).
  - `payment-prep`: Payment voucher preparation and Withholding Tax certificates (50 Tawi).
  - `payroll-check`: Payroll verification against social security and withholding tax brackets.
  - `budget-tracking`: Monthly budget vs actual analysis and variance tracking.
- **Core Automation, Memory & Graph:**
  - `accountant-chief`: Main coordinator and client register management.
  - `accountant-dashboard`: Live task and deadline dashboard.
  - `accountant-graph`: Document mapping, relationship graph, and search engine with MCP server support.
  - `accountant-memory`: Persistent ledger of job progress, cell ranges, and formulas.
  - `learn-and-improve`: Continuous learning loop capturing corrections into actionable lessons.
- **Specialized Agents:**
  - `doc-reader`: Rapid batch document processing.
  - `auditor`: Independent verification agent checking numbers and rules before handoff.
- **Licensing & Governance:**
  - Licensed under Apache License 2.0 with explicit attribution in `NOTICE`.
  - Co-developed and contributed by **Vit129** and **Claude** (Anthropic).
