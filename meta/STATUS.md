# Pali Canon Vault Status

This document captures the current status of the Pali Canon Obsidian Vault migration, cataloging what has been completed, what is in progress, and overall progress metrics.

## Overall Progress Metrics

*Last updated: 2026-06-04*

| Layer | Files | Nikāyas Active | Notes |
|---|---|---|---|
| **Mūla (Root Texts)** | `$= dv.pages().where(p => p.type == "mula").length` files | MN, DN, SN, AN, KN | Interleaved Pali/English (Sujato) |
| **Aṭṭhakathā (Commentaries)** | `$= dv.pages().where(p => p.type == "atthakatha").length` files | MN, DN, SN, AN, KN | CSCD Pali + Sujato notes |
| **Ṭīkā (Sub-commentaries)** | `$= dv.pages().where(p => p.type == "tika").length` files | MN, DN, SN, AN | CSCD Pali (Udāna, Snp, Iti have no Ṭīkā) |
| **Mātikā (Doctrinal Lists)** | `$= dv.pages().where(p => p.type == "matika").length` files | — | Pali/English, cross-linked |
| **Paths (Reading Sequences)** | `$= dv.pages().where(p => p.type == "path").length` files | — | 7 practice-domain paths + 3 question-driven paths |
| **Scripts** | 142 Python scripts | — | 56 generators, 13 crosslinkers, 50 inspectors, 10 tests, 2 refactors, 1 lib, 10 new (2026-06-04) |

---

## Migrated Texts Catalog

### Majjhima Nikāya (Middle Discourses) — 22 suttas

| Sutta | Mūla | Att | Tīkā | Cross-links |
|---|---|---|---|---|
| MN 2 Sabbāsavasutta | ✅ 3,522w | ✅ 137¶ | ✅ 120¶ | ✅ Full §-anchors & Mātikā |
| MN 7 Vatthūpamasutta | ✅ 2,456w | ✅ 52¶ | ✅ 34¶ | ✅ Full §-anchors & Mātikā |
| MN 8 Sallekhasutta | ✅ 2,860w | ✅ 46¶ | ✅ 32¶ | ✅ Full §-anchors & Mātikā |
| MN 10 Satipaṭṭhānasutta | ✅ 5,721w | ✅ 362¶ + 49 notes | ✅ 232¶ | ✅ Full §-anchors & Mātikā |
| MN 19 Dvedhāvitakkasutta | ✅ 3,032w | ✅ 6¶ | ✅ 6¶ | ✅ Full §-anchors & Mātikā |
| MN 20 Vitakkasaṇṭhānasutta | ✅ 1,798w | ✅ 40¶ + 11 notes | ✅ 26¶ | Mātikā |
| MN 22 Alagaddūpamasutta | ✅ 6,958w | ✅ 49¶ + 49 notes | ✅ 3,577w | ✅ Full §-anchors & Mātikā |
| MN 27 Cūḷahatthipadopamasutta | ✅ 4,120w | ✅ 69¶ | ✅ 62¶ | ✅ Full §-anchors & Mātikā |
| MN 28 Mahāhatthipadopamasutta | ✅ 4,890w | ✅ 40¶ | ✅ 35¶ | ✅ Full §-anchors & Mātikā |
| MN 36 Mahāsaccakasutta | ✅ 9,139w | ✅ 34¶ + 25 notes | ✅ 32¶ | Mātikā |
| MN 43 Mahāvedallasutta | ✅ 3,877w | ✅ 60¶ + 30 notes | ✅ 54¶ | Mātikā |
| MN 44 Cūḷavedallasutta | ✅ 3,096w | ✅ 39¶ + 27 notes | ✅ 40¶ | Mātikā |
| MN 51 Kandarakasutta | ✅ 3,920w | ✅ 21¶ | ✅ 18¶ | ✅ Full §-anchors & Mātikā |
| MN 52 Aṭṭhakanāgarasutta | ✅ 1,696w | ✅ 14¶ + 14 notes | ✅ 10¶ | Mātikā |
| MN 111 Anupadasutta | ✅ 2,272w | ✅ 26¶ + 18 notes | ✅ 38¶ | Mātikā |
| MN 117 Mahācattārīsakasutta | ✅ 3,126w | ✅ 22¶ + 22 notes | ✅ 1,073w | Mātikā |
| MN 118 Ānāpānasatisutta | ✅ 3,522w | ✅ 18¶ | ✅ 16¶ | ✅ Full §-anchors & Mātikā |
| MN 119 Kāyagatāsatisutta | ✅ 4,967w | ✅ 10¶ + 18 notes | ✅ 8¶ | Mātikā |
| MN 121 Cūḷsuññatasutta | ✅ 2,760w | ✅ 13¶ + 15 notes | ✅ 11¶ | Nav fixed |
| MN 128 Upakkilesasutta | ✅ 4,110w | ✅ 28¶ | ✅ 19¶ | ✅ Full §-anchors & Mātikā |
| MN 140 Dhātuvibhaṅgasutta | ✅ 3,920w | ✅ 89¶ | ✅ 46¶ | ✅ Full §-anchors & Mātikā |
| MN 148 Chachakkasutta | ✅ 3,110w | ✅ 14¶ | ✅ 13¶ | ✅ Full §-anchors & Mātikā |

