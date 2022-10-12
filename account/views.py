from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import User, ResetCode, ActivationCode
from .serializers import (
    UserSerializer,
    PasswordResetSerializer,
    ChangePasswordSerializer,
    PasswordResetConfirmSerializer,
)
from rest_framework.views import APIView
from .mail import send_password_reset, send_activation_code


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    serializer_class2 = ChangePasswordSerializer
    queryset = User.objects.all()
    model = User
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        if self.action in ['activate', 'create', 'password_reset',
                           'password_reset_confirm', 'change_password']:
            self.permission_classes = [AllowAny]
        return super(UserViewSet, self).get_permissions()

    def perform_create(self, serializer):
        super(UserViewSet, self).perform_create(serializer)
        user = serializer.instance
        user.set_password(serializer.validated_data['password'])
        user.save(update_fields=['password'])
        send_activation_code(user=user)

    @action(methods=['get'], detail=False, url_path='@me')
    def me(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='activate')
    def activate_account(self, request, *args, **kwargs):
        code = request.query_params.get('code')
        if code:
            obj = get_object_or_404(ActivationCode, code=code)
            user = obj.user
            obj.delete()
            user.is_active = True
            user.save()
            return Response(
                {'message': 'Email Verified'}, status=status.HTTP_200_OK
            )


class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        serialized = PasswordResetSerializer(data=data)
        if not serialized.is_valid():
            return Response(
                serialized.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        email = serialized.data.get("email")
        user = get_object_or_404(User, email=email)
        send_password_reset(user=user)
        return Response(
            {
                "email": email,
                "message": "Password reset link sent to your email"
            },
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serialized = PasswordResetConfirmSerializer(data=request.data)
        if serialized.is_valid():
            code = kwargs.get('code', None)
            password = serialized.data.get('password')
            obj = get_object_or_404(ResetCode, code=code)
            user = obj.user
            obj.delete()
            user.set_password(password)
            user.save()
            return Response(
                {
                    "message": "password has been changed successfully",
                    "email": user.email
                },
                status=status.HTTP_200_OK)
        return Response(serialized.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = ChangePasswordSerializer
    model = User

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
