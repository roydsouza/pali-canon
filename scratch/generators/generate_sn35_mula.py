#!/usr/bin/env python3
"""
SN 35 (Saḷāyatanasaṃyutta) mūla layer — selected suttas.
~30 key suttas covering: aniccā of sense bases, the All (Sabbam),
the Fire Sermon (Āditta), Gaddulabaddha, and closing liberation suttas.
"""

import os, json, re, time, urllib.request

VAULT    = os.environ.get("PALI_VAULT", "/Users/rds/pali_canon")
API_BASE = "https://suttacentral.net/api/bilarasuttas/{}/sujato"

SAMYUTTAS = [
    {
        "nikaya_dir":   "samyutta_nikaya",
        "slug":         "sn35",
        "sutta_code":   "SN35",
        "pali_title":   "Saḷāyatanasaṃyutta",
        "en_title":     "Linked Discourses on the Six Sense Bases",
        "nikaya_label": "Saṃyutta Nikāya",
        "num":          35,
        # Selected suttas: core aniccā/dukkha/anattā, the All, Fire Sermon,
        # key simile suttas, and liberation suttas.
        "sc_ids": (
            [f"sn35.{n}" for n in range(1, 11)] +    # sn35.1-10: aniccā of sense bases
            ["sn35.23", "sn35.28"] +                  # Sabba; Sabbam (the All defined)
            ["sn35.46"] +                             # Āditta (Fire Sermon)
            [f"sn35.{n}" for n in range(47, 56)] +   # sn35.47-55: burning group
            ["sn35.95"] +                             # Gaddulabaddha (dual tether)
            ["sn35.117", "sn35.118"] +               # Nakulapitu, Lohicca
            ["sn35.145"] +                            # Phassanānatta
            ["sn35.206", "sn35.207"] +               # Practice instruction
            ["sn35.246", "sn35.247"]                 # Final liberation suttas
        ),
        "tags": ["meditation", "six-sense-bases", "salayatana", "fire-sermon"],
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

    # SN has 3 metadata keys (:0.1, :0.2, :0.3); prefer :0.3 for sutta title
    sutta_en   = tr.get(f"{sc_id}:0.3", tr.get(f"{sc_id}:0.2", "")).strip()
    sutta_pali = root.get(f"{sc_id}:0.3", root.get(f"{sc_id}:0.2", "")).strip()
    if not sutta_pali:
        sutta_pali = root.get(f"{sc_id}:0.1", "").strip()

    # Parse display number e.g. "sn35.28" → "SN 35.28"
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
        f"**Mātikā**: [[five_spiritual_faculties|Five Spiritual Faculties]] · "
        f"[[dependent_origination|Dependent Origination]]",
        "",
        f"*Selected suttas ({selected_count} of 248): key teachings on the six sense "
        f"bases covering aniccā/dukkha/anattā of the āyatanā, the All (Sabbam), "
        f"the Fire Sermon (Ādittapariyāya), Gaddulabaddha, and liberation suttas.*",
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


def append_index(nikaya_dir, layer, slug, sutta_code, pali_title, wc):
    idx = os.path.join(VAULT, layer, "sutta", nikaya_dir, "Mula-Samyutta-Index.md")
    with open(idx, encoding="utf-8") as f:
        content = f.read()
    if slug in content:
        print(f"  (already in {layer} INDEX)")
        return
    row = f"| [[{slug}\|{sutta_code}]] | {pali_title} | {wc:,} |\n"
    with open(idx, "a", encoding="utf-8") as f:
        f.write(row)


def main():
    for s in SAMYUTTAS:
        slug         = s["slug"]
        sutta_code   = s["sutta_code"]
        pali_title   = s["pali_title"]
        nikaya_dir   = s["nikaya_dir"]
        sc_ids       = s["sc_ids"]

        print(f"\n{sutta_code}: {pali_title} ({len(sc_ids)} selected suttas)")
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
                print(f"SKIP: {e}")
            time.sleep(0.3)

        content = build_samyutta_file(s, sutta_blocks, len(sutta_blocks))
        out_dir = os.path.join(VAULT, "mula/sutta", nikaya_dir)
        fname   = f"{slug}.md"
        fpath   = os.path.join(out_dir, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(content + "\n")

        wc = len(content.split())
        print(f"  → {fname}: {wc:,} words ({len(sutta_blocks)} suttas)")
        append_index(nikaya_dir, "mula", slug, sutta_code, pali_title, wc)

    print("\nDone.")


if __name__ == "__main__":
    main()
