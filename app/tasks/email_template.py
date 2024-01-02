from email.message import EmailMessage
from pydantic import EmailStr
from app.core.config import settings

def create_camera_confirmation_template(
        camera = dict,
        email_to = EmailStr
):
    email = EmailMessage()
    email["Subject"] = "Добавлена новая камера!"
    email["From"] = settings.smtp_user
    email["To"] = email_to

    email.set_content(
        f"""
        <h1>К вашему сведению, была добавлена новая камера.</h1>
        Адрес камеры: {camera["address"]}
        URL камеры: {camera["cam_url"]}
        """,
        subtype = "html"
    )

    return email
