#!/usr/bin/env python3
import os
import re
import sys

# Configure sys.path so we can import from scratch/lib
SCRATCH_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SCRATCH_DIR)

from lib.pali_utils import get_vault_path, parse_frontmatter

# Exclude directories
EXCLUDE_DIRS = {".git", ".obsidian", "scratch", "templates", "archive"}

def parse_yaml_raw(content):
    """Custom YAML block parser that handles lists and standard key-values."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not match:
        return None
    
    yaml_text = match.group(1)
    yaml_dict = {}
    current_key = None
    for line in yaml_text.split('\n'):
        if not line.strip() or line.strip().startswith('#'):
            continue
        if line.strip().startswith('- '):
            val = line.strip()[2:].strip()
            if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
            if current_key and isinstance(yaml_dict.get(current_key), list):
                yaml_dict[current_key].append(val)
            continue
            
        if ':' in line:
            key, val = line.split(':', 1)
            key = key.strip()
            val = val.strip()
            if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
            if val == "":
                yaml_dict[key] = []
                current_key = key
            else:
                # Check if it looks like a list in brackets/quotes, excluding wikilinks
                if val.startswith('[') and val.endswith(']') and not val.startswith('[['):
                    # simple list parse
                    inner = val[1:-1].strip()
                    if inner:
                        yaml_dict[key] = [x.strip().strip('"').strip("'") for x in inner.split(',')]
                    else:
                        yaml_dict[key] = []
                else:
                    yaml_dict[key] = val
                current_key = key
    return yaml_dict

def extract_wikilinks(text):
    """Extracts target names from Obsidian wikilinks: [[target|display]] -> ['target']"""
    if not text:
        return []
    targets = []
    # Match [[target]] or [[target|display]]
    for m in re.finditer(r'\[\[([^\]|#]+)(#[^\]|]*)?(\|[^\]]*)?\]\]', text):
        targets.append(m.group(1).strip())
    return targets

def parse_link_value(val):
    """Parses a frontmatter reference field value which could be a path or wikilink(s)."""
    if not val:
        return []
    if isinstance(val, list):
        res = []
        for x in val:
            res.extend(parse_link_value(x))
        return res
    
    # If it contains wikilink syntax
    if '[[' in val:
        return extract_wikilinks(val)
    
    # If it's a placeholder like "(No Ṭīkā available)", ignore it
    val_clean = val.strip()
    if val_clean.startswith('(') and val_clean.endswith(')'):
        return []
    if 'none' in val_clean.lower() or 'no ' in val_clean.lower() or 'not available' in val_clean.lower():
        return []
    
    # Otherwise treat as path/string
    return [val_clean]

def paths_match(ref, target_filepath, vault_dir):
    """Checks if a reference string (wikilink name or path) matches target_filepath."""
    ref_clean = ref.replace('\\', '').lstrip('/').strip()
    target_rel = os.path.relpath(target_filepath, vault_dir).replace('\\', '/').lstrip('/')
    target_filename = os.path.basename(target_filepath)
    target_base = os.path.splitext(target_filename)[0]
    
    # 1. Exact relative path match (with or without .md extension)
    if ref_clean == target_rel or ref_clean + ".md" == target_rel:
        return True
        
    # 2. Base name match (Obsidian short link)
    if ref_clean == target_base:
        return True
        
    # 3. Path suffix match
    if target_rel.endswith(ref_clean) or target_rel.endswith(ref_clean + ".md"):
        return True
        
    return False

def validate_frontmatter_file(filepath, content, rel_src, vault_dir):
    errors = []
    filename = os.path.basename(filepath)
    if filename == "INDEX.md" or filename.endswith("Index.md"):
        return errors
        
    parts = rel_src.split(os.sep)
    if not parts or len(parts) < 2:
        return errors
        
    type_dir = parts[0]
    if type_dir not in {"mula", "atthakatha", "tika", "matika", "practice", "paths"}:
        return errors
        
    yaml_dict = parse_yaml_raw(content)
    if yaml_dict is None:
        errors.append({
            "file": rel_src,
            "error": "Missing or invalid YAML frontmatter block at start of file"
        })
        return errors
        
    expected_types = {
        "mula": "mula",
        "atthakatha": "atthakatha",
        "tika": "tika",
        "matika": "matika",
        "practice": "practice",
        "paths": "path"
    }
    
    if "id" not in yaml_dict or not yaml_dict["id"]:
        errors.append({
            "file": rel_src,
            "error": "Missing 'id' in frontmatter"
        })
        
    if "type" not in yaml_dict:
        errors.append({
            "file": rel_src,
            "error": "Missing 'type' in frontmatter"
        })
    elif yaml_dict["type"] != expected_types[type_dir]:
        errors.append({
            "file": rel_src,
            "error": f"Invalid type '{yaml_dict['type']}' for folder '{type_dir}/'. Expected '{expected_types[type_dir]}'."
        })
        
    if type_dir in {"mula", "atthakatha", "tika"}:
        required = ["title_pali", "pitaka", "nikaya", "sutta_number"]
        for field in required:
            if field == "sutta_number" and ("sutta" in yaml_dict and yaml_dict["sutta"]):
                continue
            if field not in yaml_dict or not yaml_dict[field]:
                errors.append({
                    "file": rel_src,
                    "error": f"Missing required field '{field}' in canonical text frontmatter"
                })
        
        if "pitaka" in yaml_dict and yaml_dict["pitaka"] not in {"sutta", "vinaya", "abhidhamma"}:
            errors.append({
                "file": rel_src,
                "error": f"Invalid pitaka value '{yaml_dict['pitaka']}'"
            })
        if "nikaya" in yaml_dict and yaml_dict["nikaya"] not in {"majjhima", "digha", "samyutta", "anguttara", "khuddaka", "None", "an", "sn", "mn", "dn", "kn"}:
            errors.append({
                "file": rel_src,
                "error": f"Invalid nikaya value '{yaml_dict['nikaya']}'"
            })
            
        for link_field in ["commentary_file", "sub_commentary_file", "mula_file", "tika_file", "att_file"]:
            if link_field in yaml_dict and yaml_dict[link_field]:
                refs = parse_link_value(yaml_dict[link_field])
                for ref in refs:
                    # Resolve to path
                    ref_path = ref.lstrip("/")
                    # If it's a short name, search for it
                    found = False
                    if os.path.exists(os.path.join(vault_dir, ref_path)):
                        found = True
                    elif os.path.exists(os.path.join(vault_dir, ref_path + ".md")):
                        found = True
                    else:
                        # short name check
                        target_filename = os.path.basename(ref_path)
                        if not target_filename.endswith(".md"):
                            target_filename += ".md"
                        # Scan vault for this filename
                        for root, dirs, files in os.walk(vault_dir):
                            if any(d in root.split(os.sep) for d in EXCLUDE_DIRS):
                                continue
                            if target_filename in files:
                                found = True
                                break
                    if not found:
                        errors.append({
                            "file": rel_src,
                            "error": f"Referenced {link_field} '{ref}' does not exist on disk."
                        })
                        
    elif type_dir == "matika":
        if "title_pali" not in yaml_dict or not yaml_dict["title_pali"]:
            errors.append({
                "file": rel_src,
                "error": "Missing 'title_pali' in matika frontmatter"
            })
        if "category" not in yaml_dict or yaml_dict["category"] not in {"list_note", "factor_note"}:
            errors.append({
                "file": rel_src,
                "error": f"Invalid category '{yaml_dict.get('category')}' in matika"
            })
            
    elif type_dir in {"practice", "paths"}:
        if "title" not in yaml_dict or not yaml_dict["title"]:
            errors.append({
                "file": rel_src,
                "error": f"Missing 'title' in {type_dir} frontmatter"
            })
            
    return errors

def validate_reciprocal_covers(vault_dir):
    errors = []
    # Walk all files to parse their frontmatter and cache them
    all_frontmatters = {}
    file_paths = {}
    
    for root, dirs, files in os.walk(vault_dir):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for file in files:
            if file.endswith(".md") and not file.startswith("FROM-CLAUDE") and file != "INDEX.md" and not file.endswith("Index.md"):
                path = os.path.join(root, file)
                rel_src = os.path.relpath(path, vault_dir)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                    yaml_dict = parse_yaml_raw(content)
                    if yaml_dict:
                        all_frontmatters[rel_src] = yaml_dict
                        # Map base name and relative path
                        file_paths[rel_src] = path
                        file_paths[os.path.splitext(file)[0]] = path
                except Exception as e:
                    print(f"Error parsing {rel_src}: {e}")

    # Now validate covers
    for rel_src, yaml_dict in all_frontmatters.items():
        if "covers" in yaml_dict and yaml_dict["covers"]:
            covers = yaml_dict["covers"]
            if isinstance(covers, str):
                covers = [covers]
                
            for target in covers:
                # Find target file
                target_path = None
                target_clean = target.lstrip("/").replace('\\', '')
                if target_clean in file_paths:
                    target_path = file_paths[target_clean]
                elif target_clean + ".md" in file_paths:
                    target_path = file_paths[target_clean + ".md"]
                else:
                    # check basename
                    base = os.path.splitext(os.path.basename(target_clean))[0]
                    if base in file_paths:
                        target_path = file_paths[base]
                        
                if not target_path:
                    errors.append({
                        "file": rel_src,
                        "error": f"covers field target '{target}' does not exist on disk."
                    })
                    continue
                    
                # Parse target frontmatter
                target_rel = os.path.relpath(target_path, vault_dir)
                target_fm = all_frontmatters.get(target_rel)
                if not target_fm:
                    errors.append({
                        "file": rel_src,
                        "error": f"Covered target file '{target}' has no valid frontmatter."
                    })
                    continue
                    
                # Check reciprocal link
                # C points to M. C = rel_src (atthakatha or tika), M = target_rel (mula or atthakatha)
                c_type = yaml_dict.get("type")
                m_type = target_fm.get("type")
                c_path_abs = file_paths[rel_src]
                
                reciprocal_found = False
                
                # Check all possible link fields in target
                link_fields = ["commentary_file", "sub_commentary_file", "mula_file", "tika_file", "att_file"]
                for field in link_fields:
                    if field in target_fm and target_fm[field]:
                        refs = parse_link_value(target_fm[field])
                        for ref in refs:
                            if paths_match(ref, c_path_abs, vault_dir):
                                reciprocal_found = True
                                break
                    if reciprocal_found:
                        break
                        
                if not reciprocal_found:
                    errors.append({
                        "file": rel_src,
                        "error": f"Reciprocal link validation failed: target '{target}' does not link back to '{rel_src}'"
                    })
                    
    return errors

def lint_all(vault_dir):
    errors = []
    
    # 1. Validate individual file frontmatter schemas
    for root, dirs, files in os.walk(vault_dir):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for file in files:
            if file.endswith(".md") and not file.startswith("FROM-CLAUDE"):
                filepath = os.path.join(root, file)
                rel_src = os.path.relpath(filepath, vault_dir)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                file_errors = validate_frontmatter_file(filepath, content, rel_src, vault_dir)
                errors.extend(file_errors)
                
    # 2. Validate reciprocal covers
    covers_errors = validate_reciprocal_covers(vault_dir)
    errors.extend(covers_errors)
    
    return errors

if __name__ == "__main__":
    vault_dir = get_vault_path()
    print(f"Linting frontmatter schemas in: {vault_dir}")
    errors = lint_all(vault_dir)
    
    if errors:
        print(f"\nFound {len(errors)} frontmatter linter errors:")
        for err in errors:
            print(f"  [{err['file']}] {err['error']}")
        sys.exit(1)
    else:
        print("\nAll frontmatter schemas and reciprocal links are valid!")
        sys.exit(0)
