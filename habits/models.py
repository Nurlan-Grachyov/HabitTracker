from django.db import models

from users.models import CustomUser


class Habits(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="user_habit"
    )
    place = models.CharField(verbose_name="место привычки", max_length=30)
    start_time = models.TimeField(verbose_name="время начала выполнения привычки")
    action = models.CharField(verbose_name="действие привычки")
    sign_pleasant_habit = models.CharField(
        verbose_name="признак приятной привычки", max_length=50
    )
    related_habit = models.CharField(verbose_name="связанная привычка", max_length=50)
    periodicity = models.PositiveSmallIntegerField(
        default=1, verbose_name="Периодичность"
    )
    reward = models.CharField(verbose_name="вознаграждение", max_length=50)
    time_to_complete = models.TimeField(verbose_name="время для выполнения привычки")
    is_public = models.BooleanField(default=False)

    class Meta:
        verbose_name = "привычка"
        verbose_name_plural = "привычки"

    def __str__(self):
        return f"я буду {self.action} в {self.start_time} в {self.place}"
