#!/usr/bin/env python3
"""Verify the lean site: every internal link resolves, no orphan pages, no leftover vocabulary."""
import os, re, sys
from urllib.parse import urlparse

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "x64base-lean")

# words the plan says to retire from the public surface
BANNED = ["campus", "glass-box", "substrate", "proof-gated", "Pinocchio",
          "SelfDoc", "MDO", "Master Documentation Organizer", "LMS",
          "ascent", "publication vertical", "dual-carrier", "Arctic",
          "TupTalk", "RelTalk", "SQLsel", "LabTalk", "DotTalk", "DotScript"]
ALLOW_LANE_CONTEXT = True  # "lane" appears in CSS/none; check anyway

pages, links, problems = [], [], []

for dp, _, fns in os.walk(ROOT):
    for fn in fns:
        if fn.endswith(".html"):
            pages.append(os.path.join(dp, fn))

def resolve(src, href):
    if href.startswith(("http://", "https://", "mailto:", "#")):
        return None
    path = urlparse(href).path
    if not path:
        return None
    # absolute hrefs are site-root relative (404.html is served from any path)
    base = ROOT if path.startswith("/") else os.path.dirname(src)
    target = os.path.normpath(os.path.join(base, path.lstrip("/")))
    if os.path.isdir(target):
        target = os.path.join(target, "index.html")
    elif not os.path.splitext(target)[1]:
        target = target + "/index.html" if os.path.isdir(target) else target
    return target

linked = set()
for p in pages:
    txt = open(p, encoding="utf-8").read()
    rel = os.path.relpath(p, ROOT)

    for href in re.findall(r'href="([^"]+)"', txt):
        t = resolve(p, href)
        if t is None:
            continue
        links.append((rel, href))
        if not os.path.exists(t):
            problems.append("BROKEN LINK  {}  ->  {}".format(rel, href))
        else:
            linked.add(os.path.relpath(t, ROOT))

    # Brand names are matched CASE-SENSITIVELY: "SQLsel" is the retired product
    # brand, "SQLSEL" is the engine's command verb and must stay sayable.
    CASE_SENSITIVE = {"SQLsel"}
    low = txt.lower()
    for w in BANNED:
        if w in CASE_SENSITIVE:
            if w in txt:
                n = txt.count(w)
                problems.append("VOCAB  {}  contains '{}' x{}".format(rel, w, n))
            continue
        if w.lower() in low:
            # count occurrences, report
            n = low.count(w.lower())
            problems.append("VOCAB  {}  contains '{}' x{}".format(rel, w, n))

    for tag in ["<title>", 'name="description"', "<h1"]:
        if tag not in txt:
            problems.append("META  {} missing {}".format(rel, tag))

# ---------------------------------------------------------------------------
# RETIREMENT POLARITY -- the other direction of freshness.
# engine-facts.json catches a CITED SPEC that disappears. It cannot catch prose
# that teaches a RETIRED form as if it still works: that failure has no entry
# in a list of what ships. Measured 2026-09-23: this site told readers to type
# `SQL SELECT ...` for nineteen days after the verb was reserved.
#
# Semantics are a port of x64base-site scripts/check-retirement-polarity.mjs
# (one idiom, two sites): register of retirements, a match is a finding only
# when no excuse marker sits within WINDOW lines, fixtures in the register are
# replayed first, exemptions must state a reason. Unlike the sibling this one
# FAILS the build -- the site is small enough that a false positive costs one
# reasoned exemption, and an advisory nobody reads decays.
# ---------------------------------------------------------------------------
import html as _html, json as _json
RET_WINDOW = 6
_HERE = os.path.dirname(os.path.abspath(__file__))

def page_lines(raw):
    raw = re.sub(r'(?is)<(script|style).*?</\1>', '', raw)
    raw = re.sub(r'(?i)<br\s*/?>|</(p|li|h[1-6]|pre|tr|div|td|th)>', '\n', raw)
    return _html.unescape(re.sub(r'<[^>]+>', '', raw)).split('\n')

