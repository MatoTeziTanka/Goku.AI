# BitPhoenix Repository Information

## 📌 Project Overview

**BitPhoenix** is an enterprise-grade data recovery platform with GPU acceleration and cryptocurrency wallet recovery support. It provides both a user-friendly interface for everyday users and advanced forensic tools for technical professionals.

**Version**: 1.0.0  
**License**: Proprietary  
**Status**: Production-ready

## 🏗️ Repository Structure

```
BitPhoenix/
├── backend/                          # Python FastAPI backend
│   ├── src/                          # Main application code
│   │   ├── main.py                   # FastAPI application entry point
│   │   ├── models.py                 # Pydantic data models
│   │   ├── config.py                 # Configuration management
│   │   ├── device_manager.py         # Storage device detection & management
│   │   ├── scanner.py                # File scanning logic
│   │   ├── file_carving.py           # File signature detection
│   │   ├── signature_library.py      # File format signatures database
│   │   ├── recovery_engine.py        # Core recovery algorithms
│   │   ├── crypto_recovery.py        # Bitcoin/Ethereum wallet recovery
│   │   ├── gpu_acceleration.py       # GPU-accelerated scanning
│   │   ├── file_preview.py           # File preview generation
│   │   ├── file_format_database.py   # File format metadata
│   │   ├── debugger.py               # Debug utilities
│   │   └── __init__.py               # Package initialization
│   ├── shenron/                      # Multi-agent system modules
│   ├── recovered/                    # Recovery output directory
│   ├── requirements.txt              # Python dependencies
│   ├── ENV_CONFIGURATION.md          # Environment setup docs
│   ├── QUICK_START_AI.md             # AI services quick start
│   ├── setup_ai_services.sh          # AI services setup script
│   └── test_api.py                   # API testing utilities
│
├── frontend/                         # React TypeScript frontend
│   ├── src/                          # React source code
│   ├── public/                       # Static assets
│   ├── package.json                  # Node.js dependencies
│   └── tsconfig.json                 # TypeScript configuration
│
├── cursor-extension/                 # VS Code/Cursor extension
│   ├── src/                          # Extension source code
│   ├── package.json                  # Extension manifest
│   └── README.md                     # Extension documentation
│
├── docs/                             # Project documentation
│   ├── technical-docs/               # Architecture & technical guides
│   ├── getting-started/              # Setup & onboarding guides
│   ├── user-guides/                  # User documentation
│   ├── faq/                          # Frequently asked questions
│   └── troubleshooting-guide.md      # Troubleshooting resources
│
├── scripts/                          # Build & deployment scripts
│   ├── linux/                        # Linux installation scripts
│   └── windows/                      # Windows/WSL scripts
│
├── Marketing-Automation/             # Marketing & automation tools
├── shenron-ultra-instinct/           # Advanced agent system phases
├── venv/                             # Python virtual environment
├── shenron-env/                      # Alternative Python environment
│
├── README.md                         # Main project documentation
├── CHANGELOG.md                      # Version history
├── API_DOCUMENTATION.md              # REST API reference
├── DEVELOPMENT_GUIDE.md              # Developer guidelines
├── CONTRIBUTING.md                   # Contributing guidelines
├── CODE_OF_CONDUCT.md                # Community standards
├── LICENSE                           # Proprietary license
└── repo.md                           # This file
```

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI 0.104.1
- **Server**: Uvicorn
- **Language**: Python 3.8+
- **Async**: aiofiles, aiohttp, websockets
- **Database/Indexing**: ChromaDB (vector database)
- **Security**: cryptography, pycryptodome, python-jose, passlib
- **Rate Limiting**: slowapi
- **Data Processing**: numpy, pandas, Pillow
- **File Analysis**: python-magic
- **System Monitoring**: psutil, pyudev

### Frontend
- **Framework**: React 18+
- **Language**: TypeScript
- **Build Tool**: react-scripts
- **Styling**: styled-components
- **HTTP Client**: axios
- **UI Components**: Lucide React, framer-motion
- **File Upload**: react-dropzone
- **Routing**: react-router-dom

