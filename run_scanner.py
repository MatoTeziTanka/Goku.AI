```python
#!/usr/bin/env python3
"""
BitPhoenix Enterprise Scanner Runner
=====================================

Executes the enterprise code quality scanner and generates reports.

Author: BitPhoenix Engineering Team
Version: 1.0.0

Critical File - Mars-level Quality Assurance Commitment:

Core Principles:
    - Enterprise-grade code quality and security
    - Fully functional, documented, and auditable
    - Security Sentinel agent: Advanced threat detection, secure coding (OWASP Top 10, CWE)

Usage:
    $ python run_scanner.py [--json-output JSON_PATH] [--html-output HTML_PATH] [--md-output MD_PATH]
    (All arguments optional; defaults used if not provided.)

Required Dependencies:
    - Python 3.x
    - enterprise_scanner.py (must be present in the current directory)
    - No hardcoded secrets or unsafe dependencies

Configuration:
    - Excluded directories can be set in EXCLUDED_DIRS at top of file
    - Output filenames (JSON, HTML, Markdown) are configurable via CLI args

Expected Environment:
    - Cross-platform: Windows and Linux compatible
    - Consistent UTF-8 encoding for all outputs
    - All references and documentation synchronized to v1.0.0

CRITICAL VERSIONING REQUIREMENT:
    - Repository version: 1.0.0
    - All files and documentation synchronized with version 1.0.0

TODO(docguru):
    - Make excluded directories and output filenames fully configurable via config file
    - Refactor main workflow for extensibility (modularize reporting, error handling)
    - Add resource cleanup hooks for scanner (if resources allocated)
    - Enhance import diagnostics and error telemetry
    - Validate and sanitize scan_results.json if loaded elsewhere (see security section)
    - Add support for loading more advanced configuration files

Wiki-Ready Documentation Index:
    - Block comments: Purpose of major code sections
    - Inline comments: Explanation of complex logic and rationale
    - Docstrings: All functions, classes, and major blocks
    - TODO(username): Future improvements and technical debt
    - Type hints: All function parameters and return values

Enterprise Documentation Standards:
    - Sphinx/Google/NumPy-style docstrings everywhere
    - Mars-level clarity, maintainability, and scalability
    - All exceptions, parameters, side effects documented
    - Comprehensive, auditable, and future-proof

Example Usage:
    $ python run_scanner.py --json-output results.json --html-output results.html --md-output results.md

SECURITY SENTINEL NOTES:
    - No hardcoded secrets, tokens, or passwords
    - No unsafe deserialization: scan_results.json is written only; if loaded elsewhere, must validate/sanitize
    - No deprecated libraries or insecure patterns
    - All input/output paths must be validated for safety if loaded elsewhere

VERSION SYNC: 1.0.0 BitPhoenix Enterprise Scanner Runner
"""

import asyncio
import codecs
import locale
import sys
import argparse
from pathlib import Path
from typing import Any, Dict, Tuple, Optional

# --- File-wide constants and configuration ---

# Grade thresholds (can be parameterized in future)
GRADE_THRESHOLDS = {
    'A': 90,
    'B': 80,
    'C': 70,
    'D': 60,
    # 'F': < 60
}

# Default output filenames (can be overridden by CLI)
DEFAULT_JSON_OUTPUT = "scan_results.json"
DEFAULT_HTML_OUTPUT = "scan_results.html"
DEFAULT_MD_OUTPUT = "scan_results.md"

# Directories to exclude from scanning
EXCLUDED_DIRS = {
    "venv",           # Python virtual environments (common)
    "env",            # Python virtual environments (alternate)
    ".venv",          # Python virtual environments (hidden)
    "node_modules",   # NodeJS dependencies (large, irrelevant)
    "__pycache__",    # Python bytecode cache
    ".git",           # Git version control (metadata)
    ".pytest_cache",  # pytest test cache
    "build",          # Build artifacts
    "dist",           # Distribution artifacts
    ".tox",           # tox test environments
    "shenron-env",    # Project-specific: custom env
    "unknown",        # Project-specific: legacy or placeholder (documented for audit)
    # TODO(docguru): Move excluded dirs to config file for easier customization
}

# --- Cross-platform encoding handling block ---
# For Windows, sys.stdout and sys.stderr encoding defaults may cause Unicode issues.
# However, direct replacement of sys.stdout/stderr may break output in redirected streams or IDEs.
# We check for the existence of .buffer and only wrap if available and safe.
# TODO(docguru): Consider better detection for redirected streams or IDE output - Medium - 2024-06-12
if sys.platform == "win32":
    def wrap_stream(stream):
        """
        Wraps a stream with UTF-8 encoding if .buffer exists and encoding is not already utf-8.
        Args:
            stream: sys.stdout or sys.stderr
        Returns:
            Wrapped stream or original stream
        """
        # Check for 'buffer' attribute and encoding
        if hasattr(stream, "buffer") and getattr(stream, "encoding", None) != "utf-8":
            # Only wrap if not already utf-8, and buffer exists
            return codecs.getwriter("utf-8")(stream.buffer, "strict")
        return stream

    # Wrap sys.stdout/stderr only if safe (to avoid breaking redirected output)
    sys.stdout = wrap_stream(sys.stdout)
    sys.stderr = wrap_stream(sys.stderr)

# --- Helper function definitions ---

def configure_scanner() -> 'ScanConfig':
    """
    Configures the scanner with project-specific settings.

    Returns:
        ScanConfig: Configuration object for scanning

    Example:
        >>> config = configure_scanner()
        >>> print(config.project_root)
        PosixPath('.')
    """
    # Import within function to handle encoding issues and circular imports
    from enterprise_scanner import ScanConfig
    # Block comment: Exclude common and project-specific directories to optimize scan.
    # EXCLUDED_DIRS is defined at top of file for clarity and customization.
    config = ScanConfig(
        project_root=Path("."),
        exclude_dirs=EXCLUDED_DIRS,
    )
    return config

def print_issue_details(issues: list, severity_label: str, emoji: str = "") -> None:
    """
    Prints issue details for a given severity.

    Args:
        issues: List of issue objects
        severity_label: Human-readable label for severity
        emoji: Emoji prefix for severity section (optional)

    Returns:
        None

    Example:
        >>> print_issue_details(issues, "Critical", "🚨")
    """
    if not issues:
        return
    print(f"\n{emoji} {severity_label.upper()} ISSUES:")
    print("-" * 50)
    for i, issue in enumerate(issues[:5], 1):
        print(f"\n{i}. [{getattr(issue, 'category', '')}] {getattr(issue, 'file_path', '')}")
        if getattr(issue, "line_number", None):
            print(f"   Line {getattr(issue, 'line_number', '')}: {getattr(issue, 'message', '')}")
        else:
            print(f"   {getattr(issue, 'message', '')}")
        print(f"   💡 Suggestion: {getattr(issue, 'suggestion', '')}")
        if getattr(issue, "code_snippet", None):
            # Show only a preview of code snippet
            snippet = getattr(issue, "code_snippet", "")
            print(f"   Code: {snippet[:80]}...")

def display_summary(results: Any) -> None:
    """
    Displays scan summary, statistics, and grading for the scan results.

    Args:
        results: ScanResults object from scanner.scan_project()

    Returns:
        None

    Raises:
        AttributeError: If expected fields are missing from results

    Example:
        >>> display_summary(results)
        # Prints summary to stdout
    """
    # Import SeverityLevel for issue breakdown
    from enterprise_scanner import SeverityLevel
    print("🚀 Starting BitPhoenix Enterprise Code Quality Scan...")
    print("=" * 60)

    print("\n" + "=" * 60)
    print("📊 SCAN RESULTS")
    print("=" * 60)

    # Summary statistics
    print(f"\n✨ Quality Score: {results.score:.1f}/100")
    print(f"⏱️  Scan Duration: {results.duration:.2f} seconds")
    print(f"📁 Files Scanned: {results.metrics.get('total_files_scanned', 0)}")
    print(f"🔍 Total Issues: {results.metrics.get('total_issues', 0)}")

    # Issue breakdown
    print("\n📋 Issues by Severity:")
    print(f"  🔴 Critical: {results.metrics.get('critical_issues', 0)}")
    print(f"  🟠 High: {results.metrics.get('high_issues', 0)}")
    print(f"  🟡 Medium: {results.metrics.get('medium_issues', 0)}")
    print(f"  🟢 Low: {results.metrics.get('low_issues', 0)}")
    print(f"  🔵 Info: {results.metrics.get('info_issues', 0)}")

    # Grade assignment
    score = results.score
    if score >= GRADE_THRESHOLDS['A']:
        grade = "A"
        grade_emoji = "🏆"
    elif score >= GRADE_THRESHOLDS['B']:
        grade = "B"
        grade_emoji = "✅"
    elif score >= GRADE_THRESHOLDS['C']:
        grade = "C"
        grade_emoji = "⚠️"
    elif score >= GRADE_THRESHOLDS['D']:
        grade = "D"
        grade_emoji = "⚠️"
    else:
        grade = "F"
        grade_emoji = "❌"

    print(f"\n📈 Overall Grade: {grade_emoji} {grade}")

    # Top critical issues (display up to 5)
    critical_issues = [
        i for i in results.issues if getattr(i, "severity", None) == SeverityLevel.CRITICAL
    ]
    print_issue_details(critical_issues, "Critical", "🚨")

    # High priority issues (display up to 5)
    high_issues = [
        i for i in results.issues if getattr(i, "severity", None) == SeverityLevel.HIGH
    ]
    print_issue_details(high_issues, "High Priority", "⚠️")

    # Issues by category
    if results.metrics.get("issues_by_category"):
        print("\n📊 Issues by Category:")
        print("-" * 30)
        for category, count in sorted(
            results.metrics["issues_by_category"].items(),
            key=lambda x: x[1],
            reverse=True,
        ):
            bar = "█" * min(count, 50)
            print(f"  {category:20} {count:3} {bar}")

    # Recommendations based on score
    print("\n💡 RECOMMENDATIONS:")
    print("=" * 60)

    if score >= GRADE_THRESHOLDS['A']:
        print("✨ Excellent code quality! Keep up the great work!")
        print("   Consider:")
        print("   • Setting up automated quality gates in CI/CD")
        print("   • Sharing best practices with the team")
        print("   • Contributing to open source with this quality")
    elif score >= GRADE_THRESHOLDS['B']:
        print("✅ Good code quality with room for improvement.")
        print("   Focus on:")
        print("   • Addressing critical and high-priority issues")
        print("   • Improving test coverage")
        print("   • Enhancing documentation")
    elif score >= GRADE_THRESHOLDS['C']:
        print("⚠️  Code quality needs attention.")
        print("   Priority actions:")
        print("   • Fix all critical issues immediately")
        print("   • Establish code review process")
        print("   • Implement automated testing")
        print("   • Add comprehensive documentation")
    else:
        print("❌ Code quality is below standards.")
        print("   Immediate actions required:")
        print("   • Stop new feature development")
        print("   • Focus on fixing critical issues")
        print("   • Implement strict code review")
        print("   • Set up linting and formatting tools")
        print("   • Establish coding standards")

def export_reports(
    results: Any,
    json_output: str = DEFAULT_JSON_OUTPUT,
    html_output: str = DEFAULT_HTML_OUTPUT,
    md_output: str = DEFAULT_MD_OUTPUT
) -> None:
    """
    Exports scan results to JSON, HTML, and Markdown files.
    Ensures all objects are serializable for robust report generation.

    Args:
        results: ScanResults object with scan outcome
        json_output: Path to JSON report file
        html_output: Path to HTML report file
        md_output: Path to Markdown report file

    Returns:
        None

    Raises:
        OSError: If file writing fails
        TypeError: If serialization fails

    Example:
        >>> export_reports(results, "out.json", "out.html", "out.md")
        # Outputs files: out.json, out.html, out.md
    """
    # --- Block comment: Export logic and rationale ---
    # 1. Serialize results and issues defensively to avoid non-primitive types
    # 2. Use custom encoder for robustness, ensuring no unsafe serialization
    # 3. Use configurable output filenames (parameterizable via CLI/config)
    # 4. Add error handling and audit trail for export operations
    # 5. SECURITY: If scan_results.json is loaded elsewhere, validate and sanitize input
    #    (No unsafe deserialization in this script, but flag for future scripts.)

    import json
    from enterprise_scanner import ReportGenerator

    print("\n📤 Export Options:")
    print("=" * 60)
    print(f"   • JSON report: {json_output}")
    print(f"   • HTML report: {html_output}")
    print(f"   • Markdown report: {md_output}")

    # --- Custom encoder to ensure all objects are serializable ---
    class ScannerResultEncoder(json.JSONEncoder):
        """
        Custom JSON encoder for scan results, serializing custom classes to dict.
        """
        def default(self, obj):
            # Serialize SeverityLevel, Path, and custom Issue objects
            if hasattr(obj, "to_dict"):
                return obj.to_dict()
            if hasattr(obj, "value"):
                return obj.value
            if isinstance(obj, Path):
                return str(obj)
            return super().default(obj)

    # Serialize issues to dict, ensuring all fields are primitive types
    issues_serialized = []
    for issue in results.issues:
        issue_dict = {
            "severity": getattr(issue.severity, "value", str(getattr(issue, "severity", ""))),
            "category": getattr(issue, "category", ""),
            "file_path": getattr(issue, "file_path", ""),
            "line_number": getattr(issue, "line_number", None),
            "message": getattr(issue, "message", ""),
            "suggestion": getattr(issue, "suggestion", ""),
            "code_snippet": getattr(issue, "code_snippet", ""),
        }
        issues_serialized.append(issue_dict)

    # Save JSON report with robust serialization
    try:
        with open(json_output, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "score": results.score,
                    "duration": results.duration,
                    "metrics": results.metrics,
                    "issues": issues_serialized,
                },
                f,
                indent=2,
                ensure_ascii=False,  # Ensures UTF-8 output for non-ASCII characters
                cls=ScannerResultEncoder,
            )
        print(f"\n✅ Results saved to {json_output}")
    except Exception as e:
        print(f"❌ Failed to write JSON report ({json_output}): {e}")
        raise

    # Save HTML report (use instance if required)
    try:
        # Confirm ReportGenerator API: use instance if not static
        if hasattr(ReportGenerator, "generate_html") and callable(getattr(ReportGenerator, "generate_html")):
            html_report = ReportGenerator.generate_html(results)
        else:
            rg = ReportGenerator()
            html_report = rg.generate_html(results)
        with open(html_output, "w", encoding="utf-8") as f:
            f.write(html_report)
        print(f"\n✅ Results saved to {html_output}")
    except Exception as e:
        print(f"❌ Failed to write HTML report ({html_output}): {e}")
        raise

    # Save Markdown report (use instance if required)
    try:
        if hasattr(ReportGenerator, "generate_markdown") and callable(getattr(ReportGenerator, "generate_markdown")):
            markdown_report = ReportGenerator.generate_markdown(results)
        else:
            rg = ReportGenerator()
            markdown_report = rg.generate_markdown(results)
        with open(md_output, "w", encoding="utf-8") as f:
            f.write(markdown_report)
        print(f"\n✅ Results saved to {md_output}")
    except Exception as e:
        print(f"❌ Failed to write Markdown report ({md_output}): {e}")
        raise

def grade_results(results: Any) -> Tuple[str, int]:
    """
    Determines grade and exit code based on scan results score.

    Args:
        results: ScanResults object

    Returns:
        Tuple[str, int]: (grade (A-F), exit_code (0 for success, 1 for error))

    Example:
        >>> grade, exit_code = grade_results(results)
        >>> print(grade, exit_code)
        'B', 0
    """
    score = results.score
    if score < GRADE_THRESHOLDS['C']:
        print("\n⚠️  Exiting with error code 1 due to low quality score")
        return "F", 1
    else:
        print("\n✅ Scan completed successfully")
        return "PASS", 0

def parse_args() -> argparse.Namespace:
    """
    Parses command-line arguments for output filenames and configuration.

    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="BitPhoenix Enterprise Scanner Runner v1.0.0"
    )
    parser.add_argument("--json-output", type=str, default=DEFAULT_JSON_OUTPUT,
                        help="Path to JSON output file (default: scan_results.json)")
    parser.add_argument("--html-output", type=str, default=DEFAULT_HTML_OUTPUT,
                        help="Path to HTML output file (default: scan_results.html)")
    parser.add_argument("--md-output", type=str, default=DEFAULT_MD_OUTPUT,
                        help="Path to Markdown output file (default: scan_results.md)")
    # TODO