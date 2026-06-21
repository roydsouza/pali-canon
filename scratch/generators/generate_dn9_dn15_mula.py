#!/usr/bin/env python3
"""
Generate DN 9 (Poṭṭhapādasutta) and DN 15 (Mahānidānasutta) — mūla layer.
Fetches from SuttaCentral API (Sujato translation).
"""

import os, json, re, time, urllib.request

VAULT    = os.environ.get("PALI_VAULT", "/Users/rds/pali_canon")
API_BASE = "https://suttacentral.net/api/bilarasuttas/{}/sujato"

SUTTAS = [
    ("dn9",  "digha_nikaya", "dn9",  9,  "Poṭṭhapādasutta",
     "With Poṭṭhapāda", "Dīgha Nikāya", "DN9"),
    ("dn15", "digha_nikaya", "dn15", 15, "Mahānidānasutta",
     "The Great Discourse on Causation", "Dīgha Nikāya", "DN15"),
]

NIKAYA_META = {
    "digha_nikaya": {"label": "Dīgha Nikāya", "en_name": "Long Discourses",
                     "nav_abbr": "digha"},
}

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

def generate_sutta(sc_id, nikaya_dir, slug, num, pali_title, en_title,
                   nikaya_label, sutta_code, data):
    root = data["root_text"]
    tr   = data["translation_text"]
    keys = data["keys_order"]
    meta = NIKAYA_META[nikaya_dir]
    nav_link = f"[[mula/sutta/{nikaya_dir}/INDEX|{meta['label']}]]"
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


def append_to_nikaya_index(nikaya_dir, layer, slug, sutta_code, pali_title, wc):
    idx = os.path.join(VAULT, layer, "sutta", nikaya_dir, {"mula": "Mula-Digha-Index.md", "atthakatha": "Atthakatha-Digha-Index.md", "tika": "Tika-Digha-Index.md"}[layer])
    with open(idx, encoding="utf-8") as f:
        content = f.read()
    if slug in content:
        return
    row = f"| [[{slug}\\|{sutta_code}]] | {pali_title} | {wc:,} |\n"
    with open(idx, "a", encoding="utf-8") as f:
        f.write(row)

def main():
    for (sc_id, nikaya_dir, slug, num, pali_title, en_title,
         nikaya_label, sutta_code) in SUTTAS:

        print(f"\n{sutta_code}: {pali_title}")

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
