from rest_framework import serializers
from .models import User, Project, Task

# User Serializer
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
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'project', 'project_name',
                 'assigned_to', 'assigned_to_name', 'created_by', 'created_by_name',
                 'priority', 'status', 'due_date', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']