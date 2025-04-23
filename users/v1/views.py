from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter


from users.v1.serializers import (
    RegisterSerializer, LoginSerializer, GoogleAuthSerializer, 
    UserProfileUpdateSerializer, UserListSerializer)
from core.utils.common import api_response, set_jwt_token_cookie, add_access_token_validity_cookie
from core.utils.pagination import UserListPagination
from users.models import User


class RegisterView(generics.CreateAPIView):
    """API endpoint for user registration."""
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Register a new user.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            data = {
                'id': user.id,
                'name': user.name,
                'email': user.email
            }
            return api_response(
                success=True,
                message="User registered successfully.",
                data=data,
                status_code=status.HTTP_201_CREATED
            )

        return api_response(
                success=False,
                message="Validation error.",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )


class LoginView(APIView):
    """API endpoint for user login and JWT token retrieval."""
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Authenticate user and return JWT token pair.
        """
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return api_response(
                success=False,
                message="Validation error.",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        tokens = serializer.validated_data
        response = Response(status=status.HTTP_200_OK)
        set_jwt_token_cookie(
                    response,
                    tokens,
                )
        add_access_token_validity_cookie(response)
        response.data = {'token': tokens['access'], 'user': tokens['email']}
        return response


class GoogleAuthView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = GoogleAuthSerializer(data=request.data)
        if not serializer.is_valid():
            return api_response(
                success=False,
                message="Validation error.",
                errors=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        tokens = serializer.validated_data
        response = Response(status=status.HTTP_200_OK)
        set_jwt_token_cookie(
                    response,
                    token,
                )
        add_access_token_validity_cookie(response)
        response.data = {'token': tokens['access'], user: tokens['email']}
        return response


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileUpdateSerializer(request.user)
        return api_response(True, "Profile fetched successfully.", serializer.data)

    def patch(self, request):
        serializer = UserProfileUpdateSerializer(request.user, data=request.data, partial=True)
        if not serializer.is_valid():
            return api_response(False, "Validation error.", errors=serializer.errors, status_code=400)
        serializer.save()
        return api_response(True, "Profile updated successfully.", serializer.data)


class UserListView(ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = UserListPagination
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        return User.objects.exclude(id=self.request.user.id)
