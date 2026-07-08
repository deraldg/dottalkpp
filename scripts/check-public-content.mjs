import { readdir, readFile } from "node:fs/promises";
import path from "node:path";

const root = process.cwd();
const scanDirs = ["app", "components", "config", "content", "public"];
const textExtensions = new Set([
  ".css",
  ".html",
  ".js",
  ".json",
  ".jsx",
  ".md",
  ".mdx",
  ".mjs",
  ".ts",
  ".tsx",
  ".txt",
  ".yml",
  ".yaml"
]);

const blockers = [
  {
    label: "Windows absolute path",
    pattern: /(^|[^A-Za-z])([A-Za-z]:[\\/][^`"'<>\r\n)]*)/g
  },
  {
    label: "User profile path",
    pattern: /C:[\\/]Users[\\/]deral\b/gi
  },
  {
    label: "AppData path",
    pattern: /\bAppData\b/gi
  },
  {
    label: "Temp clipboard path",
    pattern: /codex-clipboard|[\\/]Temp[\\/]/gi
  },
  {
    label: "Private Office artifact link",
    pattern: /(?:href|src)=["'][^"']+\.(?:pptx|docx|xlsx)["']/gi
  },
  {
    label: "Financial positioning language",
    pattern: /\b(?:profit|investor|investment return|commercial strategy|revenue model)\b/gi
  }
];

async function* walk(dir) {
  let entries;
  try {
    entries = await readdir(dir, { withFileTypes: true });
  } catch (error) {
    if (error.code === "ENOENT") {
      return;
    }
    throw error;
  }

  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      yield* walk(fullPath);
    } else if (textExtensions.has(path.extname(entry.name).toLowerCase())) {
      yield fullPath;
    }
  }
}

const findings = [];

for (const scanDir of scanDirs) {
  for await (const file of walk(path.join(root, scanDir))) {
    const content = await readFile(file, "utf8");
    for (const blocker of blockers) {
      blocker.pattern.lastIndex = 0;
      const matches = content.match(blocker.pattern);
      if (matches) {
        findings.push({
          file: path.relative(root, file),
          label: blocker.label,
          matches: [...new Set(matches)].slice(0, 3)
        });
      }
    }
  }
}

if (findings.length > 0) {
  console.error("Public content guard failed:");
  for (const finding of findings) {
    console.error(`- ${finding.file}: ${finding.label}`);
    for (const match of finding.matches) {
      console.error(`  ${match}`);
    }
  }
  process.exit(1);
}

console.log("Public content guard passed.");
