import json

import requests
from celery import shared_task
from django_celery_beat.models import CrontabSchedule, PeriodicTask

from config.settings import BOT_TOKEN, TG_URL
from habits.models import Habits
from habits.services import is_time_to_send_reminder


@shared_task
def time_habit(habit_id):
    """Отправка уведомления для конкретной привычки"""
    try:
        habit = Habits.objects.get(id=habit_id)
        print(is_time_to_send_reminder(habit))
        if habit.owner.tg_id and is_time_to_send_reminder(habit):
            params = {
                "text": f"Напоминание: {habit.action} в {habit.start_time}",
                "chat_id": habit.owner.tg_id,
            }
            response = requests.get(f"{TG_URL}{BOT_TOKEN}/sendMessage", params=params)
            print(response.json())
    except Exception as e:
        print(f"Ошибка при отправке уведомления: {e}")


def setup_habit_tasks():
    """Создание/обновление периодических задач для привычек"""
    for habit in Habits.objects.all():
        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute=str(habit.start_time.minute),
            hour=str(habit.start_time.hour),
            day_of_week="*",
            day_of_month="*",
            month_of_year="*",
            timezone="Europe/Moscow",
        )

        task_name = f"Send a reminder about {habit}"

        PeriodicTask.objects.update_or_create(
            name=task_name,
            defaults={
                "crontab": schedule,
                "task": "habits.tasks.time_habit",
                "args": json.dumps([habit.id]),
                "enabled": True,
            },
        )
