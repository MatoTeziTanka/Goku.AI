# Goku.AI

> AI-powered development framework and knowledge base for DragonBall Z-themed AI operations.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Security](https://img.shields.io/badge/Security-Active%20Blocking-green.svg)](V2.7.0_SECURITY_IMPROVEMENTS_SUMMARY.md)

## 📖 Description

Goku.AI is a comprehensive repository containing AI operational frameworks, Master Prompt documentation, and development tools. This repository serves as the central knowledge base for AI-assisted development workflows, including VM management, LLM operations, and security best practices.

**Key Features:**
- **Master Prompt Framework**: Comprehensive AI operational guidelines (v2.7.0+)
- **Security-First Design**: Active blocking mechanisms for credential protection
- **VM Integration**: Support for local VM operations (VM100, VM101)
- **LLM Operations**: Context management, state persistence, and tool execution
- **GitHub Standards**: Full compliance with repository management standards

## 🚀 Installation

This repository contains documentation and framework files. No installation required.

```bash
# Clone the repository
git clone https://github.com/MatoTeziTanka/Goku.AI.git
cd Goku.AI
```

## 📚 Usage

### Master Prompt

The Master Prompt framework is located in:
- `root/MASTER-PROMPT-PERPETUAL-SELF-UPDATING-AI-MIND-IMPROVED-v2.7.0.md`

### Credentials Management

**⚠️ IMPORTANT**: Sensitive credentials are stored in `credentials.json` which is **gitignored**.

- **For local development**: Use `credentials.json` (see `CREDENTIALS_README.md`)
- **For production**: Use environment variables or secure vault
- **Template**: See `credentials.template.json` for structure

### Security Standards

This repository follows strict security standards (v2.7.0+):
- ✅ Pre-flight sanitization checks
- ✅ Active blocking mechanisms for credential protection
- ✅ Repository visibility awareness
- ✅ Context monitoring for accidental leaks

See `V2.7.0_SECURITY_IMPROVEMENTS_SUMMARY.md` for details.

## 📁 Repository Structure

```
Goku.AI/
├── root/                    # Core framework files
│   └── MASTER-PROMPT-*.md  # Master Prompt versions
├── docs/                    # Documentation
├── scripts/                 # Automation scripts
├── End of Life/            # Archived sections
├── credentials.json        # 🔒 Gitignored - Sensitive credentials
├── credentials.template.json # ✅ Safe template
├── CREDENTIALS_README.md    # Credentials documentation
└── README.md               # This file
```

## 🔒 Security

⚠️ **IMPORTANT**: This repository does NOT contain:
- ❌ Real credentials (stored in gitignored `credentials.json`)
- ❌ API keys (use environment variables)
- ❌ Passwords (use secure storage)
- ❌ Private keys (use SSH key management)
- ❌ Internal IP addresses (use `credentials.json`)

All sensitive information uses:
- ✅ Placeholders in code (e.g., `<PLACEHOLDER_NAME>`)
- ✅ References to `credentials.json` (gitignored)
- ✅ Environment variables for production
- ✅ Secure vault for sensitive data

## 📋 Quality Standards

This repository adheres to **Master Prompt v2.7.0** quality standards:
- ✅ Active security blocking mechanisms
- ✅ Pre-flight sanitization
- ✅ Repository visibility checks
- ✅ Context monitoring
- ✅ Comprehensive documentation

See `V2.7.0_SECURITY_IMPROVEMENTS_SUMMARY.md` for full QC requirements.

## 📄 License

Apache License 2.0 - See [LICENSE](LICENSE) file for details.

## 🤝 Contributing

This is a personal repository. Contributions are not currently accepted.

## 📊 Status

✅ **Production Ready** - v2.7.0 with active security blocking

## 🔗 Links

- **GitHub**: https://github.com/MatoTeziTanka/Goku.AI
- **Master Prompt v2.7.0**: See `root/` directory
- **Security Standards**: See `V2.7.0_SECURITY_IMPROVEMENTS_SUMMARY.md`
- **Credentials Guide**: See `CREDENTIALS_README.md`

---

**Last Updated:** 2025-11-27  
**Version:** 2.7.0  
**Framework:** Master Prompt v2.7.0 with Active Security Blocking
