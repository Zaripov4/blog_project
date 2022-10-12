from django.urls import path, include
from rest_framework.routers import SimpleRouter

from account.views import ChangePasswordView, PasswordResetConfirmView, \
    PasswordResetView, UserViewSet

router = SimpleRouter()
router.register('', UserViewSet)

urlpatterns = [
      path('', include(router.urls)),
      path('password_change/', ChangePasswordView.as_view(),
           name='change_password'),
      path('password_reset/', PasswordResetView.as_view(),
           name='password_reset_email_send'),
      path('password_reset_confirm/<uuid:code>/',
           PasswordResetConfirmView.as_view(),
           name='password_reset_confirm'),
]
