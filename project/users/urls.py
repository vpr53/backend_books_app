from django.urls import path
from .views import RegisterView, MeView, VerifyEmailView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),  # email + password
    path("token/refresh/", TokenRefreshView.as_view(), name="token/refresh"),
    path("logout/", TokenBlacklistView.as_view(), name="logout"),
    path("profile/", MeView.as_view(), name="profile"),
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
]
