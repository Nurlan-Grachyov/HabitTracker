import datetime

from django.core.validators import MaxValueValidator
from django.db import models
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from users.models import CustomUser


class Habits(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="user_habit"
    )
    place = models.CharField(verbose_name="место привычки", max_length=30)
    start_time = models.TimeField(verbose_name="время начала выполнения привычки")
    action = models.CharField(verbose_name="действие привычки")
    is_pleasant_habit = models.BooleanField(verbose_name="признак приятной привычки", default=False)
    related_habit = models.ForeignKey("self", on_delete=models.CASCADE, verbose_name="связанная привычка", null=True,
                                      blank=True, validators=[])
    periodicity = models.PositiveSmallIntegerField(
        default=1, verbose_name="Периодичность"
    )
    reward = models.CharField(verbose_name="вознаграждение", max_length=50)
    time_to_complete = models.TimeField(verbose_name="время для выполнения привычки",
                                        validators=[MaxValueValidator(datetime.time(0, 2, 0))], )
    is_public = models.BooleanField(default=False)
    last_performed_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def clean(self):
        """
        Переопределение метода clean, который указывает либо связанную привычку, либо вознаграждение и проверяет, что связанная привычка является приятной
        """

        super().clean()
        if self.related_habit != self.reward:
            pass
        else:
            raise ValidationError("Должна быть указана либо связанная привычка, либо вознаграждение.")

        if self.related_habit and not self.related_habit.is_pleasant_habit:
            raise ValidationError({"related_habit": "Связанная привычка должна быть приятной."})

        if self.is_pleasant_habit and (self.reward or self.related_habit):
            raise ValidationError(
                {"message": "У приятной привычки не может быть вознаграждения или связанной привычки."})

        if timezone.now() - self.last_performed_at > timezone.timedelta(days=7):
            raise ValidationError("Нельзя выполнять привычку реже, чем в 7 дней")

    class Meta:
        verbose_name = "привычка"
        verbose_name_plural = "привычки"

    def __str__(self):
        return f"я буду {self.action} в {self.start_time} в {self.place}"