### Cursor Extension
- **Platform**: VS Code / Cursor IDE
- **Language**: TypeScript
- **Build**: tsc (TypeScript compiler)
- **HTTP Client**: axios
- **Engine**: vscode ^1.80.0

### Optional
- **GPU Support**: CUDA/OpenCL (optional)
- **AI Services**: OpenAI, Groq, Anthropic Claude, Google Gemini, DeepSeek, Together AI, Azure AI

## 🎯 Key Backend Modules

### `device_manager.py`
Handles detection and management of storage devices (HDD, SSD, USB, SD cards).

### `scanner.py`
Core scanning logic for traversing storage devices and identifying recoverable files.

### `file_carving.py`
Implements signature-based file detection and carving for deleted file recovery.

### `signature_library.py`
Maintains database of file format signatures (magic bytes) for 1000+ file types.

### `recovery_engine.py`
Orchestrates the recovery process and file reconstruction algorithms.

### `crypto_recovery.py`
Specialized recovery for cryptocurrency wallets (Bitcoin, Ethereum, seed phrases).

### `gpu_acceleration.py`
Optional GPU-accelerated scanning using CUDA/OpenCL for performance improvement.

### `file_format_database.py`
Metadata and format specifications for supported file types.

### `file_preview.py`
Generates previews for recovered files.

### `debugger.py`
Debug utilities, logging, and system analysis tools.

## 🔄 Core Features

### Advanced Recovery
- **1000+ File Formats** - Documents, images, videos, audio, archives, cryptocurrency wallets
- **Signature-Based Detection** - Advanced file carving algorithms
- **Multi-Device Support** - HDD, SSD, NVMe, USB drives, SD cards
- **Real-Time Progress** - WebSocket-based live updates

### Security & Privacy
- **Read-Only Operations** - Never modifies source data
- **Military-Grade Encryption** - Secure data handling
- **Local Processing** - No data sent to external servers
- **Audit Trails** - Comprehensive logging

### Performance
- **GPU Acceleration** - Optional hardware acceleration (3.2x faster)
- **Multi-Threaded Processing** - Optimized for multi-core systems
- **Memory Efficient** - Streaming algorithms for large devices
- **Concurrent Operations** - Handle multiple jobs simultaneously

## 🚀 Quick Start (Development)

