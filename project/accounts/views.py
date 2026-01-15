from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import (
    RegisterSerializer,
    PasswordResetCompleteSerializer,
    PasswordResetRequestSerializer
)
from .utils import send_action_email

class RegisterView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        send_action_email(
            user=user,
            request=request,
            path="verify-email",
            subject="Подтвердите регистрацию",
            template="emails/verify_email.html",
            msg="Если вы не регистрировались — проигнорируйте письмо.",
        )

        return Response(
            {"detail": "Check your email to verify account"},
            status=status.HTTP_201_CREATED,
        )


class VerifyEmailView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        uid = request.query_params.get("uid")
        token = request.query_params.get("token")

        if not uid or not token:
            return Response(
                {"detail": "Invalid verification link"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = get_object_or_404(User, pk=uid)

        if user.is_email_verified:
            return Response(
                {"detail": "Email already verified"}, status=status.HTTP_200_OK
            )

        if not default_token_generator.check_token(user, token):
            return Response(
                {"detail": "Invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.is_email_verified = True
        user.is_active = True
        user.save()

        return Response(
            {"detail": "Email successfully verified"}, status=status.HTTP_200_OK
        )


class PasswordResetRequestView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = User.objects.filter(email=email).first()

        if user:
            send_action_email(
                user=user,
                request=request,
                path="password-reset-confirm",
                subject="Сброс пароля",
                template="emails/password_reset.html",
                msg="Если вы не запрашивали смену пароля — просто проигнорируйте письмо.",
            )

        return Response(
            {"detail": "If account exists, email was sent"},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        uid = request.query_params.get("uid")
        token = request.query_params.get("token")

        if not uid or not token:
            return Response(
                {"detail": "Invalid link"}, status=status.HTTP_400_BAD_REQUEST
            )

        user = get_object_or_404(User, pk=uid)

        if not default_token_generator.check_token(user, token):
            return Response(
                {"detail": "Invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({"detail": "Token valid"}, status=status.HTTP_200_OK)


class PasswordResetCompleteView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = PasswordResetCompleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uid = serializer.validated_data["uid"]
        token = serializer.validated_data["token"]
        new_password = serializer.validated_data["new_password"]

        user = get_object_or_404(User, pk=uid)

        if not default_token_generator.check_token(user, token):
            return Response(
                {"detail": "Invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save()

        return Response({"detail": "Password successfully updated"}, status=status.HTTP_200_OK)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {"id": request.user.id, "email": request.user.email},
            status=status.HTTP_200_OK,
        )
