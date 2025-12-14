# 🚀 Quick Start (5 minutes)

## Option 1: Run Locally (Recommended for Development)

### Step 1: Clone & Setup

```bash
# Clone
git clone https://github.com/pv-udpv/opendirect21-adcom.git
cd opendirect21-adcom

# Setup venv
python3.12 -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Run Server

```bash
python -m opendirect21.main
# or
uvicorn opendirect21.main:app --reload
```

### Step 3: Access API

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## Option 2: Docker (Recommended for Production)

```bash
# Build and run
docker-compose up

# Access at http://localhost:8000/docs
```

---

## First API Calls

### Health Check

```bash
curl http://localhost:8000/health
```

### Create Organization

```bash
curl -X POST http://localhost:8000/api/v1/organizations \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Publisher",
    "type": "Publisher"
  }'
```

### List Organizations

```bash
curl http://localhost:8000/api/v1/organizations
```

---

## Run Tests

```bash
# All tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=opendirect21

# Parser tests
python -m tools.spec_parser.smoke_test
```

---

## Generate Models from Specs

```bash
# Copy spec files
cp OpenDirect.v2.1.final.md tools/spec_parser/
cp AdCOM_v1.0_FINAL.md tools/spec_parser/

# Generate
python -m tools.spec_parser.gen_models
python -m tools.spec_parser.gen_routes
python -m tools.spec_parser.smoke_test

# Restart server
python -m opendirect21.main
```

---

## Project Structure

```
opendirect21-adcom/
├── opendirect21/          # Main application
│   ├── main.py            # FastAPI app
│   ├── config.py          # Settings
│   ├── store.py           # Data store
│   ├── models/            # Data models
│   │   ├── base.py        # Base classes
│   │   └── generated/     # Auto-generated models
│   └── api/               # API routes
│       ├── health.py      # Health endpoints
│       └── generated/     # Auto-generated routes
├── tools/                 # Code generation
│   └── spec_parser/       # Parser & generators
├── tests/                 # Test suite
├── docs/                  # Documentation
├── README.md              # Full guide
├── requirements.txt       # Dependencies
├── docker-compose.yml     # Docker setup
└── Dockerfile             # Container definition
```

---

## Key Files

| File | Purpose |
|------|----------|
| [README.md](README.md) | Full documentation |
| [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md) | Detailed setup guide |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | System design |
| [docs/SETUP_INSTRUCTIONS.md](docs/SETUP_INSTRUCTIONS.md) | Production deployment |
| [.copilot-instructions.md](.copilot-instructions.md) | Development tasks |

---

## Common Commands

```bash
# Development
python -m opendirect21.main              # Start server (with reload)
uvicorn opendirect21.main:app --reload   # Alternative startup

# Testing
pytest tests/ -v                         # Run all tests
pytest tests/test_health.py -v           # Single test file
pytest tests/ --cov=opendirect21         # With coverage

# Code Quality
black opendirect21 tools tests           # Format code
ruff check opendirect21 tools tests      # Lint
mypy opendirect21                        # Type check

# Generation
python -m tools.spec_parser.gen_models   # Generate models
python -m tools.spec_parser.gen_routes   # Generate routes
python -m tools.spec_parser.smoke_test   # Verify parsers

# Docker
docker-compose up                        # Start with docker
docker-compose down                      # Stop
docker logs -f opendirect21-api          # View logs
```

---

## Troubleshooting

**Q: Port 8000 already in use**
```bash
uvicorn opendirect21.main:app --port 8001
```

**Q: ModuleNotFoundError**
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

**Q: Dependencies not installing**
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

**Q: Python version issue**
```bash
python3.12 -m venv venv
# or use pyenv for version management
```

---

## Next Steps

1. ✅ Server is running - check http://localhost:8000/docs
2. 📚 Read [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md) for full setup
3. 🧪 Run tests: `pytest tests/ -v`
4. 📊 Generate models from spec files (see "Generate Models" above)
5. 🚀 Deploy with [docs/SETUP_INSTRUCTIONS.md](docs/SETUP_INSTRUCTIONS.md)

---

## Need Help?

- **API Docs**: http://localhost:8000/docs (when running)
- **Issues**: https://github.com/pv-udpv/opendirect21-adcom/issues
- **Documentation**: See [README.md](README.md) and [docs/](docs/)
- **Specifications**:
  - [OpenDirect 2.1](https://iabtechlab.com/opendirect-2-1/)
  - [Adcom v1.0](https://iabtechlab.com/adcom/)

---

**Made with ❤️ for programmatic media trading**
