from django.urls import path
from .views import RegisterView, MeView, VerifyEmailView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", TokenObtainPairView.as_view()),  # email + password
    path("token/refresh/", TokenRefreshView.as_view()),
    path("logout/", TokenBlacklistView.as_view()),
    path("profile/", MeView.as_view()),
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
]
