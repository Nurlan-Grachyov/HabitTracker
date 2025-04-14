from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from habits.models import Habits
from habits.permission import Owner, ListHabits
from habits.serializers import HabitsSerializer


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
        print("1")
        if self.action == "list":
            print("2")
            permission_classes = [ListHabits]
        elif self.action in ("create", "retrieve", "update", "partial_update", "destroy"):
            permission_classes = [Owner]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]