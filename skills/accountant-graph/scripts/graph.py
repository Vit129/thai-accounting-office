#!/usr/bin/env python3
"""Accountant graph: the search, ledger and map engine for an accounting work folder.

Standard library only (Python 3.8+). It reads and writes the plain files under
<work folder>/Accountant/memory/ (TSV and Markdown), so every answer can be checked by
opening the files in Excel or a text editor. The same functions back the command line,
the MCP server (mcp_server.py) and the tests.

    python3 graph.py [--root WORKFOLDER] [--client SLUG] [--json] COMMAND ...

Commands: init, job, register-doc, link, party, find, neighbors, trace, impact, path,
usage, problems, check, map, index-scan, lesson, lessons-review, promote.
"""
import argparse
import datetime as dt
import html
import json
import os
import re
import sys
import unicodedata
import zipfile

VERSION = "1.0.0"

CATALOG_HEADER = ["id", "kind", "where", "title", "period", "parties", "numbers", "topics", "first_seen"]
LINKS_HEADER = ["from", "relation", "to", "via"]
KINDS = ("pdf", "email", "xlsx", "docx", "md", "csv", "image", "other")
MD_FILES = ("parties.md", "decisions.md", "recurring.md", "periods.md", "sources.md", "formulas.md")
MD_TITLES = {
    "parties.md": "Parties", "decisions.md": "Decisions", "recurring.md": "Recurring entries",
    "periods.md": "Periods", "sources.md": "Sources", "formulas.md": "Formulas and rates",
}
COMPANY_WORDS = [
    "ห้างหุ้นส่วนจำกัด", "บริษัท", "บจก.", "บจก", "บมจ.", "บมจ", "หจก.", "หจก", "จำกัด", "(มหาชน)", "มหาชน",
    "co.,ltd.", "co., ltd.", "co.,ltd", "co.", "ltd.", "ltd", "company", "limited", "inc.", "inc",
    "corporation", "corp.", "corp", "public", "plc",
]
BARE_COMPANY = {"co", "ltd", "company", "limited", "inc", "corp", "corporation", "plc", "public", "บริษัท", "จำกัด", "บจก", "บมจ", "หจก", "มหาชน"}
ID_RE = re.compile(r"\b(?:[PDRSF]-\d+|K-\d+|J-\d{8}-\d+|T-\d{4}-\d{2})\b")
THIRTEEN = re.compile(r"(?<!\d)\d(?:[- ]?\d){12}(?!\d)")
TEXT_EXT = {".md": "md", ".txt": "md", ".csv": "csv", ".tsv": "csv", ".html": "other", ".htm": "other", ".json": "other", ".log": "other"}
KIND_EXT = {".pdf": "pdf", ".xlsx": "xlsx", ".xlsm": "xlsx", ".xls": "xlsx", ".docx": "docx", ".doc": "docx",
            ".png": "image", ".jpg": "image", ".jpeg": "image", ".heic": "image", ".tif": "image", ".tiff": "image"}
KIND_EXT.update(TEXT_EXT)


class GraphError(Exception):
    """A problem the user can fix; the message is shown as is."""


