import gspread
import os
from gspread import Client
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from oauth2client.service_account import ServiceAccountCredentials
from oauth2client.tools import argparser, run_flow
from app.config import settings

# Настройки OAuth (замени значения из Google Cloud)
CLIENT_ID = settings.CLIENT_ID
CLIENT_SECRET = settings.CLIENT_SECRET
SCOPES = ["https://www.googleapis.com/auth/spreadsheets",
          'https://www.googleapis.com/auth/drive'
          ]
REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"  # Для десктопных приложений

TEST_TABLE_URL = settings.TEST_TABLE_URL
PROD_TABLE_URL = settings.PROD_TABLE_URL
SUBJECTS = {
    "ОАиП": {"sheet": "ОАиП", "cell_ilua": "I18", "cell_dima": "I28", "cell_roma": "I27", "cells": "I3:I33", "range": 31},
    "ОАиП подгруппа": {"sheet": "ОАиП", "cell_ilua": "I46", "cell_dima": "I50", "cell_roma": "I49", "cells": "I38:I53", "range": 16},
    "ПиОИвИС": {"sheet": "ПиОИвИС", "cell_ilua": "G18", "cell_dima": "G28", "cell_roma": "G27", "cells": "G3:G33", "range": 31},
    "ПиОИвИС подгруппа": {"sheet": "ПиОИвИС", "cell_ilua": "I46", "cell_dima": "G50", "cell_roma": "G49", "cells": "G38:G53", "range": 16},
    "ПиОИвИС пз": {"sheet": "ПЗ ПиОИвИС", "cell_ilua": "E18", "cell_dima": "E28", "cell_roma": "E27", "cells": "E3:E32", "range": 30},
}

CREDS_PATH = os.path.join(settings.BASE_DIR, "app", "shit", "creds.json")

def get_client():
    storage = Storage(CREDS_PATH)  # Файл для сохранения токена
    creds = storage.get()  # Пробуем загрузить сохранённый токен

    if not creds or creds.invalid:
        # Если токена нет или он невалидный, запускаем OAuth-флоу
        flow = OAuth2WebServerFlow(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            scope=SCOPES,
            redirect_uri=REDIRECT_URI,
            access_type='offline',
            prompt='consent'
        )
        flags = argparser.parse_args(args=['--noauth_local_webserver'])
        creds = run_flow(flow, storage, flags)
    return gspread.authorize(creds)


def get_table_by_url(client: Client, table_url):
    """Получение таблицы из Google Sheets по ссылке."""
    return client.open_by_url(table_url)

