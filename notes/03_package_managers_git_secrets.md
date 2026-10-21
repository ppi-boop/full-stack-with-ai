# 03 — Package Managers, Git & Secret Management Cheat Sheet

> **Quick Summary:** npm vs npx, Python virtual environments, Git staging/merge/rebase mechanics, and secret management lifecycle.

---

## 1. Package Managers: JavaScript vs Python

### JavaScript (`npm` & `npx`)
* **`package.json`:** Declares dependencies and versions.
* **`package-lock.json`:** Freezes exact sub-dependency versions and integrity hashes. **Must be committed to Git.**
* **`node_modules/`:** The local folder containing downloaded packages. **Never commit to Git.**
* **`dependencies` vs `devDependencies`:**
  * `dependencies`: Production code needed at runtime (`express`, `react`, `zod`).
  * `devDependencies`: Build, test, and typecheck tooling (`vitest`, `eslint`, `typescript`). Installed with `npm install -D <pkg>`.
* **`npx`:** Executes a package directly from a temporary cache without installing it globally (`npx create-next-app@latest`).

### Python Virtual Environments (`.venv`)
* **The Problem:** Python installs packages globally across the OS by default. Different projects requiring different library versions will conflict.
* **The Solution:** Isolated project sandboxes via `venv`.
  ```bash
  # Setup & Activation
  python3 -m venv .venv
  source .venv/bin/activate       # Mac/Linux (Look for (.venv) in prompt!)
  .venv\Scripts\Activate.ps1      # Windows PowerShell

  # Install & Freeze
  pip install requests
  pip freeze > requirements.txt
  ```

---

## 2. Git Architecture & Workflow

### The 3 Stages
1. **Working Directory:** Files modified on disk.
2. **Staging Area (`git add`):** Selected changes queued for the next commit.
3. **Local Repository (`git commit`):** Permanent historical snapshots.

### Core Commands Matrix
```bash
git init                            # Initialize local repo
git add .                           # Stage all modifications
git commit -m "feat(auth): add jwt" # Commit with Conventional Commits format
git switch -c feature/login         # Create and switch to new branch
git switch main                     # Switch back to main branch
git merge feature/login             # Merge branch changes into main
git log --oneline --graph           # Visualize commit history tree
```

### Git Merge vs Git Rebase
* **`git merge`:** Creates an explicit "merge commit" combining branches. Preserves true historical timeline. Safe for shared branches.
* **`git rebase`:** Replays your branch's commits on top of another base. Creates a clean, linear commit history. **Rule: Never rebase a public/shared branch.**

### Git Stash
* Temporarily shelves uncommitted changes to allow switching branches or pulling:
  ```bash
  git stash       # Save working state to stash stack
  git switch main # Perform other task
  git switch -    # Return to previous branch
  git stash pop   # Restore stashed changes and remove from stack
  ```

### Git Fetch vs Git Pull
* **`git fetch`:** Downloads remote commits from GitHub to local cache without modifying working files.
* **`git pull`:** Executes `git fetch` followed immediately by `git merge`.

---

## 3. Merge Conflicts Resolution
When two branches modify the same line:
```text
<<<<<<< HEAD (Current branch)
const PORT = 3000;
=======
const PORT = 8080;
>>>>>>> feature/config (Incoming branch)
```
1. Open the file and manually edit to the desired code.
2. Delete `<<<<<<<`, `=======`, and `>>>>>>>` markers.
3. Stage and commit: `git add <file>` $\rightarrow$ `git commit -m "fix: resolve port conflict"`.

---

## 4. Secret Management & `.env`

### Core Principles
* **`.env`:** Contains local secret keys (`DATABASE_URL`, `OPENAI_API_KEY`). **Must be in `.gitignore`.**
* **`.env.example`:** Committed template with empty/dummy values for team setup reference.
* **Node 20+ Native Env Loading:**
  ```bash
  node --env-file=.env server.js
  ```

### Leaked Key Incident Response Protocol
If a secret or API key is committed to GitHub:
1. **REVOKE / INVALIDATE IMMEDIATELY:** Delete or rotate the key at the provider console (OpenAI, AWS, Stripe).
2. **UPDATE SECRETS:** Generate new keys and update local `.env` and production host variables.
3. **AUDIT LOGS:** Inspect provider usage and billing logs for unauthorized access during the exposure window.
4. **PURGE REPO HISTORY:** Use `git-filter-repo` or BFG to permanently scrub the key from Git history. Simply committing a deletion does NOT remove it from past commits!
