from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    drivers_category = models.CharField(max_length=10, null=True, blank=True)
    education_documents = models.FileField(upload_to='education_docs/', null=True, blank=True)

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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def update_shared_users_from_tasks(self):
        return User.objects.filter(task__project=self).distinct()


class Card(models.Model):
    project = models.ForeignKey(Project, related_name='project_cards', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()

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
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment_project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

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
