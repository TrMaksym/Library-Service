from django.urls import path
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView, TokenVerifyView

from .views import ManageUserView, UserCreateView

app_name = "user"
urlpatterns = [
    path("", UserCreateView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", ManageUserView.as_view(), name="me"),

    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]