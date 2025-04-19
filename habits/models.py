import datetime

from django.core.validators import MaxValueValidator
from django.db import models

from config.settings import AUTH_USER_MODEL


class Habits(models.Model):
    place = models.CharField(verbose_name="место привычки", max_length=30)
    start_time = models.TimeField(verbose_name="время начала выполнения привычки")
    action = models.CharField(verbose_name="действие привычки")
    is_pleasant_habit = models.BooleanField(
        verbose_name="признак приятной привычки", default=False, null=True, blank=True
    )
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        verbose_name="связанная привычка",
        null=True,
        blank=True,
    )
    periodicity = models.PositiveSmallIntegerField(
        default=1, verbose_name="периодичность", null=True, blank=True
    )
    reward = models.CharField(
        verbose_name="вознаграждение", max_length=50, null=True, blank=True
    )
    time_to_complete = models.TimeField(
        verbose_name="время для выполнения привычки",
        validators=[MaxValueValidator(datetime.time(0, 2, 0))],
    )
    is_public = models.BooleanField(default=False)
    owner = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        verbose_name = "привычка"
        verbose_name_plural = "привычки"

    def __str__(self):
        return f"я буду {self.action} в {self.start_time} в {self.place}"