### Dīgha Nikāya (Long Discourses) — 8 suttas

| Sutta | Mūla | Att | Tīkā | Cross-links |
|---|---|---|---|---|
| DN 1 Brahmajālasutta | ✅ 18,401w | ✅ att | ✅ tik | §-anchors |
| DN 2 Sāmaññaphalasutta | ✅ 17,701w | ✅ 394¶ + 141 notes | ✅ 259¶ | Mātikā |
| DN 9 Poṭṭhapādasutta | ✅ 8,837w | ✅ 57¶ + 67 notes | ✅ 72¶ | ✅ Full §-anchors & Mātikā |
| DN 13 Tevijjasutta | ✅ 4,680w | ✅ 30¶ | ✅ 40¶ | ✅ Full §-anchors & Mātikā |
| DN 15 Mahānidānasutta | ✅ 6,706w | ✅ 138¶ + 80 notes | ✅ 122¶ | ✅ Full §-anchors & Mātikā |
| DN 16 Mahāparinibbānasutta | ✅ 35,942w | ✅ att | ✅ tik | §-anchors |
| DN 21 Sakkapañhasutta | ✅ 8,213w | ✅ att | ✅ tik | §-anchors |
| DN 22 Mahāsatipaṭṭhānasutta | ✅ 8,892w | ✅ 293¶ + 78 notes | ✅ 236¶ | Mātikā |

### Saṃyutta Nikāya (Connected Discourses) — 225 suttas (11 saṃyuttas)

| Saṃyutta | Mūla | Att | Tīkā | Cross-links |
|---|---|---|---|---|
| SN 12 Nidānasaṃyutta (18 selected) | ✅ 20,504w | ✅ 475¶ (22,013w) | ✅ 463¶ (21,458w) | Mātikā |
| SN 22 Khandhasaṃyutta (18 selected) | ✅ 23,613w | ✅ 400¶ (13,968w) | ✅ 408¶ (8,841w) | Mātikā |
| SN 35 Saḷāyatanasaṃyutta (23 selected) | ✅ 10,082w | ✅ 590¶ (20,030w) | ✅ 484¶ (10,316w) | Mātikā |
| SN 36 Vedanāsaṃyutta (3 selected) | ✅ 3,840w | ✅ 9¶ | ✅ 11¶ | ✅ Full §-anchors & Mātikā |
| SN 45 Maggasaṃyutta (20 selected) | ✅ 7,202w | ✅ 124¶ (3,463w) | ✅ 126¶ (3,007w) | ✅ 4 suttas full §-anchors & Mātikā |
| SN 46 Bojjhaṅgasaṃyutta (56 suttas) | ✅ 23,919w | ✅ 180¶ | ✅ 175¶ | Mātikā |
| SN 47 Satipaṭṭhānasaṃyutta (16 selected) | ✅ 9,504w | ✅ 220¶ (9,325w) | ✅ 149¶ (6,123w) | ✅ 4 suttas full §-anchors & Mātikā |
| SN 48 Indriyasaṃyutta (20 selected) | ✅ 6,760w | ✅ 106¶ (3,037w) | ✅ 92¶ (2,544w) | ✅ 6 suttas full §-anchors & Mātikā |
| SN 51 Iddhipādasaṃyutta (3 selected) | ✅ 2,759w | ✅ 692w | ✅ 360w | ✅ 2 suttas full §-anchors & Mātikā |
| SN 54 Ānāpānasaṃyutta (20 suttas) | ✅ 11,648w | ✅ 45¶ | ✅ 40¶ | Mātikā |
| SN 55 Sotāpattisaṃyutta (15 selected) | ✅ 12,650w | ✅ 103¶ (2,613w) | ✅ 90¶ (1,810w) | ✅ 3 suttas full §-anchors & Mātikā |
| SN 56 Saccasaṃyutta (16 selected) | ✅ 6,469w | ✅ 153¶ (2,413w) | ✅ 100¶ (1,689w) | Mātikā |

