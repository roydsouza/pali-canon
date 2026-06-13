#!/usr/bin/env python3
"""
Generate tīkā (sub-commentary) files for 6 key meditation suttas.

Source: CSCD XML from tipitaka.org/romn/cscd/ (has sutta tīkā files that
        siongui/tipitaka-romn on GitHub lacks).

Output: tika/sutta/{nikaya}/{slug}_tik.md
"""

import os, re, time, html as hmod, urllib.request

VAULT     = os.environ.get("PALI_VAULT", "/Users/rds/pali_canon")
CSCD_BASE = "https://tipitaka.org/romn/cscd/{}"

# (sc_id, nikaya_dir, slug, sutta_code, pali_title, en_title, nikaya_label,
#  cscd_file, section_pattern, commentary_name)
#
# section_pattern: regex to match the sutta heading paragraph in the XML.
#   None means use the entire file.
SUTTAS = [
    ("mn10",   "majjhima_nikaya",  "mn10",   "MN10",
     "Satipaṭṭhānasutta",    "Mindfulness Meditation",
     "Majjhima Nikāya",
     "s0201t.tik1.xml",  r"10\.\s+Satipaṭṭhāna",
     "Papañcasūdanī-ṭīkā (Majjhima Nikāya Sub-commentary)"),

    ("mn20",   "majjhima_nikaya",  "mn20",   "MN20",
     "Vitakkasaṇṭhānasutta", "The Relaxation of Thoughts",
     "Majjhima Nikāya",
     "s0201t.tik2.xml",  r"10\.\s+Vitakkasaṇṭhāna",
     "Papañcasūdanī-ṭīkā (Majjhima Nikāya Sub-commentary)"),

    ("mn119",  "majjhima_nikaya",  "mn119",  "MN119",
     "Kāyagatāsatisutta",    "Mindfulness of the Body",
     "Majjhima Nikāya",
     "s0203t.tik1.xml",  r"9\.\s+Kāyagatāsati",
     "Papañcasūdanī-ṭīkā (Majjhima Nikāya Sub-commentary)"),

    ("mn121",  "majjhima_nikaya",  "mn121",  "MN121",
     "Cūḷasuññatasutta",     "The Shorter Discourse on Emptiness",
     "Majjhima Nikāya",
     "s0203t.tik2.xml",  r"1\.\s+Cūḷasuññata",
     "Papañcasūdanī-ṭīkā (Majjhima Nikāya Sub-commentary)"),

    ("dn2",    "digha_nikaya",     "dn2",    "DN2",
     "Sāmaññaphalasutta",    "The Fruits of the Ascetic Life",
     "Dīgha Nikāya",
     "s0101t.tik2.xml",  None,   # entire file is DN 2 sub-commentary
     "Sumaṅgalavilāsinī-ṭīkā (Dīgha Nikāya Sub-commentary)"),

    ("an4.41", "anguttara_nikaya", "an4_41", "AN4.41",
     "Samādhibhāvanāsutta",  "Four Developments of Immersion",
     "Aṅguttara Nikāya",
     "s0402t.tik4.xml",  None,   # entire file (Parisavagga tīkā)
     "Manorathapūraṇī-ṭīkā (Aṅguttara Nikāya Sub-commentary)"),
]

# ── helpers ──────────────────────────────────────────────────────────────────

def fetch_bytes(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=45) as r:
        return r.read()


