import os
import json
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest, Http404, JsonResponse, HttpResponseForbidden
from django.utils import timezone
from django.utils.timezone import now
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db.models import DateField, Q, Count
from django.db.models.functions import Cast
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.middleware.csrf import get_token

from .models import (
    UserProfile,
    Task,
    Comment_task,
    Reminder,
    Project,
    ProjectMembership
)
from .forms import UserProfileForm, UserForm, ProjectForm, TaskForm
from .services.analytics import user_dashboard, pm_dashboard, admin_dashboard, project_analytics


def dashboard_view(request):
    today = date.today()
    selected_date_str = request.GET.get('date')
    try:
        selected_date = date.fromisoformat(selected_date_str) if selected_date_str else today
    except ValueError:
        selected_date = today

    # --- Birthdays today ---
    birthdays = UserProfile.objects.filter(
        date_of_birth__month=today.month,
        date_of_birth__day=today.day
    ).exclude(user=request.user) if request.user.is_authenticated else UserProfile.objects.filter(
        date_of_birth__month=today.month,
        date_of_birth__day=today.day
    )

    # --- Shared Projects ---
    shared_projects_qs = Project.objects.filter(
        tasks__assigned_to__isnull=False
    ).distinct().order_by('-created_at')
    # Show all shared projects for everyone
    shared_projects = list(shared_projects_qs)

    # === Tasks (only for logged-in users) ===
    tasks = []
    if request.user.is_authenticated:
        # Handle checkbox POST for tasks
        if request.method == 'POST' and request.POST.get('form_type') == 'update_task_status':
            task_id = request.POST.get('task_id')
            try:
                task = Task.objects.get(id=task_id)
                if task.assigned_to == request.user:
                    task.status = 'Completed'
                    task.save()
            except Task.DoesNotExist:
                pass
            return redirect(f"{request.path}?date={selected_date}")

        # Load only incomplete tasks
        tasks = Task.objects.filter(
            assigned_to=request.user,
            status__in=['Pending', 'In Progress'],
            due_date=selected_date
        ).order_by('due_date')

        for task in tasks:
            task.completed = False
            task.is_overdue = task.due_date and task.due_date < today

    # --- Analytics ---
    analytics = {
        'total_users': User.objects.count(),
        'total_projects': Project.objects.count(),
        'tasks_completed': Task.objects.filter(status='Completed').count(),
        'tasks_overdue': Task.objects.filter(status__in=['Pending', 'In Progress'], due_date__lt=today).count(),
    }

    # --- All users stats ---
    all_users = []
    for u in User.objects.all():
        tasks_assigned = Task.objects.filter(assigned_to=u).count()
        overdue_tasks = Task.objects.filter(assigned_to=u, status__in=['Pending', 'In Progress'],
                                            due_date__lt=today).count()
        all_users.append({
            'username': u.username,
            'tasks_assigned': tasks_assigned,
            'overdue_tasks': overdue_tasks,
        })

    context = {
        'birthdays': birthdays,
        'shared_projects': shared_projects,
        'tasks': tasks,
        'today': today,
        'selected_date': selected_date,
        'analytics': analytics,
        'all_users': all_users,
        'system_role': getattr(getattr(request.user, 'userprofile', None), 'system_role',
                               'guest') if request.user.is_authenticated else 'guest',
    }

    return render(request, 'mini_notion/dashboard.html', context)


