from rest_framework.permissions import BasePermission

from habits.models import Habits


class Owner(BasePermission):
    """
    Проверка на права доступа. Вернет True, если пользователь, совершающий операцию, является владельцем объекта
    """

    def has_object_permission(self, request, view, obj):
        if request.method in ("GET", "PUT", "PATCH", "DELETE"):
            return request.user == obj.owner or request.user.is_superuser
        return False


class ListHabits(BasePermission):
    """
    Проверка права доступа. Возвращает все публичные привычки
    """

    def has_permission(self, request, view):
        if request.method in ("GET",):
            return True
        return False
