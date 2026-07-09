import { SectionPage } from "@/components/SectionPage";
import { referenceItems } from "@/lib/site-data";

export default function ReferencePage() {
  return (
    <SectionPage
      eyebrow="Reference"
      title="Command And Runtime Reference Lanes"
      intro="Reference pages should be generated or reviewed from command registration, HELP, contracts, metadata, source, and runtime proof."
      items={referenceItems}
    >
      <section className="section gate-section">
        <h2>Data Mutators Need Special Labels</h2>
        <p>
          `REPLACE`, `CALC`, `CALCWRITE`, `MULTIREP`, import/export, commit,
          rollback, and table-buffer operations should carry mutates/risk,
          dirty/stale, buffered/unbuffered, and proof-status information before
          public promotion.
        </p>
      </section>
    </SectionPage>
  );
}
