# ⚡ COMMAND REFERENCE: Copy-Paste Deployment

## What to Do Right Now

Copy-paste these exact commands in order:

---

## STEP 1: Commit Locally

```bash
cd /Users/anamasiliuniene/PycharmProjects/PythonProject38
git commit -am "Improve NASA APOD template: better spacing and styling"
```

**Expected output:**
```
[main abc1234] Improve NASA APOD template: better spacing and styling
 1 file changed, 15 insertions(+), 5 deletions(-)
```

---

## STEP 2: Push to GitHub

```bash
git push origin main
```

**Expected output:**
```
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Delta compression using up to 8 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 789 bytes | 789.00 KiB/s, done.
Total 3 (delta 2), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (2/2), completed with 0 local objects.
To github.com:anamasiliuniene/mini_notion.git
   old_hash..new_hash  main -> main
```

---

## STEP 3: SSH & Pull on PythonAnywhere

```bash
ssh -l AnaMa ssh.pythonanywhere.com
cd ~/mini_notion
git pull origin main
exit
```

**Prompts & Expected Outputs:**

```
# When you run ssh:
AnaMa@ssh.pythonanywhere.com's password: [enter your PythonAnywhere password]

# When you run git pull:
remote: Enumerating objects: 5, done.
remote: Counting objects: 100% (5/5), done.
remote: Total 3 (delta 2), reused 0 (delta 0)
Unpacking objects: 100% (3/3), done.
Updating abc1234..def5678
Fast-forward
 mysite/mini_notion/templates/mini_notion/nasa_apod_demo.html | 20 ++++++++-------
 1 file changed, 15 insertions(+), 5 deletions(-)

# When you run exit:
[connection closes, you're back on your Mac]
```

---

## STEP 4: Verify in Browser

### Hard Refresh Browser

**Mac:**
```
Press: Cmd + Shift + R
```

**Windows:**
```
Press: Ctrl + Shift + R
```

### Visit URL
```
https://anama.pythonanywhere.com/integrations/nasa-apod/
```

### What You Should See
✅ Better spacing between heading and form  
✅ Professional shadows on cards  
✅ Two-column layout (image left, text right)  
✅ Calendar emoji (📅) next to date  
✅ Professional appearance overall  

---

## All Commands Combined (One-Liner)

If you want to do it all at once:

```bash
cd /Users/anamasiliuniene/PycharmProjects/PythonProject38 && git commit -am "Improve NASA APOD template: better spacing and styling" && git push origin main && echo "Now SSH into PythonAnywhere and run: cd ~/mini_notion && git pull origin main"
```

Then separately:
```bash
ssh -l AnaMa ssh.pythonanywhere.com
cd ~/mini_notion && git pull origin main && exit
```

---

## Troubleshooting Commands

### If Git Commit Says "Nothing to commit"
```bash
git status
# Check if files are already committed
# If not, try:
git add mysite/mini_notion/templates/mini_notion/nasa_apod_demo.html
git commit -m "Improve NASA APOD template"
```

### If Git Push Fails (403 Error)
```bash
# Check your git config
git config --list | grep url

# Reset with SSH:
git remote set-url origin git@github.com:anamasiliuniene/mini_notion.git
git push origin main
```

### If SSH Connection Fails
```bash
# Check SSH key:
ssh -vvv -l AnaMa ssh.pythonanywhere.com
# (verbose output shows what's happening)

# Or try HTTPS instead:
# (but use Git credentials)
```

### If Git Pull on PythonAnywhere Shows Errors
```bash
cd ~/mini_notion
git status
git log --oneline -3
cat mysite/mini_notion/templates/mini_notion/nasa_apod_demo.html | head -10
# (verify file was updated)
```

### If Changes Still Not Visible
```bash
# On PythonAnywhere, verify file was updated:
ls -la ~/mini_notion/mysite/mini_notion/templates/mini_notion/nasa_apod_demo.html
# Check modification date

# Verify content changed:
grep "mt-3" ~/mini_notion/mysite/mini_notion/templates/mini_notion/nasa_apod_demo.html
# Should show: <h2 class="mb-5 mt-3">
```

