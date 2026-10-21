---
name: financial-statements
description: >
  This skill should be used to draft statutory financial statements under TFRS for NPAEs and DBD
  Form SorBorChor 3, compile notes to financial statements, and coordinate corporate secretarial
  compliance (AGM, BorJor 5, DBD e-Filing) — when the user says "จัดทำงบการเงิน", "ออกงบการเงิน",
  "งบแสดงฐานะการเงิน", "งบกำไรขาดทุน", "หมายเหตุประกอบงบ", "ส.บช.3", "DBD e-Filing", "บอจ.5",
  "ประชุมผู้ถือหุ้น", "AGM", "financial statements", "balance sheet", or "notes disclosure".
metadata:
  version: "0.1.2"
---

# Statutory Financial Statements & DBD Compliance (การจัดทำงบการเงินและ DBD e-Filing)

Read `Accountant/lessons/financial-statements.md` first if it exists. Consult `thai-accountant`
(`skills/thai-accountant/references/reporting-disclosure.md`, `skills/thai-accountant/references/compliance.md`) for TFRS for NPAEs disclosure rules.

Every registered company in Thailand must prepare annual financial statements audited by a certified
public accountant (CPA or TA) and submit them to the Department of Business Development (DBD).

---

## 1. Statutory Corporate Calendar (รอบปีสิ้นสุด 31 ธันวาคม)

| ลำดับ | ขั้นตอน | กำหนดเวลาทางกฎหมาย | กฎหมายที่เกี่ยวข้อง |
|---|---|---|---|
| 1 | ปิดบัญชีและให้ผู้สอบบัญชีตรวจสอบ | ม.ค. - เม.ย. | พ.ร.บ.การบัญชี พ.ศ. 2543 |
| 2 | ส่งหนังสือนัดประชุมผู้ถือหุ้น (AGM) | ล่วงหน้าไม่น้อยกว่า 7 วัน (หรือ 14 วันหากมีมติพิเศษ) | ประมวลกฎหมายแพ่งและพาณิชย์ |
| 3 | จัดประชุมสามัญผู้ถือหุ้น (AGM) รับรองงบ | ภายใน 4 เดือนนับแต่วันสิ้นรอบบัญชี (ภายใน 30 เม.ย.) | ป.พ.พ. มาตรา 1197 |
| 4 | ยื่นบัญชีรายชื่อผู้ถือหุ้น (บอจ.5) | ภายใน 14 วันนับแต่วันประชุม AGM | ป.พ.พ. มาตรา 1139 |
| 5 | ยื่น ภ.ง.ด.50 ต่อกรมสรรพากร | ภายใน 150 วันนับแต่วันสิ้นรอบบัญชี (ปลายเดือน พ.ค.) | ประมวลรัษฎากร มาตรา 69 |
| 6 | นำส่งงบการเงินทาง DBD e-Filing | ภายใน 1 เดือนนับแต่วันประชุม AGM (ไม่เกิน 31 พ.ค.) | พ.ร.บ.การบัญชี พ.ศ. 2543 มาตรา 11 |

---

## 2. Structure of Financial Statements (แบบ ส.บช.3)

Draft the 4 core components according to DBD Notification B.E. 2554:

### A. Statement of Financial Position (งบแสดงฐานะการเงิน)
- **Current Assets (สินทรัพย์หมุนเวียน):** Cash and cash equivalents, temporary investments,
  trade and other receivables, short-term loans to related parties, inventories, other current assets.
- **Non-Current Assets (สินทรัพย์ไม่หมุนเวียน):** Long-term investments, property plant and
  equipment (net of accumulated depreciation), intangible assets, other non-current assets.
- **Current Liabilities (หนี้สินหมุนเวียน):** Bank overdrafts and short-term borrowings, trade and
  other payables, current portion of long-term debts, short-term loans from related parties,
  accrued corporate income tax, other current liabilities.
- **Non-Current Liabilities (หนี้สินไม่หมุนเวียน):** Long-term borrowings, provisions for employee benefits.
- **Shareholders' Equity (ส่วนของเจ้าของ):** Authorized share capital, issued and fully paid-up capital,
  retained earnings (appropriated legal reserve, unappropriated), total equity.
- **Balance Equation:** Total Assets = Total Liabilities + Total Shareholders' Equity.

### B. Statement of Income (งบกำไรขาดทุน)
- **Revenues:** Revenue from sales or services, other income.
- **Expenses:** Cost of sales or services, distribution costs, administrative expenses.
- **Profit / Loss before Finance Costs and Tax**.
- **Finance Costs** (Interest expense).
- **Profit / Loss before Income Tax**.
- **Income Tax Expense**.
- **Net Profit / Loss for the Year**.

### C. Statement of Changes in Equity (งบแสดงการเปลี่ยนแปลงส่วนของเจ้าของ)
- Beginning balance of share capital and retained earnings.
- Net profit/loss for the year.
- Dividends paid (approved by AGM/EGM).
- Appropriation to statutory legal reserve (minimum 5% of annual net profit until reaching 10%
  of registered capital under Section 1202 of the Civil and Commercial Code).
- Ending balance.

### D. Notes to Financial Statements (หมายเหตุประกอบงบการเงิน)
Must include:
1. General information (incorporation date, registered address, principal activities, employee count).
2. Basis of preparation (TFRS for NPAEs compliance statement).
3. Summary of significant accounting policies (revenue recognition, depreciation method, inventory valuation).
4. Supplementary notes: Cash breakdown, trade receivables ageing, inventory breakdown, property plant
   and equipment movement schedule, related party transactions, commitments and contingent liabilities.

---

## 3. Preparation & Filing Package

1. **Trial Balance Linking**: Link every line item in Form ส.บช.3 to the audited post-closing Trial Balance.
2. **Prior Year Comparison**: Ensure prior year comparative figures match the previous year's audited statements.
3. **Legal Reserve Check**: Check whether 5% of net profit was transferred to the legal reserve if profit exists.
4. **Prepare Corporate Secretarial Bundle**:
   - Notice of AGM and AGM Minutes draft approving financial statements and auditor appointment.
   - Form บอจ.5 draft reflecting current shareholding structure.
   - Form ส.บช.3 and financial statement upload package formatted for DBD e-Filing (Excel/XBRL).
5. **Auditor Review**: Send draft to `auditor` agent for verification.
6. **Stop-and-Ask**: Present complete package to the user; wait for CPA audit report signature
   and board approval before anything is submitted.

---

## 4. Output

A Thai reporting package:
- Draft Statement of Financial Position and Income Statement.
- Notes to Financial Statements draft.
- AGM & บอจ.5 filing schedule checklist with deadline countdown.
- DBD e-Filing preparation sheet link.

## Learn and remember (every job)
- **Before:** read `Accountant/lessons/financial-statements.md` if it exists. Search first with `accountant-graph`
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
