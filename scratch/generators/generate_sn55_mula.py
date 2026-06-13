#!/usr/bin/env python3
"""
SN 55 (Sotāpattisaṃyutta) mūla layer — selected suttas.
15 key suttas on stream-entry.
"""

import os, json, re, time, urllib.request

VAULT    = os.environ.get("PALI_VAULT", "/Users/rds/pali_canon")
API_BASE = "https://suttacentral.net/api/bilarasuttas/{}/sujato"

SAMYUTTA = {
    "nikaya_dir":   "samyutta_nikaya",
    "slug":         "sn55",
    "sutta_code":   "SN55",
    "pali_title":   "Sotāpattisaṃyutta",
    "en_title":     "Linked Discourses on Stream-Entry",
    "nikaya_label": "Saṃyutta Nikāya",
    "num":          55,
    "sc_ids": [
        "sn55.1",   # Cakkavattisutta — The Wheel-Turning Monarch
        "sn55.2",   # Brahmacariyogadhasutta — Grounded in the Spiritual Life
        "sn55.3",   # Dīghāvuupāsakasutta — About Dīghāvu the Lay Follower
        "sn55.4",   # Paṭhamasāriputtasutta — With Sāriputta (1st)
        "sn55.5",   # Dutiyasāriputtasutta — With Sāriputta (2nd)
        "sn55.7",   # Veḷudvāreyyasutta — The People of Bamboo Gate
        "sn55.21",  # Paṭhamamahānāmasutta — With Mahānāma (1st)
        "sn55.22",  # Dutiyamahānāmasutta — With Mahānāma (2nd)
        "sn55.24",  # Paṭhamasaraṇānisakkasutta — About Saraṇāni (1st)
        "sn55.25",  # Dutiyasaraṇānisakkasutta — About Saraṇāni (2nd)
        "sn55.26",  # Paṭhamaanāthapiṇḍikasuttā — About Anāthapiṇḍika (1st)
        "sn55.37",  # Mahānāmasutta — With Mahānāma (on qualities of lay follower)
        "sn55.40",  # Nandiyasutta — With Nandiya
        "sn55.53",  # Dhammadinnasutta — With Dhammadinna
        "sn55.54",  # Gilānasutta — Sick (advice to a sick lay follower)
    ],
    "tags": ["stream-entry", "sotapatti", "faith", "refuge", "ethics"],
}

def fetch(sc_id):
    url = API_BASE.format(sc_id)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def fetch_comments(sc_id):
    url = API_BASE.format(sc_id) + "?comment=true"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.load(r)
        return data.get("comment", {})
    except Exception:
        return {}

def is_meta(key):
    return bool(re.search(r':0\.\d+$', key))

def heading_level(key):
    if re.search(r':\d+\.0$', key):
        return 1
    m = re.search(r':\d+\.0\.(\d+)$', key)
    if m:
        return int(m.group(1))
    return None

def render_sutta(sc_id, data, comments):
    root  = data["root_text"]
    tr    = data["translation_text"]
    keys  = data["keys_order"]

    sutta_en   = tr.get(f"{sc_id}:0.3", tr.get(f"{sc_id}:0.2", "")).strip()
    sutta_pali = root.get(f"{sc_id}:0.3", root.get(f"{sc_id}:0.2", "")).strip()
    if not sutta_pali:
        sutta_pali = root.get(f"{sc_id}:0.1", "").strip()

    parts = sc_id.split(".")
    display_num = f"SN {parts[0][2:]}.{parts[1]}"

    lines = [f"## {display_num}: {sutta_pali} — *{sutta_en}*", ""]

    note_index = {}
    note_counter = [0]

    def maybe_note(key):
        if key in comments:
            note_counter[0] += 1
            idx = note_counter[0]
            note_index[idx] = (key, comments[key])
            return f"[^{sc_id.replace('.','_')}_{idx}]"
        return ""

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
                lines.append("")
            else:
                lines.append(f"{marker} {e or p}")
                lines.append("")
        else:
            note = maybe_note(key)
            if p and e:
                lines.append(f"**{p}**{note}  ")
                lines.append(f"*{e}*")
            elif p:
                lines.append(f"*{p}*{note}")
            else:
                lines.append(f"*{e}*{note}")
            lines.append("")

    if note_index:
        lines.append("")
        for idx, (key, text) in sorted(note_index.items()):
            fn_key = f"{sc_id.replace('.','_')}_{idx}"
            lines.append(f"[^{fn_key}]: **Note ({key})**: {text}")
        lines.append("")

    return "\n".join(lines)

