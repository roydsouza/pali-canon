🏠 [[INDEX|Dashboard]]

# CLAUDE.md — Pali Canon Vault Agent Guardrails
[[INDEX|Dashboard]] > [[topics/topics|Topics Hub]] > [[topics/texts/texts|Texts & Canon]] > [[topics/texts/pali-canon/Texts-Index|Pāḷi Canon]] > CLAUDE.md — Pali Canon Vault Agent Guardrails

*This is the project-level configuration for AI agents working on this vault.
Read this FIRST before making any changes.*

## Mission

Personal Obsidian study vault for the Pali Canon (Theravāda Buddhist scriptures).
**Primary goal**: meditation practice. **Secondary goal**: precepts study.
See `meta/VISION.md` for full scope and guiding principles.

## Data Model

**Three-layer structure** (every sutta should have all three where available):

| Layer | Directory | Content | Source |
|---|---|---|---|
| **Mūla** (root text) | `mula/` | Interleaved **bold Pali** / *italic English* segments | SuttaCentral/Bilara (CC0) + Sujato translations |
| **Atthakathā** (commentary) | `atthakatha/` | CSCD Pali commentary with `§NNN` paragraph anchors | tipitaka.org CSCD XML (cached in `scratch/xml_cache/`) |
| **Ṭīkā** (sub-commentary) | `tika/` | CSCD Pali sub-commentary with `§NNN` paragraph anchors | tipitaka.org CSCD XML |

**Cross-cutting layers**:
- `matika/` — Doctrinal lists (e.g. Noble Eightfold Path, Five Aggregates) linking suttas by doctrine
- `paths/` — Thematic reading paths for practice
- `practice/` — Meditation logs, memorization, chanting
- `paritta/` — Protective chant indexes
- `templates/` — Obsidian Templater templates for new notes

## Segment Format (Mūla files)

Each segment is an interleaved Pali/English pair:

```
**Evaṁ me sutaṁ—**
*So I have heard.*
```

Bold = Pali. Italic = English (Sujato). Never layer AI translation over Sujato's translations.

## Coordination Contract

**These are the shared agent-coordination files — update them every session:**

| File | Purpose | Update when |
|---|---|---|
| `meta/TASKS.md` | Granular task checklist | Mark done / add new tasks |
| `meta/SYNC_LOG.md` | Timestamped session log | Every session end (ISO-8601 with offset) |
| `meta/ROADMAP.md` | Phase sequencing | Phase status changes |
| `meta/STATUS.md` | Vault metrics snapshot | Counts change |

**Timestamp format**: `2026-05-27 18:00:00-07:00` (ISO-8601 with UTC offset).

## Guardrails — NEVER BYPASS

1. **Link validator** (pre-commit hook): `python3 scratch/validate_links.py`
   - Must show **0 errors** before every commit
   - Never commit with `--no-verify`

2. **Unit tests**: `python3 scratch/tests/run_all_tests.py`
   - Must show **all pass** before every commit

3. **Commit discipline**:
   - One logical change per commit
   - Conventional-commit prefixes: `fix:`, `feat:`, `docs:`, `refactor:`, `chore:`
   - Commit after each sutta or discrete task

4. **Push to GitHub after every commit**: `git push origin main`
   - The `post-commit` hook does this automatically in the background.
   - If the hook fails silently (offline, auth error), push manually before ending the session.
   - Remote: `https://github.com/roydsouza/pali-canon.git`
   - **All agents** (Claude Code, Gemini/AntiGravity, OpenCode, Pi, etc.) must leave `origin/main` in sync with local `main` at session end.

5. **Truthfulness**: Never mark a TASKS.md item done unless verified. Counts in docs must match reality.

## Data Sources & Licenses

| Source | Usage | License | Git policy |
|---|---|---|---|
| SuttaCentral / Bilara | Mūla segments + Sujato translations | CC0 | Committed |
| CSCD (tipitaka.org) | Commentary & sub-commentary XML | — | Cached in `scratch/xml_cache/` (git-ignored) |
| DPD (Digital Pāli Dictionary) | Lexicon SQLite for NLP companion | Mixed CC0 / CC BY-NC-SA | Git-ignored; verify terms before redistribution |

## Do NOT

- **AI-translate** over Sujato's translations
- **Commit** the DPD database, audio files, or XML cache (all git-ignored)
- **Rename files** without fixing all wikilinks vault-wide + re-running the validator
- **Bypass** the pre-commit hook or test suite
- **Create NLP engine code** inside this vault — the NLP system lives in a separate `pali-nlp` repo (see `meta/VISION.md`)
- **Use `file://` absolute paths** in embeds or links — use vault-relative wikilinks instead
- **Use Dataview inline expressions** (`` `$= dv.pages(...)` ``) inside HTML `<div>` blocks in INDEX.md or any dashboard file — they do not render reliably inside HTML and show as raw code strings to users. Use hardcoded counts instead; update them manually when significant content is added. Standard ` ```dataview ``` ` code blocks in Markdown sections are fine.
- **Add wikilinks to files that do not exist yet** — always verify the target file exists before linking. The pre-commit hook validates links on staged files; creating a link in an existing file without staging the target will not be caught.

## Key Scripts

| Script | Purpose |
|---|---|
| `scratch/validate_links.py` | Validate all wikilinks and HTML links vault-wide |
| `scratch/tests/run_all_tests.py` | Run all unit tests |
| `scratch/generators/generate_sutta.py` | Unified sutta generator (mūla + att + tīkā) |
| `scratch/crosslinkers/crosslink_generic.py` | Paragraph-level cross-linking between layers |
| `scratch/lib/pali_utils.py` | Shared Pali text utilities (XML, frontmatter, normalization) |

See `scratch/SKILL_GUIDE.md` for the cross-linking algorithm details.

## Workflow: Adding a New Sutta

1. Generate mūla, atthakathā, ṭīkā files (use `generate_sutta.py` or layer-specific generators)
2. Run `crosslink_generic.py` for paragraph-level alignment
3. Add mātikā reverse-links in relevant `matika/*.md` files
4. Update the nikāya INDEX file(s) for each layer
5. Run `python3 scratch/validate_links.py` — must be 0 errors
6. Run `python3 scratch/tests/run_all_tests.py` — must all pass
7. Update `meta/STATUS.md` counts
8. Update `meta/TASKS.md` (mark done / add new)
9. Commit with `feat:` prefix
10. Append a timestamped entry to `meta/SYNC_LOG.md`

## Environment

- **`PALI_VAULT`** environment variable: points to this vault's root directory. Used by all `scratch/` scripts.
- **Git remote**: `origin` → `https://github.com/roydsouza/pali-canon.git`
- **Branch**: `main`
