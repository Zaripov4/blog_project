from rest_framework import serializers, validators
from django.contrib.auth.models import User


def create(validated_data):
    username = validated_data.get('username')
    password = validated_data.get('password')
    email = validated_data.get('email')
    first_name = validated_data.get('first_name')
    last_name = validated_data.get('last_name')

    user = User.objects.create(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name
    )

    return user


class RegisterUser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = {'username', 'password', 'email', 'firstname', 'lastname'}

        extra_kwargs = {
            'password': {'write only': True},
            'email': {
                'required': True,
                'allow blank': False,
                'validators': {
                    validators.UniqueValidator(
                        User.objects.all(), 'A user with this email already exists'
                    )
                }
            }
        }
