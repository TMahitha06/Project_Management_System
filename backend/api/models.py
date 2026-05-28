from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('member', 'Member'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    phone = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

# Project Model
class Project(models.Model):
    STATUS_CHOICES = (
        ('planning', 'Planning'),
        ('active', 'Active'),
        ('completed', 'Completed'),
    )
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_projects')
    assigned_to = models.ManyToManyField(User, related_name='assigned_projects')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

# Task Model 
class Task(models.Model):
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    )
    
    VERIFICATION_STATUS_CHOICES = (
        ('unverified', 'Unverified'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_tasks')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
   
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    due_date = models.DateField()
    completed_at = models.DateTimeField(null=True, blank=True)
    
    verification_status = models.CharField(
        max_length=20, 
        choices=VERIFICATION_STATUS_CHOICES, 
        default='unverified'
    )
    verified_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='verified_tasks'
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    member_notes = models.TextField(blank=True, null=True, help_text="Notes from member about task updates")
    manager_feedback = models.TextField(blank=True, null=True, help_text="Feedback from manager during verification")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def is_verified(self):
        """Check if task is verified"""
        return self.verification_status == 'verified'
    
    def is_rejected(self):
        """Check if task is rejected"""
        return self.verification_status == 'rejected'
    
    def can_member_edit(self, user):
        """Check if a member can edit this task"""
        return user.role == 'member' and self.assigned_to.id == user.id
    
    def can_manager_verify(self, user):
        """Check if a manager can verify this task"""
        if user.role == 'admin':
            return True
        if user.role == 'manager':
            return self.project.assigned_to.filter(id=user.id).exists()
        return False
    
    def resubmit(self, notes=None):
        """Resubmit a rejected task for verification"""
        if self.verification_status == 'rejected':
            self.verification_status = 'unverified'
            self.status = 'pending'
            self.verified_by = None
            self.verified_at = None
            if notes:
                self.member_notes = notes
            self.save()
            return True
        return False
    
    def verify(self, user, feedback=None):
        """Verify a task by manager/admin"""
        if self.can_manager_verify(user):
            self.verification_status = 'verified'
            self.status = 'verified'
            self.verified_by = user
            self.verified_at = datetime.now()
            if feedback:
                self.manager_feedback = feedback
            self.save()
            return True
        return False
    
    def reject(self, user, feedback=None):
        """Reject a task by manager/admin"""
        if self.can_manager_verify(user):
            self.verification_status = 'rejected'
            self.status = 'rejected'
            self.verified_by = user
            self.verified_at = datetime.now()
            if feedback:
                self.manager_feedback = feedback
            self.save()
            return True
        return False
    
    class Meta:
        ordering = ['-created_at']