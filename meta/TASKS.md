🏠 [[INDEX|Dashboard]]

# Project Tasks Checklist
[[INDEX|Dashboard]] > [[topics/topics|Topics Hub]] > [[topics/texts/texts|Texts & Canon]] > [[topics/texts/pali-canon/pali-canon|Pāḷi Canon]] > Project Tasks Checklist

This file tracks granular task progress for the Pali Canon Vault.
See [ROADMAP.md](ROADMAP.md) for phase sequencing and [VISION.md](VISION.md) for scope/principles.
**Last updated**: 2026-06-04

---

## Priority Bugs & Issues

- [ ] **Chanting Audio Links Bug** — Absolute and relative links pointing to local files/folders inside the `practice/audio/` directory in `CHANTING.md` (and related monastic files) are not resolved or followed successfully by Obsidian. Requires investigation of Obsidian's protocol handlers on macOS for non-markdown resources.

---

## Review Findings — 2026-06-04

Vault review covering content quality, learning UX, and interface integrity. Items ordered by priority within each category.

### Bugs & Fixes (Critical)

- [x] **Broken links to mn9.md in matika factor files** — fixed by `scratch/fix_matika_links.py`; replaced with correct sutta wikilinks (sn45, mn20, sn46, sn12) ✅
- [x] **validate_links.py gap: markdown `[text](path.md)` links not checked** — extended validator to resolve all `[label](path.md)` links; wikilink count now 15,608 ✅
- [x] **80 matika factor files use markdown links instead of wikilinks** — converted to Obsidian wikilinks vault-wide via `fix_matika_links.py` ✅
- [x] **27 matika factor files: SN links point to INDEX instead of specific suttas** — updated to link to actual sutta files (sn12, sn22, sn55, sn56) ✅

### Bugs & Fixes (High)

- [x] **INDEX.md: "Six tutorials" → "Seven tutorials"** — updated; Dataview filter also added ✅
- [x] **practice/INDEX.md: broken audio embeds** — replaced with `> [!NOTE] Audio not yet configured` callout + links to patimokkha text files ✅
- [x] **Vocabulary concordance: filter out unresolved `(?)` entries before injection** — `vault_writer.py`: `if not r.found: continue`; pali-nlp commit 369a604 ✅

### Bugs & Fixes (Medium)

- [x] **Vocabulary concordance sort order: "rarest first" is wrong for learning** — changed to ascending rank (most-common-first) with `min_rank=30` floor filter; pali-nlp commit 369a604 ✅
- [ ] **Vocabulary concordance callout position: buried at end of sutta** — deferred; requires positional anchor in vault-writer injection logic and full pali-nlp re-run over 508 suttas

### Learning Experience Improvements

- [x] **Simile Index (SIMILES.md): expand** — expanded from 7 to 17 entries across 5 categories ✅
- [x] **Pericope Concordance (PERICOPES.md): expand** — expanded from 4 to 13 entries across 5 categories with full Pali + English text ✅
- [x] **Reading paths: add per-sutta progress checkboxes** — added collapsible Reading Progress callout to all 9 reading paths via `scratch/add_path_progress.py` ✅
- [x] **Graded reader: add difficulty tier groupings and "How to use" preamble** — four tiers (Beginner/Lower/Upper Intermediate/Advanced) + preamble added ✅
- [x] **Contemplation prompts on the three core meditation suttas** — `> [!QUESTION]- Practice Questions` callout added to MN 10, MN 118, DN 22 ✅
- [ ] **Theragāthā/Therīgāthā: migrate Paramatthadīpanī commentary** — deferred to Phase 21
- [ ] **Phase 21 priority sutta queue: MN 26, MN 63, MN 72, SN 1** — see Phase 21 section below; also add Thag/Thig Paramatthadīpanī

### Interface Quality Improvements

- [x] **INDEX.md "Recently Modified" Dataview: add type filter** — filter added: mula / practice / matika / path / tutorial ✅
- [x] **practice/INDEX.md: add "Currently studying" section** — manually-maintained table added ✅
- [x] **paths/INDEX.md: verify it lists all 10 paths** — verified; all 10 paths linked with descriptions ✅
- [x] **Mātikā INDEX: add factor count and "entry points" section** — "Recommended Entry Points" table added with 10 practice questions ✅
- [x] **SIMILES.md and PERICOPES.md: linked from INDEX.md** — links present with descriptive labels in Mātikā card ✅

