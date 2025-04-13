from django.urls import path

from .apps import UsersConfig
from .views import MyTokenObtainPairView

app_name = UsersConfig.name

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
]