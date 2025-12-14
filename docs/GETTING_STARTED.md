# Getting Started Guide

## Installation (5 minutes)

### 1. Clone Repository

```bash
git clone https://github.com/pv-udpv/opendirect21-adcom.git
cd opendirect21-adcom
```

### 2. Create Virtual Environment

```bash
# With venv
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# OR with conda
conda create -n opendirect21 python=3.12
conda activate opendirect21

# OR with uv (fastest)
uv venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
# With pip
pip install -r requirements.txt

# OR with uv
uv sync

# OR with poetry
pip install poetry
poetry install
```

### 4. Configure Environment

```bash
cp .env.example .env
# Edit .env if needed
```

## Running the Server

### Development Mode (with auto-reload)

```bash
# Method 1: Direct Python
python -m opendirect21.main

# Method 2: Uvicorn (recommended)
uvicorn opendirect21.main:app --reload --host 0.0.0.0 --port 8000

# Method 3: Docker
docker-compose up
```

### Production Mode

```bash
uvicorn opendirect21.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Verify Installation

Server should start at `http://localhost:8000`

```bash
# Health check
curl http://localhost:8000/health

# Expected response:
# {"status": "healthy", "service": "...", "version": "0.1.0", "timestamp": "..."}
```

## Access Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=opendirect21 --cov-report=html

# Run specific test file
pytest tests/test_health.py -v

# Run parser smoke tests
python -m tools.spec_parser.smoke_test
```

## Next Steps

1. **Read the documentation**
   - [TECHNICAL_SPECIFICATION.md](TECHNICAL_SPECIFICATION.md) — Full technical spec
   - [API_GUIDE.md](API_GUIDE.md) — API usage examples

2. **Generate models from specs**
   ```bash
   cp OpenDirect.v2.1.final.md tools/spec_parser/
   cp AdCOM\ v1.0\ FINAL.md tools/spec_parser/
   python -m tools.spec_parser.gen_models
   python -m tools.spec_parser.gen_routes
   ```

3. **Deploy to production**
   - See [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md)

## Troubleshooting

### ModuleNotFoundError: No module named 'opendirect21'

```bash
# Install in development mode
pip install -e .

# Or ensure PYTHONPATH is set
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Port 8000 already in use

```bash
# Use different port
uvicorn opendirect21.main:app --port 8001

# Or find and kill process
lsof -i :8000
kill -9 <PID>
```

### Python version mismatch

```bash
# Check Python version
python --version  # Should be 3.12+

# Use specific version
python3.12 -m venv venv
```

## Common Commands

```bash
# Code formatting
black opendirect21 tools tests

# Linting
ruff check opendirect21 tools tests

# Type checking
mypy opendirect21

# Generate API docs
python -m pdoc opendirect21 -o docs/api
```

## Environment Variables

See `.env.example` for all options:

```bash
SERVER_HOST=0.0.0.0          # Bind address
SERVER_PORT=8000             # Port number
SERVER_RELOAD=true           # Hot reload
LOG_LEVEL=INFO               # Logging level
DATABASE_URL=sqlite:///...   # Database connection
CORS_ORIGINS=["*"]           # CORS origins
```

## Questions?

- Check [README.md](../README.md) for overview
- Check [TECHNICAL_SPECIFICATION.md](TECHNICAL_SPECIFICATION.md) for detailed info
- Check GitHub [Issues](https://github.com/pv-udpv/opendirect21-adcom/issues)
