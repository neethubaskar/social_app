from django.urls import path
from friends.v1.views import (
    FriendSuggestionsView,
    SendFriendRequestView,
    ManageFriendRequestView,
    ListFriendsView,
)


urlpatterns = [
    path('suggestions/', FriendSuggestionsView.as_view(), name='friend-suggestions'),
    path('send-request/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('friend-requests/', ManageFriendRequestView.as_view(), name='received-requests'),
    path('request/<int:pk>/respond/', ManageFriendRequestView.as_view(), name='manage-request'),
    path('list/', ListFriendsView.as_view(), name='list-friends'),
]
