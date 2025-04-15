from datetime import timedelta
import pytz
import requests
from django.utils import timezone
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from config.settings import TG_URL, BOT_TOKEN
from habits.models import Habits


def send_tg_message(message, tg_id):
    params = {
        'text': message,
        'chat_id': tg_id,
    }
    requests.get(f'{TG_URL}{BOT_TOKEN}/sendMessage', params=params)


def is_time_to_send_reminder(habit):
    tolerance_minutes = 5

    moscow_tz = pytz.timezone('Europe/Moscow')
    now = timezone.now().astimezone(moscow_tz)
    start_time_moscow = habit.start_time.astimezone(moscow_tz)

    delta = abs(now - start_time_moscow)

    return delta <= timedelta(minutes=tolerance_minutes)


def time_send_message_about_habit():
    habits = Habits.objects.all()
    for habit in habits:
        if is_time_to_send_reminder(habit):
            schedule, _ = IntervalSchedule.objects.get_or_create(
                every=habit.periodicity,
                period=IntervalSchedule.DAYS,
            )

            PeriodicTask.objects.create(
                interval=schedule,
                name=f'Send a reminder about {habit.name}',
                task='habits.tasks.time_habit',
            )
