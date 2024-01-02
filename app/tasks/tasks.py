from pydantic import EmailStr
from app.core.config import settings
from app.tasks.celery_conf import celery
from app.tasks.email_template import create_camera_confirmation_template
import smtplib

@celery.task
def do_something():
    pass


@celery.task
def send_created_camera_email(
    camera: dict,
    email_to: EmailStr = settings.smtp_user
):
    msg_content = create_camera_confirmation_template(camera, email_to=settings.smtp_user)

    with smtplib.SMTP_SSL(settings.smtp_host, settings.smtp_port) as server:
        server.login(settings.smtp_user, settings.smtp_pass)
        server.send_message(msg_content)
