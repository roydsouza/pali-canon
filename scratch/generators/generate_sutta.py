#!/usr/bin/env python3
import os
import sys
import re
import json
import argparse
import time
import urllib.request

# Configure sys.path so we can import from scratch/lib
SCRATCH_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SCRATCH_DIR)

from lib.pali_utils import get_vault_path, load_cscd_paras, clean_xml

API_BASE = "https://suttacentral.net/api/bilarasuttas/{}/sujato"

NIKAYA_MAPS = {
    "dn": ("digha_nikaya", "Dīgha Nikāya", "digha"),
    "mn": ("majjhima_nikaya", "Majjhima Nikāya", "majjhima"),
    "sn": ("samyutta_nikaya", "Saṃyutta Nikāya", "samyutta"),
    "an": ("anguttara_nikaya", "Aṅguttara Nikāya", "anguttara"),
    "snp": ("khuddaka_nikaya/sutta_nipata", "Khuddaka Nikāya", "khuddaka"),
    "dhp": ("khuddaka_nikaya/dhammapada", "Khuddaka Nikāya", "khuddaka"),
    "iti": ("khuddaka_nikaya/itivuttaka", "Khuddaka Nikāya", "khuddaka"),
    "ud": ("khuddaka_nikaya/udana", "Khuddaka Nikāya", "khuddaka")
}

def get_nikaya_details(sutta_id):
    for prefix, details in NIKAYA_MAPS.items():
        if sutta_id.startswith(prefix):
            return details
    return ("sutta_generic", "Sutta Piṭaka", "sutta")

def fetch_suttacentral(sutta_id):
    url = API_BASE.format(sutta_id)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode('utf-8'))

def is_meta(key):
    return bool(re.search(r':0\.\d+$', key))

def heading_level(key):
    if re.search(r':\d+\.0$', key):
        return 1
    m = re.search(r':\d+\.0\.(\d+)$', key)
    if m:
        return int(m.group(1))
    return None

def filter_cscd_paras(paras, pattern_str):
    if not pattern_str:
        return paras
    pat = re.compile(pattern_str, re.IGNORECASE)
    results = []
    started = False
    for rend, paranum, text in paras:
        if not started:
            if pat.search(text):
                started = True
                results.append((rend, paranum, text))
        else:
            # Stop if we hit the next section
            if re.match(r'^\d+\.\s+\w+(?:vaṇṇanā|ṭīkā|suttavaṇṇanā)', text, re.IGNORECASE):
                break
            results.append((rend, paranum, text))
    return results if results else paras

def generate_mula(vault, sutta_id, data):
    sutta_id_sc = sutta_id.replace("_", ".")
    sutta_id_vault = sutta_id.replace(".", "_")
    
    root = data.get("root_text", {})
    tr = data.get("translation_text", {})
    keys = data.get("keys_order", [])
    
    nikaya_dir, nikaya_label, nav_abbr = get_nikaya_details(sutta_id_vault)
    
    # Try to extract titles
    title_pali = root.get(f"{sutta_id_sc}:0.2", root.get(f"{sutta_id_sc}:0.3", "Untitled")).strip()
    title_en = tr.get(f"{sutta_id_sc}:0.2", tr.get(f"{sutta_id_sc}:0.3", "Untitled")).strip()
    
    out_dir = os.path.join(vault, "mula/sutta", nikaya_dir)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{sutta_id_vault}.md")
    
    lines = [
        "---",
        f"id: {sutta_id_vault.upper()}",
        f"title_pali: {title_pali}",
        f"title_en: {title_en}",
        "type: mula",
        "pitaka: sutta",
        f"nikaya: {nav_abbr}",
        f"sutta_number: {sutta_id_sc}",
        "translator: Bhikkhu Sujato",
        "source: https://suttacentral.net",
        "---",
        "",
        f"# {nikaya_label}: {title_pali}",
        "",
        f"**Navigation**: [[INDEX|Pali Canon Vault]] / [[mula/Mula-Index|Mūla]] / [[mula/sutta/Mula-Sutta-Index|Sutta]] / [[mula/sutta/{nikaya_dir}/Mula-{{'digha_nikaya': 'Digha', 'majjhima_nikaya': 'Majjhima', 'samyutta_nikaya': 'Samyutta', 'anguttara_nikaya': 'Anguttara'}.get(nikaya_dir, 'Khuddaka')}}-Index|{nikaya_label}]]",
        f"**Related Texts**: [[{sutta_id_vault}_att|Commentary (Atthakathā)]] | [[{sutta_id_vault}_tik|Sub-commentary (Tīkā)]]",
        "",
        f"## {title_pali} ({title_en})",
        "",
    ]
    
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
            lines.append(f"{marker} {e or p}\n" + (f"*{p}*\n" if p and e else ""))
        else:
            if p:
                lines.append(f"**{p}**  ")
            if e:
                lines.append(f"*{e}*")
            lines.append("")
            
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
        
    print(f"Generated Mūla: {out_path} ({len(lines)} lines)")

