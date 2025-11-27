#!/usr/bin/env python3
"""
Analyze and Organize BitPhoenix Files
Identifies files that should be moved to EOL or "Doesnt Belong"
Uses Azure API (GPT-4.1) to analyze file purposes
"""

import json
import sys
from pathlib import Path
from foundry_local_agent import FoundryClaudeAgent
from datetime import datetime
import os

# Root directory
ROOT = Path("BitPhoenix")

# Files/directories that are definitely core project
CORE_FILES = {
    'backend', 'frontend', 'cursor-extension', 'docs', 
    'scripts', 'deployment', '.github', '.git',
    'README.md', 'LICENSE', 'CHANGELOG.md',
    '.gitignore', '.editorconfig',
    'API_DOCUMENTATION.md', 'DEVELOPMENT_GUIDE.md',
    'DEPLOYMENT_GUIDE.md', 'DOCKER_DEPLOYMENT.md',
    'CONTRIBUTING.md', 'CODE_OF_CONDUCT.md',
    'ENTERPRISE_STANDARDS.md', 'enterprise_scanner.py',
    'run_scanner.py', 'analyze_blockers.py',
    'docker-compose.yml', 'docker-compose.prod.yml',
    'deploy.sh', 'requirements.txt',
}

# Files/directories already in EOL
EOL_EXISTING = {
    'ALL_SERVICES_CONFIGURED.md', 'CLEANUP_COMPLETE.md',
    'CLEANUP_MULTI_AGENT.md', 'SETUP_COMPLETE.md',
    'READY_TO_START.md', 'FINAL_SETUP_INSTRUCTIONS.md',
    'MEMORY_STORAGE_CONFIRMED.md', 'MEMORY_STORAGE_SETUP.md',
    'YOUR_AI_SETUP.md', 'YOUR_COMPLETE_SETUP.md',
    'NEXT_STEPS.md', 'START_HERE.md', 'QUICK_START.md',
    'STEP_BY_STEP_SETUP.md', 'ONBOARDING_GUIDE.md',
    'ONE_EXTENSION_ALL_REPOS.md', 'CURSOR_EXTENSION_SETUP.md',
    'AUDIT_REPORT_V1.0.0.md', 'WSL_SETUP_GUIDE.md',
    'install-wsl.sh', 'test_pat_update.txt', 'scan_results.json',
}

# Files/directories already in "Doesnt Belong"
DOESNT_BELONG_EXISTING = {
    'shenron-env', 'shenron-ultra-instinct', 
    'Marketing-Automation', 'documentation', 'venv'
}

def analyze_file_with_azure(agent: FoundryClaudeAgent, file_path: Path, relative_path: str) -> dict:
    """Analyze a file using Azure API to determine if it belongs"""
    print(f"  Analyzing: {relative_path}...")
    
    try:
        # Read file (limit size for API)
        if file_path.is_file():
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()[:4000]  # Limit to 4000 chars
            except:
                content = f"[Binary or unreadable file: {file_path.name}]"
        else:
            content = f"[Directory: {file_path.name}]"
        
        # Create analysis prompt
        prompt = f"""Analyze this file from the BitPhoenix data recovery project:

Path: {relative_path}
Name: {file_path.name}

Content preview:
{content}

Determine:
1. **Purpose**: What is this file's purpose?
2. **Value**: Does it add value to the BitPhoenix project?
3. **Status**: Is it active/current or deprecated/old?
4. **Category**: 
   - KEEP: Core project file (backend, frontend, docs, scripts)
   - EOL: End of life - old setup guides, deprecated docs, completed cleanup files
   - DOESNT_BELONG: Not part of BitPhoenix (other projects, test files, unrelated)

Provide:
- Category: KEEP, EOL, or DOESNT_BELONG
- Reason: Brief explanation
- Confidence: High/Medium/Low
"""
        
        # Get analysis from Azure API (with rate limiting)
        import time
        question = prompt  # Use analyze_file which takes a question
        
        # Retry with exponential backoff for rate limits
        max_retries = 3
        retry_delay = 2
        for attempt in range(max_retries):
            try:
                response = agent.analyze_file(str(file_path), question)
                break
            except Exception as e:
                error_msg = str(e)
                if "429" in error_msg or "RateLimit" in error_msg:
                    if attempt < max_retries - 1:
                        # Extract wait time from error if available
                        if "retry after" in error_msg.lower():
                            try:
                                wait_time = int(error_msg.split("retry after")[1].split()[0])
                                print(f"    ⚠ Rate limit hit. Waiting {wait_time} seconds...")
                                time.sleep(wait_time + 1)
                            except:
                                wait_time = retry_delay * (2 ** attempt)
                                print(f"    ⚠ Rate limit hit. Waiting {wait_time} seconds...")
                                time.sleep(wait_time)
                        else:
                            wait_time = retry_delay * (2 ** attempt)
                            print(f"    ⚠ Rate limit hit. Waiting {wait_time} seconds...")
                            time.sleep(wait_time)
                        continue
                raise
        
        # Extract category from response
        category = "UNKNOWN"
        if response:
            response_lower = response.lower()
            if "doesnt belong" in response_lower or "doesn't belong" in response_lower:
                category = "DOESNT_BELONG"
            elif "eol" in response_lower or "end of life" in response_lower or "deprecated" in response_lower:
                category = "EOL"
            elif "keep" in response_lower or "core" in response_lower:
                category = "KEEP"
        
        return {
            'path': relative_path,
            'name': file_path.name,
            'type': 'directory' if file_path.is_dir() else 'file',
            'category': category,
            'analysis': response[:1000] if response else "No analysis",
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"    ✗ Error analyzing {relative_path}: {e}")
        return {
            'path': relative_path,
            'name': file_path.name,
            'type': 'directory' if file_path.is_dir() else 'file',
            'category': 'ERROR',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }

