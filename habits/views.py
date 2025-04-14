import json
from datetime import timedelta, datetime

from django.utils import timezone
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from habits.models import Habits
from habits.permission import Owner, ListHabits
from habits.serializers import HabitsSerializer
from habits.tasks import time_habit


class HabitsViewSet(ModelViewSet):
    serializer_class = HabitsSerializer
    queryset = Habits.objects.all()

    def perform_create(self, serializer):
        """
        Метод создание курса.
        """

        serializer.save(owner=self.request.user)

    def get_permissions(self):
        """
        Метод предоставления прав доступа.
        """

        if self.action == "list":
            permission_classes = [ListHabits]
        elif self.action in ("create", "retrieve", "update", "partial_update", "destroy"):
            permission_classes = [Owner]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Метод возврата списка продуктов по критериям.
        """

        if self.request.user.is_authenticated:
            return Habits.objects.filter(owner=self.request.user) or Habits.objects.filter(is_public=True)
        elif self.request.user.is_superuser:
            return Habits.objects.all()

    def time_send_message_about_habit(self):
        habits = Habits.objects.all()
        for habit in habits:
            schedule, created = IntervalSchedule.objects.get_or_create(
                every=5,
                period=IntervalSchedule.SECONDS,
            )

            PeriodicTask.objects.create(
                interval=schedule,
                name='Send a reminder about habit',
                task='habits.tasks.time_habit',
                args=json.dumps(['arg1', 'arg2']),
                kwargs=json.dumps({
                    'be_careful': True,
                }),
                expires=timezone.now() + timedelta(seconds=30)
            )
            time_habit.delay(maessage=f"Вам пора {habit.action} в {habit.place}",chat_id=habit.owner.tg_id)