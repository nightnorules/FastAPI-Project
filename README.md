# FastAPI Shop

Небольшой backend для интернет-магазина на FastAPI.

В проекте есть:
- JWT-аутентификация
- CRUD для категорий и товаров
- PostgreSQL
- Redis cache
- Celery worker и beat
- Prometheus + Grafana
- Nginx и pgAdmin в docker-стеке

## Stack

- FastAPI
- SQLAlchemy Async
- PostgreSQL
- Redis
- Celery
- Gunicorn
- Docker Compose

## Запуск

```bash
docker compose up --build
```

Проверка:

```bash
curl http://localhost:8000/health
```

## Основные адреса

- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- Grafana: `http://localhost:3000`
- Prometheus: `http://localhost:9090`
- pgAdmin: `http://localhost:5050`

## Переменные окружения

Для Docker используется:

- `.env.docker.example` — значения по умолчанию для docker-compose
- `.env.docker` — локальный файл, если захочешь вынести свои значения отдельно

Для локального запуска приложения можно использовать `.env`.
