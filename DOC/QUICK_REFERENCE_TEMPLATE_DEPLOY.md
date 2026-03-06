# QUICK REFERENCE CARD: Template Deployment

## 🎯 Question & Answer

**Q: How to apply template changes to deployed project?**

**A:** 
```
Edit → Commit → Push → Pull → Refresh
```

**That's it!** ✅

---

## 📋 Copy-Paste Commands

### Step 1: Commit Locally
```bash
cd /Users/anamasiliuniene/PycharmProjects/PythonProject38
git add mysite/mini_notion/templates/mini_notion/nasa_apod_demo.html
git commit -m "Improve NASA APOD template: spacing and styling"
```

### Step 2: Push to GitHub
```bash
git push origin main
```

### Step 3: Pull on PythonAnywhere (Choose A or B)

**A) SSH Method:**
```bash
ssh -l AnaMa ssh.pythonanywhere.com
cd ~/mini_notion && git pull origin main
exit
```

**B) Web Console:**
- Go to pythonanywhere.com
- Dashboard > Web > Web console
- Paste: `cd ~/mini_notion && git pull origin main`

### Step 4: Verify
- Hard refresh: **Cmd+Shift+R** (Mac) or **Ctrl+Shift+R** (Windows)
- Visit: https://anama.pythonanywhere.com/integrations/nasa-apod/

---

## 🔑 Core Concept

| Aspect | Details |
|--------|---------|
| **File Type** | HTML Template |
| **Location** | `mysite/mini_notion/templates/mini_notion/nasa_apod_demo.html` |
| **Needs Restart?** | ❌ NO |
| **Why?** | Templates load from disk on each request |
| **Deploy Time** | ~5 minutes |
| **Risk Level** | Low (styling only) |

---

## 📊 Changes Made

```
✅ mt-3 top margin on <h2>
✅ mb-5 spacing on alert
✅ shadow-sm on form card
✅ align-items-end on form
✅ bg-light header background
✅ 📅 emoji on date
✅ g-4 column spacing
✅ Better text styling
✅ Video media handling
✅ Emoji icons (🔍📹📸🎬)
```

---

## ✅ Checklist

- [ ] Commit changes
- [ ] Push to GitHub
- [ ] Pull on PythonAnywhere
- [ ] Hard refresh browser
- [ ] Verify at https://anama.pythonanywhere.com/integrations/nasa-apod/

**Done!** 🎉

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| Changes not showing | Hard refresh: Cmd+Shift+R |
| Git push fails | Check credentials: `git push origin main` |
| Changes still not live | SSH: `cat ~/mini_notion/mysite/.../nasa_apod_demo.html \| head -10` |
| Server error 500 | Check PythonAnywhere error log |

---

## 📚 Full Documentation

For detailed info, see:
- `DEPLOY_TEMPLATE_NOW.md` - Step-by-step with explanations
- `TECHNICAL_TEMPLATE_DEPLOYMENT.md` - How Django renders templates
- `TEMPLATE_CHANGES_VISUAL.md` - Before/after comparison

---

## ⏱️ Timeline

```
5 min: Commit + Push
1 min: Pull on PythonAnywhere
0 min: Changes live (no restart!)
────────────────────
6 min: Total time to deployment
```

---

## 🚀 Ready?

Execute the copy-paste commands above and your improved template will be live!

No backend restart needed. No Python restart needed. Just:
1. Commit
2. Push
3. Pull
4. Refresh browser

**That's the beauty of Django templates!** ✨

