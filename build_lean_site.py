#!/usr/bin/env python3
"""
Build the x64base LEAN site.

Reads nothing from the dev tree. Emits a self-contained static site to ./x64base-lean/
Design goals: six nav items, one status board, no product storefronts, no LMS,
no methodology apparatus, plain vocabulary, and a homepage that answers four
questions in ninety seconds.
"""

import os, shutil, html, json

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "x64base-lean")

NAV = [
    ("about",    "About",         "/about/"),
    ("docs",     "Documentation", "/docs/"),
    ("status",   "Status",        "/status/"),
    ("downloads","Downloads",     "/downloads/"),
    ("schemas",  "Schemas",       "/schemas/"),
    ("contact",  "Contact",       "/contact/"),
]

# --------------------------------------------------------------------------
# STATUS DATA  — the single place growth rates live
# tiers: proven | source | beta | chartered | open
# --------------------------------------------------------------------------
TIERS = {
    "proven":    ("Runtime-proven",  "A regression or transcript shows it. Evidence names the spec and whether it is in the default suite (re-proven on every REGRESSION ALL) or an explicit run."),
    "source":    ("Source-evidenced","The mechanism is confirmed in source; the end-to-end run has not happened."),
    "beta":      ("Active beta",     "Usable and exercised, still changing."),
    "chartered": ("Chartered",       "Designed and registered, not yet built."),
    "open":      ("Not started",     "Named here so its absence is visible."),
}

# --------------------------------------------------------------------------
# ENGINE FACTS -- a snapshot of the engine's own regression registry
# (kRegressionSpecs in src/cli/cmd_regression.cpp, via
# tools/reports/regression_index.py). Every REGRESSION a status row cites is
# looked up here; a spec the engine renamed or dropped FAILS THE BUILD rather
# than shipping a claim with nothing behind it. Refresh by regenerating
# engine-facts.json from the engine tree -- never hand-edit a spec state.
# --------------------------------------------------------------------------
import json as _json
FACTS = _json.loads(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                      "engine-facts.json"), encoding="utf-8").read())
ENGINE_SHA = FACTS["engine_sha"]
ENGINE_DATE = FACTS["engine_date"]

def ev(*specs, extra=None):
    parts = []
    for s in specs:
        state = FACTS["specs"].get(s)
        if state is None:
            raise SystemExit("STATUS cites REGRESSION %s, which is not in engine-facts.json "
                             "(engine %s). The engine renamed or dropped it: re-verify the "
                             "claim before rebuilding." % (s, ENGINE_SHA))
        parts.append("%s (%s)" % (s, "default suite" if state == "default" else "explicit run"))
    out = "REGRESSION " + ", ".join(parts) if parts else ""
    if extra:
        out = (out + "; " + extra) if out else extra
    return out

STATUS = [
 ("Storage", "Three DBF flavors, one binary", "proven",
  "Classic x32 DBF, Visual FoxPro DBF, and the x64 DBF_64 format all open in the same runtime. Flavor is a property of the table, not of the build.",
  ev("INDEX_X32", "INDEX_X64", extra="teaching datasets in all three formats")),
 ("Storage", "Past the classic 16-bit limits", "proven",
  "x64 tables carry 64-bit record-count and geometry fields, and a canary drives them past the record and header limits the classic format imposed.",
  ev("X64_METRICS")),
 ("Storage", "64-bit widening of every shared path", "source",
  "Not every shared runtime path has been audited and widened yet; the work proceeds path by path.",
  "DBF_64 reference; capacity matrix"),
 ("Storage", "Payload-agnostic memos", "proven",
  "x64 memos do not inspect what they store, and a seeded stress harness proves it: six chaotic operation patterns, payloads including embedded NUL and high bytes, byte-compared against a shadow model every generation across repeated close/reopen cycles.",
  "memo_zoo harness: 20,500 generations / 104,044 ops / 4 seeds / 0 divergences, 2026-08-11"),
 ("Storage", "Memo-resident mini-databases", "proven",
  "WORKSPACE SAVE ... MEMO MINIDB writes a whole small database into a memo container, and a workspace can be restored from it. Mixing it with multiple open workspaces is in the default suite.",
  ev("WORKSPACE_MINIDB", "MWXSHAKE")),
 ("Storage", "NULL values", "proven",
  "A nullable Visual FoxPro column stores, reads, displays, and filters NULL, and every step is graded.",
  ev("NULLASSERT")),

 ("Indexing", "CDX with an LMDB-backed key store", "proven",
  "The x64-generation index. v64 tables take their active order from CDX/LMDB, on a fixture the spec builds itself.",
  ev("INDEX_X64")),
 ("Indexing", "INX and CNX classic-generation indexes", "proven",
  "The classic index containers, with flavor-correct ordering and attachment.",
  ev("INDEX_X32")),
 ("Indexing", "CNX attached to an x64 table", "proven",
  "Cross-generation attachment is policy, not accident: permitted with an advisory, with REINDEX routing correctly and the CDX default unchanged.",
  ev("INDEX_X64_CNX")),
 ("Indexing", "CDX attached to a classic table", "chartered",
  "The mirror direction. Registered, awaiting its proof.",
  "-"),
 ("Indexing", "Index maintenance inside a transaction", "proven",
  "With SET INDEXTXN, buffered REPLACE and DELETE followed by COMMIT keep the live CDX/LMDB index current with no rebuild.",
  ev("INDEX_TXN")),

 ("Memory", "Whole tables and indexes in RAM", "proven",
  "An in-process virtual disk hosts complete x64 tables and their native CDX indexes with zero files on disk; a saved workspace can be hydrated into it.",
  ev("MEM", "WORKSPACE_RAM")),

 ("Query", "The SELECT statement surface", "proven",
  "SQLSEL runs SELECT over open work areas -- selection, projection, WHERE, ORDER BY, LIMIT, COUNT(*) -- and each result set is checked against an in-process SQLite referee.",
  ev("SQLSEL_SELECT_V1", "EVALDIFF")),
 ("Query", "Inner, outer, and cross joins", "proven",
  "INNER, LEFT, RIGHT, FULL, and CROSS joins over open tables, compared with SQLite as multisets. The proofs assert the path the query took as well as the answer.",
  ev("SQLSEL_INNER_JOIN", "SQLSEL_JOIN_EDGES", "SQLSEL_LEFT_JOIN", "SQLSEL_JOIN_FAMILY")),
 ("Query", "Self-joins and join chains", "proven",
  "Self-join aliases over one table, compound ON conditions, and three-table INNER/LEFT chains.",
  ev("SQLSEL_ADVANCED_JOIN")),
 ("Query", "GROUP BY, HAVING, and aggregates", "proven",
  "COUNT, SUM, AVG, MIN, and MAX over single tables and joins, compared with SQLite.",
  ev("SQLSEL_AGGREGATES")),
 ("Query", "Subqueries", "proven",
  "Scalar, IN, NOT IN, EXISTS, and NOT EXISTS subqueries, correlated and uncorrelated, compared with SQLite.",
  ev("SQLSEL_SUBQUERIES")),
 ("Query", "DISTINCT and set operations", "proven",
  "SELECT DISTINCT, UNION, UNION ALL, INTERSECT, and EXCEPT, compared with SQLite.",
  ev("SQLSEL_SET_OPS")),
 ("Query", "INSERT, UPDATE, and DELETE", "proven",
  "Data changes through SQLSEL over the house table buffer and write-ahead log, including changes that span tables in one transaction, compared with SQLite.",
  ev("SQLSEL_DML")),
 ("Query", "Parallel read-only scans", "proven",
  "SET PARALLEL partitions a read-only scan; a differential spec checks the parallel answer against the serial one.",
  ev("SQLSEL_PARALLEL")),
 ("Query", "Primary keys", "proven",
  "SET UNIQUE FIELD ... PRIMARY declares a key, a blank key field is generated on APPEND, and the declaration survives a restart. Enforcement is being extended one write path at a time; the policy spec records which paths hold today.",
  ev("PKPOLICY", "PKDURABLE", "PKEYS")),

 ("Relations and workspaces", "Positional relation traversal", "proven",
  "Classic SET RELATION navigation over a declared relation graph, with the relation store scoped to its workspace.",
  ev("RELSCOPE2", "CASCADE_ENV")),
 ("Relations and workspaces", "Joining a parent and its children into tuples", "proven",
  "REL JOIN walks a declared parent and its children and emits one tuple per combination, with DISTINCT, ALL and a scan limit that reports when it truncates. REL JOIN ONE keeps the historical single-row form and refuses a child chain rather than accepting one it cannot walk.",
  ev("RELJOIN", extra="main/rel_join_enum_regression.dts, 12 tests")),
 ("Relations and workspaces", "Two walkers, one answer", "proven",
  "Positional traversal and the set-oriented SELECT answered the same question over a 34-table schema with 58 foreign-key relations -- and agreed, down to the record.",
  ev("CASCADE_ENV", extra="both walkers, 2026-08-10")),
 ("Relations and workspaces", "Whole-database posture from one file", "proven",
  "WORKSPACE SAVE captures open areas, attached indexes, orders, aliases, and declared relations to a plain-text snapshot; WORKSPACE LOAD restores it. Demonstrated 2026-08-10 on a 43-area, 58-relation schema.",
  ev("CASCADE_ENV", extra="workspaces/cascade_all.dtschema")),
 ("Relations and workspaces", "Several workspaces at once", "proven",
  "Multiple workspaces open side by side, each owning its areas, its path environment, and a scoped CLOSE.",
  ev("WSMULTI", "WSENV", "WORKSPACE_SCOPE")),

 ("Shell", "Command surface over work areas", "proven",
  "Tables, areas, structure inspection, navigation, seeking, filtering, and cursor control.",
  ev("NONDESTRUCTIVE")),
 ("Shell", "Buffered editing, commit, and rollback", "proven",
  "Buffered edits under record locking; COMMIT applies a logged change and ROLLBACK discards one.",
  ev("WAL_COMMIT_ROLLBACK")),
 ("Shell", "Script mode", "beta",
  "Command files with variables, comments, line continuation, IF/ELSE, LOOP, WHILE, UNTIL, SCAN, and one level of subscript nesting.",
  "Script language guide"),
 ("Shell", "CSV import and export", "beta",
  "Round-trip between delimited files and DBF tables.",
  "Command catalog"),
 ("Shell", "DDL schema fetch, validate, create", "beta",
  "Schema surfaces over DBF, with implementation caveats documented rather than smoothed over.",
  "Command catalog; documented caveats"),
 ("Shell", "Localized command messages", "proven",
  "Command usage renders in Spanish, French, German, and Italian.",
  ev("LANGUAGE")),
 ("Shell", "SQLite as a companion carrier", "proven",
  "SQLite is compiled in both as a second carrier and as the referee for the SELECT surface. Competing with it and using it as referee are the same decision.",
  ev("SQLSEL_SELECT_V1", extra="ERP CHECK scorecards")),

 ("Architecture", "Separate libraries, separate responsibilities", "source",
  "Tables, indexes, memo storage, the expression evaluator, the value system, and the TUI link as distinct libraries under one command host. Every seam is a real compilation boundary, checkable in one build log.",
  "CMake target list in any build transcript"),
 ("Architecture", "Engine core independent of any front end", "source",
  "Ordering, cursor state, relations, validation, and command execution live in the engine and the shell, never duplicated in interface code.",
  "Architecture reference"),

 ("Interfaces", "Terminal shell", "proven",
  "The primary surface, and the one everything else is measured against.",
  ev("NONDESTRUCTIVE")),
 ("Interfaces", "TUI workbench", "beta",
  "A full-screen text interface over the same engine truth.",
  "Build targets"),
 ("Interfaces", "wxWidgets GUI workbench", "beta",
  "The C++ desktop surface. Runs, still moving.",
  "Build targets"),
 ("Interfaces", "Interface definition language", "chartered",
  "Menus, windows, dialogs, controls, and event handlers described as data.",
  "-"),

 ("Teaching", "Labs and teaching commands", "beta",
  "Hands-on surfaces for character encoding, index internals, historical data models, and normalization -- meant to be watched, not just run.",
  "Command catalog"),
 ("Teaching", "Teaching datasets", "proven",
  "The same datasets ship in x64, x32, and Visual FoxPro form, plus a reference copy, so a lesson can compare flavors directly.",
  "Repository datasets"),
 ("Teaching", "Lesson modules as portable units", "chartered",
  "A lesson travelling as a self-contained package. Designed; not built.",
  "-"),

 ("Distribution", "Cross-platform build", "proven",
  "Clean-clone builds pass on Ubuntu/GCC and Windows/MSVC in GitHub CI; WSL builds run the same source.",
  "GitHub CI green at main 78f95ce2c, 2026-08-10 (AIF-104)"),
 ("Distribution", "Tagged release with binaries", "open",
  "No release has been published (checked 2026-09-23). Until one is, building from source is the only way to run x64base.",
  "-"),
 ("Distribution", "Final license text", "source",
  "GPL-3.0-only. The LICENSE file is committed to the development tree.",
  "commit 2dbc29c8f, 2026-08-11"),
]

