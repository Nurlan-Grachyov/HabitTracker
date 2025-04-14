from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenViewBase

from users.serializers import RegisterSerializer


class MyTokenObtainPairView(TokenObtainPairView, TokenViewBase):
    """
    Переопределение класса TokenObtainPairView с предоставлением доступа всем
    """

    permission_classes = [AllowAny]

    # def post(self, request, *args, **kwargs):
    #     response = super().post(request, *args, **kwargs)
    #     if response.status_code == 200:
    #         print(request.data)
    #         user = self.get_user(request.data)
    #         update_last_login(None, user)
    #     return response
    #
    # def get_user(self, validated_data):
    #     return CustomUser.objects.get(email=validated_data["email"])

class RegisterCreateAPIView(generics.CreateAPIView):
    """
    Класс регистрации пользователя
    """

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    authentication_classes = []