### Prerequisites
- Python 3.8+
- Node.js 16+
- 4GB RAM minimum
- Linux (Ubuntu 18.04+) or Windows WSL2

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm start  # Opens http://localhost:3000
```

### API Access
- **Web Interface**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **API Redoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🧪 Testing & Quality

### Running Tests
```bash
cd backend
python -m pytest tests/
```

### API Testing
```bash
python test_api.py
```

### Code Quality
See individual component documentation for linting and type checking commands.

## 📚 Documentation

### Key Documents
- **[API_DOCUMENTATION.md](./API_DOCUMENTATION.md)** - REST API reference
- **[DEVELOPMENT_GUIDE.md](./DEVELOPMENT_GUIDE.md)** - Development workflow
- **[ENTERPRISE_STANDARDS.md](./ENTERPRISE_STANDARDS.md)** - Quality standards
- **[CHANGELOG.md](./CHANGELOG.md)** - Version history
- **[docs/](./docs/)** - Comprehensive documentation directory

### Setup Guides
- **[QUICK_START.md](./QUICK_START.md)** - Basic setup
- **[STEP_BY_STEP_SETUP.md](./STEP_BY_STEP_SETUP.md)** - Detailed setup
- **[WSL_SETUP_GUIDE.md](./WSL_SETUP_GUIDE.md)** - Windows WSL installation
- **[CURSOR_EXTENSION_SETUP.md](./CURSOR_EXTENSION_SETUP.md)** - Extension setup

## 🤝 Contributing

Please refer to [CONTRIBUTING.md](./CONTRIBUTING.md) for detailed contribution guidelines.

### Key Standards
- **Semantic Versioning** - Version format: MAJOR.MINOR.PATCH
- **Code Style** - Follow existing patterns and conventions
- **Testing** - All changes require tests
- **Documentation** - Update relevant docs with changes
- **Code of Conduct** - See [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md)

## 📊 Performance Benchmarks

### Recovery Speed (SSD Test)
- **Quick Scan**: 500GB in 45 seconds
- **Deep Scan**: 500GB in 8 minutes
- **Forensic Scan**: 500GB in 25 minutes

### GPU Acceleration (NVIDIA RTX 3080)
- **Speed Improvement**: 3.2x faster
- **Memory Usage**: +2.1GB RAM
- **Power**: +45W during acceleration

## 🔐 Security & Compliance

- **GDPR Ready** - European data protection compliance
- **CCPA Compliant** - California privacy law
- **SOC 2 Type II** - Enterprise security framework
- **ISO 27001** - Information security management

## 🏆 Enterprise Standards (v2.0.0)

BitPhoenix follows comprehensive enterprise engineering standards documented in **ENTERPRISE_STANDARDS.md**:

### Core Principles
1. **Simplicity Over Complexity** - Explainable code, not over-engineered
2. **Performance is a Feature** - Every millisecond counts
3. **Security by Design** - Not an afterthought, foundation-first
4. **Documentation is Code** - Undocumented code is technical debt
5. **Test Everything** - If untested, it's broken

### Code Quality Standards
- **Naming Conventions**: PascalCase classes, snake_case methods, SCREAMING_SNAKE_CASE constants
- **Error Handling**: Specific, informative exceptions with context and error codes
- **Performance Optimization**: Caching, connection pooling, batch processing, parallel execution
- **API Design**: RESTful + GraphQL, semantic versioning, rate limiting

### Testing & Quality Assurance
- **Unit Test Coverage**: 90% minimum
- **Integration Tests**: All critical paths covered
- **Performance Tests**: All endpoints and algorithms benchmarked
- **Security Tests**: Quarterly penetration testing
- **Benchmark Requirements**: p99 response time < 1 second

### Monitoring & Observability
- **Required Metrics**: Request duration, error rate, active connections, files recovered
- **Structured Logging**: JSON-formatted logs with context and request IDs
- **Performance Tracking**: CPU/memory/GPU utilization, database query times
- **Audit Trails**: All operations logged with user context

### Security Standards
- **Input Validation**: All inputs sanitized and validated
- **Authentication**: OAuth 2.0 / JWT with refresh tokens (24h expiry, 30d refresh)
- **Authorization**: Role-based access control (RBAC)
- **Encryption**: TLS 1.3+ for transit, AES-256 for storage
- **Secrets Management**: HashiCorp Vault or AWS KMS
- **Rate Limiting**: Multiple layers (API gateway, service-level)

### Performance Requirements
- **API Response Time**: p99 < 1 second
- **Database Queries**: All queries < 100ms
- **Memory Usage**: < 4GB for standard operations
- **CPU Usage**: < 80% sustained
- **Startup Time**: < 10 seconds
- **Graceful Shutdown**: < 30 seconds

### Deployment & CI/CD
- **Pipeline Checks**: Code quality, type checking, security scanning
- **Testing Matrix**: Multiple Python versions (3.9, 3.10, 3.11)
- **Container Security**: Docker image vulnerability scanning with Trivy
- **Production Checklist**: 10-point verification before deployment
- **Kubernetes**: Rolling updates with health probes and resource limits
- **Load Testing**: Required before production deployment

### Scalability
- **Horizontal Scaling**: Stateless services with distributed task queues
- **Connection Pooling**: Min 10, max 20 connections with recycling
- **Caching Strategy**: Redis with configurable TTL
- **Auto-scaling**: Worker pool scaling based on queue depth
- **Batch Processing**: Optimized batch sizes for throughput

## 📝 Configuration

### Environment Variables
See [ENV_CONFIGURATION.md](./backend/ENV_CONFIGURATION.md) for complete configuration options.

### AI Services Setup
See [QUICK_START_AI.md](./backend/QUICK_START_AI.md) for AI service integration.

## 🐛 Troubleshooting

For common issues and solutions, refer to:
- **[troubleshooting-guide.md](./docs/troubleshooting-guide.md)**
- **[BITPHOENIX-WSL-TROUBLESHOOTING-GUIDE.md](./docs/BITPHOENIX-WSL-TROUBLESHOOTING-GUIDE.md)**

## 🎯 Enterprise Improvement Action Plan (v1.0.0)

The project follows a comprehensive improvement action plan focused on achieving enterprise-grade quality standards.

### Current State Assessment
- **Current Quality Score**: Baseline establishment in progress
- **Target Quality Score**: 95+/100 (Grade: A)
- **Priority**: CRITICAL

### Major Improvement Areas
1. **Documentation** - Comprehensive API and code documentation
2. **Error Handling** - Standardized exception handling across all modules
3. **Code Complexity** - Refactor complex functions (target: < 10 complexity)
4. **Security** - Address all critical vulnerabilities
5. **Test Coverage** - Achieve 90%+ coverage

### Improvement Goals

**Immediate (Week 1-2)**
- Eliminate all critical security vulnerabilities
- Achieve 60+ quality score
- Implement automated code quality checks
- Establish baseline documentation standards

**Short-term (Month 1)**
- Achieve 80+ quality score
- Complete documentation for all public APIs
- Reduce complexity in high-risk functions
- Implement comprehensive error handling

**Long-term (Quarter 1)**
- Achieve 95+ quality score
- 100% test coverage
- Full API documentation
- Zero security vulnerabilities
- Automated quality gates in CI/CD

### Key Action Items

**🔴 CRITICAL (Week 1)**
- Fix security vulnerabilities in `enterprise_scanner.py`, `device_manager.py`, `file_carving.py`
- Replace unsafe subprocess execution with secure alternatives
- Implement security-focused code review process

**🟠 HIGH PRIORITY (Week 2)**
- Reduce code complexity in high-risk functions
- Implement standardized error handling with custom exceptions
- Add comprehensive error context and logging

**🟡 MEDIUM PRIORITY (Week 3-4)**
- Achieve 90% test coverage with pytest
- Set up CI/CD pipeline with automated quality gates
- Complete documentation standards compliance

### Documentation Standards
All functions must include:
- Clear description of purpose and use cases
- Args: Parameter descriptions with types and constraints
- Returns: Detailed return value descriptions
- Raises: List of exceptions and when they occur
- Examples: Practical usage examples
- Note: Performance implications and limitations
- See Also: Related functionality cross-references

### Error Handling Pattern
```python
@dataclass
class Result:
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None

