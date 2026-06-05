# Roadmap: Pali Canon Vault

*Created 2026-05-22. Tracks execution phases from current state to full practicing Buddhist's canonical library.*
*Companion to [VISION.md](VISION.md) (scope & principles) and [TASKS.md](TASKS.md) (granular checklist).*

---

## Phase 0 — Get Well (Immediate Fixes)

Address the five ongoing issues identified in the initial bootstrap prompt (since removed).

| Issue | Fix | Effort |
|---|---|---|
| **A. Commit hygiene** | Establish commit protocol: commit after each sutta (all layers) or at minimum after each batch. Add protocol to this doc. | 5 min |
| **C. STATUS.md stale script count** | Update "17 reusable Python scripts" → actual count. Categorize by type. | 5 min |
| **D. TASKS.md Snp entry imprecise** | Clarify what remains: Chapters 2, 3, 4, 5. | 5 min |
| **E. DN 1/16/21 missing mātikā links** | Add forward mātikā links + reverse links in mātikā files. | 15 min |
| **B. scratch/ folder cleanup** | *Deferred* — cosmetic, doesn't block content work. Revisit after Phase 8. | — |

### Commit Protocol (Issue A Resolution)

From this point forward, every agent session must:
1. **Commit after each sutta** (all layers: mūla + att + tīkā) with message format: `feat: migrate [ID] [Name] (mūla/att/tīkā)`
2. **Commit after each batch** of cross-linking or mātikā work with message: `feat: cross-link [scope]`
3. **Never leave more than 5 uncommitted sutta files** in the working tree.
4. **Update TASKS.md** before and after each block of work.
5. **Update SYNC_LOG.md** after each block of work (per user memory protocol).

---

## Phase 6 — Sutta Nipāta Completion (Completed)

*Prerequisite*: Phase 0 complete.
*Scope*: Chapters 2–5 (Chapter 1 Uragavagga already done: 12 suttas).
*Layers*: Mūla (interleaved Pali/English) + Atthakathā (CSCD Pali). No Ṭīkā exists for Snp.

### 6a — Chapter 2: Cūḷavagga (14 suttas)
- snp2.1 Ratanasutta → **paritta** cross-link
- snp2.4 Maṅgalasutta → **paritta** cross-link
- snp2.6 Dhammacariyasutta
- snp2.7 Brāhmaṇadhammikasutta
- All 14 suttas: snp2.1–snp2.14
- **Mātikā links**: five_precepts, three_refuges, four_sublime_states
- **Commit**: After all 14 + atthakathā

### 6b — Chapter 3: Mahāvagga (12 suttas)
- snp3.1 Pabbajjāsutta (the Going Forth)
- snp3.7 Selasutta (brahmin conversion)
- snp3.11 Nālakasutta (instructions to Nālaka)
- snp3.12 Dvayatānupassanāsutta (contemplation of dualities — vipassanā-relevant)
- All 12 suttas: snp3.1–snp3.12
- **Mātikā links**: noble_eightfold_path, dependent_origination, three_marks
- **Commit**: After all 12 + atthakathā

### 6c — Chapter 4: Aṭṭhakavagga (16 suttas)
- snp4.1–snp4.16
- Among the oldest strata of the canon; non-clinging, letting go of views
- **Mātikā links**: three_marks, five_aggregates
- **Commit**: After all 16 + atthakathā

### 6d — Chapter 5: Pārāyanavagga (16 questions)
- snp5.1–snp5.19 (intro + 16 questions + 2 epilogues)
- Dense, terse poetry; the Buddha's answers to 16 students
- **Mātikā links**: four_noble_truths, dependent_origination
- **Commit**: After all + atthakathā

### 6e — Snp Cross-linking & INDEX
- Update `khuddaka_nikaya/sutta_nipata/INDEX.md` with all 5 chapters
- Run link validator
- Verify all mātikā bidirectional links

**📋 Evaluation Checkpoint**: Read Snp Chapters 2 and 4 in Obsidian. Are the paritta texts useful? Does the Aṭṭhakavagga feel integrated with the mātikā web?

---

## Phase 7 — Itivuttaka (Completed) (112 short discourses)

