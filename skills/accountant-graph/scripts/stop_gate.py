#!/usr/bin/env python3
"""Stop hook: do not let a finished accounting job end without its ledger entry.

Reads the hook payload on stdin. When the assistant's last turn reported a job result
(the three-part report: ผลลัพธ์ / หลักฐาน) inside a work folder that has Accountant/, and no
ledger entry was written in that turn, it blocks once with the reason. It never blocks twice
(stop_hook_active), outside an accountant work folder, or when anything is unclear (fail open).
Standard library only.
"""
import json
import os
import sys

REPORT = ("ผลลัพธ์", "หลักฐาน")
WRITTEN = ("บันทึกงาน J-", "accountant_job", "graph.py job", "graph.py\" job", "graph.py' job")
REASON = ("Write the job ledger entry before stopping: call the accountant_job tool (or "
          "python3 graph.py job FILE) with the files (sheet and range), email subjects, formulas, "
          "checks and problems of this job, then say บันทึกงาน J-id. If this was not an accounting job, say so in one line.")


def has_work_folder(cwd):
    cur = os.path.abspath(cwd or os.getcwd())
    while True:
        if os.path.isdir(os.path.join(cur, "Accountant")):
            return True
        parent = os.path.dirname(cur)
        if parent == cur:
            return False
        cur = parent


def is_prompt(entry):
    msg = entry.get("message") or {}
    if entry.get("type") != "user" and msg.get("role") != "user":
        return False
    content = msg.get("content")
    if isinstance(content, str):
        return True
    return any(isinstance(b, dict) and b.get("type") == "text" for b in (content or []))


def last_turn(lines):
    entries = []
    for line in lines:
        try:
            entries.append(json.loads(line))
        except ValueError:
            continue
    start = 0
    for i, e in enumerate(entries):
        if is_prompt(e):
            start = i + 1
    return entries[start:]


def decide(payload, transcript_lines=None):
    """Return the block reason, or None to allow."""
    if payload.get("stop_hook_active"):
        return None
    if not has_work_folder(payload.get("cwd")):
        return None
    if transcript_lines is None:
        path = payload.get("transcript_path")
        if not path or not os.path.exists(path):
            return None
        with open(path, encoding="utf-8", errors="ignore") as f:
            transcript_lines = f.read().splitlines()
    turn = last_turn(transcript_lines)
    text = json.dumps(turn, ensure_ascii=False)
    if not all(w in text for w in REPORT):
        return None
    if any(w in text for w in WRITTEN):
        return None
    return REASON


def main():
    try:
        payload = json.load(sys.stdin)
        reason = decide(payload)
        if reason:
            print(json.dumps({"decision": "block", "reason": reason}, ensure_ascii=False))
    except Exception:
        pass  # fail open: never trap the user
    return 0


if __name__ == "__main__":
    sys.exit(main())
