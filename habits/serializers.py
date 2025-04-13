from django.db import models
from rest_framework.serializers import ModelSerializer

from habits.models import Habits


class HabitsSerializer(ModelSerializer):
    time_to_complete = models.CharField(Max=[])

    class Meta:
        model = Habits
        fields = "__all__"