*Prerequisite*: Phase 6 complete + evaluation.
*Scope*: All 112 utterances in 4 nipātas.
*Layers*: Mūla (interleaved Pali/English) + Atthakathā (CSCD Pali, if available).

### 7a — Nipāta 1 (Ekaka, ones: iti1–iti27)
### 7b — Nipāta 2 (Duka, twos: iti28–iti49)
### 7c — Nipāta 3 (Tika, threes: iti50–iti99)
### 7d — Nipāta 4 (Catukka, fours: iti100–iti112)

- SuttaCentral IDs: `iti1`–`iti112`; Sujato translation
- **Mātikā links**: four_noble_truths, three_marks, noble_eightfold_path, three_unwholesome_roots
- **Commit**: After each nipāta batch
- **INDEX**: `khuddaka_nikaya/itivuttaka/INDEX.md`
- Run link validator after completion

**📋 Evaluation Checkpoint**: Is the three-layer structure still manageable with ~350+ files? Is INDEX navigation quick?

---

## Phase 8 — Theragāthā / Therīgāthā (Completed)

*Prerequisite*: Phase 7 complete + evaluation.
*Layers*: Mūla only (interleaved Pali/English). No commentary required.

### 8a — Theragāthā (Monks' Verses)
- ~264 poems in 21 chapters (Sujato translation)
- **Mātikā links**: four_sublime_states, noble_eightfold_path

### 8b — Therīgāthā (Nuns' Verses)
- ~73 poems (Sujato translation)
- **Mātikā links**: four_sublime_states, four_foundations_of_mindfulness

- **Commit**: After each collection
- Run link validator after completion

**📋 Evaluation Checkpoint**: With ~400+ files, is the vault still navigable? Time to add Dataview query blocks to INDEX files if not already done.

---

## Phase 9 — Practice-Oriented Expansion (Completed)

*Prerequisite*: Phase 8 complete.
*Purpose*: Migrate suttas that directly support the seven practice domains. Each sub-phase also creates a thematic reading path in `paths/`.

### 9a — Jhāna Deepening
| Sutta | Description | Layers |
|---|---|---|
| MN 128 | Upakkilesasutta — jhāna obstacles | mūla + att + tīk |
| AN 9.34 | Nibbānasukhasutta — nibbāna through jhāna | mūla + att + tīk |
| AN 9.35 | Gāvīupamāsutta — cow simile for jhāna | mūla + att + tīk |
| MN 8 | Sallekhasutta — self-effacement | mūla + att + tīk |
| AN 8.63 | Saṅkhittasutta — brief jhāna instruction | mūla + att + tīk |

- **New mātikā**: `four_jhanas` (cattāri jhānāni)
- **Reading path**: `paths/entering_jhana.md`
- **Commit**: After each sutta

### 9b — Vipassanā Broadening
| Sutta | Description | Layers |
|---|---|---|
| MN 148 | Chachakkasutta — six sets of six | mūla + att + tīk |
| SN 36 (selected) | Vedanāsaṃyutta — feeling | mūla + att + tīk |
| MN 28 | Mahāhatthipadopamasutta — four elements | mūla + att + tīk |
| MN 140 | Dhātuvibhaṅgasutta — six elements | mūla + att + tīk |
| MN 2 | Sabbāsavasutta — removing taints | mūla + att + tīk |

- **Reading path**: `paths/vipassana_practice.md`
- **Commit**: After each sutta

### 9c — Brahmavihāra Practice
| Sutta | Description | Layers |
|---|---|---|
| MN 7 | Vatthūpamasutta — simile of the cloth | mūla + att + tīk |
| DN 13 | Tevijjasutta — brahmavihāra as path | mūla + att + tīk |
| AN 11.15 | Mettānisaṃsasutta — 11 benefits | mūla + att + tīk |
| AN 4.125–126 | Mettāsutta — mettā + rebirth | mūla + att + tīk |
| SN 46.54 | Mettāsahagatasutta — brahmavihāra + bojjhaṅga | mūla + att + tīk |

- **Reading path**: `paths/brahmavihara_cultivation.md`
- **Commit**: After each sutta