---

## Phase 21 — Priority Queue

*Next major phase. Gate: Phase 20B samatha arc must be at least 50% complete.*

### Phase 21A — High-Priority Suttas (not yet in vault)

- [ ] **MN 26: Ariyapariyesanā** — the First Teaching narrative; Buddha's hesitation before teaching; noble vs ignoble search
- [ ] **MN 63: Cūḷamāluṅkya** — the poisoned arrow; unanswered metaphysical questions; what the teaching is and isn't for
- [ ] **MN 72: Aggivacchagotta** — fire simile for nibbāna; clearest canonical statement on what happens to a Tathāgata after liberation
- [ ] **SN 1 (Devatāsaṃyutta)** — short verse dialogues with devas; highly readable; excellent graded-reader Tier 1 material

### Phase 21B — Commentary Expansion

- [ ] **Theragāthā/Therīgāthā: migrate Paramatthadīpanī** — select 30–40 poems; Dhammapāla's 6th-c. commentary provides elder biographies and verse interpretation

### Phase 21C — Vocabulary Re-run

- [ ] **pali-nlp re-run over all 508 suttas** — regenerate vocab concordance blocks with updated sort order (most-frequent-first) and filtered unresolved entries; run `pali-write --all-suttas` from the pali-nlp repo

---

## Phase 0 — Get Well (FROM-CLAUDE.md Issues)


- [x] **A. Commit protocol** — Establish commit-after-each-sutta discipline; document in ROADMAP.md ✅ (protocol written)
- [x] **C. STATUS.md script count** — Update "17 reusable Python scripts" to actual count (~94); categorize by type
- [x] **D. TASKS.md Snp entry** — Clarify remaining Snp scope: Chapters 2 (14 suttas), 3 (12), 4 (16), 5 (16+)
- [x] **E. DN mātikā links** — Add forward mātikā links to DN 1, 16, 21 + reverse links in mātikā files
- [x] **B. scratch/ cleanup** — move generators to `scratch/generators/`, archive inspect/test scripts ✅ (scratch/ cleaned and organized)

---

## Completed Work

### Phase 1 — Core Meditation Suttas (all three layers)
- [x] MN 10: Satipaṭṭhānasutta — 5,721w / 362¶+49 notes / 232¶
- [x] MN 20: Vitakkasaṇṭhānasutta — 1,798w / 40¶+11 notes / 26¶
- [x] MN 119: Kāyagatāsatisutta — 4,967w / 10¶+18 notes / 8¶
- [x] MN 121: Cūḷasuññatasutta — 2,760w / 13¶+15 notes / 11¶
- [x] DN 2: Sāmaññaphalasutta — 17,701w / 394¶+141 notes / 259¶
- [x] AN 4.41: Samādhibhāvanāsutta — 745w / 15¶ / 18¶

### Phase 2 — Meditation Sutta Expansion (all three layers)
- [x] MN 36: Mahāsaccakasutta — 9,139w / 34¶+25 notes / 32¶
- [x] MN 43: Mahāvedallasutta — 3,877w / 60¶+30 notes / 54¶
- [x] MN 44: Cūḷavedallasutta — 3,096w / 39¶+27 notes / 40¶
- [x] MN 52: Aṭṭhakanāgarasutta — 1,696w / 14¶+14 notes / 10¶
- [x] MN 111: Anupadasutta — 2,272w / 26¶+18 notes / 38¶
- [x] MN 118: Ānāpānasatisutta — 3,522w / 18¶ / 16¶; §-anchors + callouts done
- [x] DN 9: Poṭṭhapādasutta — 8,837w / 57¶+67 notes / 72¶; §-anchors done
- [x] DN 15: Mahānidānasutta — 6,706w / 138¶+80 notes / 122¶; §-anchors done
- [x] DN 22: Mahāsatipaṭṭhānasutta — 8,892w / 293¶+78 notes / 236¶
- [x] AN 3.100: Loṇakapallasutta — 1,681w / 37¶ / 12¶
- [x] AN 4.123–126: Nānākaraṇasuttāni — 2,607w / 22¶ / 10¶
- [x] AN 5.28: Pañcaṅgikasutta — 2,312w / 31¶ / 35¶
- [x] AN 9.36: Jhānasutta — 2,177w / 28¶ / 11¶
- [x] AN 10.2–6: Ānisaṃsasuttāni — 2,956w / 16¶ / 59¶