@login_required
def admin_panel(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    users = User.objects.all()
    memberships = ProjectMembership.objects.select_related('user', 'project')

    context = {
        'users': users,
        'memberships': memberships,
        'role_choices': ProjectMembership.ROLE_CHOICES,
    }

    return render(request, 'mini_notion/admin_panel.html', context)


@login_required
def toggle_user_active(request, user_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    user = get_object_or_404(User, id=user_id)

    # Prevent self-deactivation (very important)
    if user != request.user:
        user.is_active = not user.is_active
        user.save()

    return redirect('admin_panel')


@login_required
def toggle_superuser(request, user_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    user = get_object_or_404(User, id=user_id)

    # Prevent self-demotion (important!)
    if user != request.user:
        user.is_superuser = not user.is_superuser
        user.save()

    return redirect('admin_panel')


@login_required
def change_role(request, membership_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    membership = get_object_or_404(ProjectMembership, id=membership_id)

    if request.method == "POST":
        new_role = request.POST.get("role")
        if new_role in dict(ProjectMembership.ROLE_CHOICES):
            membership.role = new_role
            membership.save()

    return redirect('admin_panel')


@login_required
def role_dashboard(request):
    profile = request.user.userprofile
    system_role = profile.system_role

    if system_role == "admin":
        analytics = admin_dashboard()
    elif system_role == "pm":
        analytics = pm_dashboard(request.user)
    else:
        analytics = user_dashboard(request.user)

    return render(request, "mini_notion/dashboard.html", {
        "analytics": analytics,
        "system_role": system_role,
    })


@login_required
def navbar_reminders_json(request):
    today = now()

    reminders = Reminder.objects.filter(
        project__owner=request.user,
        completed=False
    ).order_by('due_time')[:5]

    data = []
    for r in reminders:
        csrf_token = get_token(request)
        data.append({
            'id': r.id,
            'title': r.title,
            'project_title': r.project.title,
            'project_id': r.project.id,
            'due_time': r.due_time.strftime("%d %b %H:%M"),
            'is_overdue': r.due_time < today,
        })

    return JsonResponse({'reminders': data})


@login_required
@require_POST
def resolve_reminder(request, reminder_id):
    reminder = get_object_or_404(
        Reminder,
        id=reminder_id,
        project__in=Project.objects.filter(
            Q(owner=request.user) | Q(members=request.user)
        )
    )

    reminder.completed = True
    reminder.save()

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def settings_view(request):
    return render(request, 'mini_notion/settings.html')


@login_required
def update_notifications(request):
    if request.method == 'POST':
        profile = request.user.userprofile
        profile.reminders = bool(request.POST.get('reminders'))
        profile.email_notifications = bool(request.POST.get('email_notifications'))
        profile.in_app_notifications = bool(request.POST.get('in_app_notifications'))
        profile.save()
        messages.success(request, "Notification settings updated.")
    return redirect('settings')


@login_required
def update_preferences(request):
    if request.method == 'POST':
        profile = request.user.userprofile
        profile.theme = request.POST.get('theme', 'light')
        profile.default_view = request.POST.get('default_view', 'list')
        profile.language = request.POST.get('language', 'en')
        profile.save()
        messages.success(request, "Preferences updated.")
    return redirect('settings')


@login_required
def deactivate_account(request):
    if request.method == 'POST':
        user = request.user
        user.is_active = False
        user.save()
        messages.warning(request, "Your account has been deactivated.")
        from django.contrib.auth import logout
        logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    today = date.today()
    selected_date_str = request.GET.get('date')
    try:
        selected_date = date.fromisoformat(selected_date_str) if selected_date_str else today
    except ValueError:
        selected_date = today

    # === Birthdays (exclude current user optionally) ===
    birthdays = UserProfile.objects.filter(
        date_of_birth__month=today.month,
        date_of_birth__day=today.day
    ).exclude(user=request.user)

    # === Shared projects ===
    shared_projects_qs = Project.objects.filter(
        tasks__assigned_to__isnull=False
    ).distinct().order_by('-created_at')

    shared_projects = [
        p for p in shared_projects_qs
        if p.owner == request.user or p.tasks.filter(assigned_to=request.user).exists()
    ]

    # === Tasks for selected date ===
    if request.user.is_authenticated:
        tasks = Task.objects.annotate(
            due_date_only=Cast('due_date', DateField())
        ).filter(
            assigned_to=request.user,
            due_date_only=selected_date
        ).order_by('due_date')

        # Annotate tasks for template convenience
        for task in tasks:
            task.completed = task.status == 'Completed'
            task.is_overdue = task.due_date and task.status != 'Completed' and task.due_date < today
    else:
        tasks = []

    # === Role & Analytics ===
    profile = request.user.userprofile
    system_role = profile.system_role
    if system_role == 'admin':
        analytics = admin_dashboard()
    elif system_role == 'pm':
        analytics = pm_dashboard(request.user)
    else:
        analytics = user_dashboard(request.user)

    context = {
        'birthdays': birthdays,
        'shared_projects': shared_projects,
        'tasks': tasks,
        'today': today,
        'selected_date': selected_date,
        'system_role': system_role,
        'analytics': analytics,
    }

    return render(request, 'mini_notion/dashboard.html', context)


def shared_project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    today = date.today()

    # Annotate tasks with 'is_overdue'
    tasks = project.tasks.all()
    for task in tasks:
        task.is_overdue = task.due_date is not None and task.due_date < today and task.status != 'Completed'
        if task.attachment:
            task.attachment_filename = os.path.basename(task.attachment.name)

    tasks = sorted(
        tasks,
        key=lambda t: (not t.is_overdue, t.due_date if t.due_date else date.max)
    )

    # Pass comments and reminders
    comments = project.comments.all()
    reminders = project.reminders.all()

    return render(request, 'mini_notion/reports.html', {
        'project': project,
        'today': today,
        'tasks': tasks,
        'comments': comments,
        'reminders': reminders,
    })


@login_required
@require_POST
def delete_reminder(request, reminder_id):
    reminder = get_object_or_404(
        Reminder,
        id=reminder_id,
        project__owner=request.user  # only project owner can delete
    )
    project_id = reminder.project.id
    reminder.delete()
    return redirect('project_detail', pk=project_id)


def search_results(request):
    query = request.GET.get('q', '').strip()
    task_status = request.GET.get('status', '').strip()
    due_before = request.GET.get('due_before', '').strip()
    today = timezone.localdate()

    results = []

    if query:
        # Find users whose username, first_name, last_name, or projects/tasks match
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(owned_projects__title__icontains=query) |
            Q(member_projects__title__icontains=query) |
            Q(tasks__title__icontains=query)
        ).distinct()

        for user in users:
            projects_with_tasks = []

            # Combine owned and member projects
            user_projects = list(user.owned_projects.all()) + list(user.member_projects.all())

            # Check if user matched by username/name or by project/task
            user_matched_by_name = (
                query.lower() in user.username.lower() or
                query.lower() in user.first_name.lower() or
                query.lower() in user.last_name.lower()
            )

            for project in user_projects:
                # Fetch all tasks in the project
                tasks_qs = Task.objects.filter(project=project)

                # Determine which tasks to show
                project_title_matches = query.lower() in project.title.lower()

                if user_matched_by_name:
                    # If user matched by name, show ALL tasks in ALL their projects (apply filters only)
                    tasks_to_show = tasks_qs
                elif project_title_matches:
                    # If project title matches, show all tasks in that project (apply filters only)
                    tasks_to_show = tasks_qs
                else:
                    # Otherwise, only show tasks that match the query title
                    tasks_to_show = tasks_qs.filter(title__icontains=query)

                # Apply task status filter if specified
                if task_status:
                    tasks_to_show = tasks_to_show.filter(status=task_status)

                # Apply due date filter if specified
                if due_before:
                    tasks_to_show = tasks_to_show.filter(due_date__lte=due_before)

                # Annotate for template with correct status values
                for t in tasks_to_show:
                    t.completed = t.status == 'done'
                    t.is_overdue = t.due_date and t.status != 'done' and t.due_date < today

                if tasks_to_show.exists():
                    projects_with_tasks.append({
                        'project': project,
                        'tasks': tasks_to_show,
                    })

            # Only add user if they have projects with matching tasks
            if projects_with_tasks:
                results.append({
                    'user': user,
                    'projects_with_tasks': projects_with_tasks,
                })

    context = {
        'query': query,
        'results': results,
        'task_status': task_status,
        'due_before': due_before,
        'today': today,
    }
    return render(request, 'mini_notion/search_results.html', context)


@login_required
def edit_profile(request):
    user = request.user
    profile = getattr(user, 'userprofile', None)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('dashboard')
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    return render(request, 'mini_notion/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'mini_notion/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('dashboard')


# Project Views
@login_required
def projects_list(request, project_type):
    if project_type not in dict(Project.PROJECT_TYPES):
        raise Http404("Project type not found")

    # Only active projects
    projects = Project.objects.filter(
        owner=request.user,
        project_type=project_type,
        is_completed=False
    ).order_by('-created_at')

    # Pagination
    paginator = Paginator(projects, 3)  # 3 projects per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'mini_notion/projects_list.html', {
        'projects': page_obj,  # pass the page object
        'project_type': project_type,
    })


@login_required
def completed_projects_archive(request):
    today = date.today()

    projects = Project.objects.filter(
        owner=request.user,
        is_completed=True
    )

    return render(request, 'mini_notion/completed_projects.html', {
        'projects': projects,
        'today': today,
    })


@login_required
def archive_project(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)

    # Only archive if all tasks are completed
    if project.tasks.exists() and all(task.status == 'done' for task in project.tasks.all()):
        project.is_completed = True
        project.save()
        messages.success(request, f'Project "{project.title}" archived.')

    return redirect('projects_list', project_type=project.project_type)


@login_required
def recover_project(request, pk):
    project = get_object_or_404(Project, pk=pk, owner=request.user)

    # Recover the project
    project.is_completed = False
    project.save()
    messages.success(request, f'Project "{project.title}" recovered.')

    # Redirect to the active projects list of the correct type
    return redirect('projects_list', project_type=project.project_type)


@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, id=pk)
    all_users = list(User.objects.exclude(id=request.user.id).order_by('username'))
    if project.owner not in all_users:
        all_users.insert(0, project.owner)

    if request.method == "POST":

        # === Checkbox POST for task status ===
        if request.POST.get('form_type') == 'update_task_status':
            task_id = request.POST.get('task_id')
            completed = request.POST.get('completed') == 'on'
            try:
                task = Task.objects.get(pk=task_id, project=project)
                task.status = 'done' if completed else 'in_progress'
                task.save()
                messages.success(request, f'Task "{task.title}" status updated!')
            except Task.DoesNotExist:
                messages.error(request, 'Task not found!')
            return redirect('project_detail', pk=project.id)

        form_type = request.POST.get('form_type')

        # === Edit project info ===
        if form_type == "edit_project":
            project.title = request.POST.get('title', project.title)
            project.description = request.POST.get('description', project.description)
            project.project_type = request.POST.get('project_type', project.project_type)
            project.save()
            messages.success(request, "Project updated!")

        # === Add task ===
        elif form_type == "add_task":
            title = request.POST.get('title')
            description = request.POST.get('description', '')
            due_date = request.POST.get('due_date') or None
            assigned_id = request.POST.get('assigned_to')
            assign_to_all = request.POST.get('assign_to_all')

            if assign_to_all == 'on':
                for user in all_users:
                    Task.objects.create(
                        project=project,
                        title=title,
                        description=description,
                        due_date=due_date,
                        assigned_to=user,
                        status='in_progress'
                    )
            else:
                assigned_user = None
                if assigned_id:
                    try:
                        assigned_user = User.objects.get(id=int(assigned_id))
                    except User.DoesNotExist:
                        pass
                Task.objects.create(
                    project=project,
                    title=title,
                    description=description,
                    due_date=due_date,
                    assigned_to=assigned_user,
                    status='in_progress'
                )

        # Add project comment
        elif form_type == "add_comment":
            content = request.POST.get('content')
            if content:
                project.comments.create(user=request.user, content=content)

        # Add reminder
        elif form_type == "add_reminder":
            title = request.POST.get('title')
            due_time = request.POST.get('due_time')
            if title and due_time:
                project.reminders.create(title=title, due_time=due_time)

        return redirect('project_detail', pk=project.id)

    # GET request – render template
    context = {
        'project': project,
        'all_users': all_users,
        'today': date.today(),
        'tasks': project.tasks.all().order_by('due_date'),
        'comments': project.comments.all().order_by('-created_at'),
        'reminders': project.reminders.all().order_by('due_time'),
    }
    return render(request, 'mini_notion/project_detail.html', context)


@login_required
def add_project(request, project_type):
    if project_type not in dict(Project.PROJECT_TYPES):
        return HttpResponseBadRequest("Invalid project type")

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.project_type = project_type  # force the type
            project.save()
            return redirect('projects_list', project_type=project_type)
    else:
        form = ProjectForm()

    if form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        form.save_m2m()

    return render(request, 'mini_notion/add_project_type.html', {'form': form, 'project_type': project_type})


@login_required
def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if project.owner == request.user:
        project.delete()
    return redirect('projects_list', project_type=project.project_type)


@login_required
def add_task(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            form.save_m2m()
            project.update_shared_users_from_tasks()
            return redirect('project_detail', pk=project.id)
    else:
        form = TaskForm()

    return render(request, 'mini_notion/add_task.html', {'form': form, 'project': project})


@login_required
def update_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    project = task.project

    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.due_date = request.POST.get('due_date') or None
        task.status = request.POST.get('status')
        task.assigned_to_id = request.POST.get('assigned_to') or None
        task.save()
        project.update_shared_users_from_tasks()

    return redirect('project_detail', pk=project.id)


@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        form_type = request.POST.get('form_type', "")

        if form_type == 'status_checkbox':
            task.status = 'Completed' if request.POST.get('status_checkbox') == 'on' else 'In Progress'
            task.save()
            return redirect('task_detail', pk=task.pk)

        # task edit form
        elif form_type == 'edit_task':
            task.title = request.POST.get('title', task.title)
            task.due_date = request.POST.get('due_date') or None
            task.status = request.POST.get('status', task.status)
            task.description = request.POST.get('description', '').strip() or ''

            if request.FILES.get("attachment"):
                task.attachment = request.FILES["attachment"]

            task.save()
            return redirect('task_detail', pk=task.pk)

        # Add comment
        elif form_type == 'add_task_comment':
            content = request.POST.get('content', '').strip()
            if content:
                Comment_task.objects.create(user=request.user, task=task, content=content)
            return redirect('task_detail', pk=task.pk)

    return render(request, 'mini_notion/task_detail.html', {'task': task})


@csrf_exempt
def update_task_status(request):
    if request.method == 'POST' and request.user.is_authenticated:
        data = json.loads(request.body)
        task_id = data.get('id')
        completed = data.get('completed', False)

        try:
            task = Task.objects.get(id=task_id)
            # only allow updating tasks assigned to the current user
            if task.assigned_to == request.user:
                task.status = 'Completed' if completed else 'Pending'
                task.save()
                return JsonResponse({'success': True})
        except Task.DoesNotExist:
            pass
    return JsonResponse({'success': False})


@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    project = task.project

    if request.user == task.assigned_to or request.user == project.owner:
        task.delete()
        messages.success(request, "Task deleted successfully.")

    return redirect('project_detail', pk=project.id)


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'mini_notion/signup.html', {'form': form})
