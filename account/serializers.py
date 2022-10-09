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


class PasswordResetSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=150)


class PasswordResetConfirmSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, max_length=255)

    extra_kwargs = {
        'password': {'write_only': True, 'min_length': 8,
                     'style': {'input_type': password}}
    }

    def validate(self, attrs):
        password = attrs['password']
        if password:
            try:
                password_validation.validate_password(password, password)
            except:
                raise ValidationError('error')

        return attrs


class ChangePasswordSerializer(serializers.ModelSerializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
