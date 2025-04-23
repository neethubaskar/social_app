from django.urls import path
from users.v1.views import (
    RegisterView, LoginView, GoogleAuthView, UserProfileView, UserListView)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('google-auth/', GoogleAuthView.as_view(), name='google-auth'),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path('users/', UserListView.as_view(), name='user-list'),
]