def retirement_sweep(files_and_rels, reg):
    markers = [m.lower() for m in reg["excuse_markers"]]
    for e in reg.get("exemptions", []):
        if not e.get("reason", "").strip():
            raise SystemExit("retirements.json: exemption for {} has no reason. Refused.".format(e.get("file")))
    exempt = lambda rel, rid: any(e["file"] == rel and e["retirement"] in ("*", rid)
                                  for e in reg.get("exemptions", []))
    def excused(lines, at):
        near = "\n".join(lines[max(0, at - RET_WINDOW): at + RET_WINDOW + 1]).lower()
        return any(m in near for m in markers)
    found = []
    for path, rel in files_and_rels:
        lines = page_lines(open(path, encoding="utf-8").read())
        for r in reg["retirements"]:
            if exempt(rel, r["id"]):
                continue
            for pat in r["patterns"]:
                rx = re.compile(pat, re.I)
                for i, line in enumerate(lines):
                    if rx.search(line) and not excused(lines, i):
                        found.append("RETIRED  {}:{}  [{}, retired {}] -> use {}\n           {}".format(
                            rel, i + 1, r["id"], r["retired_on"], r["replaced_by"], line.strip()[:120]))
    return found

def retirement_selftest(reg):
    markers = [m.lower() for m in reg["excuse_markers"]]
    bad = []
    for r in reg["retirements"]:
        hits = lambda s: any(re.search(p, s, re.I) for p in r["patterns"])
        exc = lambda s: any(m in s.lower() for m in markers)
        for s in r.get("must_flag", []):
            if not (hits(s) and not exc(s)):
                bad.append("SELFTEST {} should FLAG: {}".format(r["id"], s[:90]))
        for s in r.get("must_pass", []):
            if hits(s) and not exc(s):
                bad.append("SELFTEST {} should PASS: {}".format(r["id"], s[:90]))
    return bad

_reg = _json.load(open(os.path.join(_HERE, "retirements.json"), encoding="utf-8"))
if "--sweep" in sys.argv:          # negative-test hook: sweep an arbitrary tree of .html
    d = sys.argv[sys.argv.index("--sweep") + 1]
    fs = [(os.path.join(dp, f), os.path.relpath(os.path.join(dp, f), d))
          for dp, _, fn in os.walk(d) for f in fn if f.endswith(".html")]
    out = retirement_selftest(_reg) + retirement_sweep(fs, _reg)
    print("\n".join(out) if out else "retirement sweep: clean ({} page(s))".format(len(fs)))
    sys.exit(1 if out else 0)
problems += retirement_selftest(_reg)
problems += retirement_sweep([(p, os.path.relpath(p, ROOT)) for p in pages], _reg)

ENTRY = {"index.html", "404.html"}  # reached by URL, not by link
orphans = [os.path.relpath(p, ROOT) for p in pages
           if os.path.relpath(p, ROOT) not in linked and os.path.relpath(p, ROOT) not in ENTRY]

print("pages:  {}".format(len(pages)))
print("links checked: {}".format(len(links)))
print("orphans: {}".format(orphans if orphans else "none"))
print()
if problems:
    print("PROBLEMS ({}):".format(len(problems)))
    for x in problems:
        print("  " + x)
    sys.exit(1)
print("OK -- all internal links resolve, no retired vocabulary, all pages have title/description/h1.")
print("RETIRED    {} retirement(s) swept, fixtures pass, no page teaches a retired form".format(len(_reg["retirements"])))

# FRESHNESS (advisory, loud by design): the status board restates the engine.
import json, datetime
facts = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "engine-facts.json")))
age = (datetime.date.today() - datetime.date.fromisoformat(facts["engine_date"])).days
print("FRESHNESS  facts as of engine {} ({}), {} day(s) old".format(facts["engine_sha"], facts["engine_date"], age))
if age > 30:
    print("FRESHNESS  WARNING -- older than 30 days. Regenerate engine-facts.json from the engine tree")
    print("           and re-verify the status board before publishing (AIF-107 G2).")
