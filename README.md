# FastAPI Shop 🛒

A production-ready, scalable e-commerce backend built with FastAPI featuring async architecture, JWT authentication, background task queues, monitoring, and full Docker infrastructure.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🚀 Live Demo

> 🔗 Production API: https://fastapi-project-production-f143.up.railway.app  
> 📚 Swagger UI: https://fastapi-project-production-f143.up.railway.app/docs  
> 📖 ReDoc: https://fastapi-project-production-f143.up.railway.app/redoc

---

## 📦 Tech Stack

| Layer | Technology |
|---|---|
| **Framework** | FastAPI (async, type hints) |
| **Database** | PostgreSQL 15 + SQLAlchemy 2.0 (asyncpg) |
| **Migrations** | Alembic |
| **Cache / Broker** | Redis 7 |
| **Task Queue** | Celery (worker + beat scheduler) |
| **Monitoring** | Prometheus + Grafana |
| **Reverse Proxy** | Nginx |
| **Containerization** | Docker + Docker Compose |
| **Testing** | pytest + pytest-asyncio |
| **CI/CD** | GitHub Actions |

---

## 🏗️ Architecture

The project follows a clean layered architecture:

```
API Layer (FastAPI routers)
    ↓
Service Layer (business logic, validation, orchestration)
    ↓
Repository Layer (data access, ORM abstraction)
    ↓
Database (PostgreSQL via SQLAlchemy 2.0 async)
```

### Services included in Docker Compose

- **app** — FastAPI app served via Gunicorn + UvicornWorker
- **db** — PostgreSQL 15
- **redis** — Redis 7 (cache + Celery broker)
- **celery_worker** — background task processing
- **celery_beat** — periodic task scheduler
- **nginx** — reverse proxy with SSL support
- **prometheus** — metrics collection
- **grafana** — metrics dashboard (provisioned automatically)
- **pgadmin** — database management UI

---

## ⚡ Quick Start

### Prerequisites

- Docker & Docker Compose installed

### Run locally

```bash
git clone https://github.com/nightnorules/FastAPI-Project.git
cd FastAPI-Project
cp .env.example .env
docker-compose up --build
```

| Service | URL |
|---|---|
| API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |
| Grafana | http://localhost:3000 |
| Prometheus | http://localhost:9090 |
| pgAdmin | http://localhost:5050 |

### Apply database migrations

```bash
docker-compose exec app alembic upgrade head
```

---

## 🧪 Testing

Run the full test suite:

```bash
docker-compose exec app pytest
```

With coverage report:

```bash
docker-compose exec app pytest --cov=backend/app
```

---

## 📡 API Overview

### Auth

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "yourpassword"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "yourpassword"}'
```

### Products

```bash
# Get all products
curl http://localhost:8000/api/products

# Get product by ID (authenticated)
curl http://localhost:8000/api/products/1 \
  -H "Authorization: Bearer <your_token>"
```

Full interactive API documentation available at `/docs`.

---

## ⚙️ Environment Variables

Copy `.env.example` to `.env` and configure:

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string |
| `JWT_SECRET_KEY` | JWT signing secret (min 32 chars) |
| `REDIS_URL` | Redis connection URL |
| `CORS_ORIGINS` | Allowed CORS origins (JSON list) |
| `DEBUG_ENABLED` | Enable debug mode (`True`/`False`) |

---

## 📊 Monitoring

- **`/health`** — healthcheck endpoint
- **`/metrics`** — Prometheus metrics (request count, latency, errors)
- **Grafana** — pre-provisioned dashboard at `grafana/provisioning/`

---

## 🔒 Security

- JWT-based authentication (access tokens)
- Secrets managed via `.env` (never committed to git)
- HTTPS via Nginx + SSL
- CORS restricted to trusted origins
- Dependency scanning recommended: `safety`, `bandit`

---

## 🚢 Production Notes

- Use separate `.env` and `docker-compose.override.yml` for production
- Gunicorn + UvicornWorker already configured for production serving
- Set up automated PostgreSQL backups
- Enable Prometheus alerting rules for error rate / latency spikes

---

## 📁 Project Structure

```
FastAPI-Project/
├── backend/app/
│   ├── api/          # FastAPI routers (auth, products, orders, categories)
│   ├── core/         # Config, security, Celery setup
│   ├── models/       # SQLAlchemy models
│   ├── repositories/ # Data access layer
│   ├── schemas/      # Pydantic schemas
│   └── services/     # Business logic
├── alembic/          # DB migrations
├── tests/            # pytest test suite
├── grafana/          # Grafana provisioning
├── prometheus/       # Prometheus config
├── nginx/            # Nginx config + SSL
├── .github/workflows/# CI/CD pipelines
├── docker-compose.yml
├── Dockerfile
└── .env.example
```

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first.

---

## 📄 License

[MIT](LICENSE)
