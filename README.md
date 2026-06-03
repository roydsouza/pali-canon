# Dhamma Practice Workstation

A personal Obsidian vault for deep study and sitting practice with the Theravāda Pali Canon — built around meditation, not academic coverage.

> **If you have this vault open in Obsidian, your entry point is [INDEX.md](INDEX.md).**  
> Start there. Everything below is a map of what you will find once you do.

---

## What This Is

The **Dhamma Practice Workstation** pairs every sutta with its classical commentary and sub-commentary, weaves the whole together through a bidirectional doctrinal cross-reference web, and adds NLP reading aids — vocabulary glosses, a graded reader, and a Pali word lookup — that support a serious, ongoing meditation practice.

The organizing question for every piece of content is: *does a practitioner in the Theravāda tradition need this for their sitting practice or precepts study?* If not, it doesn't belong here.

---

## Five Layers of Text

| Layer | Folder | Content | Source |
|---|---|---|---|
| **Mūla** (root texts) | [`mula/`](mula/) | Interleaved **bold Pali** / *italic English* | SuttaCentral/Bilara (CC0) + Bhikkhu Sujato |
| **Aṭṭhakathā** (commentaries) | [`atthakatha/`](atthakatha/) | Classical Pali, `§NNN` paragraph anchors | CSCD tipitaka.org XML |
| **Ṭīkā** (sub-commentaries) | [`tika/`](tika/) | Classical Pali, `§NNN` paragraph anchors | CSCD tipitaka.org XML |
| **Pakaraṇa** (treatises) | [`pakarana/`](pakarana/) | Visuddhimagga Chs. VIII & XI; later: Abhidhamma | Buddhaghosa, 5th c. CE |
| **Mātikā** (doctrinal lists) | [`matika/`](matika/) | 22 cross-referenced canonical lists | Pali + English |

Every mūla sutta looks like this:

```
**Evaṁ me sutaṁ—**
*So I have heard.*
```

Bold = Pali. Italic = Bhikkhu Sujato's translation. Press **Cmd+R** in Obsidian to hide the English and read Pali alone.

---

## Current Inventory

| Nikāya | Suttas in vault | Layers |
|---|---|---|
| Dīgha Nikāya | [8 suttas](mula/sutta/digha_nikaya/) | Mūla + Aṭṭhakathā + Ṭīkā |
| Majjhima Nikāya | [22 suttas](mula/sutta/majjhima_nikaya/) | Mūla + Aṭṭhakathā + Ṭīkā |
| Saṃyutta Nikāya | [11 saṃyuttas (225 suttas)](mula/sutta/samyutta_nikaya/) | Mūla + Aṭṭhakathā + Ṭīkā |
| Aṅguttara Nikāya | [35 groups (~662 suttas)](mula/sutta/anguttara_nikaya/) | Mūla + Aṭṭhakathā + Ṭīkā |
| Dhammapada | [423 verses, 26 vaggas](mula/sutta/khuddaka_nikaya/dhammapada/) | Mūla + Aṭṭhakathā |
| Udāna | [80 suttas](mula/sutta/khuddaka_nikaya/) | Mūla + Aṭṭhakathā |
| Itivuttaka | [112 suttas](mula/sutta/khuddaka_nikaya/itivuttaka/) | Mūla + Aṭṭhakathā |
| Sutta Nipāta | [73 suttas, 5 chapters](mula/sutta/khuddaka_nikaya/sutta_nipata/) | Mūla + Aṭṭhakathā |
| Theragāthā | [203 poems](mula/sutta/khuddaka_nikaya/theragatha/) | Mūla |
| Therīgāthā | [73 poems](mula/sutta/khuddaka_nikaya/therigatha/) | Mūla |
| Vinaya Piṭaka | [Bhikkhu + Bhikkhunī Pātimokkha](mula/vinaya/) | Selected rules + Kaṅkhāvitaraṇī |
| **Visuddhimagga** | [Chapters VIII & XI](pakarana/visuddhimagga/) | Pakaraṇa (Buddhaghosa) |
| **Mātikā lists** | [22 lists](matika/) | Pali + English, fully cross-linked |