FAMILIES = [
 ("Tables and work areas", "USE SELECT AREA DBAREA DBAREAS STRUCT FIELDS",
  "Open a table into a numbered area, inspect its structure, and move between areas."),
 ("Navigation", "TOP BOTTOM SKIP GOTO RECNO SEEK FIND LOCATE",
  "Move the cursor by position, by key, or by condition."),
 ("Order and scope", "SET INDEX / ORDER / FILTER / RELATION / PARALLEL / INDEXTXN",
  "Choose which index drives the order, restrict what is visible, declare how tables relate, and set scan and transaction behavior."),
 ("Mutation", "REPLACE CALC CALCWRITE MULTIREP COMMIT ROLLBACK",
  "Change field values under buffering, then commit or discard."),
 ("Relations and rows", "REL RELATIONS ERSATZ TUPLE TUPEXPORT WORKSPACE",
  "Walk a declared relation graph, project rows, and save or restore a whole workspace."),
 ("Listing and browsing", "LIST SMARTLIST BROWSE SMARTBROWSER SIMPLEBROWSER",
  "Read records at the terminal, from a one-line dump to a full browser. SB is a shortcut for SIMPLEBROWSER."),
 ("Query", "SQLSEL SQLITE DDL",
  "SQLSEL is the SELECT/INSERT/UPDATE/DELETE statement surface; SQLITE reaches the companion carrier. SQL itself is a reserved word and runs nothing."),
 ("Import and export", "IMPORT EXPORT IMPORTSQL EXPORTSQL COPY",
  "Move data between DBF, delimited files, and SQLite."),
 ("Help and metadata", "HELP CMDHELP CMDHELPCHK MAINT DDICT MANUAL BBOX",
  "Ask the running system what it knows about itself, including a checker for help that has drifted."),
 ("Teaching", "ASCII SHELLO RETRO IDX COBOL CODASYL NORMALIZE",
  "Labs that make a layer visible instead of describing it."),
 ("Utility", "EDIT TEXT IMAGE WEB SFTP ZIP PSHELL",
  "Ordinary conveniences so a session does not have to leave the shell."),
 ("Verification", "REGRESSION",
  "Run the engine's own registered proofs -- the same specs this site cites as evidence."),
]

