from enum import Enum
from fastapi import APIRouter
from datetime import time, datetime, timedelta
from app.shit.config import SUBJECTS
from app.tasks.tasks import join_the_queue
import pytz
from redis import Redis
from app.config import settings
import json


router = APIRouter(prefix='/shit', tags=['Sheet'])

Subject = Enum(
    'subject',
    {key: key for key in SUBJECTS.keys()},
    type=str
)


class Pair(str, Enum):
    SECOND = "11:55"
    THIRD = "13:45"
    FOURTH = "15:20"
    NOW = "now"

    def get_execution_time(self) -> datetime:
        """Возвращает datetime с учётом часового пояса и минимальной задержки"""
        msk_tz = pytz.timezone('Europe/Moscow')
        now = datetime.now(msk_tz)

        if self.value == "now":
            return now + timedelta(seconds=10)  # Минимальная задержка

        hour, minute = map(int, self.value.split(':'))
        eta = msk_tz.localize(datetime.combine(now.date(), time(hour, minute)))

        # Если время уже прошло, переносим на следующий день
        if eta < now:
            eta += timedelta(days=1)

        return eta


@router.post('/')
async def do_the_shiiit(
    subject: Subject,
    lesson: Pair,
    password: str
):
    if password != 'kazdep':
        return "Пшёл нахуй"

    eta = lesson.get_execution_time()

    task = join_the_queue.apply_async(
        args=[subject.value],
        eta=eta  # Время выполнения
    )

    return {
        "message": "Task scheduled",
        "task_id": task.id,
        "scheduled_time": eta.isoformat(),
        "subject": subject.value,
        "lesson": lesson.value
    }

@router.get("/")
async def get_tasks():
    broker = Redis.from_url(settings.get_redis_broker_url())
    result = {}

    for task_id, task_data_str in broker.hgetall('unacked').items():
        try:
            # Парсим строку как JSON (она внутри ещё строки)
            task_list = json.loads(task_data_str)

            # Первый элемент списка - словарь с данными задачи
            task_dict = task_list[0]

            # Достаём headers и из них берём eta
            eta_str = task_dict['headers']['eta']

            # Конвертируем строку времени в datetime объект
            eta_time = datetime.fromisoformat(eta_str)

            # Сохраняем в результат
            result[task_id] = eta_time.time().isoformat()

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            result[task_id] = f"Error parsing task: {str(e)}"

    return result