def clean_xml(text):
    """Strip XML tags; convert bold hi to markdown bold; clean whitespace."""
    text = re.sub(r'<hi rend="bold">(.*?)</hi>', r'**\1**', text, flags=re.DOTALL)
    text = re.sub(r'<pb[^/]*/>', '', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = hmod.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# ── CSCD parsing ─────────────────────────────────────────────────────────────

def load_cscd_paras(filename):
    """Fetch a CSCD XML file and return list of (rend, paranum, clean_text) tuples."""
    url = CSCD_BASE.format(filename)
    raw = fetch_bytes(url)
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
        pnum_m  = re.search(r'<hi rend="paranum">\s*(\d+)\s*</hi>', body)
        paranum = pnum_m.group(1) if pnum_m else ''
        body    = re.sub(r'<hi rend="(?:paranum|dot)">[^<]*</hi>', '', body)
        text    = clean_xml(body)
        if text:
            results.append((rend, paranum, text))
    return results


def extract_section(paras, section_pattern):
    """
    Extract paragraphs for one sutta's sub-commentary.
    If section_pattern is None, return all paragraphs.
    Otherwise find the matching heading and return until the next
    same-level sutta heading or end of file.
    """
    if section_pattern is None:
        return paras

    pat = re.compile(section_pattern)
    # Stop pattern: another numbered sutta/vagga heading (but not our own)
    stop_pat = re.compile(r'^\d+\.\s+\S+(?:sutta|vagga|Vagga|Sutta)', re.IGNORECASE)
    start = None
    for i, (rend, pnum, text) in enumerate(paras):
        if start is None:
            if pat.search(text):
                start = i
        else:
            if stop_pat.match(text) and not pat.search(text):
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


# ── file assembly ─────────────────────────────────────────────────────────────

def build_tik_file(sc_id, nikaya_dir, slug, sutta_code, pali_title, en_title,
                   nikaya_label, commentary_name, pali_body):
    nav_link      = f"[[tika/sutta/{nikaya_dir}/INDEX|{nikaya_label}]]"
    mula_link     = f"[[{slug}|{pali_title} — {en_title}]]"
    att_slug      = f"{slug}_att"
    att_link      = f"[[{att_slug}|{pali_title}vaṇṇanā (atthakathā)]]"

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
        f"att_file: [[{att_slug}]]",
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


# ── index management ──────────────────────────────────────────────────────────

def ensure_tika_dirs(nikaya_dir, nikaya_label):
    """Create tika/sutta/{nikaya} directory and INDEX.md if needed."""
    tika_dir = os.path.join(VAULT, "tika/sutta", nikaya_dir)
    os.makedirs(tika_dir, exist_ok=True)
    idx = os.path.join(tika_dir, "Tika-Index.md")
    if not os.path.exists(idx):
        short = nikaya_dir.replace('_nikaya', '').capitalize()
        content = "\n".join([
            "---",
            "type: index",
            "pitaka: sutta",
            f"nikaya: {nikaya_dir.replace('_nikaya','')}",
            "layer: tika",
            "---",
            "",
            f"# {nikaya_label} — Ṭīkā",
            "",
            f"**Navigation**: [[INDEX|Pali Canon Vault]] / [[tika/Tika-Index|Ṭīkā]] / [[tika/sutta/Tika-Sutta-Index|Sutta]]",
            "",
            "## Migrated Texts",
            "",
            "| Sutta | Sub-commentary | Pali Source | Words |",
            "|---|---|---|---|",
            "",
        ])
        with open(idx, 'w', encoding='utf-8') as f:
            f.write(content)
    return tika_dir


def update_tika_index(nikaya_dir, slug, sutta_code, pali_title, word_count):
    """Append a row to the tika nikaya INDEX.md."""
    idx = os.path.join(VAULT, "tika/sutta", nikaya_dir, "Tika-Samyutta-Index.md")
    with open(idx, 'r', encoding='utf-8') as f:
        content = f.read()
    row = f"| [[{slug}|{sutta_code}]] | [[{slug}_tik|{pali_title}vaṇṇanātīkā]] | tipitaka.org CSCD | {word_count:,} |\n"
    with open(idx, 'a', encoding='utf-8') as f:
        f.write(row)


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    # Ensure top-level tika/sutta INDEX.md exists
    tika_sutta_dir = os.path.join(VAULT, "tika/sutta")
    os.makedirs(tika_sutta_dir, exist_ok=True)
    top_idx = os.path.join(tika_sutta_dir, "Tika-Sutta-Index.md")
    if not os.path.exists(top_idx):
        with open(top_idx, 'w', encoding='utf-8') as f:
            f.write("---\ntype: index\npitaka: sutta\nlayer: tika\n---\n\n"
                    "# Sutta Piṭaka — Ṭīkā\n\n"
                    "**Navigation**: [[INDEX|Pali Canon Vault]] / [[tika/Tika-Index|Ṭīkā]]\n\n"
                    "## Nikāyas\n\n"
                    "- [[tika/sutta/majjhima_nikaya/Tika-Majjhima-Index|Majjhima Nikāya]]\n"
                    "- [[tika/sutta/digha_nikaya/Tika-Digha-Index|Dīgha Nikāya]]\n"
                    "- [[tika/sutta/anguttara_nikaya/Tika-Anguttara-Index|Aṅguttara Nikāya]]\n")

    tracked_nikayas = set()

    for (sc_id, nikaya_dir, slug, sutta_code, pali_title, en_title,
         nikaya_label, cscd_file, section_pattern, commentary_name) in SUTTAS:

        print(f"\n{sutta_code}: {pali_title}")
        tika_dir = ensure_tika_dirs(nikaya_dir, nikaya_label)
        tracked_nikayas.add(nikaya_dir)

        # Fetch and parse Pali sub-commentary
        print(f"  Fetching {cscd_file} from tipitaka.org...", end=" ", flush=True)
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

        # Build and write file
        content = build_tik_file(
            sc_id, nikaya_dir, slug, sutta_code, pali_title, en_title,
            nikaya_label, commentary_name, pali_body
        )
        fname = f"{slug}_tik.md"
        out_path = os.path.join(tika_dir, fname)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(content + "\n")

        wc = len(content.split())
        print(f"  -> {fname}: {wc:,} words")

        update_tika_index(nikaya_dir, slug, sutta_code, pali_title, wc)

    print("\nDone.")


if __name__ == "__main__":
    main()
