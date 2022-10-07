from django.contrib.auth import get_user_model
from rest_framework import serializers

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