### Phase 3 — SN Expansion (this session, 2026-05-22)
- [x] SN 12 (Nidānasaṃyutta) — 18 suttas (20,504w) / 475¶ (22,013w) / 463¶ (21,458w); Mātikā: dependent_origination, four_noble_truths
- [x] SN 22 (Khandhasaṃyutta) — 18 suttas (23,613w) / 400¶ (13,968w) / 408¶ (8,841w); Mātikā: five_aggregates, three_marks
- [x] SN 35 (Saḷāyatanasaṃyutta) — 23 suttas (10,082w) / 590¶ (20,030w) / 484¶ (10,316w); Mātikā: five_spiritual_faculties, dependent_origination
- [x] SN 45 (Maggasaṃyutta) — 20 suttas (7,202w) / 124¶ (3,463w) / 126¶ (3,007w); §-anchors + callouts done; Mātikā: noble_eightfold_path
- [x] SN 46 (Bojjhaṅgasaṃyutta) — 56 suttas (23,919w) / 180¶ (6,062w) / 175¶ (5,545w); Mātikā: seven_awakening_factors
- [x] SN 47 (Satipaṭṭhānasaṃyutta) — 16 suttas (9,504w) / 220¶ (9,325w) / 149¶ (6,123w); §-anchors + callouts done; Mātikā: four_foundations_of_mindfulness
- [x] SN 48 (Indriyasaṃyutta) — 20 suttas (6,760w) / 106¶ (3,037w) / 92¶ (2,544w); §-anchors + callouts done; Mātikā: five_spiritual_faculties
- [x] SN 54 (Ānāpānasaṃyutta) — 20 suttas (11,648w) / 45¶ (2,018w) / 40¶ (1,393w); Mātikā: four_foundations_of_mindfulness
- [x] SN 55 (Sotāpattisaṃyutta) — 15 suttas (12,650w) / 103¶ (2,613w) / 90¶ (1,810w); §-anchors + callouts done; Mātikā: three_refuges, five_precepts, five_spiritual_faculties
- [x] SN 56 (Saccasaṃyutta) — 16 suttas (6,469w) / 153¶ (2,413w) / 100¶ (1,689w); Mātikā: four_noble_truths, noble_eightfold_path

### Phase 4 — Meditation Discourses Migration (completed, 2026-05-22)
- [x] MN 19: Dvedhāvitakkasutta — 3,032w / 6¶ / 6¶; §-anchors + callouts done
- [x] AN 10.60: Girimānandasutta — 1,931w / 1¶ / (No Ṭīkā available); §-anchors + callouts done

### Phase 5 — DN Expansion (completed, 2026-05-22)
- [x] DN 1: Brahmajālasutta — 18,401w / att / tik; §-anchors done
- [x] DN 16: Mahāparinibbānasutta — 35,942w / att / tik; §-anchors done
- [x] DN 21: Sakkapañhasutta — 8,213w / att / tik; §-anchors done

