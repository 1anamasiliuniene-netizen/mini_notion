# 🔐 GITHUB AUTHENTICATION FIX - STEP BY STEP

**Error:** `fatal: unable to access 'https://github.com/anamasiliuniene/mini_notion.git/': The requested URL returned error: 403`

**Cause:** HTTPS authentication is not working. Need to use Personal Access Token or SSH.

---

## ✅ SOLUTION 1: USE PERSONAL ACCESS TOKEN (Easiest)

### Step 1: Create Token on GitHub
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Name: `git-cli`
4. Expiration: 90 days (or custom)
5. **Check ONLY:** `repo` (Full control of private repositories)
6. Click "Generate token"
7. **COPY the token immediately** (you won't see it again!)

### Step 2: Use Token for Push

When Git asks for password, paste the token (not your password):

```bash
cd /Users/anamasiliuniene/PycharmProjects/PythonProject38
git push origin main
```

When prompted:
- Username: `anamasiliuniene`
- Password: `paste your token here` (won't display - that's normal)

---

## ✅ SOLUTION 2: USE SSH KEY (Recommended Long-term)

### Step 1: Check if SSH Key Exists
```bash
ls -la ~/.ssh/id_ed25519
```

If it exists, skip to Step 3. If not, create one:

### Step 2: Create SSH Key (if needed)
```bash
ssh-keygen -t ed25519 -C "your-github-email@example.com"
```
- Press Enter for all prompts (use defaults)
- You'll get: `id_ed25519` and `id_ed25519.pub`

### Step 3: Add Public Key to GitHub
```bash
cat ~/.ssh/id_ed25519.pub
```
Copy the output (starts with `ssh-ed25519`), then:

1. Go to: https://github.com/settings/keys
2. Click "New SSH key"
3. Title: "MacBook Air"
4. Paste the key
5. Click "Add SSH key"

### Step 4: Change Git Remote to SSH
```bash
cd /Users/anamasiliuniene/PycharmProjects/PythonProject38
git remote set-url origin git@github.com:anamasiliuniene/mini_notion.git
```

### Step 5: Push
```bash
git push origin main
```

---

## ⚡ QUICK FIX - RIGHT NOW

**Try this command to push with HTTPS + token:**

```bash
cd /Users/anamasiliuniene/PycharmProjects/PythonProject38
git config --global user.name "anamasiliuniene"
git config --global user.email "your-email@github.com"
git config --global credential.helper osxkeychain
git push origin main
```

When it asks for password, use your Personal Access Token (not your GitHub password!)

---

## 🔄 IF THAT DOESN'T WORK

### Clear Cached Credentials
```bash
git credential-osxkeychain erase
host=github.com
protocol=https
```
Then try pushing again.

### Use Environment Variable
```bash
cd /Users/anamasiliuniene/PycharmProjects/PythonProject38
export GIT_ASKPASS=/usr/bin/ssh-askpass
git push https://your-token@github.com/anamasiliuniene/mini_notion.git main
```

Replace `your-token` with your actual personal access token.

---

## 📋 CHECKLIST - DO THIS NOW

- [ ] Generate Personal Access Token from GitHub
- [ ] Copy the token (save it somewhere safe)
- [ ] Run: `cd /Users/anamasiliuniene/PycharmProjects/PythonProject38`
- [ ] Run: `git push origin main`
- [ ] When prompted for password, paste your token
- [ ] Press Enter

---

## ✅ WHAT SUCCESS LOOKS LIKE

```
Enumerating objects: X, done.
Counting objects: 100% (X/X), done.
Compressing objects: 100% (X/X), done.
Writing objects: 100% (X/X), done.
To github.com:anamasiliuniene/mini_notion.git
   7515cdd...xxxxx main -> main
```

---

## 🎊 AFTER SUCCESSFUL PUSH

1. Go to: https://github.com/anamasiliuniene/mini_notion
2. Refresh the page
3. You should see:
   - New commit with your deployment files
   - Files like `00_START_HERE.md`, `DEPLOYMENT_SETTINGS.md`, etc.
   - Timestamp: "just now"

---

## 🔑 PERSONAL ACCESS TOKEN INSTRUCTIONS (RECOMMENDED)

### Creating Token:
1. https://github.com/settings/tokens/new
2. Token name: `git-deployment`
3. Expiration: 90 days
4. Scopes: Check **only** `repo`
5. Click "Generate token"
6. **COPY IT IMMEDIATELY**

### Using Token:
When Git prompts:
```
Username for 'https://github.com': anamasiliuniene
Password for 'https://anamasiliuniene@github.com': ghp_xxxxxxxxxxxxxxxxxxxx
```

---

**Choose SSH or Token method and follow the steps above!** 🚀

Which method do you prefer? Or reply with "TOKEN" and I'll help you generate one!

