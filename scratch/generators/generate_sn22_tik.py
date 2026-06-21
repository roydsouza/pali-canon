#!/usr/bin/env python3
"""
SN 22 (Khandhasaṃyutta) tīkā layer from CSCD (Sāratthappakāsinī-ṭīkā).

SN 22 is in the Khandavagga (s0303). The file is s0303t.tik0.xml.
"""

import os, re, time, html as hmod, urllib.request

VAULT    = os.environ.get("PALI_VAULT", "/Users/rds/pali_canon")
TIPITAKA = "https://tipitaka.org/romn/cscd/{}"

SAMYUTTAS = [
    {
        "slug":            "sn22",
        "sutta_code":      "SN22",
        "nikaya_dir":      "samyutta_nikaya",
        "pali_title":      "Khandhasaṃyutta",
        "en_title":        "Linked Discourses on the Aggregates",
        "nikaya_label":    "Saṃyutta Nikāya",
        "commentary_name": "Sāratthappakāsinī-ṭīkā (Saṃyutta Nikāya Sub-commentary)",
        "cscd_file":       "s0303t.tik0.xml",
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


def load_cscd_paras(raw):
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


def build_tik_file(s, pali_body, para_count, cscd_file):
    slug         = s["slug"]
    sutta_code   = s["sutta_code"]
    nikaya_dir   = s["nikaya_dir"]
    pali_title   = s["pali_title"]
    en_title     = s["en_title"]
    nikaya_label = s["nikaya_label"]
    commentary   = s["commentary_name"]

    nav_link  = f"[[tika/sutta/{nikaya_dir}/INDEX|{nikaya_label}]]"
    mula_link = f"[[{slug}|{pali_title} — {en_title}]]"
    att_link  = f"[[{slug}_att|{pali_title}vaṇṇanā (Atthakathā)]]"

    header = "\n".join([
        "---",
        f"id: {sutta_code}_tik",
        f"title_pali: {pali_title}vaṇṇanāṭīkā",
        f"title_en: Sub-commentary on {pali_title}",
        "type: tika",
        "pitaka: sutta",
        "nikaya: samyutta",
        f"samyutta: {slug}",
        f"mula_file: [[{slug}]]",
        f"att_file: [[{slug}_att]]",
        "source_pali: https://tipitaka.org/romn/cscd/ (CSCD)",
        "---",
        "",
        f"# Sub-commentary on {nikaya_label}: {pali_title}",
        "",
        f"**Navigation**: [[INDEX|Pali Canon Vault]] / [[tika/Tika-Index|Ṭīkā]] / "
        f"[[tika/sutta/Tika-Sutta-Index|Sutta]] / {nav_link}",
        f"**Mūla**: {mula_link}",
        f"**Atthakathā**: {att_link}",
        "",
        f"*{commentary}*",
        f"*{para_count} paragraphs — Pali text CSCD ({cscd_file}).*",
        "",
        f"## {pali_title}vaṇṇanāṭīkā",
        "",
        "*Pali text — CSCD (Chattha Sangayana Tipitaka). "
        "Use Simsapa DPD for word lookups (double-click any Pali word).*",
        "",
    ])
    return header + "\n" + pali_body


def append_tik_index(nikaya_dir, slug, sutta_code, pali_title, wc):
    idx = os.path.join(VAULT, "tika/sutta", nikaya_dir, "Tika-Samyutta-Index.md")
    with open(idx, encoding="utf-8") as f:
        content = f.read()
    if f"{slug}_tik" in content:
        print(f"  (already in tika INDEX)")
        return
    row = (f"| [[{slug}\\|{sutta_code}]] | "
           f"[[{slug}_tik\\|{pali_title}vaṇṇanāṭīkā]] | "
           f"tipitaka.org CSCD | {wc:,} |\n")
    with open(idx, "a", encoding="utf-8") as f:
        f.write(row)


def main():
    for s in SAMYUTTAS:
        slug       = s["slug"]
        sutta_code = s["sutta_code"]
        pali_title = s["pali_title"]
        nikaya_dir = s["nikaya_dir"]
        cscd_file  = s["cscd_file"]

        print(f"\n{sutta_code}: {pali_title}")
        print(f"  Fetching {cscd_file}...", end=" ", flush=True)
        raw = fetch_bytes(cscd_file)
        print(f"OK ({len(raw):,} bytes)")

        paras     = load_cscd_paras(raw)
        pali_body = paras_to_markdown(paras)
        print(f"  Parsed {len(paras)} paragraphs")

        content = build_tik_file(s, pali_body, len(paras), cscd_file)
        out_dir = os.path.join(VAULT, "tika/sutta", nikaya_dir)
        os.makedirs(out_dir, exist_ok=True)
        fname   = f"{slug}_tik.md"
        with open(os.path.join(out_dir, fname), "w", encoding="utf-8") as f:
            f.write(content + "\n")

        wc = len(content.split())
        print(f"  → {fname}: {wc:,} words")
        append_tik_index(nikaya_dir, slug, sutta_code, pali_title, wc)
        time.sleep(1.0)

    print("\nDone.")


if __name__ == "__main__":
    main()
