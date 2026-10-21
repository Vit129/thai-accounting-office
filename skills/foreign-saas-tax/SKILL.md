---
name: foreign-saas-tax
description: >
  This skill should be used for cross-border tax compliance on cloud infrastructure and foreign SaaS
  invoices (AWS, GCP, OpenAI, GitHub, Figma, Slack) — managing Form ภ.พ.36 reverse-charge VAT and
  Form ภ.ง.ด.54 foreign withholding tax under Double Tax Agreements (DTA) — when the user says
  "ภาษี cloud", "ภาษี SaaS", "จ่าย AWS", "ยื่น ภ.พ.36", "ยื่น ภ.ง.ด.54", "หัก ณ ที่จ่ายต่างประเทศ",
  "foreign tax", "OpenAI bill", "GitHub bill", or "Google Cloud bill".
metadata:
  version: "0.1.3"
  last_improved: "2026-10-16"
---

# Foreign SaaS & Cloud Tax Compliance: ภ.พ.36 & ภ.ง.ด.54

Read `Accountant/lessons/foreign-saas-tax.md` first if it exists. Consult `thai-accountant`
(`skills/thai-accountant/references/tax-accounting.md`, `skills/thai-accountant/references/compliance.md`) for Double Tax Agreement (DTA) clauses.

A company that buys cloud and SaaS from foreign vendors pays recurring subscriptions (AWS, Google Cloud,
OpenAI, GitHub, Figma, Slack, Jira) via corporate credit card or international wire transfer. Under the
Thai Revenue Code, cross-border payments for digital services and software licenses trigger statutory
reverse-charge VAT and foreign withholding tax obligations.

---

## 1. Statutory Deadlines & Forms

| Return | Description | Paper Due | e-Filing Due | Legal Basis |
|---|---|---|---|---|
| **ภ.พ.36** | นำส่งภาษีมูลค่าเพิ่ม 7% แทนผู้ให้บริการในต่างประเทศ | 7th of next month | 15th of next month | Section 83/6 (1), Thai Revenue Code |
| **ภ.ง.ด.54** | หักภาษี ณ ที่จ่ายสำหรับเงินได้ที่จ่ายไปต่างประเทศ | 7th of next month | 15th of next month | Section 70, Thai Revenue Code & DTAs |

---

## 2. Form ภ.พ.36 (Reverse-Charge VAT 7%) vs VAT e-Service

Under Section 83/6 (1), when a Thai entity pays a service fee to a foreign provider who performed services
abroad but utilized in Thailand (or performed digital services), the Thai payer must remit **7% VAT**.

### Crucial Inspection: Did the Vendor Already Charge Thai VAT? (กฎหมาย VAT e-Service)
Many major foreign tech platforms (AWS, Google, Microsoft, Meta, etc.) are registered under the Thai VAT e-Service law:
- **Case A: Vendor Invoice has NO Thai VAT (B2B Reverse Charge):**
  - If the company registered its corporate Tax ID (VAT ID) in the vendor's billing profile, the foreign vendor will **NOT charge 7% Thai VAT** on the invoice.
  - **Action:** The company **MUST file Form ภ.พ.36** to self-remit 7% VAT to the Revenue Department by the 7th (or 15th e-Filing) of the following month.
  - **Input Tax Recovery:** The official Revenue Department receipt (ใบเสร็จรับเงิน ภ.พ.36) serves as a valid tax invoice. The company can claim this 7% amount as **Input VAT (ภาษีซื้อ)** in Form ภ.พ.30 in the tax month the receipt is issued.
- **Case B: Vendor Invoice ALREADY CHARGED 7% Thai VAT (B2C / e-Service):**
  - If the account lacks a verified corporate Tax ID, the platform automatically charges 7% Thai VAT and remits it directly to the Thai Revenue Department.
  - **Action:** **DO NOT file Form ภ.พ.36** (filing it would result in paying double VAT).
  - **Limitation:** Under the VAT e-Service law, VAT charged directly on foreign e-Service invoices **cannot be claimed as input tax credit (ภาษีซื้อต้องห้าม)**; it must be booked entirely as an expense.
  - **Remedy:** Update company profile in the vendor billing console immediately with the company's 13-digit Tax ID and Head Office branch code so future invoices fall under Case A.

---

## 3. Form ภ.ง.ด.54 (Cross-Border Withholding Tax & DTA)

Under Section 70, payments of Section 40 (2)-(6) income to foreign companies not operating in Thailand
are subject to Thai WHT (normally 15%), **unless reduced or exempted by an active Double Tax Agreement (DTA)**.

### Classification of Common Tech Expenses:

