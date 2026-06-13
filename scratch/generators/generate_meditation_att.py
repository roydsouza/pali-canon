#!/usr/bin/env python3
"""
Generate atthakathā (commentary) files for 6 key meditation suttas.

Two sources per sutta:
  1. Classical Pali commentary — CSCD XML from siongui/tipitaka-romn on GitHub
  2. Translator's notes — Bhikkhu Sujato's segment annotations from SuttaCentral

Output: atthakatha/sutta/{nikaya}/{slug}_att.md
"""

import os, json, re, time, html as hmod, urllib.request

VAULT       = os.environ.get("PALI_VAULT", "/Users/rds/pali_canon")
CSCD_BASE   = "https://raw.githubusercontent.com/siongui/tipitaka-romn/master/cscd/{}"
SC_COMMENT  = "https://suttacentral.net/api/bilarasuttas/{}/comment"
SC_SUTTA    = "https://suttacentral.net/api/bilarasuttas/{}/sujato"

# (sc_id, nikaya_dir, slug, sutta_code, pali_title, en_title, nikaya_label,
#  cscd_file, section_pattern, commentary_name)
#
# section_pattern: regex to match the sutta heading line in the CSCD file.
#   None means use the entire file (DN 2 has its own dedicated file;
#   AN 4.41's vagga is very short).
SUTTAS = [
    ("mn10",   "majjhima_nikaya",  "mn10",   "MN10",
     "Satipaṭṭhānasutta",    "Mindfulness Meditation",
     "Majjhima Nikāya",
     "s0201a.att1.xml",  r"10\.\s+Satipaṭṭhānasuttavaṇṇanā",
     "Papañcasūdanī (Majjhima Nikāya Atthakathā)"),

    ("mn20",   "majjhima_nikaya",  "mn20",   "MN20",
     "Vitakkasaṇṭhānasutta", "The Relaxation of Thoughts",
     "Majjhima Nikāya",
     "s0201a.att2.xml",  r"10\.\s+Vitakkasaṇṭhānasuttavaṇṇanā",
     "Papañcasūdanī (Majjhima Nikāya Atthakathā)"),

    ("mn119",  "majjhima_nikaya",  "mn119",  "MN119",
     "Kāyagatāsatisutta",    "Mindfulness of the Body",
     "Majjhima Nikāya",
     "s0203a.att1.xml",  r"9\.\s+Kāyagatāsatisuttavaṇṇanā",
     "Papañcasūdanī (Majjhima Nikāya Atthakathā)"),

    ("mn121",  "majjhima_nikaya",  "mn121",  "MN121",
     "Cūḷasuññatasutta",     "The Shorter Discourse on Emptiness",
     "Majjhima Nikāya",
     "s0203a.att2.xml",  r"1\.\s+Cūḷasuññatasuttavaṇṇanā",
     "Papañcasūdanī (Majjhima Nikāya Atthakathā)"),

    ("dn2",    "digha_nikaya",     "dn2",    "DN2",
     "Sāmaññaphalasutta",    "The Fruits of the Ascetic Life",
     "Dīgha Nikāya",
     "s0101a.att2.xml",  None,   # entire file is the DN 2 commentary
     "Sumaṅgalavilāsinī (Dīgha Nikāya Atthakathā)"),

    ("an4.41", "anguttara_nikaya", "an4_41", "AN4.41",
     "Samādhibhāvanāsutta",  "Four Developments of Immersion",
     "Aṅguttara Nikāya",
     "s0402a.att4.xml",  None,   # entire file (parisavagga, short)
     "Manorathapūraṇī (Aṅguttara Nikāya Atthakathā)"),
]

MULA_DIR_MAP = {
    "majjhima_nikaya":  "mula/sutta/majjhima_nikaya",
    "digha_nikaya":     "mula/sutta/digha_nikaya",
    "anguttara_nikaya": "mula/sutta/anguttara_nikaya",
}

# ── helpers ──────────────────────────────────────────────────────────────────

