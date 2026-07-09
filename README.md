# DotTalk++ documentation staging site

Local static-first staging site for DotTalk++ documentation work targeted at
`dottalkpp.com`.

This site holds the focused manual, reference, generated-documentation, and
proof-library surface for DotTalk++ while the final repository/domain split is
worked out.

It supports, but does not replace, `x64base.com`. The umbrella x64base site
remains the ecosystem home for the database engine, product family, Laboratory
Campus, project history, and selected public evidence. This site is the deeper
manual room for DotTalk++ manuals, references, generated reports, proof labels,
and documentation bundles.

`derald.com` remains useful as a document storage/retrieval and staging surface:
larger artifacts, operator-facing indexes, and retrieval workflows can live
there while `dottalkpp.com` presents the reviewed public manual/reference face.

The site may expose planned lanes such as PRONOUNS semantic field hooks, custom
field behaviors, and domain split notes, but those sections must stay labeled as
design or staging material until source/runtime/manual evidence proves them.

## Authority rules

- Source/runtime evidence is upstream of this site.
- Manuals may feed this site after review and proof labeling.
- Website prose must not become manual technical truth unless the artifact is
  website-owned, separately maintained, non-derivable elsewhere, and
  provenance-labeled.
- `README.*` files are orientation and provenance artifacts; preserve prior
  versions before replacement.

## Routes

- `/manuals`
- `/dotscript`
- `/reference`
- `/generated`
- `/downloads`
- `/governance`

Shared navigation and section inventories live in `lib/site-data.ts` so the
home page and route pages do not drift.

## Accessibility and provenance

Downloads should carry type, source, proof status, and accessibility status.
Use current language: accessibility, inclusive design, and people with
disabilities. Avoid euphemistic labels. Complex documents should have HTML or
Markdown summaries when possible.
- Domain ownership or WHOIS observations require project-owner verification
  before public claims.

## Local commands

```text
npm install
npm run dev
npm run build
```

The build runs `scripts/check-public-content.mjs` before static export.
