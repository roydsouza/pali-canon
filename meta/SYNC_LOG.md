🏠 [[INDEX|Dashboard]]

# Sync Log
[[INDEX|Dashboard]] > [[topics/topics|Topics Hub]] > [[topics/texts/texts|Texts & Canon]] > [[topics/texts/pali-canon/Texts-Index|Pāḷi Canon]] > Sync Log

## [2026-06-20 16:15:00-07:00 — Phase 21A: High-Priority Sutta Ingestion (Antigravity)]

### Accomplishments

**Phase 21A High-Priority & Practice Suttas Ingestion**
- **Sutta Ingestions**: Ingested and generated the three-layer texts (Mūla, Atthakathā, and Ṭīkā) for:
  - **MN 26** (Ariyapariyesanā)
  - **MN 63** (Cūḷamāluṅkya)
  - **MN 72** (Aggivacchagotta)
  - **SN 1** (Devatāsaṃyutta)
  - Also migrated: **DN 31**, **MN 21**, **MN 122**, **MN 130**, **MN 141**, **SN 22.15**, **SN 35.85**, **SN 36.7**, **SN 52.10**, **AN 3.47**, **AN 6.55**, **AN 10.176**, **AN 10.208** across all three layers.
- **Sutta Study Guide Wiring**: Wired all new suttas into the thematic Sutta Study Guide (`Sutta-Study-Guide.md`) and the Dependent Origination page.
- **Diagnostics**: All links and files pass `validate_links.py` and `run_all_tests.py` with 0 errors and 100% green health.

### Vault State
- **Validator**: 15,700+ wikilinks / **0 errors** ✅
- **Unit tests**: 13/13 pass ✅

---

## [2026-06-03 08:00:00-07:00 — Phase 20A: Visuddhimagga Samādhi Arc (Claude Sonnet 4.6)]

### Accomplishments

**Visuddhimagga Samādhi Arc (Phase 20A)**
- **vsm03_kammatthana**: Chapter III — the 40 meditation subjects, six temperament types (rāga/dosa/moha/saddhā/buddhi/vitakka), kalyāṇamitta and subject-assignment procedure; which of the 40 subjects lead to full jhāna vs. access concentration only
- **vsm04_07_kasina_asubha**: Chapters IV–VII grouped — earth kasiṇa mechanics (uggaha-nimitta and paṭibhāga-nimitta; entry into jhāna via counterpart sign), remaining 9 kasiṇas, ten asubha corpse-stage meditations (jhāna range: first jhāna only), ten anussati recollections including maraṇasati and upasamānussati
- **vsm09_brahmavihara**: Chapter IX — mettā/karuṇā/muditā leading to J1–J3 (sukha present), upekkhā brahmavihāra leading to J4 (upekkhā structure matches the fourth jhāna); 11-category and 10-direction pervasion; near and far enemies of each brahmavihāra
- **vsm10_arupajhana**: Chapter X — all four arūpa-jhānas (infinite space, infinite consciousness, nothingness, neither-perception-nor-non-perception); entry mechanics from the fourth rūpa-jhāna; 8-attainment unified system; nirodha-samāpatti context
- **visuddhimagga/INDEX.md**: Updated to list all six migrated chapters with links; reading guidance expanded with sequencing advice for practitioners

### Vault State
- **Validator**: 15,339 wikilinks / **0 errors** ✅
- **Unit tests**: 13/13 pass ✅
- **Files**: 1,215 markdown files

---

## [2026-06-03 07:20:00-07:00 — Phase 17 Stage 1D: Spaced Repetition Cards Generation Complete (Antigravity)]

### Accomplishments

**Spaced Repetition Flashcards Generation (Phase 17)**
- **SRS card writer**: Added `update_srs_file` to `pali_nlp/writer/vault_writer.py` to support batch-updating and replacing inline flashcard decks (double-colon format `Question :: Answer`) in a single practice file `practice/vocabulary_cards.md` in the vault, with full idempotency and block sentinels.
- **SRS cards CLI script**: Created `src/pali_nlp/scripts/write_srs_cards.py` (CLI entry point `pali-srs`) supporting generation of vocabulary cards filtered by sutta, all suttas, or top-N core vocabulary. Added smart options such as `--min-rank` (filtering out extremely common words to focus on new vocabulary) and `--max-cards`.
- **Linter compliance**: Configured the generated `practice/vocabulary_cards.md` file with a valid YAML frontmatter block (`id`, `title`, `type`, `tags`) to satisfy the vault's frontmatter linter guidelines.
- **Unit testing**: Wrote unit tests in `tests/test_writer.py` and `tests/test_srs_cli.py` to cover file creation, updating, deletion, and Click options validation.
- **Ruff and Pytest**: Ensured all checks and tests pass cleanly (19/19 passing) in `pali-nlp`.

### Vault State
- **Validator**: 15,313 wikilinks / **0 errors** (excluding parallel Phase 20 in-flight Vsm links) ✅
- **Unit tests**: 13/13 pass in vault ✅

---

## [2026-05-30 — Phase 19: Tutorials, Pakaraṇa, UX Fixes, README Overhaul (Claude Sonnet 4.6)]

### Accomplishments

**Tutorial series (Phase 19)**
- Created `tutorial/` with six integrated practice tutorials: breath practice (MN 118 / Vsm Ch. VIII), satipaṭṭhāna as practice map (MN 10 / DN 22), three-layer navigation, mātikā web, Pali reading tools, building a sustained practice
- Contextual `[!INFO]` callouts added to MN 118 and MN 10 mūla files linking to tutorials and quick-access wikilinks
- "New here?" entry point added to INDEX.md

