import requests

from config.settings import TG_URL, BOT_TOKEN
from celery import shared_task

from habits.models import Habits
from habits.services import is_time_to_send_reminder


@shared_task
def time_habit():
    # habits = Habits.objects.all()
    # for habit in habits:
    #     if habit.owner.tg_id:
    #         if is_time_to_send_reminder(habit):
    #             params = {
    #                 'text': f'Send a reminder about habit',
    #                 'chat_id': habit.owner.tg_id,
    #             }
    #             requests.get(f'{TG_URL}{BOT_TOKEN}/sendMessage', params=params)
    print("Функция работает")