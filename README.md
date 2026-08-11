# x64base lean site -- dottalkpp.com

The low-key public entry surface for [x64base](https://github.com/deraldg/x64base).
Static HTML, no build dependencies, no framework, no JavaScript except a 20-line
filter on the status board.

    Lane   : AIF-107 (low-key-entry-surface), run COWORK-20260811-001
    Lane doc: D:\code\ccode\docs\maintenance\AIF_107_LOW_KEY_ENTRY_SURFACE_LANE_V1.md
    Owner  : member.derald    Steward: member.ai.claude.cowork

## Where it lives

| Surface | Location |
| --- | --- |
| Live | https://dottalkpp.com |
| Repo | https://github.com/deraldg/dottalkpp (`main`) |
| Local working copy | `d:\dev\dottalkpp-lean` |
| Old Next.js skeleton | branch `archive/nextjs-skeleton-2026-07` (preserved, do not delete `d:\dev\dottalkpp-site` until certain) |

Deployment is automatic: every push to `main` triggers
`.github/workflows/deploy-pages.yml`, which publishes the repo root to GitHub
Pages. Live roughly one minute after push. The `CNAME` file binds the custom
domain -- do not delete it.

## Viewing locally

Two ways, both against the identical files that are deployed:

    # closest match to production (pretty URLs like /status/ work):
    python -m http.server 8080 -d d:\dev\dottalkpp-lean
    # then open http://localhost:8080/

    # zero setup (works straight off disk):
    start d:\dev\dottalkpp-lean\index.html

## Updating the site

`build_lean_site.py` is the source of truth. **Never hand-edit the HTML files**
-- the generator overwrites them. Workflow:

    cd d:\dev\dottalkpp-lean
    python build_lean_site.py        # regenerates into .\x64base-lean\
    python check_site.py             # link + vocabulary + metadata gate
    xcopy /e /y x64base-lean\* .     # copy generated output over repo root
    # preview locally (commands above), then:
    git add .
    git commit -m "what changed"
    git push origin main

Note the generator emits into a `x64base-lean\` subfolder; the deployed files
are the copies at the repo root. The xcopy step bridges them. (`git add .` is
acceptable in THIS repo only -- it is single-purpose and single-session. Never
in the engine tree.)

Content lives in the data structures at the top of the generator:

| What | Where |
| --- | --- |
| Status board rows | `STATUS` |
| Evidence tier definitions | `TIERS` |
| Command families | `FAMILIES` |
| Navigation | `NAV` |
| Deployed domain | `BASE_URL` (feeds sitemap, robots, CNAME) |
| Styling | `CSS` |
| Page bodies | `home()`, `status()`, `docs()`, `sub_pages()`, `other()` |

## Editorial rules

These are what make the site worth reading. Keep them.

1. **Every capability claim carries an evidence tier** -- runtime-proven,
   source-evidenced, active beta, chartered, or not started. Wording is demoted
   the day the evidence stops supporting it.
2. **All growth rates live on `/status/`.** Nowhere else. That page is the
   differentiator.
3. **Unstarted work is listed.** An absence you cannot see is a claim by
   omission.
4. **No product storefronts.** One engine, one shell. Command groupings are
   chapters, not products -- nothing gets a card or nav slot unless it can be
   downloaded and versioned alone.
5. **Retired vocabulary stays retired.** `check_site.py` enforces the list on
   every build.
6. **Six nav items.** Adding a seventh means removing one.

## Relationship to the rest of the estate

- **x64base.com** -- the working archive: tracking, planning, full project
  record. Linked from this site's footer as "Working archive." Untouched by
  this repo.
- **`D:\dev\x64base-site`** -- the working archive's source tree. Untouched.
- **Engine truth** lives in `D:\code\ccode`; this site restates it and must
  never outrun it. Current caveat (lane gate G2, open): the status board was
  derived from the public `main` snapshot and x64base.com, not yet reconciled
  against `development`.
- **Domain reorg** (x64base / dottalkpp / derald / dottalk) is explicitly a
  separate future effort, per owner ruling 2026-08-11.

## History

- 2026-08-11: deployed to dottalkpp.com apex (commit `c0fc326`); license
  settled the same day (GPL-3.0-only, engine commit `2dbc29c8f`) and the site
  updated to say so (`097680f`). See `CHANGELOG.md` for the running record.
