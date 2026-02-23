from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('shared/<int:pk>/', views.shared_project_detail, name='shared_project_detail'),

    # Projects
    path('projects/<str:project_type>/', views.projects_list, name='projects_list'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('projects/add/<str:project_type>/', views.add_project, name='add_project'),
    path('project/<int:pk>/delete/', views.delete_project, name='delete_project'),# <- added

    # Tasks
    path('projects/<int:project_id>/tasks/add/', views.add_task, name='add_task'),
    path('task/<int:task_id>/update/', views.update_task, name='update_task'),
    path('task/<int:pk>/', views.task_detail, name='task_detail'),
    path('update-task-status/', views.update_task_status, name='update_task_status'),

    # Auth
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='mini_notion/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Profile
    path('edit-profile/', views.edit_profile, name='edit_profile'),
]