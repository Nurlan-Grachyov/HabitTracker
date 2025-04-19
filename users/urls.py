from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .apps import UsersConfig
from .views import MyTokenObtainPairView, RegisterCreateAPIView

app_name = UsersConfig.name


urlpatterns = [
    path("login/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterCreateAPIView.as_view(), name="register"),
]
