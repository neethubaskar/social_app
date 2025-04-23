
from rest_framework import serializers
from users.models import User
from friends.models import FriendRequest

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['id', 'sender', 'receiver', 'status', 'created_on']
        read_only_fields = ['sender', 'status', 'created_on']


class FriendSuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'bio', 'profile_picture']
