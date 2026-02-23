from django.contrib import admin
from .models import UserProfile, Project


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'project_type', 'created_at', 'due_date')
    list_filter = ('project_type', 'created_at')
    search_fields = ('title', 'description', 'owner__username')


# Register your models
admin.site.register(UserProfile)
admin.site.register(Project, ProjectAdmin)
