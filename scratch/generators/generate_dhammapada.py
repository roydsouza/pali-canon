#!/usr/bin/env python3
"""
Fetch all 26 Dhammapada vaggas from SuttaCentral (Sujato translation)
and generate one interleaved mula file per vagga.
"""

import os, json, re, time, urllib.request

VAULT       = os.environ.get("PALI_VAULT", "/Users/rds/pali_canon")
OUTPUT_DIR  = os.path.join(VAULT, "mula/sutta/khuddaka_nikaya/dhammapada")
API_BASE    = "https://suttacentral.net/api/bilarasuttas/{}/sujato"

VAGGAS = [
    ("dhp1-20",    1,  "Yamakavagga",      "Pairs",          "dhp_01_yamakavagga",      1,   20),
    ("dhp21-32",   2,  "Appamādavagga",    "Heedfulness",    "dhp_02_appamadavagga",    21,  32),
    ("dhp33-43",   3,  "Cittavagga",       "The Mind",       "dhp_03_cittavagga",       33,  43),
    ("dhp44-59",   4,  "Pupphavagga",      "Flowers",        "dhp_04_pupphavagga",      44,  59),
    ("dhp60-75",   5,  "Bālavagga",        "The Fool",       "dhp_05_balavagga",        60,  75),
    ("dhp76-89",   6,  "Paṇḍitavagga",     "The Wise",       "dhp_06_panditavagga",     76,  89),
    ("dhp90-99",   7,  "Arahantavagga",    "The Arahant",    "dhp_07_arahantavagga",    90,  99),
    ("dhp100-115", 8,  "Sahassavagga",     "Thousands",      "dhp_08_sahassavagga",     100, 115),
    ("dhp116-128", 9,  "Pāpavagga",        "Evil",           "dhp_09_papavagga",        116, 128),
    ("dhp129-145", 10, "Daṇḍavagga",       "The Rod",        "dhp_10_dandavagga",       129, 145),
    ("dhp146-156", 11, "Jarāvagga",        "Old Age",        "dhp_11_jaravagga",        146, 156),
    ("dhp157-166", 12, "Attavagga",        "The Self",       "dhp_12_attavagga",        157, 166),
    ("dhp167-178", 13, "Lokavagga",        "The World",      "dhp_13_lokavagga",        167, 178),
    ("dhp179-196", 14, "Buddhavagga",      "The Buddha",     "dhp_14_buddhavagga",      179, 196),
    ("dhp197-208", 15, "Sukhavagga",       "Happiness",      "dhp_15_sukhavagga",       197, 208),
    ("dhp209-220", 16, "Piyavagga",        "Affection",      "dhp_16_piyavagga",        209, 220),
    ("dhp221-234", 17, "Kodhavagga",       "Anger",          "dhp_17_kodhavagga",       221, 234),
    ("dhp235-255", 18, "Malavagga",        "Impurity",       "dhp_18_malavagga",        235, 255),
    ("dhp256-272", 19, "Dhammaṭṭhavagga",  "The Just",       "dhp_19_dhammatthavagga",  256, 272),
    ("dhp273-289", 20, "Maggavagga",       "The Path",       "dhp_20_maggavagga",       273, 289),
    ("dhp290-305", 21, "Pakiṇṇakavagga",   "Miscellaneous",  "dhp_21_pakinnakavagga",   290, 305),
    ("dhp306-319", 22, "Nirayavagga",      "Hell",           "dhp_22_nirayavagga",      306, 319),
    ("dhp320-333", 23, "Nāgavagga",        "The Elephant",   "dhp_23_nagavagga",        320, 333),
    ("dhp334-359", 24, "Taṇhāvagga",       "Craving",        "dhp_24_tanhavagga",       334, 359),
    ("dhp360-382", 25, "Bhikkhuvagga",     "The Monk",       "dhp_25_bhikkhuvagga",     360, 382),
    ("dhp383-423", 26, "Brāhmaṇavagga",    "The Brahmin",    "dhp_26_brahmanavagga",    383, 423),
]

# Chapters most relevant to meditation — get extra tag
MEDITATION_VAGGAS = {2, 3, 7, 14, 20, 25}
# Chapters most relevant to precepts / ethics
PRECEPTS_VAGGAS   = {1, 9, 10, 17, 18, 19}

def fetch(sc_id):
    url = API_BASE.format(sc_id)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def verse_num(key):
    m = re.match(r"dhp(\d+):", key)
    return int(m.group(1)) if m else None

def is_collection_header(key):
    return bool(re.search(r":0\.[123]$", key))

def is_vatthu(key):
    return bool(re.search(r":0(\.4)?$", key))

def is_verse_line(key):
    m = re.search(r":(\d+)$", key)
    return bool(m and int(m.group(1)) >= 1)

def build_verse_block(vnum, vatthu, lines):
    out = []
    if vatthu:
        out.append(f"### {vnum}. *{vatthu}*")
    else:
        out.append(f"### {vnum}.")
    out.append("")
    for pali, en in lines:
        if pali:
            out.append(f"**{pali}**  ")
        if en:
            out.append(f"*{en}*")
    out.append("")
    return out

