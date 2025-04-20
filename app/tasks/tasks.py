from app.tasks.config import celery
import smtplib
from app.config import settings
from pydantic import EmailStr
from app.tasks.email_template import create_booking_confirmation_template

@celery.task
def send_booking_confirmation_email(
    booking: dict,
    email_to: EmailStr
):
    print(f"❗DEBUG: Trying to send email to {email_to}")  # Лог в консоль Celery
    try:
        msg_content = create_booking_confirmation_template(booking, email_to)
        with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.login(settings.SMTP_USER, settings.SMTP_PASS)
            server.send_message(msg_content)
        print("❗DEBUG: Email sent successfully")
    except Exception as e:
        print(f"❗DEBUG: SMTP Error: {str(e)}")  # Лог ошибки
        raise

