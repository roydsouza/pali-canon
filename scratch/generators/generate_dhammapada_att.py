#!/usr/bin/env python3
"""
Fetch Dhammapada-aṭṭhakathā for the 6 meditation chapters from
ancient-buddhist-texts.net (Bhante Ānandajoti's revised translation).
Generates one interleaved commentary file per vagga.
"""

import os, re, time, html as hmod
import urllib.request

VAULT      = os.environ.get("PALI_VAULT", "/Users/rds/pali_canon")
OUTPUT_DIR = os.path.join(VAULT, "atthakatha/sutta/khuddaka_nikaya/dhammapada")
BASE_URL   = "https://ancient-buddhist-texts.net/English-Texts/Dhamma-Verses-Comm"

# (chapter_num, pali_name, en_name, slug, verse_range, pages)
CHAPTERS = [
    (2,  "Appamādavagga",   "Heedfulness", "dhp_02_appamadavagga", "21–32",  range(1, 10)),
    (3,  "Cittavagga",      "The Mind",    "dhp_03_cittavagga",    "33–43",  range(1, 10)),
    (7,  "Arahantavagga",   "The Arahant", "dhp_07_arahantavagga", "90–99",  range(1, 11)),
    (14, "Buddhavagga",     "The Buddha",  "dhp_14_buddhavagga",   "179–196",range(1, 10)),
    (20, "Maggavagga",      "The Path",    "dhp_20_maggavagga",    "273–289",range(1, 13)),
    (25, "Bhikkhuvagga",    "The Monk",    "dhp_25_bhikkhuvagga",  "360–382",range(1, 13)),
]

# Slugs for mula files (for cross-links)
MULA_SLUGS = {
    2: "dhp_02_appamadavagga", 3: "dhp_03_cittavagga",
    7: "dhp_07_arahantavagga", 14: "dhp_14_buddhavagga",
    20: "dhp_20_maggavagga",   25: "dhp_25_bhikkhuvagga",
}

META_PREFIXES = ("Burlingame:", "Compare:", "Cast:", "Keywords:",
                 "last updated", "window.status")

