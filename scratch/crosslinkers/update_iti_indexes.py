import os
import re

VAULT = os.environ.get("PALI_VAULT", "/Users/rds/pali_canon")

def parse_frontmatter(filepath):
    meta = {}
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if m:
        for line in m.group(1).split("\n"):
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta

def main():
    mula_dir = os.path.join(VAULT, "mula/sutta/khuddaka_nikaya/itivuttaka")
    att_dir = os.path.join(VAULT, "atthakatha/sutta/khuddaka_nikaya/itivuttaka")
    
    mula_files = [f for f in os.listdir(mula_dir) if f.startswith("iti") and f.endswith(".md")]
    suttas = []
    for f in mula_files:
        path = os.path.join(mula_dir, f)
        meta = parse_frontmatter(path)
        sc_id = meta.get("sutta_number", f[:-3])
        suttas.append({
            "sc_id": sc_id,
            "title_pali": meta.get("title_pali", "Unknown"),
            "title_en": meta.get("title_en", "Unknown"),
            "file": f
        })
        
    def sort_key(s):
        m = re.match(r"^iti(\d+)$", s["sc_id"])
        if m:
            return int(m.group(1))
        return 999
        
    suttas.sort(key=sort_key)
    
    # Group by nipata
    nipatas = {}
    for s in suttas:
        sc_num = sort_key(s)
        if sc_num <= 27:
            nip = 1
        elif sc_num <= 49:
            nip = 2
        elif sc_num <= 99:
            nip = 3
        else:
            nip = 4
        nipatas.setdefault(nip, []).append(s)
        
    nipata_names = {
        1: "Ekakanipāta (Ones — suttas 1 to 27)",
        2: "Dukanipāta (Twos — suttas 28 to 49)",
        3: "Tikanipāta (Threes — suttas 50 to 99)",
        4: "Catukkanipāta (Fours — suttas 100 to 112)"
    }
    
    # 1. Update Mula INDEX.md
    mula_lines = [
        "---",
        "type: index",
        "pitaka: sutta",
        "nikaya: khuddaka",
        "subcollection: itivuttaka",
        "---",
        "",
        "# Itivuttaka — Mūla",
        "",
        "**Navigation**: [[INDEX|Pali Canon Vault]] / [[mula/Mula-Index|Mūla]] / [[mula/sutta/Mula-Sutta-Index|Sutta]] / [[mula/sutta/khuddaka_nikaya/Mula-Khuddaka-Index|Khuddaka Nikāya]]",
        "",
        "The Itivuttaka (\"As It Was Said\") is a collection of 112 short discourses, organized by numerical group. Each sutta features a prose discourse followed by a summarizing verse.",
        ""
    ]
    
    for nip in sorted(nipatas.keys()):
        mula_lines.append(f"## {nipata_names.get(nip, f'Nipāta {nip}')}\n")
        mula_lines.append("| Sutta | Title | English |")
        mula_lines.append("|---|---|---|")
        for s in nipatas[nip]:
            sc_upper = s["sc_id"].upper()
            mula_lines.append(f"| [[{s['sc_id']}|{sc_upper}]] | {s['title_pali']} | *{s['title_en']}* |")
        mula_lines.append("")
        
    mula_dest = os.path.join(mula_dir, "Mula-Itivuttaka-Index.md")
    with open(mula_dest, "w", encoding="utf-8") as f:
        f.write("\n".join(mula_lines) + "\n")
    print(f"Saved Mūla index to {mula_dest}")
    
    # 2. Update Atthakatha INDEX.md
    att_lines = [
        "---",
        "type: index",
        "pitaka: sutta",
        "nikaya: khuddaka",
        "subcollection: itivuttaka",
        "layer: atthakatha",
        "---",
        "",
        "# Itivuttaka — Atthakathā",
        "",
        "**Navigation**: [[INDEX|Pali Canon Vault]] / [[atthakatha/Atthakatha-Index|Atthakathā]] / [[atthakatha/sutta/Atthakatha-Sutta-Index|Sutta]] / [[atthakatha/sutta/khuddaka_nikaya/Atthakatha-Khuddaka-Index|Khuddaka Nikāya]]",
        "",
        "## Commentaries (Paramatthadīpanī)",
        ""
    ]
    
    for nip in sorted(nipatas.keys()):
        att_lines.append(f"### {nipata_names.get(nip, f'Nipāta {nip}')}\n")
        att_lines.append("| Commentary | Mūla Sutta | Pali Source |")
        att_lines.append("|---|---|---|")
        for s in nipatas[nip]:
            sc_id = s["sc_id"]
            att_path = os.path.join(att_dir, f"{sc_id}_att.md")
            comm_title = s["title_pali"] + "vaṇṇanā"
            if os.path.exists(att_path):
                att_meta = parse_frontmatter(att_path)
                comm_title = att_meta.get("title_pali", comm_title)
            
            att_lines.append(f"| [[{sc_id}_att|{comm_title}]] | [[{sc_id}]] | CSCD |")
        att_lines.append("")
        
    att_dest = os.path.join(att_dir, "Mula-Itivuttaka-Index.md")
    with open(att_dest, "w", encoding="utf-8") as f:
        f.write("\n".join(att_lines) + "\n")
    print(f"Saved Atthakathā index to {att_dest}")

if __name__ == "__main__":
    main()
