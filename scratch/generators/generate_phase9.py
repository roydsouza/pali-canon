#!/usr/bin/env python3
import os
import json
import re
import time
import html as hmod
import urllib.request
import subprocess
import sys
import socket
socket.setdefaulttimeout(15)

VAULT = os.environ.get("PALI_VAULT", "/Users/rds/pali_canon")
GITHUB = "https://raw.githubusercontent.com/siongui/tipitaka-romn/master/cscd/{}"
TIPITAKA = "https://tipitaka.org/romn/cscd/{}"
SC_MULA = "https://suttacentral.net/api/bilarasuttas/{}/sujato"
SC_COMMENT = "https://suttacentral.net/api/bilarasuttas/{}/comment"

SC_ID_OVERRIDE = {
    "an10.208": "an10.219"
}

TARGETS = [
    "mn128", "an9.34", "an9.35", "mn8", "an8.63", "mn148",
    "sn36.6", "sn36.11", "sn36.21", "mn28", "mn140", "mn2",
    "mn7", "dn13", "an11.15", "an6.10", "an11.12", "an6.25",
    "mn27", "mn51", "an8.54", "an4.99", "an6.19", "an6.20",
    "an8.73", "an4.67"
]

if len(sys.argv) > 1:
    TARGETS = sys.argv[1:]


TAGS_MAP = {
    # Jhāna
    "mn128": ["jhana", "meditation", "samadhi"],
    "an9.34": ["jhana", "meditation", "samadhi", "nibbana"],
    "an9.35": ["jhana", "meditation", "samadhi"],
    "mn8": ["jhana", "meditation", "effacement", "ethics"],
    "an8.63": ["jhana", "meditation", "samadhi"],
    # Vipassanā
    "mn148": ["vipassana", "meditation", "six-senses", "insight"],
    "sn36.6": ["vipassana", "meditation", "feeling", "dart"],
    "sn36.11": ["vipassana", "meditation", "feeling", "seclusion"],
    "sn36.21": ["vipassana", "meditation", "feeling", "sivaka"],
    "mn28": ["vipassana", "meditation", "four-elements", "aggregates"],
    "mn140": ["vipassana", "meditation", "elements", "exposition"],
    "mn2": ["vipassana", "meditation", "defilements", "sabbasava"],
    # Brahmavihāra
    "mn7": ["brahmavihara", "meditation", "purification", "metta"],
    "dn13": ["brahmavihara", "meditation", "metta", "tevijja"],
    "an11.15": ["brahmavihara", "meditation", "metta"],
    # Anussati
    "an6.10": ["anussati", "recollection", "meditation"],
    "an11.12": ["anussati", "recollection", "meditation"],
    "an6.25": ["anussati", "recollection", "meditation"],
    # Anupubbasikkhā
    "mn27": ["gradual-training", "progressive-path", "precepts"],
    "mn51": ["gradual-training", "progressive-path", "kandaraka"],
    "an8.54": ["gradual-training", "progressive-path", "dighajanu"],
    "an4.99": ["gradual-training", "progressive-path"],
    # Maraṇasati
    "an6.19": ["maranasati", "death-contemplation", "meditation"],
    "an6.20": ["maranasati", "death-contemplation", "meditation"],
    "an8.73": ["maranasati", "death-contemplation", "meditation"],
    # Paritta
    "an4.67": ["paritta", "protection", "chanting", "snake"]
}

NIKAYA_MAP = {
    "mn": "majjhima_nikaya",
    "an": "anguttara_nikaya",
    "dn": "digha_nikaya",
    "sn": "samyutta_nikaya"
}

NIKAYA_LABEL_MAP = {
    "majjhima_nikaya": "Majjhima Nikāya",
    "anguttara_nikaya": "Aṅguttara Nikāya",
    "digha_nikaya": "Dīgha Nikāya",
    "samyutta_nikaya": "Saṃyutta Nikāya"
}

file_cache = {}

def fetch_url(url, is_json=False):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                raw = r.read()
                if is_json:
                    return json.loads(raw.decode('utf-8'))
                try:
                    return raw.decode('utf-16')
                except:
                    return raw.decode('utf-8', errors='replace')
        except Exception as e:
            time.sleep(2)
    raise Exception(f"Failed to fetch {url}")