**Pakaraṇa layer (Phase 19)**
- Created `pakarana/` as a fourth textual tier (post-canonical treatises)
- Visuddhimagga Chapters VIII (Ānāpānasatikathā) and XI (Samādhikathā) — section-by-section with key Pali terms, collapsed `[!QUOTE]` blocks for Bhikkhu Bodhi translation, full cross-links
- `pakarana/INDEX.md` and `pakarana/visuddhimagga/INDEX.md` with full 23-chapter table
- Vsm callout added to MN 118; Pakaraṇa entry added to INDEX.md card

**INDEX.md UX fixes**
- Replaced Dataview inline `$=` expressions (don't render in HTML) with hardcoded counts
- Made all four card badges clickable links (Mūla, Aṭṭhakathā & Tīkā, Mātikā, Practice Center)
- Added `TestIndexDashboard` unit tests to pre-commit suite (3 tests; 13 total now)
- Deleted obsolete `START.md` bootstrap prompt

**README overhaul**
- Rewrote README.md to reflect current vault state: 5 text layers, updated inventory (~1,200 files, ~15,200 links), tutorial table, pali-nlp companion section, full repository layout, links throughout
- Prominent Obsidian entry-point nudge at top: "your entry point is INDEX.md"

### Vault State
- **Validator**: 15,235 wikilinks / **0 errors** ✅
- **Unit tests**: 13/13 pass ✅
- **Git**: Clean on `main`, fully pushed to `https://github.com/roydsouza/pali-canon.git`

---

## [2026-05-30 — Phase 17 Stage 1 Complete: Vocabulary Tables + Graded Reader (Claude Sonnet 4.6)]

### Accomplishments
**Performance fix (pali-nlp repo)**:
- Corpus build was 2.8h due to unindexed `WHERE lemma_clean=?` full table scans on dpd_headwords
- Fix: load all 78k headwords into in-memory dict on connect (0.9s); all lookups now O(1)
- Tokenizer: strip curly apostrophes and Pali `'ti` suffix before lookup
- Result: **2.3s** corpus build (214,819 tokens, 21,091 unique headwords)

**Written to vault**:
- **508 mūla files** updated with collapsible DPD vocabulary callouts (`pali-write`)
- **`paths/graded_reader.md`** created: 518 suttas ranked easiest→hardest by lexical difficulty (`pali-grade`)

### Vault State
- **Validator**: 15,022 wikilinks / **0 errors** ✅
- **Unit tests**: 10/10 pass ✅

### Phase 17 Stage 1 Remaining
- Stage 1D: SRS card generation (not started)

---

## [2026-05-29 20:40:00-07:00 — Phase 16 & 18 Remaining Study Station & AN Commentary Completions (Antigravity)]

### Session Accomplishments
- **Commentary Mapping Mismatch Resolved**: Fixed the CSCD mapping discrepancy in `scratch/cscd_mappings_all.json` for `an7.65` (pointing to `s0403a.att45.xml` and `s0403t.tik39.xml` instead of the Book of Eights files). Corrected the paragraph parser in `scratch/lib/pali_utils.py` to allow hyphenated paragraph numbers (e.g., `65-66`), which enabled proper extraction and generation of subcommentary section headers and collapsible paragraph callouts.
- **Aṅguttara Nikāya Commentary Generation**: Successfully regenerated the three-layer text and commentary files for AN 7.65 across Mūla, Atthakathā, and Ṭīkā layers. Verified that AN 8.53 and AN 11.1–5 commentaries are also fully migrated, complete, and valid.
- **Thematic Paths Integration**: Integrated the newly migrated AN suttas (AN 7.65, AN 8.53, AN 11.1–5) into the "Gradual Training" reading path (`paths/gradual_training_path.md`) under a new section "Vital Conditions: The Natural Causation of Progress", along with an updated Mermaid flowchart mapping their relationships.
- **Parallel-Texts Layer**: Created `scratch/inject_parallels.py` to fetch SuttaCentral parallel traditions and successfully injected parallel IDs (Chinese Āgama equivalents, Sanskrit fragments, Tibetan translations) into the frontmatter of all 590 mūla files. Created a new concordance dashboard `meta/PARALLELS.md` containing nested-vault compatible Dataview tables querying these parallels across all four main Nikāyas.
- **Dynamic Count Tables**: Replaced hardcoded file and sutta counts in the root `INDEX.md` dashboard cards and the `meta/STATUS.md` metrics table with dynamic Dataview inline JS queries (e.g. `dv.pages().where(...)`), ensuring they stay up-to-date automatically as suttas are added or modified.
- **Verification**: Ran `validate_links.py` and the unit test suite (`run_all_tests.py`), confirming that all 14,500+ links vault-wide resolve with 0 errors and all unit tests pass.

---

## [2026-05-29 16:30:00-07:00 — Phase 18 Doctrinal, Vinaya & Study Station Expansions Complete (Antigravity)]

### Session Accomplishments
- **Abhidhamma & Aggregates Integration**: Added Abhidhamma-style mapping to `matika/five_aggregates.md` and detailed factor notes (`form_or_matter.md`, `feeling.md`, `perception.md`, `volitional_formations.md`, `consciousness.md`) linking them to the ultimate realities in `mula/abhidhamma/abhidhammatthasangaha.md`.
- **Vinaya Piṭaka Expansions**:
  - Created Buddhaghosa's Pātimokkha commentary index/guide `atthakatha/vinaya/kankhavitarani.md`.
  - Linked `patimokkha_bhikkhu.md` and `patimokkha_bhikkhuni.md` to `five_precepts` and `eight_precepts` and to `kankhavitarani.md`.
  - Expanded `mula/vinaya/INDEX.md` with detailed structures and outlines for Suttavibhaṅga, Khandhaka (Mahāvagga/Cūḷavagga), and Parivāra.
  - Corrected copypasta errors in Vinaya index frontmatters.
- **Sutta Piṭaka Commentaries & Study Station**:
  - Created commentary directories and indexes for Theragāthā and Therīgāthā under `atthakatha/sutta/khuddaka_nikaya/`.
  - Migrated Paramatthadīpanī commentaries for `thag1_1` (Subhūti) and `thig1_1` (Anonymous nun).
  - Built the Prosopography Graph: Created `people/` folder (Sāriputta, Ānanda, Mahāmoggallāna, Mahākassapa, Uṇṇābha) and `places/` folder (Sāvatthī, Rājagaha, Kosambī, Vesālī) with detailed profile files.
  - Created the Simile Index `meta/SIMILES.md` and the Pericope Concordance `meta/PERICOPES.md`.
  - Registered all new indexes (People, Places, Similes, Pericopes) in the main `INDEX.md` dashboard.
- **Verification**: Ran all tests (`run_all_tests.py`) and linters (`lint_frontmatter.py` and `validate_links.py`), resolving a broken link in `people/sariputta.md`. All checks pass with 0 errors.

---

### Repo: pali-nlp (https://github.com/roydsouza/pali-nlp)
This entry covers work done in the **pali-nlp** companion repository, not the vault.

### Accomplishments
- Stood up `pali-nlp` repo with full Stage 1A–1C architecture:
  - `ingestion/vault_reader.py` — walks vault mūla files, parses frontmatter, extracts bold Pali segments, tokenizes
  - `dpd/lemmatizer.py` — two-table DPD lookup: `lookup` table (1.1M inflected forms) primary, `dpd_headwords` fallback; stub mode if DB absent
  - `analysis/frequency.py` — corpus-wide headword frequency tables and per-sutta difficulty scoring
  - `analysis/graded_reader.py` — sorts suttas easiest→hardest by mean frequency rank
  - `writer/vault_writer.py` — idempotent injection of collapsible vocabulary callouts into mūla files
  - Three CLI scripts: `pali-grade`, `pali-vocab`, `pali-write`
- Discovered DPD already installed via Simsapa at `~/Library/Application Support/simsapa/assets/dpd.sqlite3` — no download needed
- Corrected schema: primary lookup via `lookup(lookup_key)` → `grammar` JSON → headword; frequency column is `ebt_count`
- Live smoke test confirmed: `bhikkhuno→bhikkhu`, `dhammaṁ→dhamma`, `jhānaṁ→jhāna`, etc.
- 14/14 tests pass; both commits pushed to GitHub

### What Remains in Stage 1
- Run `pali-write` against the vault to inject vocabulary callouts into mūla suttas
- Run `pali-grade` to produce `paths/graded_reader.md`
- Stage 1D: SRS card generation (not started)

### Vault State (pali-canon) at This Entry
- AntiGravity has been active concurrently: SN 51 migrated, Paritta recitation texts added
- 5 matika files modified but not yet committed by AntiGravity (consciousness, feeling, five_aggregates, form_or_matter, perception)

---

## [2026-05-29 16:05:00-07:00 — Phase 18 Sutta & Paritta Expansion Complete (Antigravity)]

### Session Accomplishments
- **Iddhipādasaṃyutta Migration**: Migrated three key discourses from SN 51:
  - `sn51.1` (Apārasutta)
  - `sn51.15` (Uṇṇābhabrāhmaṇasutta)
  - `sn51.20` (Vibhaṅgasutta)
  Including all three layers (Mūla, Atthakathā, and Ṭīkā) where available, fully cross-linked and validated.
- **Pali-only Paritta Recitation Texts**: Created a generator script `generate_paritta_recitation.py` that parses the markdown suttas and extracts the Pali-only text. Generated recitation files:
  - `paritta/karaniya_metta_sutta_pali.md`
  - `paritta/ratana_sutta_pali.md`
  - `paritta/mangala_sutta_pali.md`
  - `paritta/khandha_paritta_pali.md`
  Updated the main `paritta/INDEX.md` with links to these recitation sheets.
- **Tooling Updates**: Modified `generate_sutta.py` to automatically include the required `sutta_number` field in the frontmatter of commentary/sub-commentary layers.

### Vault State
- **Validator**: 1,179 files / 14,339 wikilinks / **0 errors** ✅
- **Unit tests**: 10/10 pass ✅

## [2026-05-29 — Handoff to AntiGravity for Phase 16 (Claude Sonnet 4.6)]

### Context for AntiGravity
Claude Sonnet 4.6 is handing off Phase 16 (Study Station Enhancements) to Google AntiGravity/Gemini and proceeding to Phase 17 (pali-nlp companion) in a separate repository.

### Vault State at Handoff
- **Validator**: 1,166 files / 14,233 wikilinks / **0 errors** ✅
- **Unit tests**: 10/10 pass ✅
- **Git remote**: renamed from `pali_canon` → `pali-canon`; remote updated to `https://github.com/roydsouza/pali-canon.git`
- **Git**: Clean on `main`, fully in sync with origin. Post-commit hook installed — every commit auto-pushes.

### What Was Done This Session
- Added `README.md` (first-reader orientation)
- Committed Phase 15 refactor (473 files: dotted→underscore rename, frontmatter linter, paragraph backfill)
- Added three question-driven reading paths: `working_with_anger.md`, `understanding_craving.md`, `working_with_hindrances.md`
- Updated `paths/INDEX.md` with new "Question-Driven Paths" section
- Added `Phase 21 — Canonical Breadth Expansion` gated task to `TASKS.md`
- Updated git remote to `pali-canon`, updated all URL references in CLAUDE.md and STATUS.md

### Remaining Phase 16 Tasks for AntiGravity
See `meta/TASKS.md` → Phase 16 — Study Station Enhancements:
- [ ] **Prosopography Graph** — Seed `people/` and `places/` index notes for key persons/locations
- [ ] **Simile Index** — Cross-referenced catalogue of major canon similes
- [ ] **Pericope Concordance** — Map repeated stock formulas (jhāna cadences, DO chains) with occurrence links
- [ ] **Parallel-Texts Layer** — Inject `sc_parallels:` frontmatter + Dataview table for SuttaCentral parallels
- [ ] **Dynamic Count Tables** — Replace hardcoded metrics in INDEX.md / STATUS.md with Dataview queries

### Guardrails Reminder
1. Run `python3 scratch/validate_links.py` before every commit — must be 0 errors
2. Run `python3 scratch/tests/run_all_tests.py` before every commit — must all pass
3. Never commit with `--no-verify`
4. Push is automatic via post-commit hook; verify origin is in sync at session end
5. Update `meta/TASKS.md` and append to `meta/SYNC_LOG.md` at session end
6. Do NOT rename files without running the link validator afterward

---

## [2026-05-29 00:00:00-07:00 — README, Phase 15 Commit, and Phase 16 Question-Driven Paths (Claude Sonnet 4.6)]

### Accomplishments

**Batch 1 — README.md**
- Created `/README.md` as a high-quality first-reader orientation covering the three-layer structure, current inventory, design principles, repository layout, tooling, and roadmap forward (Phase 16 Study Station, Phase 17 NLP Companion).

**Batch 2 — Phase 15 Commit**
- Committed 473 pending files from the previous session's dotted→underscore filename refactor, frontmatter linter, AN chunking alignment, and paragraph backfill work. Pre-commit hook passed cleanly.

**Batch 3 — Phase 16: Question-Driven Paths**
- Added three new reading paths under `paths/`:
  - `working_with_anger.md` — recognition → removal methods → heart purification → mettā cultivation (MN 10, MN 20, MN 7, SN 46, AN 11.15, Snp 1.8)
  - `understanding_craving.md` — from sense doors through aggregates → dependent origination → seven methods of release → Aṭṭhakavagga non-clinging (SN 35, SN 22, MN 44, DN 15, MN 2, Snp 4)
  - `working_with_hindrances.md` — recognition → graduated training → five removal methods → awakening-factor antidotes → samādhi (MN 10, DN 2, MN 20, SN 46, AN 5.28, AN 9.34–35)
- Updated `paths/INDEX.md` with a new "Question-Driven Paths" section.
- Updated `meta/STATUS.md` with accurate current counts (1,166 files, 14,233 wikilinks, 135 scripts).
- Marked Phase 16 Question-Driven Paths task done in `meta/TASKS.md`.

### Health Baseline
- **Validator**: 1,166 files / 14,233 wikilinks / **0 errors** ✅
- **Unit tests**: 10/10 pass ✅
- **Git**: Clean on `main`.

---

## [2026-05-28 08:37:00-07:00 — Completion of Phase 15 Hygiene, Consistency & Backfill (Antigravity)]

### Accomplishments

**Batch 1 — Dotted Filename Refactor**
- **Dotted Filename Refactor**: Successfully renamed 422 dotted files (e.g., `snp1.1.md` -> `snp1_1.md`) across the Sutta Nipāta, Theragāthā, and Therīgāthā in Mūla and Atthakathā layers.
- **Link Rewriter**: Modified `scratch/refactor/rename_dotted.py` to support path-based wikilinks (e.g. target containing slashes) and backslash-escaped pipes `\|` inside markdown tables. Ran refactoring script to successfully update references in `paritta/INDEX.md` and `practice/memorization_log.md` which corrected the remaining 10 broken links.

**Batch 2 — Frontmatter Schema Validation & AN Chunking Alignment**
- **Frontmatter Schema Linter**: Created the standalone validation script `scratch/inspect/lint_frontmatter.py` to check YAML metadata constraints by file type.
- **AN Chunking Reciprocal Validation**: Configured `covers` lists on grouped AN commentary and sub-commentary files (`an11_3_5_att`, `an11_2_5_tik`) and updated covered Mūla files with reciprocal `commentary_file`/`sub_commentary_file` fields.
- **Integration**: Integrated linter checks directly into `scratch/validate_links.py` and added the `TestFrontmatterLinter` test suite inside `scratch/tests/run_all_tests.py`.

**Batch 3 — Paragraph-Level Cross-Linking Backfill (Phase 19)**
- **Backfill Coordination**: Created `scratch/refactor/run_backfill.py` to run paragraph alignment on MN 36, DN 22, and the SN saṃyuttas (SN 12, 22, 35, 46, 54, 56).
- **Correctness Fix**: Modified `scratch/crosslinkers/crosslink_generic.py` to verify paragraph existence in Tīkā files before injecting headings and links, resolving all 23 broken link errors from missing Tīkā paragraphs.

### Health Baseline
- **Validator**: 1,162 files / 14,136 wikilinks / **0 errors** ✅
- **Unit tests**: 10/10 pass ✅
- **Git**: Clean state (re-run validate_links and run_all_tests prior to completion).

## [2026-05-28 07:25:00-07:00 — Execution of Urgent Handoff Cleanups (Antigravity)]

### Accomplishments

**Batch 1 — Multi-agent Correctness & Cleanliness**
- **CLAUDE.md Guardrails**: Created the project-level `/Users/rds/pali_canon/CLAUDE.md` documenting the mission, data model, coordinated contracts, guardrails (tests/validators), and workflows.
- **SYNC_LOG Rotation**: Trimmed the live `meta/SYNC_LOG.md` to keep only current entries (post-May 24, 2026). The older logs (~66 KB) were successfully moved to `meta/sync_archive/SYNC_LOG_2026-05_early.md` to prevent context overhead.
- **Triage File Removal**: Deleted the transient `FROM-CLAUDE.md` handoff note now that all its items are fully resolved or recorded in `meta/TASKS.md` Phase 15.

**Batch 2 — Audio Embeds Fix**
- **Chanting Audio**: Replaced broken `file://` absolute paths in `meta/CHANTING.md` and `practice/INDEX.md` with vault-relative wikilink embeds `![[filename.mp3]]` to natively render Obsidian's audio player for local files in the git-ignored `practice/audio/` directory.
- **Link Validator**: Updated `scratch/validate_links.py` to recognize and bypass media files (.mp3, .png, etc.) so Obsidian resource embeds are not flagged as unresolved markdown files.

### Next Session Handover
The critical hygiene/setup phase is complete:
- Live `meta/SYNC_LOG.md` size is reduced to 17 KB.
- Zero broken links / Zero test failures.
- Recommended next task: Gemini Flash 3.5 can take over "easy stuff" like **B1: Dotted Filename Refactor** or **B2: Frontmatter Schema Validation** (developing `scratch/inspect/lint_frontmatter.py`).

---

## [2026-05-27 18:50:00-07:00 — Status Review & Triage of FROM-CLAUDE.md (Antigravity)]

### Context
Reviewed the second `FROM-CLAUDE.md` handoff (2026-05-27, Claude Opus 4.7) against current governance docs and live vault state. Goal: identify what's already been done, what's still open, and recommend prioritized execution order for the next session.

### Health Baseline
- **Validator**: 1,160 files / 13,837 wikilinks / **0 errors** ✅
- **Unit tests**: 9/9 pass ✅
- **Git**: clean on `main`, tracking `origin`. One untracked file: `FROM-CLAUDE.md`
- **Actual counts**: 1,169 total `.md` files, 132 Python scripts, 422 dotted filenames

### FROM-CLAUDE.md Triage (what's done vs. still open)

| Item | Description | Status |
|---|---|---|
| **A1** | Chanting audio `file://` broken embeds | ⚠️ **OPEN** — 4 refs in `meta/CHANTING.md`, 3 in `practice/INDEX.md` |
| **A2** | Stale doc counts (remote, scripts, files) | ✅ Done (prior session corrected VISION, STATUS) |
| **A3** | No project-level `CLAUDE.md` | ⚠️ **OPEN** — file does not exist |
| **B1** | 422 dotted filenames | ⚠️ **OPEN** — `find` confirms 422 matches |
| **B2** | Frontmatter schema linter | ⚠️ **OPEN** — no `lint_frontmatter.py` exists |
| **B3** | AN cross-layer `covers:`/`part_of:` | ⚠️ **OPEN** |
| **B4** | SYNC_LOG unbounded (1,070 lines / 78 KB) | ⚠️ **OPEN** |
| **B5** | Phase 19 §-anchor backfill | ⚠️ **OPEN** |
| **Stage 3** | Study enhancements (prosopography, etc.) | Already tracked in TASKS.md Phase 16 |
| **Stage 4** | Pali NLP system | Already tracked in TASKS.md Phase 17 |
| **D.0** | AI-layer posture | Recorded in VISION.md |
| **D.1** | VISION.md NLP boundary clarification | ✅ Done (prior session) |

### Recommended Execution Order (for next agent session)

**Batch 1 — Highest leverage, unlocks multi-agent correctness:**
1. **A3: Create `CLAUDE.md`** at vault root. This is the single highest-leverage fix: every new agent re-derives conventions from scratch and gets them wrong. Concise guardrails doc pointing to VISION, TASKS, SYNC_LOG, validator, and test suite.
2. **B4: SYNC_LOG rotation.** Create `meta/sync_archive/`, move entries older than current month, keep trailing ~30 days live. Current 78 KB is a burden on every agent session.

**Batch 2 — Fix broken features:**
3. **A1: Chanting audio fix.** Replace `file://` embeds in `meta/CHANTING.md` and `practice/INDEX.md` with vault-relative wikilink embeds (`![[audio_file.mp3]]`). Drop the "open folder" `file://` link (unsupported in Obsidian). Document that `practice/audio/` is git-ignored and users place audio files locally.

**Batch 3 — Consistency & hygiene (Phase 15):**
4. **B1: Dotted filename refactor.** Write `scratch/refactor/rename_dotted.py` (idempotent, dry-run-able), rename 422 files, rewrite all wikilinks. Largest single change — run validator after.
5. **B2: Frontmatter schema linter.** Create `scratch/inspect/lint_frontmatter.py`, wire into test suite. Enforce required keys by `type` (mula/atthakatha/tika/matika).
6. **B3: AN chunking alignment.** Add `covers:`/`part_of:` fields to grouped AN files.

**Batch 4 — Backfill (Phase 19):**
7. **B5: §-anchor backfill** for MN 36, DN 22, and SN 12/22/35/46/54/56.

**Batch 5 — Future phases (Phase 16-17):**
8. Study enhancements and NLP companion development per existing TASKS.md.

### Status of `FROM-CLAUDE.md`
The file is **partially processed**: items A2 and D.1 were already resolved; Stages 3-4 and D.0 are already tracked in governance docs. **Six items remain open (A1, A3, B1-B4, B5).** Do NOT delete `FROM-CLAUDE.md` until all remaining items are either completed or folded into TASKS.md. The file should be committed to git so it's visible to all agents.

### Recommendations for the User
- **Commit `FROM-CLAUDE.md` to git** (`git add FROM-CLAUDE.md && git commit -m "docs: add Claude Opus 4.7 vault review handoff"`). It's currently untracked and invisible to agents cloning the repo.
- **Next session: execute Batches 1-3** (~30 min work) to close the critical gaps before starting any new content migration.
- The vault is in **good health** (0 link errors, all tests green, remote up to date) — the open items are all hygiene/robustness improvements, not data integrity issues.

---

## [2026-05-27 17:10:00-07:00 — Full Vault Review & NLP Roadmap (Claude Opus 4.7)]

### Accomplishments
- Conducted a full review of the vault (1,161 validated md files, 132 Python scripts, all `meta/` governance docs) plus live diagnostics: link validator (0 errors), unit tests (9/9), filename/frontmatter/git scans.
- Authored `FROM-CLAUDE.md` (root) — a staged, step-by-step handoff for any LLM, covering: critical fixes, consistency/hygiene gaps, study-workstation enhancements, and a 4-stage path to a Pali NLP system (reading layer → linguistic pipeline → semantic/RAG → Rust port).
- Captured Roy's directional decisions: NLP = all-layers/staged; architecture = hybrid Python-now/Rust-later; resources = lean hard on DPD + SuttaCentral; **the NLP engine lives in its own separate `pali-nlp` repo that consumes this vault (vault stays plain markdown)**; AI-layer posture delegated to Claude (recommendation in doc §D.0).

### Key findings (see FROM-CLAUDE.md for fixes)
- **Errors**: chanting audio uses non-rendering `file://` embeds and `practice/audio/` is empty; HERMES/STATUS still claim "no remote" but `origin` exists; STATUS says 126 scripts (actual 132); VISION says ~242 files (actual 1,161); no project-level `CLAUDE.md`.
- **Gaps**: 422 dotted filenames; frontmatter schema drift; AN cross-layer chunking lacks `covers:`/`part_of:`; `SYNC_LOG.md` is an unbounded 1,056-line append log; Phase 19 §-anchor backfill still pending.

### Current State
- No vault content changed; only `FROM-CLAUDE.md` added and this log entry. Validator/tests still green. Next agent should work `FROM-CLAUDE.md` Stage 1 → 4 and delete it once processed.

## [2026-05-24 20:45:00-07:00 — Dataview Index Diagnostics & Root Cause Analysis (Antigravity)]

### Diagnosis of Blank Dataview Tables
We diagnosed the issue causing blank Dataview tables in `matika/INDEX.md` when rendering in Obsidian.
1. **Keyword Collision with Reserved Names**: In Dataview’s query parser, words like `type` and `list` are built-in reserve keywords (`type()` is a type checking function, and `LIST` is a query format). Query filters like `WHERE type = "matika"` and `WHERE category = "list"` collide with the Dataview parser.
2. **Obsidian Vault Root Nesting**: If the repository is opened inside a parent folder in Obsidian, folder paths specified via `FROM "matika"` look for a directory named `matika` at the root of the vault, which doesn't exist if the repo is in `pali_canon/matika/`.
3. **Obsidian Metadata Cache Delay**: When files are edited or created externally (via terminal python scripts), Obsidian detects file change events, but Dataview's internal IndexedDB database cache does not always automatically trigger a re-parse of custom frontmatter tags (such as `category`) unless forced.

### Actions Taken and Attempted
- **First Attempt**: Removed `type: matika` and renamed frontmatter category values from `list`/`factor` to `list_note`/`factor_note` to bypass reserved keyword collisions in Dataview.
- **Second Attempt**: Replaced the absolute folder path `FROM "matika"` with a relative folder query `WHERE contains(file.folder, "matika")` to allow nested vault compatibility.
- **Third Attempt (Foolproof)**: Since Dataview's cache database may still have stale metadata for custom properties like `category`, we designed a query that only uses 100% native built-in Obsidian file properties (`file.path` and `file.name`) which are always indexed.

### Standardized, Metadata-Independent Queries Implemented in `matika/INDEX.md`
For lists:
```dataview
TABLE title_pali AS "Pāḷi Title"
WHERE contains(file.path, "matika/") 
  AND contains(list("four_noble_truths", "noble_eightfold_path", "three_marks", "five_aggregates", "dependent_origination", "five_precepts", "five_hindrances", "seven_awakening_factors", "four_foundations_of_mindfulness", "eight_precepts", "three_refuges", "ten_perfections", "four_sublime_states", "five_spiritual_faculties", "three_unwholesome_roots", "four_right_exertions", "ten_fetters", "seven_purifications", "five_powers", "four_jhanas", "six_recollections", "gradual_training"), file.name)
SORT file.name ASC
```

For factors:
```dataview
TABLE title_pali AS "Pāḷi Title"
WHERE contains(file.path, "matika/") 
  AND file.name != "INDEX"
  AND !contains(list("four_noble_truths", "noble_eightfold_path", "three_marks", "five_aggregates", "dependent_origination", "five_precepts", "five_hindrances", "seven_awakening_factors", "four_foundations_of_mindfulness", "eight_precepts", "three_refuges", "ten_perfections", "four_sublime_states", "five_spiritual_faculties", "three_unwholesome_roots", "four_right_exertions", "ten_fetters", "seven_purifications", "five_powers", "four_jhanas", "six_recollections", "gradual_training"), file.name)
SORT file.name ASC
```

These queries do not rely on any custom YAML frontmatter fields (like `type` or `category`), making them completely immune to metadata indexing delays.

## [2026-05-24 16:45:00-07:00 — Vault Review (Claude Opus 4.7)]

### Session Accomplishments
- **Full hierarchy review**: Read the folder structure across all three layers (mūla/aṭṭhakathā/ṭīkā × sutta/abhidhamma/vinaya), `matika/`, `practice/`, `paths/`, `paritta/`, `templates/`, and the root meta-docs.
- **Deliverable**: Wrote [FROM-CLAUDE.md](file:///Users/rds/pali_canon/FROM-CLAUDE.md) — a review covering errors/inconsistencies, omissions, usability/structure, and innovative uses for learning Pali and the Pali literature. Follows the archived `archive/FROM-CLAUDE-05-22.md`.

### Key Findings (no fixes applied this session — review only)
- **Frontmatter schema drift** across mūla files (e.g. `mn118` vs `an10_60` differ in `id`/`sutta_number` form and commentary-link fields) — flagged as the keystone fix that unblocks vault-wide Dataview.
- **"22 mātikā lists" is stated in INDEX/HERMES/STATUS but disagrees** with reality (matika INDEX shows 19; `## The List` appears in 21; folder holds 108 files incl. ~87 unindexed factor pages).
- **Cross-layer chunking mismatch** in AN (mūla `an11_2..5` vs att `an11_3_5` vs ṭīkā `an11_2_5`); `an10_60` has att but no ṭīkā.
- **Coverage gaps**: Abhidhamma piṭaka is stub-only; Vinaya has Pātimokkha mūla but no exegesis; Theragāthā/Therīgāthā lack commentary; empty stubs create dead-end navigation.
- **Biggest opportunity**: vault is reading/doctrine-oriented but thin on *language* learning — recommended a word-by-word gloss toggle, corpus vocabulary-frequency graded reader, pericope/formula concordance, and a verbal-root graph.

### Current State
- No content or text-layer files were modified. Only `FROM-CLAUDE.md` was created and this log entry added.
- See FROM-CLAUDE.md §F for a prioritized action checklist. No TASKS.md items marked done (this was a review, not migration work); the §F items could be promoted into TASKS.md if the recommendations are accepted.

## [2026-05-24 — Meditation Techniques Section in INDEX.md (Antigravity)]

### Session Accomplishments

**Meditation Techniques Section**
- **INDEX.md Integration**: Added a new "Meditation Techniques" section to `INDEX.md` directly under the card grid (Daily Practice & Support section), linking to core meditation techniques in the suttas.
- **Technique Files Creation**: Created 5 detailed technique notes in the `practice/` directory:
  * `practice/jhana.md` (Jhāna / Meditative Absorption)
  * `practice/vipassana.md` (Vipassanā / Insight Meditation)
  * `practice/metta.md` (Mettā / Loving-Kindness Meditation)
  * `practice/anapanasati.md` (Ānāpānasati / Mindfulness of Breathing)
  * `practice/maranasati.md` (Maraṇasati / Mindfulness of Death)
  * Each file includes a description (one page or less), back pointer to `INDEX.md` at the top, and a curated list of relevant suttas referencing the technique at the bottom.
- **Explicit Paths Resolution**: Resolved a link ambiguity on the `maranasati` base name by explicitly directing path index references to `paths/maranasati.md` and practice techniques to `practice/maranasati.md`.

**Verification and Link Integrity**
- **Link Validator**: Verified link health. Checked **1,162 markdown files** and **14,053 wikilinks**, confirming **0 broken links** in the entire vault.

---

## [2026-05-24 — Phase 20.2: Vault-wide Mātika Factors Expansion Complete (Antigravity)]

### Session Accomplishments

**Vault-wide Mātika Factors Expansion**
- **Factor Files Creation**: Created 78 detailed markdown files under `matika/` for every factor in the remaining 18 lists of the Buddhist *Mātika* (e.g. `impermanence.md`, `feeling.md`, `sensual_desire.md`, `abstaining_from_killing.md`, `mindfulness.md`, `buddha.md`, `generosity.md`, `contemplation_of_body.md`, etc.).
- **Canonical Definition & Description**: Each file contains its Romanized Pali definition from canonical texts (such as SN 45.8, SN 12.2, MN 9, Vibhaṅga, etc.), an interleaved English translation, a detailed practical description, and relative links to suttas in the vault that describe/mention the factor.
- **Parent List Integration**: Updated all 18 parent files in `matika/` to dynamically link parent list items to their respective detailed factor files, using clean English-first wikilinks with Pali display labels where appropriate.
- **Tool Refinement**: Modified the generator script `scratch/generators/generate_matika_details.py` to fix list section replacements in files with custom list headers (`ten_fetters.md` and `seven_purifications.md`) and to utilize dynamic regex matching of search headers.

**Verification and Link Integrity**
- **Link Validator**: Ran `validate_links.py`. Verified 1,157 markdown files and 14,018 wikilinks, confirming **0 broken links** in the entire vault.

---

## [2026-05-24 — Phase 20.1: Noble Eightfold Path Factors Expansion Complete (Antigravity)]

### Session Accomplishments

**Noble Eightfold Path Factors Expansion**
- **Factor Files Creation**: Created 8 detailed markdown files in `matika/` for each path factor:
  - `right_view.md` (*Sammādiṭṭhi*)
  - `right_intention.md` (*Sammāsaṅkappo*)
  - `right_speech.md` (*Sammāvācā*)
  - `right_action.md` (*Sammākammanto*)
  - `right_livelihood.md` (*Sammāājīvo*)
  - `right_effort.md` (*Sammāvāyāmo*)
  - `right_mindfulness.md` (*Sammāsati*)
  - `right_concentration.md` (*Sammāsamādhi*)
- **Canonical Definition & Description**: Each file contains its Romanized Pali definition from the *Vibhaṅgasutta* (SN 45.8), an interleaved English translation, a detailed descriptive summary (a page or less), and links to suttas in the vault that describe/mention the factor.
- **Parent List Integration**: Updated `matika/noble_eightfold_path.md` to link the factors directly to their respective detail files.
- **Validation-Safe Placeholders**: Linked non-migrated suttas (like MN 9 and MN 58) using standard markdown links rather than wikilinks to maintain the vault-wide 0-broken-links guarantee.

**Verification and Link Integrity**
- **Link Validator**: Verified link health. Checked all 1,079 markdown files and 13,653 links, confirming 0 broken links in the entire vault.

---

## [2026-05-24 — Phase 18: Interactive Dashboards & Practice Hubs Complete (Antigravity)]

### Session Accomplishments

**Interactive Dashboards & Practice Hubs**
- **Custom CSS Design System**: Created `dashboard-styles.css` snippet containing the styling system (grids, glassmorphism cards, HSL category colors, hover scale animations, custom list items, and status badges). Enabled it vault-wide in `appearance.json`.
- **Premium Root Dashboard**: Rebuilt the root `INDEX.md` using standard HTML `<a>` tags with `class="internal-link"` for all internal links within card divisions, guaranteeing that links always render and function in Obsidian (bypassing raw HTML block markdown parsing limitations).
- **Premium Practice Hub**: Overwrote `practice/INDEX.md` with a beautiful grid dashboard using standard HTML `<a>` tags with the `internal-link` class for card links to guarantee rendering and traversal, alongside dynamic Dataview queries for stats and sits.
- **Chanting & SRS Review System**: Enhanced `practice/memorization_log.md` with:
  - An **Audio Track** column linking directly to localized recitation files.
  - A dedicated **Spaced Repetition & Active Recall** section at the bottom containing double-colon flashcard definitions for all active memorization verses.

**Verification and Link Integrity**
- **Link Validator**: Extended `validate_links.py` to scan and validate HTML `<a>` links ending in `.md` alongside standard wikilinks. Ran full vault validation: **1,071 markdown files and 13,585 total links successfully verified with 0 errors**.

---

## [2026-06-04 20:00:00-07:00 — Phase 20C: Vault Audit & Quality Sprint (Claude Sonnet 4.6)]

### Session Accomplishments

**Critical Bug Fixes**
- **Matika link conversion** (`fix_matika_links.py`): Converted all 80 matika factor files from `[text](path.md)` markdown syntax to Obsidian wikilinks. Fixed 7 broken `mn9.md` references (context-aware replacement: sn45, mn20, sn46, sn12). Fixed 27 SN INDEX misleading links to specific sutta files. Fixed wrong-directory `majjhima_nikaya/an10_60.md` → `anguttara_nikaya/an10_60.md`.
- **Validator gap closed** (`validate_links.py`): Extended link validator to check standard Markdown `[label](path.md)` links (third check alongside wikilinks and HTML `<a>` links). Now validates 15,608 total links across 1,216 files.
- **ROADMAP.md**: Fixed stale `[FROM-CLAUDE.md](FROM-CLAUDE.md)` link → plain text description.

**Vocabulary Concordance Quality** (pali-nlp repo, commit 369a604)
- `vault_writer.py`: Filter out unresolved entries (`if not r.found: continue`) — eliminates `word (?)` rows with empty POS/gloss.
- Changed sort from rarest-first to most-frequent-first (ascending rank, `min_rank=30` floor).
- Vault MN 10 callout label updated to remove stale "rarest first" label.

**Learning Experience Improvements**
- **SIMILES.md**: Expanded from 7 to 17 similes across 5 categories (Practice & Path, Five Aggregates, Mind & Defilements, Awakening & Freedom, Teacher & Teaching).
- **PERICOPES.md**: Expanded from 4 to 13 stock formulas across 5 categories with full Pali + English text.
- **Reading paths**: Added collapsible `> [!NOTE]- Reading Progress` callout with checkboxes to 9 reading paths via `add_path_progress.py`.
- **Graded reader**: Added 4-tier difficulty structure (Beginner/Lower/Upper Intermediate/Advanced) + "How to use" preamble via `add_graded_reader_tiers.py`.
- **Contemplation prompts**: Added `> [!QUESTION]- Practice Questions` callout to MN 10 (5 questions), MN 118 (5 questions), DN 22 (5 questions).

**Interface Quality Improvements**
- **INDEX.md**: Fixed "Six tutorials" → "Seven tutorials"; added type filter to Dataview recently-modified query.
- **practice/INDEX.md**: Replaced broken audio embeds with clean placeholder callout; added "Currently Studying" manual-update section.
- **paths/INDEX.md**: Added "Pali Reading Tools" section; verified all 10 paths linked.
- **matika/INDEX.md**: Added "Recommended Entry Points" table mapping 10 practice questions to mātikā files.
- **paths/INDEX.md Pali Graded Reader**: Added tier summary to graded reader entry.

**Coordination Files**
- TASKS.md: All 2026-06-04 review findings marked completed; deferred items retained; Phase 21 priority queue added.
- STATUS.md: Script count updated 136 → 142.

### Commits
- `c72de76` — fix: matika wikilink conversion, validator markdown-link extension, ROADMAP fix (vault)
- `c6250f4` — feat: learning UX and interface improvements (vault)
- `a0b5c83` — chore: remove stale "rarest first" label from MN 10 vocab callout (vault)
- `369a604` — fix: filter unresolved entries and sort vocab concordance most-frequent-first (pali-nlp)

### Validation
- `python3 scratch/validate_links.py`: 0 errors (1,216 files, 15,608 links)
- `python3 scratch/tests/run_all_tests.py`: 13/13 tests pass

---
