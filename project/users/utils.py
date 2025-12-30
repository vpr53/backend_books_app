from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse

from .tokens import email_verification_token



def send_verification_email(user, request):
    token = email_verification_token.make_token(user)

    verify_url = request.build_absolute_uri(
        reverse("verify-email") + f"?uid={user.pk}&token={token}"
    )

    send_mail(
        subject="подтвердите email",
        message=f"Перейдите по ссылке для подтверждения:\n{verify_url}", 
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )