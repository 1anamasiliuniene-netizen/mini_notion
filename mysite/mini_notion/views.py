import os, json
from datetime import date
from .models import UserProfile, Project, Task, Comment_task
from .forms import UserProfileForm, UserForm, ProjectForm, TaskForm
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, Http404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db.models import DateField
from django.db.models.functions import Cast
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .models import Reminder, Project
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q


@login_required
def navbar_reminders_json(request):
    today = now()

    reminders = Reminder.objects.filter(
        project__owner=request.user,
        completed=False
    ).order_by('due_time')[:5]

    data = []
    for r in reminders:
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
            Q(owner=request.user) | Q(shared_with=request.user)
        )
    )

    reminder.completed = True
    reminder.save()

    return redirect(request.META.get('HTTP_REFERER', '/'))

def dashboard(request):
    today = date.today()

    # Selected date (from query param ?date=YYYY-MM-DD), default to today
    selected_date_str = request.GET.get('date')
    if selected_date_str:
        try:
            selected_date = date.fromisoformat(selected_date_str)
        except ValueError:
            selected_date = today
    else:
        selected_date = today

    # Birthdays
    birthdays = UserProfile.objects.filter(
        date_of_birth__month=today.month,
        date_of_birth__day=today.day
    )

    # Public shared projects
    shared_projects_qs = Project.objects.filter(
        tasks__assigned_to__isnull=False
    ).exclude(owner=None).distinct().order_by('-created_at')

    shared_projects = []
    for project in shared_projects_qs:
        if request.user.is_authenticated:
            if project.owner == request.user or project.tasks.filter(assigned_to=request.user).exists():
                shared_projects.append(project)
        else:
            shared_projects.append(project)

    # Handle task deletion if POST
    if request.POST.get('form_type') == 'update_task_status':
        task_id = request.POST.get('task_id')
        completed = request.POST.get('completed') == 'on'

        try:
            task = Task.objects.get(id=task_id, assigned_to=request.user)
            task.status = 'Completed' if completed else 'In Progress'
            task.save()
            messages.success(request, f'Task "{task.title}" status updated!')
        except Task.DoesNotExist:
            messages.error(request, "Task not found.")

        return redirect('dashboard')

    # Tasks only for authenticated users
    if request.user.is_authenticated:
        todo_tasks = Task.objects.annotate(
            due_date_only=Cast('due_date', DateField())
        ).filter(
            assigned_to=request.user,
            due_date_only=selected_date
        ).exclude(status='Completed').order_by('due_date')
    else:
        todo_tasks = []

    return render(request, 'mini_notion/dashboard.html', {
        'birthdays': birthdays,
        'shared_projects': shared_projects,
        'tasks': todo_tasks,
        'today': today,
        'selected_date': selected_date,
    })


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
    query = request.GET.get('q', '')

    results = []

    if query:
        # Find users whose username contains the query
        users = User.objects.filter(username__icontains=query)

        for user in users:
            profile = UserProfile.objects.filter(user=user).first()
            projects = Project.objects.filter(owner=user)
            tasks = Task.objects.filter(assigned_to=user)

            results.append({
                'user': user,
                'profile': profile,
                'projects': projects if projects.exists() else None,
                'tasks': tasks if tasks.exists() else None,
            })

    context = {
        'query': query,
        'results': results,
        'today': date.today(),
    }

    return render(request, 'mini_notion/search_results.html', context)


# Authentication Views
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'mini_notion/signup.html', {'form': form})


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
    paginator = Paginator(projects, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'mini_notion/projects_list.html', {
        'projects': page_obj,
        'project_type': project_type,
    })


@login_required
def completed_projects_archive(request):
    today = date.today()

    # Only include projects where all tasks are completed
    projects = []
    for project in Project.objects.all():
        tasks = project.tasks.all()
        if tasks.exists() and all(task.status == 'Completed' for task in tasks):
            # Annotate tasks with overdue and attachment info
            for task in tasks:
                task.is_overdue = task.due_date and task.due_date < today and task.status != 'Completed'
                if task.attachment:
                    task.attachment_filename = os.path.basename(task.attachment.name)
            projects.append(project)

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

    return redirect('projects_list', project_type=project.project_type)


@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    all_users = list(User.objects.exclude(id=request.user.id).order_by('username'))
    if project.owner not in all_users:
        all_users.insert(0, project.owner)

    if request.method == "POST":

        # === Checkbox POST for task status ===
        if request.POST.get('form_type') == 'update_task_status':
            task_id = request.POST.get('task_id')
            completed = request.POST.get('completed') == 'on'
            try:
                task = Task.objects.get(id=task_id, project=project)
                task.status = 'Completed' if completed else 'In Progress'
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
                        status='In Progress'
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
                    status='In Progress'
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
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)

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

# password reset views using Django's built-in views
