from habits.services import send_tg_message
from celery import shared_task


@shared_task
def time_habit(message, tg_id):
    send_tg_message(message, tg_id)