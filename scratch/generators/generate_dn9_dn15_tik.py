#!/usr/bin/env python3
"""
Generate DN 9 and DN 15 tīkā (sub-commentary) files.
Source: tipitaka.org CSCD XML only (GitHub lacks tīkā files).

CSCD file mapping (mirrors att numbering):
  DN 9  → s0101t.tik9.xml  (Sīlakkhandhavagga)
  DN 15 → s0102t.tik1.xml  (Mahāvagga, offset DN 15 = 14+1)
"""

import os, re, time, html as hmod, urllib.request

VAULT    = os.environ.get("PALI_VAULT", "/Users/rds/pali_canon")
TIPITAKA = "https://tipitaka.org/romn/cscd/{}"

SUTTAS = [
    ("dn9",  "digha_nikaya", "dn9",  "DN9",
     "Poṭṭhapādasutta",  "With Poṭṭhapāda", "Dīgha Nikāya",
     "s0101t.tik9.xml", None,
     "Sumaṅgalavilāsinī-ṭīkā (Dīgha Nikāya Sub-commentary)"),

    ("dn15", "digha_nikaya", "dn15", "DN15",
     "Mahānidānasutta",   "The Great Discourse on Causation", "Dīgha Nikāya",
     "s0102t.tik1.xml", None,
     "Sumaṅgalavilāsinī-ṭīkā (Dīgha Nikāya Sub-commentary)"),
]

# ── helpers ───────────────────────────────────────────────────────────────────

def fetch_bytes(filename):
    req = urllib.request.Request(
        TIPITAKA.format(filename), headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=45) as r:
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
        attrs  = m.group(1); body = m.group(2)
        rend_m = re.search(r'rend="([^"]+)"', attrs)
        rend   = rend_m.group(1) if rend_m else ''
        pnum_m = re.search(r'<hi rend="paranum">\s*(\d+)\s*</hi>', body)
        paranum = pnum_m.group(1) if pnum_m else ''
        body   = re.sub(r'<hi rend="(?:paranum|dot)">[^<]*</hi>', '', body)
        text   = clean_xml(body)
        if text:
            results.append((rend, paranum, text))
    return results

def extract_section(paras, section_pattern):
    if section_pattern is None:
        return paras
    pat = re.compile(section_pattern)
    stop_pat = re.compile(r'^\d+\.\s+\S+(?:sutta|vagga|Vagga|Sutta)', re.IGNORECASE)
    start = None
    for i, (rend, pnum, text) in enumerate(paras):
        if start is None:
            if pat.search(text):
                start = i
        else:
            if stop_pat.match(text) and not pat.search(text):
                return paras[start:i]
    return paras[start:] if start is not None else []

def paras_to_markdown(paras):
    lines = []
    for rend, paranum, text in paras:
        if not text:
            continue
        if re.match(r'^\d+\.\s+\S+vaggo', text, re.IGNORECASE) or \
           re.match(r'^\d+\.\s+\S+vagga', text, re.IGNORECASE):
            lines.append(f"## {text}\n")
        elif re.match(r'^\d+\.\s+\S+(?:vaṇṇanā|ṭīkā|sutta)', text):
            lines.append(f"## {text}\n")
        elif rend in ('gatha', 'gathalast', 'indent'):
            lines.append(f"  {text}  ")
        else:
            prefix = f"({paranum}) " if paranum else ""
            lines.append(f"{prefix}{text}\n")
    return "\n".join(lines)

def build_tik_file(sc_id, nikaya_dir, slug, sutta_code, pali_title, en_title,
                   nikaya_label, commentary_name, pali_body):
    nav_link  = f"[[tika/sutta/{nikaya_dir}/INDEX|{nikaya_label}]]"
    mula_link = f"[[{slug}|{pali_title} — {en_title}]]"
    att_link  = f"[[{slug}_att|{pali_title}vaṇṇanā (atthakathā)]]"

    header = "\n".join([
        "---",
        f"id: {sutta_code}_tik",
        f"title_pali: {pali_title}vaṇṇanātīkā",
        f"title_en: Sub-commentary on {pali_title} ({en_title})",
        "type: tika",
        "pitaka: sutta",
        f"nikaya: {nikaya_dir.replace('_nikaya','')}",
        f"sutta: {sc_id}",
        "layer: tika",
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
        f"*{commentary_name}*",
        "",
        f"## {pali_title}vaṇṇanātīkā",
        "",
        "*Pali text — CSCD (Chattha Sangayana Tipitaka). "
        "Use Simsapa DPD for word lookups (double-click any Pali word).*",
        "",
    ])
    return header + "\n" + pali_body

def update_tik_index(nikaya_dir, slug, sutta_code, pali_title, wc):
    idx = os.path.join(VAULT, "tika/sutta", nikaya_dir, "Tika-Digha-Index.md")
    with open(idx, encoding="utf-8") as f:
        content = f.read()
    if slug in content:
        return
    if "| Sutta |" not in content:
        content = content.rstrip() + "\n\n## Migrated Texts\n\n| Sutta | Sub-commentary | Pali Source | Words |\n|---|---|---|---|\n"
        with open(idx, "w", encoding="utf-8") as f:
            f.write(content)
    row = f"| [[{slug}|{sutta_code}]] | [[{slug}_tik|{pali_title}vaṇṇanātīkā]] | tipitaka.org CSCD | {wc:,} |\n"
    with open(idx, "a", encoding="utf-8") as f:
        f.write(row)

def main():
    for (sc_id, nikaya_dir, slug, sutta_code, pali_title, en_title,
         nikaya_label, cscd_file, section_pattern, commentary_name) in SUTTAS:

        print(f"\n{sutta_code}: {pali_title}")
        out_dir = os.path.join(VAULT, "tika/sutta", nikaya_dir)
        os.makedirs(out_dir, exist_ok=True)

        print(f"  Fetching {cscd_file}...", end=" ", flush=True)
        try:
            all_paras = load_cscd_paras(cscd_file)
            section   = extract_section(all_paras, section_pattern)
            pali_body = paras_to_markdown(section)
            print(f"{len(section)} paragraphs ({len(all_paras)} total in file)")
        except Exception as e:
            print(f"ERROR: {e}")
            pali_body = f"*Error fetching Pali sub-commentary: {e}*\n"
            section   = []
        time.sleep(0.5)

        content = build_tik_file(
            sc_id, nikaya_dir, slug, sutta_code, pali_title, en_title,
            nikaya_label, commentary_name, pali_body)
        fname = f"{slug}_tik.md"
        with open(os.path.join(out_dir, fname), "w", encoding="utf-8") as f:
            f.write(content + "\n")

        wc = len(content.split())
        print(f"  -> {fname}: {wc:,} words")
        update_tik_index(nikaya_dir, slug, sutta_code, pali_title, wc)

    print("\nDone.")

if __name__ == "__main__":
    main()