### Aṅguttara Nikāya (Numerical Discourses) — 35 suttas/groups (662 suttas total)

| Sutta | Mūla | Att | Tīkā | Cross-links |
|---|---|---|---|---|
| AN 1 Ekakanipāta (627 suttas) | ✅ 31 files | ✅ 31 files | ✅ 30 files | Mātikā |
| AN 3.100 Loṇakapallasutta | ✅ 1,681w | ✅ 37¶ | ✅ 12¶ | Mātikā |
| AN 4.41 Samādhibhāvanāsutta | ✅ 745w | ✅ 15¶ | ✅ 18¶ | Mātikā |
| AN 4.67 Ahirājasutta | ✅ 1,110w | ✅ 3¶ | ✅ 3¶ | ✅ Full §-anchors & Mātikā |
| AN 4.99 Sikkhāpadasutta | ✅ 940w | ✅ 2¶ | ✅ 6¶ | ✅ Full §-anchors & Mātikā |
| AN 4.123–126 Nānākaraṇasuttāni (4) | ✅ 2,607w | ✅ 22¶ | ✅ 10¶ | Mātikā |
| AN 5.28 Pañcaṅgikasutta | ✅ 2,312w | ✅ 31¶ | ✅ 35¶ | Mātikā |
| AN 6.10 Mahānāmasutta | ✅ 1,420w | ✅ 4¶ | ✅ 4¶ | ✅ Full §-anchors & Mātikā |
| AN 6.19 Paṭhamamaraṇassatisutta | ✅ 1,120w | ✅ 2¶ | ✅ 5¶ | ✅ Full §-anchors & Mātikā |
| AN 6.20 Dutiyamaraṇassatisutta | ✅ 1,020w | ✅ 3¶ | ✅ 4¶ | ✅ Full §-anchors & Mātikā |
| AN 6.25 Anussatiṭṭhānasutta | ✅ 1,110w | ✅ 2¶ | ✅ 3¶ | ✅ Full §-anchors & Mātikā |
| AN 7.65 Hirīottappasutta | ✅ 709w | ✅ 77w | ✅ 76w | Mātikā |
| AN 8.53 Saṅkhittasutta | ✅ 410w | ✅ 776w | ✅ 457w | Mātikā |
| AN 8.54 Dīghajāṇusutta | ✅ 2,340w | ✅ 8¶ | ✅ 4¶ | ✅ Full §-anchors & Mātikā |
| AN 8.63 Saṅkhittasutta | ✅ 1,890w | ✅ 4¶ | ✅ 11¶ | ✅ Full §-anchors & Mātikā |
| AN 8.73 Paṭhamamaraṇassatisutta | ✅ 1,450w | ✅ 2¶ | ✅ 12¶ | ✅ Full §-anchors & Mātikā |
| AN 9.34 Nibbānasukhasutta | ✅ 1,620w | ✅ 2¶ | ✅ 3¶ | ✅ Full §-anchors & Mātikā |
| AN 9.35 Gāvīupamāsutta | ✅ 1,810w | ✅ 2¶ | ✅ 3¶ | ✅ Full §-anchors & Mātikā |
| AN 9.36 Jhānasutta | ✅ 2,177w | ✅ 28¶ | ✅ 11¶ | Mātikā |
| AN 10.2–6 Ānisaṃsasuttāni (5) | ✅ 2,956w | ✅ 16¶ | ✅ 59¶ | Mātikā |
| AN 10.60 Girimānandasutta | ✅ 1,931w | ✅ 1¶ | ❌ (No Ṭīkā) | ✅ Full §-anchors & Mātikā |
| AN 11.1 Kimatthiyasutta | ✅ 534w | ✅ 412w | ✅ 342w | Mātikā |
| AN 11.2 Cetanākaraṇīyasutta | ✅ 687w | ✅ 117w | ✅ 115w (combined) | Mātikā |
| AN 11.3–5 Upanisāsuttāni (3) | ✅ 2,365w | ✅ 103w (combined) | ✅ 115w (combined) | Mātikā |
| AN 11.12 Dutiyamahānāmasutta | ✅ 1,320w | ✅ 2¶ | ✅ 3¶ | ✅ Full §-anchors & Mātikā |
| AN 11.15 Mettāsutta | ✅ 980w | ✅ 4¶ | ✅ 16¶ | ✅ Full §-anchors & Mātikā |

