#!/usr/bin/env python3
"""Add a collapsible reading progress tracker callout to each reading path file."""
import os, re

VAULT = os.environ.get("PALI_VAULT", "/Users/rds/pali_canon")
PATHS_DIR = os.path.join(VAULT, "paths")

# Per-path sutta lists (display labels only; Obsidian checkboxes are plain markdown)
PATH_SUTTAS = {
    "entering_jhana_path.md": [
        "MN 8: Sallekhasutta",
        "MN 128: Upakkilesasutta",
        "AN 9.35: Gāvīupamāsutta",
        "AN 8.63: Saṅkhittasutta",
        "AN 9.34: Nibbānasukhasutta",
        "AN 9.36: Jhānasutta",
        "MN 111: Anupadasutta",
    ],
    "vipassana_practice.md": [
        "MN 2: Sabbāsavasutta",
        "MN 148: Chachakkasutta",
        "SN 36: Vedanāsaṃyutta",
        "MN 28: Mahāhatthipadopamasutta",
        "MN 140: Dhātuvibhaṅgasutta",
        "MN 10: Satipaṭṭhānasutta",
        "DN 22: Mahāsatipaṭṭhānasutta",
    ],
    "brahmavihara_cultivation.md": [
        "MN 7: Vatthūpamasutta",
        "AN 4.125–126: Mettāsutta",
        "DN 13: Tevijjasutta",
        "SN 46.54: Mettāsahagatasutta",
        "AN 11.15: Mettānisaṃsasutta",
        "Snp 1.8: Karaṇīyamettasutta",
    ],
    "anussati_practice.md": [
        "AN 6.10: Mahānāmasutta",
        "AN 11.12: Mahānāmasutta",
        "AN 6.25: Anussatiṭṭhānasutta",
    ],
    "gradual_training_path.md": [
        "AN 8.54: Dīghajāṇusutta",
        "AN 4.99: Sikkhāpadasutta",
        "MN 51: Kandarakasutta",
        "MN 27: Cūḷahatthipadopamasutta",
        "DN 2: Sāmaññaphalasutta",
        "AN 7.65: Hirīottappasutta",
        "AN 8.53: Gotamīsutta",
        "AN 11.1–5: Cetanākaraṇīyasuttāni",
    ],
    "maranasati_path.md": [
        "AN 6.19: Paṭhamamaraṇassatisutta",
        "AN 6.20: Dutiyamaraṇassatisutta",
        "AN 8.73: Paṭhamamaraṇassatisutta",
        "SN 47.13: Cundasutta",
    ],
    "working_with_hindrances.md": [
        "MN 10 / DN 22: Satipaṭṭhāna",
        "DN 2: Sāmaññaphalasutta",
        "MN 20: Vitakkasaṇṭhānasutta",
        "SN 46: Bojjhaṅgasaṃyutta",
        "AN 5.28: Pañcaṅgikasutta",
        "AN 9.34 / AN 9.35: Jhāna stability",
    ],
    "working_with_anger.md": [
        "MN 10 / DN 22: Satipaṭṭhāna",
        "MN 20: Vitakkasaṇṭhānasutta",
        "MN 7: Vatthūpamasutta",
        "SN 46: Bojjhaṅgasaṃyutta",
        "AN 11.15: Mettānisaṃsasutta",
        "Snp 1.8: Karaṇīyamettasutta",
    ],
    "understanding_craving.md": [
        "SN 35: Saḷāyatanasaṃyutta",
        "SN 22: Khandhasaṃyutta",
        "MN 44: Cūḷavedallasutta",
        "DN 15: Mahānidānasutta",
        "MN 2: Sabbāsavasutta",
        "Snp 4: Aṭṭhakavagga",
    ],
}

TRACKER_TEMPLATE = """> [!NOTE]- Reading Progress
> Mark each sutta as you work through it.
>
{items}

"""

for filename, suttas in PATH_SUTTAS.items():
    path = os.path.join(PATHS_DIR, filename)
    if not os.path.exists(path):
        print(f"SKIP (not found): {filename}")
        continue

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check if progress tracker already present
    if "Reading Progress" in content:
        print(f"SKIP (already has tracker): {filename}")
        continue

    # Build the callout items
    items = "\n".join(f"> - [ ] {s}" for s in suttas)
    tracker = TRACKER_TEMPLATE.format(items=items)

    # Insert after the first `---` separator that follows the frontmatter block
    # (i.e., after the second `---` in the file = end of frontmatter, then the next `---`)
    # Strategy: find the overview callout or the first `---` after the title heading,
    # and insert the tracker right after that block.

    # Find position after the first > [!NOTE] callout block (or first --- after H1)
    # Insert before the first ## section header
    match = re.search(r'\n---\n\n## ', content)
    if match:
        insert_pos = match.start() + len('\n---\n\n')
        new_content = content[:insert_pos] + tracker + content[insert_pos:]
    else:
        # Fallback: append after first H1 line
        match_h1 = re.search(r'\n# .+\n', content)
        if match_h1:
            insert_pos = match_h1.end()
            new_content = content[:insert_pos] + "\n" + tracker + content[insert_pos:]
        else:
            print(f"SKIP (no insertion point): {filename}")
            continue

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Added tracker: {filename}")
