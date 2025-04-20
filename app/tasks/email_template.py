from email.message import EmailMessage
from app.config import settings
from pydantic import EmailStr

def create_booking_confirmation_template(
    booking: dict,
    email_to: EmailStr,
):
    email = EmailMessage()

    email["Subject"] = "Подтверждение брони"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
  f"""
            <h1>Подтверждение брони<h1>
            Вы забронировали отель с {booking["date_from"]} по {booking["date_to"]}
        """,
        subtype="html"
    )
    return email


async def create_registration_confirmation_email(email_to: EmailStr, code: str):
    """Синхронная отправка email с обёрткой в async для совместимости"""
    email = EmailMessage()

    email["Subject"] = "Email Верификация"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
              <h1>Подтверждение Почты<h1>
              <h2>Ваш код: {code}<h2>
          """,
        subtype="html"
    )

    return email