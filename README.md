# DotTalk++ documentation staging site

Local static-first staging site for DotTalk++ documentation work. The current
working name is `derald.com` staging while the final `dottalkpp.com` repository
and domain split is worked out.

This site temporarily holds the focused manual, reference, generated-documentation, and proof-library surface for DotTalk++ while the final `dottalkpp.com` repository/domain split is worked out.

It supports, but does not replace, `x64base.com`. The umbrella x64base site
remains the ecosystem home for the database engine, product family, Laboratory
Campus, project history, and selected public evidence. This site is the deeper
manual room for DotTalk++ manuals, references, generated reports, proof labels,
and documentation bundles.

## Authority rules

- Source/runtime evidence is upstream of this site.
- Manuals may feed this site after review and proof labeling.
- Website prose must not become manual technical truth unless the artifact is
  website-owned, separately maintained, non-derivable elsewhere, and
  provenance-labeled.
- `README.*` files are orientation and provenance artifacts; preserve prior
  versions before replacement.

## Local commands

```text
npm install
npm run dev
npm run build
```

The build runs `scripts/check-public-content.mjs` before static export.
