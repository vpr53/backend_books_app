from django.urls import path
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import MeView, RegisterView, VerifyEmailView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),  # email + password
    path("token/refresh/", TokenRefreshView.as_view(), name="token/refresh"),
    path("logout/", TokenBlacklistView.as_view(), name="logout"),
    path("profile/", MeView.as_view(), name="profile"),
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
]
