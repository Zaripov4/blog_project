import uuid

from django.conf import settings
from django.core.mail import send_mail

from account.models import ResetCode, ActivationCode

home_url = settings.BASE_URL
password_reset_url = home_url + 'account/password_reset_confirm/'
password_reset_msg = 'Password reset link {}{}/'
password_reset_theme = 'Password reset'
activation_code_url = home_url + 'account/{}/activate/?code={}'
activation_code_theme = 'Activate Profile'
activation_code_msg = 'Activate you profile with this link {}{}/'


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
