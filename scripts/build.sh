#!/usr/bin/env bash
# Build the plugin: base + optional company layer -> dist/<name>[-<company>].plugin
# Usage: bash scripts/build.sh [company-slug]
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
COMPANY="${1:-}"
OUT="$ROOT/dist"; mkdir -p "$OUT"
BUILD="$(mktemp -d)"; trap 'rm -rf "$BUILD"' EXIT
rsync -a --exclude '/.git' --exclude '/companies' --exclude '/scripts' --exclude '/dist' \
      --exclude '/tests' --exclude '/.github' --exclude '/.tmp' --exclude '/.kouen-worktrees' --exclude '/.claude' --exclude '__pycache__' --exclude '*.html' --exclude 'CLAUDE.md' --exclude '.DS_Store' --exclude '.gitignore' --exclude '/.claude-plugin/marketplace.json' "$ROOT/" "$BUILD/"
# the handout embeds work-folder-CLAUDE.md; fail when its version drifts
V="$(grep -m1 '^Template version' "$ROOT/skills/company-profile/references/work-folder-CLAUDE.md")"
grep -qF "$V" "$ROOT"/*.html || { echo "error: handout html does not embed '$V'; regenerate it" >&2; exit 1; }
NAME=thai-accounting-office
if [[ -n "$COMPANY" ]]; then
  SRC="$ROOT/companies/$COMPANY"
  [[ -d "$SRC" ]] || { echo "no such company layer: $SRC" >&2; exit 1; }
  if grep -rq "<COMPANY_NAME>" "$SRC"; then echo "warning: $COMPANY still has <COMPANY_NAME> placeholders" >&2; fi
  mkdir -p "$BUILD/skills/company-profile"
  rsync -a --exclude ".DS_Store" "$SRC/company-profile/" "$BUILD/skills/company-profile/"
  [[ -d "$SRC/overrides" ]] && rsync -a --exclude '.DS_Store' --exclude '.gitkeep' "$SRC/overrides/" "$BUILD/"
  python3 - "$BUILD/.claude-plugin/plugin.json" "$COMPANY" <<'PY'
import json, sys
p, c = sys.argv[1], sys.argv[2]
d = json.load(open(p)); d["description"] = f"[{c}] " + d["description"]
json.dump(d, open(p, "w"), indent=2, ensure_ascii=False)
PY
  NAME="$NAME-$COMPANY"
fi
# Claude Desktop's uploader rejects a skill whose frontmatter description contains < or >
for f in "$BUILD"/skills/*/SKILL.md; do
  if awk '/^---$/{c++;next} c==1' "$f" | sed -E 's/: [>|][-+]?$/:/' | grep -q '[<>]'; then
    echo "error: ${f#"$BUILD"/} frontmatter has < or > (Desktop upload fails)" >&2; exit 1
  fi
done
# every skill of the base plugin ends with the learning block (a per-company layer may replace skills)
if [[ -z "$COMPANY" ]]; then
  for f in "$BUILD"/skills/*/SKILL.md; do
    grep -q '^## Learn and remember' "$f" || { echo "error: ${f#"$BUILD"/} lacks the '## Learn and remember (every job)' block" >&2; exit 1; }
  done
fi
# the graph engine: compile its scripts and run its tests when Python is available
if command -v python3 >/dev/null 2>&1; then
  python3 -m py_compile "$ROOT"/skills/accountant-graph/scripts/*.py || { echo "error: a graph script does not compile" >&2; exit 1; }
  (cd "$ROOT" && python3 -m unittest discover -s tests >/dev/null 2>&1) || { echo "error: tests/ failed (run: python3 -m unittest discover -s tests -v)" >&2; exit 1; }
  find "$ROOT" -name __pycache__ -prune -exec rm -rf {} + 2>/dev/null || true
else
  echo "warning: python3 not found; graph scripts and tests were not checked" >&2
fi
FILE="$OUT/$NAME.plugin"; rm -f "$FILE"
(cd "$BUILD" && zip -qr "$FILE" . -x "*.DS_Store")
cp "$FILE" "${FILE%.plugin}.zip"
echo "built $FILE ($(unzip -l "$FILE" | tail -1 | awk '{print $2}') files)"
