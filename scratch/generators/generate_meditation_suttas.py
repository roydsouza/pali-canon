#!/usr/bin/env python3
"""
Fetch mūla for 6 key meditation suttas from SuttaCentral (Sujato translation).
Generates one interleaved Pali/English file per sutta in the appropriate
nikāya directory, creating directory scaffolding as needed.

Suttas:
  MN 10  — Satipaṭṭhānasutta
  MN 20  — Vitakkasaṇṭhānasutta
  MN 119 — Kāyagatāsatisutta
  MN 121 — Cūḷasuññatasutta
  DN 2   — Sāmaññaphalasutta
  AN 4.41— Samādhibhāvanāsutta
"""

import os, json, re, time, urllib.request

VAULT    = os.environ.get("PALI_VAULT", "/Users/rds/pali_canon")
API_BASE = "https://suttacentral.net/api/bilarasuttas/{}/sujato"

# (sc_id, nikaya_dir, slug, sutta_num, pali_title, en_title, nikaya_label, sutta_code)
SUTTAS = [
    ("mn10",   "majjhima_nikaya",  "mn10",   10,  "Satipaṭṭhānasutta",
        "Mindfulness Meditation",             "Majjhima Nikāya", "MN10"),
    ("mn20",   "majjhima_nikaya",  "mn20",   20,  "Vitakkasaṇṭhānasutta",
        "The Relaxation of Thoughts",         "Majjhima Nikāya", "MN20"),
    ("mn119",  "majjhima_nikaya",  "mn119",  119, "Kāyagatāsatisutta",
        "Mindfulness of the Body",            "Majjhima Nikāya", "MN119"),
    ("mn121",  "majjhima_nikaya",  "mn121",  121, "Cūḷasuññatasutta",
        "The Shorter Discourse on Emptiness", "Majjhima Nikāya", "MN121"),
    ("dn2",    "digha_nikaya",     "dn2",    2,   "Sāmaññaphalasutta",
        "The Fruits of the Ascetic Life",     "Dīgha Nikāya",    "DN2"),
    ("an4.41", "anguttara_nikaya", "an4_41", "4.41", "Samādhibhāvanāsutta",
        "Four Developments of Immersion",     "Aṅguttara Nikāya","AN4.41"),
]

NIKAYA_META = {
    "majjhima_nikaya": {
        "label":    "Majjhima Nikāya",
        "en_name":  "Middle Discourses",
        "nav_abbr": "majjhima",
    },
    "digha_nikaya": {
        "label":    "Dīgha Nikāya",
        "en_name":  "Long Discourses",
        "nav_abbr": "digha",
    },
    "anguttara_nikaya": {
        "label":    "Aṅguttara Nikāya",
        "en_name":  "Numbered Discourses",
        "nav_abbr": "anguttara",
    },
}

INDEX_TEMPLATES = {
    "digha_nikaya": """\
---
type: index
pitaka: sutta
nikaya: digha
---

# Dīgha Nikāya — Mūla

**Navigation**: [[INDEX|Pali Canon Vault]] / [[mula/Mula-Index|Mūla]] / [[mula/sutta/Mula-Sutta-Index|Sutta]]

The Dīgha Nikāya ("Long Discourses") contains 34 suttas, covering a wide range of topics including cosmology, ethics, meditation, and the gradual training.

## Migrated Suttas

| Sutta | Title | Description |
|---|---|---|
""",
    "anguttara_nikaya": """\
---
type: index
pitaka: sutta
nikaya: anguttara
---

# Aṅguttara Nikāya — Mūla

**Navigation**: [[INDEX|Pali Canon Vault]] / [[mula/Mula-Index|Mūla]] / [[mula/sutta/Mula-Sutta-Index|Sutta]]

The Aṅguttara Nikāya ("Numbered Discourses") organizes teachings by numerical lists, from ones to elevens.

## Migrated Suttas

| Sutta | Title | Description |
|---|---|---|
""",
}


def fetch(sc_id):
    url = API_BASE.format(sc_id)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def is_meta(key):
    """Collection/title header keys: {id}:0.N"""
    return bool(re.search(r':0\.\d+$', key))


def heading_level(key):
    """
    Returns 1 for a ## section heading, 2 for a ### sub-heading, or None.
      N.0       → level 1  (DN-style: dn2:1.0)
      N.0.1     → level 1  (MN-style: mn10:4.0.1)
      N.0.2     → level 2  (MN-style: mn10:4.0.2)
    """
    if re.search(r':\d+\.0$', key):
        return 1
    m = re.search(r':\d+\.0\.(\d+)$', key)
    if m:
        return int(m.group(1))
    return None


def render_heading(level, pali, en):
    marker = "##" if level == 1 else "###"
    if en and pali:
        return f"{marker} {en}\n*{pali}*\n"
    return f"{marker} {en or pali}\n"