# --------------------------------------------------------------------------
CSS = r"""
:root{
  --paper:#fbfaf7; --ink:#14171c; --body:#3d4551; --muted:#6d7683;
  --rule:#e6e3dc; --rule-2:#efece6; --card:#ffffff;
  --accent:#a8471a; --accent-soft:#f6ece5;
  --proven:#1c6b52; --proven-bg:#e6f2ec;
  --source:#8a5c12; --source-bg:#f8efdd;
  --beta:#2a5a8c;   --beta-bg:#e7effa;
  --chartered:#5d6470; --chartered-bg:#eeefF1;
  --open:#8a8a8a;  --open-bg:#f3f2f0;
  --serif:"Iowan Old Style","Palatino Linotype",Palatino,"Book Antiqua",Georgia,serif;
  --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,Helvetica,Arial,sans-serif;
  --mono:ui-monospace,SFMono-Regular,"SF Mono",Menlo,Consolas,"Liberation Mono",monospace;
}
@media (prefers-color-scheme: dark){
  :root{
    --paper:#101317; --ink:#f0ece5; --body:#c2c8d0; --muted:#8b939e;
    --rule:#262b32; --rule-2:#1c2026; --card:#161a20;
    --accent:#e2854f; --accent-soft:#241a13;
    --proven:#6fcfa8; --proven-bg:#12261f;
    --source:#d8a94e; --source-bg:#2a2115;
    --beta:#7db3e8;   --beta-bg:#141e2b;
    --chartered:#98a1ae; --chartered-bg:#1c2027;
    --open:#8a8f97; --open-bg:#191c21;
  }
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{
  margin:0; background:var(--paper); color:var(--body);
  font-family:var(--sans); font-size:16.5px; line-height:1.65;
  -webkit-font-smoothing:antialiased;
}
.wrap{max-width:1080px;margin:0 auto;padding:0 28px}
.prose{max-width:70ch}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline;text-underline-offset:2px}
h1,h2,h3,h4{font-family:var(--serif);color:var(--ink);line-height:1.2;font-weight:600;margin:0}
h1{font-size:clamp(2.1rem,4.6vw,3.1rem);letter-spacing:-.015em}
h2{font-size:1.62rem;letter-spacing:-.01em}
h3{font-size:1.14rem;font-family:var(--sans);font-weight:650;letter-spacing:-.005em}
p{margin:0 0 1.05em}
code,kbd{font-family:var(--mono);font-size:.87em}
hr{border:0;border-top:1px solid var(--rule);margin:0}

/* header */
header.site{position:sticky;top:0;z-index:40;background:color-mix(in srgb,var(--paper) 88%,transparent);
  backdrop-filter:saturate(150%) blur(10px);border-bottom:1px solid var(--rule)}
.bar{display:flex;align-items:center;gap:26px;height:58px}
.mark{font-family:var(--mono);font-weight:600;font-size:1rem;color:var(--ink);letter-spacing:-.02em;
  display:flex;align-items:center;gap:8px;flex:none}
.mark .dot{width:9px;height:9px;background:var(--accent);border-radius:2px;display:inline-block}
nav.top{margin-left:auto;display:flex;gap:22px;flex-wrap:wrap}
nav.top a{color:var(--muted);font-size:.895rem;font-weight:500}
nav.top a:hover{color:var(--ink);text-decoration:none}
nav.top a.on{color:var(--ink)}
nav.top a.on::after{content:"";display:block;height:2px;background:var(--accent);border-radius:2px;margin-top:3px}

/* banner */
.banner{background:var(--accent-soft);border-bottom:1px solid var(--rule)}
.banner .wrap{display:flex;gap:10px;flex-wrap:wrap;align-items:center;
  font-size:.775rem;color:var(--muted);padding-top:7px;padding-bottom:7px;font-family:var(--mono)}

/* hero */
.hero{padding:76px 0 8px}
.eyebrow{font-family:var(--mono);font-size:.72rem;letter-spacing:.14em;text-transform:uppercase;
  color:var(--muted);margin:0 0 18px}
.hero h1{max-width:19ch}
.lead{font-size:1.155rem;color:var(--body);max-width:62ch;margin:20px 0 0}
.btns{display:flex;gap:12px;flex-wrap:wrap;margin:30px 0 0}
.btn{display:inline-block;padding:10px 19px;border-radius:7px;font-size:.92rem;font-weight:600;
  border:1px solid var(--accent);color:#fff;background:var(--accent)}
.btn:hover{text-decoration:none;filter:brightness(1.07)}
.btn.ghost{background:transparent;color:var(--ink);border-color:var(--rule)}
.btn.ghost:hover{border-color:var(--muted)}

/* record-grid motif */
.motif{margin:52px 0 0;height:96px;border:1px solid var(--rule);border-radius:10px;overflow:hidden;
  background:
   repeating-linear-gradient(90deg,transparent 0 39px,var(--rule-2) 39px 40px),
   repeating-linear-gradient(0deg,transparent 0 23px,var(--rule-2) 23px 24px),
   linear-gradient(90deg,var(--accent-soft),transparent 62%);
  position:relative}
.motif::after{content:"tables → records → fields → indexes → memos → work areas → relations";
  position:absolute;left:16px;bottom:11px;font-family:var(--mono);font-size:.7rem;color:var(--muted);
  background:var(--paper);padding:2px 8px;border-radius:4px;border:1px solid var(--rule)}

/* sections */
section{padding:60px 0}
section.tight{padding:44px 0}
.sechead{display:flex;align-items:baseline;gap:14px;margin:0 0 26px;flex-wrap:wrap}
.sechead .eyebrow{margin:0}

/* grid + cards */
.grid{display:grid;gap:14px}
.g2{grid-template-columns:repeat(auto-fit,minmax(288px,1fr))}
.g3{grid-template-columns:repeat(auto-fit,minmax(232px,1fr))}
.card{background:var(--card);border:1px solid var(--rule);border-radius:10px;padding:20px 22px}
.card h3{margin:0 0 7px}
.card p{margin:0;font-size:.93rem;color:var(--muted)}
a.card{display:block;color:inherit;transition:border-color .14s ease,transform .14s ease}
a.card:hover{text-decoration:none;border-color:var(--accent);transform:translateY(-1px)}
a.card h3{color:var(--ink)}
.cmds{font-family:var(--mono);font-size:.78rem;color:var(--accent);margin:0 0 9px;
  word-spacing:.35em;line-height:1.75}

/* facts / stat strip */
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:1px;
  background:var(--rule);border:1px solid var(--rule);border-radius:10px;overflow:hidden;margin:34px 0 0}
.stat{background:var(--card);padding:17px 19px}
.stat b{display:block;font-family:var(--serif);font-size:1.72rem;color:var(--ink);line-height:1.1}
.stat span{font-size:.775rem;color:var(--muted);display:block;margin-top:4px}

/* tier chips */
.chip{display:inline-flex;align-items:center;gap:6px;font-family:var(--mono);font-size:.68rem;
  letter-spacing:.05em;text-transform:uppercase;padding:3px 9px;border-radius:999px;white-space:nowrap;font-weight:600}
.chip::before{content:"";width:6px;height:6px;border-radius:50%;background:currentColor}
.t-proven{color:var(--proven);background:var(--proven-bg)}
.t-source{color:var(--source);background:var(--source-bg)}
.t-beta{color:var(--beta);background:var(--beta-bg)}
.t-chartered{color:var(--chartered);background:var(--chartered-bg)}
.t-open{color:var(--open);background:var(--open-bg);border:1px dashed currentColor}

/* status board */
.filters{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 22px}
.filters button{font-family:var(--mono);font-size:.72rem;letter-spacing:.05em;text-transform:uppercase;
  padding:6px 13px;border-radius:999px;border:1px solid var(--rule);background:var(--card);
  color:var(--muted);cursor:pointer;font-weight:600}
.filters button[aria-pressed=true]{border-color:var(--accent);color:var(--accent);background:var(--accent-soft)}
.board{border:1px solid var(--rule);border-radius:10px;overflow:hidden;background:var(--card)}
.grp{display:flex;align-items:center;gap:12px;padding:11px 20px;background:var(--rule-2);
  border-bottom:1px solid var(--rule);border-top:1px solid var(--rule)}
.grp:first-child{border-top:0}
.grp h3{font-family:var(--mono);font-size:.73rem;letter-spacing:.13em;text-transform:uppercase;color:var(--muted)}
.row{display:grid;grid-template-columns:1fr 168px;gap:18px;padding:17px 20px;border-bottom:1px solid var(--rule-2);align-items:start}
.row:last-child{border-bottom:0}
.row h4{font-family:var(--sans);font-size:.98rem;font-weight:650;color:var(--ink);margin:0 0 5px}
.row p{margin:0;font-size:.895rem;color:var(--muted)}
.row .ev{margin-top:8px;font-family:var(--mono);font-size:.72rem;color:var(--muted);opacity:.85}
.row .ev b{font-weight:600;color:var(--body);opacity:.9}
.row .tier{text-align:right}
@media (max-width:640px){.row{grid-template-columns:1fr}.row .tier{text-align:left}}

/* legend */
.legend{display:grid;gap:9px;margin:26px 0 0;font-size:.865rem;color:var(--muted)}
.legend div{display:flex;gap:11px;align-items:baseline;flex-wrap:wrap}

/* prose lists */
ul.plain{list-style:none;padding:0;margin:0 0 1em}
ul.plain li{padding:0 0 0 20px;position:relative;margin:0 0 .55em}
ul.plain li::before{content:"";position:absolute;left:2px;top:.62em;width:6px;height:6px;
  border-radius:1px;background:var(--accent);opacity:.55}
ul.tick{list-style:none;padding:0}
ul.tick li{margin:0 0 .5em;padding-left:20px;position:relative}
ul.tick li::before{content:"—";position:absolute;left:0;color:var(--muted)}

/* callout */
.note{border-left:3px solid var(--accent);background:var(--accent-soft);
  padding:16px 20px;border-radius:0 8px 8px 0;margin:26px 0}
.note p:last-child{margin:0}
.note strong{color:var(--ink)}

/* code block */
pre{background:var(--card);border:1px solid var(--rule);border-radius:9px;padding:16px 18px;
  overflow:auto;font-family:var(--mono);font-size:.82rem;line-height:1.7;color:var(--body);margin:0 0 1.1em}

/* table */
table.t{width:100%;border-collapse:collapse;font-size:.9rem;margin:0 0 1.2em}
table.t th{text-align:left;font-family:var(--mono);font-size:.71rem;letter-spacing:.1em;
  text-transform:uppercase;color:var(--muted);padding:9px 14px 9px 0;border-bottom:1px solid var(--rule);font-weight:600}
table.t td{padding:11px 14px 11px 0;border-bottom:1px solid var(--rule-2);vertical-align:top}
table.t tr:last-child td{border-bottom:0}

/* page head */
.phead{padding:56px 0 8px;border-bottom:1px solid var(--rule)}
.phead h1{font-size:clamp(1.9rem,3.6vw,2.5rem)}
.phead p{margin:14px 0 0;color:var(--muted);max-width:64ch;font-size:1.03rem}
.crumb{font-family:var(--mono);font-size:.74rem;color:var(--muted);margin:0 0 14px}

/* footer */
footer.site{border-top:1px solid var(--rule);margin-top:40px;padding:40px 0 56px;background:var(--rule-2)}
footer .cols{display:grid;grid-template-columns:1.6fr 1fr 1fr;gap:32px}
@media (max-width:700px){footer .cols{grid-template-columns:1fr 1fr}}
footer h4{font-family:var(--mono);font-size:.71rem;letter-spacing:.12em;text-transform:uppercase;
  color:var(--muted);margin:0 0 12px;font-weight:600}
footer a{display:block;color:var(--body);font-size:.89rem;margin:0 0 7px}
footer .tag{font-size:.89rem;color:var(--muted);max-width:38ch;margin:0 0 14px}
footer .fine{margin-top:30px;padding-top:20px;border-top:1px solid var(--rule);
  font-size:.79rem;color:var(--muted);display:flex;gap:18px;flex-wrap:wrap}
"""

