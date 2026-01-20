from ninja import Router
from ninja.errors import HttpError
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

from accounts.models import User
from accounts.schema import RegisterSchema
from .utils import send_action_email


api = Router(tags=["Auth"])


@api.post("/register/")
def register(request, payload: RegisterSchema):

    if User.objects.filter(email=payload.email).exists():
        raise HttpError(400, "Email already registered")

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

    return {"detail": "Check your email to verify account"}


@api.get("/verify-email/")
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
