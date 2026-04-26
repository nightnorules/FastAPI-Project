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
- **Orders**: `/api/v1/orders` (CRUD)

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
# Apply migrations
psql -h localhost -U shop_user -d shop_db < migrations/001_create_orders_table.sql
uvicorn backend.app.main:app --reload
```

---

**Версия**: 2.0.0

## 📦 Заказы (Orders)

Функциональность для управления заказами:

### Endpoints

```http
POST   /api/v1/orders           # Создать заказ
GET    /api/v1/orders           # Список заказов пользователя
GET    /api/v1/orders/{id}      # Получить заказ
PATCH  /api/v1/orders/{id}      # Обновить статус
DELETE /api/v1/orders/{id}      # Отменить заказ
```

### Статусы заказа

- `pending` - ожидание подтверждения
- `confirmed` - подтвержден
- `shipped` - отправлен
- `delivered` - доставлен
- `cancelled` - отменен

### Пример создания заказа

```bash
curl -X POST http://localhost:8000/api/v1/orders \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {"product_id": 1, "quantity": 2},
      {"product_id": 2, "quantity": 1}
    ]
  }'
```