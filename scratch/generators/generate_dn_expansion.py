#!/usr/bin/env python3
import os
import json
import re
import time
import html as hmod
import urllib.request

VAULT    = os.environ.get("PALI_VAULT", "/Users/rds/pali_canon")
API_BASE = "https://suttacentral.net/api/bilarasuttas/{}/sujato"
GITHUB   = "https://raw.githubusercontent.com/siongui/tipitaka-romn/master/cscd/{}"
TIPITAKA = "https://tipitaka.org/romn/cscd/{}"

SUTTAS = [
    {
        "sc_id": "dn1",
        "slug": "dn1",
        "sutta_code": "DN1",
        "pali_title": "Brahmajālasutta",
        "en_title": "The Prime Net",
        "num": 1,
        "cscd_att": "s0101a.att1.xml",
        "cscd_tik": "s0101t.tik1.xml",
        "commentary_name": "Sumaṅgalavilāsinī (Dīgha Nikāya Atthakathā)",
        "sub_commentary_name": "Sumaṅgalavilāsinī-ṭīkā (Dīgha Nikāya Sub-commentary)",
        "anchors": {
            1: "**Evaṁ me sutaṁ—**",
            2: "**Atha kho bhagavā ambalaṭṭhikāyaṁ",
            3: "**Atha kho sambahulānaṁ bhikkhūnaṁ",
            4: "**Atha kho bhagavā tesaṁ bhikkhūnaṁ",
            148: "**Evaṁ vutte, āyasmā ānando bhagavantaṁ",
            149: "**Attamanā te bhikkhū",
        },
        "labels": {
            1: "Opening — Evaṁ me sutaṁ",
            2: "Wanderers Suppiya and Brahmadatta",
            3: "The monks' conversation in the pavilion",
            4: "The Buddha addresses the monks",
            148: "Ānanda asks for the name of the discourse",
            149: "Conclusion of the Brahmajālasutta",
        }
    },
    {
        "sc_id": "dn16",
        "slug": "dn16",
        "sutta_code": "DN16",
        "pali_title": "Mahāparinibbānasutta",
        "en_title": "The Great Discourse on the Buddha’s Extinction",
        "num": 16,
        "cscd_att": "s0102a.att2.xml",
        "cscd_tik": "s0102t.tik2.xml",
        "commentary_name": "Sumaṅgalavilāsinī (Dīgha Nikāya Atthakathā)",
        "sub_commentary_name": "Sumaṅgalavilāsinī-ṭīkā (Dīgha Nikāya Sub-commentary)",
        "anchors": {
            131: "**Evaṁ me sutaṁ—**",
            134: "**Tena kho pana samayena āyasmā ānando bhagavato piṭṭhito ṭhito hoti bhagavantaṁ bījayamāno",
            136: "**Atha kho bhagavā acirapakkante",
            237: "**Evaṁ vutte, doṇo brāhmaṇo",
            238: "**“Evaṁ, bho”ti kho doṇo brāhmaṇo tesaṁ saṅghānaṁ",
            240: "**Evametaṁ bhūtapubbanti.",
        },
        "labels": {
            131: "Opening — Gijjhakūṭa",
            134: "Ānanda fanning the Buddha",
            136: "Buddha assembles the monks after Vassakāra departs",
            237: "Dona the Brahmin resolves the relic dispute",
            238: "Dona distributes the relics",
            240: "Conclusion of the Mahāparinibbānasutta",
        }
    },
    {
        "sc_id": "dn21",
        "slug": "dn21",
        "sutta_code": "DN21",
        "pali_title": "Sakkapañhasutta",
        "en_title": "Sakka’s Questions",
        "num": 21,
        "cscd_att": "s0102a.att7.xml",
        "cscd_tik": "s0102t.tik7.xml",
        "commentary_name": "Sumaṅgalavilāsinī (Dīgha Nikāya Atthakathā)",
        "sub_commentary_name": "Sumaṅgalavilāsinī-ṭīkā (Dīgha Nikāya Sub-commentary)",
        "anchors": {
            344: "**Evaṁ me sutaṁ—**",
            345: "**Atha kho sakko devānamindo pañcasikhaṁ",
            346: "**Tena kho pana samayena vediyako pabbato atiriva obhāsajāto",
            347: "**“durupasaṅkamā kho, tāta pañcasikha",
            368: "**“Bhūtapubbaṁ, bhante, devāsurasaṅgāmo",
            371: "**Atha kho sakko devānamindo pāṇinā pathaviṁ parāmasitvā",
        },
        "labels": {
            344: "Opening — Indasālaguhā",
            345: "Sakka summons Pañcasikha",
            346: "The cave glows with divine light",
            347: "Difficult to approach the Buddha",
            368: "Sakka recalls the war with the Asuras",
            371: "Sakka's joy and conclusion of the discourse",
        }
    }
]

