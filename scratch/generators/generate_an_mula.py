#!/usr/bin/env python3
"""
AN batch mūla — five entries from SuttaCentral (Bhikkhu Sujato):
  AN 3.100  Loṇakapallasutta      (single sutta)
  AN 4.123–126 Nānākaraṇasuttāni (4 suttas grouped)
  AN 5.28   Pañcaṅgikasutta       (single sutta)
  AN 9.36   Jhānasutta            (single sutta)
  AN 10.2–6 Ānisaṃsasuttāni       (5 suttas grouped)
"""

import os, json, re, time, urllib.request

VAULT    = os.environ.get("PALI_VAULT", "/Users/rds/pali_canon")
API_BASE = "https://suttacentral.net/api/bilarasuttas/{}/sujato"

# Each entry: sc_ids list, slug, display label, pali_title, en_title, tags
ENTRIES = [
    {
        "sc_ids":       ["an3.100"],
        "slug":         "an3_100",
        "display":      "AN 3.100",
        "pali_title":   "Loṇakapallasutta",
        "en_title":     "A Lump of Salt",
        "tags":         ["meditation", "kamma", "purification"],
    },
    {
        "sc_ids":       ["an4.123", "an4.124", "an4.125", "an4.126"],
        "slug":         "an4_123_126",
        "display":      "AN 4.123–126",
        "pali_title":   "Nānākaraṇasuttāni",
        "en_title":     "Differences (AN 4.123–126)",
        "tags":         ["meditation", "samadhi", "absorption", "rebirth"],
    },
    {
        "sc_ids":       ["an5.28"],
        "slug":         "an5_28",
        "display":      "AN 5.28",
        "pali_title":   "Pañcaṅgikasutta",
        "en_title":     "With Five Factors",
        "tags":         ["meditation", "samadhi", "jhana"],
    },
    {
        "sc_ids":       ["an9.36"],
        "slug":         "an9_36",
        "display":      "AN 9.36",
        "pali_title":   "Jhānasutta",
        "en_title":     "Depending on Absorption",
        "tags":         ["meditation", "jhana", "samadhi", "defilements"],
    },
    {
        "sc_ids":       ["an10.2", "an10.3", "an10.4", "an10.5", "an10.6"],
        "slug":         "an10_2_6",
        "display":      "AN 10.2–6",
        "pali_title":   "Ānisaṃsasuttāni",
        "en_title":     "Benefits (AN 10.2–6)",
        "tags":         ["meditation", "ethics", "samadhi", "progressive-path"],
    },
]

NIKAYA_DIR   = "anguttara_nikaya"
NIKAYA_LABEL = "Aṅguttara Nikāya"


def fetch(sc_id):
    url = API_BASE.format(sc_id)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def is_meta(key):
    return bool(re.search(r':0\.\d+$', key))


def heading_level(key):
    if re.search(r':\d+\.0$', key):
        return 1
    m = re.search(r':\d+\.0\.(\d+)$', key)
    return int(m.group(1)) if m else None


def render_sutta_block(sc_id, data):
    root  = data["root_text"]
    tr    = data["translation_text"]
    keys  = data["keys_order"]

    # :0.1 = nikāya label, :0.2 = vagga name, :0.3 = sutta title (AN has 3 header keys)
    en_title   = tr.get(f"{sc_id}:0.3", "").strip() or tr.get(f"{sc_id}:0.2", "").strip()
    pali_title = root.get(f"{sc_id}:0.3", "").strip() or root.get(f"{sc_id}:0.2", "").strip()
    n = sc_id.split(".")[-1]
    nipata = sc_id.split(".")[0].upper().replace("AN", "AN ")

    lines = [f"## {nipata}.{n}: {pali_title} — *{en_title}*", ""]

    for key in keys:
        if is_meta(key):
            continue
        p = root.get(key, "").strip()
        e = tr.get(key,   "").strip()
        if not p and not e:
            continue
        level = heading_level(key)
        if level is not None:
            marker = "###" if level == 1 else "####"
            if e and p:
                lines.append(f"{marker} {e}")
                lines.append(f"*{p}*")
            else:
                lines.append(f"{marker} {e or p}")
            lines.append("")
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


def build_file(entry, sutta_blocks):
    slug        = entry["slug"]
    display     = entry["display"]
    pali_title  = entry["pali_title"]
    en_title    = entry["en_title"]
    tags        = entry["tags"]
    sutta_id    = display.replace(" ", "").replace("–", "-")

    att_slug = f"{slug}_att"
    tik_slug = f"{slug}_tik"
    tag_lines = "\n".join(f"  - {t}" for t in tags)

    header = "\n".join([
        "---",
        f"id: {sutta_id}",
        f"title_pali: {pali_title}",
        f"title_en: {en_title}",
        "type: mula",
        "pitaka: sutta",
        "nikaya: anguttara",
        f"sutta_number: {entry['sc_ids'][0]}",
        "translator: Bhikkhu Sujato",
        "source: https://suttacentral.net",
        "tags:",
        tag_lines,
        "---",
        "",
        f"# {NIKAYA_LABEL}: {pali_title}",
        f"*{en_title}*",
        "",
        f"**Navigation**: [[INDEX|Pali Canon Vault]] / [[mula/Mula-Index|Mūla]] / "
        f"[[mula/sutta/Mula-Sutta-Index|Sutta]] / [[mula/sutta/{NIKAYA_DIR}/INDEX|{NIKAYA_LABEL}]]",
        f"**Related Texts**: [[{att_slug}|Commentary (Atthakathā)]] | "
        f"[[{tik_slug}|Sub-commentary (Tīkā)]]",
        "",
        "---",
        "",
    ])

    return header + "\n\n".join(sutta_blocks)


def append_index(slug, display, pali_title, wc):
    idx = os.path.join(VAULT, "mula/sutta", NIKAYA_DIR, "Mula-Anguttara-Index.md")
    with open(idx, encoding="utf-8") as f:
        content = f.read()
    if slug in content:
        return
    row = f"| [[{slug}\\|{display}]] | {pali_title} | {wc:,} |\n"
    with open(idx, "a", encoding="utf-8") as f:
        f.write(row)


def main():
    out_dir = os.path.join(VAULT, "mula/sutta", NIKAYA_DIR)

    for entry in ENTRIES:
        slug    = entry["slug"]
        display = entry["display"]
        sc_ids  = entry["sc_ids"]
        print(f"\n{display}: {entry['pali_title']} ({len(sc_ids)} sutta(s))")

        sutta_blocks = []
        for sc_id in sc_ids:
            print(f"  {sc_id}...", end=" ", flush=True)
            try:
                data  = fetch(sc_id)
                block = render_sutta_block(sc_id, data)
                sutta_blocks.append(block)
                print(f"{len(data['keys_order'])} segs")
            except Exception as e:
                print(f"ERROR: {e}")
                sutta_blocks.append(f"## {sc_id.upper()}\n\n*Error: {e}*\n")
            time.sleep(0.3)

        content = build_file(entry, sutta_blocks)
        fname   = f"{slug}.md"
        with open(os.path.join(out_dir, fname), "w", encoding="utf-8") as f:
            f.write(content + "\n")

        wc = len(content.split())
        print(f"  → {fname}: {wc:,} words")
        append_index(slug, display, entry["pali_title"], wc)

    print("\nDone.")


if __name__ == "__main__":
    main()
