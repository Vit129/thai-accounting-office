---
name: budget-tracking
description: >
  This skill should be used to track monthly financial performance against annual budget forecasts,
  perform expense variance analysis (flagging deviations over 10 percent), and project cash burn
  runway — when the user says "ติดตามงบประมาณ", "งบประมาณเทียบจ่ายจริง", "budget vs actual",
  "financial forecast", "วิเคราะห์ variance", "คุม budget", or "วิเคราะห์ runway".
metadata:
  version: "0.1.3"
---

# Budget Tracking & Financial Forecasts

Read `Accountant/lessons/budget-tracking.md` first if it exists. Consult `thai-accountant`
(`skills/thai-accountant/references/financial-planning.md`, `skills/thai-accountant/references/financial-analysis.md`) for financial modeling methods.

The accountant monitors monthly actuals against the annual board-approved operating budget, analyzes
variances, and maintains cash runway visibility.

---

## 1. Operating Budget Cost Categories (defaults for a tech company; replace with the company's own categories in `company-profile`)

| Budget Category | Key Cost Drivers | Typical Variance Triggers |
|---|---|---|
| **1. Personnel & Engineering** | Developer salaries, QA, DevOps, outsourced contractors, employer SSO | Unplanned hiring, contractor overtime, salary adjustments |
| **2. Cloud & SaaS Infrastructure** | AWS, Google Cloud, OpenAI API usage, GitHub, Jira, Figma | Traffic spikes, model token usage, new staging environments |
| **3. Workplace & Office Facilities** | Office lease, co-working, high-speed fiber internet, electricity | Utility price shifts, facility repairs |
| **4. Professional & Legal Fees** | Outsourced payroll fee, audit fee, legal consultation | Annual audit milestones, contract reviews |
| **5. Marketing & BD** | Google/Meta ads, conferences, client pitches | Campaign timing shifts, event sponsorships |

---

## 2. Monthly Variance Analysis Rules

At each monthly close:
1. Extract GL actual revenues and expenses for the month and Year-To-Date (YTD).
2. Compute Variance:
   - `Variance (THB) = Actual − Budget`
   - `Variance (%) = (Actual − Budget) / Budget × 100`
3. **Threshold for Management Flagging**:
   - Flag any cost center where **Variance > +10% (Over budget)** AND **difference > 20,000 THB**.
   - Flag any revenue stream where **Actual < Budget by > 10% (Shortfall)**.
4. **Variance Classification**:
   - **Timing Difference (ความแตกต่างด้านเวลา)**: Expense incurred earlier/later than planned, but full-year budget remains intact (e.g. annual software renewal paid in one lump sum).
   - **Permanent Difference (ความแตกต่างถาวร)**: Ongoing structural cost increase (e.g. cloud price increase or newly hired engineer).

---

## 3. Rolling 3-Month Cash Flow & Runway Forecast

Estimate forward-looking cash stability:
1. **Closing Cash Balance**: Bank accounts + petty cash.
2. **Projected Cash Inflows (Next 3 Months)**: Signed client project milestones, recurring maintenance contracts.
3. **Projected Cash Outflows (Next 3 Months)**: Committed payroll, recurring cloud subscriptions, office rent, scheduled tax payments (ภ.พ.30, ภ.ง.ด.51, ภ.ง.ด.50).
4. **Net Monthly Burn Rate**: Average monthly cash deficit (if negative).
5. **Cash Runway**: `Closing Cash / Monthly Burn Rate = Months of Operation Remaining`.

---

## 4. Execution Steps

1. **Load Budget Model**: Read `Accountant/budget/annual-budget.xlsx` (baseline target).
2. **Pull Actual Figures**: Take closed trial balance from `monthly-close` and `reconcile-check`.
3. **Generate Budget vs Actual Comparison Sheet**:
   - Columns: Account, Monthly Budget, Monthly Actual, Month Variance (THB & %), YTD Budget, YTD Actual, YTD Variance.
4. **Draft Commentary**: Explain top 3 overruns and top 3 savings.
5. **Calculate Runway**: Update 3-month forecast table.
6. **Auditor Check**: Hand over variance sheet to `auditor` agent.
7. **Present Report**: Deliver structured Thai summary for management review.

---

## 5. Output

A clean Thai executive dashboard:
- Variance summary table highlighting flagged items (red if over budget > 10%).
- Top variance drivers with concrete root causes.
- 3-month rolling cash runway outlook.
- Link to the detailed `Budget-vs-Actual-<period>` comparison sheet.

## Learn and remember (every job)
- **Before:** read `Accountant/lessons/budget-tracking.md` if it exists. Search first with `accountant-graph`
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
