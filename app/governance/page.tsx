import { SectionPage } from "@/components/SectionPage";
import { authorityFlow, developerItems, gateItems, plannedItems, relationshipItems } from "@/lib/site-data";

export default function GovernancePage() {
  return (
    <SectionPage
      eyebrow="Governance"
      title="Source, Manual, Website, And Accessibility Gates"
      intro="This site supports x64base.com by publishing reviewed DotTalk++ documentation without becoming detached from implementation evidence."
      items={developerItems}
    >
      <section className="section">
        <h2>Cross-Site Relationship</h2>
        <div className="card-grid relationship-grid">
          {relationshipItems.map((item) => (
            <article className="info-card" key={item.title}>
              <h3>{item.title}</h3>
              <p>{item.text}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="section gate-section">
        <h2>Publication Gates</h2>
        <div className="gate-list">
          {gateItems.map((item) => (
            <div key={item}>{item}</div>
          ))}
        </div>
      </section>

      <section className="section split">
        <div>
          <h2>Authority Flow</h2>
          <p>
            Technical claims should move through this chain before becoming
            public-facing documentation.
          </p>
        </div>
        <div className="flow-panel">
          <pre>{authorityFlow.join("\n-> ")}</pre>
        </div>
      </section>

      <section className="section">
        <h2>Planned Lanes Stay Labeled</h2>
        <div className="card-grid relationship-grid">
          {plannedItems.map((item) => (
            <article className="info-card" key={item.title}>
              <h3>{item.title}</h3>
              <p>{item.text}</p>
            </article>
          ))}
        </div>
      </section>
    </SectionPage>
  );
}
