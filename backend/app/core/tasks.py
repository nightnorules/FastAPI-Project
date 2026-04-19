import logging
from datetime import datetime
from backend.app.core.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=3)
def send_email_notification(self, email: str, subject: str, message: str):
    try:
        logger.info(f"Sending email to {email}: {subject}")
        return {"status": "sent", "email": email}
    except Exception as exc:
        logger.error(f"Email sending failed: {exc}")
        raise self.retry(exc=exc, countdown=300)


@celery_app.task(bind=True, max_retries=2)
def update_product_statistics(self, product_id: int):
    try:
        logger.info(f"Updating stats for product {product_id}")
        stats = {
            "views": 150,
            "clicks": 45,
            "conversions": 12,
            "updated_at": datetime.utcnow().isoformat(),
        }
        return stats
    except Exception as exc:
        logger.error(f"Stats update failed: {exc}")
        raise self.retry(exc=exc, countdown=60)


@celery_app.task
def cleanup_expired_sessions():
    logger.info("Cleaning up expired sessions")
    return {"status": "cleaned", "expired_sessions": 23}


@celery_app.task
def generate_daily_report():
    logger.info("Generating daily report")
    return {
        "date": datetime.utcnow().date().isoformat(),
        "orders": 87,
        "revenue": 4520.50,
        "new_users": 12,
    }