### Khuddaka Nikāya — Dhammapada, Udāna & Sutta Nipāta
- [x] Dhammapada Mūla — all 26 vaggas (423 verses, ~17,600w); Bhikkhu Sujato translation
- [x] Dhammapada Atthakathā — all 26 chapters, 294 origin stories (~498K words); Ānandajoti/Burlingame
- [x] Dhammapada Mātikā cross-links — 6 vaggas linked: dhp_02, 10, 14, 17, 20, 25
- [ ] Dhammapada Ṭīkā — **BLOCKED**: `s0502t.tik*.xml` all 404 on tipitaka.org; CSCD does not publish the Dhammapada-ṭīkā online
- [x] Udāna Mūla — 8 vaggas, 80 suttas (46,198w); Bhikkhu Sujato translation
- [x] Udāna Atthakathā — 8 vaggas, 1676 paragraphs (70,642w); CSCD Pali
- [x] Udāna Mātikā cross-links — linked to five_precepts, eight_precepts, three_marks, dependent_origination, five_spiritual_faculties
- [x] Sutta Nipāta Mūla — all 5 chapters, 73 suttas (~1140 verses); Bhikkhu Sujato translation
- [x] Sutta Nipāta Atthakathā — all 5 chapters, 73 suttas (2688 paragraphs); CSCD Paramatthajotikā II
- [x] Sutta Nipāta Mātikā cross-links — linked to five_precepts, three_refuges, four_sublime_states, five_hindrances, three_marks, four_foundations_of_mindfulness, five_spiritual_faculties, four_noble_truths, dependent_origination, five_aggregates
- [x] Itivuttaka Mūla — all 4 nipātas, 112 suttas; Bhikkhu Sujato translation
- [x] Itivuttaka Atthakathā — all 4 nipātas, 112 suttas (1166 paragraphs); CSCD Paramatthadīpanī
- [x] Itivuttaka Mātikā cross-links — linked to four_noble_truths, three_marks, noble_eightfold_path, three_unwholesome_roots, five_hindrances, ten_fetters, four_sublime_states, five_precepts, four_foundations_of_mindfulness, five_aggregates
- [x] Theragāthā Mūla — 21 nipātas, 203 poems; Bhikkhu Sujato translation
- [x] Theragāthā Mātikā cross-links — linked to noble_eightfold_path, four_sublime_states
- [x] Therīgāthā Mūla — 16 nipātas, 73 poems; Bhikkhu Sujato translation
- [x] Therīgāthā Mātikā cross-links — linked to four_foundations_of_mindfulness, four_sublime_states

### Vault Infrastructure
- [x] CSS translation toggle (`pali-translation-toggle.css`)
- [x] Simsapa DPD plugin (double-click Pali word lookup)
- [x] Dataview plugin
- [x] Templater plugin with translation toggle
- [x] Templates folder (mūla / atthakathā / tīkā sutta templates)
- [x] Git repository with `.gitignore`
- [x] Folder scaffolding for KN, Abhidhamma, Vinaya
- [x] Link validator (`scratch/validate_links.py`) — currently 201 files, 2,366 wikilinks, 0 errors

### Mātikā (19 lists — all complete)
- [x] four_noble_truths, noble_eightfold_path, three_marks, five_aggregates
- [x] dependent_origination, five_precepts, five_hindrances, seven_awakening_factors
- [x] four_foundations_of_mindfulness, eight_precepts, three_refuges, ten_perfections
- [x] four_sublime_states, five_spiritual_faculties, three_unwholesome_roots, four_right_exertions
- [x] ten_fetters, seven_purifications, five_powers (added 2026-05-22)
- [x] All 19 lists cross-linked to canonical vault sources (reverse links in every sutta)

### Phase 9 — Practice-Oriented Expansion (completed, 2026-05-23)
- [x] **Jhāna Deepening** — `four_jhanas` mātikā + 5 suttas (MN 128, AN 9.34, AN 9.35, MN 8, AN 8.63) + `paths/entering_jhana.md`
- [x] **Vipassanā Broadening** — 7 suttas (MN 148, SN 36.6, SN 36.11, SN 36.21, MN 28, MN 140, MN 2) + `paths/vipassana_practice.md`
- [x] **Brahmavihāra Practice** — 3 new suttas (MN 7, DN 13, AN 11.15) + 3 existing suttas + `paths/brahmavihara_cultivation.md`
- [x] **Anussati (Recollections)** — `six_recollections` mātikā + 3 suttas (AN 6.10, AN 11.12, AN 6.25) + `paths/anussati_practice.md`
- [x] **Anupubbasikkhā (Gradual Training)** — `gradual_training` mātikā + 4 suttas (MN 27, MN 51, AN 8.54, AN 4.99) + `paths/gradual_training.md`
- [x] **Maraṇasati (Death Contemplation)** — 3 new suttas (AN 6.19, AN 6.20, AN 8.73) + 1 existing sutta + `paths/maranasati.md`
- [x] **Paritta Collection** — 1 new sutta (AN 4.67) + 3 existing suttas + `paritta/INDEX.md` + `three_refuges` cross-links
- [x] **Vault Link Integrity** — 0 broken links across 951 files and 11,890 wikilinks.

