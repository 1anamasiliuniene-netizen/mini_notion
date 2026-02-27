from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('shared/<int:pk>/', views.shared_project_detail, name='shared_project_detail'),
    path('search/', views.search_results, name='search_results'),
    path('navbar-reminders-json/', views.navbar_reminders_json, name='navbar_reminders_json'),
    path('reminder/<int:reminder_id>/resolve/', views.resolve_reminder, name='resolve_reminder'),
    path('reminder/<int:reminder_id>/delete/', views.delete_reminder, name='delete_reminder'),

    # Projects
    path('projects/<str:project_type>/', views.projects_list, name='projects_list'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('projects/add/<str:project_type>/', views.add_project, name='add_project'),
    path('project/<int:pk>/delete/', views.delete_project, name='delete_project'),
    path('archive/completed/', views.completed_projects_archive, name='completed_projects_archive'),

    # Tasks
    path('projects/<int:project_id>/tasks/add/', views.add_task, name='add_task'),
    path('task/<int:task_id>/update/', views.update_task, name='update_task'),
    path('task/<int:pk>/', views.task_detail, name='task_detail'),
    path('update-task-status/', views.update_task_status, name='update_task_status'),
    path('task/<int:pk>/delete/', views.delete_task, name='delete_task'),
    path('project/<int:pk>/archive/', views.archive_project, name='archive_project'),

    # Auth
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='mini_notion/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    # Profile
    path('edit-profile/', views.edit_profile, name='edit_profile'),


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
]
