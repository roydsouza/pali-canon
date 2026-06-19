🏠 [[INDEX|Dashboard]]

# FROM-CLAUDE: Errors, Omissions & Improvements
[[INDEX|Dashboard]] > [[topics/topics|Topics Hub]] > [[topics/texts/texts|Texts & Canon]] > [[topics/texts/pali-canon/pali-canon|Pāḷi Canon]] > FROM-CLAUDE: Errors, Omissions & Improvements

*Quality-review notes from Claude Sonnet 4.6, 2026-05-22.*
*Covers the AntiGravity session ending with commit 9071cdd.*

---

## Bugs Fixed This Session

### 1. MN 19 missing mātikā navigation line
**File**: `mula/sutta/majjhima_nikaya/mn19.md`  
STATUS.md claimed "Full §-anchors & Mātikā" but the sutta had no `**Mātikā**: ...` line. The reverse links existed in mātikā files (five_hindrances, three_unwholesome_roots referenced mn19) but the forward link from the sutta was absent.  
**Fixed**: Added `**Mātikā**: [[noble_eightfold_path|...]] · [[five_hindrances|...]] · [[three_unwholesome_roots|...]]`

### 2. SN 55 incomplete forward mātikā links
**File**: `mula/sutta/samyutta_nikaya/sn55.md`  
The mātikā line only had `three_refuges · ten_fetters`, but the matika files for `five_precepts` and `five_spiritual_faculties` both had reverse links pointing to sn55. Bidirectionality was broken.  
**Fixed**: Added five_precepts and five_spiritual_faculties to sn55 mātikā line.

### 3. STATUS.md table formatting bug
**File**: `STATUS.md` line 8  
The table separator row was `|---|---|---|---||` (double pipe) — the closing `|` and the first data column ran together. This broke Markdown table rendering.  
**Fixed**: Corrected to `|---|---|---|---|` with a proper newline before the first data row.

### 4. STATUS.md mātikā count inconsistency (18 vs 19)
**File**: `STATUS.md`  
The metrics table said "19 lists" but the narrative section still said "18 lists total." Three new mātikā files (ten_fetters, seven_purifications, five_powers) had been added but the narrative wasn't updated.  
**Fixed**: Changed "18 lists total" to "19 lists total."

### 5. TASKS.md DN expansion not recorded
**File**: `TASKS.md`  
DN 1, DN 16, and DN 21 were fully complete with all three layers (mūla + att + tīkā), including §-anchor callouts — but all three were still marked `[ ]` pending in TASKS.md, and weren't listed in the Completed Work section. STATUS.md also had no catalog entries for them.  
**Fixed**: Added Phase 5 section to Completed Work, marked all three `[x]` in pending section, added rows to STATUS.md DN table.

### 6. Snp scope mismatch
**File**: `TASKS.md`  
The Sutta Nipāta entries said "Snp 1.3 & 1.8 — 2 suttas" but AntiGravity actually completed all 12 suttas of the Uragavagga (snp1.1–snp1.12) with both mūla and atthakathā layers.  
**Fixed**: Updated TASKS.md entries to reflect the actual completed scope.

---

## Ongoing Issues to Watch

### A. AntiGravity does not commit after each sutta
When the review started, 79 files were uncommitted. This is a recurring pattern — large batches of work exist only in the working tree until a session ends (or doesn't). If a crash or accidental `git clean` happens, all that work is lost.

**Recommendation for future agent sessions**: Commit after each sutta (all three layers) or at absolute minimum after each nikāya batch. The commit message structure is already established and takes seconds.

### B. scratch/ folder accumulation
AntiGravity created ~50 new scripts in `scratch/` during its session: `inspect_*.py`, `test_*.py`, plus the useful `generate_*.py` and `crosslink_*.py` scripts. Only the generate/crosslink scripts are worth preserving. The inspect and test scripts were scaffolding.

As the repo grows, this folder will become hard to navigate. **Suggested action** (when convenient, not urgent): move generation scripts to `scratch/generators/` and either delete or archive the one-off inspection scripts.

### C. STATUS.md script count is stale
The Infrastructure section says "17 reusable Python scripts in `scratch/`" — there are now ~50+. Not critical but will continue to drift.

### D. Sutta Nipāta pending entry needs updating
`TASKS.md` pending section still shows:
```
[ ] Sutta Nipāta — snp1.1–snp5.19 (Uragavagga/Chapter 1 complete: 12 suttas)
```
This correctly notes Uragavagga is done, but the item could be more precise about what remains: Chapters 2 (Cūḷavagga), 3 (Mahāvagga), 4 (Aṭṭhakavagga), 5 (Pārāyanavagga). See VISION.md for recommended priority.

### E. DN 1, 16, 21 have no mātikā links
The three new DN suttas (Brahmajāla, Mahāparinibbāna, Sakkapañha) were migrated without mātikā cross-links. This is defensible given their size and complexity, but:
- DN 16 touches on: four_foundations_of_mindfulness, seven_awakening_factors, noble_eightfold_path, dependent_origination
- DN 1 touches on: three_marks, dependent_origination (the 62 views are all ego-views)
- DN 21 touches on: four_sublime_states, noble_eightfold_path

A future pass adding these links would significantly improve discoverability.

---

## Quality Observations (No Action Required)

- **§-anchor callout density is consistent** across all AntiGravity's work. MN 19 has 6 callouts for a 6-paragraph sutta; SN 48 has 6 suttas with full anchors. The pattern is maintained.
- **Dhammapada att link fixes are correct**. The Dhammapada commentary frequently references verses from other vaggas (e.g., a story in Chapter 1 might be triggered by a verse from Chapter 23). AntiGravity correctly identified ~10 cross-vagga verse link errors and fixed them. These were genuine bugs — the original links pointed to the wrong vagga file.
- **New mātikā files (ten_fetters, seven_purifications, five_powers) are substantive**. Each has a canonical list, doctrinal explanation, and multiple canonical references with commentary on why they connect. The five_powers file correctly explains its relationship to five_spiritual_faculties (same factors, different context).
- **Udāna mūla word count matches STATUS.md** (46,198w confirmed). The atthakathā (70,642w) is significantly larger than the mūla — expected for Udāna, whose commentary is disproportionately rich in narrative.
- **Link validator passes cleanly** after all fixes: 238 files, 3,098 wikilinks, 0 errors.
