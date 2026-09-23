# x64base lean site -- dottalkpp.com

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
    xcopy /e /y x64base-lean\* .    # copy generated output over repo root
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
  spec disappears. It does NOT catch prose that describes a retired surface --
  check examples against source when the engine retires a verb.
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
