# Changelog

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
