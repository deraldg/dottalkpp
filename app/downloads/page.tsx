import { SectionPage } from "@/components/SectionPage";
import { downloadArtifacts } from "@/lib/site-data";

export default function DownloadsPage() {
  return (
    <SectionPage
      eyebrow="Downloads"
      title="Artifact Policy Before Bulk Uploads"
      intro="Downloads must be classified before publication, with proof status and accessibility status carried beside each artifact."
    >
      <section className="section">
        <div className="artifact-table" role="table" aria-label="Download artifact classification">
          <div className="artifact-row artifact-head" role="row">
            <span>Artifact</span>
            <span>Type</span>
            <span>Source</span>
            <span>Proof</span>
            <span>Accessibility</span>
          </div>
          {downloadArtifacts.map((artifact) => (
            <div className="artifact-row" role="row" key={artifact.title}>
              <span>{artifact.title}</span>
              <span>{artifact.type}</span>
              <span>{artifact.source}</span>
              <span>{artifact.proofStatus}</span>
              <span>
                text: {artifact.accessibility.text_summary}; contrast: {artifact.accessibility.contrast_review};
                screen reader: {artifact.accessibility.screen_reader_review}
              </span>
            </div>
          ))}
        </div>
      </section>
    </SectionPage>
  );
}
