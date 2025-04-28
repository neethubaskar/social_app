import re
import requests
from rest_framework import serializers
from django.core.validators import validate_email
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from users.validators import validate_email_format, validate_strong_password


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'confirm_password']

    def validate_email(self, value):
        """Use shared email validator."""
        return validate_email_format(value)

    def validate_password(self, value):
        """Use shared strong password validator."""
        return validate_strong_password(value)

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for login via email and password."""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError({"detail": "Invalid credentials."})
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'email': user.email,
        }


class GoogleAuthSerializer(serializers.Serializer):
    access_token = serializers.CharField()

    def validate(self, attrs):
        access_token = attrs.get("access_token")
        # Call Google UserInfo API
        user_info_response = requests.get(
            'https://www.googleapis.com/oauth2/v2/userinfo',
            # 'https://openidconnect.googleapis.com/v1/userinfo',
            headers={'Authorization': f'Bearer {access_token}'}
        )

        if user_info_response.status_code != 200:
            raise serializers.ValidationError({"access_token": "Invalid Google access token."})

        user_info = user_info_response.json()

        email = user_info.get("email")
        name = user_info.get("name")

        if not email:
            raise serializers.ValidationError({"email": "Email not found in Google response."})

        # Get or create user
        user, created = User.objects.get_or_create(email=email, defaults={"name": name})

        refresh = RefreshToken.for_user(user)

        return {
            "email": user.email,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile, email, and password."""
    password = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField(required=False)

    class Meta:
        model = User
        fields = ['name', 'bio', 'profile_picture', "location", "birth_date", 'email', 'password']

    def validate_email(self, value):
        return validate_email_format(value)

    def validate_password(self, value):
        return validate_strong_password(value)

    def update(self, instance, validated_data):
        if 'email' in validated_data:
            instance.email = validated_data['email']

        if 'password' in validated_data:
            instance.set_password(validated_data['password'])

        instance.name = validated_data.get('name', instance.name)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.profile_picture = validated_data.get('profile_picture', instance.profile_picture)
        instance.bio = validated_data.get('birth_date', instance.birth_date)
        instance.bio = validated_data.get('location', instance.location)

        instance.save()
        return instance


class UserListSerializer(serializers.ModelSerializer):
    """Serializer for listing users (excluding self)."""

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'bio', 'profile_picture', "location", "birth_date"]
