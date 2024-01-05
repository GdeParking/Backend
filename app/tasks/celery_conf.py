from celery import Celery
from celery.schedules import crontab
from app.core.config import settings

celery = Celery(
    "tasks",
    broker=f"redis://{settings.redis_host}:{settings.redis_port}",
    include=["app.tasks.tasks",
             "app.tasks.scheduled"]
)


celery.conf.beat_schedule = {
    "some_name": {
        "task": "periodic_task",
        "schedule": crontab(minute=10)
    }
}