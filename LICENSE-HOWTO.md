# Committing the license — five minutes, done forever

## 1. Copy the file

Put `LICENSE` (in this folder) at the root of `deraldg/x64base`. Name it exactly
`LICENSE` — GitHub detects it and shows "GPL-3.0" on the repo page automatically.

## 2. Fix the README

In README.md, replace:

    ## License
    To be defined.

with:

    ## License
    GPL-3.0-only. See [LICENSE](LICENSE).

## 3. Source file header (optional, do over time)

The conventional per-file header. Add to new files as you touch them; no need
for a bulk pass today:

    // x64base — a 64-bit DBF database engine and command shell.
    // Copyright (C) 1993-2026 Derald R. Grimwood Jr.
    //
    // This program is free software: you can redistribute it and/or modify it
    // under the terms of the GNU General Public License as published by the
    // Free Software Foundation, version 3.
    //
    // This program is distributed in the hope that it will be useful, but
    // WITHOUT ANY WARRANTY; without even the implied warranty of
    // MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
    // General Public License for more details: <https://www.gnu.org/licenses/>.

## 4. Update the lean site

In `build_lean_site.py`, change two strings and rebuild:

- footer: `GPLv3 (license file pending)` → `GPL-3.0-only`
- STATUS entry "Final license text": tier `open` → `proven`, text
  "GPLv3. LICENSE file committed." — and enjoy moving something off the
  not-started list on day one.

## Why this is safe to do today

- **You lose nothing.** As sole copyright holder you can still dual-license,
  sell commercial licenses later, or relicense future versions. GPLv3 binds
  *recipients* of this code, not you.
- **"3.0-only" vs "or later":** the file above is applied as GPL-3.0-only unless
  your headers say "or any later version." Only means you, not the FSF, decide
  if v4 ever applies. That is the conservative choice and the one matching the
  site footer.
- **Dependencies are fine.** SQLite is public domain; LMDB is OpenLDAP-licensed
  (permissive); both are GPLv3-compatible.
- **The only real commitment:** code published under GPLv3 stays free as
  published. You already decided that when you made the repo public and wrote
  "not for sale."

The stall was the decision, and the decision is already made. This is just the
paperwork.
