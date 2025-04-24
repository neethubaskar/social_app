import random
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q

from friends.models import FriendRequest
from users.models import User
from friends.v1.serializers import FriendRequestSerializer, FriendSuggestionSerializer
from core.utils.common import api_response
from core.utils.pagination import UserListPagination


class FriendSuggestionsView(generics.ListAPIView):
    """
    get:
    Returns a paginated list of suggested users to befriend, 
    excluding the current user and their existing friends.
    Supports optional search filtering by name.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = FriendSuggestionSerializer
    pagination_class = UserListPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        try:
            user = self.request.user
            friends = FriendRequest.objects.filter(
                Q(sender=user) | Q(receiver=user),
                status='accepted'
            ).values_list('sender', 'receiver')

            friend_ids = set()
            for sender, receiver in friends:
                friend_ids.add(sender if receiver == user.id else receiver)

            exclude_ids = list(friend_ids) + [user.id]
            return User.objects.exclude(id__in=exclude_ids)
        except Exception as e:
            return []
        


class SendFriendRequestView(APIView):
    """
    post:
    Sends a friend request to another user.

    Request body must include:
    - receiver: User ID of the person to send request to
    Restrictions:
    - Cannot send to self
    - Cannot duplicate requests
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            receiver_id = request.data.get('receiver')
            if not receiver_id:
                return api_response(False, "Receiver ID is required.", status_code=400)
            if int(receiver_id) == request.user.id:
                return api_response(False, "Cannot send request to yourself.", status_code=400)
            if FriendRequest.objects.filter(sender=request.user, receiver_id=receiver_id).exists():
                return api_response(False, "Friend request already sent.", status_code=400)

            friend_request = FriendRequest.objects.create(sender=request.user, receiver_id=receiver_id)
            serialized = FriendRequestSerializer(friend_request).data
            return api_response(True, "Friend request sent successfully.", serialized, status_code=200)
        except ValueError:
            return api_response(False, "Receiver ID must be a valid number.", status_code=400)
        except Exception as e:
            return api_response(False, "An unexpected error occurred.", status_code=500)


class ManageFriendRequestView(APIView):
    """
     get:
    List all friend requests received by the logged-in user.

    patch:
    Accept or reject a friend request.
    Request body must include:
    - status: 'accepted' or 'rejected'
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            requests = FriendRequest.objects.filter(receiver=request.user, status='pending')
            serialized = FriendRequestSerializer(requests, many=True).data
            return api_response(True, "Friend requests received.", serialized)
        except Exception as e:
            logger.error(f"Error retrieving received requests: {str(e)}")
            return api_response(False, "An unexpected error occurred.", status_code=500)

    def patch(self, request, pk):
        try:
            try:
                friend_request = FriendRequest.objects.get(pk=pk)
            except FriendRequest.DoesNotExist:
                return api_response(False, "Friend request not found.", status_code=404)

            if friend_request.receiver != request.user:
                return api_response(False, "Unauthorized to update this request.", status_code=403)

            new_status = request.data.get('status')
            if new_status not in ['accepted', 'rejected']:
                return api_response(False, "Invalid status value.", status_code=400)

            friend_request.status = new_status
            friend_request.save()
            serialized = FriendRequestSerializer(friend_request).data
            return api_response(True, f"Friend request {new_status}.", serialized)
        except Exception as e:
            return api_response(False, "An unexpected error occurred.", status_code=500)



class ListFriendsView(generics.ListAPIView):
    """
    get:
    Lists all friends of the authenticated user (accepted friend requests only).

    Supports:
    - Search filtering by name
    - Pagination
    """
    
    permission_classes = [IsAuthenticated]
    serializer_class = FriendSuggestionSerializer
    pagination_class = UserListPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        try:
            user = self.request.user
            friend_rels = FriendRequest.objects.filter(
                Q(sender=user) | Q(receiver=user),
                status='accepted'
            )

            friend_ids = []
            for friend in friend_rels:
                friend_ids.append(friend.receiver.id if friend.sender == user else friend.sender.id)

            return User.objects.filter(id__in=friend_ids)
        except Exception as e:
            return []
