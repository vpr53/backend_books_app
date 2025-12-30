from django.shortcuts import get_object_or_404
from rest_framework import generics
from .serializers import RegisterSerializer
from .models import User
from .tokens import email_verification_token
from .utils import send_verification_email
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken



class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        send_verification_email(user, request)

        return Response(
            {"detail": "Check your email to verify account"},
            status=status.HTTP_201_CREATED
        )



class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "id": request.user.id,
            "email": request.user.email
        })


class VerifyEmailView(APIView):
    authentication_classes = []  # ❗ не нужен логин
    permission_classes = []

    def get(self, request):
        uid = request.query_params.get("uid")
        token = request.query_params.get("token")

        if not uid or not token:
            return Response(
                {"detail": "Invalid verification link"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = get_object_or_404(User, pk=uid)

        if user.is_email_verified:
            return Response(
                {"detail": "Email already verified"},
                status=status.HTTP_200_OK
            )

        if not email_verification_token.check_token(user, token):
            return Response(
                {"detail": "Invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.is_email_verified = True
        user.is_active = True
        user.save()

        return Response(
            {"detail": "Email successfully verified"},
            status=status.HTTP_200_OK
        )
