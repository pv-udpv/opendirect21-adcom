# Architecture & Design

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    HTTP Clients                             │
│  (Browsers, REST Clients, Mobile Apps, etc)                │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Reverse Proxy (Nginx/Apache)                   │
│              - Load Balancing                               │
│              - SSL/TLS Termination                          │
│              - Static File Caching                          │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI Application                       │
│                  (opendirect21/main.py)                    │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                  ASGI Server (Uvicorn)                 │ │
│  │            (async, non-blocking I/O)                   │ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              Middleware Stack                          │ │
│  │  - CORS (for cross-origin requests)                   │ │
│  │  - Error Handlers (500, 404, etc)                     │ │
│  │  - Request Logging                                    │ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                  API Routers                           │ │
│  │  ├─ /health       (Health checks)                     │ │
│  │  ├─ /organizations (OpenDirect)                       │ │
│  │  ├─ /accounts      (OpenDirect)                       │ │
│  │  ├─ /orders        (OpenDirect)                       │ │
│  │  └─ /adcom         (Adcom endpoints) [TODO]           │ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │            Pydantic Models & Validation                │ │
│  │  ├─ Organization                                       │ │
│  │  ├─ Account                                            │ │
│  │  ├─ Order                                              │ │
│  │  ├─ Line                                               │ │
│  │  ├─ Creative                                           │ │
│  │  ├─ Assignment                                         │ │
│  │  └─ ... (20+ OpenDirect models)                        │ │
│  │  └─ ... (15+ Adcom models) [TODO]                      │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────┬─────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Store Layer                          │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Development: InMemoryStore (opendirect21/store.py)   │ │
│  │  - Thread-safe in-memory hash maps                    │ │
│  │  - UUID generation                                    │ │
│  │  - Fast prototyping                                   │ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Production: PostgreSQL / MongoDB (TODO)              │ │
│  │  - Persistent storage                                 │ │
│  │  - ACID transactions                                  │ │
│  │  - Scaling & Replication                              │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Data Models

### OpenDirect 2.1 Core Hierarchy

```
Organization (Publisher/Buyer/Advertiser)
  │
  ├─ Account (Buyer Account)
  │   │
  │   ├─ Order (Campaign Order)
  │   │   │
  │   │   ├─ Line (Line Item)
  │   │   │   │
  │   │   │   ├─ Creative (Advertisement)
  │   │   │   │
  │   │   │   └─ Assignment (Creative-to-Line binding)
  │   │   │
  │   │   └─ ChangeRequest
  │   │
  │   └─ Creative (Account-level Creative)
  │
  └─ Contact (Organization Contact Info)

Product (Inventory/Placement)
  │
  ├─ AdUnit (Ad Slot in Product)
  │
  └─ Pricing (CPM, CPC, etc)
```

### Adcom v1.0 Core Hierarchy (TODO)

```
Ad (Advertisement Container)
  │
  ├─ Display (Display Ad)
  │   ├─ Banner (Simple Banner)
  │   ├─ Native (Native Ad)
  │   └─ Rich Media
  │
  ├─ Video (Video Ad)
  │   ├─ Asset (Video Stream)
  │   ├─ Tracking (Impression/Click Events)
  │   └─ Extensions
  │
  └─ Audio (Audio Ad)

Asset (Media Asset)
  │
  ├─ LinkAsset (URL/Click target)
  ├─ ImageAsset (Image file)
  ├─ VideoAsset (Video file)
  ├─ TitleAsset (Text/Title)
  └─ DataAsset (Structured data)

Context (Contextual info)
  │
  ├─ Publisher (Content Publisher)
  ├─ Content (Article/Video content)
  ├─ User (Viewer/User info)
  ├─ Device (Browser/Device)
  └─ Geo (Geolocation)
```

## Request/Response Flow

```
1. CLIENT REQUEST
   ┌─────────────────────────────────────┐
   │ GET /api/v1/organizations/{org_id}  │
   │ Host: api.example.com               │
   │ Authorization: Bearer <token>       │
   └──────────────┬──────────────────────┘
                  │
                  ▼
2. NGINX REVERSE PROXY
   - Route request
   - Check rate limits
   - Add X-Forwarded headers
                  │
                  ▼
3. FASTAPI MIDDLEWARE
   - CORS check
   - Request logging
   - Error handling
                  │
                  ▼
4. API ROUTE HANDLER
   async def get_organization(org_id: str)
   - Validate org_id (Pydantic)
   - Call store.get()
   - Return response
                  │
                  ▼
5. DATA STORE QUERY
   InMemoryStore.get("organizations", org_id)
   - Lookup in hash map
   - Return entity dict
                  │
                  ▼
6. RESPONSE SERIALIZATION
   - Convert dict to Pydantic model
   - Validate response
   - Serialize to JSON
                  │
                  ▼
7. CLIENT RESPONSE
   ┌─────────────────────────────────────┐
   │ HTTP/1.1 200 OK                     │
   │ Content-Type: application/json      │
   │ {                                   │
   │   "id": "org-123",                  │
   │   "name": "Acme Publishing",        │
   │   "type": "Publisher",              │
   │   "created_at": "2024-01-01T...",  │
   │   "updated_at": "2024-01-02T..."  │
   │ }                                   │
   └─────────────────────────────────────┘
```

## Code Structure

### Package Organization

