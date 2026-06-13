#!/usr/bin/env python3
import os
import re
import json
import urllib.request
from concurrent.futures import ThreadPoolExecutor

VAULT_DIR = "/Users/rds/pali_canon"
MULA_DIR = os.path.join(VAULT_DIR, "mula/sutta")
CACHE_DIR = os.path.join(VAULT_DIR, "scratch/parallels_cache")
os.makedirs(CACHE_DIR, exist_ok=True)

LANG_MAP = {
    "pli": "Pali",
    "lzh": "Chinese",
    "skt": "Sanskrit",
    "tib": "Tibetan",
    "xct": "Khotanese",
    "pgd": "Gandhari"
}

def get_sutta_files():
    sutta_files = []
    for root, _, files in os.walk(MULA_DIR):
        for f in files:
            if f.endswith(".md") and f != "INDEX.md" and not f.endswith("Index.md"):
                sutta_files.append(os.path.join(root, f))
    return sutta_files

def fetch_parallels(sutta_id_sc):
    cache_path = os.path.join(CACHE_DIR, f"{sutta_id_sc}.json")
    if os.path.exists(cache_path) and os.path.getsize(cache_path) > 10:
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    url = f"https://suttacentral.net/api/parallels/{sutta_id_sc}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read().decode('utf-8'))
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(data, f)
            return data
    except Exception as e:
        print(f"Failed to fetch parallels for {sutta_id_sc}: {e}")
        return None

def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Parse frontmatter
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not m:
        return

    frontmatter_text = m.group(1)
    lines = frontmatter_text.split("\n")
    meta = {}
    for line in lines:
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"').strip("'")

    # Resolve Sutta ID directly from file basename to include correct prefix (e.g. an8.53)
    basename = os.path.basename(filepath)[:-3]
    sutta_id_sc = basename.replace("_", ".")

    # Skip if parallels already in frontmatter
    if "parallels:" in frontmatter_text:
        print(f"Skipping {os.path.basename(filepath)}: already has parallels.")
        return

    data = fetch_parallels(sutta_id_sc)
    if not data:
        return

    parallel_list = data.get(sutta_id_sc, [])
    if not parallel_list:
        # Sometimes keys differ
        for k in data.keys():
            parallel_list = data[k]
            break

    if not parallel_list:
        print(f"No parallels found for {sutta_id_sc}.")
        return

    formatted_parallels = []
    for p in parallel_list:
        to_data = p.get("to", {})
        uid = to_data.get("uid")
        acronym = to_data.get("acronym") or uid.upper()
        root_lang = to_data.get("root_lang") or "unknown"
        lang_name = LANG_MAP.get(root_lang, root_lang.upper())
        title = to_data.get("original_title") or to_data.get("translated_title") or "Untitled"
        
        # Clean title from XML tags if any
        title = re.sub(r'<[^>]+>', '', title).strip()
        formatted_parallels.append(f"{acronym} ({uid}) · {lang_name} · {title}")

    if not formatted_parallels:
        return

    # Construct new frontmatter
    # Insert parallels after the last key before ---
    new_lines = []
    for line in lines:
        if line.strip() and not line.startswith("parallels:"):
            new_lines.append(line)
            
    new_lines.append("parallels:")
    for p in formatted_parallels:
        # Escape single quotes in string
        p_escaped = p.replace("'", "''")
        new_lines.append(f"  - '{p_escaped}'")

    new_frontmatter = "---\n" + "\n".join(new_lines) + "\n---\n"
    new_content = new_frontmatter + content[m.end():]

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Updated parallels in {os.path.basename(filepath)} (found {len(formatted_parallels)}).")

def main():
    files = get_sutta_files()
    print(f"Found {len(files)} suttas to process.")
    
    # Process files in parallel to speed up API requests
    with ThreadPoolExecutor(max_workers=10) as executor:
        list(executor.map(process_file, files))

if __name__ == "__main__":
    main()
