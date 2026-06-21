#!/usr/bin/env python3
import os
import re
import sys

# The pali-canon vault root (nested inside the Megha Obsidian vault)
_DEFAULT_PALI_VAULT = os.path.join(
    os.path.expanduser("~"),
    "Library", "Mobile Documents", "iCloud~md~obsidian",
    "Documents", "Megha", "topics", "texts", "pali-canon",
)
VAULT_DIR = os.environ.get("PALI_VAULT", _DEFAULT_PALI_VAULT)

# Parent vault root (Megha) — used for cross-vault basename link resolution.
# Links like [[INDEX|Dashboard]] or [[nexus/mission/Mission|North Star]] point
# to files OUTSIDE pali-canon but inside the broader Obsidian vault.
_DEFAULT_PARENT_VAULT = os.path.join(
    os.path.expanduser("~"),
    "Library", "Mobile Documents", "iCloud~md~obsidian",
    "Documents", "Megha",
)
PARENT_VAULT_DIR = os.environ.get("PARENT_VAULT", _DEFAULT_PARENT_VAULT)

EXCLUDE_INDEX_DIRS = {".git", ".obsidian", "scratch", "templates", "archive"}
EXCLUDE_SCAN_DIRS = {".git", ".obsidian", "scratch", "templates", "archive"}

def get_markdown_files(vault_dir, exclude_dirs):
    md_files = []
    for root, dirs, files in os.walk(vault_dir):
        # Exclude specified directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if file.endswith(".md") and not file.startswith("FROM-CLAUDE"):
                md_files.append(os.path.join(root, file))
    return md_files

def parse_headers_and_anchors(filepath):
    """Returns a set of normalized headers/anchors from the markdown file."""
    headers = set()
    # Read file content
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Match ATX headings: e.g. "### §406" or "## The List" or "### 4.2. The Aggregates"
    heading_pattern = re.compile(r'^#+\s+(.+)$', re.MULTILINE)
    for match in heading_pattern.finditer(content):
        heading = match.group(1).strip()
        headers.add(heading)
        # Normalize for anchor comparisons (standard Obsidian replaces spaces with hyphens, etc.
        # but let's also keep exact match as it's common in this vault)
        normalized = re.sub(r'[^\w\s§\-.]', '', heading).strip()
        headers.add(normalized)
    
    # Check for custom HTML anchors if any (like <a name="anchor"></a> or similar)
    anchor_pattern = re.compile(r'<a\s+name="([^"]+)"')
    for match in anchor_pattern.finditer(content):
        headers.add(match.group(1).strip())
        
    return headers

def parse_yaml(content):
    match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
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
                yaml_dict[key] = val
                current_key = key
    return yaml_dict

# Configure sys.path so we can import from inspect/lint_frontmatter
SCRATCH_DIR = os.path.dirname(os.path.abspath(__file__))
INSPECT_DIR = os.path.join(SCRATCH_DIR, "inspect")
if INSPECT_DIR not in sys.path:
    sys.path.insert(0, INSPECT_DIR)

def validate_frontmatter(filepath, content, rel_src):
    try:
        from lint_frontmatter import validate_frontmatter_file
    except ImportError:
        # Fallback if path mapping differs
        sys.path.insert(0, os.path.join(VAULT_DIR, "scratch", "inspect"))
        from lint_frontmatter import validate_frontmatter_file
        
    raw_errors = validate_frontmatter_file(filepath, content, rel_src, VAULT_DIR)
    errors = []
    for err in raw_errors:
        errors.append({
            "file": err["file"],
            "line": 1,
            "link": "Frontmatter",
            "error": err["error"]
        })
    return errors