### 9d — Anussati (Recollections)
| Sutta | Description | Layers |
|---|---|---|
| AN 6.10 | Mahānāmasutta — six recollections | mūla + att + tīk |
| AN 11.12 | Mahānāmasutta — expanded | mūla + att + tīk |
| AN 6.25 | Anussatiṭṭhānasutta — recollection topics | mūla + att + tīk |

- **New mātikā**: `six_recollections` (cha anussati)
- **Reading path**: `paths/anussati_practice.md`
- **Commit**: After each sutta

### 9e — Anupubbasikkhā (Gradual Training)
| Sutta | Description | Layers |
|---|---|---|
| MN 27 | Cūḷahatthipadopamasutta — elephant footprint | mūla + att + tīk |
| MN 51 | Kandarakasutta — four types of persons | mūla + att + tīk |
| AN 8.54 | Dīghajāṇusutta — householder's path | mūla + att + tīk |
| AN 4.99 | Sikkhāpadasutta — training precepts | mūla + att + tīk |

- **New mātikā**: `gradual_training` (anupubbasikkhā)
- **Reading path**: `paths/gradual_training.md`
- **Commit**: After each sutta

### 9f — Maraṇasati (Death Contemplation)
| Sutta | Description | Layers |
|---|---|---|
| AN 6.19 | Maraṇassatisutta — first discourse | mūla + att + tīk |
| AN 6.20 | Maraṇassatisutta — second discourse | mūla + att + tīk |
| AN 8.73 | Maraṇassatisutta — eight directions | mūla + att + tīk |
| SN 47.13 | Cundasutta — Sāriputta's parinibbāna | mūla + att + tīk |

- **Reading path**: `paths/maranasati.md`
- **Commit**: After each sutta

### 9g — Paritta Collection
- Create `paritta/INDEX.md` with recitation order:
  1. Snp 1.8 (Mettasutta — already in vault)
  2. Snp 2.1 (Ratanasutta — from Phase 6)
  3. Snp 2.4 (Maṅgalasutta — from Phase 6)
  4. AN 4.67 (Ahisutta — migrate: mūla + att + tīk)
- Cross-link all paritta to `three_refuges` mātikā
- **Commit**: After INDEX + AN 4.67

**📋 Evaluation Checkpoint**: Do the reading paths feel natural? Are you using them during practice? Are the new mātikā lists well-integrated?

---

## Phase 10 — AN Expansion (Completed)

*Prerequisite*: Phase 9 complete.
*Purpose*: Fill the remaining AN nipāta gaps.

- AN 7 (selected suttas, focus on AN 7.65 — seven awakening factors)
- AN 8 (selected suttas, focus on AN 8.53 — dāna/sīla/bhāvanā sequence)
- AN 11 (selected suttas, focus on AN 11.1–5 — ānāpānasati series)
- AN 1 (Ekakanipāta — very short single-factor suttas; batch migration)
- All three layers where CSCD commentary exists
- **Commit**: After each nipāta batch

---

## Phase 11 — Deeper MN Coverage (Completed)

*Prerequisite*: Phase 10 complete.

- MN 117 (Mahācattārīsakasutta — right view, mundane/supramundane)
- MN 22 (Alagaddūpamasutta — snake simile, non-clinging to views)
- Any additional MN suttas identified during Phase 9 practice reading
- All three layers
- **Commit**: After each sutta

---

## Phase 12 — Vinaya Pātimokkha (Completed)

*Prerequisite*: Phase 11 complete.

- Bhikkhu Pātimokkha preamble and categories (Thanissaro translation)
- Selected rules with direct bearing on lay practice context
- Cross-link to five_precepts, eight_precepts
- `vinaya/INDEX.md`
- **Commit**: After each category

---

## Phase 13 — Practice Support Tooling (Completed)

*Prerequisite*: Phase 9 reading paths complete.
*Purpose*: Make the vault actively useful during practice.

### 13a — Practice Notes Infrastructure
- Create `practice/` folder
- Create practice note template (Templater)
- Dataview query: "recently revisited" and "flagged as important"

### 13b — Verse Memorization Log
- `practice/memorization_log.md`
- Fields: sutta ref, Pali text, English, date added, last reviewed, status

### 13c — Dataview Query Blocks
- Add live sutta lists to all nikāya INDEX files
- Add "recently modified" dashboard to main INDEX.md

