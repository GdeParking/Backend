from app.tasks.celery import celery

@celery.task
def do_something():
    pass