def build_samyutta_file(s, sutta_blocks, selected_count):
    slug         = s["slug"]
    sutta_code   = s["sutta_code"]
    pali_title   = s["pali_title"]
    en_title     = s["en_title"]
    nikaya_label = s["nikaya_label"]
    nikaya_dir   = s["nikaya_dir"]
    tags         = s["tags"]

    att_slug = f"{slug}_att"
    tik_slug = f"{slug}_tik"
    nav_link = f"[[mula/sutta/{nikaya_dir}/INDEX|{nikaya_label}]]"

    tag_lines = "\n".join(f"  - {t}" for t in tags)

    header = "\n".join([
        "---",
        f"id: {sutta_code}",
        f"title_pali: {pali_title}",
        f"title_en: {en_title}",
        "type: mula",
        "pitaka: sutta",
        "nikaya: samyutta",
        f"samyutta: {slug}",
        "translator: Bhikkhu Sujato",
        "source: https://suttacentral.net",
        "tags:",
        tag_lines,
        "---",
        "",
        f"# {nikaya_label}: {pali_title}",
        f"*{en_title}*",
        "",
        f"**Navigation**: [[INDEX|Pali Canon Vault]] / [[mula/Mula-Index|Mūla]] / "
        f"[[mula/sutta/Mula-Sutta-Index|Sutta]] / {nav_link}",
        f"**Related Texts**: [[{att_slug}|Commentary (Atthakathā)]] | "
        f"[[{tik_slug}|Sub-commentary (Tīkā)]]",
        f"**Mātikā**: [[three_refuges|Three Refuges]]",
        "",
        f"*Selected suttas ({selected_count} of 74): including Cakkavatti (sn55.1), "
        f"Brahmacariyogadha (sn55.2), Dīghāvu (sn55.3), Sāriputta (sn55.4-5), "
        f"Veḷudvāreyya (sn55.7), Mahānāma (sn55.21-22, 37), Saraṇāni (sn55.24-25), "
        f"Anāthapiṇḍika (sn55.26), Nandiya (sn55.40), Dhammadinna (sn55.53), and Gilāna (sn55.54).*",
        "",
        "---",
        "",
    ])

    return header + "\n\n".join(sutta_blocks)

def main():
    s = SAMYUTTA
    slug         = s["slug"]
    sutta_code   = s["sutta_code"]
    pali_title   = s["pali_title"]
    nikaya_dir   = s["nikaya_dir"]
    sc_ids       = s["sc_ids"]

    print(f"\n{sutta_code}: {pali_title} ({len(sc_ids)} selected suttas)")

    sutta_blocks = []
    for sc_id in sc_ids:
        print(f"  {sc_id}...", end=" ", flush=True)
        try:
            data     = fetch(sc_id)
            comments = fetch_comments(sc_id)
            block    = render_sutta(sc_id, data, comments)
            sutta_blocks.append(block)
            print(f"{len(data['keys_order'])} segs, {len(comments)} notes")
        except Exception as e:
            print(f"SKIP: {e}")
        time.sleep(0.3)

    content = build_samyutta_file(s, sutta_blocks, len(sutta_blocks))
    out_dir = os.path.join(VAULT, "mula/sutta", nikaya_dir)
    os.makedirs(out_dir, exist_ok=True)
    fname   = f"{slug}.md"
    with open(os.path.join(out_dir, fname), "w", encoding="utf-8") as f:
        f.write(content + "\n")

    wc = len(content.split())
    print(f"  → {fname}: {wc:,} words ({len(sutta_blocks)} suttas)")
    print("\nDone.")

if __name__ == "__main__":
    main()
