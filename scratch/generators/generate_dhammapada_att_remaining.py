#!/usr/bin/env python3
"""
Fetch Dhammapada-aṭṭhakathā for the remaining 20 vaggas.
(Chapters 2,3,7,14,20,25 were already done in generate_dhammapada_att.py)

Source: ancient-buddhist-texts.net — Bhante Ānandajoti's revised Burlingame.
Output: atthakatha/sutta/khuddaka_nikaya/dhammapada/{slug}_att.md
"""

import os, re, time, html as hmod
import urllib.request

VAULT      = os.environ.get("PALI_VAULT", "/Users/rds/pali_canon")
OUTPUT_DIR = os.path.join(VAULT, "atthakatha/sutta/khuddaka_nikaya/dhammapada")
BASE_URL   = "https://ancient-buddhist-texts.net/English-Texts/Dhamma-Verses-Comm"

# (chapter_num, pali_name, en_name, slug, verse_range, max_pages)
# max_pages: generous upper bound; script stops at 404 automatically.
CHAPTERS = [
    ( 1, "Yamakavagga",       "Pairs",           "dhp_01_yamakavagga",       "1–20",    25),
    ( 4, "Pupphavagga",       "Flowers",          "dhp_04_pupphavagga",       "44–59",   20),
    ( 5, "Bālavagga",         "Fools",            "dhp_05_balavagga",         "60–75",   20),
    ( 6, "Paṇḍitavagga",      "The Wise",         "dhp_06_panditavagga",      "76–89",   18),
    ( 8, "Sahassavagga",      "The Thousands",    "dhp_08_sahassavagga",      "100–115", 20),
    ( 9, "Pāpavagga",         "Evil",             "dhp_09_papavagga",         "116–128", 18),
    (10, "Daṇḍavagga",        "The Rod",          "dhp_10_dandavagga",        "129–145", 22),
    (11, "Jarāvagga",         "Old Age",          "dhp_11_jaravagga",         "146–156", 16),
    (12, "Attavagga",         "Oneself",          "dhp_12_attavagga",         "157–166", 15),
    (13, "Lokavagga",         "The World",        "dhp_13_lokavagga",         "167–178", 17),
    (15, "Sukhavagga",        "Happiness",        "dhp_15_sukhavagga",        "197–208", 17),
    (16, "Piyavagga",         "Affection",        "dhp_16_piyavagga",         "209–220", 17),
    (17, "Kodhavagga",        "Anger",            "dhp_17_kodhavagga",        "221–234", 18),
    (18, "Malavagga",         "Impurity",         "dhp_18_malavagga",         "235–255", 26),
    (19, "Dhammaṭṭhavagga",   "The Just",         "dhp_19_dhammatthavagga",   "256–272", 22),
    (21, "Pakiṇṇakavagga",    "Miscellaneous",    "dhp_21_pakinnakavagga",    "290–305", 20),
    (22, "Nirayavagga",       "Hell",             "dhp_22_nirayavagga",       "306–319", 18),
    (23, "Nāgavagga",         "The Elephant",     "dhp_23_nagavagga",         "320–333", 18),
    (24, "Taṇhāvagga",        "Craving",          "dhp_24_tanhavagga",        "334–359", 32),
    (26, "Brāhmaṇavagga",     "The Brahmin",      "dhp_26_brahmanavagga",     "383–423", 47),
]

META_PREFIXES = ("Burlingame:", "Compare:", "Cast:", "Keywords:",
                 "last updated", "window.status")

# ── fetching & parsing ────────────────────────────────────────────────────────

