# Mini Notion

This is a Django-based project and task management app with role-based collaboration.

## App Characteristics

- User authentication: sign up, login/logout, password reset.
- Role support: `admin`, `project manager (pm)`, and `user` roles.
- Project management with personal/work project types.
- Project due dates, archive/recover flow, and paginated project lists.
- Team collaboration:
  - project memberships with role assignment
  - shared project access for members and assignees
- Task management:
  - create, edit, delete, and assign tasks
  - task statuses: `todo`, `in_progress`, `done`
  - due dates, overdue detection, and completion tracking
  - optional task file attachments
- Communication and planning:
  - project comments
  - task comments
  - project reminders with resolve/delete actions
- Dashboard and analytics:
  - daily view of assigned tasks
  - birthday highlights
  - role-based analytics widgets
- Search and filtering:
  - global search across users/projects/tasks
  - task status and due-date filters
- User profile and preferences:
  - profile photo and personal info
  - notification preferences
  - UI preferences (theme/default view/language)
- External integration:
  - NASA APOD demo endpoint with caching and JSON API response.

## Tech Stack

- Python, Django 6
- SQLite (default)
- Django Crispy Forms + Bootstrap 5
- Pillow (image uploads)
- WhiteNoise (static files)