JS_STATUS = r"""
(function(){
  var btns=document.querySelectorAll('.filters button');
  var rows=document.querySelectorAll('.board .row');
  var grps=document.querySelectorAll('.board .grp');
  btns.forEach(function(b){
    b.addEventListener('click',function(){
      var f=b.dataset.f;
      btns.forEach(function(x){x.setAttribute('aria-pressed', x===b ? 'true':'false');});
      rows.forEach(function(r){
        r.style.display = (f==='all'||r.dataset.tier===f) ? '' : 'none';
      });
      grps.forEach(function(g){
        var n=0,el=g.nextElementSibling;
        while(el && el.classList.contains('row')){ if(el.style.display!=='none') n++; el=el.nextElementSibling; }
        g.style.display = n ? '' : 'none';
      });
    });
  });
})();
"""

def shell(title, nav_key, body, desc, depth, script=""):
    root = "../" * depth if depth else "./"
    navhtml = "".join(
        '<a href="{}{}" class="{}">{}</a>'.format(root, u.strip("/") + "/" if u != "/" else "", "on" if k == nav_key else "", n)
        for k, n, u in NAV)
    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<link rel="stylesheet" href="{root}assets/site.css">
</head>
<body>
<header class="site">
  <div class="wrap bar">
    <a class="mark" href="{root}"><span class="dot"></span>x64base</a>
    <nav class="top">{nav}</nav>
  </div>
</header>
<div class="banner"><div class="wrap">active beta -- every claim carries its evidence tier -- facts as of engine <a href="https://github.com/deraldg/x64base/commit/{esha}">{esha}</a>, {edate}</div></div>
<main>
{body}
</main>
<footer class="site">
  <div class="wrap">
    <div class="cols">
      <div>
        <div class="mark" style="margin-bottom:12px"><span class="dot"></span>x64base</div>
        <p class="tag">A 64-bit DBF database engine in C++20, with a command shell you can watch work. Born 1993, rebuilt for 2026.</p>
      </div>
      <div>
        <h4>Project</h4>
        <a href="{root}docs/">Documentation</a>
        <a href="{root}status/">Status</a>
        <a href="{root}downloads/">Downloads</a>
        <a href="{root}schemas/">Schemas</a>
      </div>
      <div>
        <h4>Elsewhere</h4>
        <a href="https://github.com/deraldg/x64base">Source on GitHub</a>
        <a href="https://x64base.com">Working archive</a>
        <a href="{root}about/">About &amp; scope</a>
        <a href="{root}contact/">Contact</a>
      </div>
    </div>
    <div class="fine">
      <span>© 1993–2026 Derald R. Grimwood Jr.</span>
      <span>GPL-3.0-only</span>
      <span>DBF_64 · FPT64 · indexing · teaching-first</span>
    </div>
  </div>
</footer>
{script}
</body>
</html>""".format(esha=ENGINE_SHA, edate=ENGINE_DATE, title=html.escape(title), desc=html.escape(desc), nav=navhtml,
                  body=body, root=root, script=script)


def chip(t):
    return '<span class="chip t-{}">{}</span>'.format(t, TIERS[t][0])


def write(path, content):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)


# ------------------------------- HOME -------------------------------------
def home():
    counts = {}
    for r in STATUS:
        counts[r[2]] = counts.get(r[2], 0) + 1

    fam = "".join(
        '<div class="card"><h3>{}</h3><p class="cmds">{}</p><p>{}</p></div>'.format(n, c, d)
        for n, c, d in FAMILIES[:6])

    highlights = [
      ("Three DBF flavors, one binary", "proven",
       "Classic, Visual FoxPro, and 64-bit tables open in the same runtime. Flavor belongs to the table, not the build."),
      ("A SELECT with an external referee", "proven",
       "Every shipped operator of the house SELECT is checked against an in-process SQLite implementation. The competition is the test harness."),
      ("Tables and indexes entirely in RAM", "proven",
       "A virtual disk builds, indexes, traverses, and tears down complete tables with zero files touched."),
      ("A database posture in one file", "proven",
       "One command restores 43 work areas, their indexes, orders, aliases, and 58 declared relations from a plain-text snapshot."),
    ]
    hi = "".join(
      '<div class="card"><div style="margin-bottom:9px">{}</div><h3>{}</h3><p>{}</p></div>'.format(chip(t), n, d)
      for n, t, d in highlights)

    body = """
<section class="hero"><div class="wrap">
  <p class="eyebrow">C++20 · DBF family · active beta</p>
  <h1>A 64-bit DBF database engine you can watch work.</h1>
  <p class="lead">x64base opens classic, Visual FoxPro, and 64-bit DBF tables; indexes them, relates them,
  and queries them — while showing you every layer it touches. The shell is the engine's front door,
  and nothing important happens where you cannot see it.</p>
  <div class="btns">
    <a class="btn" href="downloads/">Build it</a>
    <a class="btn ghost" href="status/">See exactly where it stands</a>
  </div>
  <div class="motif"></div>
  <div class="stats">
    <div class="stat"><b>%(proven)d</b><span>runtime-proven capabilities</span></div>
    <div class="stat"><b>3</b><span>DBF flavors, one binary</span></div>
    <div class="stat"><b>58</b><span>relations restored from one file</span></div>
    <div class="stat"><b>1993</b><span>lineage start</span></div>
  </div>
</div></section>

<hr>

<section><div class="wrap">
  <div class="sechead"><h2>What it does well</h2><p class="eyebrow">each with a transcript behind it</p></div>
  <div class="grid g2">%(hi)s</div>
</div></section>

<section class="tight"><div class="wrap">
  <div class="note prose">
    <p><strong>Every claim on this site carries a tier.</strong> Runtime-proven means a regression or
    transcript shows it. Source-evidenced means the mechanism is in the code but the end-to-end run
    has not happened. Chartered means designed, not built. Nothing here outranks its proof, and the
    <a href="status/">status board</a> lists the unfinished parts beside the finished ones.</p>
  </div>
</div></section>

<hr>

<section><div class="wrap">
  <div class="sechead"><h2>The command surface</h2><p class="eyebrow">one shell, grouped by job</p></div>
  <div class="grid g3">%(fam)s</div>
  <p style="margin-top:18px"><a href="docs/command-families/">All eleven command families →</a></p>
</div></section>

<hr>

<section><div class="wrap prose">
  <div class="sechead"><h2>Who it is for</h2></div>
  <p>Two audiences, and no others. <strong>Developers</strong> who work with DBF-family data and want an
  engine whose internals are legible rather than sealed. <strong>Educators</strong> who want to teach
  database fundamentals on a system where indexes, memos, work areas, and relations are visible
  moving parts instead of diagrams.</p>
  <p>It is not for sale, not a hosted service, and not a student portal. It is not a finished commercial
  DBMS, a Visual FoxPro clone, or a drop-in replacement for Harbour or Xbase++. What it is, precisely,
  is on the <a href="about/">About</a> page.</p>
  <p style="color:var(--muted);font-size:.93rem;margin-top:26px">Looking for design notes, historical
  source inventories, or the day-to-day development record? Those live in the
  <a href="https://x64base.com">working archive</a>, which is kept for the project's own use and is
  considerably less tidy than this.</p>
</div></section>
""" % dict(proven=counts.get("proven", 0), hi=hi, fam=fam)
    write("index.html", shell("x64base — a 64-bit DBF engine in C++20", "", body,
          "A 64-bit DBF database engine in C++20 with an inspectable command shell. Active beta; every claim carries its evidence tier.", 0))


# ------------------------------ STATUS ------------------------------------
def status():
    # Group order is DERIVED from STATUS (first appearance). A hard-coded list
    # here once dropped every row whose group it did not name -- silently.
    order = list(dict.fromkeys(r[0] for r in STATUS))
    counts = {}
    for r in STATUS:
        counts[r[2]] = counts.get(r[2], 0) + 1

    board = []
    for g in order:
        rows = [r for r in STATUS if r[0] == g]
        if not rows:
            continue
        board.append('<div class="grp"><h3>{}</h3></div>'.format(g))
        for _, name, tier, what, ev in rows:
            board.append(
              '<div class="row" data-tier="{t}">'
              '<div><h4>{n}</h4><p>{w}</p><p class="ev"><b>Evidence:</b> {e}</p></div>'
              '<div class="tier">{c}</div></div>'.format(t=tier, n=name, w=what, e=ev, c=chip(tier)))

    rendered = sum(1 for b in board if b.startswith('<div class="row"'))
    if rendered != len(STATUS):
        raise SystemExit("status board rendered %d of %d STATUS rows" % (rendered, len(STATUS)))
    filt = ['<button data-f="all" aria-pressed="true">Everything ({})</button>'.format(len(STATUS))]
    for k in ["proven", "source", "beta", "chartered", "open"]:
        if counts.get(k):
            filt.append('<button data-f="{}" aria-pressed="false">{} ({})</button>'.format(k, TIERS[k][0], counts[k]))

    legend = "".join('<div>{} <span>{}</span></div>'.format(chip(k), TIERS[k][1])
                     for k in ["proven", "source", "beta", "chartered", "open"])

    body = """
