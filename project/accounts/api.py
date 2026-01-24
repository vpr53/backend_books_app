from ninja import Router
from ninja.errors import HttpError
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

from accounts.models import User
from accounts.schema import (
    RegisterSchema, 
    LoginSchema,
    AcsessRefrashSchema,
    ErrorSchema,
    SuccessfulSchema,
    )
from .utils import send_action_email
from ninja.security import django_auth

from ninja_jwt.tokens import RefreshToken
from ninja_jwt.schema_control import SchemaControl

from ninja_jwt.settings import api_settings
from ninja_extra import api_controller
from ninja_jwt.controller import TokenObtainPairController

api = Router(tags=["Auth"])



@api.post(
        "/register/",
        response={201: SuccessfulSchema, 409: ErrorSchema}
    )
def register(request, payload: RegisterSchema):

    if User.objects.filter(email=payload.email).exists():
        raise HttpError(409, "Email already registered")

    user = User.objects.create_user(
        **payload.dict(),
        is_active=False,
    )

    send_action_email(
        user=user,
        request=request,
        path="/api/v1/auth/verify-email", 
        subject="Подтвердите регистрацию",
        template="emails/verify_email.html",
        msg="Если вы не регистрировались — просто проигнорируйте письмо.",
    )

    return 201, {"detail": "Check your email to verify account"}


@api.get(
    "/verify-email/",
    response={
        200: SuccessfulSchema,
        400: ErrorSchema,
    },
    summary="Подтверждение email",
    description="Проверяет ссылку подтверждения email и активирует пользователя"
)
def verify_email(request, uid: str, token: str):
    try:
        user_id = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=user_id)
    except (User.DoesNotExist, ValueError, TypeError):
        raise HttpError(400, "Invalid verification link")

    if not default_token_generator.check_token(user, token):
        raise HttpError(400, "Invalid or expired token")

    if user.is_active:
        return {"detail": "Email already verified"}

    user.is_active = True
    user.save(update_fields=["is_active"])

    return {"detail": "Email successfully verified"}


@api.post("/login/", response={200: AcsessRefrashSchema, 400: ErrorSchema})
def login(request, payload: LoginSchema):
    user = authenticate(request, username=payload.email, password=payload.password)
    if not user:
        raise HttpError(400, "Email or password not valid")
    

    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

