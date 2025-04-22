import requests
from celery import shared_task
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from config.settings import BOT_TOKEN, TG_URL
from habits.models import Habits
from habits.services import is_time_to_send_reminder


@shared_task
def time_habit():
    """Задача для отправки уведомления в Телеграм."""
    habits = Habits.objects.all()
    for habit in habits:
        if habit.owner.tg_id and is_time_to_send_reminder(habit):
            params = {
                "text": "Send a reminder about habit",
                "chat_id": habit.owner.tg_id,
            }
            try:
                response = requests.get(
                    f"{TG_URL}{BOT_TOKEN}/sendMessage", params=params
                )
                print(response.json())
            except Exception as e:
                print(f"Ошибка: {e}")