<div class="phead"><div class="wrap">
  <p class="crumb">Home / Status</p>
  <h1>Where every part actually stands.</h1>
  <p>Each area of x64base grows at its own rate, and this is the only page where those rates live.
  Entries are promoted when their evidence exists and demoted the day it stops holding. Work that has
  not started is listed too — an absence you cannot see is a claim by omission.</p>
</div></div>

<section><div class="wrap">
  <div class="stats" style="margin:0 0 30px">
    <div class="stat"><b>%(p)d</b><span>runtime-proven</span></div>
    <div class="stat"><b>%(s)d</b><span>source-evidenced</span></div>
    <div class="stat"><b>%(b)d</b><span>active beta</span></div>
    <div class="stat"><b>%(c)d</b><span>chartered</span></div>
    <div class="stat"><b>%(o)d</b><span>not started</span></div>
  </div>
  <div class="filters">%(filt)s</div>
  <div class="board">%(board)s</div>
  <div class="legend">%(legend)s</div>
</div></section>
""" % dict(p=counts.get("proven", 0), s=counts.get("source", 0), b=counts.get("beta", 0),
           c=counts.get("chartered", 0), o=counts.get("open", 0),
           filt="".join(filt), board="".join(board), legend=legend)
    write("status/index.html", shell("Status — x64base", "status", body,
          "Every area of x64base against its evidence tier, including the work that has not started.",
          1, script="<script>{}</script>".format(JS_STATUS)))


# ------------------------------- DOCS -------------------------------------
def docs():
    cards = [
      ("Getting started", "docs/getting-started/", "Build the engine, open a table, and run your first ordered read."),
      ("Command families", "docs/command-families/", "The whole shell surface, grouped by the job it does."),
      ("Engine architecture", "docs/architecture/", "Libraries, seams, and why the front end never owns the truth."),
      ("Storage formats", "docs/formats/", "DBF_64 and FPT64: headers, geometry, 64-bit memo identifiers."),
      ("Indexing", "docs/indexing/", "CDX, CNX, INX, the LMDB key store, and cross-generation attachment policy."),
      ("Query and relations", "docs/query/", "The house SELECT, its SQLite oracle, and two ways to walk one graph."),
      ("Script mode", "docs/scripting/", "Command files, variables, conditionals, loops, and scans."),
      ("Teaching material", "docs/teaching/", "Labs that make a layer visible instead of describing it."),
      ("Ecosystem context", "docs/ecosystem/", "Where x64base sits beside Harbour, Xbase++, XSharp, and dBASE tools."),
    ]
    g = "".join('<a class="card" href="{}"><h3>{}</h3><p>{}</p></a>'.format(u[5:], n, d) for n, u, d in cards)
    body = """
<div class="phead"><div class="wrap">
  <p class="crumb">Home / Documentation</p>
  <h1>Documentation</h1>
  <p>Written for two readers: someone who wants to build and run the engine, and someone who wants to
  teach with it. Every page carries the evidence tier of what it describes.</p>
</div></div>
<section><div class="wrap"><div class="grid g2">%s</div></div></section>
""" % g
    write("docs/index.html", shell("Documentation — x64base", "docs", body,
          "Documentation for the x64base engine and its command shell.", 1))


def doc_page(slug, title, lead, body_html):
    body = """
<div class="phead"><div class="wrap">
  <p class="crumb"><a href="../">Documentation</a> / {t}</p>
  <h1>{t}</h1>
  <p>{l}</p>
</div></div>
<section><div class="wrap prose">{b}</div></section>
""".format(t=html.escape(title), l=lead, b=body_html)
    write("docs/{}/index.html".format(slug), shell(title + " — x64base", "docs", body, lead, 2))


def sub_pages():
    # getting started
    doc_page("getting-started", "Getting started",
      "Build the engine, create a table, and query it -- using the same steps the engine's own regression runs.",
      """
<h2>Requirements</h2>
<ul class="plain">
<li>A C++20 compiler -- MSVC on Windows, or GCC/Clang on Linux and WSL</li>
<li>CMake 3.21 or newer</li>
<li>vcpkg, for dependency resolution (manifest is committed)</li>
</ul>
<h2>Build</h2>
<pre>git clone https://github.com/deraldg/x64base
cd x64base
cmake --preset default
cmake --build --preset default</pre>
<p>The result is a single command host. The engine libraries link into it; there is no separate
daemon or service to start. Clean-clone builds of the core pass in GitHub CI on Ubuntu/GCC and
Windows/MSVC. No tagged release with binaries exists yet -- see the
<a href="../../status/">status board</a>.</p>

<h2>First session</h2>
<p>This builds its own table, so it works on an empty data directory. The lines are taken from
<code>sqlsel_select_v1_regression.dts</code>, a default-suite spec the engine re-runs on every
<code>REGRESSION ALL</code>.</p>
<pre>CREATE X64 SQLSTU (SID N(6,0), LNAME C(12), MAJOR C(4))
APPEND
REPLACE SID WITH "1"
REPLACE LNAME WITH "ADAMS"
REPLACE MAJOR WITH "CSCI"
APPEND
REPLACE SID WITH "2"
REPLACE LNAME WITH "BAKER"
REPLACE MAJOR WITH "MATH"
CLOSE
USE SQLSTU
STRUCT
LIST</pre>
<p>Create a 64-bit table, append two records, close it, reopen it into a work area, look at its
structure, and read it back. Each is a separate, observable step -- which is the point of the
shell.</p>

<h2>Then query it</h2>
<pre>SQLSEL SELECT SID,LNAME FROM SQLSTU WHERE MAJOR = "CSCI"
SQLSEL SELECT SID,LNAME FROM SQLSTU ORDER BY LNAME DESC
SQLSEL SELECT COUNT(*) FROM SQLSTU</pre>
<p><code>SQLSEL</code> is the statement surface. The word <code>SQL</code> on its own is reserved
and runs nothing. Joins, grouping, subqueries, set operations, and INSERT/UPDATE/DELETE use the
same verb; see <a href="../query/">Query and relations</a>.</p>

<h2>Check it yourself</h2>
<pre>REGRESSION RUN SQLSEL_SELECT_V1</pre>
<p>Every runtime-proven claim on this site names a spec like this one. If one fails on your
machine, that is worth <a href="../../contact/">reporting</a>.</p>
""")

    # command families
    rows = "".join(
      '<div class="card"><h3>{}</h3><p class="cmds">{}</p><p>{}</p></div>'.format(n, c, d)
      for n, c, d in FAMILIES)
    doc_page("command-families", "Command families",
      "One shell, grouped by the job each group of commands does.",
      """
<p>x64base is one engine with one shell. The names below are groupings for readability, not separate
products — nothing here is downloaded, versioned, or licensed on its own.</p>
<div class="grid g2" style="margin:26px 0">{rows}</div>
<p>The shell can also answer questions about itself at runtime: <code>HELP</code> and
<code>CMDHELP</code> describe commands, <code>DDICT</code> reports metadata, and
<code>CMDHELPCHK</code> checks help text that has drifted away from the code it documents.</p>
""".format(rows=rows))

    # architecture
    doc_page("architecture", "Engine architecture",
      "Separate libraries, real compilation boundaries, and a front end that owns nothing.",
      """
<h2>Layers</h2>
<table class="t">
<tr><th>Library</th><th>Responsibility</th></tr>
<tr><td><code>xbase</code></td><td>Table runtime, work-area objects, records, cursor state, field metadata, table flavors</td></tr>
<tr><td><code>xindex</code></td><td>Index containers, tag and order behavior, backend index work</td></tr>
<tr><td><code>memo</code></td><td>Memo references, managers, objects, stores, verification</td></tr>
<tr><td><code>xexpr</code></td><td>Expression evaluation</td></tr>
<tr><td><code>value</code></td><td>The shell's value system</td></tr>
<tr><td><code>tui</code></td><td>Full-screen text interface</td></tr>
</table>
<p>These are not conceptual layers. Each is a separate link target, and the boundaries between them
are checkable in a single build log. {c}</p>
<h2>The execution chain</h2>
<pre>main → shell → command registry → one translation unit per command → libraries</pre>
<h2>The front end owns nothing</h2>
<p>Ordering, cursor state, relations, validation, and command execution live in the engine and the
shell. Terminal, text-mode, and desktop surfaces are consumers of that truth, never duplicators of it.
A front end can be added or removed without the database behaving differently. {c2}</p>
<h2>The working rule</h2>
<pre>Conventions suggest.
Registration declares.
Metadata records.
Runtime proves.
Validators enforce.</pre>
""".format(c=chip("source"), c2=chip("source")))

    # formats
    doc_page("formats", "Storage formats",
      "DBF_64 and FPT64 — what widened, what did not, and where the gates still are.",
      """