def generate(sc_id, num, pali_name, en_name, slug, v_start, v_end, data):
    root = data["root_text"]
    tr   = data["translation_text"]
    keys = data["keys_order"]

    tags = ["dhammapada"]
    if num in MEDITATION_VAGGAS: tags.append("meditation")
    if num in PRECEPTS_VAGGAS:   tags.append("precepts")
    tag_lines = "\n".join(f"  - {t}" for t in tags)

    lines = [
        "---",
        f"id: DHP_{num:02d}",
        f"title_pali: {pali_name}",
        f"title_en: {en_name}",
        "type: mula",
        "pitaka: sutta",
        "nikaya: khuddaka",
        "text: dhammapada",
        f"vagga: {num}",
        f'verse_range: "{v_start}–{v_end}"',
        "tags:",
        tag_lines,
        "---",
        "",
        f"# Dhammapada — Chapter {num}: {pali_name}",
        "",
        "**Navigation**: [[INDEX|Pali Canon Vault]] / [[mula/Mula-Index|Mūla]] / "
        "[[mula/sutta/Mula-Sutta-Index|Sutta]] / "
        "[[mula/sutta/khuddaka_nikaya/Mula-Khuddaka-Index|Khuddaka Nikāya]] / "
        "[[mula/sutta/khuddaka_nikaya/dhammapada/Mula-Dhammapada-Index|Dhammapada]]",
        "",
        f"## {pali_name} — {en_name}",
        f"*Verses {v_start}–{v_end}*",
        "",
    ]

    cur_vnum    = None
    cur_vatthu  = None
    cur_lines   = []

    for key in keys:
        if is_collection_header(key):
            continue

        vn = verse_num(key)
        if vn != cur_vnum:
            if cur_vnum is not None:
                lines.extend(build_verse_block(cur_vnum, cur_vatthu, cur_lines))
            cur_vnum   = vn
            cur_vatthu = None
            cur_lines  = []

        if is_vatthu(key):
            t = root.get(key, "").strip()
            if t:
                cur_vatthu = t
        elif is_verse_line(key):
            p = root.get(key, "").strip()
            e = tr.get(key, "").strip()
            if p or e:
                cur_lines.append((p, e))

    if cur_vnum is not None:
        lines.extend(build_verse_block(cur_vnum, cur_vatthu, cur_lines))

    content = "\n".join(lines)
    return f"{slug}.md", content

def build_index(results):
    rows = []
    for slug, num, pali_name, en_name, v_start, v_end, wc in results:
        rows.append(f"| [[{slug}\\|{num}. {pali_name}]] | {en_name} | {v_start}–{v_end} | {v_end - v_start + 1} |")

    return f"""---
type: index
pitaka: sutta
nikaya: khuddaka
text: dhammapada
---

# Dhammapada (Dhammapadapāḷi)

**Navigation**: [[INDEX|Pali Canon Vault]] / [[mula/Mula-Index|Mūla]] / [[mula/sutta/Mula-Sutta-Index|Sutta]] / [[mula/sutta/khuddaka_nikaya/Mula-Khuddaka-Index|Khuddaka Nikāya]]

The Dhammapada ("Sayings of the Dhamma") is a collection of 423 verses in 26 chapters, drawn from various parts of the Sutta Piṭaka. It is one of the most widely read texts in the Theravāda canon.

**Translation**: Bhikkhu Sujato (SuttaCentral)

## Chapters (Vaggas)

| Chapter | English | Verses | Count |
|---|---|---|---|
{chr(10).join(rows)}

## Meditation-Focused Chapters

- [[dhp_02_appamadavagga|2. Appamādavagga — Heedfulness]]
- [[dhp_03_cittavagga|3. Cittavagga — The Mind]]
- [[dhp_07_arahantavagga|7. Arahantavagga — The Arahant]]
- [[dhp_14_buddhavagga|14. Buddhavagga — The Buddha]]
- [[dhp_20_maggavagga|20. Maggavagga — The Path]]
- [[dhp_25_bhikkhuvagga|25. Bhikkhuvagga — The Monk]]

## Precepts-Focused Chapters

- [[dhp_01_yamakavagga|1. Yamakavagga — Pairs]]
- [[dhp_09_papavagga|9. Pāpavagga — Evil]]
- [[dhp_10_dandavagga|10. Daṇḍavagga — The Rod]]
- [[dhp_17_kodhavagga|17. Kodhavagga — Anger]]
- [[dhp_18_malavagga|18. Malavagga — Impurity]]
- [[dhp_19_dhammatthavagga|19. Dhammaṭṭhavagga — The Just]]
"""

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    results = []
    total_words = 0

    for sc_id, num, pali_name, en_name, slug, v_start, v_end in VAGGAS:
        print(f"  Fetching {sc_id} ({pali_name})...", end=" ", flush=True)
        data     = fetch(sc_id)
        fname, content = generate(sc_id, num, pali_name, en_name, slug, v_start, v_end, data)
        wc       = len(content.split())
        total_words += wc
        path     = os.path.join(OUTPUT_DIR, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content + "\n")
        print(f"{v_end - v_start + 1} verses, {wc} words")
        results.append((slug, num, pali_name, en_name, v_start, v_end, wc))
        time.sleep(0.4)

    index = build_index(results)
    with open(os.path.join(OUTPUT_DIR, "Mula-Dhammapada-Index.md"), "w", encoding="utf-8") as f:
        f.write(index)

    print(f"\nDone. 26 vaggas, 423 verses, ~{total_words:,} words total.")
    print(f"Output: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
