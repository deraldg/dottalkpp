# Changelog

Dated entries, no ceremony. This file replaces the old News section.

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