# Fetch functions
def fetch_mula_data(sc_id):
    url = API_BASE.format(sc_id)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def fetch_cscd_bytes(filename):
    url = GITHUB.format(filename)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            return r.read()
    except Exception as e:
        print(f"    GitHub failed for {filename} ({e}), trying tipitaka.org...")
        url = TIPITAKA.format(filename)
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=45) as r:
            return r.read()

# CSCD XML cleaner
def clean_xml(text):
    text = re.sub(r'<hi rend="bold">(.*?)</hi>', r'**\1**', text, flags=re.DOTALL)
    text = re.sub(r'<pb[^/]*/>', '', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = hmod.unescape(text)
    return re.sub(r'\s+', ' ', text).strip()

def load_cscd_paras(filename):
    raw = fetch_cscd_bytes(filename)
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

# Bilara Mula renderer
def is_meta(key):
    return bool(re.search(r':0\.\d+$', key))

def heading_level(key):
    if re.search(r':\d+\.0$', key):
        return 1
    m = re.search(r':\d+\.0\.(\d+)$', key)
    if m:
        return int(m.group(1))
    return None

def render_heading(level, pali, en):
    marker = "##" if level == 1 else "###"
    if en and pali:
        return f"{marker} {en}\n*{pali}*\n"
    return f"{marker} {en or pali}\n"

def generate_mula(s, data):
    root = data["root_text"]
    tr   = data["translation_text"]
    keys = data["keys_order"]
    
    slug = s["slug"]
    sutta_code = s["sutta_code"]
    pali_title = s["pali_title"]
    en_title = s["en_title"]
    num = s["num"]
    
    nav_link = "[[mula/sutta/digha_nikaya/Mula-Digha-Index|Dīgha Nikāya]]"
    att_slug = f"{slug}_att"
    tik_slug = f"{slug}_tik"
    
    lines = [
        "---",
        f"id: {sutta_code}",
        f"title_pali: {pali_title}",
        f"title_en: {en_title}",
        "type: mula",
        "pitaka: sutta",
        "nikaya: digha",
        f"sutta_number: {s['sc_id']}",
        "translator: Bhikkhu Sujato",
        "source: https://suttacentral.net",
        "tags:",
        "  - meditation",
        "---",
        "",
        f"# Dīgha Nikāya {num}: {pali_title}",
        "",
        "**Navigation**: [[INDEX|Pali Canon Vault]] / [[mula/Mula-Index|Mūla]] / "
        f"[[mula/sutta/Mula-Sutta-Index|Sutta]] / {nav_link}",
        f"**Related Texts**: [[{att_slug}|Commentary (Atthakathā)]] | "
        f"[[{tik_slug}|Sub-commentary (Tīkā)]]",
        "",
        f"## {pali_title}",
        f"*{en_title}*",
        "",
    ]
    
    for key in keys:
        if is_meta(key):
            continue
        p = root.get(key, "").strip()
        e = tr.get(key,   "").strip()
        if not p and not e:
            continue
        level = heading_level(key)
        if level is not None:
            lines.append(render_heading(level, p, e))
        else:
            if p and e:
                lines.append(f"**{p}**  ")
                lines.append(f"*{e}*")
            elif p:
                lines.append(f"*{p}*")
            else:
                lines.append(f"*{e}*")
            lines.append("")
            
    return "\n".join(lines)

def build_att_file(s, pali_body):
    sc_id = s["sc_id"]
    slug = s["slug"]
    sutta_code = s["sutta_code"]
    pali_title = s["pali_title"]
    en_title = s["en_title"]
    commentary_name = s["commentary_name"]
    
    nav_link  = "[[atthakatha/sutta/digha_nikaya/Atthakatha-Digha-Index|Dīgha Nikāya]]"
    mula_link = f"[[{slug}|{pali_title} — {en_title}]]"
    tik_link  = f"[[{slug}_tik|{pali_title}vaṇṇanātīkā (sub-commentary)]]"
    
    header = "\n".join([
        "---",
        f"id: {sutta_code}_att",
        f"title_pali: {pali_title}vaṇṇanā",
        f"title_en: Commentary on {pali_title} ({en_title})",
        "type: atthakatha",
        "pitaka: sutta",
        "nikaya: digha",
        f"sutta: {sc_id}",
        "layer: atthakatha",
        f"mula_file: [[{slug}]]",
        f"att_file: [[{slug}_att]]",
        "source_pali: https://github.com/siongui/tipitaka-romn (CSCD)",
        "---",
        "",
        f"# Commentary on Dīgha Nikāya: {pali_title}",
        "",
        "**Navigation**: [[INDEX|Pali Canon Vault]] / [[atthakatha/Atthakatha-Index|Atthakathā]] / "
        f"[[atthakatha/sutta/Atthakatha-Sutta-Index|Sutta]] / {nav_link}",
        f"**Mūla**: {mula_link}",
        f"**Tīkā**: {tik_link}",
        "",
        f"*{commentary_name}*",
        "",
        f"## {pali_title}vaṇṇanā",
        "",
        "*Pali text — CSCD (Chattha Sangayana Tipitaka). "
        "Use Simsapa DPD for word lookups (double-click any Pali word).*",
        "",
    ])
    return header + "\n" + pali_body

def build_tik_file(s, pali_body):
    sc_id = s["sc_id"]
    slug = s["slug"]
    sutta_code = s["sutta_code"]
    pali_title = s["pali_title"]
    en_title = s["en_title"]
    sub_commentary_name = s["sub_commentary_name"]
    
    nav_link  = "[[tika/sutta/digha_nikaya/Tika-Digha-Index|Dīgha Nikāya]]"
    mula_link = f"[[{slug}|{pali_title} — {en_title}]]"
    att_link  = f"[[{slug}_att|{pali_title}vaṇṇanā (atthakathā)]]"
    
    header = "\n".join([
        "---",
        f"id: {sutta_code}_tik",
        f"title_pali: {pali_title}vaṇṇanātīkā",
        f"title_en: Sub-commentary on {pali_title} ({en_title})",
        "type: tika",
        "pitaka: sutta",
        "nikaya: digha",
        f"sutta: {sc_id}",
        "layer: tika",
        f"mula_file: [[{slug}]]",
        f"att_file: [[{slug}_att]]",
        "source_pali: https://tipitaka.org/romn/cscd/ (CSCD)",
        "---",
        "",
        f"# Sub-commentary on Dīgha Nikāya: {pali_title}",
        "",
        "**Navigation**: [[INDEX|Pali Canon Vault]] / [[tika/Tika-Index|Ṭīkā]] / "
        f"[[tika/sutta/Tika-Sutta-Index|Sutta]] / {nav_link}",
        f"**Mūla**: {mula_link}",
        f"**Atthakathā**: {att_link}",
        "",
        f"*{sub_commentary_name}*",
        "",
        f"## {pali_title}vaṇṇanātīkā",
        "",
        "*Pali text — CSCD (Chattha Sangayana Tipitaka). "
        "Use Simsapa DPD for word lookups (double-click any Pali word).*",
        "",
    ])
    return header + "\n" + pali_body

def update_index_file(layer, slug, sutta_code, pali_title, wc):
    idx_path = os.path.join(VAULT, layer, "sutta/digha_nikaya", {"mula": "Mula-Digha-Index.md", "atthakatha": "Atthakatha-Digha-Index.md", "tika": "Tika-Digha-Index.md"}[layer])
    with open(idx_path, encoding="utf-8") as f:
        content = f.read()
    if slug in content:
        return
    
    # We append a row to the table
    if "| Sutta |" not in content:
        # construct table structure if it's missing
        if layer == "mula":
            table = "\n\n| Sutta | Title | Words |\n|---|---|---|\n"
        elif layer == "atthakatha":
            table = "\n\n## Migrated Texts\n\n| Sutta | Commentary | Pali Source | Notes | Words |\n|---|---|---|---|---|\n"
        else:
            table = "\n\n## Migrated Texts\n\n| Sutta | Sub-commentary | Pali Source | Words |\n|---|---|---|---|\n"
        content = content.rstrip() + table
    
    if layer == "mula":
        row = f"| [[{slug}\\|{sutta_code}]] | {pali_title} | {wc:,} |\n"
    elif layer == "atthakatha":
        row = f"| [[{slug}\\|{sutta_code}]] | [[{slug}_att\\|{pali_title}vaṇṇanā]] | CSCD | 0 Sujato notes | {wc:,} |\n"
    else:
        row = f"| [[{slug}\\|{sutta_code}]] | [[{slug}_tik\\|{pali_title}vaṇṇanātīkā]] | tipitaka.org CSCD | {wc:,} |\n"
        
    with open(idx_path, "a", encoding="utf-8") as f:
        f.write(row)
    print(f"  Registered in {layer} INDEX")

def main():
    for s in SUTTAS:
        print(f"\n==================================================")
        print(f"MIGRATING {s['sutta_code']}: {s['pali_title']}")
        print(f"==================================================")
        
        # 1. Fetch and write Mula
        print("  Fetching Mula from SuttaCentral...")
        mula_data = fetch_mula_data(s["sc_id"])
        mula_text = generate_mula(s, mula_data)
        
        # 2. Fetch and parse Atthakatha
        print(f"  Fetching Atthakatha {s['cscd_att']}...")
        att_paras = load_cscd_paras(s["cscd_att"])
        print(f"    Loaded {len(att_paras)} paragraphs")
        
        # 3. Fetch and parse Tika
        print(f"  Fetching Tika {s['cscd_tik']}...")
        tik_paras = load_cscd_paras(s["cscd_tik"])
        print(f"    Loaded {len(tik_paras)} paragraphs")
        
        # Find all paragraph numbers present in each
        att_nums = {pnum for _, pnum, _ in att_paras if pnum}
        tik_nums = {pnum for _, pnum, _ in tik_paras if pnum}
        common_nums = sorted([int(n) for n in (att_nums & tik_nums)])
        print(f"    Found {len(common_nums)} common paragraph numbers")
        
        # We will insert ### §NNN in Atthakatha and Tika for ALL numbered paragraphs.
        # For Atthakatha
        att_lines = []
        for rend, paranum, text in att_paras:
            if not text:
                continue
            if paranum:
                p_num = int(paranum)
                att_lines.append(f"\n### §{p_num}\n")
                
                # Check if this paragraph is also a heading
                if re.match(r'^\d+\.\s+\S+vaggo', text, re.IGNORECASE) or \
                   re.match(r'^\d+\.\s+\S+vagga', text, re.IGNORECASE) or \
                   re.match(r'^\d+\.\s+\S+(?:vaṇṇanā|ṭīkā|sutta)', text):
                    att_lines.append(f"## {text}\n")
                elif rend in ('gatha', 'gathalast', 'indent'):
                    att_lines.append(f"  {text}  ")
                else:
                    att_lines.append(f"({paranum}) {text}\n")
                
                # Insert Tika callout link if it exists in Tika too
                if p_num in tik_nums:
                    t_link = (
                        f"\n> [!abstract]- Tīkā §{p_num}\n"
                        f"> [[{s['slug']}_tik#§{p_num}|{s['pali_title']}vaṇṇanātīkā §{p_num}]]\n"
                    )
                    att_lines.append(t_link)
            else:
                if re.match(r'^\d+\.\s+\S+vaggo', text, re.IGNORECASE) or \
                   re.match(r'^\d+\.\s+\S+vagga', text, re.IGNORECASE) or \
                   re.match(r'^\d+\.\s+\S+(?:vaṇṇanā|ṭīkā|sutta)', text):
                    att_lines.append(f"\n## {text}\n")
                elif rend in ('gatha', 'gathalast', 'indent'):
                    att_lines.append(f"  {text}  ")
                else:
                    prefix = f"({paranum}) " if paranum else ""
                    att_lines.append(f"{prefix}{text}\n")
        
        # For Tika
        tik_lines = []
        for rend, paranum, text in tik_paras:
            if not text:
                continue
            if paranum:
                p_num = int(paranum)
                tik_lines.append(f"\n### §{p_num}\n")
                if re.match(r'^\d+\.\s+\S+vaggo', text, re.IGNORECASE) or \
                   re.match(r'^\d+\.\s+\S+vagga', text, re.IGNORECASE) or \
                   re.match(r'^\d+\.\s+\S+(?:vaṇṇanā|ṭīkā|sutta)', text):
                    tik_lines.append(f"## {text}\n")
                elif rend in ('gatha', 'gathalast', 'indent'):
                    tik_lines.append(f"  {text}  ")
                else:
                    tik_lines.append(f"({paranum}) {text}\n")
            else:
                if re.match(r'^\d+\.\s+\S+vaggo', text, re.IGNORECASE) or \
                   re.match(r'^\d+\.\s+\S+vagga', text, re.IGNORECASE) or \
                   re.match(r'^\d+\.\s+\S+(?:vaṇṇanā|ṭīkā|sutta)', text):
                    tik_lines.append(f"\n## {text}\n")
                elif rend in ('gatha', 'gathalast', 'indent'):
                    tik_lines.append(f"  {text}  ")
                else:
                    prefix = f"({paranum}) " if paranum else ""
                    tik_lines.append(f"{prefix}{text}\n")
                    
        # 4. Insert Mula anchors
        mula_file_text = mula_text
        anchors_inserted = 0
        att_nums_ints = {int(x) for x in att_nums}
        tik_nums_ints = {int(x) for x in tik_nums}
        for pnum, anchor in s["anchors"].items():
            if anchor in mula_file_text:
                label = s["labels"][pnum]
                links = []
                if pnum in att_nums_ints:
                    links.append(f"**Atthakathā**: [[{s['slug']}_att#§{pnum}|{s['pali_title']}vaṇṇanā §{pnum}]]")
                if pnum in tik_nums_ints:
                    links.append(f"**Tīkā**: [[{s['slug']}_tik#§{pnum}|Ṭīkā §{pnum}]]")
                
                if links:
                    callout = f"\n> [!info]- Commentary — {label}\n> " + "  ·  ".join(links) + "\n\n"
                    mula_file_text = mula_file_text.replace(anchor, callout + anchor, 1)
                    anchors_inserted += 1
            else:
                # Try finding a fuzzy or case-insensitive match, or warning
                print(f"    WARNING: Anchor '{anchor}' for §{pnum} not found in Mula")
                
        print(f"    Inserted {anchors_inserted} commentary callouts in Mula")
        
        # 5. Write files
        mula_out = os.path.join(VAULT, "mula/sutta/digha_nikaya", f"{s['slug']}.md")
        att_out = os.path.join(VAULT, "atthakatha/sutta/digha_nikaya", f"{s['slug']}_att.md")
        tik_out = os.path.join(VAULT, "tika/sutta/digha_nikaya", f"{s['slug']}_tik.md")
        
        # Write Mula
        with open(mula_out, "w", encoding="utf-8") as f:
            f.write(mula_file_text + "\n")
        mula_wc = len(mula_file_text.split())
        print(f"    Wrote Mula: {mula_wc:,} words")
        update_index_file("mula", s["slug"], s["sutta_code"], s["pali_title"], mula_wc)
        
        # Write Atthakatha
        att_body = "\n".join(att_lines)
        att_content = build_att_file(s, att_body)
        with open(att_out, "w", encoding="utf-8") as f:
            f.write(att_content + "\n")
        att_wc = len(att_content.split())
        print(f"    Wrote Atthakatha: {att_wc:,} words")
        update_index_file("atthakatha", s["slug"], s["sutta_code"], s["pali_title"], att_wc)
        
        # Write Tika
        tik_body = "\n".join(tik_lines)
        tik_content = build_tik_file(s, tik_body)
        with open(tik_out, "w", encoding="utf-8") as f:
            f.write(tik_content + "\n")
        tik_wc = len(tik_content.split())
        print(f"    Wrote Tika: {tik_wc:,} words")
        update_index_file("tika", s["slug"], s["sutta_code"], s["pali_title"], tik_wc)
        
        time.sleep(0.5)

if __name__ == "__main__":
    main()