def should_skip(path: Path) -> bool:
    """Determine if a path should be skipped from analysis"""
    name = path.name
    
    # Skip hidden files/directories
    if name.startswith('.'):
        return True
    
    # Skip if already in EOL or Doesnt Belong
    if path.parts[0] in ['EOL', 'Doesnt Belong']:
        return True
    
    # Skip core files (they're definitely keep)
    if name in CORE_FILES:
        return True
    
    # Skip common build/cache directories
    if name in ['__pycache__', 'node_modules', 'build', 'dist', 'venv', '.venv', 'env', '.env']:
        return True
    
    # Skip log files
    if name.endswith('.log'):
        return True
    
    return False

def quick_classify(path: Path) -> str:
    """Quick classification without API call for obvious cases"""
    name = path.name
    
    # Release documentation files (keep, but in root)
    if name.startswith('RELEASE_') or name.startswith('V1.0.0_') or name.startswith('prepare_'):
        return 'KEEP'
    
    # Old setup/test files
    if name in ['test.py', 'final_move.py', 'test_pat_update.txt']:
        return 'EOL'
    
    # Week progress files (might be EOL)
    if name.startswith('WEEK') and name.endswith('.md'):
        return 'EOL'
    
    # Progress/status files
    if any(keyword in name for keyword in ['PROGRESS', 'READINESS', 'FINAL_REVIEW', 'REVIEW_SUMMARY']):
        return 'EOL'
    
    # Unknown - needs API analysis
    return 'UNKNOWN'

def main():
    """Main analysis function"""
    print("="*70)
    print("BitPhoenix File Organization Analysis")
    print("Using Azure API (GPT-4.1) for file analysis")
    print("="*70)
    
    if not ROOT.exists():
        print(f"✗ Error: {ROOT} directory not found")
        sys.exit(1)
    
    # Initialize Azure agent
    try:
        agent = FoundryClaudeAgent()
        print(f"✓ Azure agent initialized (Model: {agent.model})")
    except Exception as e:
        print(f"✗ Error initializing Azure agent: {e}")
        sys.exit(1)
    
    # Find files to analyze
    print("\nScanning files...")
    files_to_analyze = []
    
    for item in ROOT.iterdir():
        if should_skip(item):
            continue
        
        quick_cat = quick_classify(item)
        if quick_cat == 'UNKNOWN':
            files_to_analyze.append(item)
        else:
            print(f"  {quick_cat}: {item.name} (quick classification)")
    
    print(f"\nFound {len(files_to_analyze)} files/directories to analyze with Azure API")
    
    # Analyze files with Azure API
    results = []
    for i, file_path in enumerate(files_to_analyze, 1):
        relative_path = str(file_path.relative_to(ROOT.parent))
        print(f"\n[{i}/{len(files_to_analyze)}] Analyzing: {file_path.name}")
        
        result = analyze_file_with_azure(agent, file_path, relative_path)
        results.append(result)
        
        print(f"  Category: {result['category']}")
    
    # Categorize results
    keep_files = [r for r in results if r['category'] == 'KEEP']
    eol_files = [r for r in results if r['category'] == 'EOL']
    doesnt_belong_files = [r for r in results if r['category'] == 'DOESNT_BELONG']
    unknown_files = [r for r in results if r['category'] == 'UNKNOWN']
    
    # Summary
    print("\n" + "="*70)
    print("ANALYSIS SUMMARY")
    print("="*70)
    print(f"\nTotal Analyzed: {len(results)}")
    print(f"✓ Keep: {len(keep_files)}")
    print(f"🗑️  EOL: {len(eol_files)}")
    print(f"📦 Doesn't Belong: {len(doesnt_belong_files)}")
    print(f"? Unknown: {len(unknown_files)}")
    
    # Show recommendations
    if eol_files:
        print("\n📋 Files recommended for EOL:")
        for r in eol_files:
            print(f"  - {r['path']}")
    
    if doesnt_belong_files:
        print("\n📋 Files recommended for 'Doesnt Belong':")
        for r in doesnt_belong_files:
            print(f"  - {r['path']}")
    
    # Save results
    output_file = ROOT / "file_organization_analysis.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'total_analyzed': len(results),
            'keep': len(keep_files),
            'eol': len(eol_files),
            'doesnt_belong': len(doesnt_belong_files),
            'unknown': len(unknown_files),
            'results': results,
            'recommendations': {
                'eol': [r['path'] for r in eol_files],
                'doesnt_belong': [r['path'] for r in doesnt_belong_files]
            }
        }, f, indent=2)
    
    print(f"\n✓ Analysis results saved to: {output_file}")
    print("\nNext step: Review recommendations and run commit script")

if __name__ == "__main__":
    main()

