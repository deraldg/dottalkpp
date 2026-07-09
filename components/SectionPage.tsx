import Link from "next/link";
import type React from "react";
import { Database } from "lucide-react";

type Item = string | { title: string; text: string };

export function SectionPage({
  eyebrow,
  title,
  intro,
  items,
  children
}: {
  eyebrow: string;
  title: string;
  intro: string;
  items?: Item[];
  children?: React.ReactNode;
}) {
  return (
    <main className="page-shell">
      <section className="page-hero">
        <p className="eyebrow">{eyebrow}</p>
        <h1>{title}</h1>
        <p className="subtitle">{intro}</p>
        <div className="actions">
          <Link href="/">Manual Room Home</Link>
          <Link href="https://x64base.com">x64base.com</Link>
        </div>
      </section>

      {items ? (
        <section className="section">
          <div className="card-grid route-grid">
            {items.map((item) =>
              typeof item === "string" ? (
                <div className="list-item" key={item}>{item}</div>
              ) : (
                <article className="info-card" key={item.title}>
                  <h3>{item.title}</h3>
                  <p>{item.text}</p>
                </article>
              )
            )}
          </div>
        </section>
      ) : null}

      {children}

      <footer>
        <Database aria-hidden="true" />
        <span>
          DotTalk++ documentation room. Ecosystem context remains at{" "}
          <Link href="https://x64base.com">x64base.com</Link>.
        </span>
      </footer>
    </main>
  );
}
