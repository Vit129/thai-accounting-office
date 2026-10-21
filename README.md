# Thai Accounting Office

Plugin สำหรับ Claude (Claude Desktop / Claude Code) ที่ทำหน้าที่เสมือน "หัวหน้าฝ่ายประสานงาน" ของสำนักงานบัญชี:
**คุณเป็นหัวหน้าที่สั่งงานและตัดสินใจ** Claude อ่านอีเมลและเอกสาร ลงบัญชีใน Excel / Google Sheets
ปิดงวด เตรียมภาษี ตรวจตัวเลขก่อนส่งทุกครั้ง แล้วมารายงาน และมีสามอย่างที่ทำให้มันดีขึ้นเรื่อยๆ:

1. **จำถาวร** ทุกงานที่เสร็จหรือติดปัญหาจะถูกจดลงสมุดบันทึกงาน: ไฟล์ไหน ชีทไหน ช่วงเซลล์ไหน เมลหัวข้ออะไร
   สูตรอะไร ตรวจอะไรผ่านบ้าง เจอปัญหาอะไร ถามย้อนได้ภายหลัง ("ตัวเลขนี้มาจากไหน")
2. **เก่งขึ้นเองทุกงาน** ทุก skill อ่านบทเรียนก่อนทำ และเรียนรู้ทุกครั้งที่คุณแก้หรือตรวจไม่ผ่าน
3. **ข้อมูลอยู่ในโฟลเดอร์ของคุณ** ความจำทั้งหมดอยู่ในโฟลเดอร์งาน (`Accountant/`) ไม่ถูกเขียนลงใน plugin

พิมพ์เป็นภาษาไทยได้เลย (skill เขียนเป็นภาษาอังกฤษ มีคำกระตุ้นภาษาไทย)

## ความสามารถหลัก

- คัดอีเมลตามลูกค้า เก็บไฟล์แนบ ร่างคำตอบ (ไม่ส่งเอง): `inbox-triage`
- อ่านใบกำกับภาษี ใบเสร็จ bank statement 50 ทวิ แล้วลงสมุดงาน: `document-intake`
- เตรียมใบสำคัญจ่าย (ไม่จ่ายเอง): `payment-prep`
- ปิดงวด VAT หัก ณ ที่จ่าย รายการปรับปรุง ค่าเสื่อมราคา สต็อกและต้นทุนขาย: `monthly-close`, `adjusting-entries`, `inventory-cogs`
- ภาษี SaaS/cloud ต่างประเทศ (ภ.พ.36, ภ.ง.ด.54) และตรวจเงินเดือน: `foreign-saas-tax`, `payroll-check`
- ภาษีครึ่งปี (ภ.ง.ด.51) และปิดบัญชีสิ้นปี (ภ.ง.ด.50): `half-year-tax`, `year-end-close`
- งบการเงิน (TFRS for NPAEs, DBD) ชุดเอกสารผู้สอบบัญชี ติดตามงบประมาณ: `financial-statements`, `audit-readiness`, `budget-tracking`
- กระทบยอดงบทดลอง ธนาคาร VAT WHT ทรัพย์สิน และหาสูตร Excel ที่พัง: `reconcile-check`
- ค้นหาและแผนที่งานจาก PDF อีเมล Word Excel CSV ของคุณเอง สืบย้อนตัวเลขถึงต้นทาง: `accountant-graph`, `accountant-memory`
- Dashboard ทุกลูกค้า deadline และเรื่องที่รอคุณตัดสินใจ: `accountant-dashboard`
- ทบทวนประจำสัปดาห์และบทเรียน: `learn-and-improve` ตั้งค่าครั้งแรกและปรับแต่ง: `company-profile`, `company-tune-up`
- `auditor` ผู้ตรวจอิสระตรวจผลเทียบกับคำสั่งก่อนรายงานทุกครั้ง

Claude จะไม่ยื่นภาษี / ประกันสังคม / DBD ส่งอีเมลหรือไฟล์ จ่ายเงิน หรือแก้งวดที่ปิดแล้ว โดยไม่มีการยืนยันจากคุณ
เงินเดือน เลขบัตรประชาชน เลขบัญชีธนาคาร และรหัสผ่าน ไม่ถูกบันทึกลงความจำหรือบทเรียนเด็ดขาด

## การติดตั้ง

### Claude Desktop: ผ่าน marketplace (แนะนำ)

1. เปิด Claude Desktop ไปที่ **Customize → Plugins**
2. ที่ **Personal plugins** กด **+ → Add marketplace → Add from a repository**
3. ใส่ `https://github.com/Vit129/thai-accounting-office` แล้วติดตั้ง `thai-accounting-office` จาก marketplace นี้

องค์กร: Owner ผูก repo นี้เป็น marketplace ขององค์กรได้ แล้ว plugin จะ sync ให้ทุกคน

### Claude Desktop: ไฟล์ zip

