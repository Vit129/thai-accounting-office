"""Tests for the accountant graph engine, the Stop gate and the MCP server (standard library only).

Run: python3 -m unittest discover -s tests -v
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

sys.dont_write_bytecode = True  # a test run must not leave files in skills/
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
SCRIPTS = os.path.join(REPO, "skills", "accountant-graph", "scripts")
sys.path.insert(0, SCRIPTS)
import graph as g  # noqa: E402
import mcp_server  # noqa: E402
import stop_gate  # noqa: E402

TMP_BASE = os.path.join(REPO, ".tmp")


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def parties_aka(ctx):
    return [a for p in g.parties(ctx) for a in p["aka"]]


class Base(unittest.TestCase):
    def setUp(self):
        os.makedirs(TMP_BASE, exist_ok=True)
        self.dir = tempfile.mkdtemp(dir=TMP_BASE)
        self.ctx = g.Ctx(self.dir)
        g.init(self.ctx)

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)
        try:
            os.rmdir(TMP_BASE)
        except OSError:
            pass

    def job(self, **kw):
        spec = {"skill": "payment-prep", "summary": "monthly vouchers", "period": "2026-10", "when": "2026-10-31T16:40:00",
                "read": [{"kind": "xlsx", "where": "Payments/2026-10.xlsx", "title": "Payments Oct", "sheet": "Sheet1", "range": "A2:F80",
                          "supplied": "vendor lines"}],
                "used": ["F-1", "P-1"], "made": ["Vouchers/PV-2026-10.xlsx!A1:H24"], "checks": "reconcile-check pass"}
        spec.update(kw)
        return g.write_job(self.ctx, spec)

    def seed_party_formula(self):
        pid = g.add_entry(self.ctx, "P", "บริษัท คลาวด์โฮสต์ จำกัด", {"role": "vendor"}, ["CloudHost Co., Ltd.", "คลาวด์โฮสต์"])
        fid = g.add_entry(self.ctx, "F", "withholding", {"expression": "base x rate", "authority": "Revenue Code s.50"})
        return pid, fid


class TestInitAndFind(Base):
    def test_init_creates_files(self):
        for fn in ("index.md", "parties.md", "catalog.tsv", "links.tsv", "sources.md", "formulas.md"):
            self.assertTrue(os.path.exists(self.ctx.p(fn)), fn)
        self.assertNotIn("created", g.init(self.ctx))  # idempotent: a second init creates nothing

    def test_party_found_by_any_spelling(self):
        pid, _ = self.seed_party_formula()
        self.assertEqual(pid, "P-1")
        for q in ("CloudHost", "คลาวด์โฮสต์", "บจก. คลาวด์โฮสต์", "cloudhost co ltd", "CLOUDHOST"):
            ids = [h["id"] for h in g.find(self.ctx, q)]
            self.assertIn("P-1", ids, q)

    def test_norm_drops_company_words(self):
        self.assertEqual(g.norm("บริษัท ก้าวไกล จำกัด"), g.norm("ก้าวไกล"))
        self.assertEqual(g.norm("Acme Co., Ltd."), g.norm("acme"))

    def test_find_document_by_number_and_subject(self):
        g.register_doc(self.ctx, "email", "mail: cloud vendor, 2026-10-29", "ใบแจ้งหนี้ตุลาคม", "2026-10", ["P-1"], ["INV-2026-0042"], ["WHT"])
        self.assertIn("K-1", [h["id"] for h in g.find(self.ctx, "INV-2026-0042")])
        self.assertIn("K-1", [h["id"] for h in g.find(self.ctx, "ใบแจ้งหนี้ตุลาคม")])
        self.assertEqual(g.find(self.ctx, "nothing-like-this-xyz"), [])

    def test_thai_name_finds_english_named_document_and_file(self):
        """The query word is expanded to every spelling and the id of the party it names."""
        self.seed_party_formula()
        docs = os.path.join(self.dir, "Docs")
        os.makedirs(docs)
        g.write_text(os.path.join(docs, "invoice-2569-10.md"), "Invoice from CloudHost Co., Ltd. October INV-9")
        g.index_scan(self.ctx, docs)
        g.register_doc(self.ctx, "email", "mail: CloudHost billing", "October invoice", "2026-10", [], ["INV-9"])
        self.assertIn("K-1", {h["id"] for h in g.find(self.ctx, "คลาวด์โฮสต์")})  # catalogued file linked to P-1 by its name
        hits = g.find(self.ctx, "คลาวด์โฮสต์ October", files_dir=docs)
        ids = {h["id"] for h in hits}
        self.assertIn("K-2", ids)  # mail named CloudHost in English
        self.assertTrue(any(h["type"] == "file" and h["id"].endswith("invoice-2569-10.md") for h in hits))

    def test_aka_keeps_commas_inside_a_name(self):
        self.seed_party_formula()
        self.assertIn("CloudHost Co., Ltd.", parties_aka(self.ctx))

    def test_id_only_read_shows_where(self):
        self.seed_party_formula()
        g.register_doc(self.ctx, "pdf", "Docs/a.pdf", "a")
        self.job(read=[{"id": "K-1", "supplied": "x"}])
        self.assertIn("K-1 (Docs/a.pdf)", g.read_text(self.ctx.p("ledger", "2026-10.md")))

    def test_empty_query_rejected(self):
        with self.assertRaises(g.GraphError):
            g.find(self.ctx, "   ")


class TestJobAndQueries(Base):
    def test_job_ids_and_files(self):
        self.seed_party_formula()
        j1, j2 = self.job(), self.job(summary="second")
        self.assertEqual((j1, j2), ("J-20261031-1", "J-20261031-2"))
        ledger = g.read_text(self.ctx.p("ledger", "2026-10.md"))
        self.assertIn("## J-20261031-1 16:40 payment-prep - monthly vouchers", ledger)
        self.assertIn("Payments/2026-10.xlsx / Sheet1 / A2:F80", ledger)
        self.assertEqual(len(g.catalog(self.ctx)), 1)  # the same document is one line
        rel = {(f, r, t) for f, r, t, v in g.links(self.ctx)}
        self.assertIn((j1, "reads", "K-1"), rel)
        self.assertIn((j1, "uses", "F-1"), rel)
        self.assertIn((j1, "applies", "P-1"), rel)
        self.assertIn((j1, "for", "T-2026-10"), rel)

    def test_trace_impact_path_neighbors(self):
        self.seed_party_formula()
        j = self.job(problems=[{"problem": "bank file uses Buddhist years", "resolution": "converted", "saved": "lessons/payment-prep.md"}])
        tr = g.trace(self.ctx, "Payments/2026-10.xlsx")
        self.assertIn(j, tr)
        self.assertIn("A2:F80", tr)
        self.assertIn("reconcile-check pass", tr)
        im = g.impact(self.ctx, "F-1")
        self.assertIn(j, im)
        self.assertIn("2026-10", im)
        self.assertIn("PV-2026-10.xlsx", im)
        pa = g.path(self.ctx, "F-1", "Payments/2026-10.xlsx")
        self.assertIn("path (2 hops)", pa)
        self.assertIn("reads", g.neighbors(self.ctx, "K-1"))

    def test_period_chain(self):
        self.seed_party_formula()
        self.job(period="2026-09", carries_to="2026-10", when="2026-09-30T10:00:00")
        self.job(period="2026-10")
        tr = g.trace(self.ctx, g.ledger_entries(self.ctx) and "J-20261031-1")
        self.assertIn("T-2026-10 <- T-2026-09", tr)

    def test_usage_and_problems(self):
        self.seed_party_formula()
        for _ in range(2):
            self.job(problems=["bank file uses Buddhist years -> converted"])
        us = g.usage(self.ctx, ["monthly-close"])
        self.assertIn("payment-prep | 2 | 2026-10-31", us)
        self.assertIn("monthly-close | 0 | - | never", us)
        pr = g.problems(self.ctx, skill="payment-prep")
        self.assertIn("repeated (2+)", pr)

    def test_forbidden_13_digit_number(self):
        with self.assertRaises(g.GraphError):
            self.job(summary="vendor tax id 0105536012345")
        with self.assertRaises(g.GraphError):
            g.register_doc(self.ctx, "pdf", "a.pdf", "x 1-2345-67890-12-3")

    def test_bad_status_and_period(self):
        with self.assertRaises(g.GraphError):
            self.job(status="weird")
        with self.assertRaises(g.GraphError):
            self.job(period="Oct 2026")


class TestCheck(Base):
    def test_consistent_after_normal_work(self):
        self.seed_party_formula()
        self.job()
        self.assertEqual(g.check(self.ctx), [])

    def test_findings(self):
        self.seed_party_formula()
        g.add_entry(self.ctx, "P", "CloudHost", {"role": "vendor"})  # same name once words are dropped
        g.register_doc(self.ctx, "pdf", "old/unread.pdf", "unread")
        g.add_link(self.ctx, "J-20260101-1", "reads", "K-99")
        text = "\n".join(g.check(self.ctx))
        self.assertIn("dangling id K-99", text)
        self.assertIn("was never read by a job", text)
        self.assertIn("share a name", text)

    def test_missing_index_line(self):
        self.seed_party_formula()
        idx = g.read_text(self.ctx.p("index.md")).replace("- [F-1]", "- [XX]")
        g.write_text(self.ctx.p("index.md"), idx)
        self.assertIn("missing from index.md", "\n".join(g.check(self.ctx)))


class TestIndexAndFiles(Base):
    def make_docx(self, path, text):
        with zipfile.ZipFile(path, "w") as z:
            z.writestr("word/document.xml", "<w:document><w:t>%s</w:t></w:document>" % text)

    def test_index_scan_and_resume(self):
        g.add_entry(self.ctx, "P", "บริษัท คลาวด์โฮสต์ จำกัด", {"role": "vendor"}, ["CloudHost"])
        docs = os.path.join(self.dir, "Docs")
        os.makedirs(docs)
        g.write_text(os.path.join(docs, "invoice-2569-10.md"), "Invoice from CloudHost Co., Ltd. for October")
        with open(os.path.join(docs, "scan-2026-09.pdf"), "wb") as f:
            f.write(b"%PDF-1.4 binary")
        self.make_docx(os.path.join(docs, "contract.docx"), "agreement with CloudHost")
        msg = g.index_scan(self.ctx, docs)
        self.assertIn("indexed 3 new", msg)
        self.assertIn("1 need a reader", msg)
        rows = {r[3]: r for r in g.catalog(self.ctx)}
        self.assertEqual(rows["invoice-2569-10"][4], "2026-10")  # Buddhist year converted
        self.assertIn("P-1", rows["invoice-2569-10"][5])
        self.assertIn("needs-read", rows["scan-2026-09"][7])
        self.assertIn("P-1", rows["contract"][5])
        self.assertIn("0 new", g.index_scan(self.ctx, docs).replace("indexed 0 new file(s)", "0 new"))
        self.assertEqual(len(g.catalog(self.ctx)), 3)

    def test_live_file_search(self):
        docs = os.path.join(self.dir, "Docs")
        os.makedirs(docs)
        g.write_text(os.path.join(docs, "note.md"), "ค่าบริการคลาวด์ ประจำเดือน INV-77")
        self.make_docx(os.path.join(docs, "memo.docx"), "withholding certificate INV-77 for hosting")
        with open(os.path.join(docs, "INV-77-scan.pdf"), "wb") as f:
            f.write(b"%PDF")
        hits = g.find(self.ctx, "INV-77", files_dir=docs)
        kinds = {(h["id"].replace("\\", "/"), h["where"]) for h in hits if h["type"] == "file"}
        self.assertIn(("Docs/note.md", "content"), kinds)
        text = " ".join(h["id"] for h in hits)
        self.assertIn("memo.docx", text)
        self.assertTrue(any("name only" == h["where"] for h in hits), hits)  # pdf matched by name, content not read


class TestMap(Base):
    def test_map_written_and_capped(self):
        self.seed_party_formula()
        self.job()
        out = g.build_map(self.ctx, period="2026-10")
        html = g.read_text(self.ctx.p("map.html"))
        self.assertIn("J-20261031-1", html)
        self.assertIn("around T-2026-10", out)
        for i in range(30):
            g.add_link(self.ctx, "J-X%d" % i, "reads", "K-%d" % i)
        self.assertIn("first 10 links only", g.build_map(self.ctx, cap=10))


class TestLessons(Base):
    def test_save_dedupe_guard_limit(self):
        self.assertIn("lesson saved", g.lesson(self.ctx, "payment-prep", "Check the buyer's branch number before claiming input VAT"))
        self.assertIn("already saved", g.lesson(self.ctx, "payment-prep", "check the buyer's branch number before claiming input VAT"))
        with self.assertRaises(g.GraphError):
            g.lesson(self.ctx, "payment-prep", "ask jane@example.com first")
        with self.assertRaises(g.GraphError):
            g.lesson(self.ctx, "payment-prep", "vendor id 0105536012345 is special")
        for i in range(g.LESSON_MAX - 1):
            g.lesson(self.ctx, "payment-prep", "distinct rule number %d" % i)
        with self.assertRaises(g.GraphError):
            g.lesson(self.ctx, "payment-prep", "one more rule")
        self.assertIn("at the limit", g.lessons_review(self.ctx))

    def test_promote_dry_run_and_apply(self):
        plugin = os.path.join(self.dir, "plugin")
        sk = os.path.join(plugin, "skills", "payment-prep")
        os.makedirs(sk)
        g.write_text(os.path.join(sk, "SKILL.md"), "---\nname: payment-prep\nmetadata:\n  version: \"0.1.2\"\n---\n# x\n\n## Learn and remember (every job)\n- before\n")
        g.lesson(self.ctx, "payment-prep", "Round WHT to 2 decimals")
        dry = g.promote(self.ctx, "payment-prep", plugin)
        self.assertIn("dry run", dry)
        self.assertNotIn("Learned rules", g.read_text(os.path.join(sk, "SKILL.md")))
        g.promote(self.ctx, "payment-prep", plugin, yes=True)
        text = g.read_text(os.path.join(sk, "SKILL.md"))
        self.assertIn("## Learned rules", text)
        self.assertIn("- Round WHT to 2 decimals", text)
        self.assertLess(text.index("## Learned rules"), text.index("## Learn and remember"))
        self.assertIn('version: "0.1.3"', text)
        self.assertEqual(g.lessons_review(self.ctx).split(":")[1].split()[0], "0")
        self.assertTrue(os.listdir(os.path.join(self.ctx.lessons, "_promoted")))


class TestStopGate(Base):
    def lines(self, assistant_text, extra=""):
        return [json.dumps({"type": "user", "message": {"role": "user", "content": "close the month"}}),
                json.dumps({"type": "assistant", "message": {"role": "assistant", "content": [{"type": "text", "text": assistant_text + extra}]}})]

    REPORT = "ผลลัพธ์: done\nหลักฐาน: reconciled\nต้องให้คุณตัดสินใจ: none"

    def test_blocks_report_without_ledger(self):
        self.assertIsNotNone(stop_gate.decide({"cwd": self.dir}, self.lines(self.REPORT)))

    def test_allows_when_ledger_written(self):
        self.assertIsNone(stop_gate.decide({"cwd": self.dir}, self.lines(self.REPORT, "\nบันทึกงาน J-20261031-1")))
        self.assertIsNone(stop_gate.decide({"cwd": self.dir}, self.lines(self.REPORT, " accountant_job")))

    def test_allows_other_cases(self):
        self.assertIsNone(stop_gate.decide({"cwd": self.dir, "stop_hook_active": True}, self.lines(self.REPORT)))
        self.assertIsNone(stop_gate.decide({"cwd": self.dir}, self.lines("just an answer")))
        outside = tempfile.mkdtemp(dir=TMP_BASE)
        try:
            self.assertIsNone(stop_gate.decide({"cwd": outside}, self.lines(self.REPORT)))
        finally:
            shutil.rmtree(outside, ignore_errors=True)

    def test_only_last_turn_counts(self):
        old = self.lines(self.REPORT, "\nบันทึกงาน J-20261001-1")
        new = [json.dumps({"type": "user", "message": {"role": "user", "content": "another job"}}),
               json.dumps({"type": "assistant", "message": {"role": "assistant", "content": [{"type": "text", "text": self.REPORT}]}})]
        self.assertIsNotNone(stop_gate.decide({"cwd": self.dir}, old + new))

    def test_fail_open_on_garbage(self):
        out = subprocess.run([sys.executable, "-B", os.path.join(SCRIPTS, "stop_gate.py")], input="not json", capture_output=True, text=True)
        self.assertEqual((out.returncode, out.stdout), (0, ""))


class TestMcp(Base):
    def rpc(self, method, params=None, mid=1):
        return mcp_server.handle({"jsonrpc": "2.0", "id": mid, "method": method, "params": params or {}})

    def test_initialize_and_list(self):
        self.assertEqual(self.rpc("initialize", {"protocolVersion": "2025-03-26"})["result"]["protocolVersion"], "2025-03-26")
        names = {t["name"] for t in self.rpc("tools/list")["result"]["tools"]}
        for n in ("accountant_find", "accountant_job", "accountant_trace", "accountant_impact", "accountant_check", "accountant_lesson", "accountant_map"):
            self.assertIn(n, names)
        self.assertIsNone(mcp_server.handle({"jsonrpc": "2.0", "method": "notifications/initialized"}))
        self.assertEqual(self.rpc("nope")["error"]["code"], -32601)

    def test_call_job_then_find_and_errors(self):
        spec = {"skill": "payment-prep", "summary": "vouchers", "period": "2026-10", "when": "2026-10-31T10:00:00",
                "read": [{"kind": "email", "sender": "mail: cloud vendor", "subject": "Invoice October", "supplied": "amounts"}]}
        r = self.rpc("tools/call", {"name": "accountant_job", "arguments": {"root": self.dir, "job": spec}})["result"]
        self.assertFalse(r["isError"])
        self.assertIn("บันทึกงาน J-20261031-1", r["content"][0]["text"])
        r = self.rpc("tools/call", {"name": "accountant_find", "arguments": {"root": self.dir, "query": "Invoice October"}})["result"]
        self.assertIn("K-1", r["content"][0]["text"])
        r = self.rpc("tools/call", {"name": "accountant_find", "arguments": {"root": self.dir}})["result"]
        self.assertTrue(r["isError"])
        r = self.rpc("tools/call", {"name": "accountant_job", "arguments": {"root": self.dir, "job": dict(spec, summary="tax id 0105536012345")}})["result"]
        self.assertTrue(r["isError"])

    def test_stdio_roundtrip(self):
        msgs = [{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
                {"jsonrpc": "2.0", "method": "notifications/initialized"},
                {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}]
        out = subprocess.run([sys.executable, "-B", os.path.join(SCRIPTS, "mcp_server.py")], input="\n".join(json.dumps(m) for m in msgs) + "\n",
                             capture_output=True, text=True, timeout=20)
        lines = [json.loads(l) for l in out.stdout.splitlines()]
        self.assertEqual([m["id"] for m in lines], [1, 2])


class TestCli(Base):
    def run_cli(self, *args, stdin=None):
        return subprocess.run([sys.executable, "-B", os.path.join(SCRIPTS, "graph.py"), "--root", self.dir] + list(args),
                              input=stdin, capture_output=True, text=True, timeout=30)

    def test_cli_job_find_check(self):
        spec = {"skill": "monthly-close", "summary": "close", "period": "2026-10", "when": "2026-10-31T10:00:00",
                "read": [{"kind": "csv", "where": "Bank/oct.csv", "title": "bank oct", "supplied": "movements"}]}
        r = self.run_cli("job", "-", stdin=json.dumps(spec))
        self.assertEqual((r.returncode, r.stdout.strip()), (0, "บันทึกงาน J-20261031-1"))
        self.assertIn("K-1", self.run_cli("find", "bank", "oct").stdout)
        self.assertEqual(self.run_cli("check").stdout.strip(), "memory is consistent")
        bad = self.run_cli("lesson", "payment-prep", "email me at a@b.co")
        self.assertEqual(bad.returncode, 2)
        self.assertIn("e-mail", bad.stderr)
        self.assertIn("map written", self.run_cli("map", "--period", "2026-10").stdout)


class TestPlugin(unittest.TestCase):
    """The plugin files agree with the engine: tools named in skills exist, the hook and server paths resolve."""

    def md_files(self):
        for base, dirs, files in os.walk(os.path.join(REPO, "skills")):
            dirs[:] = [d for d in dirs if d != "scripts"]
            for fn in files:
                if fn.endswith(".md"):
                    yield os.path.join(base, fn)

    def test_every_skill_has_the_block_and_calls_the_tools(self):
        skills = os.path.join(REPO, "skills")
        names = sorted(d for d in os.listdir(skills) if os.path.isdir(os.path.join(skills, d)))
        self.assertGreaterEqual(len(names), 22)
        for n in names:
            text = read(os.path.join(skills, n, "SKILL.md"))
            self.assertIn("## Learn and remember (every job)", text, n)
            self.assertIn("accountant_job", text, n)
            self.assertIn("accountant_lesson", text, n)
            self.assertIn("name: %s\n" % n, text, n)

    def test_tools_named_in_docs_exist(self):
        import re
        tools = {t["name"] for t in mcp_server.TOOLS}
        for path in list(self.md_files()) + [os.path.join(REPO, "README.md")]:
            for name in re.findall(r"\baccountant_[a-z_]+\b", read(path)):
                self.assertIn(name, tools, "%s names a tool that does not exist: %s" % (os.path.relpath(path, REPO), name))

    def test_every_tool_is_documented_in_the_graph_skill(self):
        text = read(os.path.join(REPO, "skills", "accountant-graph", "SKILL.md"))
        for t in mcp_server.TOOLS:
            self.assertIn(t["name"], text, t["name"])

    def test_job_progress_file_is_named_the_same_everywhere(self):
        # chief writes it, memory documents it, dashboard reads it: one name, one status marker
        for skill in ("accountant-chief", "accountant-memory", "accountant-dashboard"):
            text = read(os.path.join(REPO, "skills", skill, "SKILL.md"))
            self.assertIn("-progress.md", text, skill)
            self.assertIn("Status: open", text, skill)

    def test_hook_and_server_paths_resolve(self):
        hooks = json.loads(read(os.path.join(REPO, "hooks", "hooks.json")))
        cmds = [h for e in hooks["hooks"]["Stop"] for h in e["hooks"]]
        self.assertTrue(any(h["type"] == "prompt" for h in cmds))
        prompt = [h for h in cmds if h["type"] == "prompt"][0]["prompt"]
        # the plugin is installed globally: outside accounting work the prompt must approve first
        self.assertLess(prompt.index("Accountant/"), prompt.index("block ONLY"))
        command = [h for h in cmds if h["type"] == "command"][0]["command"]
        self.assertIn("stop_gate.py", command)
        self.assertIn("python3 -B", command)
        mcp = json.loads(read(os.path.join(REPO, ".mcp.json")))
        args = mcp["mcpServers"]["accountant-graph"]["args"]
        self.assertIn("-B", args)
        self.assertTrue(os.path.exists(args[-1].replace("${CLAUDE_PLUGIN_ROOT}", REPO)))
        self.assertTrue(os.path.exists(os.path.join(SCRIPTS, "stop_gate.py")))


if __name__ == "__main__":
    unittest.main()