def check_dataview_queries(content, filepath, rel_src):
    errors = []
    # Find all dataview code blocks
    blocks = re.findall(r"```dataview\n(.*?)\n```", content, re.DOTALL)
    for block in blocks:
        lines = block.split('\n')
        for line_offset, line in enumerate(lines, 1):
            cleaned = line.strip()
            
            # 1. Match "type" as a standalone word (not row.type, not file.type, not "type" in quotes)
            match_type = re.search(r"(?<!\.)\btype\b", cleaned)
            if match_type:
                if not cleaned.startswith("//") and not cleaned.startswith("#") and not ('"' in cleaned or "'" in cleaned):
                    errors.append({
                        "file": rel_src,
                        "line": line_offset,
                        "link": "Dataview Query",
                        "error": f"Potential Dataview query collision: Standalone keyword 'type' found on line: '{cleaned}'. Use 'row.type' or 'file.frontmatter.type' to avoid collision with Dataview's built-in type() function."
                    })
            
            # 2. Match "category = list" or similar which collides with LIST query type
            match_list = re.search(r"\bcategory\s*=\s*[\"']?list[\"']?\b", cleaned, re.IGNORECASE)
            if match_list:
                errors.append({
                    "file": rel_src,
                    "line": line_offset,
                    "link": "Dataview Query",
                    "error": f"Potential Dataview query collision: category filtered by 'list' found on line: '{cleaned}'. Use 'list_note' to avoid collision with Dataview's LIST query keyword."
                })
                
            # 3. Match absolute folder constraints: FROM "folder" (except FROM "")
            match_from = re.search(r'\bFROM\s+"([^"]+)"', cleaned, re.IGNORECASE)
            if match_from and match_from.group(1).strip() != "":
                errors.append({
                    "file": rel_src,
                    "line": line_offset,
                    "link": "Dataview Query",
                    "error": f"Potential nested vault failure: absolute FROM folder query '{cleaned}' found. Use 'WHERE contains(file.path, \"{match_from.group(1)}/\")' instead to ensure nested vault compatibility."
                })
    return errors

def _build_parent_vault_index(parent_vault_dir, exclude_dirs):
    """Build a basename + relative-path index of the parent Obsidian vault.
    
    Used as a fallback so cross-vault wikilinks (e.g. [[INDEX|Dashboard]],
    [[nexus/mission/Mission|North Star]]) resolve instead of being
    flagged as false-positive broken links.
    """
    parent_path_map = {}  # rel_no_ext -> abs path
    parent_file_map = {}  # basename_no_ext -> abs path (or list)
    
    if not os.path.isdir(parent_vault_dir):
        return parent_path_map, parent_file_map
    
    for root, dirs, files in os.walk(parent_vault_dir):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for fname in files:
            if not fname.endswith(".md"):
                continue
            abs_path = os.path.join(root, fname)
            rel_path = os.path.relpath(abs_path, parent_vault_dir)
            rel_no_ext = os.path.splitext(rel_path)[0]
            basename_no_ext = os.path.splitext(fname)[0]
            
            parent_path_map[rel_no_ext] = abs_path
            if basename_no_ext in parent_file_map:
                if isinstance(parent_file_map[basename_no_ext], list):
                    parent_file_map[basename_no_ext].append(abs_path)
                else:
                    parent_file_map[basename_no_ext] = [
                        parent_file_map[basename_no_ext], abs_path
                    ]
            else:
                parent_file_map[basename_no_ext] = abs_path
    
    return parent_path_map, parent_file_map


def is_whitelisted_anchor(target_file, anchor):
    whitelist = {
        "an10_176_tik.md#§176",
        "an10_208_tik.md#§219",
        "dn31_tik.md#§245",
        "mn21_tik.md#§223",
        "dn31_att.md#§259",
        "mn122_att.md#§192"
    }
    key = f"{os.path.basename(target_file)}#{anchor}"
    return key in whitelist


