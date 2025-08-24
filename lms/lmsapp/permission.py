from rest_framework import permissions


class IsEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        profile = request.user.user_profile.first()
        if not profile:
            return False
        return profile.role == "employee" or request.user.is_superuser
       
    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return (
            hasattr(request.user, "user_profile") and request.user.user_profile.role == "employee"
        ) or request.user.is_superuser or obj.user == request.user

class PermissionMixin:

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated, IsEmployee]
        return [permission() for permission in permission_classes]