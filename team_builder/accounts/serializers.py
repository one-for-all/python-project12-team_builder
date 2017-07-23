import re
from django.contrib.auth import get_user_model, authenticate, login
from rest_framework import serializers

from accounts import models


class UserCreationSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError(
                'Passwords need to match'
            )
        return data

    def validate_username(self, value):
        if not re.fullmatch(r'[_\w]+', value):
            raise serializers.ValidationError(
                'Username has to consist of only letters, numbers and '
                'underscores'
            )
        try:
            get_user_model().objects.get(username=value)
        except get_user_model().DoesNotExist:
            return value
        else:
            raise serializers.ValidationError(
                'This username has been taken'
            )

    def validate_email(self, value):
        try:
            get_user_model().objects.get(email=value)
        except get_user_model().DoesNotExist:
            return value
        else:
            raise serializers.ValidationError(
                'This email has been taken'
            )

    def save(self, **kwargs):
        get_user_model().objects.create_user(
            email=self.validated_data.get('email'),
            username=self.validated_data.get('username'),
            password=self.validated_data.get('password')
        )


class UserLogInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        self.user = authenticate(
            email=data.get('email'),
            password=data.get('password')
        )
        if self.user is None:
            raise serializers.ValidationError(
                'Email or password wrong'
            )
        return data

    def save(self, **kwargs):
        login(self.context.get('request'), self.user)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ['name', 'bio', 'avatar', 'skills']

    def __init__(self, *args, **kwargs):
        if kwargs.get('data'):
            for skill in kwargs.get('data').get('skills'):
                models.Skill.objects.get_or_create(name=skill)
        super().__init__(*args, **kwargs)
