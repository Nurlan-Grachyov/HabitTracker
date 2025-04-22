from datetime import datetime, timedelta

from django_celery_beat.models import IntervalSchedule, PeriodicTask

from habits.models import Habits


def is_time_to_send_reminder(habit):
    """Вычисление разницы между настоящим временем и временем, когда задача должна начаться. Если разница менее 5 минут, вернется True."""
    tolerance_minutes = 5

    now = datetime.now()

    start_time_moscow = datetime.combine(now.date(), habit.start_time)

    delta = abs(now - start_time_moscow)

    return delta <= timedelta(minutes=tolerance_minutes)


def create_periodic_tasks(sender, **kwargs):
    """ Создание задачи """
    habits = Habits.objects.all()
    for habit in habits:
        if is_time_to_send_reminder(habit):
            task_name = f"Send a reminder about {habit}"
            schedule, _ = IntervalSchedule.objects.get_or_create(
                every=habit.periodicity,
                period=IntervalSchedule.DAYS,
            )

            PeriodicTask.objects.update_or_create(
                name=task_name,
                defaults={"interval": schedule, "task": "habits.tasks.time_habit"},
            )
