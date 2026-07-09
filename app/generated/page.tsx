import { SectionPage } from "@/components/SectionPage";
import { generatedItems } from "@/lib/site-data";

export default function GeneratedPage() {
  return (
    <SectionPage
      eyebrow="Generated Docs"
      title="Generated First, Reviewed Before Trust"
      intro="Generated reports are evidence shelves. They become public documentation only after review, proof labeling, and provenance checks."
      items={generatedItems}
    />
  );
}
