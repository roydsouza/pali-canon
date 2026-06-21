#!/usr/bin/env python3
"""
Phase 2 atthakathā: MN 36, 43, 44, 52, 111 and DN 22.
Two sources:
  - GitHub (siongui/tipitaka-romn) for most MN/DN files
  - tipitaka.org for s0202a.att0.xml (Gahapativagga — not on GitHub)
"""

import os, json, re, time, html as hmod, urllib.request

VAULT      = os.environ.get("PALI_VAULT", "/Users/rds/pali_canon")
GITHUB     = "https://raw.githubusercontent.com/siongui/tipitaka-romn/master/cscd/{}"
TIPITAKA   = "https://tipitaka.org/romn/cscd/{}"
SC_COMMENT = "https://suttacentral.net/api/bilarasuttas/{}/comment"

# (sc_id, nikaya_dir, slug, sutta_code, pali_title, en_title, nikaya_label,
#  cscd_source, cscd_file, section_pattern, commentary_name)
#
# cscd_source: "github" | "tipitaka"
SUTTAS = [
    ("mn36",  "majjhima_nikaya", "mn36",  "MN36",
     "Mahāsaccakasutta",    "With Saccaka (the Longer)", "Majjhima Nikāya",
     "github",   "s0201a.att4.xml", r"6\.\s+Mahāsaccaka",
     "Papañcasūdanī (Majjhima Nikāya Atthakathā)"),

    ("mn43",  "majjhima_nikaya", "mn43",  "MN43",
     "Mahāvedallasutta",    "The Longer Analysis",       "Majjhima Nikāya",
     "github",   "s0201a.att5.xml", r"3\.\s+Mahāvedalla",
     "Papañcasūdanī (Majjhima Nikāya Atthakathā)"),

    ("mn44",  "majjhima_nikaya", "mn44",  "MN44",
     "Cūḷavedallasutta",    "The Shorter Analysis",      "Majjhima Nikāya",
     "github",   "s0201a.att5.xml", r"4\.\s+Cūḷavedalla",
     "Papañcasūdanī (Majjhima Nikāya Atthakathā)"),

    ("mn52",  "majjhima_nikaya", "mn52",  "MN52",
     "Aṭṭhakanāgarasutta",  "At Aṭṭhakanāgara",         "Majjhima Nikāya",
     "tipitaka", "s0202a.att0.xml", r"2\.\s+Aṭṭhakanāgara",
     "Papañcasūdanī (Majjhima Nikāya Atthakathā)"),

    ("mn111", "majjhima_nikaya", "mn111", "MN111",
     "Anupadasutta",        "One by One",               "Majjhima Nikāya",
     "github",   "s0203a.att1.xml", r"1\.\s+Anupada",
     "Papañcasūdanī (Majjhima Nikāya Atthakathā)"),

    ("dn22",  "digha_nikaya",   "dn22",  "DN22",
     "Mahāsatipaṭṭhānasutta", "The Longer Discourse on Mindfulness Meditation",
     "Dīgha Nikāya",
     "github",   "s0102a.att8.xml", None,   # entire file = DN 22 only
     "Sumaṅgalavilāsinī (Dīgha Nikāya Atthakathā)"),
]

# ── helpers ───────────────────────────────────────────────────────────────────

def fetch_bytes(url, source):
    base = GITHUB if source == "github" else TIPITAKA
    req = urllib.request.Request(base.format(url), headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=45) as r:
        return r.read()

