#!/usr/bin/env python3
"""
AN batch tīkā — Manorathapūraṇī-ṭīkā sections from CSCD.

Tīkā files mirror the atthakathā exactly (s040Xt.tikN = s040Xa.attN):
  AN 3.100   s0402t.tik28.xml
  AN 4.123–126 s0402t.tik48.xml
  AN 5.28    s0403t.tik2.xml
  AN 9.36    s0404t.tik13.xml
  AN 10.2–6  s0404t.tik15.xml
"""

import os, re, time, html as hmod, urllib.request

VAULT    = os.environ.get("PALI_VAULT", "/Users/rds/pali_canon")
TIPITAKA = "https://tipitaka.org/romn/cscd/{}"

NIKAYA_DIR   = "anguttara_nikaya"
NIKAYA_LABEL = "Aṅguttara Nikāya"

ENTRIES = [
    {
        "slug":         "an3_100",
        "display":      "AN 3.100",
        "pali_title":   "Loṇakapallasutta",
        "en_title":     "A Lump of Salt",
        "commentary":   "Manorathapūraṇī-ṭīkā (Aṅguttara Nikāya Sub-commentary)",
        "cscd_file":    "s0402t.tik28.xml",
    },
    {
        "slug":         "an4_123_126",
        "display":      "AN 4.123–126",
        "pali_title":   "Nānākaraṇasuttāni",
        "en_title":     "Differences (AN 4.123–126)",
        "commentary":   "Manorathapūraṇī-ṭīkā (Aṅguttara Nikāya Sub-commentary)",
        "cscd_file":    "s0402t.tik48.xml",
    },
    {
        "slug":         "an5_28",
        "display":      "AN 5.28",
        "pali_title":   "Pañcaṅgikasutta",
        "en_title":     "With Five Factors",
        "commentary":   "Manorathapūraṇī-ṭīkā (Aṅguttara Nikāya Sub-commentary)",
        "cscd_file":    "s0403t.tik2.xml",
    },
    {
        "slug":         "an9_36",
        "display":      "AN 9.36",
        "pali_title":   "Jhānasutta",
        "en_title":     "Depending on Absorption",
        "commentary":   "Manorathapūraṇī-ṭīkā (Aṅguttara Nikāya Sub-commentary)",
        "cscd_file":    "s0404t.tik13.xml",
    },
    {
        "slug":         "an10_2_6",
        "display":      "AN 10.2–6",
        "pali_title":   "Ānisaṃsasuttāni",
        "en_title":     "Benefits (AN 10.2–6)",
        "commentary":   "Manorathapūraṇī-ṭīkā (Aṅguttara Nikāya Sub-commentary)",
        "cscd_file":    "s0404t.tik15.xml",
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
        attrs   = m.group(1)
        body    = m.group(2)
        rend_m  = re.search(r'rend="([^"]+)"', attrs)
        rend    = rend_m.group(1) if rend_m else ''
        pnum_m  = re.search(r'<hi rend="paranum">\s*(\d+)\s*</hi>', body)
        paranum = pnum_m.group(1) if pnum_m else ''
        body    = re.sub(r'<hi rend="(?:paranum|dot)">[^<]*</hi>', '', body)
        text    = clean_xml(body)
        if text:
            results.append((rend, paranum, text))
    return results


def paras_to_markdown(paras):
    lines = []
    for rend, paranum, text in paras:
        if not text:
            continue
        if re.match(r'^\d+\.\s+\S+vaggo', text, re.IGNORECASE) or \
           re.match(r'^\d+\.\s+\S+vagga', text, re.IGNORECASE) or \
           re.match(r'^\(\d+\)\s+\d+\.\s+\S+vaggo', text, re.IGNORECASE):
            lines.append(f"## {text}\n")
        elif re.match(r'\d+[-–]\d+\.\s+\S+sutta|^\d+\.\s+\S+suttavaṇṇanā', text, re.IGNORECASE):
            lines.append(f"### {text}\n")
        elif rend in ('gatha', 'gathalast', 'indent'):
            lines.append(f"  {text}  ")
        else:
            prefix = f"({paranum}) " if paranum else ""
            lines.append(f"{prefix}{text}\n")
    return "\n".join(lines)


def build_tik_file(entry, pali_body, para_count):
    slug        = entry["slug"]
    display     = entry["display"]
    pali_title  = entry["pali_title"]
    en_title    = entry["en_title"]
    commentary  = entry["commentary"]

    nav_link  = f"[[tika/sutta/{NIKAYA_DIR}/INDEX|{NIKAYA_LABEL}]]"
    mula_link = f"[[{slug}|{pali_title} — {en_title}]]"
    att_link  = f"[[{slug}_att|{pali_title}vaṇṇanā (Atthakathā)]]"

    header = "\n".join([
        "---",
        f"id: {display.replace(' ', '').replace('–', '-')}_tik",
        f"title_pali: {pali_title}vaṇṇanāṭīkā",
        f"title_en: Sub-commentary on {pali_title} ({en_title})",
        "type: tika",
        "pitaka: sutta",
        "nikaya: anguttara",
        f"mula_file: [[{slug}]]",
        f"att_file: [[{slug}_att]]",
        "source_pali: https://tipitaka.org/romn/cscd/ (CSCD)",
        "---",
        "",
        f"# Sub-commentary on {NIKAYA_LABEL}: {pali_title}",
        f"*{display} — {en_title}*",
        "",
        f"**Navigation**: [[INDEX|Pali Canon Vault]] / [[tika/Tika-Index|Ṭīkā]] / "
        f"[[tika/sutta/Tika-Sutta-Index|Sutta]] / {nav_link}",
        f"**Mūla**: {mula_link}",
        f"**Atthakathā**: {att_link}",
        "",
        f"*{commentary}*",
        f"*{para_count} paragraphs — Pali text CSCD.*",
        "",
        f"## {pali_title}vaṇṇanāṭīkā",
        "",
        "*Pali text — CSCD (Chattha Sangayana Tipitaka). "
        "Use Simsapa DPD for word lookups (double-click any Pali word).*",
        "",
    ])
    return header + "\n" + pali_body


def update_index(slug, display, pali_title, wc):
    idx = os.path.join(VAULT, "tika/sutta", NIKAYA_DIR, "Tika-Anguttara-Index.md")
    with open(idx, encoding="utf-8") as f:
        content = f.read()
    if f"{slug}_tik" in content:
        return
    row = (f"| [[{slug}|{display}]] | "
           f"[[{slug}_tik|{pali_title}vaṇṇanāṭīkā]] | "
           f"tipitaka.org CSCD | {wc:,} |\n")
    with open(idx, "a", encoding="utf-8") as f:
        f.write(row)


def main():
    out_dir = os.path.join(VAULT, "tika/sutta", NIKAYA_DIR)

    for entry in ENTRIES:
        slug      = entry["slug"]
        display   = entry["display"]
        cscd_file = entry["cscd_file"]

        print(f"\n{display}: {entry['pali_title']}")
        print(f"  Fetching {cscd_file}...", end=" ", flush=True)
        try:
            paras     = load_cscd_paras(cscd_file)
            pali_body = paras_to_markdown(paras)
            print(f"{len(paras)} paragraphs")
        except Exception as e:
            print(f"ERROR: {e}")
            pali_body = f"*Error fetching Pali sub-commentary: {e}*\n"
            paras     = []

        content = build_tik_file(entry, pali_body, len(paras))
        fname   = f"{slug}_tik.md"
        with open(os.path.join(out_dir, fname), "w", encoding="utf-8") as f:
            f.write(content + "\n")

        wc = len(content.split())
        print(f"  → {fname}: {wc:,} words")
        update_index(slug, display, entry["pali_title"], wc)
        time.sleep(0.8)

    print("\nDone.")


if __name__ == "__main__":
    main()
