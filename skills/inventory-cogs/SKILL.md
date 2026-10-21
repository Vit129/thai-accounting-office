---
name: inventory-cogs
description: >
  This skill should be used for inventory accounting, Cost of Goods Sold (COGS) calculation, stock
  counts, lower of cost or net realizable value (LCNRV), and VAT inventory reports under Section
  87 (3) of the Thai Revenue Code — when the user says "สินค้าคงเหลือ", "คำนวณต้นทุนขาย", "ตรวจนับสต็อก",
  "รายงานสินค้าและวัตถุดิบ", "สต็อกขาดเกิน", "inventory", "stock count", "COGS", or "stock card".
metadata:
  version: "0.1.2"
---

# Inventory & Cost of Goods Sold (สินค้าคงเหลือและต้นทุนขาย)

Read `Accountant/lessons/inventory-cogs.md` first if it exists. Consult `thai-accountant`
(`skills/thai-accountant/references/cost-accounting.md`, `skills/thai-accountant/references/general-accounting.md`) for costing models.

Under TFRS for NPAEs (Chapter 7) and the Thai Revenue Code (Sections 65 Bis and 87 (3)), trading
and manufacturing entities must maintain accurate inventory records, valuation, and statutory
inventory reports.

---

## 1. Inventory Valuation & Cost Flow Methods

### Approved Methods under TFRS & Thai Tax Law
1. **FIFO (First-In, First-Out: เข้าก่อนออกก่อน)**:
   - Assumes earliest goods purchased are sold first.
   - Ending inventory is valued at most recent purchase prices.
2. **Weighted Average (ถัวเฉลี่ยถ่วงน้ำหนัก)**:
   - Moving average (Perpetual) or monthly weighted average (Periodic).
   - Average cost per unit = Total Cost of Goods Available for Sale / Total Units Available.
3. **LIFO Prohibited**: LIFO is strictly forbidden under TFRS and Thai tax regulations. Once a
   valuation method is chosen, it cannot be changed without prior approval from the Director-General
   of the Revenue Department.

---

## 2. Accounting Systems (Perpetual vs Periodic)

| Attribute | Perpetual Inventory System | Periodic Inventory System |
|---|---|---|
| Recording sales | Dr. COGS / Cr. Inventory continuously | No COGS entry recorded at time of sale |
| Purchases | Dr. Inventory directly | Dr. Purchases account |
| Period-end COGS | Real-time GL balance | `Beginning Inventory + Net Purchases - Ending Inventory = COGS` |
| Best suited for | Barcode/POS systems, high-value or low-volume goods | Traditional retail, high-volume low-value goods |

---

## 3. Lower of Cost or Net Realizable Value (LCNRV)

At each financial year-end, inventory must be valued at the **lower of cost or Net Realizable Value (NRV)**:
- **NRV** = Estimated selling price in the ordinary course of business minus estimated completion costs and necessary selling expenses.
- If NRV is below cost (e.g. damaged, slow-moving, or obsolete stock):
  - Accounting Entry: `Dr. Loss on Inventory Devaluation (หมวด 5) / Cr. Allowance for Inventory Devaluation (บัญชีปรับมูลค่าในหมวด 1)`
- **Tax Difference**: For tax calculation under Section 65 Ter, inventory devaluation provisions
  are non-deductible until actual destruction or disposal is completed in compliance with Revenue
  Department Notification on Rules for Destruction of Bad Stock (requires advance written notification
  to Revenue Department auditor or certified public accountant observation).

---

## 4. Statutory VAT Inventory Report (รายงานสินค้าและวัตถุดิบ ม.87(3))

For VAT-registered businesses buying/selling physical goods:
- Must maintain a **รายงานสินค้าและวัตถุดิบ** per warehouse location.
- Must record quantity received, issued, and on-hand within **3 days** from transaction date.
- Discrepancies between physical count and inventory report:
  - **Stock Missing (สินค้าขาดจากรายงาน):** Deemed as sale under Revenue Code Section 77/1 (8) (e).
    The company must output 7% VAT based on market value and issue a tax invoice to itself.
  - **Stock Overage (สินค้าเกินรายงาน):** Investigate cause (unrecorded purchase or sales return).
    If unexplainable, book as other income.

---

## 5. Physical Stock Count & Reconciliation Steps

1. **Conduct Physical Stock Count**:
   - Organize year-end count sheet with bin locations, item codes, and count teams.
2. **Reconciliation**:
   - Compare physical count against Stock Card and GL inventory balance.
   - Categorize variances: Normal shrinkage within tolerance vs unexplained losses.
3. **Calculate COGS & Adjustment Entry**:
   - For Periodic: Take physical count valued at FIFO/Average, record closing inventory entry.
   - For Perpetual: Record inventory adjustment for physical variances.
4. **Reconcile with reconcile-check**:
   - Ensure GL inventory agrees with sub-ledger stock cards.
5. **Auditor Review**: Submit stock count sheets and reconciliation report to `auditor` agent.

---

## 6. Output

Thai summary report:
- Inventory valuation summary (Item group, Quantity on hand, Unit cost, Total cost).
- COGS calculation schedule for the period.
- Physical count variance report (Deficit / Surplus with VAT implications).
- Link to statutory Section 87 (3) inventory report sheet.

## Learn and remember (every job)
- **Before:** read `Accountant/lessons/inventory-cogs.md` if it exists. Search first with `accountant-graph`
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