def fetch_bytes(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def clean_xml(text):
    """Strip XML tags; convert bold hi to markdown bold; clean whitespace."""
    # Preserve <hi rend="bold"> as **...**
    text = re.sub(r'<hi rend="bold">(.*?)</hi>', r'**\1**', text, flags=re.DOTALL)
    # Remove page-break and other hi tags
    text = re.sub(r'<pb[^/]*/>', '', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = hmod.unescape(text)
    # Collapse internal whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def strip_html(text):
    """Strip all HTML/XML tags for plain text (for SC notes)."""
    text = re.sub(r'<[^>]+>', ' ', text)
    text = hmod.unescape(text)
    return re.sub(r'\s+', ' ', text).strip()


# ── CSCD parsing ─────────────────────────────────────────────────────────────

def load_cscd_paras(filename):
    """Fetch a CSCD XML file and return list of (rend, paranum, clean_text) tuples."""
    raw = fetch_bytes(CSCD_BASE.format(filename))
    try:
        content = raw.decode('utf-16')
    except UnicodeDecodeError:
        content = raw.decode('utf-8', errors='replace')

    results = []
    for m in re.finditer(r'<p([^>]*)>(.*?)</p>', content, re.DOTALL):
        attrs   = m.group(1)
        body    = m.group(2)
        rend_m  = re.search(r'rend="([^"]+)"', attrs)
        rend    = rend_m.group(1) if rend_m else ''
        # Extract paragraph number from <hi rend="paranum">N</hi>
        pnum_m  = re.search(r'<hi rend="paranum">\s*(\d+)\s*</hi>', body)
        paranum = pnum_m.group(1) if pnum_m else ''
        # Remove paranum/dot hi from body before cleaning
        body    = re.sub(r'<hi rend="(?:paranum|dot)">[^<]*</hi>', '', body)
        text    = clean_xml(body)
        if text:
            results.append((rend, paranum, text))
    return results


def extract_section(paras, section_pattern):
    """
    Extract paragraphs belonging to one sutta's commentary.
    If section_pattern is None, return all paragraphs.
    Otherwise, find the matching heading paragraph and return from there
    until the next same-level heading or end of file.
    """
    if section_pattern is None:
        return paras

    pat = re.compile(section_pattern)
    start = None
    for i, (rend, pnum, text) in enumerate(paras):
        if start is None:
            if pat.search(text):
                start = i
        else:
            # Stop at the next sutta-level heading (different sutta)
            if re.match(r'^\d+\.\s+\w+[vaV]aṇṇanā', text) and not pat.search(text):
                return paras[start:i]
    if start is None:
        return []
    return paras[start:]


def paras_to_markdown(paras):
    """Render (rend, paranum, text) list to markdown string."""
    lines = []
    for rend, paranum, text in paras:
        if not text:
            continue
        # Chapter / vagga headings
        if re.match(r'^\d+\.\s+\w+vaggo', text) or re.match(r'^\d+\.\s+\w+vagga', text):
            lines.append(f"## {text}\n")
        # Sutta commentary heading
        elif re.match(r'^\d+\.\s+\w+[vaV]aṇṇanā', text):
            lines.append(f"## {text}\n")
        # Verse/gatha lines (indent)
        elif rend in ('gatha', 'gathalast', 'indent'):
            lines.append(f"  {text}  ")
        # Normal commentary paragraph
        else:
            prefix = f"({paranum}) " if paranum else ""
            lines.append(f"{prefix}{text}\n")
    return "\n".join(lines)


# ── SuttaCentral notes ────────────────────────────────────────────────────────

def fetch_sujato_notes(sc_id):
    """Return list of (key, note_text) for segments that have notes."""
    try:
        data = fetch_json(SC_COMMENT.format(sc_id))
    except Exception:
        return []
    ct = data.get('comment_text', {})
    notes = []
    for k, v in ct.items():
        note = strip_html(v).strip()
        if note:
            notes.append((k, note))
    return notes


def notes_to_markdown(notes, sc_id, slug, nikaya_dir):
    if not notes:
        return ""
    mula_path = f"[[{slug}|{slug.upper().replace('_','.')}]]"
    lines = [
        "## Translator's Notes",
        f"*Bhikkhu Sujato — segment annotations from SuttaCentral*",
        f"*Mūla file: {mula_path}*",
        "",
    ]
    for key, note in notes:
        # Extract just the segment number for brevity: "mn10:4.2" → "4.2"
        seg = key.split(':', 1)[1] if ':' in key else key
        lines.append(f"**{seg}** — {note}")
        lines.append("")
    return "\n".join(lines)


# ── file assembly ─────────────────────────────────────────────────────────────

def build_att_file(sc_id, nikaya_dir, slug, sutta_code, pali_title, en_title,
                   nikaya_label, commentary_name, pali_body, notes_body):
    nav_link = f"[[atthakatha/sutta/{nikaya_dir}/INDEX|{nikaya_label}]]"
    mula_slug_link = f"[[{slug}|{pali_title} — {en_title}]]"

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
        f"source_pali: https://github.com/siongui/tipitaka-romn (CSCD)",
        "source_notes: https://suttacentral.net",
        "---",
        "",
        f"# Commentary on {nikaya_label}: {pali_title}",
        "",
        f"**Navigation**: [[INDEX|Pali Canon Vault]] / [[atthakatha/Atthakatha-Index|Atthakathā]] / "
        f"[[atthakatha/sutta/Atthakatha-Sutta-Index|Sutta]] / {nav_link}",
        f"**Mūla**: {mula_slug_link}",
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


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    for (sc_id, nikaya_dir, slug, sutta_code, pali_title, en_title,
         nikaya_label, cscd_file, section_pattern, commentary_name) in SUTTAS:

        print(f"\n{sutta_code}: {pali_title}")
        out_dir = os.path.join(VAULT, "atthakatha/sutta", nikaya_dir)
        os.makedirs(out_dir, exist_ok=True)

        # 1. Fetch and parse Pali commentary
        print(f"  Fetching CSCD {cscd_file}...", end=" ", flush=True)
        try:
            all_paras = load_cscd_paras(cscd_file)
            section   = extract_section(all_paras, section_pattern)
            pali_body = paras_to_markdown(section)
            print(f"{len(section)} paragraphs")
        except Exception as e:
            print(f"ERROR: {e}")
            pali_body = f"*Error fetching Pali commentary: {e}*\n"

        time.sleep(0.3)

        # 2. Fetch Sujato's notes
        print(f"  Fetching Sujato notes for {sc_id}...", end=" ", flush=True)
        notes = fetch_sujato_notes(sc_id)
        notes_body = notes_to_markdown(notes, sc_id, slug, nikaya_dir)
        print(f"{len(notes)} annotations")

        time.sleep(0.3)

        # 3. Build and write file
        content = build_att_file(
            sc_id, nikaya_dir, slug, sutta_code, pali_title, en_title,
            nikaya_label, commentary_name, pali_body, notes_body
        )
        fname = f"{slug}_att.md"
        with open(os.path.join(out_dir, fname), "w", encoding="utf-8") as f:
            f.write(content + "\n")

        wc = len(content.split())
        print(f"  -> {fname}: {wc:,} words")

    print("\nDone.")


if __name__ == "__main__":
    main()
