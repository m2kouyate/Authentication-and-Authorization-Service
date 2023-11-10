import phonenumbers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers, exceptions
from django.contrib.auth import get_user_model, authenticate
from phonenumbers import parse as parse_phone, is_valid_number
from django.utils.translation import gettext_lazy as _
from .models import UserProfile, CustomUser

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'is_property_owner', 'is_admin')


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ('user', 'photo', 'phone_number', 'additional_info', 'created_at', 'modified_at')

    def validate_phone_number(self, value):
        try:
            phone_number = parse_phone(value, None)  # Парсинг без указания страны
        except phonenumbers.NumberParseException:
            raise serializers.ValidationError("Invalid phone number format.")

        if not is_valid_number(phone_number):
            raise serializers.ValidationError("The phone number entered is not valid.")

        return value

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        user_profile, created = UserProfile.objects.update_or_create(user=user, defaults=validated_data)
        return user_profile


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    profile = UserProfileSerializer(required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password', 'password2', 'profile']

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password2': _("Password fields didn't match.")})

        try:
            validate_password(data['password'])
        except ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})

        return data

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, **profile_data)
        # Token.objects.create(user=user)
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user is None:
            raise serializers.ValidationError(_("Invalid login credentials"))
        return data





