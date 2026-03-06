# How to Apply Template Changes to Deployed Project (PythonAnywhere)

## Quick Summary
Templates in Django are dynamically loaded from files at request time. **You do NOT need to restart the app** to see template changes on PythonAnywhere - just follow these steps:

---

## Step-by-Step Process

### 1. **Edit Template Locally** (What you just did!)
   - Edit HTML files in `/mysite/mini_notion/templates/`
   - Test locally with `python manage.py runserver`
   - Verify changes look good before pushing

### 2. **Push Changes to GitHub**
```bash
cd /Users/anamasiliuniene/PycharmProjects/PythonProject38
git add mysite/mini_notion/templates/
git commit -m "Update NASA APOD template: improve spacing and styling"
git push origin main
```

### 3. **Pull Changes on PythonAnywhere**
   
SSH into your PythonAnywhere console:
```bash
ssh -l AnaMa ssh.pythonanywhere.com
# Navigate to project
cd ~/mini_notion
# Pull latest changes
git pull origin main
```

Or use PythonAnywhere Web Console:
- Go to your PythonAnywhere account dashboard
- Click "Web" tab
- Under "Code" section, click on "Web console"
- Run: `cd ~/mini_notion && git pull origin main`

### 4. **Template Changes Take Effect Immediately** ✅
   - Django reloads templates on every request (in production)
   - No restart needed for template-only changes
   - Visit your URL: https://anama.pythonanywhere.com/integrations/nasa-apod/

---

## When You NEED to Reload the App

You **MUST reload your app** only when you change:
- ✅ Python code (views, models, urls)
- ✅ Settings.py configuration
- ✅ Static files (CSS, JS, images)
- ✅ Dependencies (requirements.txt)

You do **NOT need to reload** for:
- ✅ HTML/Template files (.html)
- ✅ Template content changes

### How to Reload App on PythonAnywhere:
1. Go to PythonAnywhere Dashboard
2. Click "Web" tab
3. Scroll to your app configuration
4. Click the green "Reload" button
5. Wait 5-10 seconds for reload to complete

---

## Detailed Workflow for Regular Updates

### Local Development Loop
```bash
# 1. Make changes
# (Edit templates/views/etc locally)

# 2. Test locally
cd ~/PycharmProjects/PythonProject38/mysite
python manage.py runserver

# 3. Visit http://localhost:8000 to verify

# 4. Push to GitHub
cd ../..
git add .
git commit -m "Descriptive message"
git push origin main
```

### Deployment to PythonAnywhere
```bash
# On PythonAnywhere console:
cd ~/mini_notion

# 1. Pull changes
git pull origin main

# 2. If you changed Python code/settings:
source .venv/bin/activate
python mysite/manage.py migrate  # if models changed
python mysite/manage.py collectstatic --noinput  # if static files changed

# 3. Go to PythonAnywhere dashboard and click "Reload"
# (if you changed Python code/settings/static files)
```

---

## What You Changed Today

✅ **Template improvements applied:**
- Added `mt-3` margin-top to `<h2>` for spacing below heading
- Increased alert bottom margin from `mb-4` to `mb-5`
- Improved form styling with `shadow-sm` class
- Aligned button vertically with fields using `align-items-end`
- Added calendar icon (📅) to date display
- Better column spacing with `g-4` (gap) class
- Added emoji icons for better UX (🔍, 📹, 📸)
- Improved card styling with `shadow-sm` and `bg-light` header
- Better handling of video content

---

## Troubleshooting Template Changes

### Changes not showing?

1. **Clear browser cache:**
   - Hard refresh: `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R` (Windows)
   - Or clear cookies/cache for the site

2. **Verify file was pushed:**
   ```bash
   git log --oneline -5  # Check recent commits
   git show <commit-hash>:mysite/mini_notion/templates/mini_notion/nasa_apod_demo.html
   ```

3. **Verify file exists on PythonAnywhere:**
   ```bash
   ls -la ~/mini_notion/mysite/mini_notion/templates/mini_notion/
   cat ~/mini_notion/mysite/mini_notion/templates/mini_notion/nasa_apod_demo.html
   ```

4. **Check template syntax:**
   ```bash
   cd ~/mini_notion
   source .venv/bin/activate
   python mysite/manage.py check
   ```

5. **Check Django logs on PythonAnywhere:**
   - Dashboard > "Web" tab
   - Look for error log link
   - Check for template syntax errors

---

## Pro Tips

1. **Use version control for templates too:**
   - Always commit template changes
   - Use descriptive messages
   - Easy to rollback if needed

2. **Test locally first:**
   - Changes to templates can affect layout
   - Always test on http://localhost:8000 before pushing

3. **Use Django template tags properly:**
   - `{% if %}` conditions work the same in production
   - Static file references use `{% static %}` tag

4. **Monitor PythonAnywhere logs:**
   - If something breaks, check the error log
   - Template syntax errors will show there

5. **Keep backups:**
   - Before major changes, create a git branch
   - Easy to revert if needed: `git revert <commit>`

---

## Summary Command Sequence

```bash
# Local
cd ~/PycharmProjects/PythonProject38
# Edit templates...
python mysite/manage.py runserver  # Test
git add -A
git commit -m "Update NASA APOD template styling"
git push origin main

# On PythonAnywhere (via SSH or Web Console)
cd ~/mini_notion
git pull origin main
# Done! Changes live immediately for templates

# If you changed Python code:
source .venv/bin/activate
python mysite/manage.py migrate  # if needed
# Then click "Reload" in PythonAnywhere dashboard
```

---

## Current Status ✅

Your template has been updated with:
- Better spacing between heading and form
- Improved two-column layout
- Enhanced styling and icons
- Better video handling

**Next:** Push to GitHub, pull on PythonAnywhere, and view the updated page!