```
opendirect21/
├── __init__.py              # Package metadata
├── main.py                  # FastAPI app factory
├── config.py                # Pydantic Settings
├── store.py                 # Data store (InMemory/DB)
│
├── models/                  # Data models
│   ├── __init__.py
│   ├── base.py              # BaseModel, IDModel, TimestampedModel
│   └── generated/
│       ├── opendirect.py    # Auto-generated OpenDirect models
│       ├── adcom.py         # Auto-generated Adcom models (TODO)
│       └── enums.py         # Enum classes
│
├── api/                     # API routers
│   ├── __init__.py
│   ├── health.py            # Health check endpoints
│   ├── dependencies.py      # Shared dependencies
│   └── generated/
│       ├── opendirect_routes.py  # Auto-generated routes
│       └── adcom_routes.py       # Auto-generated routes (TODO)
│
tools/
├── spec_parser/
│   ├── md_tables.py         # Markdown parser
│   ├── gen_models.py        # Model generator
│   ├── gen_routes.py        # Router generator
│   ├── adcom_parser.py      # Adcom-specific parser (TODO)
│   └── smoke_test.py        # Parser verification
│
tests/
├── conftest.py              # Pytest fixtures
├── test_health.py           # Health check tests
├── test_api.py              # API endpoint tests
└── test_store.py            # Data store tests
```

## Design Patterns

### 1. Model Generation Pattern

```
Markdown Spec
    ↓
    ├─ MarkdownTableParser
    │    ├─ extract_objects()
    │    └─ parse_table_body()
    ↓
ObjectDef List
    ↓
    ├─ PydanticGenerator
    │    ├─ generate_model_code()
    │    └─ render_object()
    ↓
Python Model Classes (.py files)
    ↓
    ├─ FastAPI Routes (auto-generated)
    ├─ Swagger Docs (auto-generated)
    └─ Data Validation (auto)
```

### 2. Async/Await Pattern

```python
# All endpoints are async for non-blocking I/O
@app.get("/organizations/{org_id}")
async def get_organization(org_id: str) -> OrganizationResponse:
    # Non-blocking store operation
    org = await store.get("organizations", org_id)
    if not org:
        raise HTTPException(status_code=404)
    return org
```

### 3. Dependency Injection

```python
# Pytest fixtures for testing
@pytest.fixture
async def client() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

# Pydantic settings for configuration
class Settings(BaseSettings):
    server_port: int = 8000
    database_url: str = "sqlite:///..."
```

### 4. Repository Pattern

```python
class InMemoryStore:
    """Data access layer (repository pattern)"""
    
    async def get(self, entity_type: str, entity_id: str):
        """Get entity by ID"""
        ...
    
    async def list(self, entity_type: str, skip: int, limit: int):
        """List entities with pagination"""
        ...
```

## Technology Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Web Framework | FastAPI | Async, Pydantic validation, auto-docs |
| ASGI Server | Uvicorn | High performance, async I/O |
| Data Validation | Pydantic v2 | Type hints, JSON schema, performance |
| Database | PostgreSQL | Production-ready, ACID, scaling |
| ORM | SQLAlchemy | Async support, relationships, migrations |
| Testing | pytest | Fixtures, async support, plugins |
| API Gateway | Nginx | Reverse proxy, SSL, caching |
| Container | Docker | Portability, reproducibility |
| CI/CD | GitHub Actions | Native GitHub integration |

## Scalability Considerations

### Horizontal Scaling

```
Load Balancer (HAProxy/Nginx)
    ├─ API Server 1 (Port 8001)
    ├─ API Server 2 (Port 8002)
    └─ API Server 3 (Port 8003)
        │
        └─ PostgreSQL (Central DB)
```

### Database Scaling

- **Read replicas**: For read-heavy workloads
- **Sharding**: By organization/account ID
- **Caching**: Redis for frequently accessed data

### Performance Optimization

1. **Connection pooling** (SQLAlchemy)
2. **Query optimization** (Indexes, lazy loading)
3. **Caching** (Redis/Memcached)
4. **CDN** (For static assets)
5. **Async I/O** (Non-blocking database calls)

## Security Architecture

```
Client
    │
    ├─ HTTPS (TLS 1.3)
    │
Nginx (Reverse Proxy)
    ├─ Rate limiting
    ├─ DDoS protection
    ├─ WAF (Web Application Firewall)
    │
FastAPI Application
    ├─ CORS validation
    ├─ Input sanitization (Pydantic)
    ├─ SQL injection prevention (ORM)
    ├─ CSRF tokens (if needed)
    │
Database
    ├─ Encrypted password storage
    ├─ Row-level security
    └─ Audit logging
```

## Monitoring & Observability

### Metrics

- Request count / response time
- Error rates (4xx, 5xx)
- Database query performance
- Cache hit rates
- Memory/CPU usage

### Logging

```
Application Logs
    ├─ Request/Response (INFO)
    ├─ Errors (ERROR)
    ├─ Performance (DEBUG)
    └─ Audit (WARNING)
        │
        └─ ELK Stack / CloudWatch
```

### Tracing

- Distributed tracing with OpenTelemetry
- Request ID correlation
- Dependency chain tracking

## Next Steps

1. **Database Integration**: Add PostgreSQL ORM
2. **Authentication**: Implement OAuth2/JWT
3. **Caching**: Add Redis layer
4. **Monitoring**: Set up Prometheus + Grafana
5. **Logging**: ELK stack integration
6. **Testing**: Increase coverage to 100%
