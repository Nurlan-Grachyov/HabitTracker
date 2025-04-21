from django.utils import timezone
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from habits.models import Habits


class HabitsSerializer(ModelSerializer):
    """
    Сериализатор привычек
    """

    class Meta:
        model = Habits
        exclude = ["owner"]

    def create(self, validated_data):
        habit = super().create(validated_data)
        habit.performed_at = timezone.now()
        habit.save()
        return habit

    def update(self, instance, validated_data):
        updated_instance = super().update(instance, validated_data)
        updated_instance.performed_at = timezone.now()
        updated_instance.save()
        return updated_instance

    def validate(self, data):
        if not data.get("related_habit") and not data.get("reward"):
            raise serializers.ValidationError(
                "Необходимо указать либо связанную привычку, либо награду."
            )

        if data.get("is_pleasant_habit") and (
            data.get("reward") or data.get("related_habit")
        ):
            raise serializers.ValidationError(
                {
                    "message": "У приятной привычки не может быть вознаграждения или связанной привычки."
                }
            )

        if data.get("related_habit") and not data["related_habit"].is_pleasant_habit:
            raise serializers.ValidationError(
                {"related_habit": "Связанная привычка должна быть приятной"}
            )

        if data.get("performed_at") and timezone.now() - data[
            "performed_at"
        ] > timezone.timedelta(days=7):
            raise serializers.ValidationError(
                "Привычка должна выполняться чаще, чем раз в неделю"
            )

        return data
