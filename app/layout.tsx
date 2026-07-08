import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "dottalkpp.com DotTalk++ Documentation",
  description:
    "DotTalk++ documentation surface for manuals, generated references, and proof-oriented technical documentation."
};

const navItems = [
  { href: "#manuals", label: "Manuals" },
  { href: "#dotscript", label: "DotScript" },
  { href: "#reference", label: "Reference" },
  { href: "#generated", label: "Generated Docs" },
  { href: "#relationship", label: "Relationship" },
  { href: "#developer", label: "Developer" }
];

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header className="site-header">
          <Link className="brand" href="/">
            DotTalk++
          </Link>
          <nav aria-label="Primary">
            {navItems.map((item) => (
              <a key={item.href} href={item.href}>
                {item.label}
              </a>
            ))}
          </nav>
        </header>
        {children}
      </body>
    </html>
  );
}
