import uuid
from constants import (
    password_reset_theme,
    password_reset_msg,
    password_reset_url,
    activation_code_url,
    activation_code_theme,
)
from django.conf import settings
from django.core.mail import send_mail
from account.models import ResetCode, ActivationCode


def send_password_reset(*, user):
    code = uuid.uuid4()
    ResetCode.objects.create(user=user, code=code)
    message = password_reset_msg.format(password_reset_url, code)
    send_mail(
        password_reset_theme,
        message, settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False
    )


def send_activation_code(*, user):
    code = uuid.uuid4()
    ActivationCode.objects.create(user=user, code=code)
    message = activation_code_url.format(user.id, code)
    send_mail(
        activation_code_theme,
        message, settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False
    )
