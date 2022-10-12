from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import password_validation
from rest_framework.exceptions import ValidationError


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
        )
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=150)


class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, max_length=255)

    def validate(self, attrs):
        try:
            password_validation.validate_password(attrs['password'])
        except ValidationError:
            raise ValidationError('error')
        return attrs


class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'old_password',
            'new_password',
        )
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