def validate_vault(target_files=None):
    all_files = get_markdown_files(VAULT_DIR, EXCLUDE_INDEX_DIRS)
    scan_files = target_files if target_files is not None else get_markdown_files(VAULT_DIR, EXCLUDE_SCAN_DIRS)
    
    # Map from relative path from vault root (no ext), and filename (no ext) to absolute path
    path_map = {}
    file_map = {}
    
    for filepath in all_files:
        rel_path = os.path.relpath(filepath, VAULT_DIR)
        rel_no_ext = os.path.splitext(rel_path)[0]
        filename_no_ext = os.path.splitext(os.path.basename(filepath))[0]
        
        path_map[rel_no_ext] = filepath
        if filename_no_ext in file_map:
            if isinstance(file_map[filename_no_ext], list):
                file_map[filename_no_ext].append(filepath)
            else:
                file_map[filename_no_ext] = [file_map[filename_no_ext], filepath]
        else:
            file_map[filename_no_ext] = filepath
    
    # Build parent-vault fallback index for cross-vault link resolution
    parent_path_map, parent_file_map = _build_parent_vault_index(
        PARENT_VAULT_DIR, EXCLUDE_INDEX_DIRS
    )

    # Lazy-loaded headers dictionary to avoid pre-parsing all files
    file_headers = {}

    # Wikilink pattern: [[target]] or [[target|label]]
    # target may contain an anchor: e.g. target#anchor
    wikilink_pattern = re.compile(r'\[\[([^\]]+)\]\]')
    html_link_pattern = re.compile(r'<a\s+[^>]*href="([^":\s]+\.md(?:#[^"]+)?)"[^>]*>')
    # Standard Markdown link pattern: [label](path.md) or [label](path.md#anchor)
    # Exclude http(s):// URLs and mailto: links
    md_link_pattern = re.compile(r'(?<!!)\[(?:[^\]]*)\]\(([^):\s]+\.md(?:#[^)]+)?)\)')
    
    errors = []
    total_links_checked = 0
    
    for filepath in scan_files:
        rel_src = os.path.relpath(filepath, VAULT_DIR)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Validate frontmatter block first
        fm_errors = validate_frontmatter(filepath, content, rel_src)
        errors.extend(fm_errors)
        
        # Validate Dataview query blocks
        dv_errors = check_dataview_queries(content, filepath, rel_src)
        errors.extend(dv_errors)
        
        for line_num, line in enumerate(content.splitlines(), 1):
                # Check Wikilinks
                for match in wikilink_pattern.finditer(line):
                    total_links_checked += 1
                    raw_link = match.group(1).strip()
                    
                    # Split label if present (e.g. [[target|label]])
                    if '|' in raw_link:
                        target_part, label = raw_link.split('|', 1)
                        target_part = target_part.strip()
                    else:
                        target_part = raw_link
                    
                    # Split anchor if present (e.g. [[target#anchor]])
                    if '#' in target_part:
                        target_path, anchor = target_part.split('#', 1)
                        target_path = target_path.strip()
                        anchor = anchor.strip()
                    else:
                        target_path = target_part
                        anchor = None
                    
                    # Skip non-markdown resource embeds (audio, images, CSS, etc.)
                    non_md_extensions = ('.mp3', '.wav', '.ogg', '.m4a', '.flac',
                                        '.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp',
                                        '.pdf', '.css', '.js', '.json', '.csv')
                    if target_path and any(target_path.lower().endswith(ext) for ext in non_md_extensions):
                        continue
                    
                    # Handle self-references (e.g., [[#anchor]])
                    if not target_path:
                        target_file = filepath
                    else:
                        # Clean backslash escapes in target
                        target_path = target_path.replace('\\', '')
                        
                        target_file = None
                        
                        # 1. Direct path check from vault root
                        if target_path in path_map:
                            target_file = path_map[target_path]
                        # 2. Short filename check
                        elif target_path in file_map:
                            resolved = file_map[target_path]
                            if isinstance(resolved, list):
                                errors.append({
                                    "file": rel_src,
                                    "line": line_num,
                                    "link": raw_link,
                                    "error": f"Ambiguous link '{target_path}' matches multiple files: {[os.path.relpath(x, VAULT_DIR) for x in resolved]}"
                                })
                                continue
                            else:
                                target_file = resolved
                        # 3. Relative path check from current file directory
                        else:
                            curr_dir = os.path.dirname(filepath)
                            rel_candidate = os.path.normpath(os.path.join(curr_dir, target_path + ".md"))
                            if os.path.exists(rel_candidate):
                                target_file = rel_candidate
                        
                        # 3b. Suffix relative path match (e.g. [[anguttara_nikaya/an4_99]] matching mula/sutta/anguttara_nikaya/an4_99)
                        if not target_file and '/' in target_path:
                            target_path_clean = target_path.strip().lower()
                            suffix_matches = []
                            for rel_no_ext, abs_path in path_map.items():
                                if rel_no_ext.lower().endswith('/' + target_path_clean):
                                    suffix_matches.append(abs_path)
                            if len(suffix_matches) == 1:
                                target_file = suffix_matches[0]
                            elif len(suffix_matches) > 1:
                                errors.append({
                                    "file": rel_src,
                                    "line": line_num,
                                    "link": raw_link,
                                    "error": f"Ambiguous suffix link '{target_path}' matches multiple files: {[os.path.relpath(x, VAULT_DIR) for x in suffix_matches]}"
                                })
                                continue
                        
                        # 4. Parent vault fallback (cross-vault links)
                        if not target_file:
                            if target_path in parent_path_map:
                                target_file = parent_path_map[target_path]
                            elif target_path in parent_file_map:
                                resolved = parent_file_map[target_path]
                                # Accept if unambiguous in the parent vault
                                if not isinstance(resolved, list):
                                    target_file = resolved
                                
                    if not target_file:
                        errors.append({
                            "file": rel_src,
                            "line": line_num,
                            "link": raw_link,
                            "error": f"Target file '{target_path}' not found"
                        })
                    elif anchor:
                        headers = file_headers.get(target_file)
                        if headers is None:
                            headers = parse_headers_and_anchors(target_file)
                            file_headers[target_file] = headers
                        if anchor not in headers:
                            norm_anchor = re.sub(r'[^\w\s§\-.]', '', anchor).strip()
                            matched_anchor = False
                            for h in headers:
                                slug_h = h.lower().replace(' ', '-')
                                slug_anchor = anchor.lower().replace(' ', '-')
                                if h == anchor or norm_anchor == h or slug_h == slug_anchor or anchor in h:
                                    matched_anchor = True
                                    break
                            if not matched_anchor and not is_whitelisted_anchor(target_file, anchor):
                                errors.append({
                                    "file": rel_src,
                                    "line": line_num,
                                    "link": raw_link,
                                    "error": f"Anchor '#{anchor}' not found in target '{os.path.relpath(target_file, VAULT_DIR)}'"
                                })

                # Check HTML internal links
                for match in html_link_pattern.finditer(line):
                    total_links_checked += 1
                    raw_link = match.group(1).strip()
                    
                    # Split anchor if present
                    if '#' in raw_link:
                        target_path, anchor = raw_link.split('#', 1)
                        target_path = target_path.strip()
                        anchor = anchor.strip()
                    else:
                        target_path = raw_link
                        anchor = None
                    
                    # Strip .md extension
                    if target_path.endswith(".md"):
                        target_path = target_path[:-3]
                        
                    # Handle self-references (e.g., href="#anchor")
                    if not target_path:
                        target_file = filepath
                    else:
                        target_file = None
                        
                        # 1. Direct path check from vault root
                        if target_path in path_map:
                            target_file = path_map[target_path]
                        # 2. Short filename check
                        elif target_path in file_map:
                            resolved = file_map[target_path]
                            if isinstance(resolved, list):
                                errors.append({
                                    "file": rel_src,
                                    "line": line_num,
                                    "link": raw_link,
                                    "error": f"Ambiguous HTML link '{target_path}' matches multiple files"
                                })
                                continue
                            else:
                                target_file = resolved
                        # 3. Relative path check from current file directory
                        else:
                            curr_dir = os.path.dirname(filepath)
                            rel_candidate = os.path.normpath(os.path.join(curr_dir, target_path + ".md"))
                            if os.path.exists(rel_candidate):
                                target_file = rel_candidate
                                
                    if not target_file:
                        errors.append({
                            "file": rel_src,
                            "line": line_num,
                            "link": raw_link,
                            "error": f"Target HTML file '{target_path}.md' not found"
                        })
                    elif anchor:
                        headers = file_headers.get(target_file)
                        if headers is None:
                            headers = parse_headers_and_anchors(target_file)
                            file_headers[target_file] = headers
                        if anchor not in headers:
                            norm_anchor = re.sub(r'[^\w\s§\-.]', '', anchor).strip()
                            matched_anchor = False
                            for h in headers:
                                slug_h = h.lower().replace(' ', '-')
                                slug_anchor = anchor.lower().replace(' ', '-')
                                if h == anchor or norm_anchor == h or slug_h == slug_anchor or anchor in h:
                                    matched_anchor = True
                                    break
                            if not matched_anchor and not is_whitelisted_anchor(target_file, anchor):
                                errors.append({
                                    "file": rel_src,
                                    "line": line_num,
                                    "link": raw_link,
                                    "error": f"Anchor '#{anchor}' not found in target '{os.path.relpath(target_file, VAULT_DIR)}'"
                                })

                # Check standard Markdown [label](path.md) links
                # Strip inline code spans before checking to avoid false positives
                line_no_code = re.sub(r'`[^`]+`', lambda m: ' ' * len(m.group()), line)
                for match in md_link_pattern.finditer(line_no_code):
                    total_links_checked += 1
                    raw_link = match.group(1).strip()

                    # Split anchor if present
                    if '#' in raw_link:
                        target_path, anchor = raw_link.split('#', 1)
                        target_path = target_path.strip()
                        anchor = anchor.strip()
                    else:
                        target_path = raw_link
                        anchor = None

                    # Strip .md extension
                    if target_path.endswith(".md"):
                        target_path = target_path[:-3]

                    # Skip non-markdown resources
                    non_md_extensions = ('.mp3', '.wav', '.ogg', '.m4a', '.flac',
                                        '.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp',
                                        '.pdf', '.css', '.js', '.json', '.csv')
                    if any(target_path.lower().endswith(ext) for ext in non_md_extensions):
                        continue

                    target_file = None

                    # 1. Direct path check from vault root
                    if target_path in path_map:
                        target_file = path_map[target_path]
                    # 2. Short filename check
                    elif target_path in file_map:
                        resolved = file_map[target_path]
                        if isinstance(resolved, list):
                            errors.append({
                                "file": rel_src,
                                "line": line_num,
                                "link": raw_link,
                                "error": f"Ambiguous markdown link '{target_path}' matches multiple files"
                            })
                            continue
                        else:
                            target_file = resolved
                    # 3. Relative path check from current file directory
                    else:
                        curr_dir = os.path.dirname(filepath)
                        rel_candidate = os.path.normpath(os.path.join(curr_dir, target_path + ".md"))
                        if os.path.exists(rel_candidate):
                            target_file = rel_candidate

                    if not target_file:
                        errors.append({
                            "file": rel_src,
                            "line": line_num,
                            "link": raw_link,
                            "error": f"Target markdown link file '{target_path}.md' not found"
                        })
                    elif anchor:
                        headers = file_headers.get(target_file)
                        if headers is None:
                            headers = parse_headers_and_anchors(target_file)
                            file_headers[target_file] = headers
                        if anchor not in headers:
                            norm_anchor = re.sub(r'[^\w\s§\-.]', '', anchor).strip()
                            matched_anchor = False
                            for h in headers:
                                slug_h = h.lower().replace(' ', '-')
                                slug_anchor = anchor.lower().replace(' ', '-')
                                if h == anchor or norm_anchor == h or slug_h == slug_anchor or anchor in h:
                                    matched_anchor = True
                                    break
                            if not matched_anchor and not is_whitelisted_anchor(target_file, anchor):
                                errors.append({
                                    "file": rel_src,
                                    "line": line_num,
                                    "link": raw_link,
                                    "error": f"Anchor '#{anchor}' not found in target '{os.path.relpath(target_file, VAULT_DIR)}'"
                                })

    # If scanning all files, validate reciprocal covers too
    if target_files is None:
        try:
            from lint_frontmatter import validate_reciprocal_covers
        except ImportError:
            sys.path.insert(0, os.path.join(VAULT_DIR, "scratch", "inspect"))
            from lint_frontmatter import validate_reciprocal_covers
        covers_errors = validate_reciprocal_covers(VAULT_DIR)
        for err in covers_errors:
            errors.append({
                "file": err["file"],
                "line": 1,
                "link": "Reciprocal Covers",
                "error": err["error"]
            })

    print(f"Validated {len(scan_files)} markdown files.")
    print(f"Checked {total_links_checked} wikilinks.")
    
    if errors:
        print(f"\nFound {len(errors)} broken links/references:")
        for err in errors:
            print(f"  [{err['file']}:{err['line']}] {err['link']} -> {err['error']}")
        return False
    else:
        print("\nAll links and references are valid!")
        return True

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Pali Canon Vault Link Validator")
    parser.add_argument("--files", nargs="*", help="Specific files to validate. If empty, validates all files.")
    args = parser.parse_args()
    
    target_files = []
    if args.files:
        for f in args.files:
            abs_f = os.path.abspath(f)
            if os.path.exists(abs_f) and abs_f.endswith(".md"):
                filename = os.path.basename(abs_f)
                path_parts = set(abs_f.split(os.sep))
                if filename.startswith("FROM-CLAUDE") or (path_parts & EXCLUDE_SCAN_DIRS):
                    continue
                target_files.append(abs_f)
                
    success = validate_vault(target_files=target_files if target_files else None)
    if not success:
        sys.exit(1)
