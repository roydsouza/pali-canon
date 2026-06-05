#!/usr/bin/env python3
"""Fix all markdown [label](path.md) links in matika/*.md files.

Converts them to Obsidian wikilinks and fixes broken/misleading references:
  - mn9.md (not in vault) → context-specific replacement or removal
  - mn58.md (not in vault) → remove line
  - wrong folder for an10_60 → correct to anguttara_nikaya
  - SN INDEX.md links labelled as specific suttas → link to actual sn file
  - matika internal [matika/xxx](xxx.md) → [[xxx|Title]]
"""
import os
import re
import glob

VAULT = os.environ.get("PALI_VAULT", "/Users/rds/pali_canon")
MATIKA_DIR = os.path.join(VAULT, "matika")

# Matika internal link display names (filename stem → display title)
MATIKA_TITLES = {
    "three_unwholesome_roots": "Three Unwholesome Roots",
    "four_sublime_states": "Four Brahmavihārās",
    "eight_precepts": "Eight Precepts",
    "four_right_exertions": "Four Right Exertions",
    "right_effort": "Right Effort",
    "seven_purifications": "Seven Purifications",
    "ten_fetters": "Ten Fetters",
    "right_intention": "Right Intention",
    "five_precepts": "Five Precepts",
    "eight_precepts": "Eight Precepts",
    "ten_perfections": "Ten Perfections",
    "three_refuges": "Three Refuges",
    "noble_eightfold_path": "Noble Eightfold Path",
    "four_noble_truths": "Four Noble Truths",
    "dependent_origination": "Dependent Origination",
    "five_aggregates": "Five Aggregates",
    "five_hindrances": "Five Hindrances",
    "seven_awakening_factors": "Seven Awakening Factors",
    "four_foundations_of_mindfulness": "Four Foundations of Mindfulness",
    "five_spiritual_faculties": "Five Spiritual Faculties",
    "five_powers": "Five Powers",
    "four_jhanas": "Four Jhānas",
    "six_recollections": "Six Recollections",
    "gradual_training": "Gradual Training",
    "four_right_exertions": "Four Right Exertions",
}

# Per-file replacements for mn9.md links:
# key = matika filename stem, value = replacement wikilink line (or None to delete line)
MN9_REPLACEMENTS = {
    "right_view":          "*   [[../mula/sutta/samyutta_nikaya/sn45|SN 45: Maggasaṃyutta]] — the entire connected collection elaborating each path factor including Right View.",
    "greed":               "*   [[../mula/sutta/samyutta_nikaya/sn46|SN 46: Bojjhaṅgasaṃyutta]] — the seven awakening factors as antidotes to greed, sensual desire, and attachment.",
    "hatred":              "*   [[../mula/sutta/majjhima_nikaya/mn20|MN 20: Vitakkasaṇṭhānasutta]] — five techniques for removing aversion and ill-will from the mind.",
    # The following already have sn12 linked; just remove the mn9 line:
    "delusion":            None,
    "existence_or_becoming": None,
    "name_and_form":       None,
    "ignorance":           None,
}

# SN INDEX label → actual sn file stem
SN_INDEX_MAP = {
    "SN 12.2":  ("sn12", "SN 12: Nidānasaṃyutta"),
    "SN 22.59": ("sn22", "SN 22: Khandhasaṃyutta"),
    "SN 22.95": ("sn22", "SN 22: Khandhasaṃyutta"),
    "SN 55":    ("sn55", "SN 55: Sotāpattisaṃyutta"),
    "SN 56.11": ("sn56", "SN 56: Saccasaṃyutta"),
}

# Full descriptions to preserve after the link (lookup by original label)
SN_DESCRIPTIONS = {
    "SN 12.2: Vibhaṅgasutta":               "the Nidāna-saṃyutta's analysis of each dependent-origination link.",
    "SN 22.59: Anattalakkhaṇasutta":         "the Khandha-saṃyutta's systematic refutation of self in the five aggregates.",
    "SN 22.95: Phenapiṇḍūpamasutta":        "the foam/bubble/mirage similes illustrating the insubstantial nature of the five aggregates.",
    "SN 55: Sotāpattisaṃyutta":             "the Sotāpatti-saṃyutta on stream-entry and the four factors of stream-entry.",
    "SN 56.11: Dhammacakkappavattanasutta":  "the Sacca-saṃyutta containing the First Wheel of the Dhamma discourse.",
}

