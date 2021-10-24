from rest_framework.permissions import BasePermission


class IsCamera(BasePermission):
    def has_permission(self, request, view):
        if getattr(request, 'camera') and request.camera:
            return True
        return False