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
    mula_dir = os.path.join(VAULT, "mula/sutta/khuddaka_nikaya/sutta_nipata")
    att_dir = os.path.join(VAULT, "atthakatha/sutta/khuddaka_nikaya/sutta_nipata")
    
    # Collect Mula suttas
    mula_files = [f for f in os.listdir(mula_dir) if f.startswith("snp") and f.endswith(".md")]
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
        
    # Sort suttas by chapter and sutta number
    # Key function: "snp2.1" -> (2, 1)
    def sort_key(s):
        m = re.match(r"^snp(\d+)\.(\d+)$", s["sc_id"])
        if m:
            return (int(m.group(1)), int(m.group(2)))
        return (99, 99)
        
    suttas.sort(key=sort_key)
    
    # Group by chapter
    chapters = {}
    for s in suttas:
        m = re.match(r"^snp(\d+)\.(\d+)$", s["sc_id"])
        if m:
            ch = int(m.group(1))
            chapters.setdefault(ch, []).append(s)
            
    chapter_names = {
        1: "Uragavagga (Chapter 1)",
        2: "Cūḷavagga (Chapter 2)",
        3: "Mahāvagga (Chapter 3)",
        4: "Aṭṭhakavagga (Chapter 4)",
        5: "Pārāyanavagga (Chapter 5)"
    }
    
    # 1. Update Mula INDEX.md
    mula_lines = [
        "---",
        "type: index",
        "pitaka: sutta",
        "nikaya: khuddaka",
        "subcollection: sutta_nipata",
        "---",
        "",
        "# Sutta Nipāta — Mūla",
        "",
        "**Navigation**: [[INDEX|Pali Canon Vault]] / [[mula/Mula-Index|Mūla]] / [[mula/sutta/Mula-Sutta-Index|Sutta]] / [[mula/sutta/khuddaka_nikaya/Mula-Khuddaka-Index|Khuddaka Nikāya]]",
        "",
        "The Sutta Nipāta (\"Anthology of Discourses\") is a collection of early, highly poetic Buddhist discourses.",
        ""
    ]
    
    for ch in sorted(chapters.keys()):
        mula_lines.append(f"## {chapter_names.get(ch, f'Chapter {ch}')}\n")
        mula_lines.append("| Sutta | Title | English |")
        mula_lines.append("|---|---|---|")
        for s in chapters[ch]:
            sc_upper = s["sc_id"].upper()
            mula_lines.append(f"| [[{s['sc_id']}|{sc_upper}]] | {s['title_pali']} | *{s['title_en']}* |")
        mula_lines.append("")
        
    mula_dest = os.path.join(mula_dir, "Mula-Sutta-Nipata-Index.md")
    with open(mula_dest, "w", encoding="utf-8") as f:
        f.write("\n".join(mula_lines) + "\n")
    print(f"Saved Mūla index to {mula_dest}")
    
    # 2. Update Atthakatha INDEX.md
    att_lines = [
        "---",
        "type: index",
        "pitaka: sutta",
        "nikaya: khuddaka",
        "subcollection: sutta_nipata",
        "layer: atthakatha",
        "---",
        "",
        "# Sutta Nipāta — Atthakathā",
        "",
        "**Navigation**: [[INDEX|Pali Canon Vault]] / [[atthakatha/Atthakatha-Index|Atthakathā]] / [[atthakatha/sutta/Atthakatha-Sutta-Index|Sutta]] / [[atthakatha/sutta/khuddaka_nikaya/Atthakatha-Khuddaka-Index|Khuddaka Nikāya]]",
        "",
        "## Commentaries (Paramatthajotikā II)",
        ""
    ]
    
    for ch in sorted(chapters.keys()):
        att_lines.append(f"### {chapter_names.get(ch, f'Chapter {ch}')}\n")
        att_lines.append("| Commentary | Mūla Sutta | Pali Source |")
        att_lines.append("|---|---|---|")
        for s in chapters[ch]:
            sc_id = s["sc_id"]
            # Look up commentary title from att file
            att_path = os.path.join(att_dir, f"{sc_id}_att.md")
            comm_title = s["title_pali"] + "vaṇṇanā"
            if os.path.exists(att_path):
                att_meta = parse_frontmatter(att_path)
                comm_title = att_meta.get("title_pali", comm_title)
            
            att_lines.append(f"| [[{sc_id}_att|{comm_title}]] | [[{sc_id}]] | CSCD |")
        att_lines.append("")
        
    att_dest = os.path.join(att_dir, "Mula-Sutta-Nipata-Index.md")
    with open(att_dest, "w", encoding="utf-8") as f:
        f.write("\n".join(att_lines) + "\n")
    print(f"Saved Atthakathā index to {att_dest}")

if __name__ == "__main__":
    main()
