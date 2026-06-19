🏠 [[INDEX|Dashboard]]

# Agent Skill Guide — Vault Migration & Cross-linking
[[INDEX|Dashboard]] > [[topics/topics|Topics Hub]] > [[topics/texts/texts|Texts & Canon]] > [[topics/texts/pali-canon/pali-canon|Pāḷi Canon]] > Agent Skill Guide — Vault Migration & Cross-linking

This guide details the custom agent skills, automated workflows, and validation guardrails developed for the Pali Canon Obsidian Vault. Any future agent starting a session in this vault should review this document to align on methodology.

---

## 1. Skill: Paragraph-Level Cross-Linking

We have developed a highly automated generic cross-linker script that dynamically aligns the three text layers (Mūla, Atthakathā, and Ṭīkā) using Pali text normalization.

### Execution Command
To cross-link a sutta that has paragraph-numbered comments (e.g., `(234) **Pali Phrase**` style comments in the commentary):
```bash
python3 scratch/crosslinkers/crosslink_generic.py \
  --mula mula/sutta/majjhima_nikaya/mn22.md \
  --att atthakatha/sutta/majjhima_nikaya/mn22_att.md \
  --tik tika/sutta/majjhima_nikaya/mn22_tik.md
```

### How the Alignment Algorithm Works:
1. **Atthakathā Scan**: The script scans the Atthakathā file for paragraphs starting with `(NNN) **Pali Phrase**ti` or `(NNN) **Pali Phrase**nti`.
2. **Anchor Extraction**: It extracts the `Pali Phrase` as the commentary anchor.
3. **Pali Normalization**: Both the extracted anchor and the Mūla text are normalized by:
   - Converting characters to lowercase.
   - Stripping all markdown bold tags (`*`) and punctuation.
   - Translating all Pali diacritics/accents to their flat ASCII equivalents (e.g., `ā` → `a`, `ī` → `i`, `ū` → `u`, `ṅ`/`ñ`/`ṇ` → `n`, `ṭ` → `t`, `ḍ` → `d`, `ḷ` → `l`, `ṁ`/`ṃ` → `m`).
4. **Fuzzy Substring Matching**: The script performs a substring scan in the Mūla file to locate the line containing the normalized anchor.
5. **Callout Injection**: It prepends a collapsed Obsidian callout box (linking to the commentary and sub-commentary paragraph anchors) immediately before the matched Mūla line. It also injects corresponding markdown headings (`### §NNN`) and cross-layer links in the Atthakathā and Ṭīkā files.
6. **Idempotency Guarantee**: The script checks if the target links are already present before making any insertions, preventing duplication on subsequent runs.

---

## 2. Skill: Vault Integrity Validation

### Link Validator
To ensure that all Obsidian wikilinks and relative file paths resolve successfully:
```bash
python3 scratch/validate_links.py
```
This script acts as the definitive test of vault structural health. It performs full anchor-level lookup across all files.

### Unit Tests
To run unit tests asserting the correct behavior of the decoding, cleaning, and frontmatter parsing libraries:
```bash
python3 scratch/tests/run_all_tests.py
```

---

## 3. Active Guardrails

- **Git Pre-commit Hook**: A pre-commit hook is installed at `.git/hooks/pre-commit` which automatically runs `python3 scratch/validate_links.py` before every commit. If any broken links are detected, the commit is rejected.
