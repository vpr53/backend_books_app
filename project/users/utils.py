from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.timezone import now


def send_action_email(
    *,
    user,
    request,
    path,
    subject,
    template,
    msg,
):
    token = default_token_generator.make_token(user)
    uid = user.pk

    action_url = request.build_absolute_uri(
        reverse(path) + f"?uid={uid}&token={token}"
    )

    from_email = settings.DEFAULT_FROM_EMAIL
    to = [user.email]

    context = {
        "action_url": action_url,
        "year": now().year,
        "msg": msg,
    }

    text_content = f"""
{subject}

{action_url}

{msg}
"""

    html_content = render_to_string(template, context)

    email = EmailMultiAlternatives(
        subject,
        text_content,
        from_email,
        to
    )
    email.attach_alternative(html_content, "text/html")
    email.send()

