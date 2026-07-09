import { SectionPage } from "@/components/SectionPage";
import { manualItems } from "@/lib/site-data";

export default function ManualsPage() {
  return (
    <SectionPage
      eyebrow="Manuals"
      title="Curated And Versioned Manuals"
      intro="The manual room is for reviewed DotTalk++ manuals, language guides, references, SelfDoc/MDO documentation, and versioned snapshots."
      items={manualItems}
    />
  );
}
