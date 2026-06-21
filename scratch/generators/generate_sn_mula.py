#!/usr/bin/env python3
"""
SN 46 (Bojjhaṅgasaṃyutta, 56 suttas) and SN 54 (Ānāpānasaṃyutta, 20 suttas)
mūla layer — Bhikkhu Sujato translation from SuttaCentral.

Each saṃyutta becomes one combined file (sn46.md / sn54.md) with each
individual sutta as a ## heading section.
"""

import os, json, re, time, urllib.request

VAULT    = os.environ.get("PALI_VAULT", "/Users/rds/pali_canon")
API_BASE = "https://suttacentral.net/api/bilarasuttas/{}/sujato"

SAMYUTTAS = [
    {
        "nikaya_dir":   "samyutta_nikaya",
        "slug":         "sn1",
        "sutta_code":   "SN1",
        "pali_title":   "Devatāsaṃyutta",
        "en_title":     "Linked Discourses with Devas",
        "nikaya_label": "Saṃyutta Nikāya",
        "num":          1,
        "sc_ids":       [f"sn1.{n}" for n in range(1, 82)],   # sn1.1–81
        "tags":         ["devata", "deva", "verse"],
    },
    {
        "nikaya_dir":   "samyutta_nikaya",
        "slug":         "sn46",
        "sutta_code":   "SN46",
        "pali_title":   "Bojjhaṅgasaṃyutta",
        "en_title":     "Linked Discourses on the Awakening Factors",
        "nikaya_label": "Saṃyutta Nikāya",
        "num":          46,
        "sc_ids":       [f"sn46.{n}" for n in range(1, 57)],   # sn46.1–56
        "tags":         ["meditation", "bojjhanga", "awakening-factors"],
    },
    {
        "nikaya_dir":   "samyutta_nikaya",
        "slug":         "sn54",
        "sutta_code":   "SN54",
        "pali_title":   "Ānāpānasaṃyutta",
        "en_title":     "Linked Discourses on Mindfulness of Breathing",
        "nikaya_label": "Saṃyutta Nikāya",
        "num":          54,
        "sc_ids":       [f"sn54.{n}" for n in range(1, 21)],   # sn54.1–20
        "tags":         ["meditation", "anapanasati", "breathing"],
    },
]

NIKAYA_META = {
    "samyutta_nikaya": {
        "label":    "Saṃyutta Nikāya",
        "en_name":  "Linked Discourses",
        "nav_abbr": "samyutta",
    },
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

    # Extract sutta number and titles from metadata keys
    sutta_en    = tr.get(f"{sc_id}:0.2", "").strip()
    sutta_pali  = root.get(f"{sc_id}:0.2", "").strip()
    if not sutta_pali:
        sutta_pali = root.get(f"{sc_id}:0.1", "").strip()

    # Parse sutta number from sc_id e.g. "sn46.3" → "3"
    n = sc_id.split(".")[-1]
    samyutta = sc_id.split(".")[0].upper()   # "SN46"
    display_num = f"{samyutta.replace('SN','SN ')}.{n}"   # "SN 46.3"

    lines = [f"## {display_num}: {sutta_pali} — *{sutta_en}*", ""]

    # Collect comment keys for footnote rendering
    comment_keys = sorted(comments.keys()) if comments else []
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

    # Append footnotes
    if note_index:
        lines.append("")
        for idx, (key, text) in sorted(note_index.items()):
            fn_key = f"{sc_id.replace('.','_')}_{idx}"
            lines.append(f"[^{fn_key}]: **Note ({key})**: {text}")
        lines.append("")

    return "\n".join(lines)


def build_samyutta_file(s, sutta_blocks):
    slug        = s["slug"]
    sutta_code  = s["sutta_code"]
    pali_title  = s["pali_title"]
    en_title    = s["en_title"]
    nikaya_label = s["nikaya_label"]
    nikaya_dir  = s["nikaya_dir"]
    tags        = s["tags"]

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
        "",
        "---",
        "",
    ])

    return header + "\n\n".join(sutta_blocks)


def ensure_dirs(nikaya_dir):
    meta = NIKAYA_META[nikaya_dir]
    for layer in ("mula", "atthakatha", "tika"):
        path = os.path.join(VAULT, layer, "sutta", nikaya_dir)
        os.makedirs(path, exist_ok=True)
        idx = os.path.join(path, {"mula": "Mula-Samyutta-Index.md", "atthakatha": "Atthakatha-Samyutta-Index.md", "tika": "Tika-Samyutta-Index.md"}[layer])
        if not os.path.exists(idx):
            layer_cap = {"mula": "Mūla", "atthakatha": "Atthakathā", "tika": "Ṭīkā"}[layer]
            content = (
                f"---\ntype: index\npitaka: sutta\nnikaya: {meta['nav_abbr']}\n"
                f"layer: {layer}\n---\n\n"
                f"# {meta['label']} — {layer_cap}\n\n"
                "**Navigation**: [[INDEX|Pali Canon Vault]] / "
                f"[[{layer}/INDEX|{layer_cap}]] / [[{layer}/sutta/INDEX|Sutta]]\n\n"
                "## Migrated Texts\n\n| Sutta | Title | Words |\n|---|---|---|\n"
            )
            with open(idx, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  Created {layer}/sutta/{nikaya_dir}/INDEX.md")


def append_index(nikaya_dir, layer, slug, sutta_code, pali_title, wc):
    idx = os.path.join(VAULT, layer, "sutta", nikaya_dir, {"mula": "Mula-Samyutta-Index.md", "atthakatha": "Atthakatha-Samyutta-Index.md", "tika": "Tika-Samyutta-Index.md"}[layer])
    with open(idx, encoding="utf-8") as f:
        content = f.read()
    if slug in content:
        return
    row = f"| [[{slug}\\|{sutta_code}]] | {pali_title} | {wc:,} |\n"
    with open(idx, "a", encoding="utf-8") as f:
        f.write(row)


def main():
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else None
    for s in SAMYUTTAS:
        slug         = s["slug"]
        if target and slug != target:
            continue
        sutta_code   = s["sutta_code"]
        pali_title   = s["pali_title"]
        nikaya_dir   = s["nikaya_dir"]
        sc_ids       = s["sc_ids"]

        print(f"\n{sutta_code}: {pali_title} ({len(sc_ids)} suttas)")
        ensure_dirs(nikaya_dir)

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
                print(f"ERROR: {e}")
                sutta_blocks.append(f"## {sc_id.upper()}\n\n*Error fetching: {e}*\n")
            time.sleep(0.3)

        content = build_samyutta_file(s, sutta_blocks)
        out_dir = os.path.join(VAULT, "mula/sutta", nikaya_dir)
        fname   = f"{slug}.md"
        fpath   = os.path.join(out_dir, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content + "\n")

        wc = len(content.split())
        print(f"  → {fname}: {wc:,} words")
        append_index(nikaya_dir, "mula", slug, sutta_code, pali_title, wc)

    print("\nDone.")


if __name__ == "__main__":
    main()
