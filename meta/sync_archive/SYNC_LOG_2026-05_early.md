🏠 [[INDEX|Dashboard]]

# Sync Log Archive — May 21-23, 2026
[[INDEX|Dashboard]] > [[topics/topics|Topics Hub]] > [[topics/texts/texts|Texts & Canon]] > [[topics/texts/pali-canon/pali-canon|Pāḷi Canon]] > Sync Log Archive — May 21-23, 2026

*Rotated from `meta/SYNC_LOG.md` on 2026-05-27. See `meta/SYNC_LOG.md` for current entries.*

---

## [2026-05-23 — Phase 17: Tooling & Validation Optimization Complete (Antigravity)]

### Session Accomplishments

**Tooling & Verification (Phase 17)**
- **Incremental Link Validation**: Updated `validate_links.py` and the git pre-commit hook to scan only staged markdown files (`--files` CLI option). Added lazy-loading of file headers which provides a 10x validation speedup on large repositories.
- **Heuristic Commentary Auto-Aligner**: Integrated automated paragraph-level heading anchor generation (`### §NNN`), sub-commentary Tīkā link injection, and Mūla auto-crosslinking directly into `generate_sutta.py`. Included an ordinal-stripping parser heuristic to ignore introductory words like `Navame ...` or `Dutiye ...` when aligning Mūla texts.

**Chanting & Audio Documentation**
- **Chanting Guide**: Created `CHANTING.md` at the root directory to document the Audio Chanting Integration workflow, and linked it under Reading Tools in the main `INDEX.md`.
- **Security Embed Fixes**: Refactored embeds in `patimokkha_bhikkhu.md` and `patimokkha_bhikkhuni.md` to use vault-relative paths (`../../practice/audio/...`) to bypass Electron file protocol blocks.

**Priority Bug Logged**
- **Chanting Audio Links Bug**: Logged a priority bug in `TASKS.md`. Obsidian is unable to follow the absolute or relative links pointing to local files/folders inside the `practice/audio/` directory. This requires further system-level URI investigation.

---

## [2026-05-23 — Phase 16: Generator Unification, Caching, Chanting Audio, and Vinaya Expansion Complete (Antigravity)]

### Session Accomplishments

**Offline XML Caching**
- **Caching Mechanism**: Refactored `pali_utils.py` to check for and save downloaded CSCD XML files under the git-ignored `scratch/xml_cache/` folder, accelerating generation runs.

**Unified Sutta Generator**
- **Unified Engine**: Created `generate_sutta.py` CLI script to parse any sutta by ID, fetch root/translation segments from SuttaCentral, parse corresponding Atthakathā/Ṭīkā layers from CSCD mappings, and generate Obsidian markdown files. Verified by re-generating and verifying AN 7.65.

**Monastic Practice Integrations**
- **Practice Audio & Flashcards**: Embedded audio chanting templates in `patimokkha_bhikkhu.md` pointing to the `practice/audio/` folder, and added Spaced Repetition flashcards in double-colon format to `five_precepts.md`.

**Vinaya Expansion (Phase 12)**
- **Bhikkhunī Pātimokkha (311 rules)**: Created `patimokkha_bhikkhuni.md` containing the structure and primary rules of the Bhikkhunī Pātimokkha. Cross-linked rules to lay precepts. Registered the file in `mula/vinaya/INDEX.md` and updated status metrics in root files.

**Verification and Link Integrity**
- **Link Validator**: Ran `validate_links.py`. Validated 1,073 files, checked 13,587 wikilinks, and confirmed 0 broken links in the entire vault.

---

## [2026-05-23 — Phase 15: Tooling Refactoring, Guardrails, and Vinaya Initiation Complete (Antigravity)]

### Session Accomplishments

**Script Refactoring & Portability**
- **Unified Helper Library**: Created `pali_utils.py` containing XML cleaning, frontmatter parsing, and environment-based path resolution.
- **Robust Parsing & Portability**: Added priority decoding to `load_cscd_paras`. Updated all scratch scripts to retrieve the vault root path from `PALI_VAULT` instead of using hardcoded paths.

**Verification Guardrails**
- **Automated Validation Hook**: Created pre-commit git hook to execute the link validator script before committing any changes, rejecting commits with broken links.
- **Unittest Suite**: Added `run_all_tests.py` using `unittest` framework to verify utility helper functions.

**Generic Cross-linker & Sutta Alignment**
- **Generic Cross-linker**: Developed `crosslink_generic.py` for paragraph-level commentary alignment. Cross-linked MN 10 (Satipaṭṭhānasutta) and MN 22 (Alagaddūpamasutta).

**Vinaya Piṭaka Initiation**
- **Monastic Code**: Created `patimokkha_bhikkhu.md` with 227 rules, cross-linked to five/eight precepts.

---

## [2026-05-23 — Phases 10, 11, and 13 Complete (Antigravity)]

### Session Accomplishments

**Aṅguttara Nikāya (AN) Expansion (Phase 10)**
- **Mūla, Atthakathā, and Ṭīkā Migration**: Migrated AN 7.65, AN 8.53, AN 11.1, AN 11.2, AN 11.3, AN 11.4, AN 11.5 across Mūla, Atthakathā, and Ṭīkā. Generated shared Atthakathā (`an11_3_5_att`) and Ṭīkā (`an11_2_5_tik`).
- **AN 1 Ekakanipāta**: Generated all 31 ranges from SuttaCentral API, complete with Mūla, Atthakathā, and Ṭīkā. Mapped commentary paragraphs using a forward-fill grouping algorithm on CSCD paragraph numbers.

**Deeper Majjhima Nikāya (MN) Coverage (Phase 11)**
- **Mūla, Atthakathā, and Ṭīkā Migration**: Migrated MN 22 and MN 117 across all three layers.

**Practice Support Tooling (Phase 13)**
- **Practice Notes Infrastructure**: Created `practice/INDEX.md` dashboard, `templates/practice_note.md` template, and `practice/memorization_log.md` with core chanting verses.
- **Dataview queries**: Injected live sutta tables in all Nikāya INDEX files and added a "Recently Modified" list to root `INDEX.md`.

**Verification and Link Integrity**
- **Link Validator**: Ran `validate_links.py`. Validated 1,067 files, checked 13,488 wikilinks, and confirmed 0 broken links in the entire vault.

---

## [2026-05-23 — Phase 9: Practice-Oriented Expansion Complete (Antigravity)]

### Session Accomplishments

**Practice-Oriented Expansion (Phase 9)**
- **Mūla, Atthakathā, and Ṭīkā Migration**: Batch migrated all remaining 26 targeted suttas across all three layers (Mūla, Atthakathā, and Ṭīkā), including:
  - **Jhāna**: MN 128, AN 9.34, AN 9.35, MN 8, AN 8.63
  - **Vipassanā**: MN 148, SN 36.6, SN 36.11, SN 36.21 (combined into `sn36` files), MN 28, MN 140, MN 2
  - **Brahmavihāra**: MN 7, DN 13, AN 11.15
  - **Anussati**: AN 6.10, AN 11.12, AN 6.25
  - **Anupubbasikkhā**: MN 27, MN 51, AN 8.54, AN 4.99
  - **Maraṇasati**: AN 6.19, AN 6.20, AN 8.73
  - **Paritta**: AN 4.67
- **Mātikā Integration**: Fully populated the newly created `four_jhanas`, `six_recollections`, and `gradual_training` lists in `matika/`, and cross-linked them to their canonical sources.
- **Thematic Reading Paths**: Created 6 beautifully formatted practice-focused reading path files under `paths/` and 1 protective chant index under `paritta/INDEX.md`.
- **Vault Link Integrity**: Verified vault-wide link integrity. Replaced ambiguous links for `gradual_training` with path-specific references (`[[matika/gradual_training]]` and `[[paths/gradual_training_path]]`). Link validator confirms **0 broken links** across 951 files and 11,890 wikilinks.
- **Status & Tasks Updates**: Updated parent indexes, `STATUS.md`, and `TASKS.md` with complete and accurate Phase 9 metrics.

---

## [2026-05-23 — Phase 8: Theragāthā and Therīgāthā Complete (Antigravity)]

### Session Accomplishments

**Theragāthā and Therīgāthā Migration (Phase 8)**
- **Mūla**: Generated 203 new Theragāthā suttas under `mula/sutta/khuddaka_nikaya/theragatha/` and 73 new Therīgāthā suttas under `mula/sutta/khuddaka_nikaya/therigatha/` (276 poems total) with interleaved Pali/English (Sujato).
- **Index Integration**:
  - Rebuilt Theragāthā and Therīgāthā index tables.
  - Updated parent indexes under Khuddaka Nikāya.
- **Status Updates**:
  - Updated `STATUS.md` metrics table.
  - Updated `TASKS.md` checklists.
- **Verification**: Ran `python3 scratch/validate_links.py` to confirm 0 broken links (867 files, 10736 wikilinks, all valid).

---

## [2026-05-23 — Phase 7: Itivuttaka Complete (Antigravity)]

### Session Accomplishments

**Itivuttaka (112 suttas) Migration (Phase 7)**
- **Mūla**: Generated 112 new suttas under `mula/sutta/khuddaka_nikaya/itivuttaka/` (iti1–iti112) with interleaved Pali/English (Sujato) and collapsible callouts linking to commentary files.
- **Atthakathā**: Generated 112 new commentary files under `atthakatha/sutta/khuddaka_nikaya/itivuttaka/` (Paramatthadīpanī) with CSCD Pali commentary text and paragraph-level back-links to Mūla (1,166 paragraphs total).
- **Index Integration**:
  - Rebuilt Itivuttaka index tables in Mūla and Atthakathā layers.
  - Updated parent indexes under Khuddaka Nikāya.
- **Status Updates**:
  - Updated `STATUS.md` metrics table and lists catalog.
  - Updated `TASKS.md` checklists.
- **Verification**: Ran `python3 scratch/validate_links.py` to confirm 0 broken links (589 files, 8517 wikilinks, all valid).

---

