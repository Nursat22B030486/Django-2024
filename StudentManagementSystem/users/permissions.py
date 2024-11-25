from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Admin'
    
class IsTeacher(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Teacher'


class IsStudent(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'Student'
    
class IsSelfOrAdmin(permissions.BasePermission):
    """
    Allows access to self or admin for Student profile.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the user is an admin or trying to access their own profile
        return request.user.is_authenticated and (request.user == obj.user or request.user.role == 'Admin')