def fetch_html(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception as e:
        return None

def clean(txt):
    txt = re.sub(r'<[^>]+>', '', txt)
    txt = hmod.unescape(txt)
    return txt.replace('\r\n', ' ').replace('\n', ' ').strip()

def parse_page(html_content):
    """Return a dict with story data extracted from one commentary page."""
    if not html_content:
        return None

    paras = re.findall(r'<p[^>]*>(.*?)</p>', html_content, re.DOTALL)
    cleaned = [clean(p) for p in paras]
    cleaned = [c for c in cleaned if c and not c.startswith("window.status")]

    story = {
        "chapter_heading": None,   # e.g. "7. The Chapter about the Arahats, Arahantavagga"
        "story_heading":   None,   # e.g. "7.1 The Story about Jīvaka's Question"
        "pali_vatthu":     None,   # e.g. "Jīvakapañhavatthu"
        "verse_refs":      [],     # e.g. ["90"]
        "metadata":        [],     # Burlingame, Compare, Cast, Keywords lines
        "narrative":       [],     # main prose paragraphs
        "verses_pali":     [],     # verse3 Pali lines
        "verses_en":       [],     # verse3 English lines
        "closing":         None,   # "At the end of the teaching..."
    }

    # Separate verse3 content (alternate Pali/English)
    verse3 = re.findall(r'<p class="verse3"[^>]*>(.*?)</p>', html_content, re.DOTALL)
    verse_texts = [clean(v) for v in verse3]
    for i, vt in enumerate(verse_texts):
        if i % 2 == 0:
            story["verses_pali"].append(vt)
        else:
            story["verses_en"].append(vt)

    # Parse the flat paragraph list
    heading1_done = False
    heading2_done = False

    for c in cleaned:
        # Nav bars
        if c.startswith("last updated"):
            continue
        if re.match(r'^[←-⇿]', c):  # arrows/nav symbols
            continue

        # Chapter heading (first substantial multi-line heading)
        if not heading1_done and re.match(r'^\d+\.', c) and '\n' in c.replace('\r',''):
            story["chapter_heading"] = c.replace('\r\n', ' ').replace('\n', ' ')
            heading1_done = True
            continue

        # Story heading – "N.M The Story about..."
        if not heading2_done and re.match(r'^\d+\.\d+', c):
            lines = [l.strip() for l in re.split(r'[\r\n]+', c) if l.strip()]
            story["story_heading"] = lines[0] if lines else c
            if len(lines) > 1:
                story["pali_vatthu"] = lines[1]
            heading2_done = True
            continue

        # Verse reference "Dhp 90" or "Dhp 90-91"
        if re.match(r'^Dhp\s+[\d–\-]+', c):
            nums = re.findall(r'\d+', c)
            story["verse_refs"].extend(nums)
            continue

        # Metadata lines
        if any(c.startswith(p) for p in META_PREFIXES):
            story["metadata"].append(c)
            continue

        # Closing note
        if c.startswith("At the end of the teaching") or c.startswith("At the conclusion"):
            story["closing"] = c
            continue

        # Skip short UI fragments
        if len(c) < 15:
            continue

        # Narrative prose
        story["narrative"].append(c)

    return story

def story_to_markdown(story, chapter_num, story_num):
    """Convert a parsed story dict to markdown text."""
    lines = []

    title = story["story_heading"] or f"Story {story_num}"
    pali  = story["pali_vatthu"] or ""
    refs  = story["verse_refs"]
    mula_slug = MULA_SLUGS.get(chapter_num, "")

    # Heading
    if pali:
        lines.append(f"### {title} (*{pali}*)")
    else:
        lines.append(f"### {title}")

    # Verse cross-links
    if refs and mula_slug:
        links = ", ".join(f"[[{mula_slug}#{r}|Dhp {r}]]" for r in refs)
        lines.append(f"*Verse(s): {links}*")
    lines.append("")

    # Metadata (small)
    for m in story["metadata"]:
        lines.append(f"*{m}*")
    if story["metadata"]:
        lines.append("")

    # Narrative
    for para in story["narrative"]:
        lines.append(para)
        lines.append("")

    # Verse quote
    for pali_v, en_v in zip(story["verses_pali"], story["verses_en"]):
        for pl in pali_v.split('\n'):
            pl = pl.strip()
            if pl:
                lines.append(f"> **{pl}**  ")
        for el in en_v.split('\n'):
            el = el.strip()
            if el:
                lines.append(f"> *{el}*  ")
        lines.append(">")
    if story["verses_pali"]:
        lines.append("")

    # Closing
    if story["closing"]:
        lines.append(f"*{story['closing']}*")
        lines.append("")

    lines.append("---")
    lines.append("")
    return "\n".join(lines)

def build_chapter_file(chapter_num, pali_name, en_name, slug, verse_range, stories):
    lines = [
        "---",
        f"id: DHP_{chapter_num:02d}_att",
        f"title_pali: {pali_name}vaṇṇanā",
        f"title_en: Commentary on {pali_name} ({en_name})",
        "type: atthakatha",
        "pitaka: sutta",
        "nikaya: khuddaka",
        "text: dhammapada",
        f"vagga: {chapter_num}",
        f'verse_range: "{verse_range}"',
        f"mula_file: /mula/sutta/khuddaka_nikaya/dhammapada/{slug}.md",
        "translator: Bhante Ānandajoti (revised Burlingame)",
        "source: https://ancient-buddhist-texts.net/English-Texts/Dhamma-Verses-Comm/",
        "---",
        "",
        f"# Dhammapada Commentary — Chapter {chapter_num}: {pali_name}",
        "",
        "**Navigation**: [[INDEX|Pali Canon Vault]] / [[atthakatha/Atthakatha-Index|Atthakathā]] / "
        "[[atthakatha/sutta/Atthakatha-Sutta-Index|Sutta]] / "
        "[[atthakatha/sutta/khuddaka_nikaya/Atthakatha-Khuddaka-Index|Khuddaka Nikāya]] / "
        "[[atthakatha/sutta/khuddaka_nikaya/dhammapada/Atthakatha-Dhammapada-Index|Dhammapada]]",
        f"**Mūla**: [[{slug}|{pali_name} — {en_name}]]",
        "",
        f"## {pali_name}vaṇṇanā — {en_name}",
        f"*Verses {verse_range}*",
        "",
        "*Translation: Bhante Ānandajoti's revised edition of Burlingame's Buddhist Legends.*",
        "",
    ]

    for i, story in enumerate(stories, 1):
        if story:
            lines.append(story_to_markdown(story, chapter_num, i))

    return "\n".join(lines)

def build_index(chapters_done):
    rows = [f"| [[{slug}_att\\|{num}. {pali}]] | {en} | {vr} |"
            for num, pali, en, slug, vr in chapters_done]
    return f"""---
type: index
pitaka: sutta
nikaya: khuddaka
text: dhammapada
layer: atthakatha
---

# Dhammapada — Atthakathā (Commentary)

**Navigation**: [[INDEX|Pali Canon Vault]] / [[atthakatha/Atthakatha-Index|Atthakathā]] / [[atthakatha/sutta/Atthakatha-Sutta-Index|Sutta]] / [[atthakatha/sutta/khuddaka_nikaya/Atthakatha-Khuddaka-Index|Khuddaka Nikāya]]

Commentary (Dhammapada-aṭṭhakathā) in English. Translation by Bhante Ānandajoti (revised edition of Burlingame's *Buddhist Legends*, 1921).

Each entry contains: origin story (vatthu), narrative, verse quote, and closing note.

## Migrated Chapters

| Chapter | English | Verses |
|---|---|---|
{chr(10).join(rows)}
"""

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    chapters_done = []

    for chapter_num, pali_name, en_name, slug, verse_range, pages in CHAPTERS:
        print(f"\nChapter {chapter_num}: {pali_name}")
        stories = []

        for page_n in pages:
            url = f"{BASE_URL}/{chapter_num:02d}-{page_n:02d}.htm"
            print(f"  Fetching {chapter_num:02d}-{page_n:02d}.htm...", end=" ", flush=True)
            html_content = fetch_html(url)
            if html_content:
                story = parse_page(html_content)
                if story and (story["story_heading"] or story["narrative"]):
                    stories.append(story)
                    title = story.get("story_heading","?")[:50]
                    print(f"ok ({len(story['narrative'])} paragraphs) — {title}")
                else:
                    print("no content")
            else:
                print("404/error")
            time.sleep(0.3)

        content = build_chapter_file(chapter_num, pali_name, en_name, slug, verse_range, stories)
        fname   = f"{slug}_att.md"
        with open(os.path.join(OUTPUT_DIR, fname), "w", encoding="utf-8") as f:
            f.write(content + "\n")
        wc = len(content.split())
        print(f"  -> {fname}: {len(stories)} stories, {wc:,} words")
        chapters_done.append((chapter_num, pali_name, en_name, slug, verse_range))

    index = build_index(chapters_done)
    with open(os.path.join(OUTPUT_DIR, "Atthakatha-Dhammapada-Index.md"), "w", encoding="utf-8") as f:
        f.write(index)
    print("\nDone.")

if __name__ == "__main__":
    main()