# ----------------------------------------------------------------------------- paths
def find_root(start=None):
    """Return the work folder: the nearest directory (from start upward) holding Accountant/."""
    env = os.environ.get("ACCOUNTANT_ROOT")
    if env:
        return os.path.abspath(env)
    cur = os.path.abspath(start or os.getcwd())
    while True:
        if os.path.isdir(os.path.join(cur, "Accountant")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            return os.path.abspath(start or os.getcwd())
        cur = parent


class Ctx:
    """Where one company's (or one client's) files live."""

    def __init__(self, root=None, client=None):
        self.root = os.path.abspath(root) if root else find_root()
        self.client = client
        self.base = os.path.join(self.root, "Accountant")
        self.mem = os.path.join(self.base, "memory", client) if client else os.path.join(self.base, "memory")
        self.lessons = os.path.join(self.base, "lessons")
        self.proposals = os.path.join(self.base, "proposals")

    def p(self, *parts):
        return os.path.join(self.mem, *parts)


# ----------------------------------------------------------------------------- text helpers
_COMPANY_KEYS = sorted({unicodedata.normalize("NFKC", w).casefold() for w in COMPANY_WORDS}, key=len, reverse=True)


def norm(s):
    """Match key for names: width/case folded, company words, spaces and punctuation removed."""
    s = unicodedata.normalize("NFKC", str(s)).casefold()
    for w in _COMPANY_KEYS:
        s = s.replace(w, " ")
    return re.sub(r"[\s.,;:()\[\]{}'\"/\\|_-]+", "", s)


def now():
    return dt.datetime.now()


def check_text(*values):
    """Refuse to store a 13-digit number (a personal ID or tax ID)."""
    for v in values:
        if v and THIRTEEN.search(str(v)):
            raise GraphError("refused: a 13-digit number (ID or tax ID) must not be stored in memory; remove it and refer to the document instead")


def clean(s):
    return re.sub(r"[\t\r\n]+", " ", str(s if s is not None else "")).strip()


def read_text(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""


def write_text(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def append_text(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8", newline="\n") as f:
        f.write(text)


# ----------------------------------------------------------------------------- tsv
def read_tsv(path, header):
    text = read_text(path)
    rows = []
    for i, line in enumerate(text.splitlines()):
        if not line.strip():
            continue
        cells = line.split("\t")
        if i == 0 and cells[0] == header[0]:
            continue
        rows.append(cells + [""] * (len(header) - len(cells)))
    return rows


def ensure_tsv(path, header):
    if not os.path.exists(path):
        write_text(path, "\t".join(header) + "\n")


def append_tsv(path, header, row):
    ensure_tsv(path, header)
    append_text(path, "\t".join(clean(c) for c in row) + "\n")


def rewrite_tsv(path, header, rows):
    write_text(path, "\t".join(header) + "\n" + "".join("\t".join(clean(c) for c in r) + "\n" for r in rows))


# ----------------------------------------------------------------------------- markdown entries
ENTRY_RE = re.compile(r"^## ((?:[PDRSF]-\d+)|(?:T-\d{4}-\d{2}))\b(.*)$", re.M)


def md_entries(ctx):
    """{id: {id, file, title, body}} from the entry files."""
    out = {}
    for fn in MD_FILES:
        text = read_text(ctx.p(fn))
        marks = list(ENTRY_RE.finditer(text))
        for i, m in enumerate(marks):
            end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
            out[m.group(1)] = {"id": m.group(1), "file": fn, "title": m.group(2).strip(), "body": text[m.end():end].strip()}
    return out


LEDGER_RE = re.compile(r"^## (J-\d{8}-\d+) (\d{2}:\d{2}) (\S+) - (.*)$", re.M)


def ledger_entries(ctx):
    out = {}
    d = ctx.p("ledger")
    if not os.path.isdir(d):
        return out
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".md"):
            continue
        text = read_text(os.path.join(d, fn))
        marks = list(LEDGER_RE.finditer(text))
        for i, m in enumerate(marks):
            end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
            body = text[m.end():end].strip()
            out[m.group(1)] = {"id": m.group(1), "file": "ledger/" + fn, "time": m.group(2), "skill": m.group(3),
                               "title": m.group(4).strip(), "body": body,
                               "date": "%s-%s-%s" % (m.group(1)[2:6], m.group(1)[6:8], m.group(1)[8:10])}
    return out


def parties(ctx):
    """[{id, name, aka:[...], keys:[...]}]"""
    res = []
    for e in md_entries(ctx).values():
        if e["file"] != "parties.md":
            continue
        names = [e["title"]]
        for line in e["body"].splitlines():
            m = re.match(r"-\s*aka:\s*(.*)$", line.strip())
            if m:
                names += [x.strip() for x in m.group(1).split(";") if x.strip()]
        names = [n for n in names if n and not n.startswith("<")]
        res.append({"id": e["id"], "name": e["title"], "aka": names[1:], "keys": [k for k in {norm(n) for n in names} if k]})
    return res


def party_ids_in(ctx, text):
    """Ids of known parties whose name or alias occurs in text."""
    t = norm(text)
    return [p["id"] for p in parties(ctx) if any(len(k) >= 3 and k in t for k in p["keys"])]


# ----------------------------------------------------------------------------- ids
def next_num(prefix, existing):
    best = 0
    for i in existing:
        m = re.fullmatch(re.escape(prefix) + r"-(\d+)", i)
        if m:
            best = max(best, int(m.group(1)))
    return "%s-%d" % (prefix, best + 1)


def next_job_id(ctx, day):
    n = 0
    for jid in ledger_entries(ctx):
        m = re.fullmatch(r"J-(\d{8})-(\d+)", jid)
        if m and m.group(1) == day:
            n = max(n, int(m.group(2)))
    return "J-%s-%d" % (day, n + 1)


# ----------------------------------------------------------------------------- init
INDEX_HEADER = "# Memory index\nOne line per entry: `- [<id>] <topic> -> <file> (<status>, <date>)`. Status: active or replaced.\n\n"


def init(ctx):
    made = []
    os.makedirs(ctx.lessons, exist_ok=True)
    os.makedirs(ctx.proposals, exist_ok=True)
    os.makedirs(ctx.p("ledger"), exist_ok=True)
    for fn in MD_FILES:
        if not os.path.exists(ctx.p(fn)):
            write_text(ctx.p(fn), "# %s\n\n" % MD_TITLES[fn])
            made.append(fn)
    if not os.path.exists(ctx.p("index.md")):
        write_text(ctx.p("index.md"), INDEX_HEADER)
        made.append("index.md")
    for fn, hd in (("catalog.tsv", CATALOG_HEADER), ("links.tsv", LINKS_HEADER)):
        if not os.path.exists(ctx.p(fn)):
            ensure_tsv(ctx.p(fn), hd)
            made.append(fn)
    return "memory ready at %s%s" % (ctx.mem, (" (created: %s)" % ", ".join(made)) if made else "")


def index_add(ctx, eid, topic, fn, status="active"):
    path = ctx.p("index.md")
    if not os.path.exists(path):
        write_text(path, INDEX_HEADER)
    text = read_text(path)
    if re.search(r"^- \[%s\]" % re.escape(eid), text, re.M):
        return
    append_text(path, "- [%s] %s -> %s (%s, %s)\n" % (eid, clean(topic), fn, status, now().strftime("%Y-%m-%d")))


# ----------------------------------------------------------------------------- catalog and links
def catalog(ctx):
    return read_tsv(ctx.p("catalog.tsv"), CATALOG_HEADER)


def links(ctx):
    return read_tsv(ctx.p("links.tsv"), LINKS_HEADER)


def add_link(ctx, frm, rel, to, via=""):
    frm, rel, to = clean(frm), clean(rel), clean(to)
    if not (frm and rel and to):
        raise GraphError("a link needs from, relation and to")
    check_text(frm, to)
    for r in links(ctx):
        if r[0] == frm and r[1] == rel and r[2] == to:
            return False
    append_tsv(ctx.p("links.tsv"), LINKS_HEADER, [frm, rel, to, via])
    return True


def register_doc(ctx, kind, where, title, period="", parties_=(), numbers=(), topics=(), first_seen=""):
    """Add or update a catalog line; returns its K id. Never stores bodies, amounts or ID numbers."""
    kind = kind if kind in KINDS else "other"
    where, title = clean(where), clean(title)
    if not (where or title):
        raise GraphError("a document needs a where or a title")
    check_text(where, title, " ".join(parties_), " ".join(numbers), " ".join(topics))
    rows = catalog(ctx)
    pj, nj, tj = ";".join(clean(x) for x in parties_), ";".join(clean(x) for x in numbers), ";".join(clean(x) for x in topics)
    for r in rows:
        if r[2] == where and r[3] == title:
            for idx, val in ((4, period), (5, pj), (6, nj), (7, tj)):
                if val and r[idx] != val:
                    r[idx] = val if idx == 4 else ";".join(dict.fromkeys([x for x in (r[idx].split(";") + val.split(";")) if x]))
            rewrite_tsv(ctx.p("catalog.tsv"), CATALOG_HEADER, rows)
            return r[0]
    kid = next_num("K", [r[0] for r in rows])
    append_tsv(ctx.p("catalog.tsv"), CATALOG_HEADER, [kid, kind, where, title, period, pj, nj, tj, first_seen or now().strftime("%Y-%m-%d")])
    for pid in party_ids_in(ctx, " ".join([where, title, pj])):
        add_link(ctx, kid, "mentions", pid, first_seen)
    if period:
        add_link(ctx, kid, "for", "T-" + period, first_seen)
    return kid


# ----------------------------------------------------------------------------- job
def _list(v):
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def write_job(ctx, spec):
    """Write one ledger entry plus its catalog lines and links. Returns the job id."""
    skill = clean(spec.get("skill")) or "unknown"
    summary = clean(spec.get("summary")) or "(no summary)"
    status = clean(spec.get("status")) or "done"
    if status not in ("done", "blocked", "partial"):
        raise GraphError("status must be done, blocked or partial")
    period = clean(spec.get("period"))
    if period and not re.fullmatch(r"\d{4}-\d{2}", period):
        raise GraphError("period must look like 2026-10")
    when = spec.get("when")
    t = dt.datetime.fromisoformat(when) if when else now()
    day = t.strftime("%Y%m%d")
    init(ctx)
    all_text = json.dumps(spec, ensure_ascii=False)
    check_text(all_text)
    jid = next_job_id(ctx, day)

    read_lines, edges = [], []
    for item in _list(spec.get("read")):
        if isinstance(item, str):
            m = re.fullmatch(r"([SK]-\d+)(?:\s*[:=-]\s*(.*))?", item.strip())
            if m:
                read_lines.append("%s -> %s" % (m.group(1), m.group(2) or "supplied figures"))
                edges.append((jid, "reads", m.group(1)))
            else:
                read_lines.append(clean(item))
            continue
        kid = clean(item.get("id"))
        if not kid:
            kid = register_doc(ctx, clean(item.get("kind")) or "other", item.get("where") or item.get("path") or item.get("sender") or "",
                               item.get("title") or item.get("subject") or "", item.get("period") or period,
                               _list(item.get("parties")), _list(item.get("numbers")), _list(item.get("topics")), jid)
        rng = " / ".join(clean(item[k]) for k in ("sheet", "range") if item.get(k))
        where = clean(item.get("where") or item.get("path") or item.get("subject") or item.get("title") or "")
        if not where:
            row = next((r for r in catalog(ctx) if r[0] == kid), None)
            where = (row[2] or row[3]) if row else ""
        label = "%s (%s%s)" % (kid, where, (" / " + rng) if rng else "")
        read_lines.append("%s -> %s" % (label, clean(item.get("supplied")) or "supplied figures"))
        edges.append((jid, "reads", kid))
        for pid in _list(item.get("party_ids")):
            edges.append((kid, "mentions", pid))

    used_lines = []
    for item in _list(spec.get("used")):
        if isinstance(item, dict):
            used_lines.append("formula: %s%s" % (clean(item.get("formula")), (" @ " + clean(item.get("where"))) if item.get("where") else ""))
            continue
        item = clean(item)
        used_lines.append(item)
        for i in ID_RE.findall(item):
            rel = "uses" if i.startswith("F-") else "applies"
            edges.append((jid, rel, i))

    made_lines = [clean(x) for x in _list(spec.get("made"))]
    for m in made_lines:
        edges.append((jid, "makes", m))
    problems = []
    for pr in _list(spec.get("problems")):
        if isinstance(pr, dict):
            problems.append("%s -> %s (saved: %s)" % (clean(pr.get("problem")), clean(pr.get("resolution")) or "unresolved", clean(pr.get("saved")) or "none"))
        else:
            problems.append(clean(pr))
    decisions = [clean(x) for x in _list(spec.get("decisions"))]
    for d in decisions:
        for i in ID_RE.findall(d):
            edges.append((jid, "applies", i))
    if period:
        edges.append((jid, "for", "T-" + period))
    carry = clean(spec.get("carries_to"))
    if carry and period:
        edges.append(("T-" + period, "carries-to", "T-" + carry))

    lines = [
        "## %s %s %s - %s" % (jid, t.strftime("%H:%M"), skill, summary),
        "- client / period: %s / %s" % (clean(spec.get("client")) or "-", period or "-"),
        "- status: %s" % status,
        "- read: %s" % ("; ".join(read_lines) or "-"),
        "- used: %s" % ("; ".join(used_lines) or "-"),
        "- made: %s" % ("; ".join(made_lines) or "-"),
        "- checks: %s" % (clean(spec.get("checks")) or "-"),
        "- problems: %s" % ("; ".join(problems) or "-"),
    ]
    if decisions:
        lines.append("- decisions: %s" % "; ".join(decisions))
    month = t.strftime("%Y-%m")
    path = ctx.p("ledger", month + ".md")
    if not os.path.exists(path):
        write_text(path, "# Ledger %s\n\n" % month)
    append_text(path, "\n".join(lines) + "\n\n")
    for f, r, to in edges:
        add_link(ctx, f, r, to, jid)
    return jid


# ----------------------------------------------------------------------------- party and entries
def add_entry(ctx, kind, name, fields=None, aka=()):
    """Create a P/D/R/S/F entry in its file with the template fields; returns the id."""
    files = {"P": "parties.md", "D": "decisions.md", "R": "recurring.md", "S": "sources.md", "F": "formulas.md"}
    if kind not in files:
        raise GraphError("kind must be one of P D R S F")
    init(ctx)
    check_text(name, json.dumps(fields or {}, ensure_ascii=False), " ".join(aka))
    existing = md_entries(ctx)
    eid = next_num(kind, existing.keys())
    lines = ["", "## %s %s" % (eid, clean(name))]
    for k, v in (fields or {}).items():
        lines.append("- %s: %s" % (clean(k), clean(v)))
    if aka:
        lines.append("- aka: %s" % "; ".join(clean(a) for a in aka))
    append_text(ctx.p(files[kind]), "\n".join(lines) + "\n")
    index_add(ctx, eid, name, files[kind])
    return eid


# ----------------------------------------------------------------------------- search
def term_groups(ctx, query):
    """One group per query word: the word itself plus every other spelling and id of a party it names."""
    pts = parties(ctx)
    groups = []
    for a, b in re.findall(r'"([^"]+)"|(\S+)', query):
        word = a or b
        k = norm(word)
        if not k or re.sub(r"[.,]", "", word).casefold() in BARE_COMPANY:
            continue
        keys, ids = {k}, set()
        if ID_RE.fullmatch(word.strip()):
            ids.add(word.strip())
        for p in pts:
            if any(k == pk or (len(k) >= 3 and len(pk) >= 3 and (k in pk or pk in k)) for pk in p["keys"]):
                keys.update(p["keys"])
                ids.add(p["id"])
        groups.append({"keys": sorted(keys), "ids": sorted(ids), "word": k})
    return groups


def group_hit(group, raw, nraw):
    if any(key in nraw for key in group["keys"]):
        return True
    return any(re.search(r"(?<![A-Za-z0-9-])%s(?!\d)" % re.escape(i), raw) for i in group["ids"])


def _hit(text, groups):
    raw, nraw = str(text), norm(text)
    return sum(1 for g_ in groups if group_hit(g_, raw, nraw))


def find(ctx, query, limit=20, files_dir=None):
    """Ranked hits across the catalog, links, entries, ledger and (optionally) live files.

    Every query word also matches the other spellings and the id of a party it names, so a Thai
    name finds the English-named invoice and the other way round.
    """
    groups = term_groups(ctx, query)
    if not groups:
        raise GraphError("empty query")
    hits = []

    def add(score, kind, eid, where, snippet):
        hits.append({"score": score, "type": kind, "id": eid, "where": where, "snippet": clean(snippet)[:200]})

    for r in catalog(ctx):
        full = " ".join(r)
        if _hit(full, groups) == len(groups):
            add(3 + _hit(" ".join(r[3:4] + r[5:7]), groups), "document", r[0], r[2],
                "%s | %s | period %s | parties %s | numbers %s | topics %s" % (r[1], r[3], r[4], r[5], r[6], r[7]))
    for e in list(md_entries(ctx).values()) + list(ledger_entries(ctx).values()):
        if _hit(e["title"] + " " + e["body"], groups) == len(groups):
            add(2 + 2 * _hit(e["title"], groups), "entry" if e["id"][0] != "J" else "job", e["id"], e["file"],
                e["title"] + " :: " + e["body"].replace("\n", " "))
    for r in links(ctx):
        if _hit(" ".join(r[:3]), groups) == len(groups) and not ID_RE.fullmatch(" ".join(r[:3])):
            add(1, "link", "%s %s %s" % (r[0], r[1], r[2]), "links.tsv", "via %s" % r[3])
    if files_dir:
        hits += search_files(files_dir, groups, ctx.root)
    hits.sort(key=lambda h: (-h["score"], h["id"]))
    return hits[:limit]


def _docx_text(path):
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8", "ignore")
    return html.unescape(re.sub(r"<[^>]+>", " ", xml))


def _xlsx_text(path):
    out = []
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        if "xl/workbook.xml" in names:
            out += re.findall(r'<sheet [^>]*name="([^"]+)"', z.read("xl/workbook.xml").decode("utf-8", "ignore"))
        if "xl/sharedStrings.xml" in names:
            out.append(html.unescape(re.sub(r"<[^>]+>", " ", z.read("xl/sharedStrings.xml").decode("utf-8", "ignore"))))
    return " ".join(out)


def read_file_text(path):
    """Searchable text of a file, or None when its content cannot be read here (pdf, image, old formats)."""
    ext = os.path.splitext(path)[1].lower()
    try:
        if os.path.getsize(path) > 8 * 1024 * 1024:
            return None
        if ext in TEXT_EXT:
            with open(path, encoding="utf-8", errors="ignore") as f:
                return f.read()
        if ext == ".docx":
            return _docx_text(path)
        if ext in (".xlsx", ".xlsm"):
            return _xlsx_text(path)
    except (OSError, KeyError, zipfile.BadZipFile):
        return None
    return None


def walk_files(root, skip=("Accountant", ".git", ".kouen-worktrees", "node_modules", "dist", ".tmp")):
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if x not in skip and not x.startswith(".")]
        for fn in sorted(files):
            if not fn.startswith(".") and not fn.startswith("~$"):
                yield os.path.join(d, fn)


def search_files(root, groups, base=None, cap=300):
    res, unreadable = [], 0
    base = os.path.abspath(base or root)
    for path in walk_files(root):
        rel = os.path.relpath(path, base) if os.path.abspath(path).startswith(base + os.sep) else path
        ext = os.path.splitext(path)[1].lower()
        in_name = _hit(rel, groups)
        text = read_file_text(path)
        if text is None:
            if ext in KIND_EXT and in_name == len(groups):
                res.append({"score": 2, "type": "file", "id": rel, "where": "name only", "snippet": "content not searched (%s); ask doc-reader" % (ext or "no extension")})
            elif ext in (".pdf",) + tuple(k for k, v in KIND_EXT.items() if v == "image"):
                unreadable += 1
            continue
        if _hit(text, groups) == len(groups) or in_name == len(groups):
            low = clean(text).casefold()
            pos = min([low.find(k) for k in groups[0]["keys"] if low.find(k) >= 0] or [0])
            raw = clean(text)[max(0, pos - 40):pos + 120]
            res.append({"score": 2 + (1 if in_name == len(groups) else 0), "type": "file", "id": rel,
                        "where": "name" if in_name == len(groups) else "content", "snippet": raw})
        if len(res) >= cap:
            break
    if unreadable:
        res.append({"score": 0, "type": "note", "id": "unreadable", "where": "folder", "snippet": "%d pdf/image files were matched by name only; their content needs doc-reader" % unreadable})
    return res


# ----------------------------------------------------------------------------- graph queries
def graph(ctx):
    adj, rel = {}, []
    for f, r, t, v in links(ctx):
        adj.setdefault(f, set()).add(t)
        adj.setdefault(t, set()).add(f)
        rel.append((f, r, t, v))
    return adj, rel


def resolve(ctx, ref):
    """An id, a file path/label, a number or a name -> the best matching id."""
    ref = clean(ref)
    if ID_RE.fullmatch(ref):
        return ref
    key = norm(ref)
    for p in parties(ctx):
        if key and key in p["keys"]:
            return p["id"]
    for r in catalog(ctx):
        if ref in (r[2], r[3]) or any(ref == x for x in r[6].split(";") if x):
            return r[0]
    for h in find(ctx, ref, limit=1):
        if ID_RE.fullmatch(h["id"]):
            return h["id"]
    return ref


def describe(ctx, i, cat=None, ents=None, jobs=None):
    cat = cat if cat is not None else {r[0]: r for r in catalog(ctx)}
    ents = ents if ents is not None else md_entries(ctx)
    jobs = jobs if jobs is not None else ledger_entries(ctx)
    if i in cat:
        r = cat[i]
        return "%s [%s] %s | %s | period %s" % (i, r[1], r[3], r[2], r[4] or "-")
    if i in ents:
        return "%s %s (%s)" % (i, ents[i]["title"], ents[i]["file"])
    if i in jobs:
        j = jobs[i]
        return "%s %s %s %s - %s" % (i, j["date"], j["time"], j["skill"], j["title"])
    return i


def neighbors(ctx, ref):
    node = resolve(ctx, ref)
    adj, rel = graph(ctx)
    cat = {r[0]: r for r in catalog(ctx)}
    ents, jobs = md_entries(ctx), ledger_entries(ctx)
    out = ["%s" % describe(ctx, node, cat, ents, jobs)]
    for f, r, t, v in rel:
        if f == node:
            out.append("  --%s--> %s" % (r, describe(ctx, t, cat, ents, jobs)))
        elif t == node:
            out.append("  <--%s-- %s" % (r, describe(ctx, f, cat, ents, jobs)))
    if len(out) == 1:
        out.append("  (no links yet)")
    return "\n".join(out)


def trace(ctx, ref):
    """Follow a file, document, number or job back to its jobs, sources, formulas, checks and period chain."""
    node = resolve(ctx, ref)
    adj, rel = graph(ctx)
    cat = {r[0]: r for r in catalog(ctx)}
    ents, jobs = md_entries(ctx), ledger_entries(ctx)
    out = ["trace of %s" % describe(ctx, node, cat, ents, jobs)]
    job_ids = [node] if node in jobs else sorted({f for f, r, t, v in rel if t == node and f in jobs})
    if not job_ids:
        out.append("  no job has read or made this yet")
    for jid in job_ids:
        j = jobs[jid]
        out.append("  job %s %s %s %s - %s" % (jid, j["date"], j["time"], j["skill"], j["title"]))
        for line in j["body"].splitlines():
            if re.match(r"-\s*(read|used|made|checks|problems|client / period|status):", line.strip()):
                out.append("    " + line.strip())
        for f, r, t, v in rel:
            if f == jid and r == "for":
                out.append("    period chain: " + " <- ".join(period_chain(rel, t)))
    return "\n".join(out)


def period_chain(rel, period, depth=12):
    chain = [period]
    cur = period
    for _ in range(depth):
        prev = [f for f, r, t, v in rel if r == "carries-to" and t == cur]
        if not prev:
            break
        cur = prev[0]
        chain.append(cur)
    return chain


def impact(ctx, ref):
    """Jobs, periods and files that depend on a formula, source, party or decision."""
    node = resolve(ctx, ref)
    adj, rel = graph(ctx)
    jobs = ledger_entries(ctx)
    ents = md_entries(ctx)
    cat = {r[0]: r for r in catalog(ctx)}
    users = sorted({f for f, r, t, v in rel if t == node and f in jobs} | {t for f, r, t, v in rel if f == node and t in jobs})
    for f, r, t, v in rel:
        if t == node and f.startswith("K-"):
            users += sorted({ff for ff, rr, tt, vv in rel if tt == f and ff in jobs})
    users = sorted(set(users))
    out = ["impact of %s: %d job(s)" % (describe(ctx, node, cat, ents, jobs), len(users))]
    months, periods, made = set(), set(), []
    for jid in users:
        j = jobs[jid]
        months.add(j["file"])
        out.append("  %s %s %s - %s" % (jid, j["date"], j["skill"], j["title"]))
        for f, r, t, v in rel:
            if f == jid and r == "for":
                periods.add(t)
            if f == jid and r == "makes":
                made.append(t)
    if periods:
        out.append("  periods: " + ", ".join(sorted(periods)))
    if made:
        out.append("  produced: " + "; ".join(sorted(set(made))))
    if months:
        out.append("  ledger months: " + ", ".join(sorted(months)))
    return "\n".join(out)


def path(ctx, a, b, max_hops=4):
    na, nb = resolve(ctx, a), resolve(ctx, b)
    adj, rel = graph(ctx)
    if na not in adj or nb not in adj:
        return "no path: %s or %s is not in the links yet" % (na, nb)
    prev, frontier = {na: None}, [na]
    for _ in range(max_hops):
        nxt = []
        for n in frontier:
            for m in sorted(adj.get(n, ())):
                if m not in prev:
                    prev[m] = n
                    nxt.append(m)
        frontier = nxt
        if nb in prev:
            break
    if nb not in prev:
        return "no path of %d hops or fewer between %s and %s" % (max_hops, na, nb)
    seq, cur = [], nb
    while cur is not None:
        seq.append(cur)
        cur = prev[cur]
    seq.reverse()
    cat = {r[0]: r for r in catalog(ctx)}
    ents, jobs = md_entries(ctx), ledger_entries(ctx)
    return "\n".join(["path (%d hops):" % (len(seq) - 1)] + ["  " + describe(ctx, n, cat, ents, jobs) for n in seq])


def usage(ctx, skills=()):
    stats = {}
    for j in ledger_entries(ctx).values():
        s = stats.setdefault(j["skill"], {"count": 0, "last": ""})
        s["count"] += 1
        s["last"] = max(s["last"], j["date"])
    for s in skills:
        stats.setdefault(s, {"count": 0, "last": ""})
    rows = sorted(stats.items(), key=lambda kv: (kv[1]["last"] or "0000", kv[0]))
    today = now().date()
    out = ["skill | uses | last used | days ago"]
    for s, v in rows:
        ago = (today - dt.date.fromisoformat(v["last"])).days if v["last"] else "never"
        out.append("%s | %d | %s | %s" % (s, v["count"], v["last"] or "-", ago))
    return "\n".join(out)


def problems(ctx, skill=None, party=None):
    out = []
    for j in ledger_entries(ctx).values():
        if skill and j["skill"] != skill:
            continue
        for line in j["body"].splitlines():
            m = re.match(r"-\s*problems:\s*(.*)$", line.strip())
            if m and m.group(1) != "-":
                if party and norm(party) not in norm(j["body"]):
                    continue
                out.append("%s %s %s: %s" % (j["id"], j["date"], j["skill"], m.group(1)))
    counts = {}
    for l in out:
        key = norm(l.split(": ", 1)[1].split("->")[0])
        counts[key] = counts.get(key, 0) + 1
    rep = [k for k, v in counts.items() if v >= 2]
    res = out or ["no problems recorded"]
    if rep:
        res.append("repeated (2+): %d problem(s); each needs a lesson or a decision" % len(rep))
    return "\n".join(res)


# ----------------------------------------------------------------------------- integrity
def check(ctx):
    """Return a list of findings; empty means the memory is consistent."""
    issues = []
    cat = {r[0]: r for r in catalog(ctx)}
    ents, jobs = md_entries(ctx), ledger_entries(ctx)
    known = set(cat) | set(ents) | set(jobs)
    rel = links(ctx)
    for f, r, t, v in rel:
        for end in (f, t):
            if ID_RE.fullmatch(end) and end not in known and not end.startswith("T-"):  # periods need no entry
                issues.append("dangling id %s used in link %s %s %s" % (end, f, r, t))
    read_k = {t for f, r, t, v in rel if r == "reads"}
    for kid in cat:
        if kid not in read_k:
            issues.append("document %s (%s) was never read by a job" % (kid, cat[kid][3] or cat[kid][2]))
    linked_jobs = {f for f, r, t, v in rel} | {t for f, r, t, v in rel}
    for jid in jobs:
        if jid not in linked_jobs:
            issues.append("job %s has no links" % jid)
    seen = {}
    for p in parties(ctx):
        for k in p["keys"]:
            if k in seen and seen[k] != p["id"]:
                issues.append("parties %s and %s share a name once company words are dropped; merge under one aka:" % (seen[k], p["id"]))
            seen[k] = p["id"]
    idx = read_text(ctx.p("index.md"))
    for eid, e in ents.items():
        if not re.search(r"^- \[%s\]" % re.escape(eid), idx, re.M):
            issues.append("entry %s (%s) is missing from index.md" % (eid, e["file"]))
    seen_ids = {}
    for fn in MD_FILES:
        for m in ENTRY_RE.finditer(read_text(ctx.p(fn))):
            if m.group(1) in seen_ids:
                issues.append("duplicate entry id %s" % m.group(1))
            seen_ids[m.group(1)] = fn
    return issues


# ----------------------------------------------------------------------------- map
MAP_HTML = """<!doctype html><meta charset="utf-8"><title>Accountant map</title>
<style>body{font:14px system-ui,sans-serif;margin:0;display:flex;height:100vh}#side{width:300px;padding:12px;overflow:auto;border-right:1px solid #ccc}
#c{flex:1}input{width:100%%;padding:6px;box-sizing:border-box}.k{display:inline-block;width:10px;height:10px;margin-right:4px;border-radius:50%%}</style>
<div id="side"><b>Accountant map</b><p>%(note)s</p><input id="q" placeholder="search an id or a name"><div id="info"></div>
<p>%(legend)s</p></div><svg id="c"></svg>
<script>
const N=%(nodes)s,E=%(edges)s,col={P:"#2a7",D:"#a62",R:"#68c",S:"#c8a",F:"#d90",K:"#555",J:"#37c",T:"#c33"};
const svg=document.getElementById("c"),W=()=>svg.clientWidth,H=()=>svg.clientHeight;
const idx={};N.forEach((n,i)=>{n.x=Math.random()*600;n.y=Math.random()*500;n.vx=0;n.vy=0;idx[n.id]=n});
const L=E.filter(e=>idx[e.f]&&idx[e.t]);
function step(){for(const a of N)for(const b of N){if(a===b)continue;let dx=a.x-b.x,dy=a.y-b.y,d=Math.hypot(dx,dy)+.1,f=900/(d*d);a.vx+=f*dx/d;a.vy+=f*dy/d}
for(const e of L){const a=idx[e.f],b=idx[e.t];let dx=b.x-a.x,dy=b.y-a.y,d=Math.hypot(dx,dy)+.1,f=(d-70)*.02;a.vx+=f*dx/d;a.vy+=f*dy/d;b.vx-=f*dx/d;b.vy-=f*dy/d}
for(const n of N){n.vx+=(W()/2-n.x)*.002;n.vy+=(H()/2-n.y)*.002;n.x+=n.vx*.6;n.y+=n.vy*.6;n.vx*=.6;n.vy*=.6}}
for(let i=0;i<250;i++)step();
let sel=null;function draw(){let s="";for(const e of L){const a=idx[e.f],b=idx[e.t],on=sel&&(e.f==sel||e.t==sel);s+=`<line x1="${a.x}" y1="${a.y}" x2="${b.x}" y2="${b.y}" stroke="${on?"#000":"#bbb"}" stroke-width="${on?2:1}"><title>${e.r}</title></line>`}
for(const n of N){s+=`<g onclick="pick('${n.id}')" style="cursor:pointer"><circle cx="${n.x}" cy="${n.y}" r="${n.id==sel?9:6}" fill="${col[n.id[0]]||"#999"}"/><text x="${n.x+8}" y="${n.y+4}" font-size="11">${n.id}</text><title>${n.label}</title></g>`}
svg.innerHTML=s}
function pick(id){sel=id;const n=idx[id];const nb=L.filter(e=>e.f==id||e.t==id).map(e=>(e.f==id?"&rarr; "+e.r+" ":"&larr; "+e.r+" ")+(idx[e.f==id?e.t:e.f].label));
document.getElementById("info").innerHTML="<p><b>"+id+"</b><br>"+n.label+"</p><ul><li>"+nb.join("</li><li>")+"</li></ul>";draw()}
document.getElementById("q").oninput=e=>{const v=e.target.value.toLowerCase();const m=N.find(n=>n.id.toLowerCase()==v||n.label.toLowerCase().includes(v));if(v&&m)pick(m.id)};
draw();
</script>"""


def build_map(ctx, focus=None, period=None, out=None, cap=300):
    adj, rel = graph(ctx)
    cat = {r[0]: r for r in catalog(ctx)}
    ents, jobs = md_entries(ctx), ledger_entries(ctx)
    if focus:
        start = {resolve(ctx, focus)}
    elif period:
        start = {"T-" + period}
    else:
        start = set()
    keep = set(start)
    if start:
        for _ in range(2):
            keep |= {m for n in list(keep) for m in adj.get(n, ())}
    edges = [e for e in rel if (not start) or (e[0] in keep and e[2] in keep)]
    note = "everything"
    if len(edges) > cap:
        edges = edges[:cap]
        note = "first %d links only; pick a party or a period (map --party / --period) to see one area" % cap
    elif start:
        note = "around %s, two hops" % ", ".join(sorted(start))
    ids = {x for e in edges for x in (e[0], e[2])} | start
    nodes = [{"id": i, "label": describe(ctx, i, cat, ents, jobs)} for i in sorted(ids)]
    data = {"nodes": json.dumps(nodes, ensure_ascii=False), "edges": json.dumps([{"f": f, "r": r, "t": t} for f, r, t, v in edges], ensure_ascii=False),
            "note": html.escape(note), "legend": "P party, D decision, R recurring, S source, F formula, K document, J job, T period"}
    target = out or ctx.p("map.html")
    write_text(target, MAP_HTML % data)
    return "map written to %s (%d nodes, %d links; %s)" % (target, len(nodes), len(edges), note)


# ----------------------------------------------------------------------------- index scan
def guess_period(text):
    m = re.search(r"(?<!\d)(20\d{2}|25\d{2})[-_.]?(0[1-9]|1[0-2])(?!\d)", text)
    if not m:
        return ""
    y = int(m.group(1))
    if y > 2400:
        y -= 543
    return "%04d-%s" % (y, m.group(2))


def index_scan(ctx, folder, month=None, max_new=200):
    """Catalog files in a folder by name, kind, period and known parties; resumable (skips known paths)."""
    init(ctx)
    folder = os.path.abspath(folder)
    known = {r[2] for r in catalog(ctx)}
    new, skipped, needs_read = 0, 0, 0
    for p in walk_files(folder):
        ext = os.path.splitext(p)[1].lower()
        if ext not in KIND_EXT:
            continue
        rel = os.path.relpath(p, ctx.root) if p.startswith(ctx.root) else p
        if rel in known:
            skipped += 1
            continue
        stem = os.path.splitext(os.path.basename(p))[0]
        per = guess_period(rel) or dt.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%Y-%m")
        if month and per != month:
            continue
        text = read_file_text(p)
        pids = party_ids_in(ctx, rel + " " + (text or "")[:20000])
        topics = [] if text is not None else ["needs-read"]
        if text is None:
            needs_read += 1
        kid = register_doc(ctx, KIND_EXT[ext], rel, stem, per, pids, [], topics, "index-" + now().strftime("%Y-%m-%d"))
        for pid in pids:
            add_link(ctx, kid, "mentions", pid, "index")
        new += 1
        if new >= max_new:
            break
    return "indexed %d new file(s), %d already known, %d need a reader (pdf/image/old format; ask doc-reader)%s" % (
        new, skipped, needs_read, "; run again to continue" if new >= max_new else "")


# ----------------------------------------------------------------------------- lessons (improve a skill directly)
LESSON_MAX = 40
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")


def lesson(ctx, skill, text):
    skill = re.sub(r"[^a-z0-9-]", "", clean(skill).lower())
    text = clean(text)
    if not skill or not text:
        raise GraphError("lesson needs a skill name and a text")
    if EMAIL_RE.search(text):
        raise GraphError("refused: a lesson must not contain an e-mail address")
    check_text(text)
    path_ = os.path.join(ctx.lessons, skill + ".md")
    cur = read_text(path_)
    lines = [l for l in cur.splitlines() if l.strip().startswith("- ")]
    if any(norm(l.split("]", 1)[-1]) == norm(text) for l in lines):
        return "already saved: %s" % text
    if len(lines) >= LESSON_MAX:
        raise GraphError("%s.md already has %d lessons (limit %d); merge similar ones or promote them first (lessons-review, promote)" % (skill, len(lines), LESSON_MAX))
    if not cur:
        cur = "# Lessons for %s\n\n" % skill
    write_text(path_, cur.rstrip("\n") + "\n- [%s] %s\n" % (now().strftime("%Y-%m-%d"), text))
    return "lesson saved to lessons/%s.md (%d of %d): %s" % (skill, len(lines) + 1, LESSON_MAX, text)


def lessons_review(ctx):
    out = []
    if not os.path.isdir(ctx.lessons):
        return "no lessons yet"
    for fn in sorted(os.listdir(ctx.lessons)):
        if not fn.endswith(".md"):
            continue
        lines = [l for l in read_text(os.path.join(ctx.lessons, fn)).splitlines() if l.strip().startswith("- ")]
        keys = [norm(l.split("]", 1)[-1]) for l in lines]
        dup = len(keys) - len(set(keys))
        flag = []
        if len(lines) >= LESSON_MAX:
            flag.append("at the limit: merge or promote")
        if dup:
            flag.append("%d duplicate(s)" % dup)
        out.append("%s: %d lesson(s)%s" % (fn[:-3], len(lines), (" - " + "; ".join(flag)) if flag else ""))
    return "\n".join(out) or "no lessons yet"


def promote(ctx, skill, plugin_dir, yes=False):
    """Fold a skill's lessons into its SKILL.md (a '## Learned rules' section) and bump its patch version."""
    skill = re.sub(r"[^a-z0-9-]", "", skill.lower())
    src = os.path.join(plugin_dir, "skills", skill, "SKILL.md")
    if not os.path.exists(src):
        raise GraphError("no such skill file: %s" % src)
    lp = os.path.join(ctx.lessons, skill + ".md")
    lines = [l.strip() for l in read_text(lp).splitlines() if l.strip().startswith("- ")]
    if not lines:
        return "nothing to promote for %s" % skill
    bullets = [re.sub(r"^- \[[^\]]*\]\s*", "- ", l) for l in lines]
    preview = "would add %d rule(s) to skills/%s/SKILL.md under '## Learned rules':\n%s" % (len(bullets), skill, "\n".join(bullets))
    if not yes:
        return preview + "\n(dry run; run again with --yes after the user approves)"
    text = read_text(src)
    block = "\n".join(bullets)
    if "## Learned rules" in text:
        text = re.sub(r"(## Learned rules\n(?:.*\n)*?)(?=\n## |\Z)", lambda m: m.group(1).rstrip("\n") + "\n" + block + "\n", text, count=1)
    else:
        marker = "\n## Learn and remember"
        i = text.find(marker)
        section = "\n## Learned rules\nPromoted from real jobs; each was verified when it was saved.\n" + block + "\n"
        text = (text[:i] + section + text[i:]) if i >= 0 else text.rstrip("\n") + "\n" + section
    m = re.search(r'(metadata:\s*\n\s*version: ")(\d+)\.(\d+)\.(\d+)(")', text)
    if m:
        text = text[:m.start()] + "%s%s.%s.%d%s" % (m.group(1), m.group(2), m.group(3), int(m.group(4)) + 1, m.group(5)) + text[m.end():]
    write_text(src, text)
    arch = os.path.join(ctx.lessons, "_promoted", "%s-%s.md" % (skill, now().strftime("%Y-%m-%d")))
    write_text(arch, read_text(lp))
    write_text(lp, "# Lessons for %s\n\n" % skill)
    return "promoted %d rule(s) into %s (patch version bumped); lessons archived at %s. Rebuild and reinstall the plugin to ship it." % (len(bullets), src, arch)


# ----------------------------------------------------------------------------- formatting and cli
def fmt_hits(hits):
    if not hits:
        return "nothing found"
    return "\n".join("%s %s | %s | %s" % (h["type"], h["id"], h["where"], h["snippet"]) for h in hits)


def run(ctx, args, as_json=False):
    c = args.command
    if c == "init":
        return init(ctx)
    if c == "job":
        spec = json.load(sys.stdin) if args.json_file == "-" else json.load(open(args.json_file, encoding="utf-8"))
        jid = write_job(ctx, spec)
        return "บันทึกงาน %s" % jid
    if c == "register-doc":
        kid = register_doc(ctx, args.kind, args.where, args.title, args.period or "", args.parties or [], args.numbers or [], args.topics or [])
        return kid
    if c == "link":
        return "added" if add_link(ctx, args.frm, args.relation, args.to, args.via or "") else "already there"
    if c == "party":
        pid = add_entry(ctx, "P", args.name, {"role": args.role or "vendor"}, args.aka or [])
        return pid
    if c == "find":
        hits = find(ctx, " ".join(args.query), args.limit, args.files)
        return json.dumps(hits, ensure_ascii=False, indent=1) if as_json else fmt_hits(hits)
    if c == "neighbors":
        return neighbors(ctx, " ".join(args.ref))
    if c == "trace":
        return trace(ctx, " ".join(args.ref))
    if c == "impact":
        return impact(ctx, " ".join(args.ref))
    if c == "path":
        return path(ctx, args.a, args.b)
    if c == "usage":
        names = []
        if args.plugin and os.path.isdir(os.path.join(args.plugin, "skills")):
            names = sorted(d for d in os.listdir(os.path.join(args.plugin, "skills")) if os.path.isdir(os.path.join(args.plugin, "skills", d)))
        return usage(ctx, names)
    if c == "problems":
        return problems(ctx, args.skill, args.party)
    if c == "check":
        issues = check(ctx)
        text = "memory is consistent" if not issues else "%d finding(s):\n%s" % (len(issues), "\n".join("  - " + i for i in issues))
        if issues and args.strict:
            print(text)
            raise SystemExit(1)
        return text
    if c == "map":
        return build_map(ctx, args.party, args.period, args.out)
    if c == "index-scan":
        return index_scan(ctx, args.folder, args.month, args.max)
    if c == "lesson":
        return lesson(ctx, args.skill, " ".join(args.text))
    if c == "lessons-review":
        return lessons_review(ctx)
    if c == "promote":
        return promote(ctx, args.skill, args.plugin, args.yes)
    raise GraphError("unknown command %s" % c)


def build_parser():
    ap = argparse.ArgumentParser(prog="graph.py", description=__doc__.split("\n\n")[0])
    ap.add_argument("--root", help="the work folder (default: nearest folder holding Accountant/, or ACCOUNTANT_ROOT)")
    ap.add_argument("--client", help="client slug (firm mode)")
    ap.add_argument("--json", action="store_true", help="JSON output where supported")
    ap.add_argument("--version", action="version", version=VERSION)
    sub = ap.add_subparsers(dest="command", required=True)
    sub.add_parser("init")
    j = sub.add_parser("job"); j.add_argument("json_file", help="a JSON file, or - for stdin")
    r = sub.add_parser("register-doc"); r.add_argument("--kind", default="other"); r.add_argument("--where", default="")
    r.add_argument("--title", default=""); r.add_argument("--period"); r.add_argument("--parties", nargs="*"); r.add_argument("--numbers", nargs="*"); r.add_argument("--topics", nargs="*")
    l = sub.add_parser("link"); l.add_argument("frm"); l.add_argument("relation"); l.add_argument("to"); l.add_argument("--via")
    p = sub.add_parser("party"); p.add_argument("--name", required=True); p.add_argument("--role"); p.add_argument("--aka", nargs="*")
    f = sub.add_parser("find"); f.add_argument("query", nargs="+"); f.add_argument("--limit", type=int, default=20); f.add_argument("--files", help="also search this folder live")
    for name in ("neighbors", "trace", "impact"):
        x = sub.add_parser(name); x.add_argument("ref", nargs="+")
    pa = sub.add_parser("path"); pa.add_argument("a"); pa.add_argument("b")
    u = sub.add_parser("usage"); u.add_argument("--plugin", help="plugin folder, to list skills never used")
    pr = sub.add_parser("problems"); pr.add_argument("--skill"); pr.add_argument("--party")
    ck = sub.add_parser("check"); ck.add_argument("--strict", action="store_true")
    m = sub.add_parser("map"); m.add_argument("--party"); m.add_argument("--period"); m.add_argument("--out")
    ix = sub.add_parser("index-scan"); ix.add_argument("folder"); ix.add_argument("--month"); ix.add_argument("--max", type=int, default=200)
    ls = sub.add_parser("lesson"); ls.add_argument("skill"); ls.add_argument("text", nargs="+")
    sub.add_parser("lessons-review")
    pm = sub.add_parser("promote"); pm.add_argument("skill"); pm.add_argument("--plugin", required=True); pm.add_argument("--yes", action="store_true")
    return ap


def main(argv=None):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    args = build_parser().parse_args(argv)
    ctx = Ctx(args.root, args.client)
    try:
        print(run(ctx, args, args.json))
    except GraphError as e:
        print("error: %s" % e, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
