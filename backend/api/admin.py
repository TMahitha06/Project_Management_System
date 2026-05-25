from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import User, Project, Task

admin.site.unregister(Group)

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active')
    list_filter = ()
    search_fields = ('username', 'email')
    actions = None
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('username', 'password', 'email', 'first_name', 'last_name', 'phone')
        }),
        ('Role & Status', {
            'fields': ('role', 'is_active')
        }),
        ('Important Dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'is_active'),
        }),
    )
    
    readonly_fields = ('last_login', 'date_joined')

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'start_date', 'created_by')
    list_filter = ()
    search_fields = ('name',)

 
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'assigned_to', 'priority', 'status', 'due_date')
    list_filter = ()
    search_fields = ('title',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)