def generate_sutta(sc_id, nikaya_dir, slug, num, pali_title, en_title,
                   nikaya_label, sutta_code, data):
    root = data["root_text"]
    tr   = data["translation_text"]
    keys = data["keys_order"]

    meta = NIKAYA_META[nikaya_dir]
    nav_link = f"[[mula/sutta/{nikaya_dir}/INDEX|{meta['label']}]]"

    lines = [
        "---",
        f"id: {sutta_code}",
        f"title_pali: {pali_title}",
        f"title_en: {en_title}",
        "type: mula",
        "pitaka: sutta",
        f"nikaya: {meta['nav_abbr']}",
        f"sutta_number: {sc_id}",
        "translator: Bhikkhu Sujato",
        "source: https://suttacentral.net",
        "tags:",
        "  - meditation",
        "---",
        "",
        f"# {nikaya_label} {num}: {pali_title}",
        "",
        "**Navigation**: [[INDEX|Pali Canon Vault]] / [[mula/Mula-Index|Mūla]] / "
        f"[[mula/sutta/Mula-Sutta-Index|Sutta]] / {nav_link}",
        "",
        f"## {pali_title}",
        f"*{en_title}*",
        "",
    ]

    for key in keys:
        if is_meta(key):
            continue

        p = root.get(key, "").strip()
        e = tr.get(key,   "").strip()

        if not p and not e:
            continue

        level = heading_level(key)
        if level is not None:
            lines.append(render_heading(level, p, e))
        else:
            if p and e:
                lines.append(f"**{p}**  ")
                lines.append(f"*{e}*")
            elif p:
                lines.append(f"*{p}*")
            else:
                lines.append(f"*{e}*")
            lines.append("")

    return "\n".join(lines)


def ensure_nikaya_dirs(nikaya_dir):
    for layer in ("mula", "atthakatha", "tika"):
        path = os.path.join(VAULT, layer, "sutta", nikaya_dir)
        os.makedirs(path, exist_ok=True)
        idx = os.path.join(path, {"digha_nikaya": "Mula-Digha-Index.md", "majjhima_nikaya": "Mula-Majjhima-Index.md", "samyutta_nikaya": "Mula-Samyutta-Index.md", "anguttara_nikaya": "Mula-Anguttara-Index.md", "khuddaka_nikaya": "Mula-Khuddaka-Index.md"}[nikaya_dir])
        if not os.path.exists(idx):
            if layer == "mula" and nikaya_dir in INDEX_TEMPLATES:
                with open(idx, "w", encoding="utf-8") as f:
                    f.write(INDEX_TEMPLATES[nikaya_dir])
                print(f"  Created {layer}/sutta/{nikaya_dir}/INDEX.md")
            elif layer != "mula":
                meta = NIKAYA_META[nikaya_dir]
                content = (
                    f"---\ntype: index\npitaka: sutta\nnikaya: {meta['nav_abbr']}\n"
                    f"layer: {layer}\n---\n\n"
                    f"# {meta['label']} — {layer.capitalize()}\n\n"
                    f"**Navigation**: [[INDEX|Pali Canon Vault]] / "
                    f"[[{layer}/INDEX|{layer.capitalize()}]] / "
                    f"[[{layer}/sutta/INDEX|Sutta]]\n\n"
                    f"## Migrated Texts\n\n*None yet.*\n"
                )
                with open(idx, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"  Created {layer}/sutta/{nikaya_dir}/INDEX.md")


def update_mula_sutta_index(results_by_nikaya):
    """Append new sutta entries to mula/sutta/INDEX.md."""
    idx_path = os.path.join(VAULT, "mula/sutta/Mula-Sutta-Index.md")
    if not os.path.exists(idx_path):
        return
    with open(idx_path, encoding="utf-8") as f:
        content = f.read()

    # Check if DN / AN headings need adding
    if "Dīgha Nikāya" not in content:
        content = content.rstrip() + "\n\n## Dīgha Nikāya\n\n" \
            "| Sutta | Title | Description |\n|---|---|---|\n"
    if "Aṅguttara Nikāya" not in content:
        content = content.rstrip() + "\n\n## Aṅguttara Nikāya\n\n" \
            "| Sutta | Title | Description |\n|---|---|---|\n"

    with open(idx_path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    results_by_nikaya = {}

    for (sc_id, nikaya_dir, slug, num, pali_title, en_title,
         nikaya_label, sutta_code) in SUTTAS:

        print(f"\n{sutta_code}: {pali_title}")
        ensure_nikaya_dirs(nikaya_dir)

        print(f"  Fetching {sc_id}...", end=" ", flush=True)
        data = fetch(sc_id)
        print(f"{len(data['keys_order'])} segments")

        content = generate_sutta(
            sc_id, nikaya_dir, slug, num,
            pali_title, en_title, nikaya_label, sutta_code, data
        )

        out_dir = os.path.join(VAULT, "mula/sutta", nikaya_dir)
        fname   = f"{slug}.md"
        with open(os.path.join(out_dir, fname), "w", encoding="utf-8") as f:
            f.write(content + "\n")

        wc = len(content.split())
        print(f"  -> {fname}: {wc:,} words")
        results_by_nikaya.setdefault(nikaya_dir, []).append(
            (slug, sutta_code, pali_title, en_title, wc)
        )
        time.sleep(0.4)

    update_mula_sutta_index(results_by_nikaya)
    print("\nDone. Remember to update nikāya INDEX.md files with new sutta entries.")


if __name__ == "__main__":
    main()