changed_files = []

for md_path in sorted(glob.glob(os.path.join(MATIKA_DIR, "*.md"))):
    stem = os.path.splitext(os.path.basename(md_path))[0]
    with open(md_path, "r", encoding="utf-8") as f:
        original = f.read()
    lines = original.splitlines(keepends=True)
    new_lines = []
    changed = False

    for line in lines:
        # ── 1. Remove lines with broken mn9.md links ──────────────────────────
        if re.search(r'\[.*?\]\(\.\./mula/sutta/majjhima_nikaya/mn9\.md\)', line):
            replacement = MN9_REPLACEMENTS.get(stem)
            if replacement is None:
                # Delete line entirely
                changed = True
                continue
            else:
                new_line = replacement + "\n"
                if new_line != line:
                    changed = True
                new_lines.append(new_line)
                continue

        # ── 2. Remove lines with broken mn58.md links ─────────────────────────
        if re.search(r'\[.*?\]\(\.\./mula/sutta/majjhima_nikaya/mn58\.md\)', line):
            changed = True
            continue  # delete line

        # ── 3. Fix wrong-path an10_60 (majjhima_nikaya → anguttara_nikaya) ────
        if re.search(r'\(\.\./mula/sutta/majjhima_nikaya/an10_60\.md\)', line):
            new_line = line.replace(
                "(../mula/sutta/majjhima_nikaya/an10_60.md)",
                "(../mula/sutta/anguttara_nikaya/an10_60.md)"
            )
            if new_line != line:
                changed = True
            line = new_line

        # ── 4. Fix SN INDEX links labelled as specific suttas ────────────────
        sn_index_match = re.search(
            r'\[([^\]]+)\]\(\.\./mula/sutta/samyutta_nikaya/INDEX\.md\)',
            line
        )
        if sn_index_match:
            label = sn_index_match.group(1)
            # Find the SN prefix key
            matched_key = None
            for k in SN_INDEX_MAP:
                if label.startswith(k):
                    matched_key = k
                    break
            if matched_key:
                sn_stem, sn_title = SN_INDEX_MAP[matched_key]
                desc = SN_DESCRIPTIONS.get(label, "")
                desc_str = f" — {desc}" if desc else ""
                new_link = f"[[../mula/sutta/samyutta_nikaya/{sn_stem}|{sn_title}]]{desc_str}"
                new_line = re.sub(
                    r'\[' + re.escape(label) + r'\]\(\.\./mula/sutta/samyutta_nikaya/INDEX\.md\)',
                    new_link,
                    line
                )
                if new_line != line:
                    changed = True
                line = new_line
            else:
                # Unknown SN label pointing to INDEX — link to sn55 as fallback
                pass

        # ── 5. Convert remaining markdown links to wikilinks ─────────────────
        def convert_md_link(m):
            label = m.group(1)
            path = m.group(2)

            # Matika internal link: e.g. [matika/xxx](xxx.md)
            if not path.startswith(".."):
                stem_name = path.replace(".md", "")
                display = MATIKA_TITLES.get(stem_name, label)
                return f"[[{stem_name}|{display}]]"

            # External link: strip .md → wikilink path
            wikilink_path = path.replace(".md", "")
            return f"[[{wikilink_path}|{label}]]"

        new_line = re.sub(r'\[([^\]]+)\]\(([^)]+\.md)\)', convert_md_link, line)
        if new_line != line:
            changed = True
        line = new_line

        new_lines.append(line)

    if changed:
        new_content = "".join(new_lines)
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        changed_files.append(os.path.basename(md_path))

print(f"Modified {len(changed_files)} files:")
for f in changed_files:
    print(f"  {f}")
