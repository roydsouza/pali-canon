#!/usr/bin/env python3
import os
import sys
import subprocess
import time

# Target suttas for the first run of Parcel D
SUTTAS = ["mn4", "mn9", "mn18", "mn62", "mn143", "mn152"]

VAULT = "/Users/rds/Library/Mobile Documents/iCloud~md~obsidian/Documents/Megha/topics/texts/pali-canon"
os.environ["PALI_VAULT"] = VAULT

def run_cmd(cmd, cwd=VAULT):
    print(f"Running command: {cmd}")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
    if res.returncode != 0:
        print(f"ERROR running command: {cmd}\nStdout:\n{res.stdout}\nStderr:\n{res.stderr}")
        return False, res.stdout, res.stderr
    return True, res.stdout, res.stderr

def main():
    print(f"Starting batch migration of {len(SUTTAS)} suttas...")
    
    for sutta in SUTTAS:
        print(f"\n========================================\nProcessing Sutta: {sutta}\n========================================")
        
        # 1. Generate sutta
        success, stdout, stderr = run_cmd(f"python3 scratch/generators/generate_sutta.py --sutta {sutta}")
        if not success:
            print(f"Skipping {sutta} due to generation error.")
            continue
            
        print(stdout)
        
        # 2. Run validator
        val_success, val_out, val_err = run_cmd("python3 scratch/validate_links.py")
        if not val_success:
            print(f"Link validation failed after generating {sutta}. Restoring changes...")
            run_cmd(f"git checkout -- mula/sutta/")
            continue
            
        # 3. Add & Commit
        # Determine if commentary files exist so we can commit them too
        mula_path = f"mula/sutta/majjhima_nikaya/{sutta}.md"
        att_path = f"atthakatha/sutta/majjhima_nikaya/{sutta}_att.md"
        tika_path = f"tika/sutta/majjhima_nikaya/{sutta}_tik.md"
        
        git_add_cmd = f"git add {mula_path}"
        if os.path.exists(os.path.join(VAULT, att_path)):
            git_add_cmd += f" {att_path}"
        if os.path.exists(os.path.join(VAULT, tika_path)):
            git_add_cmd += f" {tika_path}"
            
        run_cmd(git_add_cmd)
        
        commit_msg = f"feat: migrate {sutta} (mula)"
        if os.path.exists(os.path.join(VAULT, att_path)):
            commit_msg = f"feat: migrate {sutta} (mula/att/tika)" if os.path.exists(os.path.join(VAULT, tika_path)) else f"feat: migrate {sutta} (mula/att)"
            
        success_commit, _, _ = run_cmd(f'git commit -m "{commit_msg}"')
        if success_commit:
            print(f"Successfully committed {sutta}!")
            # Run git push since the post-commit hook might run it or we can push manually
            run_cmd("git push origin main")
            
        # Be gentle to APIs
        time.sleep(2)
        
    print("\nBatch migration complete!")

if __name__ == "__main__":
    main()
