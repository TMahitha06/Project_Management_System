from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q
from datetime import datetime
from .models import User, Project, Task
from .serializers import UserSerializer, ProjectSerializer, TaskSerializer, TaskVerifySerializer
from .permissions import IsAdmin, ProjectAccessPermission, TaskAccessPermission

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()  
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [AllowAny]  # Allow anyone to register
        elif self.action in ['update', 'partial_update', 'destroy']:
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
        elif request.user.role == 'manager':
            tasks = tasks.filter(project__assigned_to=request.user)
        
        verification_status = request.query_params.get('verification_status')
        if verification_status:
            tasks = tasks.filter(verification_status=verification_status)
        
        serializer = TaskSerializer(tasks, many=True, context={'request': request})
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
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def mark_complete(self, request, pk=None):
        task = self.get_object()
        user = request.user
        
        if user.role == 'member' and task.assigned_to.id != user.id:
            return Response({'error': 'You can only complete your own tasks'},
                          status=status.HTTP_403_FORBIDDEN)
        
        task.status = 'completed'
        task.completed_at = datetime.now()
        
        if user.role == 'member':
            task.verification_status = 'unverified'
        
        task.save()
        
        serializer = self.get_serializer(task)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        task = self.get_object()
        user = request.user
        
        if user.role not in ['admin', 'manager']:
            return Response({'error': 'Only managers and admins can verify tasks'},
                          status=status.HTTP_403_FORBIDDEN)
        
        if user.role == 'manager' and not task.project.assigned_to.filter(id=user.id).exists():
            return Response({'error': 'You are not assigned to this project'},
                          status=status.HTTP_403_FORBIDDEN)
        
        serializer = TaskVerifySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        action_type = serializer.validated_data['action']
        feedback = serializer.validated_data.get('feedback', '')
        
        if action_type == 'approve':
            task.verification_status = 'verified'
            task.status = 'verified'
            task.verified_by = user
            task.verified_at = datetime.now()
            task.manager_feedback = feedback
            task.save()
            
            return Response({
                'message': 'Task verified successfully',
                'task': self.get_serializer(task).data
            })
        
        elif action_type == 'reject':
            task.verification_status = 'rejected'
            task.status = 'rejected'
            task.verified_by = user
            task.verified_at = datetime.now()
            task.manager_feedback = feedback
            task.save()
            
            return Response({
                'message': 'Task rejected. Please update and resubmit.',
                'task': self.get_serializer(task).data
            })
    
    @action(detail=True, methods=['post'])
    def resubmit(self, request, pk=None):
        task = self.get_object()
        user = request.user
        
        if user.role != 'member':
            return Response({'error': 'Only members can resubmit tasks'},
                          status=status.HTTP_403_FORBIDDEN)
        
        if task.assigned_to.id != user.id:
            return Response({'error': 'You can only resubmit your own tasks'},
                          status=status.HTTP_403_FORBIDDEN)
        
        if task.verification_status != 'rejected':
            return Response({'error': 'Only rejected tasks can be resubmitted'},
                          status=status.HTTP_400_BAD_REQUEST)
        
        notes = request.data.get('notes', '')
        task.resubmit(notes)
        
        return Response({
            'message': 'Task resubmitted for verification',
            'task': self.get_serializer(task).data
        })


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
            
            stats_data = {
                'total_projects': projects.count(),
                'total_tasks': tasks.count(),
                'completed_tasks': tasks.filter(status='completed').count(),
                'pending_tasks': tasks.filter(status='pending').count(),
                'in_progress_tasks': tasks.filter(status='in_progress').count(),
                'verified_tasks': tasks.filter(verification_status='verified').count(),
                'pending_verification': tasks.filter(verification_status='unverified', status='completed').count(),
                'rejected_tasks': tasks.filter(verification_status='rejected').count(),
                'total_users': users.count(),
            }
            
        elif user.role == 'manager':
            projects = Project.objects.filter(assigned_to=user)
            tasks = Task.objects.filter(project__assigned_to=user)
            users = User.objects.filter(assigned_projects__in=projects).distinct()
            
            stats_data = {
                'total_projects': projects.count(),
                'total_tasks': tasks.count(),
                'completed_tasks': tasks.filter(status='completed').count(),
                'pending_tasks': tasks.filter(status='pending').count(),
                'in_progress_tasks': tasks.filter(status='in_progress').count(),
                'verified_tasks': tasks.filter(verification_status='verified').count(),
                'pending_verification': tasks.filter(verification_status='unverified', status='completed', project__assigned_to=user).count(),
                'rejected_tasks': tasks.filter(verification_status='rejected').count(),
                'total_users': users.count(),
            }
            
        else:
            projects = Project.objects.filter(assigned_to=user)
            tasks = Task.objects.filter(assigned_to=user)
            
            stats_data = {
                'total_projects': projects.count(),
                'total_tasks': tasks.count(),
                'completed_tasks': tasks.filter(status='completed').count(),
                'pending_tasks': tasks.filter(status='pending').count(),
                'in_progress_tasks': tasks.filter(status='in_progress').count(),
                'verified_tasks': tasks.filter(verification_status='verified').count(),
                'rejected_tasks': tasks.filter(verification_status='rejected').count(),
                'pending_verification': tasks.filter(verification_status='unverified', status='completed').count(),
            }
        
        return Response(stats_data)
