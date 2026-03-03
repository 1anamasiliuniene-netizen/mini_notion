from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta

from ..models import Project, Task, TimeEntry, ProjectMembership

def user_dashboard(user):
    """
    Returns analytics for a regular user dashboard.
    """

    today = timezone.now().date()
    week_ago = timezone.now() - timedelta(days=7)

    # Projects where user is member
    projects = Project.objects.filter(
        memberships__user=user
    ).distinct()

    # Tasks assigned to the user
    tasks = Task.objects.filter(assigned_to=user)

    completed_tasks = tasks.filter(status="done").count()
    overdue_tasks = tasks.filter(
        due_date__lt=today
    ).exclude(status="done").count()

    weekly_time = TimeEntry.objects.filter(
        user=user,
        created_at__gte=week_ago
    ).aggregate(total=Sum("duration"))["total"] or 0

    return {
        "projects_count": projects.count(),
        "assigned_tasks": tasks.count(),
        "completed_tasks": completed_tasks,
        "overdue_tasks": overdue_tasks,
        "weekly_logged_time": weekly_time,
    }

def pm_dashboard(user):
    """
    Returns analytics for a Project Manager dashboard.
    """

    today = timezone.now().date()

    pm_projects = Project.objects.filter(
        memberships__user=user,
        memberships__role='pm'
    )

    total_tasks = Task.objects.filter(project__in=pm_projects).count()
    completed_tasks = Task.objects.filter(project__in=pm_projects, status='done').count()
    overdue_tasks = Task.objects.filter(
        project__in=pm_projects,
        due_date__lt=today
    ).exclude(status='done').count()

    total_time = TimeEntry.objects.filter(
        task__project__in=pm_projects
    ).aggregate(total=Sum("duration"))["total"] or 0

    return {
        "projects_count": pm_projects.count(),
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "overdue_tasks": overdue_tasks,
        "total_logged_time": total_time,
    }

from django.contrib.auth.models import User

def admin_dashboard():
    """
    Returns system-wide analytics for admin users.
    """

    today = timezone.now().date()

    total_projects = Project.objects.count()
    total_users = User.objects.count()
    total_tasks = Task.objects.count()
    overdue_tasks = Task.objects.filter(
        due_date__lt=today
    ).exclude(status='done').count()

    total_time = TimeEntry.objects.aggregate(total=Sum("duration"))["total"] or 0

    return {
        "total_projects": total_projects,
        "total_users": total_users,
        "total_tasks": total_tasks,
        "overdue_tasks": overdue_tasks,
        "total_logged_time": total_time,
    }

def project_analytics(project):
    """
    Returns analytics for a specific project.
    """

    today = timezone.now().date()

    tasks = project.tasks.all()
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status='done').count()

    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks else 0

    total_logged_time = TimeEntry.objects.filter(
        task__project=project
    ).aggregate(total=Sum("duration"))["total"] or 0

    days_remaining = (project.due_date - today).days if project.due_date else None

    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "completion_rate": completion_rate,
        "total_logged_time": total_logged_time,
        "days_remaining": days_remaining,
    }

from django.db.models import Count

def workload_distribution(project):
    """
    Returns number of tasks per assigned user in a project.
    """

    distribution = Task.objects.filter(
        project=project
    ).values("assigned_to__username").annotate(
        task_count=Count("id")
    )

    return list(distribution)