def fetch_html(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception:
        return None


def clean(txt):
    txt = re.sub(r'<[^>]+>', '', txt)
    txt = hmod.unescape(txt)
    return txt.replace('\r\n', ' ').replace('\n', ' ').strip()


def parse_page(html_content):
    if not html_content:
        return None

    paras = re.findall(r'<p[^>]*>(.*?)</p>', html_content, re.DOTALL)
    cleaned = [clean(p) for p in paras]
    cleaned = [c for c in cleaned if c and not c.startswith("window.status")]

    story = {
        "chapter_heading": None,
        "story_heading":   None,
        "pali_vatthu":     None,
        "verse_refs":      [],
        "metadata":        [],
        "narrative":       [],
        "verses_pali":     [],
        "verses_en":       [],
        "closing":         None,
    }

    verse3 = re.findall(r'<p class="verse3"[^>]*>(.*?)</p>', html_content, re.DOTALL)
    verse_texts = [clean(v) for v in verse3]
    for i, vt in enumerate(verse_texts):
        if i % 2 == 0:
            story["verses_pali"].append(vt)
        else:
            story["verses_en"].append(vt)

    heading1_done = False
    heading2_done = False

    for c in cleaned:
        if c.startswith("last updated"):
            continue
        if re.match(r'^[←⇐\-⇿»«]', c):
            continue

        if not heading1_done and re.match(r'^\d+\.', c) and '\n' in c.replace('\r', ''):
            story["chapter_heading"] = c.replace('\r\n', ' ').replace('\n', ' ')
            heading1_done = True
            continue

        if not heading2_done and re.match(r'^\d+\.\d+', c):
            lines = [l.strip() for l in re.split(r'[\r\n]+', c) if l.strip()]
            story["story_heading"] = lines[0] if lines else c
            if len(lines) > 1:
                story["pali_vatthu"] = lines[1]
            heading2_done = True
            continue

        if re.match(r'^Dhp\s+[\d–\-]+', c):
            nums = re.findall(r'\d+', c)
            story["verse_refs"].extend(nums)
            continue

        if any(c.startswith(p) for p in META_PREFIXES):
            story["metadata"].append(c)
            continue

        if c.startswith("At the end of the teaching") or c.startswith("At the conclusion"):
            story["closing"] = c
            continue

        if len(c) < 15:
            continue

        story["narrative"].append(c)

    return story


# ── markdown assembly ─────────────────────────────────────────────────────────

def story_to_markdown(story, chapter_num, story_num, slug):
    lines = []
    title = story["story_heading"] or f"Story {story_num}"
    pali  = story["pali_vatthu"] or ""
    refs  = story["verse_refs"]

    if pali:
        lines.append(f"### {title} (*{pali}*)")
    else:
        lines.append(f"### {title}")

    if refs and slug:
        links = ", ".join(f"[[{slug}#{r}|Dhp {r}]]" for r in refs)
        lines.append(f"*Verse(s): {links}*")
    lines.append("")

    for m in story["metadata"]:
        lines.append(f"*{m}*")
    if story["metadata"]:
        lines.append("")

    for para in story["narrative"]:
        lines.append(para)
        lines.append("")

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
            lines.append(story_to_markdown(story, chapter_num, i, slug))
    return "\n".join(lines)


# ── index update ─────────────────────────────────────────────────────────────

def update_index(all_chapters_data):
    """Rewrite the Dhammapada att INDEX.md with all 26 chapters (done + remaining)."""
    # Already-done chapters
    done_chapters = [
        ( 2, "Appamādavagga",   "Heedfulness", "dhp_02_appamadavagga",  "21–32"),
        ( 3, "Cittavagga",      "The Mind",    "dhp_03_cittavagga",     "33–43"),
        ( 7, "Arahantavagga",   "The Arahant", "dhp_07_arahantavagga",  "90–99"),
        (14, "Buddhavagga",     "The Buddha",  "dhp_14_buddhavagga",    "179–196"),
        (20, "Maggavagga",      "The Path",    "dhp_20_maggavagga",     "273–289"),
        (25, "Bhikkhuvagga",    "The Monk",    "dhp_25_bhikkhuvagga",   "360–382"),
    ]
    all_data = [(num, pali, en, slug, vr, wc)
                for num, pali, en, slug, vr, wc in all_chapters_data]
    # Add already-done (word count unknown, mark as —)
    existing_nums = {row[0] for row in all_chapters_data}
    for num, pali, en, slug, vr in done_chapters:
        if num not in existing_nums:
            all_data.append((num, pali, en, slug, vr, None))

    all_data.sort(key=lambda r: r[0])

    rows = []
    for num, pali, en, slug, vr, wc in all_data:
        wc_str = f"{wc:,}" if wc else "—"
        rows.append(f"| [[{slug}_att\\|{num}. {pali}]] | {en} | {vr} | {wc_str} |")

    index_content = f"""---
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

## All 26 Chapters

| Chapter | English | Verses | Words |
|---|---|---|---|
{chr(10).join(rows)}
"""
    idx_path = os.path.join(OUTPUT_DIR, "Atthakatha-Dhammapada-Index.md")
    with open(idx_path, "w", encoding="utf-8") as f:
        f.write(index_content)
    print(f"  Index updated: {idx_path}")


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    all_chapters_data = []
    consecutive_404s = 0

    for chapter_num, pali_name, en_name, slug, verse_range, max_pages in CHAPTERS:
        print(f"\nChapter {chapter_num}: {pali_name}")
        stories = []
        consecutive_404s = 0

        for page_n in range(1, max_pages + 1):
            url = f"{BASE_URL}/{chapter_num:02d}-{page_n:02d}.htm"
            html_content = fetch_html(url)
            if html_content:
                consecutive_404s = 0
                story = parse_page(html_content)
                if story and (story["story_heading"] or story["narrative"]):
                    stories.append(story)
                    title = (story.get("story_heading") or "")[:50]
                    print(f"  {chapter_num:02d}-{page_n:02d}: {title}")
                else:
                    print(f"  {chapter_num:02d}-{page_n:02d}: no content")
            else:
                consecutive_404s += 1
                print(f"  {chapter_num:02d}-{page_n:02d}: 404")
                if consecutive_404s >= 3:
                    break  # stop after 3 consecutive 404s
            time.sleep(0.3)

        content = build_chapter_file(
            chapter_num, pali_name, en_name, slug, verse_range, stories)
        fname = f"{slug}_att.md"
        with open(os.path.join(OUTPUT_DIR, fname), "w", encoding="utf-8") as f:
            f.write(content + "\n")
        wc = len(content.split())
        print(f"  -> {fname}: {len(stories)} stories, {wc:,} words")
        all_chapters_data.append((chapter_num, pali_name, en_name, slug, verse_range, wc))

    update_index(all_chapters_data)
    print("\nDone.")


if __name__ == "__main__":
    main()
