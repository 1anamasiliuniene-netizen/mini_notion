from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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
    due_date = models.DateField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    shared_with = models.ManyToManyField(User, blank=True, related_name='shared_projects')
    created_at = models.DateTimeField(auto_now_add=True)

    is_completed = models.BooleanField(default=False)

    def update_completion_status(self):
        self.is_completed = all(task.status == 'done' for task in self.tasks.all())
        self.save()

    def __str__(self):
        return self.title

    def update_shared_users_from_tasks(self):
        return User.objects.filter(task__project=self).distinct()

class ProjectMembership(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('pm', 'Project Manager'),
        ('user', 'User'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ('user', 'project')

class Task(models.Model):
    STATUS_CHOICES = (
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(upload_to='task_attachments/', blank=True, null=True)

    def __str__(self):
        return self.title


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


