---
id: tutorial_07
title: "Tutorial 7: Vocabulary Spaced Repetition (SRS)"
type: tutorial
tags:
  - tutorial
  - srs
  - flashcards
  - vocabulary
  - nlp
---

# Tutorial 7: Vocabulary Spaced Repetition (SRS)

**Navigation**: [[INDEX|Vault Home]] / [[tutorial/INDEX|Tutorials]] / ← [[tutorial/06_building_a_practice|Tutorial 6]]

---

## 1. Concise Reference (Quick Start)

The `pali-srs` tool is part of the `pali-nlp` companion suite. It automatically extracts Pali headwords from the vault's Mūla suttas, retrieves their grammatical categories and English meanings using the Digital Pāḷi Dictionary (DPD), and generates flashcards for the **Obsidian Spaced Repetition** plugin.

### CLI Quick Start
Before running, make sure your Python environment is active and `PALI_VAULT` points to your vault directory:
```bash
cd ~/pali-nlp && source .venv/bin/activate
export PALI_VAULT=/Users/rds/pali_canon
```

Generate cards using one of the primary modes:
```bash
# Mode A: Sutta-specific vocabulary (e.g., MN 10)
pali-srs --sutta MN10

# Mode B: Core canon vocabulary (e.g., top 200 most frequent headwords)
pali-srs --top 200

# Mode C: Generate cards for all migrated suttas in the vault
pali-srs --all-suttas
```

*   **Default Output File:** `practice/vocabulary_cards.md` in the vault.
*   **Obsidian Card Format:** Inline double-colon cards: `Pali word :: [POS] Meaning`.
*   **Flashcard Deck Organization:** Automatically organized into Obsidian sub-decks (e.g., `Vocabulary/MN10`, `Vocabulary/Core200`).

---

## 2. Comprehensive Reference

### CLI Options and Parameters
The CLI executable `pali-srs` (registered from `src/pali_nlp/scripts/write_srs_cards.py`) accepts the following options:

| Flag | Env Variable | Default | Description |
|---|---|---|---|
| `--vault DIRECTORY` | `PALI_VAULT` | Required | Path to the `pali-canon` vault root directory. |
| `--dpd PATH` | `PALI_DPD` | `~/Library/.../dpd.sqlite3` | Path to the DPD SQLite database. Defaults to Simsapa's macOS location. |
| `--sutta TEXT` | — | `None` | Sutta ID (case-insensitive, e.g. `MN10`) to generate cards for. |
| `--all-suttas` | — | `False` | Walk all suttas in the vault and generate cards for each. |
| `--top INTEGER` | — | `None` | Generate flashcards for the top N most frequent headwords in the corpus. |
| `--min-rank INTEGER` | — | `50` | Excludes top-N common words (e.g. 50) to filter basic terms. Ignored when using `--top`. |
| `--max-cards INTEGER` | — | `50` | Cap on the number of cards generated per block (per sutta or top-N deck). |
| `--out PATH` | — | `practice/vocabulary_cards.md` | Custom output file path for cards in the vault. |
| `--dry-run` | — | `False` | Run analysis and report what would be updated without writing to disk. |

### Block Structure & Idempotency
Cards are written into the output file using block sentinels:
```markdown
<!-- pali-nlp:srs-start target=sutta:MN10 -->
### MN10: Satipaṭṭhānasutta
<!-- card-deck: Vocabulary/MN10 -->

natthi :: [pr] is not; there is not
vutta :: [pp] sown; planted
...
<!-- pali-nlp:srs-end target=sutta:MN10 -->
```
*   **In-Place Replacement:** The script searches the output file for block tags matched to the specified target. If found, they are replaced in-place. If missing, they are appended.
*   **Deletion:** If `--sutta` is called but returns zero cards (or the cards list is empty), the target block is automatically deleted from the file to prevent empty placeholders.

---

## 3. Comprehensive Tutorial

This tutorial guides you through setting up Obsidian and generating flashcards to learn Pali vocabulary systematically.

### Step 1: Install and Configure Obsidian Spaced Repetition
1. In Obsidian, open **Settings** > **Community plugins**.
2. Search for and install **Spaced Repetition** (by st3v3nmw). Enable it.
3. Open the **Spaced Repetition** settings panel:
    *   **Flashcard tags:** Add `flashcards` to ensure the plugin scans the vocabulary file.
    *   **Flashcard categories:** Ensure **Inline flashcards** (double colons `::`) are enabled.
    *   **Notes folder:** If you want to isolate flashcards, configure it to look in `practice/` or leave it global.

### Step 2: Initialize Your Vocabulary File
Run the `pali-srs` CLI tool to generate your first deck. For example, let's build cards for the Satipaṭṭhānasutta (MN 10) and the top 200 core words:
```bash
# 1. Generate MN 10 cards (skipping the top 50 most common words)
pali-srs --sutta MN10 --min-rank 50

# 2. Generate a Core 200 deck (includes the most common words)
pali-srs --top 200
```
This creates [[practice/vocabulary_cards|practice/vocabulary_cards.md]] containing both card blocks.

### Step 3: Open the Spaced Repetition Pane in Obsidian
1. Click the **Spaced Repetition** sidebar icon on the Obsidian ribbon (looks like a calendar/card deck).
2. You will see a flashcard deck tree:
    *   `Vocabulary`
        *   `MN10`
        *   `Core200`
3. Click **Review** on the deck you want to study.
    *   The front of the card displays the Pali headword (e.g. `bojjhaṅga`).
    *   Click **Show Answer** to reveal the part of speech and DPD meaning (e.g. `[masc] element of awakening; factor of enlightenment`).
    *   Select your recall level (**Easy**, **Good**, or **Hard**). The plugin schedules the next review automatically.

### Step 4: Establish a Learning Workflow
For the most efficient vocabulary retention, integrate card generation into your sutta studies:

1.  **Start with the Core:** Review `Vocabulary/Core200` to master the structural grammar particles, pronouns, and verbs (`ta`, `ya`, `viharati`) that form 80% of all canonical text lines.
2.  **Study Before Reading:** If you are about to read a new sutta (e.g. DN 9), run `pali-srs --sutta DN9` to build its flashcard block. Spend 5 minutes reviewing the cards *first* to seed the definitions in your mind.
3.  **Read and Contextualize:** Read the sutta. When you encounter terms you just reviewed, your brain will lock onto them in their syntactic context.
4.  **Prune the Noise:** By setting `--min-rank 50` (or higher), you ensure that your sutta decks only quiz you on *fresh* vocabulary, preventing you from reviewing common terms like `bhikkhu` or `dhamma` repeatedly.