### Phase 10 — AN Expansion (completed, 2026-05-23)
- [x] **AN 1 Ekakanipāta** — Generated all 31 ranges from SuttaCentral API, complete with Mūla, Atthakathā, and Ṭīkā layers
- [x] **AN 7, 8, 11 Expansion** — Migrated AN 7.65, AN 8.53, AN 11.1–5 across Mūla, Atthakathā, and Ṭīkā layers

### Phase 11 — Deeper MN Coverage (completed, 2026-05-23)
- [x] **MN Expansion** — Migrated MN 22 and MN 117 across Mūla, Atthakathā, and Ṭīkā layers

### Phase 13 — Practice Support Tooling (completed, 2026-05-23)
- [x] **Practice Notes Infrastructure** — Created `practice/INDEX.md` dashboard and `templates/practice_note.md` template
- [x] **Verse Memorization Log** — Created `practice/memorization_log.md` with core chanting verses
- [x] **Dataview Query Blocks** — Injected live sutta tables in all Nikāya INDEX files and added "Recently Modified" list to root INDEX.md

### Phase 15 — Tooling Refactoring, Guardrails, and Vinaya Initiation (completed, 2026-05-23)
- [x] **Unified Helper Library** — Consolidated common parser operations and paths into `scratch/lib/pali_utils.py`
- [x] **Git Verification Guardrails** — Implemented git pre-commit hook link validation and automated unittest suite
- [x] **Generic Cross-linker** — Aligned commentary paragraphs to root texts in MN 10 and MN 22
- [x] **Vinaya Piṭaka Initiation** — Migrated Bhikkhu Pātimokkha structure and rules to `patimokkha_bhikkhu.md`

### Phase 16 — Generator Unification, Caching, Chanting Audio, and Vinaya Expansion (completed, 2026-05-23)
- [x] **Offline Caching Layer** — Enabled local caching of CSCD XML files under `scratch/xml_cache/`
- [x] **Unified Sutta Generator** — Completed command-line generator `generate_sutta.py` which dynamically generates all layers for a given sutta ID
- [x] **Practice Audio & Flashcards** — Embedded audio files and Spaced Repetition cards in five precepts and Bhikkhu Pātimokkha
- [x] **Vinaya Expansion** — Migrated Bhikkhunī Pātimokkha rules (311 rules) to `patimokkha_bhikkhuni.md`

### Phase 17 — Tooling & Validation Optimization (completed, 2026-05-24)
- [x] **Incremental Link Validation** — Updated pre-commit hook and link validator to scan only staged files.
- [x] **Heuristic Commentary Auto-Aligner** — Added automatic paragraph anchor injection and Mūla auto-crosslinking to `generate_sutta.py`.

### Phase 18 — Interactive Dashboards & Practice Hubs (completed, 2026-05-24)
- [x] **Interactive Home Dashboard** — Rebuild root `INDEX.md` and `practice/INDEX.md` using curated styling (glassmorphism/gradients) and Dataview cards for reading paths.
- [x] **Chanting Review & Memorization System** — Connect Spaced Repetition cards to review workflows and integrate chanting audio tracking into the memorization log.

### Phase 20.1 — Noble Eightfold Path Factors Expansion (completed, 2026-05-24)
- [x] **Noble Eightfold Path Factors Expansion** — Create individual files for each of the 8 path factors under `matika/`, detailing their canonical definitions, practice descriptions, and sutta links.

### Phase 20.2 — Vault-wide Mātika Factors Expansion (completed, 2026-05-24)
- [x] **Vault-wide Mātika Factors Expansion** — Create detailed sub-files for every item in the remaining 18 mātika lists, featuring canonical definitions (Pali + English), descriptions, and cross-references.

---

## Pending Work

