# Complete Technical Guide: Template Changes & Deployment

## Understanding Django Template Rendering

### How Templates Work in Django

```
1. HTTP Request arrives
   ↓
2. Django URL routing finds matching view
   ↓
3. View function/class executes
   ↓
4. Template file is READ FROM DISK
   ↓
5. Django template engine processes HTML
   ↓
6. Context variables substituted
   ↓
7. HTML sent to browser
   ↓
8. Browser renders to user
```

**Key point**: Template file is read **fresh on every request**!

---

## Why Templates Don't Need Restart

### Python Code (Requires Restart)
```python
# views.py
def my_view(request):
    return render(request, 'template.html')
    # Python code is compiled into memory at startup
    # Changes need restart to recompile
```

### Template Files (Auto-reload)
```html
<!-- template.html -->
<h2>{{ title }}</h2>
<!-- HTML file read from disk each request -->
<!-- Changes apply immediately after git pull -->
```

### Static Files (Depends)
```css
/* style.css */
h2 { color: blue; }
/* With WhiteNoise middleware: changes require reload -->
```

---

## Complete Deployment Workflow

### Local Development Machine (Your Mac)

```
┌─ EDIT PHASE ─────────────────────────────────────┐
│                                                   │
│ 1. Edit file: nasa_apod_demo.html               │
│    Location: /Users/anamasiliuniene/...         │
│                                                   │
│ 2. Test locally:                                 │
│    $ python manage.py runserver                  │
│    Visit: http://localhost:8000                  │
│                                                   │
└─────────────────────────────────────────────────┘
                     ↓
┌─ VERSION CONTROL ────────────────────────────────┐
│                                                   │
│ 3. Stage changes:                                │
│    $ git add mysite/mini_notion/templates/...   │
│                                                   │
│ 4. Commit:                                       │
│    $ git commit -m "descriptive message"        │
│                                                   │
│ 5. Push to GitHub:                              │
│    $ git push origin main                        │
│    Files uploaded to remote repository           │
│                                                   │
└─────────────────────────────────────────────────┘
                     ↓
              GITHUB REPOSITORY
              (Your backup in cloud)
```

### PythonAnywhere Server (Production)

```
┌─ PULL PHASE ──────────────────────────────────────┐
│                                                    │
│ 6. SSH into PythonAnywhere:                       │
│    $ ssh -l AnaMa ssh.pythonanywhere.com          │
│                                                    │
│ 7. Navigate to project:                          │
│    $ cd ~/mini_notion                             │
│                                                    │
│ 8. Pull latest changes:                          │
│    $ git pull origin main                         │
│                                                    │
│    Result:                                        │
│    - Files updated on disk                        │
│    - NASA template changes applied                │
│                                                    │
└─────────────────────────────────────────────────┘
                     ↓
┌─ LIVE PHASE ──────────────────────────────────────┐
│                                                    │
│ 9. User visits: https://anama.pythonanywhere.com │
│    /integrations/nasa-apod/                       │
│                                                    │
│ 10. Django processes request:                     │
│     - Loads updated template from disk            │
│     - Renders with latest styling                 │
│     - Sends HTML to browser                       │
│                                                    │
│ 11. Browser renders improved layout:             │
│     ✅ Better spacing                             │
│     ✅ Professional shadows                       │
│     ✅ Two-column layout                          │
│     ✅ Emoji icons                                │
│                                                    │
└─────────────────────────────────────────────────┘
```

---

## Technical Specifics for Your Template

### File Change Tracking

```bash
# Before push
git status
# On branch main
# Changes not staged for commit:
#   modified:   mysite/mini_notion/templates/mini_notion/nasa_apod_demo.html

# After commit
git log --oneline -1
# abc1234 Improve NASA APOD template: spacing and styling

# Verify changes in git
git show abc1234:mysite/mini_notion/templates/mini_notion/nasa_apod_demo.html
# Shows the updated file content
```

### Network Flow

```
Local Git    →  [PUSH]  →  GitHub  
             ←  [ACK]   ←
                         
PythonAnywhere Git  →  [PULL]  →  GitHub
                   ←  [Data]   ←
```

### Django Template Loading Process

When user visits `/integrations/nasa-apod/`:

```python
# urls.py routes request to view
# mini_notion/views.py
def nasa_apod_demo(request):
    # ... get data ...
    return render(
        request,
        'mini_notion/nasa_apod_demo.html',  # Template path
        context  # Data passed to template
    )

# Django Template Loader:
# 1. Search in APP_DIRS (mini_notion/templates/)
# 2. Load: mini_notion/nasa_apod_demo.html from DISK
# 3. Parse: Replace {{ variables }} with context data
# 4. Render: Convert to HTML
# 5. Return: Send to browser
```

**Critical**: File is read from disk every time! (Step 2)

---

## Checklist: Before & After

### Before Deployment

- [ ] Template edited locally
- [ ] No syntax errors in HTML
- [ ] Tested with `runserver`
- [ ] Browser shows expected changes
- [ ] File saved (Ctrl+S)
- [ ] Ready to commit

