#!/usr/bin/env python3
"""Add How-to-use preamble and difficulty tier headers to graded_reader.md."""
import os, re

VAULT = os.environ.get("PALI_VAULT", "/Users/rds/pali_canon")
PATH = os.path.join(VAULT, "paths", "graded_reader.md")

PREAMBLE_REPLACEMENT = """\
# Pali Graded Reader

518 suttas ranked easiest to hardest by vocabulary difficulty. Use it as a reading ladder:
start at the beginning of your current tier and work forward until each sutta feels comfortable
before moving to the next.

**How to use:**
1. Find your entry tier below (start with Tier 1 if unsure).
2. Open the sutta in the vault; read it with the translation toggle (`Cmd+R`) or the DPD lookup.
3. Before reading a new sutta, run `pali-srs --sutta <ID>` (from pali-nlp) to prime its vocabulary.
4. Once a tier feels comfortable, advance to the next.

**Score** = mean DPD frequency rank of unique non-structural headwords. Lower = more common = easier.
**Tokens** = total Pali word tokens (proxy for length). **Unique Words** = distinct lemmas.

---

"""

TIER_HEADERS = {
    1:   "\n## Tier 1 — Beginner (Ranks 1–50)\n*Mostly short Itivuttaka and AN 1 texts. Very common vocabulary.*\n\n",
    51:  "\n## Tier 2 — Lower Intermediate (Ranks 51–200)\n*Short-to-medium suttas. Familiar practice vocabulary with some technical terms.*\n\n",
    201: "\n## Tier 3 — Upper Intermediate (Ranks 201–400)\n*Medium-length suttas. Expect doctrinal terminology and longer sentences.*\n\n",
    401: "\n## Tier 4 — Advanced (Ranks 401–518)\n*Longer, lexically dense suttas. Rich Abhidhamma-style analysis and rare vocabulary.*\n\n",
}

with open(PATH, "r", encoding="utf-8") as f:
    content = f.read()

if "Tier 1" in content:
    print("Already has tiers; nothing to do.")
    exit(0)

lines = content.splitlines(keepends=True)
new_lines = []
in_table = False

for line in lines:
    # Replace the original short intro block (lines before the table)
    if line.startswith("# Pali Graded Reader"):
        new_lines.append(PREAMBLE_REPLACEMENT)
        in_table = False
        continue

    if line.startswith("Suttas ordered") or line.startswith("Score =") or line.startswith("Lower score"):
        # Drop the old intro lines; they're replaced by PREAMBLE_REPLACEMENT
        continue

    # Detect table header
    if line.startswith("| Rank |"):
        in_table = True

    if in_table and line.startswith("| "):
        # Extract rank from row
        m = re.match(r'\| (\d+) \|', line)
        if m:
            rank = int(m.group(1))
            if rank in TIER_HEADERS:
                new_lines.append(TIER_HEADERS[rank])
                # Re-add table header after each tier section header
                new_lines.append("| Rank | Sutta | Nikāya | Score | Tokens | Unique Words |\n")
                new_lines.append("|---|---|---|---|---|---|\n")
                in_table = True

    new_lines.append(line)

with open(PATH, "w", encoding="utf-8") as f:
    f.write("".join(new_lines))

print("Done — tiers and preamble added.")
