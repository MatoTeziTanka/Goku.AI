#!/usr/bin/env python3
"""
Estimate cost for Claude Opus 4.5 comprehensive review.

Calculates token usage and cost for:
1. Reviewing entire codebase using Master Prompt v2.6.0 as QC
2. Auditing Master Prompt v2.6.0 itself for improvements
3. Logging all issues, changes, before/after (no actual changes)
"""

import os
from pathlib import Path

# Claude Opus 4.5 Pricing (per million tokens)
OPUS_4_5_INPUT = 5.00  # $5 per MTok
OPUS_4_5_OUTPUT = 25.00  # $25 per MTok
OPUS_4_5_CACHE_WRITE = 6.25  # $6.25 per MTok
OPUS_4_5_CACHE_READ = 0.50  # $0.50 per MTok

# Batch pricing (if using batch API)
OPUS_4_5_BATCH_INPUT = 2.50  # $2.50 per MTok
OPUS_4_5_BATCH_OUTPUT = 12.50  # $12.50 per MTok

def estimate_tokens(text: str) -> int:
    """
    Rough token estimation: ~4 characters per token for English text.
    More accurate: ~0.75 tokens per word, or use tiktoken for exact count.
    """
    # Conservative estimate: 4 chars per token
    char_estimate = len(text) / 4
    
    # Word-based estimate (more accurate for English)
    words = len(text.split())
    word_estimate = words * 0.75
    
    # Use the higher estimate (more conservative)
    return int(max(char_estimate, word_estimate))

def read_master_prompt() -> tuple[str, int]:
    """Read master prompt and estimate tokens."""
    master_prompt_path = Path("MASTER-PROMPT-PERPETUAL-SELF-UPDATING-AI-MIND-IMPROVED-v2.6.0.md")
    
    if not master_prompt_path.exists():
        # Try parent directory
        master_prompt_path = Path("../MASTER-PROMPT-PERPETUAL-SELF-UPDATING-AI-MIND-IMPROVED-v2.6.0.md")
    
    if master_prompt_path.exists():
        content = master_prompt_path.read_text(encoding='utf-8')
        tokens = estimate_tokens(content)
        return content, tokens
    else:
        print(f"⚠️  Master prompt not found at {master_prompt_path}")
        return "", 0

def estimate_codebase_size() -> tuple[int, int]:
    """Estimate total codebase size in tokens."""
    github_root = Path("C:/Users/sethp/Documents/Github")
    
    # Key directories to review
    code_dirs = [
        github_root / "BitPhoenix",
        github_root / "DinoCloud",
        github_root / "Goku.AI",
        github_root / "GSMG.IO",
        github_root / "KeyHound",
        github_root / "ScalpStorm",
        github_root / "StreamForge",
        github_root / "FamilyFork",
    ]
    
    total_tokens = 0
    total_files = 0
    
    code_extensions = {'.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rs', '.md'}
    
    # Directories to skip
    skip_dirs = {
        'node_modules', '.git', '__pycache__', '.pytest_cache', 
        'venv', 'env', '.venv', 'dist', 'build', '.next', 
        'target', 'bin', 'obj', '.idea', '.vscode'
    }
    
    for code_dir in code_dirs:
        if not code_dir.exists():
            continue
        
        try:
            for file_path in code_dir.rglob('*'):
                try:
                    # Skip if path contains any skip directory
                    if any(skip_dir in file_path.parts for skip_dir in skip_dirs):
                        continue
                    
                    # Skip if not a file or wrong extension
                    if not file_path.is_file() or file_path.suffix not in code_extensions:
                        continue
                    
                    # Try to read file
                    try:
                        content = file_path.read_text(encoding='utf-8', errors='ignore')
                        tokens = estimate_tokens(content)
                        total_tokens += tokens
                        total_files += 1
                    except (OSError, PermissionError, UnicodeDecodeError):
                        # Skip files that can't be read
                        continue
                        
                except (OSError, PermissionError):
                    # Skip inaccessible files/directories
                    continue
        except (OSError, PermissionError):
            # Skip inaccessible directories
            continue
    
    return total_tokens, total_files

