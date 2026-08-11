# Deploy the lean site to lean.dottalkpp.com

GitHub Pages, on a subdomain. **Nothing existing is touched** — dottalkpp.com,
x64base.com, and `dev\x64base-site` all keep running exactly as they are.

Two things happen: a new repo, and one DNS record. About ten minutes, most of it
waiting for DNS.

---

## Step 1 — Get the files

Download `x64base-lean-site.zip` from the chat and extract it. You want a folder
whose **root** contains `index.html` — not a nested `x64base-lean/` inside it.

    d:\dev\x64base-lean-site\
      index.html          ← must be at this level
      CNAME
      .nojekyll
      assets\
      docs\
      status\
      ...

## Step 2 — Create the repo

At <https://github.com/new>:

- Name: `lean-site` (or `dottalkpp-lean` — the name doesn't appear publicly)
- Public
- Do **not** add a README, .gitignore, or license — the folder already has what
  it needs

Then, in PowerShell:

    cd d:\dev\x64base-lean-site
    git init
    git add .
    git commit -m "Lean site: initial publication"
    git branch -M main
    git remote add origin https://github.com/deraldg/lean-site.git
    git push -u origin main

> If `git push` asks for a password, use a personal access token, not your
> account password — GitHub stopped accepting passwords for git in 2021. Create
> one at Settings → Developer settings → Personal access tokens.

## Step 3 — Turn on Pages

In the new repo: **Settings → Pages**

- Source: **Deploy from a branch**
- Branch: **main**, folder: **/ (root)**
- Save

Under "Custom domain" it should already show `lean.dottalkpp.com` — the `CNAME`
file in the repo sets that automatically. If the box is empty, type it in and
save.

Leave **Enforce HTTPS** unchecked for now; you can tick it once the certificate
is issued (usually within an hour).

At this point the site is already live at
`https://deraldg.github.io/lean-site/` — worth opening to confirm before you
touch DNS. Some styling may look off at that URL because of the `/lean-site/`
path prefix; that resolves once the custom domain is active.

## Step 4 — One DNS record

At whatever registrar holds dottalkpp.com, add:

| Type | Name / Host | Value | TTL |
| --- | --- | --- | --- |
| CNAME | `lean` | `deraldg.github.io` | default (or 3600) |

That is the only change. Subdomains need just this one record — no A records,
no touching the existing `@` or `www` entries that serve dottalkpp.com today.

DNS usually propagates in 5–30 minutes. Check with:

    nslookup lean.dottalkpp.com

When it answers with a GitHub address, you're live at
**https://lean.dottalkpp.com**

## Step 5 — Post-launch check

- [ ] Homepage: light background, serif headline, six nav items
- [ ] `/status/` — filter buttons respond
- [ ] `/nope/` — shows the styled 404, not GitHub's
- [ ] `/sitemap.xml` and `/robots.txt` say `lean.dottalkpp.com`
- [ ] Footer "Working archive" link reaches x64base.com
- [ ] Tick **Enforce HTTPS** in Settings → Pages once the cert appears

---

## Updating it later

    # edit build_lean_site.py, then:
    python build_lean_site.py
    python check_site.py
    git add . && git commit -m "what changed" && git push

Pages redeploys on push, typically within a minute.

## Moving it to x64base.com at the reorg

One line in `build_lean_site.py`:

    BASE_URL = "https://x64base.com"

Rebuild (which regenerates `CNAME`, `sitemap.xml`, and `robots.txt`), push,
update the custom domain in Pages settings, and point DNS. The domain appears
nowhere else in the site that isn't generated.
