#!/usr/bin/env python3
"""
SN 35 (Saḷāyatanasaṃyutta) atthakathā layer from CSCD (Sāratthappakāsinī).

SN 35 is in the Saḷāyatanavagga (s0304). The file is s0304a.att0.xml.
Probing: try att0 first; fallback to checking att1, att2 if needed.
"""

import os, re, time, html as hmod, urllib.request

VAULT    = os.environ.get("PALI_VAULT", "/Users/rds/pali_canon")
TIPITAKA = "https://tipitaka.org/romn/cscd/{}"

SAMYUTTAS = [
    {
        "slug":             "sn35",
        "sutta_code":       "SN35",
        "nikaya_dir":       "samyutta_nikaya",
        "pali_title":       "Saḷāyatanasaṃyutta",
        "en_title":         "Linked Discourses on the Six Sense Bases",
        "nikaya_label":     "Saṃyutta Nikāya",
        "commentary_name":  "Sāratthappakāsinī (Saṃyutta Nikāya Atthakathā)",
        # SN 35 = Saḷāyatanavagga, first saṃyutta → s0304a.att0.xml
        # Candidates to probe: att0, att1, att2
        "cscd_candidates":  ["s0304a.att0.xml", "s0304a.att1.xml", "s0304a.att2.xml"],
    },
]


def fetch_bytes(filename):
    req = urllib.request.Request(
        TIPITAKA.format(filename), headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def probe_cscd(candidates):
    """Return (filename, raw_bytes) for the first candidate that returns non-empty content."""
    for fname in candidates:
        print(f"  Probing {fname}...", end=" ", flush=True)
        try:
            raw = fetch_bytes(fname)
            if len(raw) > 1000:
                print(f"OK ({len(raw):,} bytes)")
                return fname, raw
            print(f"empty ({len(raw)} bytes)")
        except Exception as e:
            print(f"failed: {e}")
        time.sleep(0.5)
    return None, None


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


def build_att_file(s, pali_body, para_count, cscd_file):
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
        f"*{para_count} paragraphs — Pali text CSCD ({cscd_file}).*",
        "",
        f"## {pali_title}vaṇṇanā",
        "",
        "*Pali text — CSCD (Chattha Sangayana Tipitaka). "
        "Use Simsapa DPD for word lookups (double-click any Pali word).*",
        "",
    ])
    return header + "\n" + pali_body


def append_index(nikaya_dir, slug, sutta_code, pali_title, wc):
    idx = os.path.join(VAULT, "atthakatha/sutta", nikaya_dir, "Atthakatha-Samyutta-Index.md")
    with open(idx, encoding="utf-8") as f:
        content = f.read()
    if f"{slug}_att" in content:
        print(f"  (already in atthakatha INDEX)")
        return
    row = (f"| [[{slug}\|{sutta_code}]] | "
           f"[[{slug}_att\|{pali_title}vaṇṇanā]] | "
           f"tipitaka.org CSCD | {wc:,} |\n")
    with open(idx, "a", encoding="utf-8") as f:
        f.write(row)


def main():
    for s in SAMYUTTAS:
        slug       = s["slug"]
        sutta_code = s["sutta_code"]
        pali_title = s["pali_title"]
        nikaya_dir = s["nikaya_dir"]
        candidates = s["cscd_candidates"]

        print(f"\n{sutta_code}: {pali_title}")

        cscd_file, raw = probe_cscd(candidates)
        if not raw:
            print(f"  ERROR: no CSCD file found for {sutta_code}")
            continue

        paras     = load_cscd_paras(raw)
        pali_body = paras_to_markdown(paras)
        print(f"  Parsed {len(paras)} paragraphs")

        content = build_att_file(s, pali_body, len(paras), cscd_file)
        out_dir = os.path.join(VAULT, "atthakatha/sutta", nikaya_dir)
        os.makedirs(out_dir, exist_ok=True)
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
