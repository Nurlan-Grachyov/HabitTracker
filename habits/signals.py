from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from habits.models import Habits
from habits.services import is_time_to_send_reminder


@receiver(post_migrate)
def create_periodic_tasks(sender, **kwargs):
    PeriodicTask.objects.filter(name__startswith="Send a reminder about").delete()
    habits = Habits.objects.all()
    for habit in habits:
        if is_time_to_send_reminder(habit):
            task_name = f"Send a reminder about {habit}"
            schedule, _ = IntervalSchedule.objects.get_or_create(
                every=habit.periodicity,
                period=IntervalSchedule.SECONDS,
            )

            PeriodicTask.objects.update_or_create(
                name=task_name,
                defaults={
                    'interval': schedule,
                    'task': "habits.tasks.time_habit"
                }
            )
