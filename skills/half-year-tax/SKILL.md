---
name: half-year-tax
description: >
  This skill should be used for interim corporate income tax (ภ.ง.ด.51) preparation, net profit
  forecasting, and the 25 percent underestimation penalty risk assessment under Revenue Code
  Sections 67 Bis and 67 Ter — when the user says "ภาษีครึ่งปี", "ทำ ภ.ง.ด.51", "ประมาณการกำไรสุทธิ",
  "ยื่น ภงด51", "half-year tax", "interim corporate tax", "PND51", or "เช็คความเสี่ยง 25%".
metadata:
  version: "0.1.2"
---

# Half-Year Corporate Income Tax: ภ.ง.ด.51 (ภาษีเงินได้นิติบุคคลครึ่งปี)

Read `Accountant/lessons/half-year-tax.md` first if it exists. Consult `thai-accountant`
(`skills/thai-accountant/references/tax-accounting.md`, `skills/thai-accountant/references/compliance.md`) for tax calculations.

Under Thai Revenue Code Section 67 Bis, companies must estimate their full-year net profit
at the end of the first 6 months and pay half-year corporate income tax.

---

## 1. Deadlines & Statutory Basis

| Return | Paper Filing | e-Filing | Legal Basis |
|---|---|---|---|
| ภ.ง.ด.51 (Half-year CIT) | Within 2 months from the end of the first 6 months (August 31 for calendar year) | +8 days (approx September 8) | Section 67 Bis, Thai Revenue Code |

*Note: If the deadline falls on a weekend or public holiday, it moves to the next business day.*

---

## 2. Estimation Methods

For Thai private companies and SMEs, tax is based on **estimated full-year net profit**:
1. Compute actual accounting results for the first 6 months (January - June).
2. Project operating income and expenses for the remaining 6 months (July - December) based on
   sales pipelines, signed contracts, seasonality, and confirmed overheads.
3. Apply tax adjustments to project full-year taxable net profit:
   - Add back non-deductible expenses (Section 65 Ter).
   - Deduct tax-exempt income or extra tax allowances (Section 65 Bis).
   - Adjust for tax depreciation differences (Royal Decree No. 145).
4. **Estimated Taxable Net Profit / 2 = Tax Base for ภ.ง.ด.51**.

---

## 3. The 25% Underestimation Penalty (มาตรา 67 ตรี)

Under Section 67 Ter, if the estimated full-year net profit falls short of the actual full-year
net profit by **more than 25% without justifiable reason**, the company is subject to a
**20% surcharge (เงินเพิ่ม 20%)** on the underpaid tax amount.

### Formula for Shortfall Percentage:
`Shortfall % = ((Actual Full-Year Taxable Net Profit - Estimated Full-Year Net Profit) / Actual Full-Year Taxable Net Profit) × 100`

### The "Safe Harbor" Justifiable Reason (คำสั่งกรมสรรพากร ที่ ป.50/2537 แก้ไขเพิ่มเติมโดย ป.152/2558)
Even if the shortfall exceeds 25%, the Revenue Department considers the estimation to have "justifiable reason" (exempt from the 20% penalty) under either of the following criteria:
1. **Criterion 1 (Tax Liability Test - เกณฑ์จำนวนภาษี):**
   The company filed Form ภ.ง.ด.51 with corporate income tax payable of **not less than half (≥ 50%) of the total corporate income tax liability filed in Form ภ.ง.ด.50 of the preceding accounting period**.
2. **Criterion 2 (Net Profit Test for Tax-Exempt/Reduced-Rate Entities - เกณฑ์กำไรสุทธิ):**
   In cases where the half-year tax payable is less than half of the previous year's tax due to tax rate reductions or statutory tax exemptions, the company estimated full-year net profit of **not less than the actual taxable net profit filed in Form ภ.ง.ด.50 of the preceding accounting period**.

---

## 4. Tax Rate Computation

Compute tax using applicable rates:
- **General Company Rate:** 20% flat.
- **Qualifying SME Rate** (Paid-up capital on last day of accounting period not exceeding 5M THB
  AND total annual revenue not exceeding 30M THB):
  - 0 to 300,000 THB: Exempt (0%)
  - 300,001 to 3,000,000 THB: 15%
  - Above 3,000,000 THB: 20%
- **Tax Credits Deducted:**
  - Withholding tax (WHT) deducted from company revenues received during the first 6 months
    (documented by Form 50 Tawi certificates).
  - Tax paid abroad (if eligible under Double Tax Agreements).

---

## 5. Execution Steps

1. **Close 6-Month Books**: Run `monthly-close` and `reconcile-check` through June 30.
2. **Collect 6-Month WHT Certificates**: Verify total 50 Tawi tax credits received.
3. **Forecast Second Half**:
   - Run Conservative (Base case), Aggressive, and Previous-Year Safe Harbor scenarios.
4. **Run 25% Threshold Test**:
   - Compare projection against Safe Harbor (ป.50/2537) threshold.
   - If projected profit is below previous year, document concrete commercial reasons (e.g. loss of major customer, macro slowdown, planned capital expansion).
5. **Prepare Form ภ.ง.ด.51 Draft**:
   - Fill in Part 1 (Estimated net profit), Part 2 (Tax computation), and Part 3 (Tax credits).
6. **Auditor Check**: Hand over to `auditor` agent.
7. **Stop-and-Ask**: Present the 3 scenarios, the recommended tax amount, and the filing draft
   to the user for final sign-off.

---

## 6. Output

Thai summary report:
- 6-month actual figures vs full-year projected taxable net profit.
- Scenario comparison table (Profit, Tax, WHT Credits, Net Tax Payable).
- Risk assessment of Section 67 Ter (Underestimation penalty analysis).
- Draft filing sheet link with all formulas exposed.

## Learn and remember (every job)
- **Before:** read `Accountant/lessons/half-year-tax.md` if it exists. Search first with `accountant-graph`
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