def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def clean_xml(text):
    text = re.sub(r'<hi rend="bold">(.*?)</hi>', r'**\1**', text, flags=re.DOTALL)
    text = re.sub(r'<pb[^/]*/>', '', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = hmod.unescape(text)
    return re.sub(r'\s+', ' ', text).strip()

def strip_html(text):
    text = re.sub(r'<[^>]+>', ' ', text)
    return re.sub(r'\s+', ' ', hmod.unescape(text)).strip()

# ── CSCD parsing ──────────────────────────────────────────────────────────────

def load_cscd_paras(filename, source):
    raw = fetch_bytes(filename, source)
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
    stop_pat = re.compile(r'^\d+\.\s+\w+[vaV]aṇṇanā')
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
        if re.match(r'^\d+\.\s+\S+vaggo', text, re.IGNORECASE):
            lines.append(f"## {text}\n")
        elif re.match(r'^\d+\.\s+\S+[vaV]aṇṇanā', text):
            lines.append(f"## {text}\n")
        elif rend in ('gatha', 'gathalast', 'indent'):
            lines.append(f"  {text}  ")
        else:
            prefix = f"({paranum}) " if paranum else ""
            lines.append(f"{prefix}{text}\n")
    return "\n".join(lines)

# ── SC notes ──────────────────────────────────────────────────────────────────

def fetch_sujato_notes(sc_id):
    try:
        data = fetch_json(SC_COMMENT.format(sc_id))
    except Exception:
        return []
    ct = data.get('comment_text', {})
    return [(k, strip_html(v).strip()) for k, v in ct.items() if strip_html(v).strip()]

def notes_to_markdown(notes, slug):
    if not notes:
        return ""
    lines = [
        "## Translator's Notes",
        "*Bhikkhu Sujato — segment annotations from SuttaCentral*",
        f"*Mūla file: [[{slug}]]*",
        "",
    ]
    for key, note in notes:
        seg = key.split(':', 1)[1] if ':' in key else key
        lines.append(f"**{seg}** — {note}")
        lines.append("")
    return "\n".join(lines)

# ── file assembly ─────────────────────────────────────────────────────────────

def build_att_file(sc_id, nikaya_dir, slug, sutta_code, pali_title, en_title,
                   nikaya_label, commentary_name, pali_body, notes_body):
    nav_link      = f"[[atthakatha/sutta/{nikaya_dir}/INDEX|{nikaya_label}]]"
    mula_link     = f"[[{slug}|{pali_title} — {en_title}]]"
    tik_link      = f"[[{slug}_tik|{pali_title}vaṇṇanātīkā (sub-commentary)]]"

    header = "\n".join([
        "---",
        f"id: {sutta_code}_att",
        f"title_pali: {pali_title}vaṇṇanā",
        f"title_en: Commentary on {pali_title} ({en_title})",
        "type: atthakatha",
        "pitaka: sutta",
        f"nikaya: {nikaya_dir.replace('_nikaya','')}",
        f"sutta: {sc_id}",
        "layer: atthakatha",
        f"mula_file: [[{slug}]]",
        f"att_file: [[{slug}_att]]",
        "source_pali: https://github.com/siongui/tipitaka-romn (CSCD)",
        "source_notes: https://suttacentral.net",
        "---",
        "",
        f"# Commentary on {nikaya_label}: {pali_title}",
        "",
        f"**Navigation**: [[INDEX|Pali Canon Vault]] / [[atthakatha/Atthakatha-Index|Atthakathā]] / "
        f"[[atthakatha/sutta/Atthakatha-Sutta-Index|Sutta]] / {nav_link}",
        f"**Mūla**: {mula_link}",
        f"**Tīkā**: {tik_link}",
        "",
        f"*{commentary_name}*",
        "",
    ])

    parts = [header]
    if notes_body:
        parts.append(notes_body)
        parts.append("\n---\n")
    parts.append(f"## {pali_title}vaṇṇanā\n")
    parts.append("*Pali text — CSCD (Chattha Sangayana Tipitaka). "
                 "Use Simsapa DPD for word lookups (double-click any Pali word).*\n")
    parts.append(pali_body)
    return "\n".join(parts)

# ── index update ──────────────────────────────────────────────────────────────

def update_att_index(nikaya_dir, slug, sutta_code, pali_title, notes_count, wc):
    idx = os.path.join(VAULT, "atthakatha/sutta", nikaya_dir, "Atthakatha-Samyutta-Index.md")
    with open(idx, encoding="utf-8") as f:
        content = f.read()
    if slug in content:
        return
    # Ensure table exists
    if "| Sutta |" not in content:
        content = content.rstrip() + "\n\n## Migrated Texts\n\n| Sutta | Commentary | Pali Source | Notes | Words |\n|---|---|---|---|---|\n"
    nikaya_short = nikaya_dir.replace('_nikaya', '')
    row = (f"| [[{slug}\|{sutta_code}]] | [[{slug}_att\|{pali_title}vaṇṇanā]] | "
           f"CSCD | {notes_count} Sujato notes | {wc:,} |\n")
    with open(idx, "a", encoding="utf-8") as f:
        f.write(row)

# ── main ──────────────────────────────────────────────────────────────────────

def main():
    for (sc_id, nikaya_dir, slug, sutta_code, pali_title, en_title,
         nikaya_label, cscd_source, cscd_file, section_pattern,
         commentary_name) in SUTTAS:

        print(f"\n{sutta_code}: {pali_title}")
        out_dir = os.path.join(VAULT, "atthakatha/sutta", nikaya_dir)
        os.makedirs(out_dir, exist_ok=True)

        print(f"  Fetching {cscd_file} ({cscd_source})...", end=" ", flush=True)
        try:
            all_paras = load_cscd_paras(cscd_file, cscd_source)
            section   = extract_section(all_paras, section_pattern)
            pali_body = paras_to_markdown(section)
            print(f"{len(section)} paragraphs")
        except Exception as e:
            print(f"ERROR: {e}")
            pali_body = f"*Error fetching Pali commentary: {e}*\n"
            section   = []
        time.sleep(0.4)

        print(f"  Fetching Sujato notes for {sc_id}...", end=" ", flush=True)
        notes     = fetch_sujato_notes(sc_id)
        notes_body = notes_to_markdown(notes, slug)
        print(f"{len(notes)} annotations")
        time.sleep(0.3)

        content = build_att_file(
            sc_id, nikaya_dir, slug, sutta_code, pali_title, en_title,
            nikaya_label, commentary_name, pali_body, notes_body)
        fname = f"{slug}_att.md"
        with open(os.path.join(out_dir, fname), "w", encoding="utf-8") as f:
            f.write(content + "\n")

        wc = len(content.split())
        print(f"  -> {fname}: {wc:,} words")
        update_att_index(nikaya_dir, slug, sutta_code, pali_title, len(notes), wc)

    print("\nDone.")

if __name__ == "__main__":
    main()
