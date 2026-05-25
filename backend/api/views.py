from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import User, Project, Task
from .serializers import UserSerializer, ProjectSerializer, TaskSerializer
from .permissions import IsAdmin, ProjectAccessPermission, TaskAccessPermission

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()  #
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsAdmin]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
    
    def get_queryset(self):
        if self.request.user.role == 'admin':
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)
    
    @action(detail=False, methods=['get', 'patch'])
    def profile(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        
        elif request.method == 'PATCH':
            serializer = self.get_serializer(request.user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()  
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.role == 'admin':
            return Project.objects.all()
        else:
            return Project.objects.filter(assigned_to=user)
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, ProjectAccessPermission]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['get'])
    def tasks(self, request, pk=None):
        project = self.get_object()
        tasks = project.tasks.all()
        
        if request.user.role == 'member':
            tasks = tasks.filter(assigned_to=request.user)
        
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()  
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.role == 'admin':
            return Task.objects.all()
        elif user.role == 'manager':
            return Task.objects.filter(project__assigned_to=user)
        else:  
            return Task.objects.filter(assigned_to=user)
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, TaskAccessPermission]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def mark_complete(self, request, pk=None):
        task = self.get_object()
        task.status = 'completed'
        task.save()
        
        serializer = self.get_serializer(task)
        return Response(serializer.data)

class DashboardViewSet(viewsets.GenericViewSet):
    queryset = Project.objects.none()  
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        user = request.user
        
        if user.role == 'admin':
            projects = Project.objects.all()
            tasks = Task.objects.all()
            users = User.objects.all()
        elif user.role == 'manager':
            projects = Project.objects.filter(assigned_to=user)
            tasks = Task.objects.filter(project__assigned_to=user)
            users = User.objects.filter(assigned_projects__in=projects).distinct()
        else:  
            projects = Project.objects.filter(assigned_to=user)
            tasks = Task.objects.filter(assigned_to=user)
            users = User.objects.filter(id=user.id)
        
        data = {
            'total_projects': projects.count(),
            'total_tasks': tasks.count(),
            'completed_tasks': tasks.filter(status='completed').count(),
            'pending_tasks': tasks.filter(status='pending').count(),
            'in_progress_tasks': tasks.filter(status='in_progress').count(),
            'total_users': users.count(),
        }
        
        return Response(data)