---

## Environment Variables Reference

### If You Need to Check PythonAnywhere Settings

```bash
ssh -l AnaMa ssh.pythonanywhere.com
cat ~/.env
# (shows your environment variables)
```

---

## Git Status Commands

### Check Current Status
```bash
cd /Users/anamasiliuniene/PycharmProjects/PythonProject38
git status
```

### See What Changed
```bash
git diff mysite/mini_notion/templates/mini_notion/nasa_apod_demo.html
```

### See Commit History
```bash
git log --oneline -5
git log --oneline -5 -- mysite/mini_notion/templates/mini_notion/nasa_apod_demo.html
```

### See Remote Status
```bash
git remote -v
git branch -a
```

---

## PythonAnywhere SSH Reference

### Basic SSH Commands
```bash
# Connect
ssh -l AnaMa ssh.pythonanywhere.com

# List files
ls -la ~/mini_notion/

# Navigate
cd ~/mini_notion/mysite

# View file
cat nasa_apod_demo.html

# Count lines
wc -l nasa_apod_demo.html

# Search in file
grep "mt-3" nasa_apod_demo.html

# Exit SSH
exit
```

---

## Django Commands (Local Only)

### Test Server
```bash
cd /Users/anamasiliuniene/PycharmProjects/PythonProject38/mysite
python manage.py runserver
# Visit http://localhost:8000
# Press Ctrl+C to stop
```

### Check for Errors
```bash
cd /Users/anamasiliuniene/PycharmProjects/PythonProject38/mysite
python manage.py check
```

---

## Verification Commands

### After Commit
```bash
git log --oneline -1
# Should show your new commit
```

### After Push
```bash
git log --oneline -1
git log origin/main --oneline -1
# Both should match
```

### After Pull on PythonAnywhere
```bash
# On PythonAnywhere:
cd ~/mini_notion
git log --oneline -1
# Should show your new commit

# Check file modification time:
stat mysite/mini_notion/templates/mini_notion/nasa_apod_demo.html
# Should be recent (within last few minutes)
```

---

## Complete Sequence (Copy-Paste Version)

```bash
# LOCAL - Commit and Push
cd /Users/anamasiliuniene/PycharmProjects/PythonProject38
git commit -am "Improve NASA APOD template: better spacing and styling"
git push origin main
git log --oneline -1

# Wait for output showing successful push...

# PYTHONANYWHERE - SSH and Pull
ssh -l AnaMa ssh.pythonanywhere.com
cd ~/mini_notion
git pull origin main
git log --oneline -1
exit

# BROWSER - Verify
# Hard refresh: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)
# Visit: https://anama.pythonanywhere.com/integrations/nasa-apod/
# Check for improved spacing and styling
```

---

## Time Breakdown

```
cd to directory:         5 sec
git commit:              2 sec  
git push:              10 sec
git pull on server:    15 sec
Hard refresh:           2 sec
─────────────────────────────
Total:              34 seconds
Plus SSH login:      30 seconds
──────────────────────────────
Grand Total:         ~1 minute
```

---

## Success Indicators

✅ After `git commit`: See "[main abc1234] Improve NASA APOD template..."  
✅ After `git push`: See "To github.com:...main -> main"  
✅ After `git pull`: See "Updating...Fast-forward" or "Already up to date"  
✅ After refresh: See new styling in browser  

---

## Next Time

Same commands, every time:
```
git commit -am "message"
git push origin main
# On PythonAnywhere:
git pull origin main
```

---

## Got Stuck?

Check these in order:
1. `git status` - what changed?
2. `git log --oneline -3` - recent commits?
3. `git diff HEAD` - what exactly changed?
4. Browser dev tools (F12) - is CSS loading?
5. PythonAnywhere error log - any errors?

---

**Ready? Run the commands above!** 🚀

