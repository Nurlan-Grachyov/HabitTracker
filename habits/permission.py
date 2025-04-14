from rest_framework.permissions import BasePermission

from habits.models import Habits


class Owner(BasePermission):
    """
    Проверка на права доступа. Вернет True, если пользователь, совершающий операцию, является владельцем объекта
    """

    def has_object_permission(self, request, view, obj):
        print("3")
        if request.method in ("GET", "PUT", "PATCH", "DELETE"):
            print("4")
            return request.user == obj.owner
        return False


class ListHabits(BasePermission):
    """
    Проверка права доступа. Возвращает все публичные привычки
    """

    def has_permission(self, request, view):
        print("3")
        if request.method in ("GET",):
            print("4")
            return Habits.objects.filter(is_public=True)
        return False
