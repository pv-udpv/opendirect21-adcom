# OpenDirect 2.1 + Adcom v1.0 FastAPI Server

Fully automated REST API server for programmatic media trading with auto-generated Pydantic models and FastAPI routes from IAB specifications.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python: 3.12+](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com)

## 🚀 Quick Start (5 minutes)

### Prerequisites
- Python 3.12 or higher
- pip or uv package manager

### Installation

```bash
# Clone repository
git clone https://github.com/pv-udpv/opendirect21-adcom.git
cd opendirect21-adcom

# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt
# OR with uv (faster):
uv sync
```

### Run Server

```bash
# Development mode
python -m opendirect21.main

# OR with uvicorn directly
uvicorn opendirect21.main:app --reload --host 0.0.0.0 --port 8000
```

### Access API

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json
- **Health Check**: http://localhost:8000/health

## 📋 Project Structure

```
opendirect21-adcom/
├── opendirect21/                   # Main application
│   ├── __init__.py
│   ├── main.py                    # FastAPI app entry point
│   ├── config.py                  # Settings & configuration
│   ├── store.py                   # In-memory data store
│   ├── models/                    # Data models
│   │   ├── __init__.py
│   │   ├── base.py               # Base model classes
│   │   ├── generated/            # Auto-generated from specs
│   │   │   ├── opendirect.py    # OpenDirect 2.1 models
│   │   │   └── adcom.py         # Adcom v1.0 models
│   │   └── custom/              # Custom validators
│   └── api/                       # API endpoints
│       ├── __init__.py
│       ├── health.py             # Health check endpoints
│       └── generated/            # Auto-generated routers
│           └── opendirect_routes.py
│
├── tools/                          # Code generation & parsing
│   ├── spec_parser/
│   │   ├── __init__.py
│   │   ├── md_tables.py          # Markdown table parser
│   │   ├── gen_models.py         # Pydantic model generator
│   │   ├── gen_routes.py         # FastAPI router generator
│   │   └── smoke_test.py         # Parser verification
│   └── scripts/
│       └── generate.sh           # Run all generators
│
├── tests/                          # Test suite
│   ├── __init__.py
│   ├── test_health.py
│   ├── test_api.py
│   └── conftest.py
│
├── pyproject.toml                 # Project metadata (PEP 517)
├── requirements.txt               # pip dependencies
├── .env.example                   # Environment variables template
├── .gitignore                     # Git ignore rules
└── README.md                      # This file
```

## 🎯 Features

### ✅ OpenDirect 2.1 Support
- [x] Automatic parsing of IAB specification
- [x] 20+ core objects (Organization, Account, Order, Line, Creative, etc.)
- [x] Full CRUD endpoints (GET, POST, PUT, DELETE)
- [x] Nested resources (Orders/Lines, Accounts/Creatives)
- [x] Automatic Swagger/ReDoc documentation
- [x] Type validation with Pydantic v2

### ✅ Adcom v1.0 Support  
- [ ] Automatic parsing of Adcom specification
- [ ] 15+ media objects (Ad, Display, Banner, Video, Audio, Native)
- [ ] Asset objects (LinkAsset, ImageAsset, VideoAsset, etc.)
- [ ] Context objects (Publisher, Content, User, Device, Geo)
- [ ] Enum definitions (API Frameworks, Creative Subtypes, etc.)
- [ ] Integration with OpenDirect models

### ✅ Developer Experience
- [x] Hot reload development mode
- [x] Automatic API documentation (Swagger UI + ReDoc)
- [x] Type hints (100% coverage)
- [x] Pydantic validation
- [x] In-memory data store (replace with PostgreSQL/MongoDB easily)
- [x] Python 3.12+ async/await throughout
- [x] Code generation from specs (zero duplication)

## 🔌 API Examples

### Create Organization

```bash
curl -X POST http://localhost:8000/api/v1/organizations \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Acme Publishing",
    "type": "Publisher",
    "contacts": []
  }'
```

### List Organizations

```bash
curl http://localhost:8000/api/v1/organizations
```

### Create Account

```bash
curl -X POST http://localhost:8000/api/v1/accounts \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Q1 2025 Campaign",
    "advertiser_id": "org-123",
    "buyer_id": "buyer-456"
  }'
```

## 🔧 Configuration

Copy `.env.example` to `.env` and customize:

```bash
cp .env.example .env
```

**Key settings**:
- `SERVER_HOST` — Bind address (default: 0.0.0.0)
- `SERVER_PORT` — Port number (default: 8000)
- `LOG_LEVEL` — Logging level (default: INFO)
- `CORS_ORIGINS` — Allowed CORS origins

