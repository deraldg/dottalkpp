import { SectionPage } from "@/components/SectionPage";
import { dotscriptTopics } from "@/lib/site-data";

export default function DotScriptPage() {
  return (
    <SectionPage
      eyebrow="DotScript"
      title="Readable Scripts For Repeatable Work"
      intro="DotScript documentation should explain the command-language syntax without overstating planned runtime behavior."
      items={dotscriptTopics}
    >
      <section className="section split">
        <div>
          <h2>Current Coverage Target</h2>
          <p>
            Syntax pages should cover comments, continuation, variables, IF,
            LOOP, WHILE, UNTIL, SCAN/ENDSCAN, nesting limits, examples, and
            mutation-safe automation.
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
    </SectionPage>
  );
}