<h2>Three flavors, one runtime</h2>
<p>{c} The same binary opens classic MS-DOS-era DBF, Visual FoxPro DBF, and the x64 <code>DBF_64</code>
format. Flavor is a property of the table on disk, not a compile-time choice. The teaching datasets
ship in all three plus a reference copy, so a lesson can put them side by side.</p>
<h2>What x64 actually widened</h2>
<ul class="plain">
<li>Table headers carry 64-bit record-count and geometry fields</li>
<li>Memos use 64-bit object identifiers and offsets</li>
<li>Metadata supports richer table and field names, with classic descriptor fallback tokens preserved</li>
</ul>
<div class="note"><p><strong>What has not been widened yet.</strong> Some shared runtime paths still
carry compatibility gates that must be audited one at a time, and each index backend needs its own
audit for true 64-bit record payloads and offsets. x64base does not claim every command path is
unlimited. {s}</p></div>
<h2>Memos</h2>
<p>{s2} Memo storage is payload-agnostic by design: the memo layer addresses objects by 64-bit
identifier and does not inspect what they contain. The destination built on that has landed: {pr}
<code>WORKSPACE SAVE ... MEMO MINIDB</code> writes an entire small database into a memo container,
and a workspace can be restored from it.</p>
""".format(c=chip("proven"), s=chip("source"), s2=chip("source"), pr=chip("proven")))

    # indexing
    doc_page("indexing", "Indexing",
      "An index family, not an index — and a policy for mixing generations.",
      """
<p>x64base carries several index containers rather than one, and publishes the attach, rebuild, order,
seek, and verification seams as architecture instead of sealed internals.</p>
<table class="t">
<tr><th>Container</th><th>Generation</th><th>Status</th></tr>
<tr><td><code>INX</code></td><td>Classic</td><td>{p}</td></tr>
<tr><td><code>CNX</code></td><td>Classic</td><td>{p}</td></tr>
<tr><td><code>CDX</code> with an LMDB key store</td><td>x64</td><td>{p}</td></tr>
</table>
<h2>Cross-generation attachment is policy</h2>
<p>{p} A classic <code>CNX</code> may be explicitly attached to an x64 table, with an advisory. Rebuild
routing follows correctly and the <code>CDX</code> default is unchanged. This is a decision the engine
makes deliberately, not an accident of permissiveness.</p>
<p>{ch} The mirror direction — <code>CDX</code> on a classic table — is registered and awaiting its
proof. It is not claimed until a regression shows it.</p>
<h2>Indexes in memory</h2>
<p>{p} The in-process virtual disk hosts complete x64 tables <em>and their native CDX indexes</em> with
zero files on disk: created, indexed, read back in order, and torn down entirely in RAM.</p>
""".format(p=chip("proven"), ch=chip("chartered")))

    # query
    doc_page("query", "Query and relations",
      "One statement surface, checked against SQLite at every step, and two ways to walk a relation graph.",
      """
<h2>SQLSEL, and what it covers</h2>
<p>{p} <code>SQLSEL</code> runs SELECT over open work areas: selection, projection, WHERE,
ORDER BY, LIMIT, and COUNT(*). The word <code>SQL</code> on its own is reserved and runs nothing.</p>
<table class="t">
<tr><th>Capability</th><th>Proof</th></tr>
<tr><td>SELECT, WHERE, ORDER BY, LIMIT, COUNT(*)</td><td>{p} default suite</td></tr>
<tr><td>INNER, LEFT, RIGHT, FULL, CROSS joins</td><td>{p} default suite</td></tr>
<tr><td>Self-joins, compound ON, three-table chains</td><td>{p} explicit run</td></tr>
<tr><td>GROUP BY, HAVING, COUNT/SUM/AVG/MIN/MAX</td><td>{p} explicit run</td></tr>
<tr><td>Scalar, IN, EXISTS subqueries, correlated or not</td><td>{p} explicit run</td></tr>
<tr><td>DISTINCT, UNION, UNION ALL, INTERSECT, EXCEPT</td><td>{p} explicit run</td></tr>
<tr><td>INSERT, UPDATE, DELETE, cross-table transactions</td><td>{p} explicit run</td></tr>
<tr><td>SET PARALLEL partitioned read-only scans</td><td>{p} default suite</td></tr>
</table>
<p>Default suite means the engine re-proves it on every <code>REGRESSION ALL</code>. Explicit run
means a registered spec proves it on demand while it waits for soak and review. Spec names are on
the <a href="../../status/">status board</a>.</p>

<h2>The referee</h2>
<p>Each of those specs compares SQLSEL's row sets with an in-process SQLite implementation.
SQLite is compiled in both as a companion carrier and as the referee: competing with it and
testing against it are the same decision, made on purpose. The join proofs also assert the path
the query took, not only the answer it returned.</p>

<h2>One graph, two walkers</h2>
<p>{p} A declared relation graph can be walked positionally -- the child cursor follows the
parent, classic <code>SET RELATION</code> -- or as a set through SQLSEL. On 2026-08-10 both
answered the same question over a 34-table schema with 58 foreign-key relations and agreed down to
the record. The relation store is scoped to its workspace.</p>

<h2>A whole database posture in one file</h2>
<p>{p} <code>WORKSPACE SAVE</code> captures open areas, attached indexes, selected orders,
aliases, and declared relations into a plain-text snapshot; <code>WORKSPACE LOAD</code> restores
it. Several workspaces can be open at once, each owning its own areas and environment.</p>
""".format(p=chip("proven")))

    # scripting
    doc_page("scripting", "Script mode",
      "The repeatable form of the same command language.",
      """
<p>{b} Anything typed at the shell can be written to a command file and replayed. Script mode currently
covers:</p>
<ul class="plain">
<li>Variables, comments, and line continuation</li>
<li><code>IF</code> / <code>ELSE</code> / <code>ENDIF</code></li>
<li><code>LOOP</code> / <code>ENDLOOP</code>, <code>WHILE</code> / <code>ENDWHILE</code>, <code>UNTIL</code> / <code>ENDUNTIL</code></li>
<li><code>SCAN</code> / <code>ENDSCAN</code> over a work area</li>
<li>One level of subscript nesting</li>
<li>CSV and DBF import/export workflows</li>
</ul>
<pre>USE SQLSTU
SCAN
TUPLE *
ENDSCAN</pre>
<p>Visit every record in the current area and print it as a tuple. The same loop appears in
<code>canaries/major_shakedown.dts</code>.</p>
<div class="note"><p>{ch} A language for describing <em>interfaces</em> — menus, windows, dialogs,
controls, event handlers — is a direction, not current syntax. Script mode operates on data today.</p></div>
""".format(b=chip("beta"), ch=chip("chartered")))

    # teaching
    doc_page("teaching", "Teaching material",
      "Labs that make a layer visible instead of describing it.",
      """
<p>The reason to teach on x64base is not that it is small. It is that the parts a database course
usually has to draw on a whiteboard are, here, things a student can open and step through: an index
node, a memo block, a work area, a relation.</p>
<h2>What ships</h2>
<ul class="plain">
<li>{p} <strong>Datasets in every flavor.</strong> The same data as x64, x32, and Visual FoxPro tables,
plus a reference copy — so "what changed between generations" is a diff, not a claim.</li>
<li>{b} <strong>Labs.</strong> Character encoding, index internals, historical data models, and
normalization, each as a command you run and watch.</li>
<li>{p} <strong>Transcripts and regressions.</strong> The same evidence the project uses to check
itself works as courseware: here is the question, here is the run, here is the answer.</li>
</ul>
<h2>What this is not</h2>
<p>Not a learning-management system. It does not enroll students, track them, or grade them, and there
is no plan for it to. {ch} Packaging a lesson as a portable unit is designed but not built.</p>
""".format(p=chip("proven"), b=chip("beta"), ch=chip("chartered")))

    # ecosystem
    doc_page("ecosystem", "Ecosystem context",
      "Where x64base sits, and what it is not trying to replace.",
      """
<p>The xBase world is still alive: open-source compilers, commercial platforms, migration tools, DBF
libraries, and a great deal of running legacy code. x64base belongs in that conversation without
claiming to end it.</p>
<table class="t">
<tr><th>Project</th><th>What it is</th><th>Overlap with x64base</th></tr>
<tr><td>Harbour / xHarbour</td><td>Mature open-source xBase compilers</td><td>Language and DBF handling. Harbour is far more complete as a compiler; x64base is not one.</td></tr>
<tr><td>Alaska Xbase++</td><td>Commercial xBase platform</td><td>Commercial support and tooling. x64base is not for sale.</td></tr>
<tr><td>XSharp</td><td>xBase on .NET</td><td>Language lineage, different runtime entirely.</td></tr>
<tr><td>dBASE tools</td><td>Commercial descendants of the original</td><td>File-format compatibility.</td></tr>
<tr><td>Python DBF libraries</td><td>Read/write access to DBF files</td><td>Format handling, no engine or shell.</td></tr>
</table>
<h2>The actual difference</h2>
<p>x64base is the only one of these built so that the layers are the product. The others aim to make
the database invisible and reliable, which is the correct goal for production software. This one aims
to make it visible and explainable, which is a different job.</p>
<h2>The honest constraint</h2>
<p>Classic DBF-family formats carry structural assumptions from an earlier era of computing. Widening
them to 64 bits is not a recompile; it changes the engineering math throughout — headers, offsets,
memo identifiers, and every index backend, each audited separately. That work is in progress and
tracked openly on the <a href="../../status/">status board</a>.</p>
""")


# ------------------------------ OTHER PAGES --------------------------------
def other():
    # ABOUT
    body = """