## 📊 Database Setup

### Development (In-Memory)
No setup needed — uses `InMemoryStore` by default.

### Production (PostgreSQL)

```bash
# Install async driver
pip install asyncpg sqlalchemy

# Update config.py
DATABASE_URL=postgresql+asyncpg://user:password@localhost/opendirect21

# Run migrations
alembic upgrade head
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=opendirect21 --cov-report=html

# Run specific test
pytest tests/test_api.py::test_create_organization -v

# Run parser tests
python -m tools.spec_parser.smoke_test
```

## 📚 Documentation

- **[TECHNICAL_SPECIFICATION.md](docs/TECHNICAL_SPECIFICATION.md)** — Complete technical requirements
- **[SETUP_INSTRUCTIONS.md](docs/SETUP_INSTRUCTIONS.md)** — Production deployment
- **[API_GUIDE.md](docs/API_GUIDE.md)** — API usage examples
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** — System design & data models

## 🚀 Deployment

### Docker

```bash
# Build image
docker build -t opendirect21-adcom .

# Run container
docker run -p 8000:8000 opendirect21-adcom
```

### Docker Compose

```bash
docker-compose up -d
```

### Systemd Service

See [SETUP_INSTRUCTIONS.md](docs/SETUP_INSTRUCTIONS.md) for systemd configuration.

## 📦 Auto-Generation

Generate models and routes from specifications:

```bash
# Place spec files in tools/spec_parser/
cp OpenDirect.v2.1.final.md tools/spec_parser/
cp AdCOM\ v1.0\ FINAL.md tools/spec_parser/

# Generate all
python -m tools.spec_parser.gen_models
python -m tools.spec_parser.gen_routes
python -m tools.spec_parser.smoke_test
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  FastAPI Application                         │
│                  (opendirect21/main.py)                      │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
   ┌────▼────┐  ┌────▼────┐  ┌────▼────┐
   │ Health  │  │ OpenDir │  │ Adcom   │
   │ Checks  │  │ Routes  │  │ Routes  │
   └────┬────┘  └────┬────┘  └────┬────┘
        │              │           │
        └──────────────┼───────────┘
                       │
            ┌──────────▼──────────┐
            │  Pydantic Models   │
            │  (auto-generated)  │
            └──────────┬──────────┘
                       │
            ┌──────────▼──────────┐
            │  Data Store (InMemory/DB) │
            └────────────────────┘
```

## 📈 Roadmap

- [x] Project structure
- [x] Health check endpoints
- [ ] OpenDirect 2.1 parser & models
- [ ] OpenDirect 2.1 CRUD endpoints
- [ ] Adcom v1.0 parser & models
- [ ] Adcom v1.0 endpoints
- [ ] PostgreSQL integration
- [ ] Authentication (OAuth2)
- [ ] Rate limiting
- [ ] caching
- [ ] Comprehensive tests (100% coverage)
- [ ] Production deployment guide

## 🤝 Contributing

Contributions welcome! Please:

1. Fork repository
2. Create feature branch (`git checkout -b feature/amazing-thing`)
3. Commit changes (`git commit -m 'Add amazing thing'`)
4. Push to branch (`git push origin feature/amazing-thing`)
5. Open Pull Request

## 📄 License

MIT License — see [LICENSE](LICENSE) file

## 🔗 References

### IAB Specifications
- [OpenDirect 2.1](https://iabtechlab.com/opendirect-2-1/) — Programmatic Guaranteed Trading
- [Adcom v1.0](https://iabtechlab.com/adcom/) — Common Data Model
- [OpenDirect GitHub](https://github.com/InteractiveAdvertisingBureau/OpenDirect)
- [Adcom GitHub](https://github.com/InteractiveAdvertisingBureau/AdCOM)

### Technologies
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Pydantic v2](https://docs.pydantic.dev)
- [Python Async](https://docs.python.org/3/library/asyncio.html)

## 👤 Author

**AdTech Architect**
- GitHub: [@pv-udpv](https://github.com/pv-udpv)
- Email: pv@udpv.org

## 🙏 Acknowledgments

- [IAB Tech Lab](https://iabtechlab.com) — For OpenDirect & Adcom specifications
- [FastAPI](https://fastapi.tiangolo.com) — For amazing framework
- [Pydantic](https://pydantic-ai.jina.ai/) — For data validation

---

**Made with ❤️ for programmatic media trading**
