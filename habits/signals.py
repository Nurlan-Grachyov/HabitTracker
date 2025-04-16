from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from habits.models import Habits
from habits.services import is_time_to_send_reminder

@receiver(post_migrate)
def create_periodic_tasks(sender, **kwargs):
    """ Обработчик сигнала, создающий периодические задачи после миграции базы данных. """
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