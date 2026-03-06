# 🔄 Update PythonAnywhere with Latest Changes

## Quick Update Steps

### 1️⃣ Open PythonAnywhere Bash Console
- Go to https://www.pythonanywhere.com
- Click on **"Consoles"** tab
- Click **"Bash"** to open a new console (or use existing one)

### 2️⃣ Navigate to Your Project
```bash
cd ~/mini_notion
```

### 3️⃣ Pull Latest Changes
```bash
git pull
```

### 4️⃣ Reload Your Web App
Go to **"Web"** tab and click the green **"Reload"** button

---

## What Was Just Updated (March 6, 2026)

### ✅ NASA APOD Demo Fixes
- **Dark Mode**: Explanation text now properly adapts to dark/light mode (removed hardcoded `color: #333;`)
- **Cleaner UI**: Removed calendar emoji (📅) from date display in header

### ✅ Security Fix
- Removed database files from git tracking (db.sqlite3, backups)

---

## Troubleshooting

### If `git pull` shows conflicts:
```bash
git stash           # Save local changes
git pull            # Pull updates
git stash pop       # Restore local changes (if needed)
```

### If you need to force pull:
```bash
git fetch origin
git reset --hard origin/main
```

### Check current git status:
```bash
git status
git log -1 --oneline    # See last commit
```

---

## Repository Info
- **GitHub Account**: 1anamasiliuniene-netizen
- **Repository**: https://github.com/1anamasiliuniene-netizen/mini_notion
- **Branch**: main

---

## After Pulling Changes

1. ✅ Check that files updated: `ls -l mysite/mini_notion/templates/mini_notion/`
2. ✅ Go to Web tab in PythonAnywhere
3. ✅ Click **Reload** button (green button at top)
4. ✅ Test your site: Check NASA APOD page in dark mode

---

**Latest commit**: "Fix NASA APOD dark mode: remove hardcoded text color and calendar emoji"

