from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from habits.models import Habits
from habits.views import HabitsViewSet
from users.models import CustomUser


class HabitsTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.habit_owner = CustomUser.objects.create(
            username="owner", email="owner@mail.ru"
        )
        self.habit_owner.set_password("12345678")
        self.habit_owner.save()

        self.normal_user = CustomUser.objects.create(
            username="normal_user", email="normal_user@mail.ru"
        )
        self.normal_user.set_password("12345678")
        self.normal_user.save()

        self.superuser = CustomUser.objects.create(
            username="superuser", email="superuser@mail.ru"
        )
        self.superuser.set_password("12345678")
        self.superuser.save()

        self.habit_data = {
            "place": "дом",
            "start_time": "05:25:00",
            "action": "убраться",
            "reward": "полежать на диване",
            "time_to_complete": "00:02:00",
            "is_public": "True",
            "owner": self.habit_owner.id,
        }
        self.habit = Habits.objects.create(
            place="дом",
            start_time="05:25:00",
            action="убраться",
            reward="полежать на диване",
            time_to_complete="00:02:00",
            is_public="True",
            owner=self.habit_owner,
        )

        Habits.objects.filter(
            place="дом",
            start_time="05:25:00",
            action="убраться",
            reward="полежать на диване",
            time_to_complete="00:02:00",
            is_public="True",
            owner=self.habit_owner,
        ).update(place="гараж")
        self.update_habit = Habits.objects.get(
            place="гараж",
            start_time="05:25:00",
            action="убраться",
            reward="полежать на диване",
            time_to_complete="00:02:00",
            is_public="True",
            owner=self.habit_owner,
        )
        self.update_data_habit = {
            "place": "гараж",
            "start_time": "05:25:00",
            "action": "убраться",
            "reward": "полежать на диване",
            "time_to_complete": "00:02:00",
            "is_public": "True",
            "owner": self.habit_owner.id,
        }

    def test_create_habit(self):
        request = self.factory.post("habits/", data=self.habit_data)

        force_authenticate(request, user=self.habit_owner)
        response = HabitsViewSet.as_view({"post": "create"})(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(Habits.objects.filter(place="дом").exists())

    def test_retrieve_habit(self):
        request = self.factory.get(f"habits/{self.habit.id}/", json=self.habit)
        force_authenticate(request, user=self.habit_owner)
        response = HabitsViewSet.as_view({"get": "retrieve"})(request, pk=self.habit.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_habit_with_root(self):
        request = self.factory.put(
            f"habits/{self.habit.id}/", data=self.update_data_habit
        )
        force_authenticate(request, user=self.habit_owner)
        response = HabitsViewSet.as_view({"put": "update"})(request, pk=self.habit.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Habits.objects.filter(place="гараж").exists())

    def test_update_habit_without_root(self):
        request = self.factory.put(
            f"habits/{self.habit.id}/", data=self.update_data_habit
        )
        force_authenticate(request, user=self.normal_user)
        response = HabitsViewSet.as_view({"put": "update"})(request, pk=self.habit.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_habit(self):
        request = self.factory.delete(f"habits/{self.habit.id}/", json=self.habit)
        force_authenticate(request, user=self.habit_owner)
        response = HabitsViewSet.as_view({"delete": "destroy"})(
            request, pk=self.habit.id
        )
        self.update_habit.delete()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Habits.objects.all().exists())
