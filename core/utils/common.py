from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.conf import settings


def set_jwt_token_cookie(response, token=None):
    """
    Util method to set the token in cookie
    @param response: Response object
    @param token: token to be set in cookie
    @return: None
    """
    if token['refresh']:
        expires_in = timezone.now() + settings.SIMPLE_JWT[
            'REFRESH_TOKEN_LIFETIME']

        response.set_cookie(
            key=settings.AUTH_COOKIE_REFRESH,
            value=token['refresh'],
            expires=expires_in,
            secure=settings.SESSION_COOKIE_SECURE,
            httponly=settings.SESSION_COOKIE_HTTPONLY,
            samesite=settings.SESSION_COOKIE_SAMESITE,
            domain=settings.TOKEN_COOKIE_DOMAIN,
        )


def add_access_token_validity_cookie(response):
    """
    Method for updating access token expiry cookie
    """
    expires_in = timezone.now() + settings.SIMPLE_JWT[
        'ACCESS_TOKEN_LIFETIME']
    response.set_cookie(
        key=settings.AUTH_COOKIE_ACCESS,
        value=expires_in,
        expires=expires_in,
        secure=settings.SESSION_COOKIE_SECURE,
        httponly=False,
        domain=settings.TOKEN_COOKIE_DOMAIN,
    )


def api_response(success: bool, message: str, data=None, errors=None, status_code=status.HTTP_200_OK):
    response_data = {
        "status": success,
        "message": message
    }
    if success is True:
        response_data["data"] = data
    else:
        response_data["errors"] = errors

    return Response(response_data, status=status_code)
