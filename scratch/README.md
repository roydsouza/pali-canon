🏠 [[INDEX|Dashboard]]

# Pali Canon Obsidian Vault — Scratch Tooling
[[INDEX|Dashboard]] > [[topics/topics|Topics Hub]] > [[topics/texts/texts|Texts & Canon]] > [[topics/texts/pali-canon/pali-canon|Pāḷi Canon]] > Pali Canon Obsidian Vault — Scratch Tooling

This directory contains utility scripts, generators, inspectors, and testing tools designed to automate the curation, migration, indexing, and link integrity of the Pali Canon Obsidian Vault.

## Directory Structure

- **`lib/`**: Contains unified utility library (`pali_utils.py`) with shared logic for XML cleaning, CSCD parsing, frontmatter extraction, and vault path resolution.
- **`crosslinkers/`**: Scripts that parse the vault and establish paragraph-level or chapter-level wikilink commentary callouts between Mūla, Atthakathā, and Ṭīkā layers.
- **`generators/`**: Automated crawlers and parsers that download XML files from tipitaka.org and JSON from SuttaCentral to produce segment-interleaved bilingual markdown files.
- **`inspect/`**: Ad-hoc inspection scripts used to analyze CSCD file structures, verify divisions, and map paragraph offsets.
- **`tests/`**: Automated unit tests using `unittest` and manual integration probes.

---

## Configuration & Environment Variables

To keep scripts portable across different machines, all scripts support path resolution via the `PALI_VAULT` environment variable.

- **Default Vault Path**: `/Users/rds/pali_canon`
- **Overriding Vault Path**:
  ```bash
  export PALI_VAULT="/path/to/your/pali_canon"
  ```

---

## Validation and Guardrails

### 1. Run Unit Tests
To run the unified unit-test suite checking the parser and clean utilities:
```bash
python3 scratch/tests/run_all_tests.py
```

### 2. Run Link Validator
To scan the entire vault for broken relative wikilinks and anchors:
```bash
python3 scratch/validate_links.py
```

### 3. Git Pre-Commit Hook
A Git pre-commit hook is installed at `.git/hooks/pre-commit` to act as an automated validation guardrail. It automatically runs the link validator before every commit and blocks commits if any broken links or references are found.
