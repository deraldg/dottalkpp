import { SectionPage } from "@/components/SectionPage";
import { downloadArtifacts, downloadBuckets } from "@/lib/site-data";

export default function DownloadsPage() {
  return (
    <SectionPage
      eyebrow="Downloads"
      title="DotTalk++ Manual And Proof Downloads"
      intro="This is the DotTalk++ download library for manuals, references, generated reports, proof packets, accessible text versions, and archived snapshots. x64base.com should stay the curated ecosystem entry point."
    >
      <section className="section split">
        <div>
          <h2>Download Lane Ownership</h2>
          <p>
            The full download library belongs with DotTalk++ documentation. It
            can hold larger manual bundles, generated reports, and proof packets
            without turning x64base.com into an artifact shelf.
          </p>
        </div>
        <div className="flow-panel" aria-label="Download lane split">
          <pre>{`x64base.com/downloads
  curated starting points
  stable public artifacts
  links into DotTalk++ bundles

dottalkpp.com/downloads
  manuals
  references
  generated reports
  proof packets
  accessible text versions
  archived snapshots`}</pre>
        </div>
      </section>

      <section className="section">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Buckets</p>
            <h2>Grouped By Reader Purpose</h2>
          </div>
        </div>
        <div className="card-grid route-grid">
          {downloadBuckets.map((bucket) => (
            <article className="info-card" key={bucket.title}>
              <h3>{bucket.title}</h3>
              <p>{bucket.text}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="section">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Manifest</p>
            <h2>Publication Classification</h2>
          </div>
        </div>
        <p>
          These rows are the current publication manifest shape. Links should be
          added only after the artifact is public-ready or intentionally marked
          as staged, generated, historical, or review-needed.
        </p>
        <div className="artifact-table" role="table" aria-label="Download artifact classification">
          <div className="artifact-row artifact-head" role="row">
            <span>Artifact</span>
            <span>Bucket</span>
            <span>Type</span>
            <span>Source</span>
            <span>Proof</span>
            <span>Review</span>
            <span>Accessibility</span>
          </div>
          {downloadArtifacts.map((artifact) => (
            <div className="artifact-row" role="row" key={artifact.title}>
              <span>
                <strong>{artifact.title}</strong>
                <small>{artifact.role}</small>
              </span>
              <span>{artifact.bucket}</span>
              <span>{artifact.type}</span>
              <span>{artifact.source}</span>
              <span>{artifact.proofStatus}</span>
              <span>{artifact.reviewStatus}</span>
              <span>
                alt: {artifact.accessibility.alt_text}; text: {artifact.accessibility.text_summary};
                keyboard: {artifact.accessibility.keyboard_path}; contrast: {artifact.accessibility.contrast_review};
                screen reader: {artifact.accessibility.screen_reader_review}
              </span>
            </div>
          ))}
        </div>
      </section>

      <section className="section gate-section">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Rules</p>
            <h2>Before A File Becomes A Download</h2>
          </div>
        </div>
        <div className="gate-list">
          <div>Classify the artifact before upload.</div>
          <div>Attach source/provenance and proof status.</div>
          <div>Preserve versioned snapshots instead of replacing history.</div>
          <div>Provide text alternatives for visual or binary-heavy documents.</div>
        </div>
      </section>
    </SectionPage>
  );
}
