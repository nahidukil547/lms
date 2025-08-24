from rest_framework import permissions

class IsEmployee(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
       
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if hasattr(obj, "role") and hasattr(obj, "is_superuser"):
            return obj.role == "employee" or obj.is_superuser
        return False
    