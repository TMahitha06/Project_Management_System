from rest_framework import serializers
from .models import User, Project, Task
from datetime import datetime

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                 'role', 'phone', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }
    
    def validate(self, data):
        if 'password' in data and data.get('password'):
            if data['password'] != data.get('confirm_password'):
                raise serializers.ValidationError({"password": "Passwords don't match"})
        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        validated_data.pop('confirm_password', None)
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

class ProjectSerializer(serializers.ModelSerializer):
    created_by_name = serializers.ReadOnlyField(source='created_by.username')
    assigned_to_names = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'status', 'start_date', 'end_date',
                 'created_by', 'created_by_name', 'assigned_to', 'assigned_to_names',
                 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']
    
    def get_assigned_to_names(self, obj):
        return [user.username for user in obj.assigned_to.all()]

class TaskSerializer(serializers.ModelSerializer):
    project_name = serializers.ReadOnlyField(source='project.name')
    assigned_to_name = serializers.ReadOnlyField(source='assigned_to.username')
    created_by_name = serializers.ReadOnlyField(source='created_by.username')
    verification_status_display = serializers.SerializerMethodField()
    can_verify = serializers.SerializerMethodField()
    can_edit = serializers.SerializerMethodField()
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'project', 'project_name',
                 'assigned_to', 'assigned_to_name', 'created_by', 'created_by_name',
                 'priority', 'status', 'verification_status', 'verification_status_display',
                 'verified_by', 'verified_at', 'member_notes', 'manager_feedback',
                 'due_date', 'created_at', 'updated_at', 'can_verify', 'can_edit']
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at', 
                           'verified_by', 'verified_at', 'verification_status']
    
    def get_verification_status_display(self, obj):
        status_map = {
            'unverified': 'Pending Verification',
            'verified': 'Verified',
            'rejected': 'Rejected'
        }
        return status_map.get(obj.verification_status, obj.verification_status)
    
    def get_can_verify(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        user = request.user
        if user.role == 'admin':
            return True
        if user.role == 'manager':
            return obj.project.assigned_to.filter(id=user.id).exists()
        return False
    
    def get_can_edit(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        user = request.user
        if user.role == 'admin':
            return True
        if user.role == 'manager':
            return obj.project.assigned_to.filter(id=user.id).exists()
        if user.role == 'member':
            return obj.assigned_to.id == user.id
        return False
    
    def validate(self, data):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return data
        if request.user.role == 'member' and 'verification_status' in data:
            raise serializers.ValidationError({"verification_status": "Members cannot change verification status"})
        if request.user.role == 'member' and 'assigned_to' in data:
            if data.get('assigned_to') and data['assigned_to'].id != request.user.id:
                raise serializers.ValidationError({"assigned_to": "Members can only assign tasks to themselves"})
        return data
    
    def update(self, instance, validated_data):
        request = self.context.get('request')
        user = request.user
        
        if user.role == 'member':
            validated_data['verification_status'] = 'unverified'
            validated_data['verified_by'] = None
            validated_data['verified_at'] = None
            if 'status' in validated_data and validated_data['status'] == 'verified':
                validated_data['status'] = 'completed'
            if 'member_notes' not in validated_data and 'description' in validated_data:
                validated_data['member_notes'] = f"Updated: {validated_data['description']}"
        
        elif user.role in ['manager', 'admin']:
            if 'verification_status' in validated_data:
                if validated_data['verification_status'] == 'verified':
                    validated_data['verified_by'] = user
                    validated_data['verified_at'] = datetime.now()
                    validated_data['status'] = 'verified'
                elif validated_data['verification_status'] == 'rejected':
                    validated_data['status'] = 'rejected'
            
            if 'assigned_to' in validated_data and user.role == 'manager':
                assigned_user = validated_data.get('assigned_to')
                if assigned_user and not instance.project.assigned_to.filter(id=assigned_user.id).exists():
                    raise serializers.ValidationError({"assigned_to": "Can only assign tasks to project members"})
        
        return super().update(instance, validated_data)
    
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['created_by'] = request.user
        validated_data['verification_status'] = 'unverified'
        if request.user.role == 'member':
            validated_data['assigned_to'] = request.user
        return super().create(validated_data)

class TaskVerifySerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['approve', 'reject'])
    feedback = serializers.CharField(required=False, allow_blank=True)
    
    def validate_action(self, value):
        if value not in ['approve', 'reject']:
            raise serializers.ValidationError("Action must be 'approve' or 'reject'")
        return value
