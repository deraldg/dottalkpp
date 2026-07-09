export const primaryLinks = [
  { href: "/manuals", label: "Read the Manual" },
  { href: "/dotscript", label: "DotScript Guide" },
  { href: "/reference", label: "Command Reference" },
  { href: "/generated", label: "Generated Docs" },
  { href: "/downloads", label: "Downloads" },
  { href: "https://x64base.com", label: "x64base.com" }
];

export const statusItems = [
  { label: "Site role", value: "Focused documentation home" },
  { label: "Current state", value: "Staging skeleton" },
  { label: "Publication rule", value: "Proof labels required" },
  { label: "Source posture", value: "Generated docs must be reviewed" }
];

export const manualItems = [
  "DotTalk++ User Manual",
  "DotScript Language Guide",
  "Command Reference",
  "Function Reference",
  "Developer Manual",
  "SelfDoc Manual",
  "MDO Manual",
  "Versioned manual snapshots"
];

export const dotscriptTopics = [
  "syntax",
  "comments",
  "line continuation",
  "variables",
  "IF / ELSE / ENDIF",
  "LOOP / ENDLOOP",
  "WHILE",
  "UNTIL",
  "SCAN / ENDSCAN",
  "nesting limits",
  "examples",
  "mutation-safe scripting"
];

export const referenceItems = [
  "Commands",
  "Functions",
  "SET family",
  "Data mutators",
  "Workspaces and areas",
  "Table buffering",
  "Relations",
  "Indexing",
  "Memos",
  "Semantic field hooks",
  "DDL",
  "Import/export",
  "External app commands",
  "HELP / CMDHELP / CMDHELPCHK"
];

export const generatedItems = [
  {
    title: "SelfDoc outputs",
    text: "Generated reports from runtime, command, metadata, help, and source-contract layers."
  },
  {
    title: "MDO curation",
    text: "Curated report and manual lanes that turn generated material into public documentation."
  },
  {
    title: "Command contracts",
    text: "Source-derived command metadata, usage contracts, proof labels, and review status."
  },
  {
    title: "Proof reports",
    text: "Runtime transcripts, canary outputs, CMDHELPCHK reports, and generated proof indexes."
  },
  {
    title: "Manualgen outputs",
    text: "Inventories, validation results, dry-run manuals, accepted sections, and publication manifests."
  }
];

export const developerItems = [
  "Coding standards",
  "Command registration",
  "Documentation contracts",
  "SelfDoc feed",
  "Public-content guard",
  "Artifact policy",
  "Manual release policy",
  "README preservation",
  "Planned lanes must stay labeled",
  "Accessibility status"
];

export const relationshipItems = [
  {
    title: "x64base.com",
    text: "Ecosystem home for the engine, product family, DBF_64/FPT64 specs, Laboratory Campus, project story, and selected evidence."
  },
  {
    title: "dottalkpp.com",
    text: "Likely public identity for the focused technical library: manuals, command references, generated documentation, proof reports, and downloadable document bundles."
  },
  {
    title: "derald.com",
    text: "Optional staging, storage, retrieval, and operator-facing organization surface. It should not become confusing product branding."
  },
  {
    title: "Source authority",
    text: "Runtime behavior, command syntax, file formats, mutators, table buffering, HELP, metadata, SelfDoc, and MDO remain upstream of public prose."
  }
];

export const gateItems = [
  "Implementation evidence -> reviewed manuals -> website summaries",
  "Manual sections may feed this site after review and proof labeling",
  "Website prose must not become manual truth unless the artifact is website-owned and non-derivable",
  "README.* files are preserved as orientation and provenance artifacts",
  "Domain ownership or WHOIS observations require owner verification before public claims",
  "Downloads need artifact class, proof status, and accessibility status"
];

export const plannedItems = [
  {
    title: "When the world changes your schema",
    text: "Student lesson using Y2K, the Euro, ERP modernization, and PRONOUNS semantic fields to ask whether a system can adapt safely before it is replaced."
  },
  {
    title: "PRONOUNS semantic field hook",
    text: "Design lane for character-backed semantic metadata, validation, normalization, and optional SEX relationship rules. Not a current runtime claim."
  },
  {
    title: "Custom field behaviors",
    text: "Future handlers should resolve through metadata/DDICT/FIELDMGR and prove behavior across REPLACE, MULTIREP, CALCWRITE, buffering, import/export, FIELDS, STRUCT, and SelfDoc."
  },
  {
    title: "Domain split",
    text: "dottalkpp.com is the intended reviewed public manual/reference face; derald.com can remain staging, storage, and retrieval support. dottalk.com should only be discussed publicly after owner verification."
  }
];

export const downloadArtifacts = [
  {
    title: "Manual bundle",
    type: "manual draft",
    source: "manualgen lane",
    proofStatus: "review-needed",
    accessibility: {
      alt_text: "not-applicable",
      text_summary: "needed",
      keyboard_path: "not-applicable",
      contrast_review: "needed",
      screen_reader_review: "needed"
    }
  },
  {
    title: "Generated report packet",
    type: "generated-but-unreviewed",
    source: "SelfDoc / MDO reports",
    proofStatus: "source-evidenced",
    accessibility: {
      alt_text: "not-applicable",
      text_summary: "ready",
      keyboard_path: "not-applicable",
      contrast_review: "checked",
      screen_reader_review: "needed"
    }
  },
  {
    title: "Proof packet",
    type: "proof packet",
    source: "runtime transcripts and canaries",
    proofStatus: "runtime-evidenced",
    accessibility: {
      alt_text: "needed",
      text_summary: "ready",
      keyboard_path: "not-applicable",
      contrast_review: "checked",
      screen_reader_review: "needed"
    }
  }
];

export const authorityFlow = [
  "implementation/source evidence",
  "HELP / metadata / comments / contracts",
  "SelfDoc / MDO",
  "manualgen",
  "reviewed manuals",
  "x64base.com summaries",
  "DotTalk++ manual-room pages"
];
