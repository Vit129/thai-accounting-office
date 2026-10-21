---
name: payment-prep
description: >
  This skill should be used to prepare Payment Vouchers (PV), calculate domestic withholding tax
  deductions (1%, 3%, 5%), generate Form 50 Tawi certificates, and format bank transfer summaries
  for online corporate banking — when the user says "ทำใบสำคัญจ่าย", "เตรียมจ่ายเงิน", "จ่ายเงินคู่ค้า",
  "ทำ PV", "payment voucher", "เตรียมโอนเงิน", "หัก 3%", or "ออก 50 ทวิ".
metadata:
  version: "0.1.3"
  last_improved: "2026-10-16"
---

# Payment Voucher & Bank Transfer Preparation

Read `Accountant/lessons/payment-prep.md` first if it exists. Consult `thai-accountant`
(`skills/thai-accountant/references/tax-accounting.md`, `skills/thai-accountant/references/general-accounting.md`) for WHT rates and journal entries.

The accountant (following the payment policy in `company-profile` when one is installed) prepares vendor payments,
voucher packages, and withholding certificates. **Crucial Rule: Claude prepares the figures; releasing
money is strictly the executive's action. Never enter or store banking passwords anywhere.**

---

## 1. 3-Way Matching & Document Verification

Before generating a Payment Voucher (PV), verify that three elements match:
1. **Vendor Invoice / Tax Invoice / Receipt**: Seller Tax ID, address, items billed, and bank details.
2. **Purchase Order (PO) / Agreement / SOW**: Approved budget, agreed unit rates, payment milestones.
3. **Proof of Delivery / Acceptance**: Signed acceptance sheet, Dev team confirmation, or Jira ticket sign-off.

---

## 2. Domestic Withholding Tax (WHT) Rates (มาตรา 3 เตรส)

When paying Thai registered entities or individuals, deduct statutory WHT:

| Payment Nature | Standard Rate | Conditions & Forms |
|---|---|---|
| **Service fees, software dev, consulting, repair** | **3%** | Most common for IT contractors and agencies (ภ.ง.ด.3 / ภ.ง.ด.53) |
| **Transportation & freight** | **1%** | Registered transport companies (non-public transport) |
| **Advertising fees** | **2%** | Media agencies, PR placements |
| **Office & asset rental** | **5%** | Lease of real estate, server co-location space |
| **Purchase of hardware / finished goods** | **0%** | No WHT on pure goods purchase (only VAT 7% applies) |
| **Prizes / Performance rewards** | **5%** | Competition awards, promotional incentives |

*Note: Payments below 1,000 THB are exempt from withholding tax, unless part of an ongoing contract exceeding 1,000 THB.*

---

## 3. Calculation & Payment Voucher (PV) Structure

### Calculation Formula:
- **Net Purchase Amount** = Gross Service Amount (before VAT)
- **VAT 7%** = Net Purchase Amount × 7%
- **WHT Amount** = Net Purchase Amount × Applicable WHT Rate (e.g. 3%)
- **Net Bank Transfer Payable** = Net Purchase Amount + VAT 7% − WHT Amount

Example: service 100,000 + VAT 7,000 − WHT 3% 3,000 = **104,000** to transfer.

Rates in section 2 are defaults: a rate in `Accountant/company-facts.md` → `## Tax rate overrides` wins.

### Journal Entry (บันทึกบัญชีใบสำคัญจ่าย):
- `Dr. Expense / Software Dev Asset (ต้นทุนหรือค่าใช้จ่าย)`
- `Dr. Input VAT (ภาษีซื้อ - if valid tax invoice)`
- `Cr. WHT Payable (ภาษีหัก ณ ที่จ่ายค้างจ่าย - ภ.ง.ด.3 หรือ 53)`
- `Cr. Accounts Payable / Cash at Bank (เจ้าหนี้การค้า หรือ ธนาคาร)`

---

## 4. Withholding Tax Certificate (หนังสือรับรอง 50 ทวิ)

Prepare the statutory Form 50 Tawi (หนังสือรับรองการหักภาษี ณ ที่จ่าย ตามมาตรา 50 ทวิ แห่งประมวลรัษฎากร):
- **ฉบับที่ 1**: "สำหรับผู้ถูกหักภาษี ณ ที่จ่าย ใช้แนบพร้อมกับแบบแสดงรายการภาษี"
- **ฉบับที่ 2**: "สำหรับผู้ถูกหักภาษี ณ ที่จ่าย เก็บไว้เป็นหลักฐาน"
- **สำเนา**: ผู้มีหน้าที่หักภาษี ณ ที่จ่าย (the company) เก็บไว้เป็นหลักฐานประกอบใบสำคัญจ่าย (PV)
- Ensure Payer (the company) and Payee tax IDs, addresses, payment date, and income classification (Section 40 (1), (2), (7), or (8)) are accurately populated.

---

## 5. Online Banking Payment Schedule

Compile verified transactions into a clean schedule ready for online corporate banking
(e.g. SCB Business Anywhere, K-Corporate):

| PV No. | Payee Name | Bank Code | Account No. | Net Transfer (THB) | WHT 50 Tawi No. | Invoice Reference |
|---|---|---|---|---|---|---|
| PV-202610-001 | บริษัท ไอที ซิสเต็มส์ จำกัด | 014 (SCB) | 123-4-56789-0 | 104,000.00 | WT-202610-001 | INV-8891 |

---

## 6. Execution Steps & Stop-and-Ask

1. **Verify Documents**: Check vendor invoice math and bank details.
2. **Compute Net & WHT**: Calculate VAT, WHT, and net payable.
3. **Generate PV & 50 Tawi**: Fill voucher details in `Accountant/vouchers/` sheet.
4. **Prepare Banking Table**: Create the bank transfer list.
5. **Auditor Check**: Hand over package to `auditor` agent.
6. **Stop-and-Ask**: Present payment summary table and net amounts to the user for executive
   authorization and banking OTP approval. Never attempt to automate banking transfers.

---

## 7. Output

A concise Thai payment briefing:
- Summary table of payments due (Payee, Gross, VAT, WHT, Net payable).
- Links to draft Payment Voucher (PV) and 50 Tawi certificate sheets.
- Banking copy-paste table ready for corporate online banking entry.

## Learn and remember (every job)
- **Before:** read `Accountant/lessons/payment-prep.md` if it exists. Search first with `accountant-graph`
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
