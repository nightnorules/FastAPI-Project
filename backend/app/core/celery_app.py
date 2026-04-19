from celery import Celery

from backend.app.core.config import settings

celery_app = Celery(
    "fastapi_shop",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)


celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    broker_connection_retry_on_startup=True,
    task_track_started=True,
    task_time_limit=30 * 60,
    task_soft_time_limit=25 * 60,
    result_expires=3600,
    result_backend_transport_options={
        "master_name": "mymaster",
        "retry_on_timeout": True,
    },
    worker_prefetch_multiplier=4,
    worker_max_tasks_per_child=1000,
)