### Khuddaka Nikāya — Dhammapada, Udāna & Sutta Nipāta

#### Dhammapada
| Component | Status | Details |
|---|---|---|
| Mūla (26 vaggas, 423 verses) | ✅ ~17,600w | Sujato translation |
| Aṭṭhakathā (26 chapters) | ✅ ~498,000w | 294 origin stories (Ānandajoti/Burlingame) |
| Ṭīkā | ❌ Not started (BLOCKED) | — |

#### Udāna
| Component | Status | Details |
|---|---|---|
| Mūla (8 vaggas, 80 suttas) | ✅ 46,198w | Sujato translation |
| Aṭṭhakathā (8 vaggas, 1676 paragraphs) | ✅ 70,642w | CSCD Pali |
| Ṭīkā | ❌ None exists | No ancient sub-commentary exists |
 
#### Itivuttaka
| Component | Status | Details |
|---|---|---|
| Mūla (4 nipātas, 112 suttas) | ✅ 112 suttas | Interleaved Pali/English |
| Aṭṭhakathā (4 nipātas) | ✅ 112 suttas (1,166 paragraphs) | CSCD Paramatthadīpanī |
| Ṭīkā | ❌ None exists | No ancient sub-commentary exists |

#### Sutta Nipāta
| Component | Status | Details |
|---|---|---|
| Mūla (Chapters 1-5, snp1.1–snp5.19) | ✅ 73 suttas (~1140 verses) | Interleaved Pali/English |
| Aṭṭhakathā (Chapters 1-5) | ✅ 73 suttas (2,688 paragraphs) | CSCD Pali |
| Ṭīkā | ❌ None exists | No sub-commentary exists for Snp |
 
#### Theragāthā
| Component | Status | Details |
|---|---|---|
| Mūla (21 nipātas, 203 poems) | ✅ 203 poems | Interleaved Pali/English |
| Aṭṭhakathā | ❌ None migrated | No commentary migrated |
| Ṭīkā | ❌ None exists | No sub-commentary exists |

#### Therīgāthā
| Component | Status | Details |
|---|---|---|
| Mūla (16 nipātas, 73 poems) | ✅ 73 poems | Interleaved Pali/English |
| Aṭṭhakathā | ❌ None migrated | No commentary migrated |
| Ṭīkā | ❌ None exists | No sub-commentary exists |

---

## Vault Infrastructure Status

*   **Vault Index**: [INDEX.md](INDEX.md) (Operational)
*   **Obsidian Plugins**: Simsapa DPD, Dataview, Templater (all configured)
*   **CSS Toggle**: Translation toggle for pure Pali reading
*   **Templates**: Mūla, Atthakathā, Tīkā sutta templates
*   **Git**: Repository initialized with remote `https://github.com/roydsouza/pali-canon.git`, Git pre-commit hook link validation guardrail installed
*   **Scripts**: 132 Python scripts in `scratch/` (55 generators, 8 crosslinkers, 49 inspectors, 14 tests, 6 utilities)