### Phase 15 — Vault Hygiene & Consistency
- [x] **Chanting Audio Player Fix** — Replace broken `file://` absolute paths in `meta/CHANTING.md` and monastic files with vault-relative wikilink embeds `! [ [ audio_file.mp3 ] ]` to render Obsidian's native audio player, and remove folder link stubs.
- [x] **Dotted Filename Refactor** — Write a python script to rename all 422 dotted filenames (`snp1.1.md` -> `snp1_1.md`) and rewrite all wikilinks vault-wide to maintain a clean, shell-tool-friendly naming convention.
- [x] **Frontmatter Schema Validation** — Add a frontmatter schema linter (`scratch/inspect/lint_frontmatter.py`) and wire it into the unit tests to enforce required keys by note type.
- [x] **AN Chunking Alignment** — Implement `covers:` (list) / `part_of:` fields to handle suttas mapped to grouped commentary/ṭīkā files.
- [x] **SYNC_LOG Rotation** — Rotate entries older than 30 days in `meta/SYNC_LOG.md` into `meta/sync_archive/SYNC_LOG_YYYY-MM.md` to limit file size overhead.
- [x] **CLAUDE.md Guardrails** — Create a project-level `CLAUDE.md` to define standard procedures, formatting, and validation scripts for new agents.
- [x] **Phase 19 Paragraph-Level Cross-Linking Backfill** — Re-generate the commentaries for MN 36, DN 22, and SN saṃyuttas (SN 12, 22, 35, 46, 54, 56) to ensure paragraph headers (`### §NNN`) are generated, and run the Heuristic Auto-Aligner to insert collapsible commentary callouts at the paragraph level.

### Phase 16 — Study Station Enhancements
- [x] **Prosopography Graph** — Seed manual people (`people/`) and place (`places/`) index notes. ✅
- [x] **Simile Index** — Build a cross-referenced catalogue of canon similes. ✅
- [x] **Pericope Concordance** — Map out repeated formulas (jhāna cadences, dependent origination chains) with links to occurrences. ✅
- [x] **Parallel-Texts Layer** — Inject SuttaCentral parallel IDs into frontmatter and render via Dataview.
- [x] **Question-Driven Paths** — Added three paths under `paths/`: `working_with_anger.md`, `understanding_craving.md`, `working_with_hindrances.md`. ✅
- [x] **Dynamic Count Tables** — Replace hardcoded count metrics in `INDEX.md` and `STATUS.md` with dynamic Dataview queries.

### Phase 17 — Pali NLP Companion Development (External Repo)
**Repo**: https://github.com/roydsouza/pali-nlp (local: `~/pali-nlp/`)
**Setup**: `cd ~/pali-nlp && source .venv/bin/activate`; DPD DB auto-detected from Simsapa.
- [x] **Stage 1: Lemmatization & Graded Reader (3A)**
    - [x] Stand up the separate `pali-nlp` repository with ingestion, DPD sqlite, and vault-writer modules. ✅
    - [x] Lemmatize tokens against DPD SQLite database (Simsapa install; 1.1M inflected forms via `lookup` table). ✅
    - [x] Append vocabulary concordance tables to vault mūla files — 508 suttas updated via `pali-write`. ✅
    - [x] Build the vocabulary frequency-based graded reader — `paths/graded_reader.md` written (518 suttas, 214k tokens, 21k headwords). ✅
    - [x] Auto-generate Obsidian-native spaced-repetition vocabulary cards. ✅
- [ ] **Stage 2: Linguistic Pipeline (3B)**
    - [ ] Build an offline concordance and collocation search index.
    - [ ] Train/configure NER pass to auto-populate Phase 16 prosopography pages.
- [ ] **Stage 3: Semantic Search & RAG (3C)**
    - [ ] Set up local-first vector search (embeddings + vector store).
    - [ ] Build answer generator behind a swappable interface (local default, optional Claude-API backend) with citation links to vault paragraph anchors.
- [ ] **Stage 4: Performance Porting (3D)**
    - [ ] Re-write performance-critical tokenizer and sandhi-splitting layers in Rust.

### Phase 18 — Text & Doctrinal Expansion (Abhidhamma & Vinaya Future)
- [x] **Sutta Piṭaka (Primary)** — All items complete. ✅
    - [x] Migrate remaining high-value suttas in Aṅguttara Nikāya (AN) for practice reading paths (e.g., AN 7.65, 8.53, 11.1–5).
    - [x] Migrate SN 51 (Iddhipādasaṃyutta) (lower priority).
    - [x] Migrate Theragāthā and Therīgāthā commentary (Paramatthadīpanī) for migrated verses.
    - [x] Compile continuous, Pali-only paritta recitation texts in the `paritta/` folder.
