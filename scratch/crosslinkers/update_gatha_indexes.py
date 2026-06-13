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

def update_collection_index(subcoll, title_pali, title_en, nipata_names):
    mula_dir = os.path.join(VAULT, f"mula/sutta/khuddaka_nikaya/{subcoll}")
    
    mula_files = [f for f in os.listdir(mula_dir) if f.startswith("th") and f.endswith(".md")]
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
        sc_prefix = "thag" if subcoll == "theragatha" else "thig"
        m = re.match(rf"^{sc_prefix}(\d+)\.(\d+)$", s["sc_id"])
        if m:
            return (int(m.group(1)), int(m.group(2)))
        return (999, 999)
        
    suttas.sort(key=sort_key)
    
    # Group by nipata
    nipatas = {}
    for s in suttas:
        key = sort_key(s)
        nip = key[0]
        nipatas.setdefault(nip, []).append(s)
        
    mula_lines = [
        "---",
        "type: index",
        "pitaka: sutta",
        "nikaya: khuddaka",
        f"subcollection: {subcoll}",
        "---",
        "",
        f"# {title_pali} — Mūla",
        "",
        "**Navigation**: [[INDEX|Pali Canon Vault]] / [[mula/Mula-Index|Mūla]] / [[mula/sutta/Mula-Sutta-Index|Sutta]] / [[mula/sutta/khuddaka_nikaya/Mula-Khuddaka-Index|Khuddaka Nikāya]]",
        "",
        f"The {title_pali} (\"{title_en}\") is a collection of verses attributed to the senior {('monks' if subcoll == 'theragatha' else 'nuns')} of the early Buddhist Sangha, recording their struggles, realizations, and attainment of liberation.",
        ""
    ]
    
    for nip in sorted(nipatas.keys()):
        mula_lines.append(f"## {nipata_names.get(nip, f'Nipāta {nip}')}\n")
        mula_lines.append("| Verse | Monk/Nun | English |") if subcoll == "theragatha" else mula_lines.append("| Verse | Nun | English |")
        mula_lines.append("|---|---|---|")
        for s in nipatas[nip]:
            sc_upper = s["sc_id"].upper()
            mula_lines.append(f"| [[{s['sc_id']}|{sc_upper}]] | {s['title_pali']} | *{s['title_en']}* |")
        mula_lines.append("")
        
    mula_dest = os.path.join(mula_dir, ("Mula-Theragatha-Index.md" if subcoll == "theragatha" else "Mula-Therigatha-Index.md"))
    with open(mula_dest, "w", encoding="utf-8") as f:
        f.write("\n".join(mula_lines) + "\n")
    print(f"Saved {title_pali} index to {mula_dest}")

def main():
    thag_nipata_names = {
        1: "Ekakanipāta (Book of the Ones)",
        2: "Dukanipāta (Book of the Twos)",
        3: "Tikanipāta (Book of the Threes)",
        4: "Catukkanipāta (Book of the Fours)",
        5: "Pañcakanipāta (Book of the Fives)",
        6: "Chakkanipāta (Book of the Sixes)",
        7: "Sattakanipāta (Book of the Sevens)",
        8: "Aṭṭhakanipāta (Book of the Eights)",
        9: "Navakanipāta (Book of the Nines)",
        10: "Dasakanipāta (Book of the Tens)",
        11: "Ekādasanipāta (Book of the Elevens)",
        12: "Dvādasanipāta (Book of the Twelves)",
        13: "Terasanipāta (Book of the Thirteens)",
        14: "Cuddasanipāta (Book of the Fourteens)",
        15: "Soḷasanipāta (Book of the Sixteens — thag15)", # CSCD calls it 15th
        16: "Vīsatinipāta (Book of the Twenties)",
        17: "Tiṁsanipāta (Book of the Thirties)",
        18: "Cattālīsanipāta (Book of the Forties)",
        19: "Paññāsanipāta (Book of the Fifties)",
        20: "Saṭṭhinipāta (Book of the Sixties)",
        21: "Mahānipāta (Great Book)"
    }
    
    thig_nipata_names = {
        1: "Ekakanipāta (Book of the Ones)",
        2: "Dukanipāta (Book of the Twos)",
        3: "Tikanipāta (Book of the Threes)",
        4: "Catukkanipāta (Book of the Fours)",
        5: "Pañcakanipāta (Book of the Fives)",
        6: "Chakkanipāta (Book of the Sixes)",
        7: "Sattakanipāta (Book of the Sevens)",
        8: "Aṭṭhakanipāta (Book of the Eights)",
        9: "Navakanipāta (Book of the Nines)",
        10: "Dasakanipāta (Book of the Tens)",
        11: "Ekādasanipāta (Book of the Elevens)",
        12: "Dvādasanipāta (Book of the Twelves)",
        13: "Vīsatinipāta (Book of the Twenties — thig13)",
        14: "Tiṁsanipāta (Book of the Thirties)",
        15: "Cattālīsanipāta (Book of the Forties)",
        16: "Mahānipāta (Great Book)"
    }
    
    update_collection_index("theragatha", "Theragāthā", "Verses of the Senior Monks", thag_nipata_names)
    update_collection_index("therigatha", "Therīgāthā", "Verses of the Senior Nuns", thig_nipata_names)

if __name__ == "__main__":
    main()