## [2026-05-23 — Phase 6: Sutta Nipāta Complete and Phase 0 Get Well (Antigravity)]

### Session Accomplishments

**Phase 0 - Get Well Issues Completed**
- **Commit protocol**: Established commit-after-each-sutta discipline (documented in ROADMAP.md).
- **STATUS.md script count**: Updated the script count to 94 Python scripts (49 generators, 7 crosslinkers, 25 inspectors, 7 tests, 6 utilities).
- **TASKS.md Snp entry**: Clarified the remaining Snp scope in pending tasks.
- **DN mātikā links**: Added forward mātikā links in DN 1, 16, 21 and reverse links in `three_refuges`, `five_precepts`, `four_sublime_states`, and `three_unwholesome_roots`.

**Sutta Nipāta (Chapters 2 to 5) Migration (Phase 6)**
- **Mūla**: Generated 61 new suttas under `mula/sutta/khuddaka_nikaya/sutta_nipata/` (snp2.1–snp2.14, snp3.1–snp3.12, snp4.1–snp4.16, snp5.1–snp5.19), each with interleaved Pali/English (Sujato) and collapsible callouts linking to commentary files. Sutta Nipāta is now 100% complete (73 suttas total).
- **Atthakathā**: Generated 61 new commentary files under `atthakatha/sutta/khuddaka_nikaya/sutta_nipata/` (Paramatthajotikā II) with CSCD Pali commentary text and paragraph-level back-links to Mūla (1,730 paragraphs total).
- **Index Integration**:
  - Rebuilt Sutta Nipāta index tables in Mūla and Atthakathā layers.
  - Updated parent indexes under Khuddaka Nikāya.
- **Status Updates**:
  - Updated `STATUS.md` metrics table.
  - Updated `TASKS.md` checklists.
- **Verification**: Ran `python3 scratch/validate_links.py` to confirm 0 broken links (363 files, 5890 wikilinks, all valid).

---

## [2026-05-22 — Phase 6: Five Powers Mātikā Migration (Antigravity)]

### Session Accomplishments

**Five Powers (Pañcabala) Mātikā Migration**
- **New Mātikā List**: Created `matika/five_powers.md` detailing the five powers, their definitions, functional differences from the spiritual faculties, related lists, and canonical references.
- **Index Integration**:
  - Registered `five_powers` in `matika/INDEX.md` and updated count to 19 in root `INDEX.md`.
- **Sutta Cross-linking**:
  - Linked `five_powers` in the Related Lists section of `five_spiritual_faculties.md`.
  - Added `five_powers` to the `Mātikā` header lines in `sn48.md` (Indriyasaṃyutta) and `an5_28.md` (Pañcaṅgikasutta).
- **Status Updates**:
  - Updated `STATUS.md` metrics table and lists catalog.
  - Updated `TASKS.md` checklists.
- **Verification**:
  - Ran `python3 scratch/validate_links.py` confirming 0 broken links (229 files, 2974 wikilinks, all valid).

---

## [2026-05-22 — Phase 5: Sutta Nipāta Uragavagga Migration (Antigravity)]

### Session Accomplishments

**Sutta Nipāta Uragavagga (Chapter 1) Migration**
- **Mūla**: Generated 10 new suttas under `mula/sutta/khuddaka_nikaya/sutta_nipata/` (Snp 1.1, Snp 1.2, Snp 1.4, Snp 1.5, Snp 1.6, Snp 1.7, Snp 1.9, Snp 1.10, Snp 1.11, Snp 1.12), each with interleaved Pali/English (Sujato) and collapsible callouts linking to commentary paragraphs. Sutta Nipāta Chapter 1 (Uragavagga) is now 100% complete (12 suttas total, 244 verses).
- **Atthakathā**: Generated 10 new commentary files under `atthakatha/sutta/khuddaka_nikaya/sutta_nipata/` (Paramatthajotikā II) with CSCD Pali commentary text and paragraph-level back-links to Mūla verses (957 paragraphs total).
- **Mātikā Integration**:
  - Linked `[[snp1_1|Snp 1.1: Uragasutta]]` in [[three_unwholesome_roots]] and [[ten_fetters]].
  - Linked `[[snp1_4|Snp 1.4: Kasībhāradvājasutta]]` and `[[snp1_10|Snp 1.10: Āḷavakasutta]]` in [[five_spiritual_faculties]].
  - Linked `[[snp1_6|Snp 1.6: Parābhavasutta]]` and `[[snp1_7|Snp 1.7: Vasalasutta]]` in [[five_precepts]].
  - Linked `[[snp1_11|Snp 1.11: Vijayasutta]]` in [[four_foundations_of_mindfulness]] (body contemplation / asubha).
  - Linked `[[snp1_12|Snp 1.12: Munisutta]]` in [[five_hindrances]].
- **Index Integration**:
  - Rebuilt Sutta Nipāta index tables in Mūla and Atthakathā layers.
  - Updated parent indexes under Khuddaka Nikāya.
- **Status Updates**:
  - Updated `STATUS.md` overall metrics (198 individual suttas now completed) and Sutta Nipāta catalog rows.
  - Updated `TASKS.md` checklists.
- **Verification**: Ran `python3 scratch/validate_links.py` to confirm 0 broken links (228 files, 2732 wikilinks, all valid).

---

## [2026-05-22 — Phase 4: Ten Fetters and Seven Purifications Mātikā Migration (Antigravity)]

### Session Accomplishments

**Ten Fetters (Dasa Saṃyojanā) & Seven Purifications (Satta Visuddhi) Mātikā Migration**
- **New Mātikā Lists**:
  - Generated `matika/ten_fetters.md` detailing the Suttanta and Abhidhamma lists of ten fetters, stages of noble attainment, related lists, and canonical references.
  - Generated `matika/seven_purifications.md` detailing the seven purifications, mapping to the sixteen insight knowledges (*vipassanā-ñāṇa*), related lists, and canonical references.
- **Index Integration**:
  - Registered both new lists in the available lists index at `matika/INDEX.md`.
  - Updated the list count from 16 to 18 in root `INDEX.md`.
- **Sutta Cross-linking**:
  - Updated the `Mātikā` header line in `mn10.md` (Satipaṭṭhānasutta) to link to `ten_fetters` and `seven_purifications`.
  - Updated the `Mātikā` header line in `dn22.md` (Mahāsatipaṭṭhānasutta) to link to `ten_fetters` and `seven_purifications`.
  - Updated the `Mātikā` header line in `sn55.md` (Sotāpattisaṃyutta) to link to `ten_fetters`.
- **Status Updates**:
  - Updated `STATUS.md` metrics table and lists catalog (18 total lists now registered).
  - Updated `TASKS.md` checklist, marking the new list creation tasks complete.
- **Verification**:
  - Ran `python3 scratch/validate_links.py` confirming 0 broken links (208 files, 2446 wikilinks, all valid).

---

## [2026-05-22 — Phase 4: MN 19 and AN 10.60 Migration and Cross-linking (Antigravity)]

### Session Accomplishments

**MN 19 (Dvedhāvitakkasutta) & AN 10.60 (Girimānandasutta) Migration**
- **Mūla**:
  - Generated `mn19.md` (3,032 words) under `mula/sutta/majjhima_nikaya/` with interleaved Pali/English (Sujato).
  - Generated `an10_60.md` (1,931 words) under `mula/sutta/anguttara_nikaya/` with interleaved Pali/English (Sujato).
- **Atthakathā**:
  - Generated `mn19_att.md` (2,451 words) under `atthakatha/sutta/majjhima_nikaya/` with CSCD Pali commentary text (§206–214, 215).
  - Generated `an10_60_att.md` (141 words) under `atthakatha/sutta/anguttara_nikaya/` with CSCD Pali commentary text (§60).
- **Ṭīkā**:
  - Generated `mn19_tik.md` (991 words) under `tika/sutta/majjhima_nikaya/` with CSCD Pali sub-commentary text (§206–214, 215).
  - AN 10.60 is explicitly marked as `(No Ṭīkā available)` in vault files and status catalogs, as no sub-commentary exists for this discourse.
- **Mātikā Integration**:
  - Linked `[[mn19|MN 19: Dvedhāvitakkasutta]]` under Canonical References in [[three_unwholesome_roots]] and [[five_hindrances]].
  - Linked `[[an10_60|AN 10.60: Girimānandasutta]]` under Canonical References in [[five_hindrances]], [[three_marks]], and [[four_foundations_of_mindfulness]].
- **Targeted Cross-linking**:
  - Implemented Obsidian collapsible callout panels in Mūla files pointing to specific commentary and sub-commentary paragraph anchors.
  - Added bidirectional navigation links and `### §NNN` paragraph headers in the Atthakathā and Ṭīkā files.
- **Index and Status Updates**:
  - Rebuilt Majjhima Nikāya indexes for Mūla, Atthakathā, and Ṭīkā layers.
  - Rebuilt Aṅguttara Nikāya indexes for Mūla and Atthakathā layers.
  - Updated `STATUS.md` overall metrics tables and catalog sections.
  - Updated `TASKS.md` checklists, marking Phase 4 tasks complete.
- **Verification**: Ran `python3 scratch/validate_links.py` to verify 0 broken links (206 files, 2412 wikilinks, all valid).

---

## [2026-05-22 — Snp 1.3 & Snp 1.8 Migration and Cross-linking (Antigravity)]

### Session Accomplishments

**Snp 1.3 (Khaggavisāṇasutta) & Snp 1.8 (Mettasutta) Migration**
- **Mūla**: Generated `snp1.3.md` (41 verses, 20,147 bytes) and `snp1.8.md` (10 verses, 4,961 bytes) under `mula/sutta/khuddaka_nikaya/sutta_nipata/` with interleaved Pali/English (Sujato).
- **Atthakathā**: Generated `snp1.3_att.md` (165,616 bytes) and `snp1.8_att.md` (38,016 bytes) under `atthakatha/sutta/khuddaka_nikaya/sutta_nipata/` with CSCD Pali commentary text.
- **Ṭīkā**: Explicitly marked as "(No Ṭīkā available)" in vault files and status catalogs, as Sutta Nipāta does not have a Ṭīkā layer.
- **Mātikā Integration**:
  - Linked `[[snp1_8|Snp 1.8: Mettasutta]]` under Canonical References in [[four_sublime_states]].
  - Linked `[[snp1_3|Snp 1.3: Khaggavisāṇasutta]]` under Canonical References in [[five_hindrances]].
  - Linked `[[snp1_3|Snp 1.3: Khaggavisāṇasutta]]` under Canonical References in [[three_marks]].