> **Rates are defaults, not law.** Before using any rate below, check `Accountant/company-facts.md` →
> `## Tax rate overrides`. If the user (or their tax advisor) has entered a rate there, use it and
> cite their source. If the user gives a different rate in chat, ask "บันทึกเป็นอัตราของบริษัทไหม",
> then add it there as `- <item>: <rate> (source: <ruling / advisor / date>)`. Treaty and decree
> rates change; when unsure, show the default with its source and let the user confirm.

1. **Cloud Computing Infrastructure & Server Rental (AWS EC2/S3, GCP, DigitalOcean):**
   - **Unsettled — do not default to 0%.** Revenue Department rulings have treated payments for
     using foreign systems (e.g. internet service from the US) as royalties under Section 40(3),
     and practitioners treat SaaS such as Google Workspace as 40(3) subject to ภ.ง.ด.54. Other
     rulings found some services were not royalties; it depends on what is actually bought.
   - Ask the user which treatment the company (or its tax advisor) uses, record it in the overrides,
     and only then compute. If treated as Business Profits (Article 7, vendor has no PE) → 0%.
   - Keep the vendor invoice and the Certificate of Tax Residence (TRC) to claim a treaty rate.
2. **Software Licenses & API Royalty (OpenAI API, GitHub, Figma, Adobe, JetBrains):**
   - Evaluated based on whether payment is for "Right to Use" (Royalty - Article 12) or standard shrink-wrap software.
   - If classified as Royalty (ค่าสิทธิ์):
     - No treaty / no TRC: 15% (Section 70).
     - US-Thailand DTA (Art. 12): 5% literary, artistic or scientific copyright (an RD ruling
       applied 5% to software right-to-use, rd.go.th/37040.html); 8% industrial, commercial or
       scientific equipment; 15% other (patents, trademarks, know-how).
     - Singapore-Thailand DTA (2015, in force from 1 Jan 2017): 5% copyright, 8% equipment, 10% other.
     - Ireland-Thailand DTA (2013): sources disagree (5/10/15 vs 10%) — read Art. 12 before use.
     - Treaty text: rd.go.th/fileadmin/user_upload/porpor/double-tax-agreements/
   - Note: If payment is made by corporate card without withholding, the gross payment represents
     the net amount. The company may need to absorb the tax (grossing-up).
3. **Advertising Platforms (Google Ads, Meta/Facebook):**
   - Typically treated as Business Profits under Article 7 (0% WHT if no PE in Thailand).

---

## 4. Monthly Execution Steps

1. **Collect Foreign Invoices & Card Statements**:
   - Match monthly invoice PDF from vendor console with corporate credit card statement in THB.
2. **Verify Currency Conversion Rate**:
   - Check THB converted amount against Bank of Thailand (BOT) weighted average selling rate or actual card billing rate.
3. **Compute ภ.พ.36**:
   - Calculate 7% VAT for every foreign digital invoice.
4. **Determine ภ.ง.ด.54 Position**:
   - Tag each invoice by category (Cloud compute = exempt; Software license/API = evaluate DTA rate).
   - Document the applicable DTA article and country of origin.
5. **Reconcile**:
   - Cross-check against GL accounts: `Bank/Credit Card`, `Cloud Infrastructure Expense`, `Software Subscription`.
6. **Prepare Filing Drafts**:
   - Draft `Filing-PP36` and `Filing-PND54` sheets in workbook.
7. **Stop-and-Ask**:
   - Present tax summary and recommended remittance amounts to the accountant for executive approval.

---

## 5. Output

A Thai executive summary:
- Table of foreign invoices processed (Vendor, Country, USD/EUR amount, THB amount, ภ.พ.36 VAT 7%, ภ.ง.ด.54 WHT).
- Input VAT credit recovery schedule for next month's ภ.พ.30.
- Draft filing sheet links with calculation formulas.

## Learn and remember (every job)
- **Before:** read `Accountant/lessons/foreign-saas-tax.md` if it exists. Search first with `accountant-graph`
  (tool `accountant_find` on the names, document numbers, forms and period in the request) and
  look up `Accountant/memory/` with `accountant-memory`.
- **During:** note what you read (file, sheet, range; email subject), each formula or rate you
  use, and every problem as it happens.
- **After:** record the job with the tool `accountant_job` (one call writes the ledger entry, the
  catalog lines and the links; if the tool is not available, follow the manual steps in
  `accountant-memory`) and say "บันทึกงาน J-id". If the user corrected the work, a check failed
  and was fixed, or a step here was wrong or missing, save one lesson with the tool
  `accountant_lesson` (rules in `learn-and-improve`). Record verified decisions and party
  treatments. Say in one line what was saved.
