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
async def get_scheduled_tasks():
    """Возвращает все запланированные задачи из Redis"""
    broker = Redis.from_url(settings.get_redis_broker_url())
    tasks = {}

    # Получаем все задачи из unacked-очереди
    unacked_tasks = broker.hgetall('unacked')

    for task_id, task_data_str in unacked_tasks.items():
        try:
            # Преобразуем строку в Python-объект
            task_data = json.loads(task_data_str)
            tasks[task_id.decode()] = task_data
        except json.JSONDecodeError:
            tasks[task_id.decode()] = {"error": "Invalid JSON data"}

    return {
        "count": len(tasks),
        "tasks": tasks
    }