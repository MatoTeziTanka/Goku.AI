#!/usr/bin/env python3
"""
Goku.AI Structure Enforcer (v2.9.0 Compliance)
Creates the mandatory directory tree and configuration files.
Ref: Master Prompt Section 18.10 (Visual Tree)
"""

import os
from pathlib import Path

# 1. Define the Perfect v2.9.0 Structure
REQUIRED_DIRS = [
    ".github/ISSUE_TEMPLATE",
    ".vscode",
    "config",
    "docs/architecture",
    "scripts/windows",
    "scripts/linux",
    "src/api",
    "src/services",
    "src/utils",
    "tests/unit",
    "tests/integration",
]

REQUIRED_FILES = {
    ".gitignore": """# v2.9.0 STANDARD GITIGNORE
.env
.env.*
!.env.example
*.pem
*.key
credentials.json
secrets.yaml
__pycache__/
*.pyc
.pytest_cache/
.coverage
dist/
build/
.vscode/
! .vscode/settings.json
! .vscode/extensions.json
""",
    "README.md": """# 🚀 Goku.AI

> **Autonomous AI Agent Framework**

## 📝 Overview

Goku.AI is an autonomous AI agent framework built on Master Prompt v2.9.0 engineering standards.

## 🏗️ Architecture

- **Framework:** Master Prompt v2.9.0
- **Language:** Python 3.10+
- **Structure:** Enterprise-grade modular architecture

## 🚀 Getting Started

See `scripts/windows/install.bat` or `scripts/linux/install.sh`

## 📋 Prerequisites

- Python 3.10+
- Git

## 🔧 Installation

### Windows
```bash
scripts\\windows\\install.bat
```

### Linux
```bash
scripts/linux/install.sh
```

## 📖 Usage

[Add usage instructions]

## 🤝 Contributing

See `CONTRIBUTING.md`

## 📄 License

See `LICENSE`
""",
    "CONTRIBUTING.md": """# Contributing Guide

All PRs must reference a GitHub Issue.

## Commit Format

Use Conventional Commits: `<type>(<scope>): <description> (Ref #<issue-id>)`

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `chore`
""",
    "CHANGELOG.md": """# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- Initial repository structure aligned with v2.9.0 standards
""",
    "LICENSE": """MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""",
    ".secrets.baseline": "{}",  # Placeholder for detect-secrets
    ".vscode/settings.json": """{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  },
  "python.defaultInterpreterPath": "python",
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true
  }
}
""",
    ".vscode/extensions.json": """{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "ms-python.black-formatter",
    "charliermarsh.ruff"
  ]
}
""",
    ".editorconfig": """root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true

[*.py]
indent_style = space
indent_size = 4

[*.{json,yml,yaml}]
indent_style = space
indent_size = 2

[*.md]
trim_trailing_whitespace = false
"""
}

def main():
    root = Path.cwd()
    print("=" * 70)
    print("GOKU.AI STRUCTURE ENFORCER (v2.9.0 Compliance)".center(70))
    print("=" * 70)
    print()
    print(f"🏗️  Aligning {root.name} to v2.9.0 Standards...")
    print()

    # 2. Create Directories
    print("📁 Creating directory structure...")
    for d in REQUIRED_DIRS:
        target = root / d
        if not target.exists():
            target.mkdir(parents=True, exist_ok=True)
            print(f"  ✅ Created: {d}/")
        else:
            print(f"  🆗 Exists:  {d}/")
    print()

    # 3. Create/Update Config Files
    print("📝 Creating configuration files...")
    for filename, content in REQUIRED_FILES.items():
        target = root / filename
        if not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding='utf-8')
            print(f"  ✅ Created: {filename}")
        else:
            print(f"  ⚠️  Skipped: {filename} (already exists)")
    print()

    # 4. Create Placeholder Install Scripts (Section 18.12)
    print("🔧 Creating installation scripts...")
    
    win_install = root / "scripts/windows/install.bat"
    if not win_install.exists():
        win_install.write_text(
            "@echo off\n"
            "echo ========================================\n"
            "echo   Goku.AI Installation (Windows)\n"
            "echo ========================================\n"
            "echo.\n"
            "echo Installing Python dependencies...\n"
            "pip install -r ..\\..\\requirements.txt\n"
            "echo.\n"
            "echo ✅ Installation complete!\n"
            "pause\n",
            encoding='utf-8'
        )
        print("  ✅ Created: scripts/windows/install.bat")
    else:
        print("  🆗 Exists:  scripts/windows/install.bat")
    
    win_uninstall = root / "scripts/windows/uninstall.bat"
    if not win_uninstall.exists():
        win_uninstall.write_text(
            "@echo off\n"
            "echo ========================================\n"
            "echo   Goku.AI Uninstallation (Windows)\n"
            "echo ========================================\n"
            "echo.\n"
            "set /p confirm=\"Are you sure? (yes/no): \"\n"
            "if /i not \"%confirm%\"==\"yes\" (\n"
            "    echo Uninstallation cancelled.\n"
            "    pause\n"
            "    exit /b\n"
            ")\n"
            "echo Uninstalling...\n"
            "pip uninstall -r ..\\..\\requirements.txt -y\n"
            "echo.\n"
            "echo ✅ Uninstallation complete!\n"
            "pause\n",
            encoding='utf-8'
        )
        print("  ✅ Created: scripts/windows/uninstall.bat")
    else:
        print("  🆗 Exists:  scripts/windows/uninstall.bat")
    
    linux_install = root / "scripts/linux/install.sh"
    if not linux_install.exists():
        linux_install.write_text(
            "#!/bin/bash\n"
            "echo \"========================================\"\n"
            "echo \"  Goku.AI Installation (Linux)\"\n"
            "echo \"========================================\"\n"
            "echo\n"
            "echo \"Installing Python dependencies...\"\n"
            "pip install -r ../../requirements.txt\n"
            "echo\n"
            "echo \"✅ Installation complete!\"\n",
            encoding='utf-8'
        )
        os.chmod(linux_install, 0o755)
        print("  ✅ Created: scripts/linux/install.sh")
    else:
        print("  🆗 Exists:  scripts/linux/install.sh")
    
    linux_uninstall = root / "scripts/linux/uninstall.sh"
    if not linux_uninstall.exists():
        linux_uninstall.write_text(
            "#!/bin/bash\n"
            "echo \"========================================\"\n"
            "echo \"  Goku.AI Uninstallation (Linux)\"\n"
            "echo \"========================================\"\n"
            "echo\n"
            "read -p \"Are you sure? (yes/no): \" confirm\n"
            "if [ \"$confirm\" != \"yes\" ]; then\n"
            "    echo \"Uninstallation cancelled.\"\n"
            "    exit 1\n"
            "fi\n"
            "echo \"Uninstalling...\"\n"
            "pip uninstall -r ../../requirements.txt -y\n"
            "echo\n"
            "echo \"✅ Uninstallation complete!\"\n",
            encoding='utf-8'
        )
        os.chmod(linux_uninstall, 0o755)
        print("  ✅ Created: scripts/linux/uninstall.sh")
    else:
        print("  🆗 Exists:  scripts/linux/uninstall.sh")
    
    print()
    print("=" * 70)
    print("✅ STRUCTURE ALIGNMENT COMPLETE".center(70))
    print("=" * 70)
    print()
    print("📋 Next Steps:")
    print("   1. Review the created structure")
    print("   2. Move your source code into 'src/'")
    print("   3. Move documentation into 'docs/'")
    print("   4. Move scripts into 'scripts/'")
    print("   5. Delete files that don't belong")
    print()

if __name__ == "__main__":
    main()

