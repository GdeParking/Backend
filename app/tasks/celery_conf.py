from .celery import Celery
from app.core.config import settings

print(settings.REDIS_PORT)
celery = Celery(
    "tasks",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    include=["app.tasks.tasks"]
)