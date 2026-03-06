# 🔑 SSH KEYS CREATED - ADD THEM TO GITHUB NOW

**Created:** March 6, 2026  
**Status:** SSH keys generated, ready to add to GitHub

---

## 📋 YOUR SSH PUBLIC KEYS

### 1️⃣ Main Account Key (ana.masiliuniene@gmail.com)

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAINKrRtwyvBTiDjN0Z6ZVPahr/IRiiD6NI0nmOTYKTb4C ana.masiliuniene@gmail.com
```

### 2️⃣ Showcase Account Key (1ana.masiliuniene@gmail.com)

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIL5rfp3T6HVH210bPydklZgZrdcGKTHceojdWAMZ1FCJ 1ana.masiliuniene@gmail.com
```

---

## ✅ HOW TO ADD KEYS TO GITHUB

### For Main Account (ana.masiliuniene@gmail.com):

1. **Log into GitHub** with ana.masiliuniene@gmail.com account
2. **Go to:** https://github.com/settings/keys
3. **Click:** "New SSH key"
4. **Title:** MacBook Main
5. **Key type:** Authentication Key
6. **Key:** Copy and paste the entire first SSH key above
7. **Click:** "Add SSH key"

### For Showcase Account (1ana.masiliuniene@gmail.com):

1. **Log into GitHub** with 1ana.masiliuniene@gmail.com account
2. **Go to:** https://github.com/settings/keys
3. **Click:** "New SSH key"
4. **Title:** MacBook Showcase
5. **Key type:** Authentication Key
6. **Key:** Copy and paste the entire second SSH key above
7. **Click:** "Add SSH key"

---

## 🎯 NEXT STEPS

After adding both keys to GitHub:

### Update mini_notion repo (ana.masiliuniene@gmail.com):
```bash
cd /Users/anamasiliuniene/PycharmProjects/PythonProject38
git remote set-url origin git@github-ana:anamasiliuniene/mini_notion.git
git push origin main
```

### For future showcase repos (1ana.masiliuniene@gmail.com):
```bash
git clone git@github-ana-showcase:1anamasiliuniene/showcase-repo.git
# Then push normally: git push origin main
```

---

## 🚀 AFTER ADDING KEYS

You can push like normal:
```bash
git push origin main
```

No tokens, no passwords, just works! ✅

---

## 🔒 SSH KEY LOCATIONS

Your keys are stored at:
- `~/.ssh/id_ed25519_ana` (private - keep safe)
- `~/.ssh/id_ed25519_ana.pub` (public - paste to GitHub)
- `~/.ssh/id_ed25519_ana_showcase` (private - keep safe)
- `~/.ssh/id_ed25519_ana_showcase.pub` (public - paste to GitHub)

---

*SSH keys generated March 6, 2026*