- [x] **Abhidhamma Piṭaka (Secondary)** — All items complete. ✅
    - [x] Scaffold and migrate the *Abhidhammatthasaṅgaha* mūla (Bhikkhu Bodhi's manual).
    - [x] Add Abhidhamma-style mātikā cross-links for the five aggregates.
- [x] **Vinaya Piṭaka (Tertiary)** — All items complete. ✅
    - [x] Integrate the *Kaṅkhāvitaraṇī* (commentary on the Pātimokkha rules).
    - [x] Create Vinaya indexes for the *Suttavibhaṅga*, *Khandhaka*, and *Parivāra*.
    - [x] Link Vinaya Pātimokkha notes to the `five_precepts` / `eight_precepts` mātikā.

### Phase 19 — Tutorials and Pakaraṇa Layer (completed 2026-05-30)
- [x] **Tutorial series** — Six integrated practice tutorials in `tutorial/`: breath practice (MN 118), satipaṭṭhāna (MN 10/DN 22), three layers, mātikā web, Pali reading tools, building a sustained practice. Contextual callouts on MN 118 and MN 10. ✅
- [x] **Pakaraṇa layer** — `pakarana/` directory with Visuddhimagga Chapters VIII (ānāpānasati) and XI (jhānas). Full cross-linking to vault suttas and mātikā. ✅
- [x] **README overhaul** — Updated to reflect current vault state (5 layers, tutorials, pali-nlp, accurate counts), links throughout, Obsidian entry-point nudge. ✅
- [x] **INDEX.md UX fixes** — All four card badges made clickable; Dataview inline expressions replaced with hardcoded counts; regression tests added to pre-commit suite. ✅

### Phase 20 — Remaining Visuddhimagga
- [x] **Vsm Samādhi section (Phase 20A)** — Ch. III (40 subjects, temperament matching), Ch. IV–VII (kasiṇas, foulness, recollections), Ch. IX (brahmavihārā as jhāna basis), Ch. X (formless attainments) ✅ (2026-06-03)
- [ ] **Vsm Paññā section (Phase 20B)** — Ch. XIV–XXII (insight knowledges through liberation; only after samatha practice is well-established)

---

### Phase 21 — Canonical Breadth Expansion (Future)

**Trigger**: Begin only when all of the following are true:
- Phase 16 (Study Station) is complete and actively used during reading sessions
- Phase 17 (pali-nlp companion: graded reader + concordance) is operational
- The seven practice domains feel covered — you reach for the vault and find what you need
- The mātikā web feels saturated (no obvious cross-links missing)

**Goal**: Shift from practice-curated selection to systematic breadth. Fill the remaining canon methodically, with full three-layer structure, prioritized by doctrinal importance rather than immediate practice urgency.

- [ ] **Remaining Majjhima Nikāya** — Target ~40–50 additional suttas to reach meaningful MN coverage. Priority candidates: MN 63 (Cūḷamāluṅkya — unanswered questions), MN 72 (Aggivacchagotta — fire simile for nibbāna), MN 26 (Ariyapariyesanā — the noble search, the first teaching), MN 36 (already in vault), MN 38 (Mahātaṇhāsankhaya — craving and consciousness).
- [ ] **Remaining Dīgha Nikāya** — The 26 DN suttas not yet migrated. Lower priority; many are cosmological or historical rather than practice-focused.
- [ ] **Saṃyutta Nikāya gaps** — The 45 saṃyuttas not yet covered. Priority: SN 1 (Devatāsaṃyutta — short verse dialogues), SN 3 (Kosalasaṃyutta — the king suttas), SN 4 (Mārasaṃyutta), SN 6 (Brahmasaṃyutta).
- [ ] **Aṅguttara Nikāya systematic fill** — AN nipātas 2–11 have large gaps. The AN has ~9,557 suttas total; many are formulaic repetitions. Strategy: migrate complete nipātas for AN 2–6 (shorter, more varied), batch-process AN 7–11 where formulas repeat.
- [ ] **Remaining Khuddaka Nikāya** — Jātaka (birth stories, selected), Vimānavatthu, Petavatthu, Niddesa (commentary on Aṭṭhakavagga/Pārāyanavagga — directly relevant to Snp 4–5), Paṭisambhidāmagga (analytical treatise on insight), Buddhavaṃsa, Cariyāpiṭaka.
- [ ] **Review and re-evaluate scope** before beginning — the canon is vast; wholesale migration is a multi-year effort. Confirm the vault is still serving its practice purpose before going broad.
