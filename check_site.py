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

# FRESHNESS (advisory, loud by design): the status board restates the engine.
import json, datetime
facts = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "engine-facts.json")))
age = (datetime.date.today() - datetime.date.fromisoformat(facts["engine_date"])).days
print("FRESHNESS  facts as of engine {} ({}), {} day(s) old".format(facts["engine_sha"], facts["engine_date"], age))
if age > 30:
    print("FRESHNESS  WARNING -- older than 30 days. Regenerate engine-facts.json from the engine tree")
    print("           and re-verify the status board before publishing (AIF-107 G2).")
