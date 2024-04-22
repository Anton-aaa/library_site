from datetime import timedelta, datetime
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.utils import timezone


class CustomTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        user, token = super().authenticate_credentials(key)
        if token.created + timedelta(hours=2) < timezone.now():
            token.delete()
            raise exceptions.AuthenticationFailed('Token expired')
        return user, token