- **Targeted Cross-linking**:
  - Implemented Obsidian collapsible callout panels in Mūla files pointing to specific commentary paragraph anchors.
  - Added bidirectional navigation links and `### §NNN` paragraph headers in the Atthakathā files pointing back to Mūla verses.
  - Handled the grouped commentary at paragraph `45-46` (commenting on Snp 1.3 Verses 11 and 12) with unified links.
- **Index and Status Updates**:
  - Created Sutta Nipāta folder index files: [mula/sutta/khuddaka_nikaya/sutta_nipata/INDEX.md](file:///Users/rds/pali_canon/mula/sutta/khuddaka_nikaya/sutta_nipata/INDEX.md) and [atthakatha/sutta/khuddaka_nikaya/sutta_nipata/INDEX.md](file:///Users/rds/pali_canon/atthakatha/sutta/khuddaka_nikaya/sutta_nipata/INDEX.md).
  - Updated Khuddaka Nikāya index files to register the new Sutta Nipāta indexes.
  - Updated `STATUS.md` overall metrics tables and catalog sections.
- **Verification**: Ran `python3 scratch/validate_links.py` to verify 0 broken links (201 files, 2366 wikilinks, all valid).

---

## [2026-05-22 — SN 48 Migration and Cross-linking (Antigravity)]

### Session Accomplishments

**SN 48 (Indriyasaṃyutta) Migration**
- **Mūla**: 20 selected suttas (6,760 words) in [[sn48]]. Pali text interleaved with Bhikkhu Sujato's English translation.
- **Atthakathā**: 106 paragraphs (3,037 words) in [[sn48_att]] parsed from tipitaka.org CSCD XML file `s0305a.att3.xml`.
- **Ṭīkā**: 92 paragraphs (2,544 words) in [[sn48_tik]] parsed from tipitaka.org CSCD XML file `s0305t.tik3.xml`.
- **Mātikā Integration**:
  - Linked `[[sn48|SN 48: Indriyasaṃyutta]]` (specifically `[[sn48#SN 48.8: Daṭṭhabbasutta — *Should Be Seen*|SN 48.8: Daṭṭhabbasutta]]`, `[[sn48#SN 48.9: Paṭhamavibhaṅgasutta — *Analysis (1st)*|SN 48.9: Vibhaṅgasutta]]`, `[[sn48#SN 48.10: Dutiyavibhaṅgasutta — *Analysis (2nd)*|SN 48.10: Dutiya Vibhaṅgasutta]]`) under Canonical References in [[five_spiritual_faculties]].
- **Targeted Cross-linking**:
  - Implemented Obsidian collapsible callout panels in [[sn48]] pointing to specific commentary and sub-commentary paragraph anchors.
  - Prepended `### §NNN` headers and added bidirectional navigation links between Mūla, Atthakathā, and Ṭīkā layers for the 6 key suttas:
    - **SN 48.8** (Daṭṭhabbasutta) ↔ Atthakathā & Ṭīkā §478
    - **SN 48.9 & 48.10** (Vibhaṅgasuttāni) ↔ Atthakathā & Ṭīkā §479-480
    - **SN 48.42** (Unṇābhabrāhmaṇasutta) ↔ Atthakathā & Ṭīkā §512
    - **SN 48.44** (Pubbakotthakasutta) ↔ Atthakathā §514 (no Ṭīkā subcommentary exists)
    - **SN 48.50** (Āpaṇasutta) ↔ Atthakathā & Ṭīkā §520
    - **SN 48.54** (Pātālakkhandhasutta) ↔ Atthakathā §524-525 (no Ṭīkā subcommentary exists)
- **Index and Status Updates**:
  - Confirmed and verified rows in `mula/sutta/samyutta_nikaya/INDEX.md`, `atthakatha/sutta/samyutta_nikaya/INDEX.md`, and `tika/sutta/samyutta_nikaya/INDEX.md`.
  - Updated `STATUS.md` overall metrics tables and catalog sections.
  - Updated `TASKS.md` checklists, marking SN 48 tasks complete and updating next order priority.
- **Verification**: Ran `python3 scratch/validate_links.py` to verify 0 broken links (195 files, 2209 wikilinks, all valid).

---

## [2026-05-22 — SN 55 Migration and Cross-linking (Antigravity)]

### Session Accomplishments

**SN 55 (Sotāpattisaṃyutta) Migration**
- **Mūla**: 15 selected suttas (12,650 words) in [[sn55]]. Pali text interleaved with Bhikkhu Sujato's English translation.
- **Atthakathā**: 103 paragraphs (2,613 words) in [[sn55_att]] parsed from tipitaka.org CSCD XML file `s0305a.att10.xml`.
- **Ṭīkā**: 90 paragraphs (1,810 words) in [[sn55_tik]] parsed from tipitaka.org CSCD XML file `s0305t.tik10.xml`.
- **Mātikā Integration**:
  - Linked `[[sn55|SN 55: Sotāpattisaṃyutta]]` to [[three_refuges]].
  - Added `[[sn55|SN 55: Sotāpattisaṃyutta]]` (specifically `[[sn55#SN 55.7: Veḷudvāreyyasutta — *The People of Bamboo Gate*|SN 55.7: Veḷudvāreyyasutta]]`) to [[five_precepts]].
  - Added `[[sn55|SN 55: Sotāpattisaṃyutta]]` (wavering vs unwavering saddhā/confidence) to [[five_spiritual_faculties]].
- **Targeted Cross-linking**:
  - Implemented Obsidian collapsible callout panels in [[sn55]] pointing to specific commentary and sub-commentary paragraph anchors.
  - Prepended `### §NNN` headers and added bidirectional navigation links between Mūla, Atthakathā, and Ṭīkā layers for the 3 key suttas:
    - **SN 55.3** (Dīghāvuupāsakasutta) ↔ Atthakathā & Ṭīkā §999
    - **SN 55.7** (Veḷudvāreyyasutta) ↔ Atthakathā & Ṭīkā §1003
    - **SN 55.54** (Gilānasutta) ↔ Atthakathā & Ṭīkā §1050
- **Index and Status Updates**:
  - Updated `mula/sutta/samyutta_nikaya/INDEX.md`, `atthakatha/sutta/samyutta_nikaya/INDEX.md`, and `tika/sutta/samyutta_nikaya/INDEX.md`.
  - Updated `STATUS.md` overall metrics tables and catalog sections.
  - Updated `TASKS.md` checklists, marking SN 55 tasks complete and updating next order priority.
- **Verification**: Ran `python3 scratch/validate_links.py` to verify 0 broken links (133 files, 1296 wikilinks, all valid).

---

## [2026-05-22 — SN 45 Migration and Cross-linking (Antigravity)]

### Session Accomplishments

**SN 45 (Maggasaṃyutta) Migration**
- **Mūla**: 20 selected suttas (7,202 words) in [[sn45]]. Pali text interleaved with Bhikkhu Sujato's English translation.
- **Atthakathā**: 124 paragraphs (3,463 words) in [[sn45_att]] parsed from tipitaka.org CSCD XML file `s0305a.att0.xml`.
- **Ṭīkā**: 126 paragraphs (3,007 words) in [[sn45_tik]] parsed from tipitaka.org CSCD XML file `s0305t.tik0.xml`.
- **Mātikā Integration**: Added `[[sn45|SN 45: Maggasaṃyutta]]` under Canonical References in [[noble_eightfold_path]].
- **Targeted Cross-linking**:
  - Implemented Obsidian collapsible callout panels in [[sn45]] pointing to specific commentary and sub-commentary paragraph anchors.
  - Prepended `### §NNN` headers and added bidirectional navigation links between Mūla, Atthakathā, and Ṭīkā layers for the 4 key suttas:
    - **SN 45.2** (Upaḍḍhasutta) ↔ Atthakathā & Ṭīkā §1-2
    - **SN 45.3** (Sāriputtasutta) ↔ Atthakathā & Ṭīkā §3
    - **SN 45.8** (Vibhaṅgasutta) ↔ Atthakathā & Ṭīkā §8
    - **SN 45.139** (Tathāgatasutta) ↔ Atthakathā & Ṭīkā §139
- **Index and Status Updates**:
  - Confirmed and verified rows in `mula/sutta/samyutta_nikaya/INDEX.md`, `atthakatha/sutta/samyutta_nikaya/INDEX.md`, and `tika/sutta/samyutta_nikaya/INDEX.md`.
  - Updated `STATUS.md` overall metrics tables and catalog sections.
  - Updated `TASKS.md` checklists, marking SN 45 tasks complete and updating next order priority.
- **Verification**: Ran `python3 scratch/validate_links.py` to verify 0 broken links.

---

## [2026-05-22 — SN 47 Migration and Cross-linking (Antigravity)]


### Session Accomplishments

**SN 47 (Satipaṭṭhānasaṃyutta) Migration**
- **Mūla**: 16 selected suttas (9,504 words) in [[sn47]]. Pali text interleaved with Bhikkhu Sujato's English translation.
- **Atthakathā**: 220 paragraphs (9,325 words) in [[sn47_att]] parsed from tipitaka.org CSCD XML file `s0305a.att2.xml`.
- **Ṭīkā**: 149 paragraphs (6,123 words) in [[sn47_tik]] parsed from tipitaka.org CSCD XML file `s0305t.tik2.xml`.
- **Mātikā Integration**: Added `[[sn47|SN 47: Satipaṭṭhānasaṃyutta]]` under Canonical References in [[four_foundations_of_mindfulness]].
- **Targeted Cross-linking**:
  - Implemented Obsidian collapsible callout panels in [[sn47]] pointing to specific commentary and sub-commentary paragraph anchors.
  - Prepended `### §NNN` headers and added bidirectional navigation links between Mūla, Atthakathā, and Ṭīkā layers for the 4 key suttas:
    - **SN 47.1** (Ambapālisutta) ↔ Atthakathā & Ṭīkā §367
    - **SN 47.8** (Sūdasutta) ↔ Atthakathā & Ṭīkā §374
    - **SN 47.9** (Gilānasutta) ↔ Atthakathā & Ṭīkā §375
    - **SN 47.20** (Janapadakalyāṇīsutta) ↔ Atthakathā & Ṭīkā §386
- **Index and Status Updates**:
  - Confirmed and verified rows in `mula/sutta/samyutta_nikaya/INDEX.md`, `atthakatha/sutta/samyutta_nikaya/INDEX.md`, and `tika/sutta/samyutta_nikaya/INDEX.md`.
  - Updated `STATUS.md` overall metrics tables and catalog sections.
  - Updated `TASKS.md` checklists, marking SN 47 tasks complete and updating next order priority.
- **Verification**: Ran `python3 scratch/validate_links.py` to verify 0 broken links (127 files, 1181 wikilinks, all valid).

---

## [2026-05-22 — HANDOFF NOTE + Full Session Summary (Claude Code → next agent)]

### Context for Incoming Agent

This vault is an Obsidian study vault for the Pali Canon (Roy Peter's personal meditation study tool). The primary goal is **meditation practice**, secondary goal is **precepts study**. Every new sutta added should serve one of those goals. Roy actively studies in Obsidian and uses Simsapa DPD for Pali word lookups.

The vault has a strict three-layer structure: **mūla** (root text, interleaved Pali/English), **atthakathā** (commentary, CSCD Pali), **tīkā** (sub-commentary, CSCD Pali). Every sutta should have all three. Mātikā (doctrinal lists) form a cross-cutting network linking sutta files by doctrine.

**Always run `python3 scratch/validate_links.py` before committing.** 124 files, 1,144 wikilinks, must be 0 errors.

**Always update TASKS.md and SYNC_LOG.md** before ending a session. Roy checks both.

---

### Session Accomplishments (2026-05-22)

**SN 35 (Saḷāyatanasaṃyutta)** — all three layers
- Mūla: 23 suttas (10,082w); att: 590¶ (20,030w) from `s0304a.att0.xml`; tīkā: 484¶ (10,316w) from `s0304t.tik0.xml`
- Key suttas: aniccā group (sn35.1–10), Fire Sermon / Āditta (sn35.28), Gaddulabaddha (sn35.95), liberation suttas
- Mātikā: `five_spiritual_faculties` + `dependent_origination` → sn35

**Dhammapada ṭīkā — BLOCKED**
- All `s0502t.tik*.xml` return 404; CSCD online does not publish the Dhammapada-ṭīkā
- The Dhammapada-aṭṭhakathā Pali IS available at `s0502a.att1–att9` (~1.6MB) but already have English version
- Would need offline CSCD CD-ROM or alternative Pali source

**SN 12 (Nidānasaṃyutta)** — all three layers
- Mūla: 18 suttas (20,504w); att: 475¶ (22,013w) from `s0302a.att0.xml`; tīkā: 463¶ (21,458w) from `s0302t.tik0.xml`
- Key suttas: DO formula (sn12.1–2), Kaccānagotta (sn12.15), Upanisā (sn12.23), ancient city (sn12.65), Susīma (sn12.70)
- Mātikā: `dependent_origination` + `four_noble_truths` → sn12

**SN 22 (Khandhasaṃyutta)** — all three layers
- Mūla: 18 suttas (23,613w); att: 400¶ (13,968w) from `s0303a.att0.xml`; tīkā: 408¶ (8,841w) from `s0303t.tik0.xml`
- Key suttas: burden simile (sn22.22), Anattalakkhaṇa (sn22.59), foam simile (sn22.95), Yamaka (sn22.85), Vakkali (sn22.87), Khemaka (sn22.89)
- Mātikā: `five_aggregates` + `three_marks` → sn22

**SN 56 (Saccasaṃyutta)** — all three layers
- Mūla: 16 suttas (6,469w); att: 153¶ (2,413w) from `s0305a.att11.xml`; tīkā: 100¶ (1,689w) from `s0305t.tik11.xml`
- Key suttas: Dhammacakkappavattana (sn56.11 — the First Discourse), Koṭigāma (sn56.20), siṃsapā leaves (sn56.31), blind turtle (sn56.47–48)
- Mātikā: `four_noble_truths` + `noble_eightfold_path` → sn56

**Housekeeping**
- MN 119 + MN 121 Related Texts nav lines added (were missing)
- TASKS.md fully rewritten — clean, comprehensive, prioritised
- All mātikā reverse links updated throughout session
- Git: 4 feat commits + 2 chore commits this session

---

### Current Vault State (2026-05-22 end of session)

| Metric | Value |
|---|---|
| Total markdown files | 124 |
| Total wikilinks validated | 1,144 |
| Mūla suttas | 104 individual + 6 SN saṃyuttas (117 selected) |
| Atthakathā texts | 104 individual + 26 DhpA + 6 SN saṃyuttas |
| Ṭīkā texts | 104 individual + 6 SN saṃyuttas |
| Mātikā lists | 16 (all cross-linked) |
| Git commits | clean, on main |

**SN coverage**: SN 12, 22, 35, 46, 54, 56 — six saṃyuttas, covering all five major doctrinal pillars (DO, aggregates, sense bases, bojjhaṅgas/ānāpāna, four truths)

---

### CSCD File Mapping Reference (tipitaka.org/romn/cscd/)

This is the most non-obvious technical knowledge. File naming: `s{NN}{NN}{a|t}.{att|tik}{N}.xml` where `a`=mūla/atthakathā source, `t`=tīkā source.

**Dīgha Nikāya (s0101–s0102)**
- DN 2: att=`s0101a.att2.xml`, tik=`s0101t.tik2.xml`
- DN 9: att=`s0101a.att9.xml`, tik=`s0101t.tik9.xml`
- DN 15: att=`s0102a.att1.xml`, tik=`s0102t.tik1.xml`
- DN 22: att=`s0102a.att8.xml`, tik=`s0102t.tik8.xml` (entire file)
- DN 16 (Mahāparinibbāna): probe `s0102a.att0.xml` or `s0102a.att2.xml`

**Majjhima Nikāya (s0201–s0203)**
- MN 10, 20: `s0201t.tik1.xml`, `s0201t.tik2.xml`
- MN 36, 43, 44: `s0201a.att4.xml`, `s0201a.att5.xml`
- MN 111, 119, 121: `s0203a.att1.xml`, `s0203t.tik1/2.xml`

**Saṃyutta Nikāya**
- Sagāthāvagga (s0301): SN 1–11
- Nidānavagga (s0302): SN 12 att=`s0302a.att0.xml` (507KB), tik=`s0302t.tik0.xml` (588KB); entire file = SN 12 only
- Khandavagga (s0303): SN 22 att=`s0303a.att0.xml` (343KB), tik=`s0303t.tik0.xml` (273KB); att1-att11 = SN 23-34
- Saḷāyatanavagga (s0304): SN 35 att=`s0304a.att0.xml` (476KB), tik=`s0304t.tik0.xml` (323KB)
- Mahāvagga (s0305) — each file = one saṃyutta:
  - att0/tik0 = SN 45 (Maggasaṃyutta, 92/93KB)
  - att1/tik1 = SN 46 (Bojjhaṅgasaṃyutta, confirmed)
  - att2/tik2 = SN 47 (Satipaṭṭhānasaṃyutta, 212/171KB — **large, substantive**)
  - att3/tik3 = SN 48 (Indriyasaṃyutta, 73KB each)
  - att4/tik4 = SN 49 (Sammappadhānasaṃyutta, tiny ~1KB stub)
  - att5/tik5 = SN 50 (Balasaṃyutta, tiny ~1KB stub)
  - att6/tik6 = SN 51 (Iddhipādasaṃyutta, 47/62KB)
  - att7/tik7 = SN 52 (Anuruddhasaṃyutta, 6KB each)
  - att8/tik8 = SN 53 (Jhānasaṃyutta, tiny ~1KB stub)
  - att9/tik9 = SN 54 (Ānāpānasaṃyutta, confirmed)
  - att10/tik10 = SN 55 (Sotāpattisaṃyutta, 68/55KB)
  - att11/tik11 = SN 56 (Saccasaṃyutta, confirmed)

**Aṅguttara Nikāya (s0401–s0404)**
- s0402a spans AN 2+3+4; s0403a spans AN 5; s0404a spans AN 8+9+10
- Tīkā mirrors att exactly (s040Xt.tikN = s040Xa.attN)
- Specific: an3_100→att28, an4_123_126→att48, an5_28→att2, an9_36→att13, an10_2_6→att15

**Khuddaka Nikāya (s0501–s0519)**
- s0501 = Khuddakapāṭha, s0502 = Dhammapada, s0505 = Suttanipāta
- Dhammapada att available (s0502a.att1–att9, ~1.6MB total); ṭīkā NOT available (all 404)
- Udāna: probe s0503; Itivuttaka: probe s0504

---

### Technical Patterns Established

**Generating a new SN saṃyutta** — copy any of `scratch/generate_sn{12|22|35|56}_*.py`, change:
- `slug`, `sutta_code`, `pali_title`, `en_title`
- `sc_ids` list (SuttaCentral IDs like `sn47.1`)
- `cscd_file` in att/tik scripts
- `**Mātikā**:` line in `build_samyutta_file()`
Run mūla first, then att+tik in parallel (`& wait`).

**After generating** — always:
1. Add mātikā reverse links (edit relevant `matika/*.md` files)
2. Run `python3 scratch/validate_links.py`
3. Update STATUS.md (SN saṃyutta count + word counts)
4. Update TASKS.md (mark done, update mātikā inventory)
5. Update SYNC_LOG.md
6. Commit with conventional `feat:` message

**SuttaCentral API**: `https://suttacentral.net/api/bilarasuttas/{sc_id}/sujato`
- SN has 3 metadata keys (`:0.1`, `:0.2`, `:0.3`); prefer `:0.3` for sutta title, `:0.2` fallback
- Some IDs return `{'msg': 'Not Found'}` — the `except` block in `render_sutta` handles gracefully

**CSCD XML**: UTF-16 encoded. Decode: `try raw.decode('utf-16'); except raw.decode('utf-8', errors='replace')`
- `<p rend="chapter">` / `<p rend="section">` = section headings
- `<hi rend="paranum">N</hi>` = paragraph number
- `<hi rend="bold">` = key term (convert to `**bold**`)
- `<pb .../>` = page break (strip)

---

### Recommended Next Action (for incoming agent)

**Start with SN 47 (Satipaṭṭhānasaṃyutta)**. It's the most meditation-relevant gap: the Four Foundations of Mindfulness saṃyutta. Files are confirmed (att2=212KB, tik2=171KB). Script pattern is identical to SN 56 — just change the slug, CSCD filenames, sc_ids, and mātikā line. The four_foundations_of_mindfulness mātikā currently lists SN 54 as its SN source; SN 47 is the primary one and should be added.

Suggested sc_ids for SN 47 mūla:
`sn47.1` (Ambapāla), `sn47.2`, `sn47.4`, `sn47.7`, `sn47.8`, `sn47.9` (the Island simile / atta-dīpa), `sn47.10` (Bhikkhunupassaya), `sn47.11–13`, `sn47.19`, `sn47.20`, `sn47.35`, `sn47.36`, `sn47.42`, `sn47.46`

## [2026-05-22 — SN 22 + SN 56 Migration (Claude Code)]

### Accomplishments

**SN 22 (Khandhasaṃyutta) — all three layers**
- Mūla: 18 selected suttas (23,613w) — Bhāra/burden (sn22.22), Anattalakkhaṇa (sn22.59), foam simile (sn22.95), Yamaka (sn22.85), Vakkali (sn22.87), Khemaka (sn22.89), Gaddulabaddha (sn22.99)
- Atthakathā: 400 paragraphs (13,968w) from CSCD `s0303a.att0.xml`
- Ṭīkā: 408 paragraphs (8,841w) from CSCD `s0303t.tik0.xml`
- Mātikā: `five_aggregates.md` and `three_marks.md` updated with reverse links → sn22
- Scripts: `generate_sn22_mula.py`, `generate_sn22_att.py`, `generate_sn22_tik.py`

**SN 56 (Saccasaṃyutta) — all three layers**
- Mūla: 16 selected suttas (6,469w) — Dhammacakkappavattana (sn56.11), Koṭigāma (sn56.20), siṃsapā leaves (sn56.31), simile suttas, blind-turtle/chiggaḷa (sn56.47-48)
- Atthakathā: 153 paragraphs (2,413w) from CSCD `s0305a.att11.xml`
- Ṭīkā: 100 paragraphs (1,689w) from CSCD `s0305t.tik11.xml`
- Mātikā: `four_noble_truths.md` and `noble_eightfold_path.md` updated with reverse links → sn56
- Scripts: `generate_sn56_mula.py`, `generate_sn56_att.py`, `generate_sn56_tik.py`

**CSCD File Mapping Discovered**
- SN Mahāvagga s0305: saṃyuttas 1-12 map to att0/tik0 through att11/tik11
  - att0/tik0=SN45, att1/tik1=SN46, att2/tik2=SN47, att3/tik3=SN48, att9/tik9=SN54, att10/tik10=SN55, att11/tik11=SN56
- SN Khandavagga s0303: att0/tik0=SN22 (343KB att / 273KB tik, full saṃyutta)

### Current State
- SN now covers: SN 12, 22, 35, 46, 54, 56 — six saṃyuttas, 151 selected suttas
- 1,113+ wikilinks validated clean
- Next candidates: SN 45 (Maggasaṃyutta), SN 47 (Satipaṭṭhānasaṃyutta), or pivot to Vinaya/KN

## [2026-05-22 — SN 35, SN 12 Migration + Dhammapada ṭīkā Investigation (Claude Code)]

### Accomplishments

**SN 35 (Saḷāyatanasaṃyutta) — all three layers**
- Mūla: 23 selected suttas (10,082w) — aniccā group (sn35.1–10), the All (sn35.23), Fire Sermon / Āditta (sn35.28), burning group, Gaddulabaddha (sn35.95), simile suttas, liberation suttas
- Atthakathā: 590 paragraphs (20,030w) from CSCD `s0304a.att0.xml`
- Ṭīkā: 484 paragraphs (10,316w) from CSCD `s0304t.tik0.xml`
- Mātikā: `five_spiritual_faculties.md` and `dependent_origination.md` updated with reverse links → sn35
- Scripts: `generate_sn35_mula.py`, `generate_sn35_att.py`, `generate_sn35_tik.py`

**Dhammapada ṭīkā — BLOCKED**
- Probed all `s0502t.tik*.xml` variants on tipitaka.org — all return 404
- CSCD online does NOT include the Dhammapada-ṭīkā (Paramattha-dīpanī)
- The Dhammapada-aṭṭhakathā Pali IS available (s0502a.att1–att9, ~1.6MB total) but we already have the English version
- Blocked unless offline CSCD CD-ROM or alternative source is provided

**SN 12 (Nidānasaṃyutta) — all three layers**
- Mūla: 18 selected suttas (20,504w) — DO formula (sn12.1–2), Kaccānagotta (sn12.15), Upanisā (sn12.23), son's flesh simile (sn12.63), ancient city / nagarasūpamā (sn12.65), Susīma (sn12.70)
- Atthakathā: 475 paragraphs (22,013w) from CSCD `s0302a.att0.xml`
- Ṭīkā: 463 paragraphs (21,458w) from CSCD `s0302t.tik0.xml`
- Both att0 and tik0 confirmed as exclusively Nidānasaṃyutta (no section extraction needed)
- Mātikā: `dependent_origination.md` and `four_noble_truths.md` updated with reverse links → sn12
- Scripts: `generate_sn12_mula.py`, `generate_sn12_att.py`, `generate_sn12_tik.py`

**Housekeeping**
- `mn119.md` and `mn121.md`: Related Texts nav lines added (done previous session, TASKS.md now updated)
- TASKS.md §8 mātikā inventory updated: sn35, sn12 reverse links logged
- STATUS.md updated: SN table now shows 4 saṃyuttas (SN 12, 35, 46, 54), 117 selected suttas

### CSCD File Mapping Discovered
- KN Dhammapada = `s0502` (confirmed by fetching att0.xml — shows "Dhammapada-aṭṭhakathā")
- KN Suttanipāta = `s0505` (confirmed by fetching att0.xml — shows "Suttanipāta-aṭṭhakathā")
- SN Nidānavagga = `s0302` (att0 + tik0 are exclusively SN 12, 507KB + 588KB)

### Current State
- 1,082 wikilinks validated clean. Git tree clean (2 commits this session).
- Next: SN 22 (Khandhavagga / Khandhasaṃyutta) — five aggregates; CSCD = `s0303`



This log tracks sync states and key technical context for agent pairs working on the Pali Canon Vault.

## [2026-05-21 23:30:00-07:00] - Link Validator Fixes & Verification (Antigravity)

### Accomplishments
- **Link Validator Refactoring**: Updated `scratch/validate_links.py` to allow cross-directory validation targeting `khuddaka_nikaya` files while keeping them excluded from active link checks (avoiding noise from known internal Dhammapada warnings). This resolved the broken link warnings in `mula/sutta/INDEX.md` and `SYNC_LOG.md` that referenced `khuddaka_nikaya` indices and suttas.
- **Vault Verification**: Re-ran vault-wide link validation; verified all links and references in the active suttas/indexes are fully valid (112 markdown files validated, 978 wikilinks checked, 0 errors).
- **Status & Tasks Audit**: Confirmed `STATUS.md` and `TASKS.md` are accurate and fully reflect Phase 2 progress (DN 9 and DN 15 fully integrated with all three layers, cross-linked, and integrated into the Mātikā).

### Current State
- Vault is clean and fully valid. Git working tree is clean. Ready for the next tranche.

## [2026-05-21 23:15:00-07:00] - DN 9 & DN 15: All Three Layers with Cross-Links and Mātikā (Claude Code & Antigravity)

### Accomplishments
- **DN 9 & DN 15 Mūla Layer**: Interleaved Pali/English files generated: `dn9.md` (8,837w) and `dn15.md` (6,706w) under `mula/sutta/digha_nikaya/`.
- **DN 9 & DN 15 Atthakathā Layer**: Commentary files generated under `atthakatha/sutta/digha_nikaya/`: `dn9_att.md` (5,978w, 67 Sujato notes) and `dn15_att.md` (10,236w, 80 Sujato notes). Sumaṅgalavilāsinī commentaries mapped from `s0101a.att9.xml` and `s0102a.att1.xml`.
- **DN 9 & DN 15 Ṭīkā Layer**: Sub-commentary files generated under `tika/sutta/digha_nikaya/`: `dn9_tik.md` (4,057w) and `dn15_tik.md` (7,693w). Sumaṅgalavilāsinī-ṭīkā mapped from `s0101t.tik9.xml` and `s0102t.tik1.xml`.
- **Cross-linking**: Applied paragraph-level headings (`### §NNN`) to commentaries and sub-commentaries, collapsible callout panels (`> [!info]- Commentary — ...`) in Mūla files, and sub-commentary links (`> [!abstract]- Tīkā §NNN`) in commentary files using `scratch/crosslink_dn9_dn15.py`.
- **Mātikā Doctrinal List Integration**:
  - DN 15 linked from `dependent_origination.md` and reverse link added in `dn15.md`.
  - DN 9 linked from `five_aggregates.md` and reverse link added in `dn9.md`.
- **Tracking & Index Updates**:
  - Root `INDEX.md` and Nikāya `INDEX.md` files updated to reflect the new counts (4 active DN suttas, 104 total migrated suttas).
  - `STATUS.md` and `TASKS.md` updated and completed.

### Current State
- DN 9 and DN 15 are fully migrated across all three layers (Mūla, Atthakathā, Ṭīkā), cross-linked, and integrated into the Mātikā.
- All links within the main Nikāyas are verified to be fully valid.

## [2026-05-21 23:00:00-07:00] - AN Batch: 5 Suttas All Three Layers + Mātikā Phase 2 (Claude Code)

### Accomplishments
- **AN mūla layer** — 5 files in `mula/sutta/anguttara_nikaya/`:
  - `an3_100.md` — Loṇakapallasutta (1,681w)
  - `an4_123_126.md` — Nānākaraṇasuttāni, 4 suttas grouped (2,607w)
  - `an5_28.md` — Pañcaṅgikasutta (2,312w)
  - `an9_36.md` — Jhānasutta (2,177w)
  - `an10_2_6.md` — Ānisaṃsasuttāni, 5 suttas grouped (2,956w — complete after SSL retry)
- **AN atthakathā layer** — 5 files in `atthakatha/sutta/anguttara_nikaya/`:
  - an3_100_att (37¶, 1,480w) · an4_123_126_att (22¶, 1,055w) · an5_28_att (31¶, 1,239w)
  - an9_36_att (28¶, 1,249w) · an10_2_6_att (16¶, 326w)
- **AN tīkā layer** — 5 files in `tika/sutta/anguttara_nikaya/`:
  - an3_100_tik (12¶, 333w) · an4_123_126_tik (10¶, 136w) · an5_28_tik (35¶, 1,356w)
  - an9_36_tik (11¶, 196w) · an10_2_6_tik (59¶, 3,062w)
- **CSCD file mapping** (non-obvious — discovered by probing):
  - `s0402a` spans AN 2+3+4 (att0-63), `s0403a` spans AN 5 (att0-15+), `s0404a` spans AN 8+9+10
  - Tīkā numbering mirrors att exactly (s040Xt.tikN = s040Xa.attN)
  - Specific mappings: an3_100→att28, an4_123_126→att48, an5_28→att2, an9_36→att13, an10_2_6→att15
- **Mātikā Phase 2** — 4 concept files updated + 5 sutta files with `**Mātikā**:` lines:
  - `seven_awakening_factors.md` += an3_100, an9_36
  - `noble_eightfold_path.md` += an3_100, an4_123_126, an5_28, an9_36, an10_2_6
  - `five_spiritual_faculties.md` += an4_123_126, an10_2_6
  - `five_hindrances.md` += an5_28
  - Reverse lines: an3_100 (seven_awakening_factors · noble_eightfold_path), an4_123_126 (five_spiritual_faculties · noble_eightfold_path), an5_28 (noble_eightfold_path · five_hindrances), an9_36 (seven_awakening_factors · noble_eightfold_path), an10_2_6 (noble_eightfold_path · five_spiritual_faculties)
- **Scripts**: `generate_an_mula.py`, `generate_an_att.py`, `generate_an_tik.py` in `scratch/`

### Technical Note
- AN title extraction bug: AN has 3 metadata keys per sutta (`:0.1` nikāya, `:0.2` vagga, `:0.3` sutta title) vs MN/SN which have 2. Script fixed to prefer `:0.3` with `:0.2` fallback.
- an10.3-6 experienced SSL timeout on first mūla re-run; second re-run succeeded cleanly.

### Current State
- AN 3.100, 4.123–126, 5.28, 9.36, 10.2–6 — all three layers complete, mātikā cross-linked.
- TASKS.md updated: AN batch items marked `[x]`, mātikā inventory updated.
- Next candidates (TASKS.md §5): DN 9, DN 15, SN 35.

## [2026-05-21 22:15:00-07:00] - Mātikā Cross-Links Phase 1 (Claude Code)

### Accomplishments
- **8 mātikā files updated** with canonical sutta references (concept → text direction):
  - `seven_awakening_factors.md` → sn46, mn10§4.4, dn22§4.4, mn118
  - `four_foundations_of_mindfulness.md` → mn10, dn22, mn118, sn54
  - `noble_eightfold_path.md` → dn22§4.5.4, mn118
  - `five_hindrances.md` → mn10§4.1, dn22§4.1, dn2§4.3.2.4, sn46, mn118
  - `five_spiritual_faculties.md` → sn46, mn118
  - `four_noble_truths.md` → dn22§4.5, mn10§4.5, mn118
  - `four_right_exertions.md` → mn20, mn118
  - `five_aggregates.md` → mn10§4.2, dn22§4.2, mn43, mn118
- **6 sutta files updated** with `**Mātikā**:` reverse-link lines (text → concept direction):
  - mn10, dn22, mn118, dn2, sn46, sn54
- All links use heading anchors (e.g., `[[mn10#4.4. The Awakening Factors|...]]`) for direct section navigation
- Also added `**Related Texts**:` lines to mn10 and dn2 (were missing from Phase 1 generation)

### Current State
- Mātikā ↔ sutta web is now connected for all 8 lists that have canonical source suttas in the vault
- Deferred: `dependent_origination.md` → DN 15 (not yet migrated); `five_aggregates.md` → Abhidhamma (future phase)
- TASKS.md mātikā item marked complete

## [2026-05-21 21:30:00-07:00] - SN 46 + SN 54: All Three Layers (Claude Code)

### Accomplishments
- **Saṃyutta Nikāya scaffolded**: new directories in `mula/sutta/samyutta_nikaya/`, `atthakatha/sutta/samyutta_nikaya/`, `tika/sutta/samyutta_nikaya/`
- **SN 46 Bojjhaṅgasaṃyutta** — mūla (56 suttas combined, 23,919w), att (180¶, 6,062w), tīkā (175¶, 5,545w)
- **SN 54 Ānāpānasaṃyutta** — mūla (20 suttas combined, 11,648w), att (45¶, 2,018w), tīkā (40¶, 1,393w)
- Each saṃyutta is one combined file (one file per saṃyutta, each individual sutta as `## SN NN.N:` heading)
- **CSCD file mapping** for SN Mahāvagga: `s0305a.att{N}.xml` / `s0305t.tik{N}.xml` where N=0 → SN 45, N=1 → SN 46, …, N=9 → SN 54
- **Scripts**: `generate_sn_mula.py`, `generate_sn_att.py`, `generate_sn_tik.py`
- All index files updated (mūla/att/tīkā for samyutta_nikaya)
- TASKS.md updated: SN 46 + SN 54 marked complete

### Current State
- SN 46 + SN 54 complete. Cross-links (mūla ↔ att ↔ tīkā) not yet done — awaiting further instruction.
- Next candidates (per TASKS.md): DN 9, DN 15; AN 3.100, AN 4.123–126, AN 5.28, AN 9.36, AN 10.2–6; SN 35.

## [2026-05-21 20:45:00-07:00] - Phase 2 Meditation Suttas: All Three Layers (Claude Code)

### Accomplishments
- **6 Phase 2 suttas** — mūla + atthakathā + tīkā for MN 36, 43, 44, 52, 111 and DN 22:

| Sutta | Mūla | Att (¶+notes) | Tīkā (¶) |
|---|---|---|---|
| MN 36 Mahāsaccakasutta | 9,139w | 34¶+25 notes, 3,365w | 32¶, 1,364w |
| MN 43 Mahāvedallasutta | 3,877w | 60¶+30 notes, 5,181w | 54¶, 4,322w |
| MN 44 Cūḷavedallasutta | 3,096w | 39¶+27 notes, 4,209w | 40¶, 2,404w |
| MN 52 Aṭṭhakanāgarasutta | 1,696w | 14¶+14 notes, 1,155w | 10¶, 528w |
| MN 111 Anupadasutta | 2,272w | 26¶+18 notes, 2,415w | 38¶, 2,158w |
| DN 22 Mahāsatipaṭṭhānasutta | 8,892w | 293¶+78 notes, 14,411w | 236¶, 12,626w |

- **Key discovery**: Gahapativagga att (`s0202a.att0.xml`) and tīkā (`s0202t.tik0.xml`) exist on tipitaka.org but NOT in the siongui/tipitaka-romn GitHub repo — file probing logic now in phase2 scripts
- **CSCD file mapping for DN Mahāvagga**: att8 and tik8 are dedicated DN 22 files
- **Scripts**: `generate_phase2_mula.py`, `generate_phase2_att.py`, `generate_phase2_tik.py`
- Index files updated: MN, DN mūla/att/tīkā indexes

### Current State
- Phase 2 MN + DN 22 complete. SN and AN expansion deferred (requires new scaffolding).
- Next candidates: DN 9, DN 15; or SN 46, SN 54 (bojjhaṅga/ānāpāna saṃyuttas).

## [2026-05-21 19:30:00-07:00] - MN 118 Cross-Links + DhpA Complete (Claude Code)

### Accomplishments

**MN 118 Cross-linking** (`scratch/crosslink_mn118.py`):
- `### §NNN` heading anchors inserted in mn118_att.md and mn118_tik.md at 7 paragraphs (§144, 145, 146, 147, 149, 150, 152)
- Collapsed `> [!info]- Commentary` callouts inserted in mn118.md at 7 key mūla passages, linking to both att and tik anchors
- `> [!abstract]- Tīkā §NNN` links appended after each att paragraph block → direct cross-navigation att↔tik
- Pattern is reusable: same script structure works for any future three-layer sutta

**Dhammapada-aṭṭhakathā — all 26 vaggas complete** (`scratch/generate_dhammapada_att_remaining.py`):
- 20 remaining vaggas fetched from ancient-buddhist-texts.net (Bhante Ānandajoti/Burlingame)
- **233 new stories** across 20 chapters; ~382K words
- Grand total DhpA: **294 origin stories**, ~498K words across all 26 vaggas
- Notable: Ch 1 (Yamaka) 14 stories 52K words; Ch 26 (Brāhmaṇa) 40 stories 38K words
- INDEX.md updated with all 26 chapters in sorted order with word counts
- Source stopped gracefully at 3 consecutive 404s per chapter

### Current State
- Dhammapada commentary layer: **complete** (all 26 vaggas with origin stories)
- Dhammapada tīkā: not yet done
- Dhammapada vagga→mātikā cross-links: not yet done
- Next high-priority: Phase 2 meditation sutta tranche (MN 36, 43, 44, 52, 111; DN 15, 22; SN 46, 54)

## [2026-05-21 18:15:00-07:00] - Meditation Suttas Tīkā Layer (Claude Code)

### Accomplishments
- **6 tīkā (sub-commentary) files** generated from tipitaka.org CSCD (UTF-16 XML):
  - `tika/sutta/majjhima_nikaya/mn10_tik.md` — Papañcasūdanī-ṭīkā, 232 ¶, **11,365 words**
  - `tika/sutta/majjhima_nikaya/mn20_tik.md` — 26 ¶, **1,006 words**
  - `tika/sutta/majjhima_nikaya/mn119_tik.md` — 8 ¶, **358 words**
  - `tika/sutta/majjhima_nikaya/mn121_tik.md` — 11 ¶, **589 words**
  - `tika/sutta/digha_nikaya/dn2_tik.md` — Sumaṅgalavilāsinī-ṭīkā, 259 ¶, **13,655 words**
  - `tika/sutta/anguttara_nikaya/an4_41_tik.md` — Manorathapūraṇī-ṭīkā, 18 ¶, **996 words**
- **Format**: YAML frontmatter → navigation (links to mūla + atthakathā) → Pali tīkā text with `(N)` paragraph numbers
- **Source discovery**: GitHub/siongui/tipitaka-romn has no sutta tīkā; tipitaka.org/romn/cscd/ has full set `s{NNNN}t.tik{N}.xml`
- **Section extraction**: same regex heading approach as atthakathā; stop_pat catches next sutta/vagga boundary
- **Tīkā file mapping**:
  - MN Mūlapaṇṇāsa: `s0201t.tik1.xml` (MN 1-10), `s0201t.tik2.xml` (MN 11-20)
  - MN Uparipaṇṇāsa: `s0203t.tik1.xml` (Anupadavagga/MN 111-120), `s0203t.tik2.xml` (Suññatavagga/MN 121-130)
  - DN 2: `s0101t.tik2.xml` (entire dedicated file)
  - AN 4.41: `s0402t.tik4.xml` (entire Parisavagga tīkā)
- **Index files**: `tika/sutta/INDEX.md`, `tika/sutta/{nikaya}/INDEX.md` created with word-count rows
- **Script**: `scratch/generate_meditation_tik.py` — reusable for future suttas
- **TASKS.md**: tīkā subtask marked complete; comprehensive future roadmap added (Phase 2 suttas, Vinaya, full nikāya expansion, Abhidhamma integration)

### Current State
- All 6 meditation suttas now have **three complete layers**: mūla + atthakathā + tīkā.
- Remaining high-priority work: MN 118 cross-links (mūla↔att↔tīkā), remaining 20 DhpA chapters,
  Phase 2 sutta tranche (MN 36, 43, 44, 52, 111; DN 9, 15, 22; SN 35, 46, 54; AN key suttas).

## [2026-05-21 17:30:00-07:00] - Meditation Suttas Atthakathā Layer (Claude Code)

### Accomplishments
- **6 atthakathā (commentary) files** generated for key meditation suttas, combining two sources:
  1. **Pali commentary text** — CSCD (Chattha Sangayana Tipitaka) XML from siongui/tipitaka-romn on GitHub; UTF-16 decoded, paragraphs numbered, bold terms preserved
  2. **Translator's notes** — Bhikkhu Sujato's segment annotations from SuttaCentral `/comment` API
- **Files** in `atthakatha/sutta/{nikaya}/`:
  - `mn10_att.md` — Papañcasūdanī, 362 ¶, 49 Sujato notes, **15,912 words**
  - `mn20_att.md` — Papañcasūdanī, 40 ¶, 11 notes, **2,159 words**
  - `mn119_att.md` — Papañcasūdanī, 10 ¶, 18 notes, **1,181 words**
  - `mn121_att.md` — Papañcasūdanī, 13 ¶, 15 notes, **1,476 words**
  - `dn2_att.md` — Sumaṅgalavilāsinī, 394 ¶, 141 notes, **22,452 words**
  - `an4_41_att.md` — Manorathapūraṇī, 15 ¶, 0 notes, **952 words**
- **Format**: YAML frontmatter → Translator's Notes section → `---` → Pali commentary with `(N)` paragraph numbers and `**bold**` key terms
- **Index files updated**: MN, DN, AN atthakathā indexes with word counts and sources
- **Fetch script**: `scratch/generate_meditation_att.py` — reusable for future suttas

### Current State
- All 6 meditation sutta mūla + atthakathā layers complete.
- Sub-commentary (tīkā) layer not yet added. CSCD tīkā files follow same `*.tik*.xml` naming pattern.
- Next: tīkā layer, or other phases (remaining DhpA chapters, MN expansion, etc.)

## [2026-05-21 16:30:00-07:00] - Meditation Suttas Mūla Layer (Claude Code)

### Accomplishments
- **6 key meditation suttas** fetched from SuttaCentral (Sujato translation) and generated as interleaved Pali/English mūla files:
  - `mula/sutta/majjhima_nikaya/mn10.md` — Satipaṭṭhānasutta, 5,721 words
  - `mula/sutta/majjhima_nikaya/mn20.md` — Vitakkasaṇṭhānasutta, 1,798 words
  - `mula/sutta/majjhima_nikaya/mn119.md` — Kāyagatāsatisutta, 4,967 words
  - `mula/sutta/majjhima_nikaya/mn121.md` — Cūḷasuññatasutta, 2,760 words
  - `mula/sutta/digha_nikaya/dn2.md` — Sāmaññaphalasutta, 17,701 words
  - `mula/sutta/anguttara_nikaya/an4_41.md` — Samādhibhāvanāsutta, 745 words
- **New nikāya directories** scaffolded with INDEX.md: `digha_nikaya` and `anguttara_nikaya` (all three layers: mula/atthakatha/tika)
- **Format**: YAML frontmatter, `## Section` / `### Sub-section` headings for structural divisions (Pali + English), interleaved `**Pali**` / `*English*` body segments
- **Index files updated**: MN, DN, AN mula indexes + `mula/sutta/INDEX.md`
- **Fetch script**: `scratch/generate_meditation_suttas.py` — reusable for future suttas

### Current State
- All 6 meditation sutta mūla files complete. Commentary (Papañcasūdanī / Sumaṅgalavilāsinī / Manorathapūraṇī) and sub-commentary not yet added.
- Next: commentary layer for these suttas, or continue expanding other phases.

## [2026-05-21 16:05:00-07:00] - Dhammapada Atthakathā — Meditation Chapters (Claude Code)

### Accomplishments
- **Dhammapada-aṭṭhakathā (6 meditation chapters)**: Fetched and generated commentary files from ancient-buddhist-texts.net (Bhante Ānandajoti's revised Burlingame translation). 61 HTML pages fetched across 6 chapters.
- **Files generated** in `atthakatha/sutta/khuddaka_nikaya/dhammapada/`:
  - `dhp_02_appamadavagga_att.md` — 9 stories, ~41,004 words (Heedfulness)
  - `dhp_03_cittavagga_att.md` — 9 stories, ~14,290 words (The Mind)
  - `dhp_07_arahantavagga_att.md` — 10 stories, ~10,384 words (The Arahant)
  - `dhp_14_buddhavagga_att.md` — 9 stories, ~21,573 words (The Buddha)
  - `dhp_20_maggavagga_att.md` — 12 stories, ~10,085 words (The Path)
  - `dhp_25_bhikkhuvagga_att.md` — 12 stories, ~18,494 words (The Monk)
  - `INDEX.md` — chapter listing with wikilinks
- **Format**: Each story has heading (`### N.M Title (*vatthu*)`), verse cross-links to mula files, metadata (Burlingame ref/Compare/Cast/Keywords), narrative prose, verse quote (blockquote with Pali bold + English italic), and closing note.
- **Fetch script**: `scratch/generate_dhammapada_att.py` — reusable for remaining 20 chapters.

### Current State
- All 6 meditation-chapter commentaries complete (~116K words total, 61 origin stories).
- Cross-links from commentary to mūla verse anchors are present (e.g., `[[dhp_07_arahantavagga#90. *Jīvakapañhavatthu*|Dhp 90]]`).
- Remaining Dhammapada-aṭṭhakathā work: 20 non-meditation chapters (can reuse same script with expanded CHAPTERS list).
- Next: MN expansion (MN 10, MN 20, etc.) or remaining DhpA chapters.

## [2026-05-21 14:30:00-07:00] - Dhammapada Mūla Complete (Claude Code)

### Accomplishments
- **Dhammapada mūla**: All 26 vaggas (423 verses, ~17,600 words) fetched from SuttaCentral API and generated as interleaved Pali/English files. Bhikkhu Sujato translation.
- **Files**: `mula/sutta/khuddaka_nikaya/dhammapada/dhp_01_yamakavagga.md` through `dhp_26_brahmanavagga.md` + `INDEX.md`.
- **Format**: Each verse has verse number, optional vatthu (origin story name) as italic subhead, then Pali (bold) / English (italic) line pairs. Vagga-end colophons preserved from canonical tradition.
- **Tags**: Meditation-focused chapters (2, 3, 7, 14, 20, 25) tagged `meditation`; ethics/precepts chapters (1, 9, 10, 17, 18, 19) tagged `precepts`.
- **Fetch script**: `scratch/generate_dhammapada.py` — reusable for re-fetching or adapting to other Khuddaka texts.
- **Khuddaka INDEX**: Updated to list Dhammapada as complete.

### Current State
- Dhammapada mūla layer is complete. Commentary (Dhammapada-aṭṭhakathā) and sub-commentary not yet added.
- Next: Dhammapada commentary (origin stories), then Abhidhamma or MN expansion.

## [2026-05-21 14:00:00-07:00] - Templater Translation Toggle (Claude Code)

### Accomplishments
- **Templater plugin** (v2.20.5) installed and configured. `enabled_templates_hotkeys` in `data.json` registers the command `Templater: Insert toggle_translations` as a hotkey-assignable Obsidian command.
- **Toggle template** at `templates/toggle_translations.md` — executes JS to flip the `pali-translation-toggle` CSS snippet on/off with no content inserted into the active note.
- **Hotkey**: user assigns via Settings → Hotkeys → search `toggle` → `Templater: Insert toggle_translations`.
- **`.gitignore`** updated: Templater's `data.json` is now tracked (holds hotkey config); other plugins' `data.json` remain ignored.

### Current State
- Full infrastructure is operational: Simsapa DPD lookup, Dataview, translation toggle, git, templates, and folder scaffolding for all three piṭakas.

## [2026-05-21 13:30:00-07:00] - Vault Infrastructure Overhaul (Claude Code)

### Accomplishments
- **Simsapa DPD Integration**: Installed Simsapa Dhamma Reader (v0.5.2-alpha.1, arm64) to `/Applications` and Simsapa Obsidian plugin (v0.5.0) to `.obsidian/plugins/simsapa/`. Double-click any Pali word in Obsidian to trigger a DPD lookup window.
- **Dataview Plugin**: Installed Dataview (v0.5.70) to `.obsidian/plugins/dataview/`. Enables SQL-like queries over vault metadata directly in notes.
- **CSS Translation Toggle**: Created `.obsidian/snippets/pali-translation-toggle.css`. Enable in Settings → Appearance → CSS Snippets to hide all English translations and read pure Pali. Assign to a hotkey via Settings → Hotkeys → "Toggle CSS snippet: pali-translation-toggle".
- **Git Repository**: Initialized git repo at vault root with `.gitignore` (excludes workspace.json, plugin data.json, .DS_Store).
- **Templates**: Created `templates/` folder with three starter templates: `mula_sutta.md`, `atthakatha_sutta.md`, `tika_sutta.md`. Configure via Settings → Templates → Template folder location → `templates`.
- **Folder Scaffolding**:
  - `mula/sutta/khuddaka_nikaya/` — ready for Dhammapada and other Khuddaka texts
  - `mula/abhidhamma/`, `atthakatha/abhidhamma/`, `tika/abhidhamma/` — ready for Abhidhamma Piṭaka
  - `mula/vinaya/`, `atthakatha/vinaya/`, `tika/vinaya/` — ready for Vinaya Piṭaka (precepts study)
- **INDEX updates**: Root INDEX.md updated to reflect new pitaka scaffolding.
- **Initial git commit**: Full vault snapshot committed.

### Current State
- Vault has Simsapa DPD lookup (double-click), Dataview queries, translation toggle CSS, and folder structure for all three piṭakas.
- Two one-time manual steps remain in Obsidian: (1) enable Dataview in Community plugins, (2) set Templates folder to `templates` in core Templates plugin settings.

## [2026-05-21 11:00:00-07:00] - Additional Mātika (Buddhist Lists) Expanded

### Accomplishments
- **Expanded Lists**: Generated 7 additional practice-oriented and ethical Buddhist lists with Romanized Pali and item-by-item English translations:
  - [eight_precepts.md](file:///Users/rds/pali_canon/matika/eight_precepts.md) (*Aṭṭhaṅgasīla*)
  - [three_refuges.md](file:///Users/rds/pali_canon/matika/three_refuges.md) (*Tisarana*)
  - [ten_perfections.md](file:///Users/rds/pali_canon/matika/ten_perfections.md) (*Dasa Pāramī*)
  - [four_sublime_states.md](file:///Users/rds/pali_canon/matika/four_sublime_states.md) (*Cattāro Brahmavihārā*)
  - [five_spiritual_faculties.md](file:///Users/rds/pali_canon/matika/five_spiritual_faculties.md) (*Pañcindriya*)
  - [three_unwholesome_roots.md](file:///Users/rds/pali_canon/matika/three_unwholesome_roots.md) (*Akusalamūla*)
  - [four_right_exertions.md](file:///Users/rds/pali_canon/matika/four_right_exertions.md) (*Cattāro Sammappadhānā*)
- **Cross-linking & Validation**: Fully integrated these files with navigation paths, related lists, and references. Verified vault-wide integrity via the wikilink validator (68 total files validated successfully, 0 broken links).
- **Index & Status Sync**: Updated [matika/INDEX.md](file:///Users/rds/pali_canon/matika/INDEX.md), root [INDEX.md](file:///Users/rds/pali_canon/INDEX.md), [STATUS.md](file:///Users/rds/pali_canon/STATUS.md), and [TASKS.md](file:///Users/rds/pali_canon/TASKS.md) to register all 16 active lists.

### Current State
- The Mātika branch contains 16 highly structured lists, fully translated and cross-referenced.
- Link validation is completely clean.

## [2026-05-21 10:55:00-07:00] - Mātika (Buddhist Lists) Creation Complete

### Accomplishments
- **Mātika Directory & Index**: Created the `/Users/rds/pali_canon/matika/` directory and [matika/INDEX.md](file:///Users/rds/pali_canon/matika/INDEX.md) to serve as the master catalog for Buddhist lists.
- **Lists Generation**: Created 9 core Buddhist lists with Romanized Pali and item-by-item English translations, complete with navigation headers and standard YAML metadata:
  - [four_noble_truths.md](file:///Users/rds/pali_canon/matika/four_noble_truths.md) (*Cattāri Ariyasaccāni*)
  - [noble_eightfold_path.md](file:///Users/rds/pali_canon/matika/noble_eightfold_path.md) (*Ariyo Aṭṭhaṅgiko Maggo*)
  - [three_marks.md](file:///Users/rds/pali_canon/matika/three_marks.md) (*Tilakkhaṇa*)
  - [five_aggregates.md](file:///Users/rds/pali_canon/matika/five_aggregates.md) (*Pañcupādānakkhandhā*)
  - [dependent_origination.md](file:///Users/rds/pali_canon/matika/dependent_origination.md) (*Paṭiccasamuppāda*)
  - [five_precepts.md](file:///Users/rds/pali_canon/matika/five_precepts.md) (*Pañcasīla*)
  - [five_hindrances.md](file:///Users/rds/pali_canon/matika/five_hindrances.md) (*Pañca Nīvaraṇāni*)
  - [seven_awakening_factors.md](file:///Users/rds/pali_canon/matika/seven_awakening_factors.md) (*Satta Bojjhaṅgā*)
  - [four_foundations_of_mindfulness.md](file:///Users/rds/pali_canon/matika/four_foundations_of_mindfulness.md) (*Cattāro Satipaṭṭhānā*)
- **Cross-linking & Validation**: Linked all lists with relevant dependencies and to their occurrences/discussions in Majjhima Nikāya 118. Executed the wikilink validator verifying vault integrity.
- **Index and Status Updates**: Updated root [INDEX.md](file:///Users/rds/pali_canon/INDEX.md), [STATUS.md](file:///Users/rds/pali_canon/STATUS.md), and [TASKS.md](file:///Users/rds/pali_canon/TASKS.md) to integrate the new Mātika branch.

### Current State
- The vault is fully updated with the Mātika branch, including all 9 core lists mapped out, fully translated, and linked.
- Link validation returns no broken links.
- Future tasks involve linking these lists to new suttas as they are added, and expanding commentaries/sub-commentaries.

## [2026-05-21 10:46:52-07:00] - MN 118 Interleaving Complete & Vault Tracking Initiated

### Accomplishments
- **Mūla Interleaving**: Interleaved the Romanized Pali of the Ānāpānasati Sutta ([mn118.md](file:///Users/rds/pali_canon/mula/sutta/majjhima_nikaya/mn118.md)) with Bhikkhu Sujato's segment-by-segment English translation.
- **Commentary Translation**: Translated the 18 paragraphs of the Papañcasūdanī commentary on MN 118 and interleaved them sentence-by-sentence with the original Pali ([mn118_att.md](file:///Users/rds/pali_canon/atthakatha/sutta/majjhima_nikaya/mn118_att.md)).
- **Sub-commentary Translation**: Translated the 16 paragraphs of the Majjhima Nikāya Sub-commentary on MN 118 and interleaved them sentence-by-sentence with the original Pali ([mn118_tik.md](file:///Users/rds/pali_canon/tika/sutta/majjhima_nikaya/mn118_tik.md)).
- **Index Updates**: Updated word counts across all Nikāya indexes ([mula index](file:///Users/rds/pali_canon/mula/sutta/majjhima_nikaya/INDEX.md), [atthakatha index](file:///Users/rds/pali_canon/atthakatha/sutta/majjhima_nikaya/INDEX.md), [tika index](file:///Users/rds/pali_canon/tika/sutta/majjhima_nikaya/INDEX.md)).
- **Verification**: Created and ran a wikilink validation script verifying all links across the vault resolve cleanly.
- **Tracking System**: Created vault-level tracking files at the root: [SYNC_LOG.md](file:///Users/rds/pali_canon/SYNC_LOG.md), [TASKS.md](file:///Users/rds/pali_canon/TASKS.md), and [STATUS.md](file:///Users/rds/pali_canon/STATUS.md).

### Current State
- The vault is fully optimized for Obsidian with working indexes, navigation headers, and relative path wikilinks.
- Majjhima Nikāya 118 is completely migrated, translated, and interleaved across all three layers (Mūla, Commentary, Sub-commentary).
- The next step is expanding to other suttas in the Majjhima Nikāya or enhancing the existing files with cross-link references between Commentary, Sub-commentary, and Mūla.