def generate_layer(vault, sutta_id, layer_name, mapping_info, has_tika=False):
    if not mapping_info:
        return
        
    sutta_id_sc = sutta_id.replace("_", ".")
    sutta_id_vault = sutta_id.replace(".", "_")
    
    nikaya_dir, nikaya_label, nav_abbr = get_nikaya_details(sutta_id_vault)
    
    filename = mapping_info.get("file")
    pattern = mapping_info.get("pattern")
    heading = mapping_info.get("heading", f"{sutta_id_vault.upper()} {layer_name.capitalize()}")
    
    print(f"Loading {layer_name.upper()} from {filename}...")
    try:
        paras = load_cscd_paras(filename)
    except Exception as e:
        print(f"Failed to load CSCD file {filename}: {e}")
        return
        
    filtered = filter_cscd_paras(paras, pattern)
    
    suffix = "att" if layer_name == "att" else "tik"
    out_folder = "atthakatha" if layer_name == "att" else "tika"
    out_dir = os.path.join(vault, out_folder, "sutta", nikaya_dir)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{sutta_id_vault}_{suffix}.md")
    
    mula_ref = f"{sutta_id_vault}"
    other_ref = f"{sutta_id_vault}_tik" if suffix == "att" else f"{sutta_id_vault}_att"
    other_label = "Tīkā" if suffix == "att" else "Atthakathā"
    
    lines = [
        "---",
        f"id: {sutta_id_vault.upper()}_{suffix}",
        f"title_pali: {heading}",
        f"type: {out_folder}",
        "pitaka: sutta",
        f"nikaya: {nav_abbr}",
        f"sutta_number: {sutta_id_sc}",
        f"mula_file: [[{mula_ref}]]",
    ]
    if suffix == "att":
        lines.append(f"tika_file: [[{other_ref}]]")
    else:
        lines.append(f"commentary_file: [[{other_ref}]]")
        
    lines.extend([
        "---",
        "",
        f"# {heading}",
        "",
        f"**Navigation**: [[INDEX|Pali Canon Vault]] / [[{out_folder}/{'Atthakatha' if suffix == 'att' else 'Tika'}-Index|{'Atthakathā' if suffix == 'att' else 'Tīkā'}]] / [[{out_folder}/sutta/{'Atthakatha' if suffix == 'att' else 'Tika'}-Sutta-Index|Sutta]] / [[{out_folder}/sutta/{nikaya_dir}/{'Atthakatha' if suffix == 'att' else 'Tika'}-{{'digha_nikaya': 'Digha', 'majjhima_nikaya': 'Majjhima', 'samyutta_nikaya': 'Samyutta', 'anguttara_nikaya': 'Anguttara'}.get(nikaya_dir, 'Khuddaka')}}-Index|{nikaya_label}]]",
        f"**Mūla**: [[{mula_ref}]]",
        f"**{other_label}**: [[{other_ref}]]",
        "",
        f"*Pali text CSCD ({filename}).*",
        "",
    ])
    
    for rend, paranum, text in filtered:
        if paranum:
            lines.append(f"\n### §{paranum}\n")
            
        prefix = f"({paranum}) " if paranum else ""
        if rend in ('gatha', 'gathalast', 'indent'):
            lines.append(f"  {text}  ")
        else:
            lines.append(f"{prefix}{text}\n")
            
        if paranum and suffix == "att" and has_tika:
            tika_link = (
                f"\n> [!abstract]- Tīkā §{paranum}\n"
                f"> [[{other_ref}#§{paranum}|Sub-commentary §{paranum}]]\n"
            )
            lines.append(tika_link)
            
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
        
    print(f"Generated {layer_name.upper()}: {out_path} ({len(lines)} lines)")

