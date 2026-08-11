# x64base — lean site

The public front door for [x64base](https://github.com/deraldg/x64base). Static HTML, no build
dependencies, no JavaScript except a 20-line filter on the status board.

## Regenerating

    python3 build_lean_site.py     # emits ./x64base-lean/
    python3 check_site.py          # link + vocabulary + metadata check

`build_lean_site.py` is the source of truth. **Do not hand-edit files in `x64base-lean/`** — they are
overwritten on every build. Content lives in the Python data structures at the top of the generator:

| What | Where |
| --- | --- |
| Status board rows | `STATUS` |
| Evidence tier definitions | `TIERS` |
| Command families | `FAMILIES` |
| Navigation | `NAV` |
| Styling | `CSS` |
| Page bodies | `home()`, `status()`, `docs()`, `sub_pages()`, `other()` |

## Deploying

Copy `x64base-lean/` to any static host. No server-side anything. Set the 404 handler to `404.html`.

## Editorial rules

These are what make the site worth reading — keep them.

1. **Every capability claim carries an evidence tier.** Runtime-proven, source-evidenced, active beta,
   chartered, or not started. Wording gets demoted the day the evidence stops supporting it.
2. **All growth rates live on `/status/`.** Nowhere else. That page is the differentiator.
3. **Unstarted work is listed.** An absence you cannot see is a claim by omission.
4. **No product storefronts.** x64base is one engine with one shell. Command groupings are chapters,
   not products — nothing gets a card or a nav slot unless it can be downloaded and versioned alone.
5. **Retired vocabulary stays retired.** `check_site.py` enforces the list. If you need a coined term,
   it must replace a phrase you would otherwise repeat ten times, and it gets defined on first use.
6. **Six nav items.** Adding a seventh means removing one.

## What deliberately is not here

The methodology material — the co-development system, self-documenting publication chain, and
documentation organizer — belongs to a separate project and is not part of the engine's front door.
The full working archive stays where it is; this site never claims to be complete, only current.