class RecoveryError(Exception):
    def __init__(self, message: str, code: str, context: dict):
        self.message = message
        self.code = code
        self.context = context
```

### Tools & Configuration
- **Linting**: pylint (target: 8.0+)
- **Formatting**: black, isort
- **Type Checking**: mypy (strict mode)
- **Testing**: pytest with coverage (90%+ target)
- **Security**: bandit, safety
- **Pre-commit Hooks**: Automated checks before commits

### Success Metrics
| Week | Quality Score | Critical Issues | Documentation | Test Coverage |
|------|--------------|-----------------|---------------|---------------|
| 1    | 60+          | 0               | 50%           | 60%           |
| 2    | 75+          | 0               | 75%           | 75%           |
| 3    | 85+          | 0               | 90%           | 85%           |
| 4    | 95+          | 0               | 100%          | 90%           |

### Definition of Done
A task is complete when:
- [ ] Code reviewed by 2+ developers
- [ ] Documentation is complete and accurate
- [ ] Tests passing with 90%+ coverage
- [ ] Security scan shows no vulnerabilities
- [ ] Performance benchmarks met
- [ ] Code quality score ≥ 90
- [ ] Changes deployed to staging
- [ ] Rollback plan documented

## 📞 Support

- **Issues**: GitHub Issues
- **Documentation**: See [docs/](./docs/) directory
- **Email**: support@bitphoenix.io

## 📄 License

Proprietary License - See [LICENSE](./LICENSE) for details.

---

**Last Updated**: November 2025  
**Project Version**: 1.0.0  
**Action Plan Version**: 1.0.0
