import os

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    SYSTEM_ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('pm', 'Project Manager'),
        ('user', 'User'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    system_role = models.CharField(
        max_length=10,
        choices=SYSTEM_ROLE_CHOICES,
        default='user'
    )

    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    drivers_category = models.CharField(max_length=10, null=True, blank=True)
    education_documents = models.FileField(upload_to='education_docs/', null=True, blank=True)

    # Notifications
    reminders = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=True)
    in_app_notifications = models.BooleanField(default=True)

    # Preferences
    theme = models.CharField(max_length=10, choices=[('light', 'Light'), ('dark', 'Dark')], default='light')
    default_view = models.CharField(max_length=10, choices=[('list', 'List'), ('grid', 'Grid')], default='list')
    language = models.CharField(max_length=5, choices=[('en', 'English'), ('lt', 'Lithuanian')], default='en')

    # Optional profile photo
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    def __str__(self):
        return self.user.username


class Project(models.Model):
    PROJECT_TYPES = [
        ('personal', 'Personal'),
        ('work', 'Work'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPES)
    due_date = models.DateField(null=True, blank=True, db_index=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_projects'
    )

    members = models.ManyToManyField(
        User,
        through='ProjectMembership',
        related_name='member_projects'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    is_completed = models.BooleanField(default=False)

    def update_completion_status(self):
        self.is_completed = not self.tasks.exclude(status='done').exists()
        self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Ensure owner is a project admin
        membership, created = ProjectMembership.objects.get_or_create(
            user=self.owner,
            project=self,
            defaults={'role': 'admin'}
        )
        if not created and membership.role != 'admin':
            membership.role = 'admin'
            membership.save()

    def update_shared_users_from_tasks(self):
        """
        Keep project memberships aligned with task assignees.
        Owner is always admin; assignees are added as regular users.
        """
        assignee_ids = self.tasks.exclude(assigned_to__isnull=True).values_list('assigned_to_id', flat=True).distinct()
        for user_id in assignee_ids:
            if user_id == self.owner_id:
                continue
            ProjectMembership.objects.get_or_create(
                user_id=user_id,
                project=self,
                defaults={'role': 'user'}
            )

    def __str__(self):
        return self.title


class ProjectMembership(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('pm', 'Project Manager'),
        ('user', 'User'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="project_memberships"
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="memberships"
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        db_index=True
    )

    class Meta:
        unique_together = ('user', 'project')


class Task(models.Model):

    STATUS_TODO = 'todo'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_DONE = 'done'

    STATUS_CHOICES = (
        (STATUS_TODO, 'To Do'),
        (STATUS_IN_PROGRESS, 'In Progress'),
        (STATUS_DONE, 'Done'),
    )
    LEGACY_STATUS_MAP = {
        'Not Started': STATUS_TODO,
        'Pending': STATUS_TODO,
        'In Progress': STATUS_IN_PROGRESS,
        'Completed': STATUS_DONE,
    }

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_TODO,
        db_index=True
    )
    due_date = models.DateField(null=True, blank=True, db_index=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(upload_to='task_attachments/', blank=True, null=True)
    estimated_time = models.DurationField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Normalize legacy values to canonical enum values.
        self.status = self.LEGACY_STATUS_MAP.get(self.status, self.status)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def is_overdue(self):
        from django.utils import timezone

        if not self.due_date:
            return False

        if self.status == self.STATUS_DONE:
            return False

        return self.due_date < timezone.now().date()


class Comment_project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.project.title}"


class Comment_task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey("Task", on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.task.title}"


class Reminder(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='reminders')
    title = models.CharField(max_length=200)
    due_time = models.DateTimeField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class TimeEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="time_entries")

    duration = models.DurationField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"{self.user} - {self.task.title}"
