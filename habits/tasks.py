import json

from celery import shared_task
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from django.utils.timezone import now
import requests
from config.settings import BOT_TOKEN, TG_URL
from habits.models import Habits
from habits.services import is_time_to_send_reminder


@shared_task
def time_habit(habit_id):
    """Отправка уведомления для конкретной привычки"""
    try:
        habit = Habits.objects.get(id=habit_id)
        if habit.owner.tg_id and is_time_to_send_reminder(habit):
            params = {
                "text": f"Напоминание: {habit.action} в {habit.time}",
                "chat_id": habit.owner.tg_id,
            }
            response = requests.get(f"{TG_URL}{BOT_TOKEN}/sendMessage", params=params)
            print(response.json())
    except Exception as e:
        print(f"Ошибка при отправке уведомления: {e}")


def setup_habit_tasks():
    """Создание/обновление периодических задач для привычек"""
    for habit in Habits.objects.all():
        schedule, _ = IntervalSchedule.objects.get_or_create(
            every=habit.periodicity,
            period=IntervalSchedule.DAYS,
        )

        task_name = f"Send a reminder about {habit}"

        PeriodicTask.objects.update_or_create(
            name=task_name,
            defaults={
                'interval': schedule,
                'task': 'habits.tasks.time_habit',
                'args': json.dumps([habit.id]),
                'start_time': now().replace(hour=habit.start_time.hour, minute=habit.start_time.minute),
                'enabled': True
            }
        )