---

## Phase 14 — Abhidhamma (Future, Conditional)

*Only if the canonical sutta content reaches saturation and the user requests it.*

- Abhidhammatthasaṅgaha mūla (Bhikkhu Bodhi)
- Dhammasaṅgaṇī, Vibhaṅga (mātikā cross-links for five aggregates)

---

## Phase 15 — Vault Hygiene, Consistency & Chanting Fixes

*Focus on standardizing file naming, fixing broken features, and setting up multi-agent guardrails.*

- **Chanting Audio Player Fix**: Replace broken `file://` absolute paths in `meta/CHANTING.md` and monastic files with vault-relative wikilink embeds `! [ [ audio_file.mp3 ] ]` to render Obsidian's native audio player, and remove folder link stubs.
- **Dotted Filename Refactor**: Write a python script to rename all 422 dotted filenames (`snp1.1.md` -> `snp1_1.md`) and rewrite all wikilinks vault-wide to maintain a clean, shell-tool-friendly naming convention.
- **Frontmatter Schema Validation**: Add a frontmatter schema linter (`scratch/inspect/lint_frontmatter.py`) and wire it into the unit tests to enforce required keys by note type.
- **AN Chunking Alignment**: Implement `covers:` (list) / `part_of:` fields to handle suttas mapped to grouped commentary/ṭīkā files.
- **SYNC_LOG Rotation**: Rotate entries older than 30 days in `meta/SYNC_LOG.md` into `meta/sync_archive/SYNC_LOG_YYYY-MM.md` to limit file size overhead.
- **CLAUDE.md Guardrails**: Create a project-level `CLAUDE.md` to define standard procedures, formatting, and validation scripts for new agents.

---

## Phase 16 — Study Station Enhancements

*Markdown-native enhancements to the vault's reading environment, serving as the bridge to NLP.*

- **Prosopography Graph**: Seed manual people (`people/`) and place (`places/`) index notes.
- **Simile Index**: Build a cross-referenced catalogue of canon similes.
- **Pericope Concordance**: Map out repeated formulas (jhāna cadences, dependent origination chains) with links to occurrences.
- **Parallel-Texts Layer**: Inject SuttaCentral parallel IDs into frontmatter and render via Dataview.
- **Question-Driven Paths**: Add thematic reading paths (e.g. "working with anger", "facing death") under `paths/`.

---

## Phase 17 — Pali NLP Companion Development (External Repo)

*Development of the companion `pali-nlp` repository to process vault texts and write back reading aids.*

- **Stage 1: Graded Reader & Gloss (3A)**: Extract vocabulary, lemmatize against DPD, append vocabulary concordance tables to suttas (Option C), and build the vocabulary-based reading ladder.
- **Stage 2: Linguistic Pipeline (3B)**: Build an off-line concordance search index and NER tagger, auto-populating Phase 16 index pages.
- **Stage 3: Semantic Search & RAG (3C)**: Implement local-first vector search and offline LLM generation (e.g. MLX/llama.cpp) with citation links to the vault's paragraph anchors.
- **Stage 4: Performance Porting (3D)**: Re-write performance-critical tokenizer and sandhi-splitting layers in Rust.

---

## New Mātikā Lists (Cumulative)

| Mātikā | Phase | Cross-links |
|---|---|---|
| `four_jhanas` | 9a | MN 111, AN 9.36, MN 128, DN 2, MN 52 |
| `six_recollections` | 9d | AN 6.10, AN 11.12, AN 6.25 |
| `gradual_training` | 9e | DN 2, MN 27, MN 51, AN 8.54 |

---

## Summary Statistics (Actual & Projected)

| Milestone | Files | Suttas | Mātikā | Description |
|---|---|---|---|---|
| Current State (May 2026) | 1,161 | ~750 | 22 | Completed Phases 1-13; repository pushed to remote |
| After Phase 15 | 1,161 | ~750 | 22 | Vault hygiene, dotted names refactored, audio fixed |
| After Phase 16 | ~1,200 | ~750 | 22 | Prosopography, simile, and pericope index pages added |
| After Phase 17 | ~1,200 | ~750 | 22 | Appended vocabulary concordance tables and SRS cards added |