def normalize_pali(text):
    if not text:
        return ""
    text = text.replace('*', ' ')
    text = re.sub(r'[\[\]#|—\-–]', ' ', text)
    text = text.lower()
    replacements = {
        'ā': 'a', 'ī': 'i', 'ū': 'u',
        'ṅ': 'n', 'ñ': 'n', 'ṇ': 'n',
        'ṭ': 't', 'ḍ': 'd', 'ḷ': 'l', 
        'ṁ': 'm', 'ṃ': 'm'
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    text = re.sub(r'[^a-z\s]', '', text)
    return ' '.join(text.split())

def extract_anchors_from_att(att_content):
    pattern = re.compile(r'\((\d+)\)\s+(.*?)(?:nti|ti)\b', re.DOTALL)
    anchors = {}
    ordinals = {
        'pathame', 'dutiye', 'tatiye', 'catutthe', 'pancame', 'chatthe',
        'sattame', 'atthame', 'navame', 'dasame', 'ekadasame', 'dvadasame',
        'telasame', 'catuddasame', 'pannarasame', 'solasame', 'sattarasame',
        'attharasame', 'ekunavisitime', 'visitime'
    }
    for m in pattern.finditer(att_content):
        para_num = int(m.group(1))
        anchor_text = m.group(2).strip()
        anchor_cleaned = re.sub(r'<[^>]+>', '', anchor_text)
        words = anchor_cleaned.split()
        if words:
            first_word_norm = normalize_pali(words[0])
            if first_word_norm in ordinals:
                words = words[1:]
        if len(words) > 10:
            anchor_cleaned = " ".join(words[:6])
        else:
            anchor_cleaned = " ".join(words)
        anchors[para_num] = anchor_cleaned
    return anchors


def crosslink_mula(mula_path, att_anchors, att_base, tik_base):
    with open(mula_path, "r", encoding="utf-8") as f:
        mula_content = f.read()
    mula_lines = mula_content.splitlines(keepends=True)
    mula_modified = False
    
    for para_num, anchor_text in sorted(att_anchors.items()):
        if f"[[{att_base}#§{para_num}" in mula_content:
            continue
        norm_anchor = normalize_pali(anchor_text)
        if not norm_anchor:
            continue
        matched_idx = -1
        for idx, line in enumerate(mula_lines):
            if line.startswith("#") or line.startswith("---") or line.startswith(">"):
                continue
            norm_line = normalize_pali(line)
            if norm_anchor in norm_line:
                matched_idx = idx
                break
        if matched_idx != -1:
            callout = (
                f"\n> [!info]- Commentary §{para_num}\n"
                f"> **Atthakathā**: [[{att_base}#§{para_num}|Commentary §{para_num}]]"
            )
            if tik_base:
                callout += f"  ·  **Tīkā**: [[{tik_base}#§{para_num}|Sub-commentary §{para_num}]]"
            callout += "\n\n"
            mula_lines.insert(matched_idx, callout)
            mula_modified = True
            mula_content = "".join(mula_lines)
            mula_lines = mula_content.splitlines(keepends=True)
        else:
            print(f"  Warning: could not resolve Mūla anchor '{anchor_text}' for §{para_num}")
            
    if mula_modified:
        with open(mula_path, "w", encoding="utf-8") as f:
            f.write(mula_content)
        print(f"Updated Mūla file {os.path.basename(mula_path)} with paragraph callouts.")

def main():
    parser = argparse.ArgumentParser(description="Unified Sutta generator engine.")
    parser.add_argument("--sutta", required=True, help="Sutta ID to generate (e.g. mn22, sn12.1)")
    args = parser.parse_args()
    
    sutta_id = args.sutta.lower().strip()
    sutta_id_sc = sutta_id.replace("_", ".")
    sutta_id_vault = sutta_id.replace(".", "_")
    
    vault = get_vault_path()
    
    print(f"Unified Generator starting for Sutta ID: {sutta_id_sc} (Vault ID: {sutta_id_vault})")
    
    # 1. Generate Mūla
    try:
        print("Fetching SuttaCentral segments...")
        sc_data = fetch_suttacentral(sutta_id_sc)
        generate_mula(vault, sutta_id_vault, sc_data)
    except Exception as e:
        print(f"Failed to generate Mūla layer from SuttaCentral: {e}")
        
    # 2. Check mappings for Att & Tika
    mapping_path = os.path.join(vault, "scratch", "cscd_mappings_all.json")
    if os.path.exists(mapping_path):
        with open(mapping_path, "r", encoding="utf-8") as f:
            mappings = json.load(f)
            
        sutta_map = mappings.get(sutta_id_sc)
        if sutta_map:
            att_maps = sutta_map.get("att", [])
            tika_maps = sutta_map.get("tika", [])
            has_tika = bool(tika_maps)
            
            if att_maps:
                generate_layer(vault, sutta_id_vault, "att", att_maps[0], has_tika=has_tika)
            if tika_maps:
                generate_layer(vault, sutta_id_vault, "tika", tika_maps[0])
        else:
            print(f"No CSCD mappings found for {sutta_id_sc} in cscd_mappings_all.json. Skipping commentary layers.")
    else:
        print("Mappings file cscd_mappings_all.json not found. Skipping commentary layers.")
        
    # 3. Post-generation: Auto-crosslink Mūla and Aṭṭhakathā/Ṭīkā
    nikaya_dir, _, _ = get_nikaya_details(sutta_id_vault)
    mula_file_path = os.path.join(vault, "mula/sutta", nikaya_dir, f"{sutta_id_vault}.md")
    att_file_path = os.path.join(vault, "atthakatha/sutta", nikaya_dir, f"{sutta_id_vault}_att.md")
    tika_file_path = os.path.join(vault, "tika/sutta", nikaya_dir, f"{sutta_id_vault}_tik.md")
    
    if os.path.exists(mula_file_path) and os.path.exists(att_file_path):
        print(f"Post-processing cross-links for {sutta_id_vault}...")
        with open(att_file_path, "r", encoding="utf-8") as f:
            att_content = f.read()
        att_anchors = extract_anchors_from_att(att_content)
        if att_anchors:
            print(f"Found {len(att_anchors)} paragraph anchors for cross-linking.")
            att_base = f"{sutta_id_vault}_att"
            tik_base = f"{sutta_id_vault}_tik" if os.path.exists(tika_file_path) else ""
            crosslink_mula(mula_file_path, att_anchors, att_base, tik_base)
        else:
            print("No paragraph anchors found in Atthakathā for auto-linking.")
            
    print("Generation complete.")

if __name__ == "__main__":
    main()
