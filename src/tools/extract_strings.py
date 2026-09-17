"""List every visible string in the built English pages.

Input for the Italian dictionary: run this, translate what it prints, put the
pairs in tools/i18n_it.py. Text inside script/style, prices, and pure numbers
are skipped, as are the two restored pages, which are captured HTML rather than
generated and are not part of the switch.
"""
import json
import pathlib
import re
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP_PAGES = {"events/index.html", "reservation/index.html", "index-wp-legacy.html"}
BLOCK = re.compile(r"<(script|style|noscript)\b.*?</\1>", re.S | re.I)
TAG = re.compile(r"<[^>]+>")
JUNK = re.compile(r"^[\s\d\$&;#·—–\-/|.,:()]*$")


def visible_strings(html_text):
    html_text = BLOCK.sub(" ", html_text)
    out = []
    for chunk in re.split(r"<[^>]+>", html_text):
        t = re.sub(r"\s+", " ", chunk).strip()
        if not t or JUNK.match(t) or len(t) < 2:
            continue
        out.append(t)
    return out


def main():
    pages = [p for p in ROOT.rglob("index.html")
             if "wp-content" not in str(p) and "node_modules" not in str(p)]
    counts = Counter()
    for p in pages:
        rel = str(p.relative_to(ROOT))
        if rel in SKIP_PAGES or rel.startswith(("2024", "2025", "2026", "category", "blogs")):
            continue
        # only the pages this generator writes carry the new stylesheet
        text = p.read_text(errors="ignore")
        if "amami.css" not in text:
            continue
        for s in visible_strings(text):
            counts[s] += 1
    items = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    out = ROOT / "tools" / "strings_en.json"
    out.write_text(json.dumps([{"n": n, "s": s} for s, n in items], indent=1, ensure_ascii=False))
    print(f"{len(items)} distinct strings across the generated pages -> {out.relative_to(ROOT)}")
    print(f"{sum(len(s.split()) for s, _ in items)} words total")


if __name__ == "__main__":
    main()
