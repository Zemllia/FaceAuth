from django.contrib.auth.models import AnonymousUser

from FaceAuth.models import Camera
from django.http import HttpResponseForbidden, HttpResponse


class TokenAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        token_header = request.META.get('HTTP_AUTHORIZATION', None)
        request.camera = None
        if token_header:
            try:
                _, api_key = token_header.split(' ')
            except:
                return HttpResponse("Wrong token format, please use next format: Token <token>")
            try:
                camera = Camera.objects.get(api_key=api_key)
            except Camera.DoesNotExist:
                pass
            else:
                request.camera = camera

        response = self.get_response(request)
        return response