def calculate_review_cost():
    """Calculate total cost for comprehensive review."""
    print("=" * 70)
    print("CLAUDE OPUS 4.5 COMPREHENSIVE REVIEW COST ESTIMATE")
    print("=" * 70)
    print()
    
    # 1. Read Master Prompt
    print("📋 Step 1: Analyzing Master Prompt v2.6.0...")
    master_content, master_tokens = read_master_prompt()
    print(f"   Master Prompt: {master_tokens:,} tokens ({len(master_content):,} chars)")
    print()
    
    # 2. Estimate codebase size
    print("📁 Step 2: Estimating codebase size...")
    codebase_tokens, file_count = estimate_codebase_size()
    print(f"   Codebase: ~{codebase_tokens:,} tokens across ~{file_count:,} files")
    print()
    
    # 3. Calculate review requirements
    print("🔍 Step 3: Calculating review requirements...")
    print()
    
    # Review prompt (instructions for Claude)
    review_prompt = """
    Perform comprehensive review of codebase using Master Prompt v2.6.0 as QC reference.
    
    For each file:
    1. Log all problems and issues
    2. Log what should be changed and why
    3. Provide before/after examples (no actual changes)
    4. Rate against Master Prompt standards
    
    Also audit Master Prompt itself for improvements.
    """
    
    review_prompt_tokens = estimate_tokens(review_prompt)
    
    # Input tokens = Master Prompt + Codebase + Review Instructions
    total_input_tokens = master_tokens + codebase_tokens + review_prompt_tokens
    
    # Output tokens (comprehensive review report)
    # Estimate: ~30-50% of input for detailed review
    # For comprehensive logging, estimate higher
    output_tokens = int(total_input_tokens * 0.4)  # 40% of input
    
    print(f"   Input tokens: {total_input_tokens:,}")
    print(f"   Estimated output tokens: {output_tokens:,}")
    print()
    
    # 4. Calculate costs
    print("💰 Step 4: Cost Calculation")
    print("-" * 70)
    
    # Standard pricing
    input_cost_standard = (total_input_tokens / 1_000_000) * OPUS_4_5_INPUT
    output_cost_standard = (output_tokens / 1_000_000) * OPUS_4_5_OUTPUT
    total_cost_standard = input_cost_standard + output_cost_standard
    
    print(f"Standard API Pricing:")
    print(f"  Input:  ${input_cost_standard:,.2f} ({total_input_tokens:,} tokens × $5/MTok)")
    print(f"  Output: ${output_cost_standard:,.2f} ({output_tokens:,} tokens × $25/MTok)")
    print(f"  Total:  ${total_cost_standard:,.2f}")
    print()
    
    # Batch pricing (if using batch API - 50% discount)
    input_cost_batch = (total_input_tokens / 1_000_000) * OPUS_4_5_BATCH_INPUT
    output_cost_batch = (output_tokens / 1_000_000) * OPUS_4_5_BATCH_OUTPUT
    total_cost_batch = input_cost_batch + output_cost_batch
    
    print(f"Batch API Pricing (50% discount):")
    print(f"  Input:  ${input_cost_batch:,.2f} ({total_input_tokens:,} tokens × $2.50/MTok)")
    print(f"  Output: ${output_cost_batch:,.2f} ({output_tokens:,} tokens × $12.50/MTok)")
    print(f"  Total:  ${total_cost_batch:,.2f}")
    print()
    
    # With prompt caching (if Master Prompt is cached)
    # First request: Write cache (Master Prompt)
    cache_write_cost = (master_tokens / 1_000_000) * OPUS_4_5_CACHE_WRITE
    
    # Subsequent requests: Read from cache
    cache_read_cost = (master_tokens / 1_000_000) * OPUS_4_5_CACHE_READ
    
    # If reviewing multiple times, cache helps
    print(f"With Prompt Caching (if reviewing multiple times):")
    print(f"  First request (write cache): ${cache_write_cost:,.2f}")
    print(f"  Subsequent requests (read cache): ${cache_read_cost:,.2f} per review")
    print(f"  Savings on subsequent reviews: ${(master_tokens / 1_000_000) * (OPUS_4_5_INPUT - OPUS_4_5_CACHE_READ):,.2f}")
    print()
    
    # 5. Recommendations
    print("💡 Recommendations:")
    print("-" * 70)
    print(f"1. Use Batch API if possible: Save ${total_cost_standard - total_cost_batch:,.2f} (50% discount)")
    print(f"2. Use Prompt Caching: Cache Master Prompt to save on repeated reviews")
    print(f"3. Break into smaller reviews: Review one repo at a time to manage costs")
    print(f"4. Focus on critical files first: Review high-priority files, then expand")
    print()
    
    # 6. Alternative: Review just Master Prompt
    print("📊 Alternative: Review Only Master Prompt v2.6.0")
    print("-" * 70)
    
    master_review_prompt = "Audit Master Prompt v2.6.0 for improvements. Log all issues, suggested changes, and before/after examples."
    master_review_input = master_tokens + estimate_tokens(master_review_prompt)
    master_review_output = int(master_review_input * 0.5)  # 50% for detailed audit
    
    master_input_cost = (master_review_input / 1_000_000) * OPUS_4_5_INPUT
    master_output_cost = (master_review_output / 1_000_000) * OPUS_4_5_OUTPUT
    master_total_cost = master_input_cost + master_output_cost
    
    print(f"  Input:  ${master_input_cost:,.2f}")
    print(f"  Output: ${master_output_cost:,.2f}")
    print(f"  Total:  ${master_total_cost:,.2f}")
    print()
    
    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Full Codebase Review:")
    print(f"  Standard: ${total_cost_standard:,.2f}")
    print(f"  Batch:    ${total_cost_batch:,.2f} (recommended)")
    print()
    print(f"Master Prompt Only Review:")
    print(f"  Cost:     ${master_total_cost:,.2f}")
    print()
    print(f"Note: Actual costs may vary based on:")
    print(f"  - Actual token counts (this is an estimate)")
    print(f"  - Response length (comprehensive reviews may be longer)")
    print(f"  - Number of files reviewed")
    print(f"  - Whether prompt caching is used")
    print()

if __name__ == "__main__":
    calculate_review_cost()

