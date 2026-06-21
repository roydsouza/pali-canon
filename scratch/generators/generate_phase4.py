import os
import json
import re
import time
import html as hmod
import urllib.request

VAULT = os.environ.get("PALI_VAULT", "/Users/rds/pali_canon")
SC_API = "https://suttacentral.net/api/bilarasuttas/{}/sujato"
SC_COMMENT = "https://suttacentral.net/api/bilarasuttas/{}/comment"
CSCD_GITHUB = "https://raw.githubusercontent.com/siongui/tipitaka-romn/master/cscd/{}"
CSCD_TIPITAKA = "https://tipitaka.org/romn/cscd/{}"

def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def fetch_bytes(filename):
    for base in [CSCD_GITHUB, CSCD_TIPITAKA]:
        url = base.format(filename)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read()
        except Exception as e:
            print(f"Fetch failed for {url}: {e}")
    raise RuntimeError(f"Could not fetch {filename} from any source.")

def clean_xml(text):
    text = re.sub(r'<hi rend="bold">(.*?)</hi>', r'**\1**', text, flags=re.DOTALL)
    text = re.sub(r'<pb[^/]*/>', '', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = hmod.unescape(text)
    return re.sub(r'\s+', ' ', text).strip()

def strip_html(text):
    text = re.sub(r'<[^>]+>', ' ', text)
    text = hmod.unescape(text)
    return re.sub(r'\s+', ' ', text).strip()

def load_cscd_paras(filename):
    raw = fetch_bytes(filename)
    try:
        content = raw.decode('utf-16')
    except:
        content = raw.decode('utf-8', errors='replace')
    results = []
    for m in re.finditer(r'<p([^>]*)>(.*?)</p>', content, re.DOTALL):
        attrs = m.group(1)
        body = m.group(2)
        rend_m = re.search(r'rend="([^"]+)"', attrs)
        rend = rend_m.group(1) if rend_m else ''
        pnum_m = re.search(r'<hi rend="paranum">\s*(\d+)\s*</hi>', body)
        paranum = pnum_m.group(1) if pnum_m else ''
        body = re.sub(r'<hi rend="(?:paranum|dot)">[^<]*</hi>', '', body)
        text = clean_xml(body)
        if text:
            results.append((rend, paranum, text))
    return results

def fetch_sujato_notes(sc_id):
    try:
        data = fetch_json(SC_COMMENT.format(sc_id))
        ct = data.get('comment_text', {})
        notes = []
        for k, v in ct.items():
            note = strip_html(v).strip()
            if note:
                notes.append((k, note))
        return notes
    except Exception as e:
        print(f"  Note fetch failed/none for {sc_id}: {e}")
        return []

def notes_to_markdown(notes, slug):
    if not notes:
        return ""
    mula_path = f"[[{slug}|{slug.upper().replace('_','.')}]]"
    lines = [
        "## Translator's Notes",
        "*Bhikkhu Sujato — segment annotations from SuttaCentral*",
        f"*Mūla file: {mula_path}*",
        ""
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

def is_meta(key):
    return bool(re.search(r':0\.\d+$', key))

# ── MN 19 Mūla ────────────────────────────────────────────────────────────────
def make_mn19_mula(data):
    root = data["root_text"]
    tr = data["translation_text"]
    keys = data["keys_order"]
    
    lines = [
        "---",
        "id: MN19",
        "title_pali: Dvedhāvitakkasutta",
        "title_en: Two Kinds of Thought",
        "type: mula",
        "pitaka: sutta",
        "nikaya: majjhima",
        "sutta_number: mn19",
        "translator: Bhikkhu Sujato",
        "source: https://suttacentral.net",
        "tags:",
        "  - meditation",
        "  - thought-management",
        "  - right-resolve",
        "---",
        "",
        "# Majjhima Nikāya 19: Dvedhāvitakkasutta",
        "",
        "**Navigation**: [[INDEX|Pali Canon Vault]] / [[mula/Mula-Index|Mūla]] / [[mula/sutta/Mula-Sutta-Index|Sutta]] / [[mula/sutta/majjhima_nikaya/Mula-Majjhima-Index|Majjhima Nikāya]]",
        "**Related Texts**: [[mn19_att|Commentary (Atthakathā)]] | [[mn19_tik|Sub-commentary (Ṭīkā)]]",
        "",
        "## Dvedhāvitakkasutta",
        "*Two Kinds of Thought*",
        ""
    ]
    
    callouts = {
        "mn19:2.2": (206, "Two kinds of thought (dvedhāvitakka)"),
        "mn19:3.1": (207, "Sensual thoughts (kāmavitakka)"),
        "mn19:4-5.1": (208, "Malicious thoughts (byāpādavitakka)"),
        "mn19:8.1": (209, "Thoughts of renunciation (nekkhammavitakka)"),
        "mn19:9-10.1": (210, "Thoughts of good will (abyāpādavitakka)"),
        "mn19:25.1": (215, "Simile of the marsh and deer (seyyathāpi araññe)")
    }
    
    for key in keys:
        if is_meta(key):
            continue
        p = root.get(key, "").strip()
        e = tr.get(key, "").strip()
        if not p and not e:
            continue
            
        level = heading_level(key)
        if level is not None:
            marker = "##" if level == 1 else "###"
            lines.append(f"{marker} {e}\n*{p}*\n")
        else:
            if key in callouts:
                pnum, label = callouts[key]
                lines.append(f"\n> [!info]- Commentary — {label}\n> **Atthakathā**: [[mn19_att#§{pnum}|Papañcasūdanī §{pnum}]]  ·  **Tīkā**: [[mn19_tik#§{pnum}|Ṭīkā §{pnum}]]\n")
            
            if p and e:
                lines.append(f"**{p}**  ")
                lines.append(f"*{e}*")
            elif p:
                lines.append(f"*{p}*")
            else:
                lines.append(f"*{e}*")
            lines.append("")
            
    return "\n".join(lines)

# ── AN 10.60 Mūla ─────────────────────────────────────────────────────────────
def make_an10_60_mula(data):
    root = data["root_text"]
    tr = data["translation_text"]
    keys = data["keys_order"]
    
    lines = [
        "---",
        "id: AN10.60",
        "title_pali: Girimānandasutta",
        "title_en: With Girimānanda",
        "type: mula",
        "pitaka: sutta",
        "nikaya: anguttara",
        "sutta_number: an10.60",
        "translator: Bhikkhu Sujato",
        "source: https://suttacentral.net",
        "tags:",
        "  - meditation",
        "  - perceptions",
        "  - breath-meditation",
        "  - healing",
        "---",
        "",
        "# Aṅguttara Nikāya 10.60: Girimānandasutta",
        "",
        "**Navigation**: [[INDEX|Pali Canon Vault]] / [[mula/Mula-Index|Mūla]] / [[mula/sutta/Mula-Sutta-Index|Sutta]] / [[mula/sutta/anguttara_nikaya/Mula-Anguttara-Index|Aṅguttara Nikāya]]",
        "**Related Texts**: [[an10_60_att|Commentary (Atthakathā)]] | (No Ṭīkā available)",
        "",
        "## Girimānandasutta",
        "*With Girimānanda*",
        ""
    ]
    
    callouts = {
        "an10.60:2.2": (60, "Out of sympathy (anukampaṃ upādāya)")
    }
    
    for key in keys:
        if is_meta(key):
            continue
        p = root.get(key, "").strip()
        e = tr.get(key, "").strip()
        if not p and not e:
            continue
            
        level = heading_level(key)
        if level is not None:
            marker = "###" if level == 1 else "####"
            lines.append(f"{marker} {e}\n*{p}*\n")
        else:
            if key in callouts:
                pnum, label = callouts[key]
                lines.append(f"\n> [!info]- Commentary — {label}\n> **Atthakathā**: [[an10_60_att#§{pnum}|Manorathapūraṇī §{pnum}]]  ·  **Tīkā**: (No Ṭīkā available)\n")
            
            if p and e:
                lines.append(f"**{p}**  ")
                lines.append(f"*{e}*")
            elif p:
                lines.append(f"*{p}*")
            else:
                lines.append(f"*{e}*")
            lines.append("")
            
    return "\n".join(lines)

# ── MN 19 Atthakathā ──────────────────────────────────────────────────────────
def make_mn19_att(paras, notes_body):
    header = "\n".join([
        "---",
        "id: MN19_att",
        "title_pali: Dvedhāvitakkasuttavaṇṇanā",
        "title_en: Commentary on Dvedhāvitakkasutta",
        "type: atthakatha",
        "pitaka: sutta",
        "nikaya: majjhima",
        "sutta: mn19",
        "layer: atthakatha",
        "mula_file: [[mn19]]",
        "tika_file: [[mn19_tik]]",
        "source_pali: https://github.com/siongui/tipitaka-romn (CSCD)",
        "source_notes: https://suttacentral.net",
        "---",
        "",
        "# Commentary on Majjhima Nikāya 19: Dvedhāvitakkasutta",
        "",
        "**Navigation**: [[INDEX|Pali Canon Vault]] / [[atthakatha/Atthakatha-Index|Atthakathā]] / [[atthakatha/sutta/Atthakatha-Sutta-Index|Sutta]] / [[atthakatha/sutta/majjhima_nikaya/Atthakatha-Majjhima-Index|Majjhima Nikāya]]",
        "**Mūla**: [[mn19|Dvedhāvitakkasutta — Two Kinds of Thought]]",
        "**Tīkā**: [[mn19_tik|Dvedhāvitakkasuttavaṇṇanātīkā (Sub-commentary)]]",
        "",
        "*Papañcasūdanī (Majjhima Nikāya Atthakathā)*",
        ""
    ])
    
    body_lines = [
        "## Dvedhāvitakkasuttavaṇṇanā",
        "",
        "*Pali text — CSCD (Chattha Sangayana Tipitaka). Use Simsapa DPD for word lookups (double-click any Pali word).*",
        ""
    ]
    
    current_pnum = None
    for rend, pnum, text in paras:
        if pnum:
            if current_pnum:
                body_lines.append(f"\n> [!abstract]- Tīkā §{current_pnum}\n> [[mn19_tik#§{current_pnum}|Papañcasūdanī-ṭīkā §{current_pnum}]]\n")
            current_pnum = int(pnum)
            body_lines.append(f"\n### §{pnum}\n")
            
        if rend == "subhead":
            body_lines.append(f"### {text}\n")
        elif rend == "centre":
            body_lines.append(f"\n{text}\n")
        elif rend in ('gatha', 'gathalast', 'indent'):
            body_lines.append(f"  {text}  ")
        else:
            prefix = f"({pnum}) " if pnum else ""
            body_lines.append(f"{prefix}{text}\n")
            
    if current_pnum:
        body_lines.append(f"\n> [!abstract]- Tīkā §{current_pnum}\n> [[mn19_tik#§{current_pnum}|Papañcasūdanī-ṭīkā §{current_pnum}]]\n")
        
    parts = [header]
    if notes_body:
        parts.append(notes_body)
        parts.append("\n---\n")
    parts.append("\n".join(body_lines))
    return "\n".join(parts)

# ── MN 19 Tīkā ────────────────────────────────────────────────────────────────
def make_mn19_tik(paras):
    header = "\n".join([
        "---",
        "id: MN19_tik",
        "title_pali: Dvedhāvitakkasuttavaṇṇanātīkā",
        "title_en: Sub-commentary on Dvedhāvitakkasutta",
        "type: tika",
        "pitaka: sutta",
        "nikaya: majjhima",
        "sutta: mn19",
        "layer: tika",
        "mula_file: [[mn19]]",
        "att_file: [[mn19_att]]",
        "source_pali: https://tipitaka.org/romn/cscd/ (CSCD)",
        "---",
        "",
        "# Sub-commentary on Majjhima Nikāya 19: Dvedhāvitakkasutta",
        "",
        "**Navigation**: [[INDEX|Pali Canon Vault]] / [[tika/Tika-Index|Ṭīkā]] / [[tika/sutta/Tika-Sutta-Index|Sutta]] / [[tika/sutta/majjhima_nikaya/Tika-Majjhima-Index|Majjhima Nikāya]]",
        "**Mūla**: [[mn19|Dvedhāvitakkasutta — Two Kinds of Thought]]",
        "**Atthakathā**: [[mn19_att|Dvedhāvitakkasuttavaṇṇanā (Atthakathā)]]",
        "",
        "*Papañcasūdanī-ṭīkā (Majjhima Nikāya Sub-commentary)*",
        ""
    ])
    
    body_lines = [
        "## Dvedhāvitakkasuttavaṇṇanātīkā",
        "",
        "*Pali text — CSCD (Chattha Sangayana Tipitaka). Use Simsapa DPD for word lookups (double-click any Pali word).*",
        ""
    ]
    
    for rend, pnum, text in paras:
        if pnum:
            body_lines.append(f"\n### §{pnum}\n")
            
        if rend == "subhead":
            body_lines.append(f"### {text}\n")
        elif rend == "centre":
            body_lines.append(f"\n{text}\n")
        elif rend in ('gatha', 'gathalast', 'indent'):
            body_lines.append(f"  {text}  ")
        else:
            prefix = f"({pnum}) " if pnum else ""
            body_lines.append(f"{prefix}{text}\n")
            
    return header + "\n" + "\n".join(body_lines)

# ── AN 10.60 Atthakathā ────────────────────────────────────────────────────────
def make_an10_60_att(paras, notes_body):
    header = "\n".join([
        "---",
        "id: AN10.60_att",
        "title_pali: Girimānandasuttavaṇṇanā",
        "title_en: Commentary on Girimānandasutta",
        "type: atthakatha",
        "pitaka: sutta",
        "nikaya: anguttara",
        "sutta: an10.60",
        "layer: atthakatha",
        "mula_file: [[an10_60]]",
        "tika_file: \"(No Ṭīkā available)\"",
        "source_pali: https://tipitaka.org/romn/cscd/ (CSCD)",
        "source_notes: https://suttacentral.net",
        "---",
        "",
        "# Commentary on Aṅguttara Nikāya 10.60: Girimānandasutta",
        "",
        "**Navigation**: [[INDEX|Pali Canon Vault]] / [[atthakatha/Atthakatha-Index|Atthakathā]] / [[atthakatha/sutta/Atthakatha-Sutta-Index|Sutta]] / [[atthakatha/sutta/anguttara_nikaya/Atthakatha-Anguttara-Index|Aṅguttara Nikāya]]",
        "**Mūla**: [[an10_60|Girimānandasutta — With Girimānanda]]",
        "**Tīkā**: (No Ṭīkā available)",
        "",
        "*Manorathapūraṇī (Aṅguttara Nikāya Atthakathā)*",
        ""
    ])
    
    body_lines = [
        "## Girimānandasuttavaṇṇanā",
        "",
        "*Pali text — CSCD (Chattha Sangayana Tipitaka). Use Simsapa DPD for word lookups (double-click any Pali word).*",
        ""
    ]
    
    for rend, pnum, text in paras:
        if pnum:
            body_lines.append(f"\n### §{pnum}\n")
            
        if rend == "subhead":
            body_lines.append(f"### {text}\n")
        elif rend == "centre":
            body_lines.append(f"\n{text}\n")
        elif rend in ('gatha', 'gathalast', 'indent'):
            body_lines.append(f"  {text}  ")
        else:
            prefix = f"({pnum}) " if pnum else ""
            body_lines.append(f"{prefix}{text}\n")
            
    parts = [header]
    if notes_body:
        parts.append(notes_body)
        parts.append("\n---\n")
    parts.append("\n".join(body_lines))
    return "\n".join(parts)

# ── Rebuilding indexes ────────────────────────────────────────────────────────
def clean_and_rebuild_indexes():
    # 1. Majjhima Mūla INDEX
    mn_mula_idx = os.path.join(VAULT, "mula/sutta/majjhima_nikaya/Mula-Majjhima-Index.md")
    if os.path.exists(mn_mula_idx):
        with open(mn_mula_idx, "r", encoding="utf-8") as f:
            lines = f.readlines()
        # Find all rows in markdown tables
        # Format: | [[mn10|MN 10]] | Satipaṭṭhānasutta | Mindfulness Meditation | 5,721 |
        rows = {}
        for l in lines:
            m = re.search(r'\|\s*\[\[(mn\d+)\|([^\]]+)\]\]\s*\|\s*([^|]+?)\s*\|\s*(?:([^|]+?)\s*\|)?\s*([\d,]+)\s*\|', l)
            if m:
                slug = m.group(1)
                code = m.group(2)
                pali = m.group(3).strip()
                en = m.group(4).strip() if m.group(4) else ""
                wc = m.group(5).strip()
                rows[slug] = (code, pali, en, wc)
        
        # Add MN 19
        mn19_path = os.path.join(VAULT, "mula/sutta/majjhima_nikaya/mn19.md")
        if os.path.exists(mn19_path):
            with open(mn19_path, "r", encoding="utf-8") as f:
                wc = len(f.read().split())
            rows["mn19"] = ("MN 19", "Dvedhāvitakkasutta", "Two Kinds of Thought", f"{wc:,}")
            
        # Re-fetch word counts for others if files exist
        for slug in list(rows.keys()):
            path = os.path.join(VAULT, "mula/sutta/majjhima_nikaya", f"{slug}.md")
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    wc = len(f.read().split())
                code, pali, en, _ = rows[slug]
                rows[slug] = (code, pali, en, f"{wc:,}")

        # Let's fix missing translations for Phase 2 suttas in our database:
        meta_translations = {
            "mn36": "With Saccaka (the Longer)",
            "mn43": "The Longer Analysis",
            "mn44": "The Shorter Analysis",
            "mn52": "At Aṭṭhakanāgara",
            "mn111": "One by One"
        }
        for slug, en_val in meta_translations.items():
            if slug in rows:
                code, pali, _, wc = rows[slug]
                rows[slug] = (code, pali, en_val, wc)

        # Write clean sorted table
        sorted_slugs = sorted(rows.keys(), key=lambda x: int(re.search(r'\d+', x).group()))
        table_lines = [
            "| Sutta | Pali Title | English | Words |",
            "|---|---|---|---|"
        ]
        for s in sorted_slugs:
            code, pali, en, wc = rows[s]
            table_lines.append(f"| [[{s}\|{code}]] | {pali} | {en} | {wc} |")
            
        content = "\n".join([
            "# Majjhima Nikāya Index",
            "",
            "**Navigation**: [[INDEX|Pali Canon Vault]] / [[mula/Mula-Index|Mūla]] / [[mula/sutta/Mula-Sutta-Index|Sutta]] / [[mula/sutta/majjhima_nikaya/Mula-Majjhima-Index|Majjhima Nikāya]]",
            "",
            "This directory contains the Middle Length Discourses (Majjhima Nikāya) from the Sutta Piṭaka.",
            "",
            "## Migrated Suttas",
            "",
            "\n".join(table_lines),
            "",
            "---",
            "*Back to [[mula/sutta/Mula-Sutta-Index|Sutta Index]]*",
            ""
        ])
        with open(mn_mula_idx, "w", encoding="utf-8") as f:
            f.write(content)
        print("Rebuilt Majjhima Mūla index.")

    # 2. Majjhima Atthakathā INDEX
    mn_att_idx = os.path.join(VAULT, "atthakatha/sutta/majjhima_nikaya/Atthakatha-Majjhima-Index.md")
    if os.path.exists(mn_att_idx):
        with open(mn_att_idx, "r", encoding="utf-8") as f:
            lines = f.readlines()
        rows = {}
        for l in lines:
            m = re.search(r'\|\s*\[\[(mn\d+)\|([^\]]+)\]\]\s*\|\s*\[\[(mn\d+_att)\|([^\]]+)\]\]\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([\d,]+)\s*\|', l)
            if m:
                slug = m.group(1)
                code = m.group(2)
                att_slug = m.group(3)
                pali = m.group(4)
                src = m.group(5).strip()
                notes = m.group(6).strip()
                wc = m.group(7)
                rows[slug] = (code, att_slug, pali, src, notes, wc)
                
        # Add MN 19
        mn19_att_path = os.path.join(VAULT, "atthakatha/sutta/majjhima_nikaya/mn19_att.md")
        if os.path.exists(mn19_att_path):
            with open(mn19_att_path, "r", encoding="utf-8") as f:
                wc = len(f.read().split())
            # Find annotations count
            notes_count = len(fetch_sujato_notes("mn19"))
            notes_str = f"{notes_count} Sujato notes" if notes_count > 0 else "—"
            rows["mn19"] = ("MN 19", "mn19_att", "Dvedhāvitakkasuttavaṇṇanā", "Papañcasūdanī (CSCD)", notes_str, f"{wc:,}")
            
        for slug in list(rows.keys()):
            path = os.path.join(VAULT, "atthakatha/sutta/majjhima_nikaya", f"{slug}_att.md")
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    wc = len(f.read().split())
                code, att_slug, pali, src, notes, _ = rows[slug]
                rows[slug] = (code, att_slug, pali, src, notes, f"{wc:,}")

        sorted_slugs = sorted(rows.keys(), key=lambda x: int(re.search(r'\d+', x).group()))
        table_lines = [
            "| Sutta | Commentary | Pali Source | Notes | Words |",
            "|---|---|---|---|---|"
        ]
        for s in sorted_slugs:
            code, att_slug, pali, src, notes, wc = rows[s]
            table_lines.append(f"| [[{s}\|{code}]] | [[{att_slug}\|{pali}]] | {src} | {notes} | {wc} |")
            
        content = "\n".join([
            "# Majjhima Nikāya Commentary (Papañcasūdanī) Index",
            "",
            "**Navigation**: [[INDEX|Pali Canon Vault]] / [[atthakatha/Atthakatha-Index|Atthakathā]] / [[atthakatha/sutta/Atthakatha-Sutta-Index|Sutta]] / [[atthakatha/sutta/majjhima_nikaya/Atthakatha-Majjhima-Index|Majjhima Nikāya]]",
            "",
            "This directory contains commentaries on the Middle Length Discourses (Majjhima Nikāya), representing sections of the Papañcasūdanī.",
            "",
            "## Migrated Commentary Notes",
            "",
            "\n".join(table_lines),
            "",
            "---",
            "*Back to [[atthakatha/sutta/Atthakatha-Sutta-Index|Sutta Commentaries Index]]*",
            ""
        ])
        with open(mn_att_idx, "w", encoding="utf-8") as f:
            f.write(content)
        print("Rebuilt Majjhima Atthakathā index.")

    # 3. Majjhima Ṭīkā INDEX
    mn_tik_idx = os.path.join(VAULT, "tika/sutta/majjhima_nikaya/Tika-Majjhima-Index.md")
    if os.path.exists(mn_tik_idx):
        with open(mn_tik_idx, "r", encoding="utf-8") as f:
            lines = f.readlines()
        rows = {}
        for l in lines:
            m = re.search(r'\|\s*\[\[(mn\d+)\|([^\]]+)\]\]\s*\|\s*\[\[(mn\d+_tik)\|([^\]]+)\]\]\s*\|\s*([^|]+?)\s*\|\s*([\d,]+)\s*\|', l)
            if m:
                slug = m.group(1)
                code = m.group(2)
                tik_slug = m.group(3)
                pali = m.group(4)
                src = m.group(5).strip()
                wc = m.group(6)
                rows[slug] = (code, tik_slug, pali, src, wc)
                
        mn19_tik_path = os.path.join(VAULT, "tika/sutta/majjhima_nikaya/mn19_tik.md")
        if os.path.exists(mn19_tik_path):
            with open(mn19_tik_path, "r", encoding="utf-8") as f:
                wc = len(f.read().split())
            rows["mn19"] = ("MN 19", "mn19_tik", "Dvedhāvitakkasuttavaṇṇanātīkā", "tipitaka.org CSCD", f"{wc:,}")
            
        for slug in list(rows.keys()):
            path = os.path.join(VAULT, "tika/sutta/majjhima_nikaya", f"{slug}_tik.md")
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    wc = len(f.read().split())
                code, tik_slug, pali, src, _ = rows[slug]
                rows[slug] = (code, tik_slug, pali, src, f"{wc:,}")

        sorted_slugs = sorted(rows.keys(), key=lambda x: int(re.search(r'\d+', x).group()))
        table_lines = [
            "| Sutta | Sub-commentary | Pali Source | Words |",
            "|---|---|---|---|"
        ]
        for s in sorted_slugs:
            code, tik_slug, pali, src, wc = rows[s]
            table_lines.append(f"| [[{s}\|{code}]] | [[{tik_slug}\|{pali}]] | {src} | {wc} |")
            
        content = "\n".join([
            "---",
            "type: index",
            "pitaka: sutta",
            "nikaya: majjhima",
            "layer: tika",
            "---",
            "",
            "# Majjhima Nikāya — Ṭīkā",
            "",
            "**Navigation**: [[INDEX|Pali Canon Vault]] / [[tika/Tika-Index|Ṭīkā]] / [[tika/sutta/Tika-Sutta-Index|Sutta]] / [[tika/sutta/majjhima_nikaya/Tika-Majjhima-Index|Majjhima Nikāya]]",
            "",
            "This directory contains sub-commentaries (Papañcasūdanī-ṭīkā) on the Middle Length Discourses.",
            "",
            "## Migrated Texts",
            "",
            "\n".join(table_lines),
            "",
            "---",
            "*Back to [[tika/sutta/Tika-Sutta-Index|Sutta Sub-commentaries Index]]*",
            ""
        ])
        with open(mn_tik_idx, "w", encoding="utf-8") as f:
            f.write(content)
        print("Rebuilt Majjhima Ṭīkā index.")

    # 4. Aṅguttara Mūla INDEX
    an_mula_idx = os.path.join(VAULT, "mula/sutta/anguttara_nikaya/Mula-Anguttara-Index.md")
    if os.path.exists(an_mula_idx):
        with open(an_mula_idx, "r", encoding="utf-8") as f:
            lines = f.readlines()
        rows = {}
        for l in lines:
            m = re.search(r'\|\s*\[\[(an\d+(?:_\d+)+)\|([^\]]+)\]\]\s*\|\s*([^|]+?)\s*\|\s*(?:([^|]+?)\s*\|)?\s*([\d,]+)\s*\|', l)
            if m:
                slug = m.group(1)
                code = m.group(2)
                pali = m.group(3).strip()
                en = m.group(4).strip() if m.group(4) else ""
                wc = m.group(5).strip()
                rows[slug] = (code, pali, en, wc)
                
        an10_60_path = os.path.join(VAULT, "mula/sutta/anguttara_nikaya/an10_60.md")
        if os.path.exists(an10_60_path):
            with open(an10_60_path, "r", encoding="utf-8") as f:
                wc = len(f.read().split())
            rows["an10_60"] = ("AN 10.60", "Girimānandasutta", "With Girimānanda", f"{wc:,}")
            
        for slug in list(rows.keys()):
            path = os.path.join(VAULT, "mula/sutta/anguttara_nikaya", f"{slug}.md")
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    wc = len(f.read().split())
                code, pali, en, _ = rows[slug]
                rows[slug] = (code, pali, en, f"{wc:,}")

        # Set missing translations for other AN suttas
        meta_translations = {
            "an3_100": "A Lump of Salt",
            "an4_123_126": "Differences",
            "an5_28": "With Five Factors",
            "an9_36": "Depending on Absorption",
            "an10_2_6": "Benefits"
        }
        for slug, en_val in meta_translations.items():
            if slug in rows:
                code, pali, _, wc = rows[slug]
                rows[slug] = (code, pali, en_val, wc)

        def sort_key_an(slug):
            # Parse numbers out of "an3_100", "an10_60", "an4_123_126"
            parts = [int(x) for x in re.findall(r'\d+', slug)]
            return parts
            
        sorted_slugs = sorted(rows.keys(), key=sort_key_an)
        table_lines = [
            "| Sutta | Pali Title | English | Words |",
            "|---|---|---|---|"
        ]
        for s in sorted_slugs:
            code, pali, en, wc = rows[s]
            table_lines.append(f"| [[{s}\|{code}]] | {pali} | {en} | {wc} |")
            
        content = "\n".join([
            "---",
            "type: index",
            "pitaka: sutta",
            "nikaya: anguttara",
            "---",
            "",
            "# Aṅguttara Nikāya — Mūla",
            "",
            "**Navigation**: [[INDEX|Pali Canon Vault]] / [[mula/Mula-Index|Mūla]] / [[mula/sutta/Mula-Sutta-Index|Sutta]]",
            "",
            "The Aṅguttara Nikāya (\"Numbered Discourses\") organizes teachings by numerical lists, from ones to elevens.",
            "",
            "## Migrated Suttas",
            "",
            "\n".join(table_lines),
            "",
            "---",
            "*Back to [[mula/sutta/Mula-Sutta-Index|Sutta Index]]*",
            ""
        ])
        with open(an_mula_idx, "w", encoding="utf-8") as f:
            f.write(content)
        print("Rebuilt Aṅguttara Mūla index.")

    # 5. Aṅguttara Atthakathā INDEX
    an_att_idx = os.path.join(VAULT, "atthakatha/sutta/anguttara_nikaya/Atthakatha-Anguttara-Index.md")
    if os.path.exists(an_att_idx):
        with open(an_att_idx, "r", encoding="utf-8") as f:
            lines = f.readlines()
        rows = {}
        for l in lines:
            m = re.search(r'\|\s*\[\[(an\d+(?:_\d+)+)\|([^\]]+)\]\]\s*\|\s*\[\[(an\d+(?:_\d+)+_att)\|([^\]]+)\]\]\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([\d,]+)\s*\|', l)
            if m:
                slug = m.group(1)
                code = m.group(2)
                att_slug = m.group(3)
                pali = m.group(4)
                src = m.group(5).strip()
                notes = m.group(6).strip()
                wc = m.group(7)
                rows[slug] = (code, att_slug, pali, src, notes, wc)
                
        an10_60_att_path = os.path.join(VAULT, "atthakatha/sutta/anguttara_nikaya/an10_60_att.md")
        if os.path.exists(an10_60_att_path):
            with open(an10_60_att_path, "r", encoding="utf-8") as f:
                wc = len(f.read().split())
            notes_count = len(fetch_sujato_notes("an10.60"))
            notes_str = f"{notes_count} Sujato notes" if notes_count > 0 else "—"
            rows["an10_60"] = ("AN 10.60", "an10_60_att", "Girimānandasuttavaṇṇanā", "Manorathapūraṇī (CSCD)", notes_str, f"{wc:,}")
            
        for slug in list(rows.keys()):
            path = os.path.join(VAULT, "atthakatha/sutta/anguttara_nikaya", f"{slug}_att.md")
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    wc = len(f.read().split())
                code, att_slug, pali, src, notes, _ = rows[slug]
                rows[slug] = (code, att_slug, pali, src, notes, f"{wc:,}")

        def sort_key_an(slug):
            parts = [int(x) for x in re.findall(r'\d+', slug)]
            return parts
            
        sorted_slugs = sorted(rows.keys(), key=sort_key_an)
        table_lines = [
            "| Sutta | Commentary | Pali Source | Notes | Words |",
            "|---|---|---|---|---|"
        ]
        for s in sorted_slugs:
            code, att_slug, pali, src, notes, wc = rows[s]
            table_lines.append(f"| [[{s}\|{code}]] | [[{att_slug}\|{pali}]] | {src} | {notes} | {wc} |")
            
        content = "\n".join([
            "---",
            "type: index",
            "pitaka: sutta",
            "nikaya: anguttara",
            "layer: atthakatha",
            "---",
            "",
            "# Aṅguttara Nikāya — Atthakathā",
            "",
            "**Navigation**: [[INDEX|Pali Canon Vault]] / [[atthakatha/Atthakatha-Index|Atthakathā]] / [[atthakatha/sutta/Atthakatha-Sutta-Index|Sutta]] / [[atthakatha/sutta/anguttara_nikaya/Atthakatha-Anguttara-Index|Aṅguttara Nikāya]]",
            "",
            "## Migrated Texts",
            "",
            "\n".join(table_lines),
            "",
            "---",
            "*Back to [[atthakatha/sutta/Atthakatha-Sutta-Index|Sutta Commentaries Index]]*",
            ""
        ])
        with open(an_att_idx, "w", encoding="utf-8") as f:
            f.write(content)
        print("Rebuilt Aṅguttara Atthakathā index.")

def main():
    print("=== Phase 4 Migration Script ===")
    
    # ── 1. Fetch Sutta Mūla Data ──
    print("\nFetching MN 19 from SuttaCentral...")
    mn19_data = fetch_json(SC_API.format("mn19"))
    print("Fetching AN 10.60 from SuttaCentral...")
    an10_60_data = fetch_json(SC_API.format("an10.60"))
    
    # ── 2. Fetch Sujato's annotations ──
    print("\nFetching Sujato notes for MN 19...")
    mn19_notes = fetch_sujato_notes("mn19")
    mn19_notes_md = notes_to_markdown(mn19_notes, "mn19")
    
    print("Fetching Sujato notes for AN 10.60...")
    an10_60_notes = fetch_sujato_notes("an10.60")
    an10_60_notes_md = notes_to_markdown(an10_60_notes, "an10_60")

    # ── 3. Fetch CSCD Commentaries ──
    print("\nFetching MN 19 Atthakatha (s0201a.att2.xml)...")
    mn19_att_all = load_cscd_paras("s0201a.att2.xml")
    
    # Find start and end indices of section 9. Dvedhāvitakkasuttavaṇṇanā
    mn19_att_start = None
    mn19_att_end = None
    for i, (rend, pnum, text) in enumerate(mn19_att_all):
        if "9. Dvedhāvitakkasuttavaṇṇanā" in text:
            mn19_att_start = i
        if "Dvedhāvitakkasuttavaṇṇanā niṭṭhitā" in text:
            mn19_att_end = i
            break
    mn19_att_paras = mn19_att_all[mn19_att_start:mn19_att_end + 1]
    print(f"MN 19 Att extracted: {len(mn19_att_paras)} paragraphs")
    
    print("\nFetching MN 19 Tika (s0201t.tik2.xml)...")
    mn19_tik_all = load_cscd_paras("s0201t.tik2.xml")
    mn19_tik_start = None
    mn19_tik_end = None
    for i, (rend, pnum, text) in enumerate(mn19_tik_all):
        if "9. Dvedhāvitakkasuttavaṇṇanā" in text:
            mn19_tik_start = i
        if mn19_tik_start is not None and i > mn19_tik_start:
            if "Vitakkasaṇṭhāna" in text or "10." in text:
                mn19_tik_end = i - 1
                break
    if mn19_tik_end is None:
        mn19_tik_end = len(mn19_tik_all) - 1
    mn19_tik_paras = mn19_tik_all[mn19_tik_start:mn19_tik_end + 1]
    print(f"MN 19 Tik extracted: {len(mn19_tik_paras)} paragraphs")

    print("\nFetching AN 10.60 Atthakatha (s0404a.att20.xml)...")
    an10_60_att_all = load_cscd_paras("s0404a.att20.xml")
    an10_60_att_paras = []
    # Extract Girimānandasuttavaṇṇanā (heading at 7, body at 8)
    for i, (rend, pnum, text) in enumerate(an10_60_att_all):
        if "10. Girimānandasuttavaṇṇanā" in text or pnum == "60":
            an10_60_att_paras.append((rend, pnum, text))
    print(f"AN 10.60 Att extracted: {len(an10_60_att_paras)} paragraphs")

    # ── 4. Generate & Save Files ──
    print("\nGenerating & Saving MN 19 files...")
    mn19_mula_md = make_mn19_mula(mn19_data)
    with open(os.path.join(VAULT, "mula/sutta/majjhima_nikaya/mn19.md"), "w", encoding="utf-8") as f:
        f.write(mn19_mula_md + "\n")
        
    mn19_att_md = make_mn19_att(mn19_att_paras, mn19_notes_md)
    with open(os.path.join(VAULT, "atthakatha/sutta/majjhima_nikaya/mn19_att.md"), "w", encoding="utf-8") as f:
        f.write(mn19_att_md + "\n")
        
    mn19_tik_md = make_mn19_tik(mn19_tik_paras)
    with open(os.path.join(VAULT, "tika/sutta/majjhima_nikaya/mn19_tik.md"), "w", encoding="utf-8") as f:
        f.write(mn19_tik_md + "\n")

    print("\nGenerating & Saving AN 10.60 files...")
    an10_60_mula_md = make_an10_60_mula(an10_60_data)
    with open(os.path.join(VAULT, "mula/sutta/anguttara_nikaya/an10_60.md"), "w", encoding="utf-8") as f:
        f.write(an10_60_mula_md + "\n")
        
    an10_60_att_md = make_an10_60_att(an10_60_att_paras, an10_60_notes_md)
    with open(os.path.join(VAULT, "atthakatha/sutta/anguttara_nikaya/an10_60_att.md"), "w", encoding="utf-8") as f:
        f.write(an10_60_att_md + "\n")

    # ── 5. Rebuild Indexes ──
    print("\nRebuilding index files...")
    clean_and_rebuild_indexes()
    
    print("\nMigration Completed successfully!")

if __name__ == "__main__":
    main()
