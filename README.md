# 🛍️ FastAPI Shop

Backend для интернет-магазина на FastAPI с JWT-аутентификацией, Redis кешем и мониторингом.

## ⚡ Быстрый старт

```bash
docker compose up --build
curl http://localhost:8000/health
```

## 🛠️ Стек

- FastAPI, SQLAlchemy Async, PostgreSQL, Redis, Celery
- Prometheus + Grafana (мониторинг)
- Nginx (reverse proxy), pgAdmin

## 📱 API

- **Docs**: http://localhost:8000/docs
- **Auth**: `/api/v1/auth/register`, `/api/v1/auth/login`
- **Categories**: `/api/v1/categories` (CRUD)
- **Products**: `/api/v1/products` (CRUD)

## 🔗 Сервисы

| Сервис | URL |
|--------|-----|
| API | http://localhost:8000 |
| Swagger | http://localhost:8000/docs |
| Grafana | http://localhost:3000 |
| Prometheus | http://localhost:9090 |
| pgAdmin | http://localhost:5050 |

## ⚙️ Конфиг

Основные переменные в `.env`:

```env
DATABASE_URL=postgresql://shop_user:shop_password@localhost:5432/shop_db
JWT_SECRET_KEY=your-secure-key-min-32-chars
REDIS_URL=redis://localhost:6379/0
```

Примеры: `.env.example`, `.env.docker.example`

## 🧪 Тесты

```bash
pytest                    # Все тесты
pytest --cov=backend     # С покрытием
pytest tests/test_auth.py # Конкретный файл
```

## 📦 Локальная установка

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn backend.app.main:app --reload
```

---

**Версия**: 2.0.0
