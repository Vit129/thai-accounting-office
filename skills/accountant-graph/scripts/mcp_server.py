#!/usr/bin/env python3
"""MCP server (stdio) exposing the accountant graph engine as tools for Claude Desktop.

Newline-delimited JSON-RPC 2.0. Standard library only; the work is done by graph.py in the
same folder. Every tool takes an optional root (the work folder) and client (firm mode).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import graph as g  # noqa: E402

S = {"type": "string"}
SL = {"type": "array", "items": S}
COMMON = {"root": {"type": "string", "description": "work folder; default: nearest folder holding Accountant/"},
          "client": {"type": "string", "description": "client slug in firm mode"}}


def tool(name, desc, props, required=()):
    return {"name": name, "description": desc,
            "inputSchema": {"type": "object", "properties": dict(props, **COMMON), "required": list(required)}}


TOOLS = [
    tool("accountant_init", "Create the memory files in a work folder (idempotent).", {}),
    tool("accountant_find", "Search first: names, document numbers, forms, periods across the catalog, links, entries, ledger and optionally live files.",
         {"query": S, "files_dir": S, "limit": {"type": "integer"}}, ["query"]),
    tool("accountant_neighbors", "Everything linked to a party, document, number, job or period.", {"ref": S}, ["ref"]),
    tool("accountant_trace", "Trace a figure, file, document number or job back to its jobs, sources, formulas, checks and period chain.", {"ref": S}, ["ref"]),
    tool("accountant_impact", "Jobs, periods and files that depend on a formula, source, party or decision.", {"ref": S}, ["ref"]),
    tool("accountant_path", "How two things connect (up to 4 hops).", {"a": S, "b": S}, ["a", "b"]),
    tool("accountant_job", "Write the job ledger entry with its catalog lines and links after a job; returns the job id (say it as: บันทึกงาน J-...).",
         {"job": {"type": "object", "description": "skill, summary, client, period (YYYY-MM), status (done|blocked|partial), read[], used[], made[], checks, problems[], decisions[], carries_to"}}, ["job"]),
    tool("accountant_register_doc", "Add or update one document or email in the catalog; returns its K id.",
         {"kind": S, "where": S, "title": S, "period": S, "parties": SL, "numbers": SL, "topics": SL}, ["where"]),
    tool("accountant_party", "Add a party (vendor, customer, payee) with its alternative names.", {"name": S, "role": S, "aka": SL}, ["name"]),
    tool("accountant_lesson", "Save one verified lesson for a skill (the skill reads it before its next job).", {"skill": S, "text": S}, ["skill", "text"]),
    tool("accountant_index_scan", "Catalog the files of a folder by name, period and known parties (resumable).", {"folder": S, "month": S, "max": {"type": "integer"}}, ["folder"]),
    tool("accountant_usage", "Uses and last use per skill from the ledger.", {}),
    tool("accountant_problems", "Problems recorded in the ledger, with repeated ones flagged.", {"skill": S, "party": S}),
    tool("accountant_check", "Integrity check of the memory: dangling ids, unread documents, duplicate parties, missing index lines.", {}),
    tool("accountant_map", "Write a map.html of one party or one period (or everything, capped).", {"party": S, "period": S, "out": S}),
]


def call(name, a):
    ctx = g.Ctx(a.get("root"), a.get("client"))
    if name == "accountant_init":
        return g.init(ctx)
    if name == "accountant_find":
        return g.fmt_hits(g.find(ctx, a["query"], int(a.get("limit") or 20), a.get("files_dir")))
    if name == "accountant_neighbors":
        return g.neighbors(ctx, a["ref"])
    if name == "accountant_trace":
        return g.trace(ctx, a["ref"])
    if name == "accountant_impact":
        return g.impact(ctx, a["ref"])
    if name == "accountant_path":
        return g.path(ctx, a["a"], a["b"])
    if name == "accountant_job":
        return "บันทึกงาน " + g.write_job(ctx, a["job"])
    if name == "accountant_register_doc":
        return g.register_doc(ctx, a.get("kind", "other"), a.get("where", ""), a.get("title", ""), a.get("period", ""),
                              a.get("parties") or [], a.get("numbers") or [], a.get("topics") or [])
    if name == "accountant_party":
        return g.add_entry(ctx, "P", a["name"], {"role": a.get("role") or "vendor"}, a.get("aka") or [])
    if name == "accountant_lesson":
        return g.lesson(ctx, a["skill"], a["text"])
    if name == "accountant_index_scan":
        return g.index_scan(ctx, a["folder"], a.get("month"), int(a.get("max") or 200))
    if name == "accountant_usage":
        return g.usage(ctx)
    if name == "accountant_problems":
        return g.problems(ctx, a.get("skill"), a.get("party"))
    if name == "accountant_check":
        issues = g.check(ctx)
        return "memory is consistent" if not issues else "%d finding(s):\n%s" % (len(issues), "\n".join("  - " + i for i in issues))
    if name == "accountant_map":
        return g.build_map(ctx, a.get("party"), a.get("period"), a.get("out"))
    raise g.GraphError("unknown tool %s" % name)


def handle(msg):
    """One JSON-RPC message -> a response dict, or None for a notification."""
    mid, method = msg.get("id"), msg.get("method")
    if method == "initialize":
        ver = (msg.get("params") or {}).get("protocolVersion") or "2024-11-05"
        return {"jsonrpc": "2.0", "id": mid, "result": {"protocolVersion": ver, "capabilities": {"tools": {}},
                                                       "serverInfo": {"name": "accountant-graph", "version": g.VERSION}}}
    if method == "ping":
        return {"jsonrpc": "2.0", "id": mid, "result": {}}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": mid, "result": {"tools": TOOLS}}
    if method == "tools/call":
        p = msg.get("params") or {}
        try:
            text, err = call(p.get("name", ""), p.get("arguments") or {}), False
        except g.GraphError as e:
            text, err = "error: %s" % e, True
        except (KeyError, ValueError, TypeError) as e:
            text, err = "error: bad arguments (%s)" % e, True
        return {"jsonrpc": "2.0", "id": mid, "result": {"content": [{"type": "text", "text": text}], "isError": err}}
    if mid is None:
        return None
    return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": "method not found: %s" % method}}


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            resp = handle(json.loads(line))
        except Exception as e:  # keep serving
            resp = {"jsonrpc": "2.0", "id": None, "error": {"code": -32603, "message": str(e)}}
        if resp is not None:
            sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    main()
