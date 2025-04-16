import requests

from config.settings import TG_URL, BOT_TOKEN
from celery import shared_task

from habits.models import Habits


@shared_task
def time_habit():
    habits = Habits.objects.all()
    for habit in habits:
        if habit.owner.tg_id:
            params = {
                'text': f'Send a reminder about {habit.name}',
                'chat_id': habit.owner.tg_id,
            }
            print(habit.name)
            requests.get(f'{TG_URL}{BOT_TOKEN}/sendMessage', params=params)