<div class="phead"><div class="wrap">
  <p class="crumb">Home / About</p>
  <h1>About x64base</h1>
  <p>A modern 64-bit evolution of the xBase lineage, built to be taught from.</p>
</div></div>
<section><div class="wrap prose">
<h2>What it is</h2>
<p>x64base is a DBF-family database engine written in modern C++, driven by a command shell. It handles
tables, records, fields, work areas, indexes, memos, relations, metadata, help, and scripts — and it is
built so that each of those is a thing you can look at while it works.</p>
<p>It exists for two reasons. First, DBF data has not gone away, and a 64-bit engine for it that is
readable rather than sealed is worth having. Second, database fundamentals are taught almost entirely
through abstraction, and they do not have to be.</p>

<h2>What it is not</h2>
<p>Stated plainly, so nobody has to infer it:</p>
<ul class="tick">
<li>Not a finished commercial database system</li>
<li>Not a Visual FoxPro clone</li>
<li>Not a drop-in replacement for Harbour or Alaska Xbase++</li>
<li>Not unlimited in scale — the 64-bit widening is partial and audited in the open</li>
<li>Not compatible with every DBF dialect</li>
<li>Not for sale, and not a hosted service</li>
<li>Not a learning-management system, and not a student portal</li>
</ul>

<h2>How claims work here</h2>
<p>Every capability on this site is labelled with the strength of its evidence, and the labels are
enforced by demotion: wording changes the day the evidence stops supporting it.</p>
<div class="legend">%(legend)s</div>
<p style="margin-top:22px">The <a href="../status/">status board</a> is the only place these live, and
it includes work that has not been started — because an absence you cannot see is a claim by
omission.</p>

<h2>Lineage</h2>
<p>The project has roots in ANSI C xBase work from 1993 and later recovery branches. Those historical
sources are inventoried separately from the current codebase, with checksums and evidence labels, so
old code can be studied without being confused for present behavior. Thirty-three years is the reason
the DBF focus is deliberate rather than nostalgic.</p>

<h2>Author</h2>
<p>Derald Grimwood. B.S. Management Information Systems; xBase, SAP, and ERP background.</p>

<div class="note"><p><strong>On documentation.</strong> Parts of this site were drafted with AI
assistance and reviewed against source. That is disclosed rather than hidden, and it does not change
the evidence rules: a tier is earned by a transcript, a regression, or a line of code — never by
prose.</p></div>

<p style="margin-top:26px"><em>Preserve the past. Teach the layers. Fix the architecture. Move forward.</em></p>
</div></section>
""" % dict(legend="".join('<div>{} <span>{}</span></div>'.format(chip(k), TIERS[k][1])
                          for k in ["proven", "source", "beta", "chartered", "open"]))
    write("about/index.html", shell("About — x64base", "about", body,
          "What x64base is, what it is not, and how its evidence tiers work.", 1))

    # DOWNLOADS
    body = """
<div class="phead"><div class="wrap">
  <p class="crumb">Home / Downloads</p>
  <h1>Downloads</h1>
  <p>Source today. A tagged release with binaries is the next milestone, and it has not shipped.</p>
</div></div>
<section><div class="wrap prose">
<div class="note"><p><strong>No release has been published yet.</strong> {o} There is no binary to
download; that gap is listed on the <a href="../status/">status board</a> as not started rather than
quietly omitted. The license is settled: <strong>GPL-3.0-only</strong>, committed 2026-08-11. Until a
release exists, building from source is the only way to run x64base.</p></div>

<h2>Source</h2>
<pre>git clone https://github.com/deraldg/x64base</pre>
<p><a href="https://github.com/deraldg/x64base">github.com/deraldg/x64base</a></p>

<h2>Build</h2>
<pre>cmake --preset default
cmake --build --preset default</pre>
<p>C++20, CMake 3.21+, and vcpkg for dependencies. Exercised on Windows/MSVC and WSL/Ubuntu. See
<a href="../docs/getting-started/">Getting started</a> for the first session once it builds.</p>

<h2>What you get</h2>
<ul class="plain">
<li>The command host — one executable, with the engine libraries linked in</li>
<li>Teaching datasets in x64, x32, and Visual FoxPro form, plus a reference copy</li>
<li>The regression suite that produces the evidence cited across this site</li>
<li>Workspace snapshots, including the 43-area, 58-relation demonstration schema</li>
</ul>

<h2>External dependencies</h2>
<p>LMDB backs the CDX key store and SQLite is compiled in as a companion carrier and verification
oracle. Both stay external libraries rather than being absorbed into the engine.</p>
</div></section>
""".format(o=chip("open"))
    write("downloads/index.html", shell("Downloads — x64base", "downloads", body,
          "Build x64base from source. No tagged release has shipped yet.", 1))

    # SCHEMAS
    body = """
<div class="phead"><div class="wrap">
  <p class="crumb">Home / Schemas</p>
  <h1>Schemas</h1>
  <p>The datasets the engine is proved against, and the graph both relation walkers agree on.</p>
</div></div>
<section><div class="wrap prose">
<h2>The demonstration schema</h2>
<p>A production-shaped ERP schema: <strong>34 tables</strong> joined by <strong>58 foreign-key
relations</strong>. It is not a toy, and that matters — positional traversal and the house SELECT
agreeing on a three-table question proves considerably less than agreeing on this one.</p>
<p>{p} The whole thing restores from a single plain-text workspace file: open areas, attached indexes,
selected tag orders, aliases, and every declared relation.</p>

<h2>Dual carrier</h2>
<p>{p} Teaching schemas ship twice — as x64base tables and as a sealed SQLite copy. The SQLite side is
the authority for checking, which is what lets a lesson ask "is the engine right?" and get an answer
rather than an assurance.</p>

<h2>Teaching datasets</h2>
<table class="t">
<tr><th>Form</th><th>Purpose</th></tr>
<tr><td>x64 <code>DBF_64</code></td><td>The current format: 64-bit headers, wide metadata, 64-bit memo identifiers</td></tr>
<tr><td>Classic x32 DBF</td><td>The MS-DOS-era baseline, for comparison</td></tr>
<tr><td>Visual FoxPro DBF</td><td>Field and data-type compatibility, including currency types</td></tr>
<tr><td>Reference copy</td><td>Known-good values for checking a lab's output</td></tr>
</table>
<p>Because the same data exists in every flavor, "what changed between generations" is something a
student can diff rather than take on faith.</p>
</div></section>
""".format(p=chip("proven"))
    write("schemas/index.html", shell("Schemas — x64base", "schemas", body,
          "The 34-table demonstration schema and the teaching datasets, in every DBF flavor.", 1))

    # CONTACT
    body = """
<div class="phead"><div class="wrap">
  <p class="crumb">Home / Contact</p>
  <h1>Contact</h1>
  <p>One maintainer. Issues are the fastest route.</p>
</div></div>
<section><div class="wrap prose">
<h2>Bugs, build failures, and documentation defects</h2>
<p>Open an issue at <a href="https://github.com/deraldg/x64base/issues">github.com/deraldg/x64base/issues</a>.
A build that fails while following the published instructions counts as a documentation defect and is
worth reporting as one.</p>

<h2>Email</h2>
<p>No GitHub account, or something that does not fit an issue? Write to
<a href="mailto:deraldg@gmail.com">deraldg@gmail.com</a>. Issues are still preferred for anything
another user might benefit from finding later.</p>

<h2>Teaching use</h2>
<p>If you want to use x64base in a course, say so in an issue. The teaching material is the part most
likely to be shaped by someone actually trying to teach with it, and it is currently shaped by one
person's guess about that.</p>

<h2>Contributing</h2>
<p>The project is one person's work and the internal structure moves quickly. Small, well-scoped
patches and evidence — a regression that fails, a transcript that contradicts a claim on this site —
are more useful right now than large features.</p>

