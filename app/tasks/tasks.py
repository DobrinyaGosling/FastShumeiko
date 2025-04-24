import smtplib

import gspread.exceptions
from loguru import logger
from pydantic import EmailStr

from app.config import settings
from app.tasks.config import celery
from app.shit.config import SUBJECTS, PROD_TABLE_URL, TEST_TABLE_URL, get_client, get_table_by_url
from app.tasks.email_template import create_registration_confirmation_email, create_booking_confirmation_template
from datetime import datetime
import pytz

table_url = PROD_TABLE_URL

@celery.task
def send_booking_email(
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


@celery.task
def send_confirmation_registration_email(
        email_to: EmailStr,
        code: str
):
    try:
        msg_content = create_registration_confirmation_email(email_to=email_to, code=code)
        with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.login(settings.SMTP_USER, settings.SMTP_PASS)
            server.send_message(msg_content)
    except Exception as e:
        print(str(e))

@celery.task(bind=True)
def join_the_queue(self, subject: str):
    try:
        print(f"Starting task for subject: {subject}")  # Добавьте это
        subject_dict = SUBJECTS[subject]
        worksheet_title = subject_dict['sheet']
        print(worksheet_title)
        client = get_client()
        table = get_table_by_url(client, table_url)
        worksheet = table.worksheet(worksheet_title)

        values = [["идите нахуй"] for _ in range(subject_dict.get('range'))]
        worksheet.update(range_name=subject_dict['cells'], values=values)

        self.update_state(state='PROGRESS')
        values2 = [[""] for _ in range(subject_dict['range'])]
        worksheet.update(range_name=subject_dict['cells'], values=values2)

        worksheet.update(range_name=subject_dict['cell_dima'], values=[[1]])
        worksheet.update(range_name=subject_dict['cell_roma'], values=[[3]])

        return {
            "status": "completed",
            "subject": subject,
            "executed_at": datetime.now(pytz.timezone('Europe/Moscow')).isoformat()
        }

    except gspread.exceptions.GSpreadException as e:
        print(f"Error in task: {str(e)}")  # Логируем все ошибки
        self.retry(exc=e, countdown=30)
