#!/usr/bin/env python3
"""
SN 46 (Bojjhaṅgasaṃyutta) and SN 54 (Ānāpānasaṃyutta) atthakathā layer
from CSCD (Sāratthappakāsinī).

  SN 46 att:  s0305a.att1.xml  (entire file = SN 46)
  SN 54 att:  s0305a.att9.xml  (entire file = SN 54)
"""

import os, re, time, html as hmod, urllib.request

VAULT    = os.environ.get("PALI_VAULT", "/Users/rds/pali_canon")
TIPITAKA = "https://tipitaka.org/romn/cscd/{}"

SAMYUTTAS = [
    {
        "slug":             "sn1",
        "sutta_code":       "SN1",
        "nikaya_dir":       "samyutta_nikaya",
        "pali_title":       "Devatāsaṃyutta",
        "en_title":         "Linked Discourses with Devas",
        "nikaya_label":     "Saṃyutta Nikāya",
        "commentary_name":  "Sāratthappakāsinī (Saṃyutta Nikāya Atthakathā)",
        "cscd_file":        "s0301a.att1.xml",
        "section_pattern":  None,
    },
    {
        "slug":             "sn46",
        "sutta_code":       "SN46",
        "nikaya_dir":       "samyutta_nikaya",
        "pali_title":       "Bojjhaṅgasaṃyutta",
        "en_title":         "Linked Discourses on the Awakening Factors",
        "nikaya_label":     "Saṃyutta Nikāya",
        "commentary_name":  "Sāratthappakāsinī (Saṃyutta Nikāya Atthakathā)",
        "cscd_file":        "s0305a.att1.xml",
        "section_pattern":  None,   # entire file = this saṃyutta
    },
    {
        "slug":             "sn54",
        "sutta_code":       "SN54",
        "nikaya_dir":       "samyutta_nikaya",
        "pali_title":       "Ānāpānasaṃyutta",
        "en_title":         "Linked Discourses on Mindfulness of Breathing",
        "nikaya_label":     "Saṃyutta Nikāya",
        "commentary_name":  "Sāratthappakāsinī (Saṃyutta Nikāya Atthakathā)",
        "cscd_file":        "s0305a.att9.xml",
        "section_pattern":  None,   # entire file = this saṃyutta
    },
]


