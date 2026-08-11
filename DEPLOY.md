# Deploying to dottalkpp.com

Static HTML. No build step, no Node, no framework. Pick whichever matches how
dottalkpp.com is already set up.

> **Nothing here touches x64base.com or `dev\x64base-site`.** This is a separate
> site on a separate domain. The old site keeps running exactly as it does today.

---

## Option A — Netlify (easiest, drag and drop)

1. Go to <https://app.netlify.com/drop>
2. Drag the whole `x64base-lean-site` folder onto the page
3. Site is live in about ten seconds on a `*.netlify.app` URL
4. Site settings → Domain management → Add custom domain → `dottalkpp.com`
5. Point DNS at Netlify (they show the exact records)

`netlify.toml` is already in the folder — caching and security headers are set.

## Option B — Vercel

    npm i -g vercel
    cd d:\dev\x64base-lean-site
    vercel --prod

Then add `dottalkpp.com` in the project's Domains tab. `vercel.json` is already
present with `cleanUrls` on, so `/status/` works without the `index.html`.

## Option C — GitHub Pages

1. Create a repo, e.g. `deraldg/dottalkpp-site`
2. Commit the contents of this folder to `main`
3. Settings → Pages → Source: `main` / root
4. `CNAME` and `.nojekyll` are already in the folder, so the custom domain and
   raw-file serving are handled
5. At your registrar, point `dottalkpp.com` at GitHub Pages:

       A     185.199.108.153
       A     185.199.109.153
       A     185.199.110.153
       A     185.199.111.153
       CNAME www → deraldg.github.io

## Option D — Any host you already have

Upload the folder contents to the web root. Apache, nginx, IIS, shared hosting —
all fine. Two optional server settings:

- Serve `404.html` for not-found requests
- Enable directory indexes (any host does this by default) so `/status/` finds
  `/status/index.html`

---

## After it is live — a five-minute check

- [ ] Homepage loads with the light background and six nav items
- [ ] `/status/` filter buttons work (they need JavaScript, nothing else)
- [ ] A made-up URL like `/nope/` shows the styled 404, not the host's default
- [ ] `/sitemap.xml` and `/robots.txt` both say `dottalkpp.com`
- [ ] Footer "Working archive" link goes to x64base.com
- [ ] Open it on a phone — the layout is fluid, but confirm

## When you do the reorg later

Change one line in `build_lean_site.py`:

    BASE_URL = "https://x64base.com"

Rebuild, redeploy to x64base.com, move the working archive to
`lab.x64base.com`, and point `dottalkpp.com` at a 301 redirect. Nothing else in
the site needs editing — the domain only appears in `sitemap.xml`, `robots.txt`,
and `CNAME`, all generated.
