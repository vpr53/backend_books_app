import secrets
from abc import ABC
from urllib.parse import urlencode

from django.conf import settings
from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.timezone import now

from core.domain.accounts.entity import User
from core.domain.accounts.service import BaseTokenSenderService
from core.domain.accounts.value_objects import Token


class BaseEmailTokenSenderService(BaseTokenSenderService, ABC):
    path: str = ""
    template: str = ""
    subject: str = ""
    msg: str = ""

    def send_token(self, email: str, user_id: str, token: Token) -> None:
        query = urlencode({"uid": user_id, "token": token.value})
        action_url = f"{settings.BASE_URL}{self.path}?{query}"

        context = {"action_url": action_url, "year": now().year, "msg": self.msg}

        text_content = f"{self.subject}\n\n{action_url}\n\n{self.msg}"
        html_content = render_to_string(self.template, context)

        email_message = EmailMultiAlternatives(
            subject=self.subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )

        email_message.attach_alternative(html_content, "text/html")
        email_message.send(fail_silently=False)

    def generate_and_save_token(self, user: User) -> Token:
        token = Token(secrets.token_urlsafe(32))
        cache.set(f"user_token:{user.user_id}", token, timeout=3600)
        return token

    def check_token(self, user: User, token: Token) -> bool:
        cache_token = cache.get(f"user_token:{user.user_id}")
        return cache_token == token


class EmailVerifySenderService(BaseEmailTokenSenderService):
    path = "/api/auth/verify-email"
    template = "emails/verify_email.html"
    subject = "Подтвердите регистрацию"
    msg = "Если вы не регистрировались — просто проигнорируйте письмо."


class VerifyPasswordSenderService(BaseEmailTokenSenderService):
    path = "/api/auth/password-reset/confirm"
    template = "emails/password_reset.html"
    subject = "Сброс пароля"
    msg = "Если вы не запрашивали сброс пароля — проигнорируйте письмо."