---

## Mātikā (Buddhist Lists)

*   **Mātika Index**: [matika/INDEX.md](matika/INDEX.md)
    *   *Status*: **Completed** (22 lists total, cross-linked to canonical sources).
*   **Migrated Lists**:
    *   [[four_noble_truths|Four Noble Truths (Cattāri Ariyasaccāni)]]
    *   [[noble_eightfold_path|Noble Eightfold Path (Ariyo Aṭṭhaṅgiko Maggo)]]
    *   [[three_marks|Three Marks of Existence (Tilakkhaṇa)]]
    *   [[five_aggregates|Five Aggregates (Pañcupādānakkhandhā)]]
    *   [[dependent_origination|Dependent Origination (Paṭiccasamuppāda)]]
    *   [[five_precepts|Five Precepts (Pañcasīla)]]
    *   [[five_hindrances|Five Hindrances (Pañca Nīvaraṇāni)]]
    *   [[seven_awakening_factors|Seven Awakening Factors (Satta Bojjhaṅgā)]]
    *   [[four_foundations_of_mindfulness|Four Foundations of Mindfulness (Cattāro Satipaṭṭhānā)]]
    *   [[eight_precepts|Eight Precepts (Aṭṭhaṅgasīla)]]
    *   [[three_refuges|Three Refuges (Tisarana / Tiratana)]]
    *   [[ten_perfections|Ten Perfections (Dasa Pāramī)]]
    *   [[four_sublime_states|Four Sublime States (Cattāro Brahmavihārā)]]
    *   [[five_spiritual_faculties|Five Spiritual Faculties (Pañcindriya)]]
    *   [[three_unwholesome_roots|Three Unwholesome Roots (Akusalamūla)]]
    *   [[four_right_exertions|Four Right Exertions (Cattāro Sammappadhānā)]]
    *   [[ten_fetters|Ten Fetters (Dasa Saṃyojanā)]]
    *   [[seven_purifications|Seven Purifications (Satta Visuddhi)]]
    *   [[five_powers|Five Powers (Pañcabala)]]
    *   [[four_jhanas|Four Jhānas (Cattāri Jhānāni)]]
    *   [[six_recollections|Six Recollections (Cha Anussati)]]
    *   [[matika/gradual_training|Gradual Training (Anupubbasikkhā)]]

---

## Vinaya Piṭaka (Monastic Discipline)

*   **Vinaya Index**: [mula/vinaya/INDEX.md](mula/vinaya/INDEX.md)
    *   *Status*: **Completed Phase 18 Scaffolding**.
*   **Migrated Rules**:
    *   [[patimokkha_bhikkhu|Bhikkhu Pātimokkha (227 rules)]] (Initial migration structure, key rules, and cross-links to five/eight precepts).
    *   [[patimokkha_bhikkhuni|Bhikkhunī Pātimokkha (311 rules)]] (Initial migration structure, key rules, and cross-links to five/eight precepts).
*   **Migrated Commentary**:
    *   [[kankhavitarani|Kaṅkhāvitaraṇī]] (Buddhaghosa's commentary on the Pātimokkha rules).

---

## Prosopography & Doctrinal Indices

*   **People Index**: [people/INDEX.md](people/INDEX.md) (Key disciples Sāriputta, Ānanda, Mahāmoggallāna, Mahākassapa, and Uṇṇābha profiled).
*   **Places Index**: [places/INDEX.md](places/INDEX.md) (Key locations Sāvatthī, Rājagaha, Kosambī, and Vesālī profiled).
*   **Simile Index**: [meta/SIMILES.md](meta/SIMILES.md) (Index of major similes including the Raft, the Lute, the Six Animals, etc.).
*   **Pericope Concordance**: [meta/PERICOPES.md](meta/PERICOPES.md) (Index of stock textual formulas like the Jhāna and Dependent Origination formulas).
