from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """Only admin users can access"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class ProjectAccessPermission(permissions.BasePermission):
    """Control access to projects based on user role"""
    
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
    """Control access to tasks with member edit and manager verification"""
    
    def has_object_permission(self, request, view, obj):
        
        if request.user.role == 'admin':
            return True
        
        if request.user.role == 'manager':
            if request.method in permissions.SAFE_METHODS:
                return obj.project.assigned_to.filter(id=request.user.id).exists()
            
            if request.method in ['PUT', 'PATCH', 'DELETE']:
                return obj.project.assigned_to.filter(id=request.user.id).exists()
            
            if request.method == 'POST' and 'verify' in request.path:
                return obj.project.assigned_to.filter(id=request.user.id).exists()
            
            return False
        if request.user.role == 'member':
        
            if request.method in permissions.SAFE_METHODS:
                return obj.assigned_to.id == request.user.id
            
            if request.method in ['PUT', 'PATCH']:
                return obj.assigned_to.id == request.user.id
            
            if request.method == 'DELETE':
                return False
            
            return False
        
        return False