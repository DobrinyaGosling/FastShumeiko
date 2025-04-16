from app.config import settings
from celery import Celery

celery_app = Celery(
    'tasks',
    broker=settings.get_redis_broker_url(),
    backend=settings.get_redis_back_url()
)
celery_app.autodiscover_tasks(['app.tasks'])



"""
from fastapi import requests

from app.config import celery_app

celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    enable_utc=True,  # Убедитесь, что UTC включен
    timezone='Europe/Moscow',  # Устанавливаем московское время
    broker_connection_retry_on_startup=True,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
)

@celery_app.task(
    name='',
    bind=True,
    max_retries=3,
    default_retry_delay=5
)
def upload(self)
"""