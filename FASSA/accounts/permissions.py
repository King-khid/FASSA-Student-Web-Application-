from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsSuperAdmin(BasePermission):
    """Allows access only to Super Admins."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'SUPERADMIN'


class IsAdmin(BasePermission):
    """Allows access to Admins and Super Admins."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['ADMIN', 'SUPERADMIN']


class IsStudent(BasePermission):
    """Allows access only to Students."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'STUDENT'


class ReadOnly(BasePermission):
    """Allows read-only access for unauthenticated users (GET, HEAD, OPTIONS)."""
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