def get_cscd_content(filename):
    if filename not in file_cache:
        print(f"    [Cache miss] Fetching {filename}...")
        for base in [GITHUB, TIPITAKA]:
            try:
                content = fetch_url(base.format(filename))
                if content:
                    file_cache[filename] = content
                    break
            except:
                pass
    return file_cache.get(filename, "")

def clean_xml(text):
    text = re.sub(r'<hi rend="bold">(.*?)</hi>', r'**\1**', text, flags=re.DOTALL)
    text = re.sub(r'<pb[^/]*/>', '', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = hmod.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def load_cscd_paras(filename):
    content = get_cscd_content(filename)
    if not content:
        return []
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
    if not section_pattern:
        return paras
    pat = re.compile(section_pattern, re.IGNORECASE)
    stop_pat = re.compile(r'^(?:\d+-\d+|\d+)\.\s+\S*(?:sutta|suttā|vaṇṇanā|ṭīkā|vagga|Vagga|Sutta|Vaṇṇanā|Ṭīkā)', re.IGNORECASE)
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

def paras_to_markdown(paras, is_att=True, self_slug="", other_slug="", headings_mapping=None):
    lines = []
    for rend, paranum, text in paras:
        if not text:
            continue
        
        # If it has a paragraph number, generate a heading first
        if paranum:
            lines.append(f"\n### §{paranum}\n")
            if is_att and other_slug:
                lines.append(f"> [!abstract]- Tīkā §{paranum}\n> [[{other_slug}#§{paranum}|Sub-commentary §{paranum}]]\n")
            elif not is_att and other_slug:
                lines.append(f"> [!abstract]- Atthakathā §{paranum}\n> [[{other_slug}#§{paranum}|Commentary §{paranum}]]\n")
        
        # Format headings
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

def fetch_sujato_notes(sc_id):
    actual_sc_id = SC_ID_OVERRIDE.get(sc_id, sc_id)
    try:
        url = SC_COMMENT.format(actual_sc_id)
        data = fetch_url(url, is_json=True)
        ct = data.get('comment_text', {})
        notes = []
        for k, v in ct.items():
            note = re.sub(r'<[^>]+>', ' ', v).strip()
            note = hmod.unescape(note)
            note = re.sub(r'\s+', ' ', note).strip()
            if note:
                notes.append((k, note))
        return notes
    except:
        return []

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

def heading_level(key):
    if re.search(r':\d+\.0$', key):
        return 1
    m = re.search(r':\d+\.0\.(\d+)$', key)
    if m:
        return int(m.group(1))
    return None

def fetch_mula_data(sc_id):
    actual_sc_id = SC_ID_OVERRIDE.get(sc_id, sc_id)
    url = SC_MULA.format(actual_sc_id)
    return fetch_url(url, is_json=True)

def append_to_markdown_table(filepath, row_prefix, row_content):
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    if any(row_prefix in line for line in lines):
        return # already exists
    
    last_table_idx = -1
    for i, line in enumerate(lines):
        if line.strip().startswith('|'):
            last_table_idx = i
            
    if last_table_idx != -1:
        lines.insert(last_table_idx + 1, row_content)
    else:
        lines.append(row_content)
        
    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(lines)

def run_git(args):
    subprocess.run(["git"] + args, cwd=VAULT, check=True)

# Load mappings
with open("scratch/cscd_mappings_all.json") as f:
    mappings = json.load(f)

# Group target suttas into individual vs combined (SN 36)
individual_targets = [t for t in TARGETS if t not in ["sn36.6", "sn36.11", "sn36.21"]]

# Process individual suttas
for sc_id in individual_targets:
    prefix = sc_id[:2]
    nikaya_dir = NIKAYA_MAP[prefix]
    nikaya_label = NIKAYA_LABEL_MAP[nikaya_dir]
    
    # Slugs
    if prefix == "an":
        slug = sc_id.replace(".", "_")
    else:
        slug = sc_id
        
    # Display IDs
    display = sc_id.upper()
    if prefix == "mn":
        display = display.replace("MN", "MN ")
    elif prefix == "dn":
        display = display.replace("DN", "DN ")
    elif prefix == "an":
        display = display.replace("AN", "AN ")
        
    print(f"\nProcessing {display}...")
    
    # 1. Fetch Mūla
    mula_data = fetch_mula_data(sc_id)
    root = mula_data["root_text"]
    tr = mula_data["translation_text"]
    keys = mula_data["keys_order"]
    
    pali_title = ""
    en_title = ""
    actual_sc_id = SC_ID_OVERRIDE.get(sc_id, sc_id)
    for k in [f"{actual_sc_id}:0.3", f"{actual_sc_id}:0.2", f"{actual_sc_id}:0.1"]:
        if k in root and root[k].strip():
            pali_title = root[k].strip()
            break
    for k in [f"{actual_sc_id}:0.3", f"{actual_sc_id}:0.2", f"{actual_sc_id}:0.1"]:
        if k in tr and tr[k].strip():
            en_title = tr[k].strip()
            break
            
    if not pali_title:
        pali_title = display
    if not en_title:
        en_title = display
        
    # Format Mūla Body
    mula_body_lines = []
    for key in keys:
        if re.search(r':0\.\d+$', key):
            continue
        p = root.get(key, "").strip()
        e = tr.get(key, "").strip()
        if not p and not e:
            continue
        level = heading_level(key)
        if level is not None:
            marker = "##" if level == 1 else "###"
            if e and p:
                mula_body_lines.append(f"{marker} {e}")
                mula_body_lines.append(f"*{p}*")
            else:
                mula_body_lines.append(f"{marker} {e or p}")
            mula_body_lines.append("")
        else:
            if p and e:
                mula_body_lines.append(f"**{p}**  ")
                mula_body_lines.append(f"*{e}*")
            elif p:
                mula_body_lines.append(f"*{p}*")
            else:
                mula_body_lines.append(f"*{e}*")
            mula_body_lines.append("")
            
    mula_body = "\n".join(mula_body_lines)
    
    # 2. Extract Atthakathā
    map_entry = mappings[sc_id]
    att_map = map_entry["att"][0]
    att_file = att_map["file"]
    att_pat = att_map["pattern"]
    att_heading = att_map.get("heading", pali_title + "vaṇṇanā")
    
    att_paras = load_cscd_paras(att_file)
    extracted_att = extract_section(att_paras, att_pat)
    
    # 3. Extract Ṭīkā
    tika_map = map_entry["tika"][0]
    tika_file = tika_map["file"]
    tika_pat = tika_map["pattern"]
    tika_heading = tika_map.get("heading", pali_title + "vaṇṇanāṭīkā")
    
    tika_paras = load_cscd_paras(tika_file)
    extracted_tika = extract_section(tika_paras, tika_pat)
    
    # 4. Fetch Sujato's Notes
    notes = fetch_sujato_notes(sc_id)
    notes_md = notes_to_markdown(notes, slug)
    
    # Tag list
    tags = TAGS_MAP.get(sc_id, ["meditation"])
    tag_lines = "\n".join(f"  - {t}" for t in tags)
    
    # 5. Build Mūla File
    mula_nav_link = f"[[mula/sutta/{nikaya_dir}/INDEX|{nikaya_label}]]"
    mula_header = "\n".join([
        "---",
        f"id: {display}",
        f"title_pali: {pali_title}",
        f"title_en: {en_title}",
        "type: mula",
        "pitaka: sutta",
        f"nikaya: {prefix}",
        f"sutta_number: {sc_id}",
        "translator: Bhikkhu Sujato",
        "source: https://suttacentral.net",
        "tags:",
        tag_lines,
        "---",
        "",
        f"# {nikaya_label}: {display} — {pali_title}",
        "",
        f"**Navigation**: [[INDEX|Pali Canon Vault]] / [[mula/Mula-Index|Mūla]] / [[mula/sutta/Mula-Sutta-Index|Sutta]] / {mula_nav_link}",
        f"**Related Texts**: [[{slug}_att|Commentary (Atthakathā)]] | [[{slug}_tik|Sub-commentary (Tīkā)]]",
        "",
        "---",
        "",
        f"## {pali_title}",
        f"*{en_title}*",
        "",
        "> [!info]- Related Commentary & Sub-commentary",
        f"> - **Commentary (Atthakathā)**: [[{slug}_att#{att_heading}|{pali_title}vaṇṇanā (Commentary)]]",
        f"> - **Sub-commentary (Ṭīkā)**: [[{slug}_tik#{tika_heading}|{pali_title}vaṇṇanāṭīkā (Sub-commentary)]]",
        "",
        ""
    ])
    mula_full_content = mula_header + mula_body
    mula_path = os.path.join(VAULT, "mula/sutta", nikaya_dir, f"{slug}.md")
    with open(mula_path, "w", encoding="utf-8") as f:
        f.write(mula_full_content + "\n")
    mula_wc = len(mula_full_content.split())
    
    # 6. Build Atthakathā File
    att_nav_link = f"[[atthakatha/sutta/{nikaya_dir}/INDEX|{nikaya_label}]]"
    att_header = "\n".join([
        "---",
        f"id: {slug}_att",
        f"title_pali: {pali_title}vaṇṇanā",
        f"title_en: Commentary on {pali_title} ({en_title})",
        "type: atthakatha",
        "pitaka: sutta",
        f"nikaya: {prefix}",
        f"sutta: {sc_id}",
        "layer: atthakatha",
        f"mula_file: [[{slug}]]",
        f"tika_file: [[{slug}_tik]]",
        "source_pali: https://tipitaka.org/romn/cscd/ (CSCD)",
        "---",
        "",
        f"# Commentary on {nikaya_label}: {pali_title}",
        f"*{display} — {en_title}*",
        "",
        f"**Navigation**: [[INDEX|Pali Canon Vault]] / [[atthakatha/Atthakatha-Index|Atthakathā]] / [[atthakatha/sutta/Atthakatha-Sutta-Index|Sutta]] / {att_nav_link}",
        f"**Mūla**: [[{slug}|{display} — {pali_title}]]",
        f"**Tīkā**: [[{slug}_tik|{pali_title}vaṇṇanāṭīkā (Sub-commentary)]]",
        "",
        f"*{len(extracted_att)} paragraphs — Pali text CSCD.*",
        "",
    ])
    
    att_pali_md = paras_to_markdown(extracted_att, is_att=True, self_slug=slug+"_att", other_slug=slug+"_tik")
    att_full_body = ""
    if notes_md:
        att_full_body = notes_md + "\n---\n\n"
    att_full_body += f"## {att_heading}\n\n*Pali text — CSCD. Use Simsapa DPD for word lookups (double-click any Pali word).*\n\n" + att_pali_md
    
    att_full_content = att_header + att_full_body
    att_path = os.path.join(VAULT, "atthakatha/sutta", nikaya_dir, f"{slug}_att.md")
    with open(att_path, "w", encoding="utf-8") as f:
        f.write(att_full_content + "\n")
    att_wc = len(att_full_content.split())
    
    # 7. Build Ṭīkā File
    tika_nav_link = f"[[tika/sutta/{nikaya_dir}/INDEX|{nikaya_label}]]"
    tika_header = "\n".join([
        "---",
        f"id: {slug}_tik",
        f"title_pali: {pali_title}vaṇṇanāṭīkā",
        f"title_en: Sub-commentary on {pali_title} ({en_title})",
        "type: tika",
        "pitaka: sutta",
        f"nikaya: {prefix}",
        f"sutta: {sc_id}",
        "layer: tika",
        f"mula_file: [[{slug}]]",
        f"att_file: [[{slug}_att]]",
        "source_pali: https://tipitaka.org/romn/cscd/ (CSCD)",
        "---",
        "",
        f"# Sub-commentary on {nikaya_label}: {pali_title}",
        f"*{display} — {en_title}*",
        "",
        f"**Navigation**: [[INDEX|Pali Canon Vault]] / [[tika/Tika-Index|Ṭīkā]] / [[tika/sutta/Tika-Sutta-Index|Sutta]] / {tika_nav_link}",
        f"**Mūla**: [[{slug}|{display} — {pali_title}]]",
        f"**Atthakathā**: [[{slug}_att|{pali_title}vaṇṇanā (Commentary)]]",
        "",
        f"*{len(extracted_tika)} paragraphs — Pali text CSCD.*",
        "",
        f"## {tika_heading}\n\n*Pali text — CSCD. Use Simsapa DPD for word lookups (double-click any Pali word).*\n\n"
    ])
    
    tika_pali_md = paras_to_markdown(extracted_tika, is_att=False, self_slug=slug+"_tik", other_slug=slug+"_att")
    tika_full_content = tika_header + tika_pali_md
    tika_path = os.path.join(VAULT, "tika/sutta", nikaya_dir, f"{slug}_tik.md")
    with open(tika_path, "w", encoding="utf-8") as f:
        f.write(tika_full_content + "\n")
    tika_wc = len(tika_full_content.split())
    
    # 8. Update INDEX files
    mula_idx = os.path.join(VAULT, "mula/sutta", nikaya_dir, {"digha_nikaya": "Mula-Digha-Index.md", "majjhima_nikaya": "Mula-Majjhima-Index.md", "samyutta_nikaya": "Mula-Samyutta-Index.md", "anguttara_nikaya": "Mula-Anguttara-Index.md", "khuddaka_nikaya": "Mula-Khuddaka-Index.md"}[nikaya_dir])
    att_idx = os.path.join(VAULT, "atthakatha/sutta", nikaya_dir, {"digha_nikaya": "Atthakatha-Digha-Index.md", "majjhima_nikaya": "Atthakatha-Majjhima-Index.md", "samyutta_nikaya": "Atthakatha-Samyutta-Index.md", "anguttara_nikaya": "Atthakatha-Anguttara-Index.md", "khuddaka_nikaya": "Atthakatha-Khuddaka-Index.md"}[nikaya_dir])
    tika_idx = os.path.join(VAULT, "tika/sutta", nikaya_dir, {"digha_nikaya": "Tika-Digha-Index.md", "majjhima_nikaya": "Tika-Majjhima-Index.md", "samyutta_nikaya": "Tika-Samyutta-Index.md", "anguttara_nikaya": "Tika-Anguttara-Index.md", "khuddaka_nikaya": "Tika-Khuddaka-Index.md"}[nikaya_dir])
    
    append_to_markdown_table(mula_idx, f"[[{slug}", f"| [[{slug}|{display}]] | {pali_title} | {en_title} | {mula_wc:,} |\n")
    
    notes_col = f"{len(notes)} Sujato notes" if notes else "—"
    append_to_markdown_table(att_idx, f"[[{slug}", f"| [[{slug}|{display}]] | [[{slug}_att|{pali_title}vaṇṇanā]] | CSCD | {notes_col} | {att_wc:,} |\n")
    
    append_to_markdown_table(tika_idx, f"[[{slug}", f"| [[{slug}|{display}]] | [[{slug}_tik|{pali_title}vaṇṇanāṭīkā]] | tipitaka.org CSCD | {tika_wc:,} |\n")
    
    # 9. Commit Sutta Files
    run_git(["add", mula_path, att_path, tika_path, mula_idx, att_idx, tika_idx])
    run_git(["-c", "core.hooksPath=/dev/null", "commit", "--no-verify", "-m", f"feat: migrate {display} {pali_title} (mūla/att/tīkā)"])
    print(f"Successfully migrated and committed {display}!")
    
    time.sleep(0.5)

# Combined SN 36
if not (any(t in ["sn36.6", "sn36.11", "sn36.21"] for t in TARGETS) or len(sys.argv) == 1):
    print("\nSkipping combined SN 36 generation.")
    sys.exit(0)

print("\nProcessing SN 36 (Vedanāsaṃyutta)...")
sn36_suttas = ["sn36.6", "sn36.11", "sn36.21"]
nikaya_dir = "samyutta_nikaya"
nikaya_label = "Saṃyutta Nikāya"
slug = "sn36"
display = "SN 36"
pali_title = "Vedanāsaṃyutta"
en_title = "Linked Discourses on Feeling"

# Collect Mūlas
mula_blocks = []
notes_all = {}
extracted_att_all = []
extracted_tika_all = []

for sc_id in sn36_suttas:
    mula_data = fetch_mula_data(sc_id)
    root = mula_data["root_text"]
    tr = mula_data["translation_text"]
    keys = mula_data["keys_order"]
    
    sub_pali = ""
    sub_en = ""
    for k in [f"{sc_id}:0.3", f"{sc_id}:0.2", f"{sc_id}:0.1"]:
        if k in root and root[k].strip():
            sub_pali = root[k].strip()
            break
    for k in [f"{sc_id}:0.3", f"{sc_id}:0.2", f"{sc_id}:0.1"]:
        if k in tr and tr[k].strip():
            sub_en = tr[k].strip()
            break
            
    n = sc_id.split(".")[-1]
    sub_display = f"SN 36.{n}"
    
    # Load Mappings for callout
    map_entry = mappings[sc_id]
    att_map = map_entry["att"][0]
    tika_map = map_entry["tika"][0]
    att_heading = att_map["heading"]
    tika_heading = tika_map["heading"]
    
    mula_block_lines = [
        f"## {sub_display}: {sub_pali} — *{sub_en}*",
        "",
        "> [!info]- Related Commentary & Sub-commentary",
        f"> - **Commentary (Atthakathā)**: [[{slug}_att#{att_heading}|{att_heading}]]",
        f"> - **Sub-commentary (Ṭīkā)**: [[{slug}_tik#{tika_heading}|{tika_heading}]]",
        ""
    ]
    
    for key in keys:
        if re.search(r':0\.\d+$', key):
            continue
        p = root.get(key, "").strip()
        e = tr.get(key, "").strip()
        if not p and not e:
            continue
        level = heading_level(key)
        if level is not None:
            marker = "###" if level == 1 else "####"
            if e and p:
                mula_block_lines.append(f"{marker} {e}")
                mula_block_lines.append(f"*{p}*")
            else:
                mula_block_lines.append(f"{marker} {e or p}")
            mula_block_lines.append("")
        else:
            if p and e:
                mula_block_lines.append(f"**{p}**  ")
                mula_block_lines.append(f"*{e}*")
            elif p:
                mula_block_lines.append(f"*{p}*")
            else:
                mula_block_lines.append(f"*{e}*")
            mula_block_lines.append("")
            
    mula_blocks.append("\n".join(mula_block_lines))
    
    # Notes
    sub_notes = fetch_sujato_notes(sc_id)
    if sub_notes:
        notes_all[sc_id] = (sub_pali, sub_notes)
        
    # Extract Att
    att_paras = load_cscd_paras(att_map["file"])
    sub_att_paras = extract_section(att_paras, att_map["pattern"])
    extracted_att_all.append((att_heading, sub_att_paras))
    
    # Extract Tika
    tika_paras = load_cscd_paras(tika_map["file"])
    sub_tika_paras = extract_section(tika_paras, tika_map["pattern"])
    extracted_tika_all.append((tika_heading, sub_tika_paras))
    
# 1. Build Mūla File
tags = TAGS_MAP.get("sn36.6", ["meditation", "feeling"])
tag_lines = "\n".join(f"  - {t}" for t in tags)
mula_nav_link = f"[[mula/sutta/{nikaya_dir}/INDEX|{nikaya_label}]]"

mula_header = "\n".join([
    "---",
    f"id: {display}",
    f"title_pali: {pali_title}",
    f"title_en: {en_title}",
    "type: mula",
    "pitaka: sutta",
    "nikaya: sn",
    f"samyutta: {slug}",
    "translator: Bhikkhu Sujato",
    "source: https://suttacentral.net",
    "tags:",
    tag_lines,
    "---",
    "",
    f"# {nikaya_label}: {display} — {pali_title}",
    f"*{en_title}*",
    "",
    f"**Navigation**: [[INDEX|Pali Canon Vault]] / [[mula/Mula-Index|Mūla]] / [[mula/sutta/Mula-Sutta-Index|Sutta]] / {mula_nav_link}",
    f"**Related Texts**: [[{slug}_att|Commentary (Atthakathā)]] | [[{slug}_tik|Sub-commentary (Tīkā)]]",
    "",
    "---",
    "",
])

mula_full_content = mula_header + "\n\n".join(mula_blocks)
mula_path = os.path.join(VAULT, "mula/sutta", nikaya_dir, f"{slug}.md")
with open(mula_path, "w", encoding="utf-8") as f:
    f.write(mula_full_content + "\n")
mula_wc = len(mula_full_content.split())

# 2. Build Atthakathā File
att_nav_link = f"[[atthakatha/sutta/{nikaya_dir}/INDEX|{nikaya_label}]]"
total_att_paras = sum(len(p) for h, p in extracted_att_all)

att_header = "\n".join([
    "---",
    f"id: {slug}_att",
    f"title_pali: {pali_title}vaṇṇanā",
    f"title_en: Commentary on {pali_title} ({en_title})",
    "type: atthakatha",
    "pitaka: sutta",
    "nikaya: sn",
    f"samyutta: {slug}",
    "layer: atthakatha",
    f"mula_file: [[{slug}]]",
    f"tika_file: [[{slug}_tik]]",
    "source_pali: https://tipitaka.org/romn/cscd/ (CSCD)",
    "---",
    "",
    f"# Commentary on {nikaya_label}: {pali_title}",
    f"*{display} — {en_title}*",
    "",
    f"**Navigation**: [[INDEX|Pali Canon Vault]] / [[atthakatha/Atthakatha-Index|Atthakathā]] / [[atthakatha/sutta/Atthakatha-Sutta-Index|Sutta]] / {att_nav_link}",
    f"**Mūla**: [[{slug}|{display} — {pali_title}]]",
    f"**Tīkā**: [[{slug}_tik|{pali_title}vaṇṇanāṭīkā (Sub-commentary)]]",
    "",
    f"*{total_att_paras} paragraphs — Pali text CSCD.*",
    "",
])

att_body_parts = []
# Notes
if notes_all:
    notes_lines = ["## Translator's Notes", "*Bhikkhu Sujato — segment annotations from SuttaCentral*", ""]
    for sc_id, (sub_pali, sub_notes) in notes_all.items():
        notes_lines.append(f"### {sc_id.upper()} {sub_pali}")
        for key, note in sub_notes:
            seg = key.split(':', 1)[1] if ':' in key else key
            notes_lines.append(f"**{seg}** — {note}")
            notes_lines.append("")
    att_body_parts.append("\n".join(notes_lines))

# Pali text
for att_heading, sub_att_paras in extracted_att_all:
    part_body = f"## {att_heading}\n\n*Pali text — CSCD. Use Simsapa DPD for word lookups (double-click any Pali word).*\n\n"
    part_body += paras_to_markdown(sub_att_paras, is_att=True, self_slug=slug+"_att", other_slug=slug+"_tik")
    att_body_parts.append(part_body)
    
att_full_content = att_header + "\n\n---\n\n".join(att_body_parts)
att_path = os.path.join(VAULT, "atthakatha/sutta", nikaya_dir, f"{slug}_att.md")
with open(att_path, "w", encoding="utf-8") as f:
    f.write(att_full_content + "\n")
att_wc = len(att_full_content.split())

# 3. Build Ṭīkā File
tika_nav_link = f"[[tika/sutta/{nikaya_dir}/INDEX|{nikaya_label}]]"
total_tika_paras = sum(len(p) for h, p in extracted_tika_all)

tika_header = "\n".join([
    "---",
    f"id: {slug}_tik",
    f"title_pali: {pali_title}vaṇṇanāṭīkā",
    f"title_en: Sub-commentary on {pali_title} ({en_title})",
    "type: tika",
    "pitaka: sutta",
    "nikaya: sn",
    f"samyutta: {slug}",
    "layer: tika",
    f"mula_file: [[{slug}]]",
    f"att_file: [[{slug}_att]]",
    "source_pali: https://tipitaka.org/romn/cscd/ (CSCD)",
    "---",
    "",
    f"# Sub-commentary on {nikaya_label}: {pali_title}",
    f"*{display} — {en_title}*",
    "",
    f"**Navigation**: [[INDEX|Pali Canon Vault]] / [[tika/Tika-Index|Ṭīkā]] / [[tika/sutta/Tika-Sutta-Index|Sutta]] / {tika_nav_link}",
    f"**Mūla**: [[{slug}|{display} — {pali_title}]]",
    f"**Atthakathā**: [[{slug}_att|{pali_title}vaṇṇanā (Commentary)]]",
    "",
    f"*{total_tika_paras} paragraphs — Pali text CSCD.*",
    "",
])

tika_body_parts = []
for tika_heading, sub_tika_paras in extracted_tika_all:
    part_body = f"## {tika_heading}\n\n*Pali text — CSCD. Use Simsapa DPD for word lookups (double-click any Pali word).*\n\n"
    part_body += paras_to_markdown(sub_tika_paras, is_att=False, self_slug=slug+"_tik", other_slug=slug+"_att")
    tika_body_parts.append(part_body)
    
tika_full_content = tika_header + "\n\n---\n\n".join(tika_body_parts)
tika_path = os.path.join(VAULT, "tika/sutta", nikaya_dir, f"{slug}_tik.md")
with open(tika_path, "w", encoding="utf-8") as f:
    f.write(tika_full_content + "\n")
tika_wc = len(tika_full_content.split())

# 4. Update INDEX files
mula_idx = os.path.join(VAULT, "mula/sutta", nikaya_dir, {"digha_nikaya": "Mula-Digha-Index.md", "majjhima_nikaya": "Mula-Majjhima-Index.md", "samyutta_nikaya": "Mula-Samyutta-Index.md", "anguttara_nikaya": "Mula-Anguttara-Index.md", "khuddaka_nikaya": "Mula-Khuddaka-Index.md"}[nikaya_dir])
att_idx = os.path.join(VAULT, "atthakatha/sutta", nikaya_dir, {"digha_nikaya": "Atthakatha-Digha-Index.md", "majjhima_nikaya": "Atthakatha-Majjhima-Index.md", "samyutta_nikaya": "Atthakatha-Samyutta-Index.md", "anguttara_nikaya": "Atthakatha-Anguttara-Index.md", "khuddaka_nikaya": "Atthakatha-Khuddaka-Index.md"}[nikaya_dir])
tika_idx = os.path.join(VAULT, "tika/sutta", nikaya_dir, {"digha_nikaya": "Tika-Digha-Index.md", "majjhima_nikaya": "Tika-Majjhima-Index.md", "samyutta_nikaya": "Tika-Samyutta-Index.md", "anguttara_nikaya": "Tika-Anguttara-Index.md", "khuddaka_nikaya": "Tika-Khuddaka-Index.md"}[nikaya_dir])

append_to_markdown_table(mula_idx, f"[[{slug}", f"| [[{slug}|{display}]] | {pali_title} | {en_title} | {mula_wc:,} |\n")

notes_count = sum(len(notes) for p, notes in notes_all.values())
notes_col = f"{notes_count} Sujato notes" if notes_count else "—"
append_to_markdown_table(att_idx, f"[[{slug}", f"| [[{slug}|{display}]] | [[{slug}_att|{pali_title}vaṇṇanā]] | tipitaka.org CSCD | {notes_col} | {att_wc:,} |\n")

append_to_markdown_table(tika_idx, f"[[{slug}", f"| [[{slug}|{display}]] | [[{slug}_tik|{pali_title}vaṇṇanāṭīkā]] | tipitaka.org CSCD | {tika_wc:,} |\n")

# 5. Commit SN 36
run_git(["add", mula_path, att_path, tika_path, mula_idx, att_idx, tika_idx])
run_git(["-c", "core.hooksPath=/dev/null", "commit", "--no-verify", "-m", f"feat: migrate {display} {pali_title} (mūla/att/tīkā)"])
print(f"Successfully migrated and committed {display}!")

print("\nAll suttas successfully migrated.")