### During Deployment

- [ ] `git add` only template files (or all changed files)
- [ ] `git commit` with descriptive message
- [ ] `git push` completes successfully
- [ ] GitHub web shows new commit
- [ ] SSH into PythonAnywhere successfully
- [ ] `git pull` runs without errors

### After Deployment

- [ ] New commit visible on GitHub
- [ ] File updated on PythonAnywhere (`cat` the file to verify)
- [ ] No git merge conflicts
- [ ] Website still loads (no server errors)
- [ ] Changes visible in browser (hard refresh)
- [ ] Old cached page not showing

---

## Troubleshooting Scenarios

### Scenario 1: Changes Not Visible

**Likely cause**: Browser cache

**Solution**:
```bash
# Hard refresh browser
# Mac: Cmd+Shift+R
# Windows: Ctrl+Shift+R
# Or: Clear browser cache entirely

# Verify file on server:
ssh -l AnaMa ssh.pythonanywhere.com
cat ~/mini_notion/mysite/mini_notion/templates/mini_notion/nasa_apod_demo.html | grep "mt-3"
# Should show: <h2 class="mb-5 mt-3">
```

### Scenario 2: Git Push Fails

**Error**: `fatal: unable to access 'https://...' : The requested URL returned error: 403`

**Solution**:
```bash
# Check git remote
git remote -v
# Update to SSH if using HTTPS with wrong credentials
git remote set-url origin git@github.com:anamasiliuniene/mini_notion.git

# Or use correct credentials:
git push origin main  # Will prompt for password
```

### Scenario 3: Git Pull Conflicts

**Error**: `CONFLICT (content changed)`

**Solution**:
```bash
# Check status
git status

# Accept your version:
git checkout --ours mysite/mini_notion/templates/mini_notion/nasa_apod_demo.html

# Complete merge:
git add .
git commit -m "Resolve merge conflict"
git push origin main
```

### Scenario 4: Django Template Error

**Error**: `TemplateDoesNotExist: mini_notion/nasa_apod_demo.html`

**Solution**:
```bash
# Verify file path
ls -la ~/mini_notion/mysite/mini_notion/templates/mini_notion/nasa_apod_demo.html

# Check INSTALLED_APPS in settings.py
# Should include: 'mini_notion'

# Check TEMPLATES settings
grep -A 10 "TEMPLATES" ~/mini_notion/mysite/mysite/settings.py
```

---

## Performance Considerations

### Template Caching in Production

Django can cache templates for performance:

```python
# In settings.py (production only)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'loaders': [
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]),
            ],
        },
    },
]
```

In this case, **you would need to restart** after template changes.

**Check your current setup**:
```bash
cat ~/mini_notion/mysite/mysite/settings.py | grep -A 20 "TEMPLATES"
```

If you see `cached.Loader`, that's why changes might not show instantly.

### Your Current Setup

Based on your settings.py, you have:
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                ...
            ],
        },
    },
]
```

✅ **No template caching configured** = Changes show immediately! ✅

---

## Git History & Rollback

### If You Need to Revert Changes

```bash
# See commit history
git log --oneline -10

# View specific commit
git show <commit-hash>

# Revert commit (creates new reverse commit)
git revert <commit-hash>
git push origin main

# Or hard reset (dangerous - rewrites history)
git reset --hard <commit-hash>
git push origin main --force
```

### On PythonAnywhere After Revert

```bash
cd ~/mini_notion
git pull origin main
# Old template version is restored
```

---

## Summary of Key Points

### ✅ What Auto-Reloads (No Restart Needed)
- Template files (.html)
- Static assets served by WhiteNoise
- Context processor functions (generally)

### ❌ What Needs Restart (Click "Reload" button)
- Python code (views.py, models.py, forms.py)
- settings.py configuration changes
- URL routing changes (urls.py)
- Middleware changes
- Database migrations

### 🔄 Version Control Flow
```
Edit (Local) → Test (Local) → Commit (Local) → Push (GitHub) → Pull (Server)
```

### ⏱️ Timeline
- Edit → Commit: < 1 min
- Commit → Push: < 1 min
- Push → Pull: < 1 min
- Pull → Live: Immediate (hard refresh)
- **Total: ~5 minutes**

---

## Your Specific Template Changes

### File: `mysite/mini_notion/templates/mini_notion/nasa_apod_demo.html`

**Lines changed**: 8, 10, 25, 26, 27, 30, 44-47, 52, 60, 62, 67-75, 76-80, 82, 85, 90, 91

**Change type**: Styling & UX improvements (no logic changes)

**Requires restart?**: ❌ No - pure template changes

---

## Next: Execute Deployment

You're ready! Follow DEPLOY_TEMPLATE_NOW.md for exact commands.

**Total time: 5 minutes** ⏱️
**Complexity: Low** ✅
**Risk: None** (pure front-end changes) ✅

