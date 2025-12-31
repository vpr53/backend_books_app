from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.timezone import now
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse


def send_verification_email(user, request):
    token = default_token_generator.make_token(user)
    uid = user.pk

    verify_url = request.build_absolute_uri(
        reverse("verify-email") + f"?uid={uid}&token={token}"
    )

    subject = "Подтверждение email"
    from_email = settings.DEFAULT_FROM_EMAIL
    to = [user.email]

    context = {
        "verify_url": verify_url,
        "year": now().year,
    }

    text_content = f"""
Подтвердите email:

{verify_url}

Если вы не регистрировались — проигнорируйте письмо.
"""

    html_content = render_to_string(
        "emails/verify_email.html",
        context
    )

    email = EmailMultiAlternatives(
        subject,
        text_content,
        from_email,
        to
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