**~1,200 Markdown files · ~15,200 wikilinks · 0 broken links**

---

## Practice & Study Support

### Seven Practice Domains
Content is organized around seven practice domains. Each has a dedicated reading path in [`paths/`](paths/):

| Domain           | Key suttas                                                                                                                                        | Reading path                                       |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| Jhāna            | [MN 118](mula/sutta/majjhima_nikaya/mn118.md), [AN 9.36](mula/sutta/anguttara_nikaya/an9_36.md), [MN 111](mula/sutta/majjhima_nikaya/mn111.md)    | [Entering Jhāna](paths/entering_jhana_path.md)     |
| Vipassanā        | [MN 10](mula/sutta/majjhima_nikaya/mn10.md), [DN 22](mula/sutta/digha_nikaya/dn22.md), [MN 148](mula/sutta/majjhima_nikaya/mn148.md)              | [Vipassanā Practice](paths/vipassana_practice.md)  |
| Brahmavihāra     | [MN 7](mula/sutta/majjhima_nikaya/mn7.md), [DN 13](mula/sutta/digha_nikaya/dn13.md), [Snp 1.8](mula/sutta/khuddaka_nikaya/sutta_nipata/snp1_8.md) | [Brahmavihāra](paths/brahmavihara_cultivation.md)  |
| Anussati         | [AN 6.10](mula/sutta/anguttara_nikaya/an6_10.md), [AN 11.12](mula/sutta/anguttara_nikaya/an11_12.md)                                              | [Anussati Practice](paths/anussati_practice.md)    |
| Gradual Training | [MN 27](mula/sutta/majjhima_nikaya/mn27.md), [DN 2](mula/sutta/digha_nikaya/dn2.md), [AN 8.54](mula/sutta/anguttara_nikaya/an8_54.md)             | [Gradual Training](paths/gradual_training_path.md) |
| Maraṇasati       | [AN 6.19](mula/sutta/anguttara_nikaya/an6_19.md), [AN 6.20](mula/sutta/anguttara_nikaya/an6_20.md)                                                | [Maraṇasati](paths/maranasati_path.md)             |
| Paritta          | [Snp 1.8](mula/sutta/khuddaka_nikaya/sutta_nipata/snp1_8.md), [Snp 2.1](mula/sutta/khuddaka_nikaya/sutta_nipata/snp2_1.md)                        | [Paritta Index](paritta/INDEX.md)                  |

Three additional **question-driven paths** answer specific practice situations:
[Working with the Hindrances](paths/working_with_hindrances.md) ·
[Working with Anger](paths/working_with_anger.md) ·
[Understanding Craving](paths/understanding_craving.md)

### The Mātikā Web
Twenty-two canonical Buddhist lists — [Four Noble Truths](matika/four_noble_truths.md), [Noble Eightfold Path](matika/noble_eightfold_path.md), [Five Aggregates](matika/five_aggregates.md), [Seven Awakening Factors](matika/seven_awakening_factors.md), and 18 more — each link forward to every sutta in the vault that treats that doctrine, and every sutta links back. Start at any list, navigate to the canonical treatments; start at any sutta, follow its doctrinal threads outward.

### NLP Reading Aids (pali-nlp companion)
A separate [`pali-nlp`](https://github.com/roydsouza/pali-nlp) repository processes the vault corpus and writes reading aids back in:

- **Vocabulary callouts** — every mūla sutta has a collapsible `[!NOTE]- Vocabulary` block at the bottom listing the 60 rarest Pali headwords with DPD glosses (508 suttas updated)
- **[Graded reader](paths/graded_reader.md)** — 518 suttas ranked easiest to hardest by lexical difficulty; a structured reading ladder for Pali learners
- **DPD double-click lookup** — Simsapa plugin: double-click any bold Pali word to open the Digital Pāli Dictionary sidebar

### Study Tools
- [People index](people/) — Prosopography: Sāriputta, Ānanda, Mahāmoggallāna, and others, each linked to every sutta they appear in
- [Places index](places/) — Geographic index: Sāvatthī, Rājagaha, Vesālī, and others
- [Simile Index](meta/SIMILES.md) — Cross-referenced catalogue of the canon's major similes
- [Pericope Concordance](meta/PERICOPES.md) — Map of repeated stock formulas (jhāna cadences, dependent origination chains)
- [Paritta texts](paritta/) — Continuous Pali-only recitation texts for protective chanting

---

## Tutorials

The [`tutorial/`](tutorial/) folder contains six integrated practice tutorials — written *inside* the vault rather than as external documentation, so every step links directly to the relevant sutta, commentary, or mātikā note:

| Tutorial | What it covers |
|---|---|
| [01 — Sitting with the Ānāpānasati Sutta](tutorial/01_breath_practice.md) | The sixteen steps, how to use the commentary, how to carry it into a sitting session |
| [02 — Satipaṭṭhāna as a Practice Map](tutorial/02_satipatthana_as_map.md) | Four foundations, the refrain, MN 10 vs DN 22 |
| [03 — The Three Layers](tutorial/03_reading_the_layers.md) | When and how to use commentary and sub-commentary |
| [04 — Following a Doctrine](tutorial/04_matika_web.md) | Using the mātikā web as a live practice tool |
| [05 — Reading Pali](tutorial/05_pali_reading.md) | Toggle, DPD, vocabulary callouts, graded reader |
| [06 — Building a Sustained Practice](tutorial/06_building_a_practice.md) | Reading paths and long-term practice structure |

→ **[Open the tutorial index in Obsidian](tutorial/INDEX.md)**

---

## Design Principles

**Practice first, study second.** A sutta is added because a practitioner working in the Theravāda tradition needs it — not to fill gaps in coverage. Seven practice domains set the priority order; everything else follows.

**Four layers, not one.** Mūla for practice, Aṭṭhakathā for precision, Ṭīkā for edge cases, Pakaraṇa (Visuddhimagga) for systematic synthesis. Commentary paragraphs are cross-linked to root-text paragraphs at the `§NNN` level so study stays in context.

**Markdown-native.** An Obsidian vault is a folder of plain `.md` files. No database, no server, no lock-in. Every file is readable in any Markdown editor; the cross-links and plugins enhance the experience but are not required to read the texts.

**One canonical translation.** [Bhikkhu Sujato's SuttaCentral translations](https://suttacentral.net) (CC0) are the authoritative English text. No AI translation is layered over them.

---

## Repository Layout

```
pali_canon/
├── INDEX.md             ← Vault home — start here in Obsidian
├── mula/                # Root texts (interleaved Pali/English)
│   ├── sutta/
│   │   ├── digha_nikaya/
│   │   ├── majjhima_nikaya/
│   │   ├── samyutta_nikaya/
│   │   ├── anguttara_nikaya/
│   │   └── khuddaka_nikaya/
│   └── vinaya/
├── atthakatha/          # Classical commentaries (CSCD Pali, §-anchored)
├── tika/                # Classical sub-commentaries (CSCD Pali, §-anchored)
├── pakarana/            # Post-canonical treatises (Visuddhimagga)
├── matika/              # 22 doctrinal lists + 8 path-factor sub-files
├── paths/               # 7 practice-domain + 3 question-driven reading sequences
├── tutorial/            # 6 integrated practice tutorials
├── paritta/             # Protective chanting texts (continuous Pali)
├── practice/            # Meditation log, memorization tracker, practice dashboard
├── people/              # Prosopography index
├── places/              # Geographic index
├── meta/                # TASKS, ROADMAP, STATUS, SYNC_LOG, SIMILES, PERICOPES
├── templates/           # Obsidian Templater templates
└── scratch/             # Python tooling
    ├── generators/      #   Sutta file generators (SuttaCentral API + CSCD XML)
    ├── crosslinkers/    #   Paragraph-level commentary alignment
    ├── inspect/         #   Frontmatter linter, link validator
    ├── lib/             #   Shared utilities (pali_utils.py)
    └── tests/           #   Unit tests (run before every commit)
```

---

## Tooling

All scripts require Python 3.11+. Set `PALI_VAULT` to the vault root:

```bash
export PALI_VAULT=/path/to/pali_canon
```

| Script | Purpose |
|---|---|
| [`scratch/validate_links.py`](scratch/validate_links.py) | Validate all wikilinks vault-wide — must be 0 errors before every commit |
| [`scratch/tests/run_all_tests.py`](scratch/tests/run_all_tests.py) | Full unit-test suite — must all pass before every commit |
| [`scratch/generators/generate_sutta.py`](scratch/generators/generate_sutta.py) | Generate mūla + atthakathā + ṭīkā for any sutta ID via SuttaCentral API + CSCD XML |
| [`scratch/crosslinkers/crosslink_generic.py`](scratch/crosslinkers/crosslink_generic.py) | Inject paragraph-level cross-links between commentary and root text |
| [`scratch/lib/pali_utils.py`](scratch/lib/pali_utils.py) | Shared utilities: XML parsing, frontmatter I/O, Pali normalization |

A git pre-commit hook (`scratch/validate_links.py`) runs automatically on every commit. A `post-commit` hook pushes to `origin/main`. Never commit with `--no-verify`.

The companion **[pali-nlp](https://github.com/roydsouza/pali-nlp)** repository handles corpus analysis and writes vocabulary/grading artefacts back into the vault.

---

## Roadmap

### Done
- ✅ Phases 1–16: All practice-domain suttas (three layers), 22 mātikā lists, 10 reading paths, prosopography, simile index, pericope concordance, parallel texts, Vinaya, Abhidhamma stubs
- ✅ Phase 17 Stage 1: pali-nlp companion — vocabulary callouts (508 suttas), graded reader (518 suttas), DPD lemmatizer
- ✅ Tutorial series: 6 integrated practice tutorials in `tutorial/`
- ✅ Visuddhimagga: Chapters VIII (ānāpānasati) and XI (jhānas) in `pakarana/`

### In Progress / Planned
- Phase 17 Stage 1D: SRS vocabulary card generation
- Phase 17 Stage 2: Concordance index, NER → prosopography
- Phase 17 Stage 3: Local vector search + RAG
- Visuddhimagga: Remaining samādhi chapters (III–VII, IX–X) and wisdom section (XIV–XXII)
- Phase 21 (gated): Systematic canonical breadth expansion — begins only after practice domains feel saturated

See [`meta/TASKS.md`](meta/TASKS.md) and [`meta/ROADMAP.md`](meta/ROADMAP.md) for granular tracking.

---

## What This Is Not

- **Not a public resource.** Format and density are optimized for one reader.
- **Not an academic database.** No paper annotations, citation management, or research metadata.
- **Not a translation project.** Sujato's translations are the text; this vault adds structure and commentary.
- **Not mobile-first or cloud-synced.** Designed for a single macOS machine with local storage.

---

## Data Sources and Licenses

| Source | Usage | License |
|---|---|---|
| [SuttaCentral / Bilara](https://github.com/suttacentral/bilara-data) | Mūla segments + Sujato translations | CC0 |
| [CSCD (tipitaka.org)](https://tipitaka.org) | Commentary and sub-commentary XML | Personal use; cached in `scratch/xml_cache/` (git-ignored) |
| [Digital Pāli Dictionary](https://digitalpalidictionary.github.io) | Lexicon SQLite for pali-nlp | Mixed CC0 / CC BY-NC-SA (git-ignored) |

Audio files, the XML cache, and the DPD database are git-ignored and must not be committed.

---

## Coordination

Multi-agent session work is tracked in [`meta/`](meta/):

| File | Purpose |
|---|---|
| [`meta/TASKS.md`](meta/TASKS.md) | Granular task checklist — never mark done unless verified |
| [`meta/ROADMAP.md`](meta/ROADMAP.md) | Phase sequencing with evaluation checkpoints |
| [`meta/STATUS.md`](meta/STATUS.md) | Vault metrics snapshot |
| [`meta/SYNC_LOG.md`](meta/SYNC_LOG.md) | Timestamped session log; entries >30 days rotate to `meta/sync_archive/` |
| [`CLAUDE.md`](CLAUDE.md) | Agent guardrails — read before making any changes |
