from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import dashboard_view
from django.shortcuts import redirect

urlpatterns = [
    # Dashboard
    path('', lambda request: redirect('dashboard'), name='home'),
    path('dashboard/', dashboard_view, name='dashboard'),

    # Admin Panel
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/toggle-superuser/<int:user_id>/', views.toggle_superuser, name='toggle_superuser'),
    path('admin-panel/toggle-active/<int:user_id>/', views.toggle_user_active, name='toggle_user_active'),
    path('admin-panel/change-role/<int:membership_id>/', views.change_role, name='change_role'),

    # Auth
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='mini_notion/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    # Password reset
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="mini_notion/registration/password_reset_form.html",
            email_template_name="mini_notion/registration/password_reset_email.txt",
            html_email_template_name="mini_notion/registration/password_reset_email.html",
            success_url="/password_reset/done/"
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="mini_notion/registration/password_reset_done.html"
        ),
        name="password_reset_done"
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="mini_notion/registration/password_reset_confirm.html",
            success_url="/password_reset/complete/"
        ),
        name="password_reset_confirm"
    ),
    path(
        "password_reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="mini_notion/registration/password_reset_complete.html"
        ),
        name="password_reset_complete"
    ),

    # Profile
    path('edit-profile/', views.edit_profile, name='edit_profile'),

    # User Settings
    path('settings/', views.settings_view, name='settings'),
    path('settings/update_notifications/', views.update_notifications, name='update_notifications'),
    path('settings/update_preferences/', views.update_preferences, name='update_preferences'),
    path('settings/deactivate_account/', views.deactivate_account, name='deactivate_account'),

    # Projects
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),  # detail view
    path('projects/<str:project_type>/', views.projects_list, name='projects_list'),  # list by type
    path('projects/add/<str:project_type>/', views.add_project, name='add_project'),  # add project
    path('projects/<int:pk>/delete/', views.delete_project, name='delete_project'),
    path('projects/<int:pk>/archive/', views.archive_project, name='archive_project'),
    path('projects/<int:pk>/recover/', views.recover_project, name='recover_project'),
    path('archive/completed/', views.completed_projects_archive, name='completed_projects_archive'),

    # Tasks
    path('projects/<int:project_id>/tasks/add/', views.add_task, name='add_task'),
    path('tasks/<int:task_id>/update/', views.update_task, name='update_task'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('update-task-status/', views.update_task_status, name='update_task_status'),

    # Reminders
    path('reminders/<int:reminder_id>/resolve/', views.resolve_reminder, name='resolve_reminder'),
    path('reminders/<int:reminder_id>/delete/', views.delete_reminder, name='delete_reminder'),
    path('navbar-reminders-json/', views.navbar_reminders_json, name='navbar_reminders_json'),

    # Shared Projects
    path('shared/<int:pk>/', views.shared_project_detail, name='shared_project_detail'),

    # Search
    path('search/', views.search_results, name='search_results'),
]