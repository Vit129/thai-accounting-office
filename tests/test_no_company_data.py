"""Company data never lives in this repo (NDA): no work-folder files, tracked or not.

build.sh copies the working tree, so an untracked Accountant/ would ship inside the zip;
this walks the tree, not just git ls-files. Run: python3 -m unittest discover -s tests -v
"""
import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = {".git", ".tmp", "dist", ".kouen-worktrees", ".claude", "__pycache__"}
# work-folder files from skills/company-profile/references/handoff.md; a real company layer
# under companies/ (only _template/ belongs here)
FORBIDDEN = re.compile(
    r"(^|/)Accountant/"
    r"|(^|/)company-facts\.md$"
    r"|(^|/)tune-up(-week-\d+)?\.md$"
    r"|(^|/)(client-)?register\.xlsx$"
    r"|^companies/(?!_template/)"
)


def repo_files():
    for d, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in SKIP]
        for f in files:
            yield os.path.relpath(os.path.join(d, f), ROOT).replace(os.sep, "/")


class NoCompanyData(unittest.TestCase):
    def test_no_work_folder_files(self):
        found = [p for p in repo_files() if FORBIDDEN.search(p)]
        self.assertEqual(found, [], "company data in the repo; move it to the work folder")

    def test_pattern_catches_and_spares(self):
        for bad in ["Accountant/lessons/x.md", "a/Accountant/memory/i.md", "company-facts.md",
                    "tune-up-week-2.md", "register.xlsx", "companies/acme/x.md"]:
            self.assertRegex(bad, FORBIDDEN)
        for ok in ["skills/thai-accountant/SKILL.md", "skills/company-tune-up/SKILL.md",
                   "companies/_template/README.md"]:
            self.assertNotRegex(ok, FORBIDDEN)


if __name__ == "__main__":
    unittest.main()
