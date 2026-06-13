#!/usr/bin/env python3
"""
Phase 2 mūla: MN 36, 43, 44, 52, 111 and DN 22 from SuttaCentral (Sujato).
"""

import os, json, re, time, urllib.request

VAULT    = os.environ.get("PALI_VAULT", "/Users/rds/pali_canon")
API_BASE = "https://suttacentral.net/api/bilarasuttas/{}/sujato"

# (sc_id, nikaya_dir, slug, sutta_num, pali_title, en_title, nikaya_label, sutta_code)
SUTTAS = [
    ("mn36",  "majjhima_nikaya", "mn36",  36,  "Mahāsaccakasutta",
     "With Saccaka (the Longer)", "Majjhima Nikāya", "MN36"),
    ("mn43",  "majjhima_nikaya", "mn43",  43,  "Mahāvedallasutta",
     "The Longer Analysis",       "Majjhima Nikāya", "MN43"),
    ("mn44",  "majjhima_nikaya", "mn44",  44,  "Cūḷavedallasutta",
     "The Shorter Analysis",      "Majjhima Nikāya", "MN44"),
    ("mn52",  "majjhima_nikaya", "mn52",  52,  "Aṭṭhakanāgarasutta",
     "At Aṭṭhakanāgara",         "Majjhima Nikāya", "MN52"),
    ("mn111", "majjhima_nikaya", "mn111", 111, "Anupadasutta",
     "One by One",               "Majjhima Nikāya", "MN111"),
    ("dn22",  "digha_nikaya",    "dn22",  22,  "Mahāsatipaṭṭhānasutta",
     "The Longer Discourse on Mindfulness Meditation", "Dīgha Nikāya", "DN22"),
]

NIKAYA_META = {
    "majjhima_nikaya": {"label": "Majjhima Nikāya", "en_name": "Middle Discourses",
                        "nav_abbr": "majjhima"},
    "digha_nikaya":    {"label": "Dīgha Nikāya",    "en_name": "Long Discourses",
                        "nav_abbr": "digha"},
}

# ── helpers ───────────────────────────────────────────────────────────────────

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
    if m:
        return int(m.group(1))
    return None

def render_heading(level, pali, en):
    marker = "##" if level == 1 else "###"
    if en and pali:
        return f"{marker} {en}\n*{pali}*\n"
    return f"{marker} {en or pali}\n"

# ── sutta generation ──────────────────────────────────────────────────────────

def generate_sutta(sc_id, nikaya_dir, slug, num, pali_title, en_title,
                   nikaya_label, sutta_code, data):
    root = data["root_text"]
    tr   = data["translation_text"]
    keys = data["keys_order"]
    meta = NIKAYA_META[nikaya_dir]
    nav_link = f"[[mula/sutta/{nikaya_dir}/INDEX|{meta['label']}]]"

    # Commentary / tīkā backlinks (files will be created in later scripts)
    att_slug = f"{slug}_att"
    tik_slug = f"{slug}_tik"

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
        f"**Related Texts**: [[{att_slug}|Commentary (Atthakathā)]] | "
        f"[[{tik_slug}|Sub-commentary (Tīkā)]]",
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

# ── index management ──────────────────────────────────────────────────────────

def ensure_dirs(nikaya_dir):
    for layer in ("mula", "atthakatha", "tika"):
        path = os.path.join(VAULT, layer, "sutta", nikaya_dir)
        os.makedirs(path, exist_ok=True)
        idx = os.path.join(path, {"mula": "Mula-", "atthakatha": "Atthakatha-", "tika": "Tika-"}[layer] + {"digha_nikaya": "Digha", "majjhima_nikaya": "Majjhima", "samyutta_nikaya": "Samyutta", "anguttara_nikaya": "Anguttara", "khuddaka_nikaya": "Khuddaka"}[nikaya_dir] + "-Index.md")
        if not os.path.exists(idx):
            meta = NIKAYA_META[nikaya_dir]
            layer_cap = {"mula": "Mūla", "atthakatha": "Atthakathā", "tika": "Ṭīkā"}[layer]
            content = (
                f"---\ntype: index\npitaka: sutta\nnikaya: {meta['nav_abbr']}\n"
                f"layer: {layer}\n---\n\n"
                f"# {meta['label']} — {layer_cap}\n\n"
                f"**Navigation**: [[INDEX|Pali Canon Vault]] / "
                f"[[{layer}/INDEX|{layer_cap}]] / [[{layer}/sutta/INDEX|Sutta]]\n\n"
                f"## Migrated Texts\n\n| Sutta | Title | Words |\n|---|---|---|\n"
            )
            with open(idx, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  Created {layer}/sutta/{nikaya_dir}/INDEX.md")


def append_to_nikaya_index(nikaya_dir, layer, slug, sutta_code, pali_title, wc):
    idx = os.path.join(VAULT, layer, "sutta", nikaya_dir, {"mula": "Mula-", "atthakatha": "Atthakatha-", "tika": "Tika-"}[layer] + {"digha_nikaya": "Digha", "majjhima_nikaya": "Majjhima", "samyutta_nikaya": "Samyutta", "anguttara_nikaya": "Anguttara", "khuddaka_nikaya": "Khuddaka"}[nikaya_dir] + "-Index.md")
    with open(idx, encoding="utf-8") as f:
        content = f.read()
    # Don't double-add
    if slug in content:
        return
    row = f"| [[{slug}|{sutta_code}]] | {pali_title} | {wc:,} |\n"
    with open(idx, "a", encoding="utf-8") as f:
        f.write(row)

# ── main ──────────────────────────────────────────────────────────────────────

def main():
    for (sc_id, nikaya_dir, slug, num, pali_title, en_title,
         nikaya_label, sutta_code) in SUTTAS:

        print(f"\n{sutta_code}: {pali_title}")
        ensure_dirs(nikaya_dir)

        print(f"  Fetching SC API...", end=" ", flush=True)
        data = fetch(sc_id)
        print(f"{len(data['keys_order'])} segments")

        content = generate_sutta(
            sc_id, nikaya_dir, slug, num,
            pali_title, en_title, nikaya_label, sutta_code, data)

        out_dir = os.path.join(VAULT, "mula/sutta", nikaya_dir)
        fname   = f"{slug}.md"
        with open(os.path.join(out_dir, fname), "w", encoding="utf-8") as f:
            f.write(content + "\n")

        wc = len(content.split())
        print(f"  -> {fname}: {wc:,} words")
        append_to_nikaya_index(nikaya_dir, "mula", slug, sutta_code, pali_title, wc)
        time.sleep(0.4)

    print("\nDone.")

if __name__ == "__main__":
    main()
