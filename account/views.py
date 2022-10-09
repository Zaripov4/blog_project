import uuid
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import User, ResetCode
from .serializers import UserSerializer, PasswordResetSerializer, \
    ChangePasswordSerializer, PasswordResetConfirmSerializer
from rest_framework.views import APIView
from blog import settings
from django.core.mail import send_mail


home_url = 'adminsite249@gmail.com'
password_reset_url = home_url + 'password_reset_confirm/'
password_reset_msg = 'Password reset link {}{}'
password_reset_theme = 'Password reset'


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        return super(UserViewSet, self).get_permissions()

    def perform_create(self, serializer):
        super(UserViewSet, self).perform_create(serializer)
        user = serializer.instance
        user.set_password(serializer.validated_data['password'])
        user.save(update_fields=['password'])

    @action(methods=['get'], detail=False, url_path='@me')
    def me(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


def send_password_reset(email):
    print(email)
    user = get_user_model().objects.filter(email=email).all()
    print(user)
    if not user.exists():
        return

    user = user.first()
    code = uuid.uuid4()
    ResetCode.objects.create(user=user, code=code)
    message = password_reset_msg.format(password_reset_url, code)
    send_mail(password_reset_theme, message, settings.EMAIL_HOST_USER,
              [email], fail_silenty=False)


class PasswordResetAPIView(APIView):
    """Password reset api to send a reset link to email"""
    permission_classes = [AllowAny, ]

    @action(detail=False, methods=['post'])
    def password_reset(self, request, *args, **kwargs):
        data = request.data
        serialized = PasswordResetSerializer(data=data)
        if not serialized.is_valid():
            return Response(serialized.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        email = serialized.data.get("email")
        send_password_reset(email)
        return Response({"email": email,
                         "message": "Password reset link sent to your email"},
                        status=status.HTTP_200_OK)


class PasswordResetConfirmAPIView(APIView):
    """Password reset complete url=/reset/<uuid:code>/"""
    permission_classes = [AllowAny, ]

    @action(methods=['put'], detail=False,)
    def reset_confirm(self, request, *args, **kwargs):
        data = request.data
        serialized = PasswordResetConfirmSerializer(data=data)
        if serialized.is_valid():
            code = kwargs.get('code', None)
            password = serialized.data.get('password')
            obj = get_object_or_404(ResetCode, code=code)
            user = obj.user
            obj.delete()
            user.set_password(password)
            user.save()
            return Response({"msg": "password has been changed successfully",
                             "email": user.email},
                            status=status.HTTP_200_OK)
        return Response(serialized.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.UpdateAPIView):
    """Password change view requires auth"""
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(
                    serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
