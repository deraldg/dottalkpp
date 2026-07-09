import Link from "next/link";
import {
  Archive,
  BookOpen,
  Braces,
  CheckCircle2,
  Database,
  FileCode2,
  FileText,
  GitBranch,
  Library,
  ScrollText,
  ShieldCheck,
  TerminalSquare
} from "lucide-react";
import {
  developerItems,
  gateItems,
  generatedItems,
  manualItems,
  plannedItems,
  primaryLinks,
  referenceItems,
  relationshipItems,
  statusItems
} from "@/lib/site-data";

const generatedIconMap = {
  "SelfDoc outputs": Library,
  "MDO curation": FileText,
  "Command contracts": ShieldCheck,
  "Proof reports": CheckCircle2,
  "Manualgen outputs": FileText
};

export default function HomePage() {
  return (
    <main>
      <section className="hero">
        <div className="hero-copy">
          <p className="eyebrow">Manual room for the x64base command surface</p>
          <h1>DotTalk++</h1>
          <p className="subtitle">
            Command shell, script language, and self-documenting database workbench
            for the x64base system.
          </p>
          <div className="actions">
            {primaryLinks.map((link) =>
              link.href.startsWith("http") ? (
                <a key={link.href} href={link.href}>
                  {link.label}
                </a>
              ) : (
                <Link key={link.href} href={link.href}>
                  {link.label}
                </Link>
              )
            )}
          </div>
        </div>
        <div className="terminal-panel" aria-label="DotTalk++ documentation status">
          <div className="terminal-top">
            <span />
            <span />
            <span />
          </div>
          <pre>{`DOTHELP MANUALS
CMDHELP COMMANDS
SELFDOCCHECK STATUS

publication lane:
source/runtime truth
-> HELP and metadata
-> SelfDoc collection
-> MDO curation
-> versioned public docs`}</pre>
        </div>
      </section>

      <section className="status-grid" aria-label="Current status">
        {statusItems.map((item) => (
          <div className="status-cell" key={item.label}>
            <span>{item.label}</span>
            <strong>{item.value}</strong>
          </div>
        ))}
      </section>

      <section className="intro">
        <div>
          <h2>What This Site Handles</h2>
          <p>
            `dottalkpp.com` is not a second marketing site. It is the deeper
            technical library for DotTalk++ manuals,
            references, generated documentation, proof reports, and downloadable
            documentation bundles.
          </p>
        </div>
        <div>
          <h2>What Stays at x64base.com</h2>
          <p>
            `x64base.com` remains the ecosystem home for the engine, DBF_64 and
            FPT64 specifications, product family overview, Laboratory Campus,
            project history, and selected public evidence.
          </p>
        </div>
      </section>

      <section className="section" id="manuals">
        <div className="section-heading">
          <BookOpen aria-hidden="true" />
          <div>
            <p className="eyebrow">Manuals</p>
            <h2>Curated and Versioned Manuals</h2>
          </div>
        </div>
        <div className="list-grid">
          {manualItems.map((item) => (
            <div className="list-item" key={item}>
              {item}
            </div>
          ))}
        </div>
      </section>

      <section className="section split" id="dotscript">
        <div>
          <div className="section-heading">
            <ScrollText aria-hidden="true" />
            <div>
              <p className="eyebrow">DotScript</p>
              <h2>Readable Scripts for Repeatable Work</h2>
            </div>
          </div>
          <p>
            DotScript is the script form of the DotTalk++ command language. It
            should document variables, comments, continuation, IF/ELSE/ENDIF,
            LOOP/ENDLOOP, WHILE, UNTIL, SCAN, nesting limits, examples, smoke
            scripts, and mutation-safe automation.
          </p>
        </div>
        <div className="code-card">
          <pre>{`* Inspect a current lab table.
USE students
STRUCT
LIST

IF recno() = 1
  ? "first record"
ENDIF`}</pre>
        </div>
      </section>

      <section className="section" id="reference">
        <div className="section-heading">
          <TerminalSquare aria-hidden="true" />
          <div>
            <p className="eyebrow">Reference</p>
            <h2>Command and Runtime Reference Lanes</h2>
          </div>
        </div>
        <div className="tag-grid">
          {referenceItems.map((item) => (
            <span key={item}>{item}</span>
          ))}
        </div>
      </section>

      <section className="section" id="generated">
        <div className="section-heading">
          <GitBranch aria-hidden="true" />
          <div>
            <p className="eyebrow">Generated Docs</p>
            <h2>Generated First, Reviewed Before Trust</h2>
          </div>
        </div>
        <div className="card-grid">
          {generatedItems.map((item) => {
            const Icon = generatedIconMap[item.title as keyof typeof generatedIconMap] ?? FileText;
            return (
              <article className="info-card" key={item.title}>
                <Icon aria-hidden="true" />
                <h3>{item.title}</h3>
                <p>{item.text}</p>
              </article>
            );
          })}
        </div>
      </section>

      <section className="section" id="relationship">
        <div className="section-heading">
          <Database aria-hidden="true" />
          <div>
            <p className="eyebrow">Relationship</p>
            <h2>Companion Site, Not a Replacement</h2>
          </div>
        </div>
        <div className="card-grid relationship-grid">
          {relationshipItems.map((item) => (
            <article className="info-card" key={item.title}>
              <h3>{item.title}</h3>
              <p>{item.text}</p>
            </article>
          ))}
        </div>
        <div className="flow-panel" aria-label="Documentation authority flow">
          <pre>{`source/runtime evidence
-> HELP, metadata, comments, contracts
-> SelfDoc and MDO collection
-> manualgen inventory and validation
-> reviewed manual sections
-> x64base.com summaries and DotTalk++ manual-room pages`}</pre>
        </div>
      </section>

      <section className="section split" id="developer">
        <div>
          <div className="section-heading">
            <FileCode2 aria-hidden="true" />
            <div>
              <p className="eyebrow">Developer</p>
              <h2>Rules for Public Documentation</h2>
            </div>
          </div>
          <p>
            Public pages must avoid private local paths, unsupported feature
            claims, and private artifacts. Each generated document should carry a
            date, source snapshot label, generator name, proof level, and review
            status.
          </p>
        </div>
        <div className="policy-list">
          {developerItems.map((item) => (
            <div key={item}>{item}</div>
          ))}
        </div>
      </section>

      <section className="section gate-section">
        <div className="section-heading">
          <ShieldCheck aria-hidden="true" />
          <div>
            <p className="eyebrow">Publication Gates</p>
            <h2>Rules That Prevent Documentation Drift</h2>
          </div>
        </div>
        <div className="gate-list">
          {gateItems.map((item) => (
            <div key={item}>{item}</div>
          ))}
        </div>
      </section>

      <section className="section" id="planned">
        <div className="section-heading">
          <FileText aria-hidden="true" />
          <div>
            <p className="eyebrow">Planned Lanes</p>
            <h2>Design Work That Must Stay Labeled</h2>
          </div>
        </div>
        <div className="card-grid relationship-grid">
          {plannedItems.map((item) => (
            <article className="info-card" key={item.title}>
              <h3>{item.title}</h3>
              <p>{item.text}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="section downloads" id="downloads">
        <div className="section-heading">
          <Archive aria-hidden="true" />
          <div>
            <p className="eyebrow">Downloads</p>
            <h2>Artifact Policy Before Bulk Uploads</h2>
          </div>
        </div>
        <p>
          Large PDFs, generated reports, and release documentation bundles should
          be classified before publication. Public pages can describe private or
          local artifacts, but should only link reviewed public assets stored in
          the site, release system, or approved object storage.
        </p>
      </section>

      <footer>
        <Database aria-hidden="true" />
        <span>
          DotTalk++ documentation site. Umbrella project context remains at{" "}
          <Link href="https://x64base.com">x64base.com</Link>.
        </span>
        <Braces aria-hidden="true" />
      </footer>
    </main>
  );
}
