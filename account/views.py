import uuid
import constants
from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import User, ResetCode
from .serializers import UserSerializer, PasswordResetSerializer
from rest_framework.views import APIView


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

    @action(methods=['get'], detail=False, url_path='@men')
    def me(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
