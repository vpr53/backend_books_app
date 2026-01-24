from urllib.parse import urlencode
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.timezone import now
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings


def send_action_email(
    *,
    user,
    request,
    path: str,         
    subject: str,
    template: str,
    msg: str,
    params: dict | None = None,
):
    if params is None:
        params = {}

    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    query = urlencode({**params, "uid": uid, "token": token})

    # исправлено: ? вместо &
    action_url = f"{request.build_absolute_uri(path)}?{query}"

    context = {
        "action_url": action_url,
        "year": now().year,
        "msg": msg,
    }

    text_content = f"{subject}\n\n{action_url}\n\n{msg}"
    html_content = render_to_string(template, context)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    email.attach_alternative(html_content, "text/html")
    email.send(fail_silently=False)
