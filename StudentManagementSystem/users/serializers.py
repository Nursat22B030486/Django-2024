from rest_framework import serializers
from users.models import User


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')

    extra_kwargs = {
        'first_name': {'required': True, 'allow_blank': False},
        'last_name': {'required': True, 'allow_blank': False},
        'email': {'required': True, 'allow_blank': False},
        'password': {'required': True, 'allow_blank': False},
    }

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username')