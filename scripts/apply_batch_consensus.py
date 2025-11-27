#!/usr/bin/env python3
import os
import json
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

GITHUB_ROOT = Path("C:/Users/sethp/Documents/Github")
REPOS = {
    "Keyhound": "Keyhound",
    "BitPhoenix": "BitPhoenix",
    "Dell-Server-Roadmap": "Dell-Server-Roadmap",
    "Scalpstorm": "Scalpstorm",
    "Goku.AI": "Goku.AI",
    "Dino-Cloud": "Dino-Cloud",
    "FamilyFork": "FamilyFork",
    "DinoCloud": "DinoCloud",
    "GSMG.IO": "GSMG.IO",
    "Server-Roadmap": "Server-Roadmap",
    "StreamForge": "StreamForge"
}

PRIORITY_LEVELS = {
    "Critical": 1,
    "High": 2,
    "Medium": 3,
    "Low": 4
}

class BatchConsensusApplier:
    def __init__(self):
        self.consensus_files = {}
        self.changes_log = []
        self.errors_log = []
        self.applied_count = 0
        self.skipped_count = 0
    
    def load_consensus_files(self):
        print("[PHASE 2] Loading consensus files...")
        for cf in GITHUB_ROOT.glob("*-FINAL-CONSENSUS.md"):
            try:
                with open(cf, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.consensus_files[cf.name] = content
                    print(f"  [OK] {cf.name}")
            except Exception as e:
                self.errors_log.append(f"Failed to load {cf.name}: {e}")
                print(f"  [FAIL] {cf.name}: {e}")
        
        print(f"\n[OK] Loaded {len(self.consensus_files)} consensus files")
        return len(self.consensus_files) > 0
    
    def extract_changes(self):
        print("\n[PHASE 2] Extracting changes from consensus files...")
        changes_by_priority = defaultdict(list)
        
        for filename, content in self.consensus_files.items():
            json_match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
            if json_match:
                try:
                    spec = json.loads(json_match.group(1))
                    priority = spec.get("priority", "Medium")
                    
                    change_entry = {
                        "file": filename,
                        "repo": filename.split("-FINAL")[0],
                        "priority": priority,
                        "spec": spec,
                        "changes": spec.get("changes", [])
                    }
                    changes_by_priority[priority].append(change_entry)
                    print(f"  [OK] {filename}: {len(spec.get('changes', []))} changes (Priority: {priority})")
                except json.JSONDecodeError as e:
                    self.errors_log.append(f"JSON parse error in {filename}: {e}")
            else:
                print(f"  [SKIP] {filename}: No JSON spec found")
                self.skipped_count += 1
        
        print(f"\n[OK] Extracted changes by priority:")
        for priority in sorted(changes_by_priority.keys(), key=lambda p: PRIORITY_LEVELS.get(p, 999)):
            count = sum(len(c["changes"]) for c in changes_by_priority[priority])
            print(f"  - {priority}: {count} changes")
        
        return changes_by_priority
    
    def apply_changes_in_order(self, changes_by_priority):
        print("\n[PHASE 2] Applying changes in priority order...")
        total_changes = 0
        
        sorted_priorities = sorted(changes_by_priority.keys(), 
                                   key=lambda p: PRIORITY_LEVELS.get(p, 999))
        
        for priority in sorted_priorities:
            print(f"\n[APPLYING {priority.upper()} PRIORITY CHANGES]")
            for change_entry in changes_by_priority[priority]:
                repo_name = change_entry["repo"]
                repo_path = GITHUB_ROOT / repo_name
                
                if not repo_path.exists():
                    self.errors_log.append(f"Repository not found: {repo_name}")
                    print(f"  [SKIP] {repo_name} - Repository not found")
                    self.skipped_count += 1
                    continue
                
                for change in change_entry["changes"]:
                    self._apply_single_change(repo_name, repo_path, change, priority)
                    total_changes += 1
        
        print(f"\n[OK] Applied {self.applied_count} changes, skipped {self.skipped_count}")
        return total_changes
    
    def _apply_single_change(self, repo_name, repo_path, change, priority):
        change_type = change.get("type", "").upper()
        
        if change_type == "CREATE":
            self._create_file(repo_name, repo_path, change)
        elif change_type == "UPDATE":
            self._update_file(repo_name, repo_path, change)
        elif change_type == "DELETE":
            self._delete_file(repo_name, repo_path, change)
        else:
            self.errors_log.append(f"Unknown change type: {change_type}")
    
    def _create_file(self, repo_name, repo_path, change):
        file_path = repo_path / change.get("file", "")
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(change.get("content", ""))
            
            self.applied_count += 1
            self.changes_log.append({
                "repo": repo_name,
                "type": "CREATE",
                "file": str(file_path),
                "status": "OK"
            })
            print(f"  [CREATE] {repo_name}/{change.get('file')}")
        except Exception as e:
            self.errors_log.append(f"Failed to create {file_path}: {e}")
            print(f"  [FAIL] {repo_name}/{change.get('file')}: {e}")
    
    def _update_file(self, repo_name, repo_path, change):
        file_path = repo_path / change.get("file", "")
        
        if not file_path.exists():
            self.errors_log.append(f"File not found for update: {file_path}")
            print(f"  [SKIP] {repo_name}/{change.get('file')} - File not found")
            self.skipped_count += 1
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            old_string = change.get("old_string", "")
            new_string = change.get("new_string", "")
            
            if old_string not in content:
                self.errors_log.append(f"Old string not found in {file_path}")
                print(f"  [SKIP] {repo_name}/{change.get('file')} - Pattern not found")
                self.skipped_count += 1
                return
            
            updated_content = content.replace(old_string, new_string)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            self.applied_count += 1
            self.changes_log.append({
                "repo": repo_name,
                "type": "UPDATE",
                "file": str(file_path),
                "status": "OK"
            })
            print(f"  [UPDATE] {repo_name}/{change.get('file')}")
        except Exception as e:
            self.errors_log.append(f"Failed to update {file_path}: {e}")
            print(f"  [FAIL] {repo_name}/{change.get('file')}: {e}")
    
    def _delete_file(self, repo_name, repo_path, change):
        file_path = repo_path / change.get("file", "")
        
        if not file_path.exists():
            print(f"  [SKIP] {repo_name}/{change.get('file')} - File not found")
            self.skipped_count += 1
            return
        
        try:
            file_path.unlink()
            self.applied_count += 1
            self.changes_log.append({
                "repo": repo_name,
                "type": "DELETE",
                "file": str(file_path),
                "status": "OK"
            })
            print(f"  [DELETE] {repo_name}/{change.get('file')}")
        except Exception as e:
            self.errors_log.append(f"Failed to delete {file_path}: {e}")
            print(f"  [FAIL] {repo_name}/{change.get('file')}: {e}")
    
    def save_log(self):
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "applied": self.applied_count,
            "skipped": self.skipped_count,
            "errors": len(self.errors_log),
            "changes": self.changes_log[:100],
            "errors_log": self.errors_log[:50]
        }
        
        with open("CODE_AGENT_CHANGES_LOG.md", 'w', encoding='utf-8') as f:
            f.write("# Code Agent Changes Log - Phase 2\n\n")
            f.write(f"**Timestamp**: {log_data['timestamp']}\n\n")
            f.write(f"## Summary\n")
            f.write(f"- Applied: {self.applied_count}\n")
            f.write(f"- Skipped: {self.skipped_count}\n")
            f.write(f"- Errors: {len(self.errors_log)}\n\n")
            
            if self.errors_log:
                f.write("## Errors\n")
                for error in self.errors_log[:10]:
                    f.write(f"- {error}\n")
        
        print(f"\n[OK] Log saved to CODE_AGENT_CHANGES_LOG.md")

def main():
    print("="*80)
    print("PHASE 2: BATCH APPLICATION - Code Agent")
    print("="*80)
    
    applier = BatchConsensusApplier()
    
    if not applier.load_consensus_files():
        print("[FAIL] No consensus files loaded")
        return False
    
    changes_by_priority = applier.extract_changes()
    
    if not changes_by_priority:
        print("[WARN] No changes found in consensus files")
        return False
    
    total = applier.apply_changes_in_order(changes_by_priority)
    
    applier.save_log()
    
    print("\n" + "="*80)
    print(f"PHASE 2 COMPLETE: {applier.applied_count} changes applied")
    print("="*80)
    
    return applier.applied_count > 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
