from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class ProjectAccessPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
      
        if request.user.role == 'admin':
            return True
        
        if request.method in permissions.SAFE_METHODS:
            return obj.assigned_to.filter(id=request.user.id).exists()
        
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            if request.user.role == 'manager':
                return obj.assigned_to.filter(id=request.user.id).exists()
            return False
        
        return False

class TaskAccessPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        
        if request.method in permissions.SAFE_METHODS:
            if request.user.role == 'manager':
                return obj.project.assigned_to.filter(id=request.user.id).exists()
            elif request.user.role == 'member':
                return obj.assigned_to.id == request.user.id
            return False
        
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            if request.user.role == 'manager':
                return obj.project.assigned_to.filter(id=request.user.id).exists()
            return False
        
        return False