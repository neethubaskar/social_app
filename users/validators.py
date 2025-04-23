# users/validators.py

import re
from django.core.validators import validate_email
from rest_framework import serializers

def validate_email_format(value):
    try:
        validate_email(value)
    except serializers.ValidationError:
        raise serializers.ValidationError("Enter a valid email address.")
    return value

def validate_strong_password(value):
    if len(value) < 8:
        raise serializers.ValidationError("Password must be at least 8 characters long.")
    if not re.search(r'[A-Z]', value):
        raise serializers.ValidationError("Password must contain at least one uppercase letter.")
    if not re.search(r'\d', value):
        raise serializers.ValidationError("Password must contain at least one digit.")
    if not re.search(r'[!@#$%^&*(),.?\":{}|<>]', value):
        raise serializers.ValidationError("Password must contain at least one special character.")
    return value