1. ดาวน์โหลด `thai-accounting-office.zip` จากหน้า [Release ล่าสุด](https://github.com/Vit129/thai-accounting-office/releases/latest)
2. เปิด Claude Desktop ไปที่ **Customize → Plugins → Add → Upload plugin** แล้วเลือกไฟล์ zip

ใช้ทางใดทางหนึ่งเท่านั้น ถ้าติดตั้งทั้งสองแบบ hook จะรันซ้ำสองครั้ง

### Claude Code (อัปเดตอัตโนมัติ)

```
/plugin marketplace add Vit129/thai-accounting-office
/plugin install thai-accounting-office@thai-accounting-office
```

จากนั้นเปิด auto-update ของ marketplace นี้ในเมนู `/plugin` → Marketplaces ถ้าเคยอัปโหลดไฟล์ zip ไว้ ให้ถอดตัวนั้นออกก่อน ไม่อย่างนั้น hook จะรันซ้ำสองครั้ง

## การอัปเดต

- Claude Desktop (marketplace): กด Check for updates ในหน้า Plugins ถ้ายังค้างเวอร์ชันเก่า ให้ลบ marketplace → ปิดเปิดแอปใหม่ → เพิ่ม marketplace อีกครั้ง (Desktop ยังไม่มี auto-update และบางครั้งไม่ดึงเวอร์ชันใหม่)
- Claude Desktop (zip): ลบ plugin เก่าแล้วอัปโหลด zip ตัวใหม่
- ทุกแบบ: ข้อมูลใน `Accountant/` ไม่หาย
- Claude Code: อัปเดตเองเมื่อเปิด auto-update

## เริ่มต้นครั้งแรก

1. สร้างโฟลเดอร์งานสำหรับเอกสารบัญชี (แนะนำพาธสั้นๆ บน Google Drive หรือ OneDrive)
2. คัดลอก [`skills/company-profile/references/work-folder-CLAUDE.md`](skills/company-profile/references/work-folder-CLAUDE.md) ไปวางในโฟลเดอร์งาน แล้วเปลี่ยนชื่อเป็น `CLAUDE.md` (`CLAUDE.md` ที่ root ของ repo เป็นโน้ตสำหรับคนดูแล plugin ไม่ใช่ไฟล์นี้)
3. เปิดแชทในโฟลเดอร์งาน แล้วพิมพ์ **`เริ่มงาน`** Claude จะถามข้อมูลบริษัทเป็นข้อความเดียว แล้วสร้างโฟลเดอร์ `Accountant/`

## ปรับให้เป็นงานของตัวเอง (ไม่ต้องแก้ plugin)

ห้ามแก้ไฟล์ใน plugin ที่ติดตั้งแล้ว อัปเดตครั้งถัดไปจะเขียนทับ ปรับได้ 2 ทาง:

1. **ในโฟลเดอร์งาน** (ใช้ทางนี้ก่อน): ข้อมูลบริษัทและอัตราภาษีใส่ `Accountant/company-facts.md` (`## Tax rate overrides`) วิธีทำงานที่ต่างจากต้นฉบับใส่ `Accountant/lessons/<skill>.md` ("ที่นี่ทำแบบนี้แทน") กฎส่วนตัวใส่ `CLAUDE.md` ของโฟลเดอร์งาน ทุก skill อ่านไฟล์เหล่านี้ก่อนเริ่มงาน และ skill ต้นฉบับยังได้อัปเดตตามปกติ
2. **Skill ส่วนตัว** (Customize > Skills): สำหรับงานใหม่ที่ plugin ไม่มี หรือเมื่อต้องเปลี่ยนวิธีทำเกือบทั้ง skill ให้คัด `SKILL.md` ต้นฉบับไปแก้ แล้ว
   - ตั้งชื่อใหม่ (เช่น `my-monthly-close`) และแก้ description ให้ต่างจากต้นฉบับ ถ้าชื่อหรือคำสั่งซ้ำ Claude จะเลือกตัวผิด
   - เขียนใน `CLAUDE.md` ของโฟลเดอร์งานว่า "งานปิดงบใช้ `my-monthly-close` แทน `monthly-close`"
   - เก็บบล็อก `## Learn and remember (every job)` ท้ายไฟล์ไว้ ไม่งั้นงานไม่ถูกบันทึกลงสมุดงาน
   - ตัวที่คัดมาไม่อัปเดตตาม plugin ทุกครั้งที่ plugin ออกเวอร์ชันใหม่ ให้เทียบ `version` ของต้นฉบับกับของเรา แล้วตามแก้เอง (เช่น อัตราภาษีหรือกฎใหม่)

งานที่ปรับฝั่งบริษัท (lessons, `CLAUDE.md`, skill ส่วนตัว) อยู่ที่บริษัทเท่านั้น ห้ามส่งกลับเข้า repo นี้เด็ดขาด ถ้าเจอจุดที่ plugin ควรแก้ให้ทุกคน ให้แจ้งผ่าน `tune-up-week-<n>.md` ซึ่งไม่มีข้อมูลบริษัท

## ข้อมูลและความเป็นส่วนตัว

ความจำ บทเรียน สมุดบันทึกงาน และแผนที่เอกสาร เป็นไฟล์ข้อความธรรมดาในโฟลเดอร์งานภายใต้ `Accountant/` เปิดอ่าน แก้ หรือลบเองได้
ไม่มีอะไรถูกเขียนลงใน plugin และห้ามนำข้อมูลลูกค้าใส่ใน repo นี้
ตัวเลขภาษีและกำหนดยื่นใน skill เป็นค่าตั้งต้น ตรวจประกาศกรมสรรพากรปีปัจจุบันก่อนยื่นจริงเสมอ
Claude ช่วยเตรียมงาน ความรับผิดชอบทางวิชาชีพยังเป็นของผู้ทำบัญชีและผู้สอบบัญชี

## เอกสาร

- [docs/user-guide.th.md](docs/user-guide.th.md): คู่มือการใช้งานฉบับเต็ม (ภาษาไทย)
- [CONTRIBUTING.md](CONTRIBUTING.md): การสร้างและดูแล plugin (ภาษาอังกฤษ)
- [CHANGELOG.md](CHANGELOG.md)

## สัญญาอนุญาต

Apache License 2.0 ดู [LICENSE](LICENSE) และ [NOTICE](NOTICE)
