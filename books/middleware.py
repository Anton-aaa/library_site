from django.utils.deprecation import MiddlewareMixin
from datetime import datetime
from django.utils import timezone
import json
from re import sub
from rest_framework.authtoken.models import Token

class LastActionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        now = datetime.utcnow()
        request.session['last_action'] = json.dumps(now.strftime('%Y-%m-%dT%H:%M:%S'))


class MyMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)


    def getUsername(self, request):
        header_token = request.META.get('HTTP_AUTHORIZATION', None)
        if header_token is not None:
            try:
                token = sub('Token ', '', header_token)
                token_obj = Token.objects.get(key=token)
            except Token.DoesNotExist:
                pass
        return token_obj.user.username