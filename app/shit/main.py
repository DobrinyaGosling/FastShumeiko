import gspread
from gspread import Spreadsheet

from app.shit.config import (get_client, get_table_by_url,
                             TEST_TABLE_URL, PROD_TABLE_URL)
from app.shit.utils import get_fake_users
from app.shit.utils import get_fake_users
from app.shit.config import SUBJECTS

table_url = TEST_TABLE_URL

def join_the_queue(subject: str):
    subject_dict = SUBJECTS[subject]
    worksheet_title = subject_dict['sheet']

    client = get_client()
    table = get_table_by_url(client, table_url)
    worksheet = table.worksheet(worksheet_title)

    values = [["идите нахуй"] for _ in range(subject_dict['range'])]
    worksheet.update(range_name=subject_dict['cells'], values=values)
    values2 = [[""] for _ in range(subject_dict['range'])]
    worksheet.update(range_name=subject_dict['cells'], values=values2)
    worksheet.update(range_name=subject_dict['cell_dima'], values=[[1]])
    worksheet.update(range_name=subject_dict['cell_roma'], values=[[3]])