def fetch_bytes(filename):
    req = urllib.request.Request(
        TIPITAKA.format(filename), headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def clean_xml(text):
    text = re.sub(r'<hi rend="bold">(.*?)</hi>', r'**\1**', text, flags=re.DOTALL)
    text = re.sub(r'<pb[^/]*/>', '', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = hmod.unescape(text)
    return re.sub(r'\s+', ' ', text).strip()


def load_cscd_paras(filename):
    raw = fetch_bytes(filename)
    try:    content = raw.decode('utf-16')
    except: content = raw.decode('utf-8', errors='replace')
    results = []
    for m in re.finditer(r'<p([^>]*)>(.*?)</p>', content, re.DOTALL):
        attrs  = m.group(1)
        body   = m.group(2)
        rend_m = re.search(r'rend="([^"]+)"', attrs)
        rend   = rend_m.group(1) if rend_m else ''
        pnum_m = re.search(r'<hi rend="paranum">\s*(\d+)\s*</hi>', body)
        paranum = pnum_m.group(1) if pnum_m else ''
        body   = re.sub(r'<hi rend="(?:paranum|dot)">[^<]*</hi>', '', body)
        text   = clean_xml(body)
        if text:
            results.append((rend, paranum, text))
    return results


def paras_to_markdown(paras):
    lines = []
    for rend, paranum, text in paras:
        if not text:
            continue
        if (re.match(r'^\d+\.\s+\S+vaggo', text, re.IGNORECASE) or
                re.match(r'^\d+\.\s+\S+vagga', text, re.IGNORECASE)):
            lines.append(f"## {text}\n")
        elif re.match(r'^\d+\.\s+\S+(?:vaṇṇanā|suttavaṇṇanā|ṭīkā)', text):
            lines.append(f"### {text}\n")
        elif rend in ('gatha', 'gathalast', 'indent'):
            lines.append(f"  {text}  ")
        else:
            prefix = f"({paranum}) " if paranum else ""
            lines.append(f"{prefix}{text}\n")
    return "\n".join(lines)


def build_att_file(s, pali_body, para_count):
    slug          = s["slug"]
    sutta_code    = s["sutta_code"]
    nikaya_dir    = s["nikaya_dir"]
    pali_title    = s["pali_title"]
    en_title      = s["en_title"]
    nikaya_label  = s["nikaya_label"]
    commentary    = s["commentary_name"]

    nav_link  = f"[[atthakatha/sutta/{nikaya_dir}/INDEX|{nikaya_label}]]"
    mula_link = f"[[{slug}|{pali_title} — {en_title}]]"
    tik_link  = f"[[{slug}_tik|{pali_title}vaṇṇanāṭīkā (Sub-commentary)]]"

    header = "\n".join([
        "---",
        f"id: {sutta_code}_att",
        f"title_pali: {pali_title}vaṇṇanā",
        f"title_en: Commentary on {pali_title}",
        "type: atthakatha",
        "pitaka: sutta",
        "nikaya: samyutta",
        f"samyutta: {slug}",
        f"mula_file: [[{slug}]]",
        f"tika_file: [[{slug}_tik]]",
        "source_pali: https://tipitaka.org/romn/cscd/ (CSCD)",
        "---",
        "",
        f"# Commentary on {nikaya_label}: {pali_title}",
        "",
        f"**Navigation**: [[INDEX|Pali Canon Vault]] / [[atthakatha/Atthakatha-Index|Atthakathā]] / "
        f"[[atthakatha/sutta/Atthakatha-Sutta-Index|Sutta]] / {nav_link}",
        f"**Mūla**: {mula_link}",
        f"**Tīkā**: {tik_link}",
        "",
        f"*{commentary}*",
        f"*{para_count} paragraphs — Pali text CSCD.*",
        "",
        f"## {pali_title}vaṇṇanā",
        "",
        "*Pali text — CSCD (Chattha Sangayana Tipitaka). "
        "Use Simsapa DPD for word lookups (double-click any Pali word).*",
        "",
    ])
    return header + "\n" + pali_body


def ensure_samyutta_index(nikaya_dir):
    meta = {
        "label": "Saṃyutta Nikāya", "en_name": "Linked Discourses",
        "nav_abbr": "samyutta",
    }
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
                "## Migrated Texts\n\n| Sutta | Commentary | Pali Source | Words |\n|---|---|---|---|\n"
            )
            with open(idx, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  Created {layer}/sutta/{nikaya_dir}/INDEX.md")


def append_index(nikaya_dir, slug, sutta_code, pali_title, wc):
    idx = os.path.join(VAULT, "atthakatha/sutta", nikaya_dir, "Atthakatha-Samyutta-Index.md")
    with open(idx, encoding="utf-8") as f:
        content = f.read()
    if f"{slug}_att" in content:
        return
    row = (f"| [[{slug}\\|{sutta_code}]] | "
           f"[[{slug}_att\\|{pali_title}vaṇṇanā]] | "
           f"tipitaka.org CSCD | {wc:,} |\n")
    with open(idx, "a", encoding="utf-8") as f:
        f.write(row)


def main():
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else None
    for s in SAMYUTTAS:
        slug       = s["slug"]
        if target and slug != target:
            continue
        sutta_code = s["sutta_code"]
        pali_title = s["pali_title"]
        nikaya_dir = s["nikaya_dir"]
        cscd_file  = s["cscd_file"]

        print(f"\n{sutta_code}: {pali_title}")
        ensure_samyutta_index(nikaya_dir)

        print(f"  Fetching {cscd_file}...", end=" ", flush=True)
        try:
            paras     = load_cscd_paras(cscd_file)
            pali_body = paras_to_markdown(paras)
            print(f"{len(paras)} paragraphs")
        except Exception as e:
            print(f"ERROR: {e}")
            pali_body  = f"*Error fetching Pali commentary: {e}*\n"
            paras      = []

        content = build_att_file(s, pali_body, len(paras))
        out_dir = os.path.join(VAULT, "atthakatha/sutta", nikaya_dir)
        fname   = f"{slug}_att.md"
        with open(os.path.join(out_dir, fname), "w", encoding="utf-8") as f:
            f.write(content + "\n")

        wc = len(content.split())
        print(f"  → {fname}: {wc:,} words")
        append_index(nikaya_dir, slug, sutta_code, pali_title, wc)
        time.sleep(1.0)

    print("\nDone.")


if __name__ == "__main__":
    main()
