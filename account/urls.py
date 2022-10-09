from django.urls import path, include
from rest_framework.routers import SimpleRouter

from account.api import UserViewSet
from account.views import ChangePasswordView, PasswordResetConfirmAPIView, \
      PasswordResetAPIView

router = SimpleRouter()
router.register('', UserViewSet)


urlpatterns = [
      path('', include(router.urls)),
      path('password_change/', ChangePasswordView.as_view(),
           name='change_password'),
      path('password_reset/', PasswordResetAPIView.as_view(),
           name='password_reset_email_send'),
      path('password_reset_confirm/<uuid:code>/',
           PasswordResetConfirmAPIView.as_view(),
           name='password_reset_confirm'),
]
