
# FastAPI Shop

Масштабируемый backend-магазин на FastAPI с асинхронной архитектурой, аутентификацией, мониторингом, очередями задач и инфраструктурой на Docker.

## Архитектура

- **FastAPI** — основной web-фреймворк (async, type hints)
- **SQLAlchemy 2.0** (asyncpg) — ORM, асинхронные транзакции
- **Alembic** — миграции схемы БД
- **Celery + Redis** — фоновые задачи и брокер
- **Prometheus + Grafana** — метрики и мониторинг (`/metrics`)
- **Nginx** — обратный прокси, SSL
- **Docker Compose** — инфраструктура (app, db, redis, nginx)

### Слои приложения
- **API**: FastAPI endpoints (авторизация, продукты, категории, заказы)
- **Services**: бизнес-логика, валидация, orchestration
- **Repositories**: доступ к данным, абстракция над ORM
- **Schemas**: Pydantic-схемы для валидации и сериализации

## Быстрый старт

```bash
git clone <repo-url>
cd fastapi-project-1
cp .env.example .env
docker-compose up --build
```
Приложение: http://localhost:8000
Swagger UI: http://localhost:8000/docs

## Миграции БД

```bash
docker-compose exec app alembic upgrade head
```

## Тестирование

```bash
docker-compose exec app pytest
```
Покрытие:
```bash
docker-compose exec app pytest --cov=backend/app
```

## Переменные окружения

- `DATABASE_URL` — строка подключения к Postgres
- `JWT_SECRET_KEY` — секрет для токенов (min 32 символа)
- `REDIS_URL` — адрес брокера Redis
- `CORS_ORIGINS` — список разрешённых origin
- `DEBUG_ENABLED` — режим отладки (True/False)

## Мониторинг и метрики

- `/metrics` — Prometheus-метрики (requests, latency)
- `/health` — healthcheck endpoint
- Grafana dashboard — provisioning в папке `grafana/`


## Примеры API-запросов

Регистрация пользователя:
```bash
curl -X POST http://localhost:8000/api/auth/register \
	-H "Content-Type: application/json" \
	-d '{"email": "user@example.com", "password": "string"}'
```

Авторизация:
```bash
curl -X POST http://localhost:8000/api/auth/login \
	-H "Content-Type: application/json" \
	-d '{"email": "user@example.com", "password": "string"}'
```

Получить список товаров:
```bash
curl http://localhost:8000/api/products
```

---

## CI/CD

- Рекомендуется использовать GitHub Actions или GitLab CI для автоматизации тестов, линтинга и деплоя
- Пример шагов: build, pytest, flake8, black, alembic upgrade, docker push

---

## Безопасность

- Храните секреты вне git (используйте .env, секреты CI/CD)
- Используйте HTTPS (nginx + SSL)
- Включайте CORS только для доверенных origin
- Регулярно обновляйте зависимости (safety, bandit)

---

## Production

- Для production используйте отдельные .env и docker-compose.override.yml
- Настройте мониторинг (Prometheus, Grafana)
- Используйте gunicorn + uvicorn worker
- Настройте резервное копирование БД

---

## Расширяемость

- Чистая архитектура: легко добавлять новые endpoints, сервисы, репозитории
- Поддержка версионирования API (v1, v2)

---



