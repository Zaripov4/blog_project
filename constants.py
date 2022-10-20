from django.conf import settings

home_url = settings.BASE_URL
password_reset_url = home_url + 'account/password_reset_confirm/'
password_reset_msg = 'Password reset link {}{}/'
password_reset_theme = 'Password reset'
activation_code_url = home_url + 'account/{}/activate/?code={}'
activation_code_theme = 'Activate Profile'
activation_code_msg = 'Activate you profile with this link {}{}/'