<div class="note"><p><strong>The most useful thing you can send.</strong> A capability listed here as
runtime-proven that does not reproduce on your machine. That is the claim the whole site rests on, and
finding a hole in it is a favor.</p></div>
</div></section>
"""
    write("contact/index.html", shell("Contact — x64base", "contact", body,
          "How to report bugs, ask about teaching use, or contribute to x64base.", 1))


# Where this lean site is deployed. Staging home is dottalkpp.com; when the
# reorg happens this becomes https://x64base.com and the working archive moves
# to lab.x64base.com. Changing this one line updates sitemap.xml and robots.txt.
BASE_URL = "https://dottalkpp.com"
ARCHIVE_URL = "https://x64base.com"

def extras():
    urls = ["/", "/about/", "/docs/", "/status/", "/downloads/", "/schemas/", "/contact/",
            "/docs/getting-started/", "/docs/command-families/", "/docs/architecture/",
            "/docs/formats/", "/docs/indexing/", "/docs/query/", "/docs/scripting/",
            "/docs/teaching/", "/docs/ecosystem/"]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append("  <url><loc>{}{}</loc><lastmod>2026-08-10</lastmod></url>".format(BASE_URL, u))
    sm.append("</urlset>")
    write("sitemap.xml", "\n".join(sm) + "\n")

    write("robots.txt", "User-agent: *\nAllow: /\n\nSitemap: {}/sitemap.xml\n".format(BASE_URL))

    # --- host configs: harmless on hosts that ignore them -------------------
    write("vercel.json", """{
  "cleanUrls": true,
  "trailingSlash": true,
  "headers": [
    { "source": "/assets/(.*)", "headers": [
      { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" } ] },
    { "source": "/(.*)", "headers": [
      { "key": "X-Content-Type-Options", "value": "nosniff" },
      { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" } ] }
  ]
}
""")

    write("netlify.toml", """[build]
  publish = "."
  command = ""

[[headers]]
  for = "/assets/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"

[[headers]]
  for = "/*"
  [headers.values]
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
""")

    # GitHub Pages: skip Jekyll processing, and claim the domain
    write(".nojekyll", "")
    write("CNAME", BASE_URL.replace("https://", "").replace("http://", "") + "\n")

    write("404.html", shell("Not found — x64base", "", """
<section class="hero"><div class="wrap">
  <p class="eyebrow">404</p>
  <h1>That page is not here.</h1>
  <p class="lead">This is the lean site — a lot of older material lives in the project's working
  archive rather than here. The <a href="/status/">status board</a> lists every area of the project
  and where it stands, which is usually what a missing page was going to say anyway.</p>
  <div class="btns"><a class="btn" href="/">Home</a><a class="btn ghost" href="/docs/">Documentation</a></div>
</div></section>""", "Page not found.", 0))

    write("CHANGELOG.md", """# Changelog

Dated entries, no ceremony. This file replaces the old News section.

## 2026-09-23 (later)
- Retirement polarity sweep added to check_site.py: every page is checked
  against retirements.json and the build fails if one teaches a retired form.
  Negative-tested: the 0083f82 getting-started page (which taught `SQL SELECT`)
  is flagged at the exact line. The upstream register missed that form; a local
  row carries it until adopted upstream.

## 2026-09-23
- Reconciled against engine development ee1b446e3 (AIF-107 G2). Status board
  rebuilt from the engine's regression registry snapshot (engine-facts.json:
  84 specs, 32 default suite): 31 of 45 rows runtime-proven.
- Corrected: joins shipped (INNER/LEFT/RIGHT/FULL/CROSS, default suite) --
  the board still called them chartered. Added GROUP BY, subqueries, set
  operations, DML, parallel scans, primary keys, NULLs, transactional index
  maintenance, multiple workspaces, memo-resident mini-databases.
- Fixed Getting Started: `SQL SELECT` has been a reserved no-op since
  2026-09-04; examples now come from a default-suite regression script.
- Fixed command families: SMARTBROWSE/SIMPLEBROWSE are SMARTBROWSER/
  SIMPLEBROWSER; SB is a shortcut for SIMPLEBROWSER; URL is not a command.
  Removed an invented `SCAN AREAS` example and `LIST NEXT`. Rows added by
  other sessions on 2026-08-11 and 2026-09-03 (memo zoo, REL JOIN, the
  two-walker agreement) were carried forward, not replaced.
- New guards: the build fails if a cited spec leaves the registry, or if the
  status board renders fewer rows than STATUS holds; check_site.py warns when
  the engine facts are more than 30 days old. Banner shows the engine stamp.

## 2026-08-11
- Lean site deployed to dottalkpp.com (GitHub Pages, commit c0fc326). Lane AIF-107.
- LICENSE committed: GPL-3.0-only (engine tree, commit 2dbc29c8f). The
  "Final license text" status entry moves from not-started to done.
- Workspaces now live in memos: a whole database posture (43 areas, 58
  relations) saves into a memo field of a self-creating catalog table and
  restores from inside it, byte-compare verified on every save. Registered
  as the WORKSPACE_MEMO regression.
- The memo store survived its zoo: a seeded stress harness ran six chaotic
  operation patterns (mutation, cross-memo overwrites, growth and shedding,
  duplication, merge-and-retire, erasure; payloads including embedded NUL
  bytes) against a shadow-model oracle -- 20,500 generations, 104,044
  operations, four seeds, zero divergences. "Payload-agnostic memos" moves
  from source-evidenced to runtime-proven.

## 2026-08-10
- Both relation walkers — positional traversal and the house SELECT — answered the same question
  over the 34-table, 58-relation demonstration schema and agreed down to the record.

## 2026-08-05
- Development tree refresh: new commands, reconciled references, rebuilt help text.

## 2026-07-28
- Memo-resident mini-databases registered as a chartered design.

## 2026-07-18
- Documentation set brought current against source.

<!-- Add newest entries at the top. Keep them short and factual; if a claim moves
     between evidence tiers, say so here and update the status board in the same commit. -->
""")

    write("README.md", """# x64base lean site -- dottalkpp.com

The low-key public entry surface for [x64base](https://github.com/deraldg/x64base).
Static HTML, no build dependencies, no framework, no JavaScript except a 20-line
filter on the status board.

    Lane    : AIF-107 (low-key-entry-surface), run COWORK-20260811-001
    Lane doc: D:/code/ccode/docs/maintenance/AIF_107_LOW_KEY_ENTRY_SURFACE_LANE_V1.md
    Owner   : member.derald    Steward: member.ai.claude.cowork

## Where it lives

| Surface | Location |
| --- | --- |
| Live | https://dottalkpp.com |
| Repo | https://github.com/deraldg/dottalkpp (`main`) |
| Local working copy | `d:/dev/dottalkpp-lean` |
| Old Next.js skeleton | branch `archive/nextjs-skeleton-2026-07` |

Deployment is automatic: every push to `main` runs
`.github/workflows/deploy-pages.yml`, publishing the repo root to GitHub Pages.
Live about a minute after push. `CNAME` binds the domain -- do not delete it.

## Viewing locally

    # closest to production (pretty URLs like /status/ work):
    python -m http.server 8080 -d d:/dev/dottalkpp-lean
    # then open http://localhost:8080/

    # zero setup, straight off disk:
    start d:/dev/dottalkpp-lean/index.html

## Updating the site

`build_lean_site.py` is the source of truth -- including THIS README, which it
regenerates on every build. **Never hand-edit the HTML files or this file**;
edit the generator. Workflow:

    cd d:/dev/dottalkpp-lean
    python build_lean_site.py        # regenerates into ./x64base-lean/
    python check_site.py             # link + vocabulary + metadata gate
    xcopy /e /y x64base-lean\\* .    # copy generated output over repo root
    git add .
    git commit -m "what changed"
    git push origin main

(`git add .` is acceptable in THIS repo only -- single-purpose, single-session.
Never in the engine tree.)

Content lives in the data structures at the top of the generator: `STATUS`
(status board rows), `TIERS`, `FAMILIES`, `NAV`, `BASE_URL` (feeds sitemap,
robots, CNAME), `CSS`, and the page-body functions.

## Editorial rules

1. **Every capability claim carries an evidence tier.** Wording is demoted the
   day the evidence stops supporting it.
2. **All growth rates live on `/status/`.** Nowhere else.
3. **Unstarted work is listed.** An absence you cannot see is a claim by
   omission.
4. **No product storefronts.** One engine, one shell; command groupings are
   chapters, not products.
5. **Retired vocabulary stays retired.** `check_site.py` enforces the list on
   every build.
6. **Six nav items.** Adding a seventh means removing one.

## Relationship to the rest of the estate

- **x64base.com** -- the working archive: tracking, planning, the full record.
  Linked from the footer. Untouched by this repo.
- **Engine truth** lives in `D:/code/ccode`; this site restates it and must
  never outrun it. The status board cites registered regression specs from
  `engine-facts.json` (snapshot of `development`); the build fails if a cited
  spec disappears. `check_site.py` also sweeps every page against
  `retirements.json` and fails if a page teaches a retired form (e.g. `SQL
  SELECT`). That register is copied from x64base-site's draft; when the engine
  retires another verb, add the row upstream and re-copy. A retirement nobody
  registered is still invisible -- the sweep is only as good as its register.
- **Domain reorg** (x64base / dottalkpp / derald / dottalk) is explicitly a
  separate future effort, per owner ruling 2026-08-11.

## History

2026-08-11: deployed to the dottalkpp.com apex (c0fc326); license settled the
same day (GPL-3.0-only, engine commit 2dbc29c8f) and the site updated to say so
(097680f).
2026-09-23: reconciled against engine ee1b446e3 (AIF-107 G2); facts now come
from `engine-facts.json`, a snapshot of the engine's regression registry.
Refresh it from the engine tree whenever the board is updated.
Running record: `CHANGELOG.md`.
""")


def main():
    os.makedirs(OUT, exist_ok=True)  # overwrite in place
    write("assets/site.css", CSS)
    home(); status(); docs(); sub_pages(); other(); extras()

    n = sum(len(f) for _, _, f in os.walk(OUT))
    print("built {} files -> {}".format(n, OUT))
    for root, _, files in sorted(os.walk(OUT)):
        for f in sorted(files):
            p = os.path.relpath(os.path.join(root, f), OUT)
            print("  ", p)


if __name__ == "__main__":
    main()
