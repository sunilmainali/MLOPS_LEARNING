# Git & GitHub Documentation

A comprehensive guide to Git version control and GitHub collaboration.

---

## 📋 Table of Contents

- [Git Workflow](#git-workflow)
- [Getting Started](#getting-started)
- [Essential Git Commands](#essential-git-commands)
- [Commit Message Conventions](#commit-message-conventions)
- [Understanding .gitignore](#understanding-gitignore)
- [Branching Strategies](#branching-strategies)
- [Merge vs Rebase](#merge-vs-rebase)
- [Undoing Changes](#undoing-changes)
- [Git Stashing](#git-stashing)

---

## Git Workflow

```
Working Files ──(git add)──► Staging Area ──(git commit)──► Local Repository ──(git push)──► Remote Repository
```

| Stage | Description |
|-------|-------------|
| **Working Directory** | Your local files where you make changes |
| **Staging Area** | Files ready to be committed |
| **Local Repository** | Your local Git history |
| **Remote Repository** | GitHub/GitLab hosted repository |

---

## Getting Started

### Initial Setup

```bash
# Configure your identity
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Initialize a new repository
git init

# Clone an existing repository
git clone <repository-url>
```

### Connecting to GitHub

```bash
# Create a new repository on GitHub, then:
echo "# project-name" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/username/repository.git
git push -u origin main
```

---

## Essential Git Commands

### Repository Info

```bash
git status          # Check the status of your working directory
git remote -v       # View remote repository URLs
git log             # View commit history
git log --oneline   # Compact commit history
```

### Making Changes

```bash
git add <filename>      # Stage a specific file
git add .               # Stage all changes
git commit -m "message" # Commit staged changes
git push origin <branch> # Push to remote
```

### Syncing with Remote

```bash
git pull origin <branch>   # Fetch and merge remote changes
git fetch origin <branch>  # Fetch remote changes without merging
```

### Viewing Differences

```bash
git diff <filename>           # Compare working directory with staging
git diff <commit1> <commit2>  # Compare two commits
```

### Discarding Changes

```bash
git checkout -- <filename>  # Discard changes in working directory
git restore <filename>      # Restore file to last committed state
```

---

## Commit Message Conventions

Follow these prefixes for clear and consistent commit messages:

| Prefix | Purpose | Example |
|--------|---------|---------|
| `feat:` | New feature | `feat: add user authentication` |
| `fix:` | Bug fix | `fix: resolve login redirect issue` |
| `refactor:` | Code restructuring (no feature/fix) | `refactor: simplify validation logic` |
| `docs:` | Documentation updates | `docs: update API documentation` |
| `perf:` | Performance improvements | `perf: optimize database queries` |
| `style:` | Formatting only (indentation, whitespace) | `style: fix indentation in utils.py` |
| `chore:` | Maintenance tasks | `chore: update dependencies` |
| `test:` | Adding or updating tests | `test: add unit tests for auth module` |

### Examples

```bash
git commit -m "feat: add dark mode toggle to settings"
git commit -m "fix: prevent crash when user input is empty"
git commit -m "docs: add installation instructions to README"
```

---

## Understanding .gitignore

The `.gitignore` file tells Git which files and folders should **not** be tracked.

### Why Use .gitignore?

- 🔒 **Security**: Exclude sensitive files (passwords, API keys, `.env`)
- 📦 **Clean Repository**: Ignore auto-generated files (cache, logs)
- 💾 **Reduce Size**: Exclude large files (datasets, media)
- 🤝 **Easier Collaboration**: Prevent unnecessary merge conflicts

### Common .gitignore Patterns

```gitignore
# Python
__pycache__/
*.pyc
.env
venv/

# IDE
.vscode/
.idea/

# OS files
.DS_Store
Thumbs.db

# Data & Logs
*.log
data/
*.csv

# Jupyter Notebook checkpoints
.ipynb_checkpoints/
```

---

## Branching Strategies

### Basic Branch Commands

```bash
git branch                  # List branches
git branch <branch-name>    # Create new branch
git checkout <branch-name>  # Switch to branch
git checkout -b <branch>    # Create and switch to new branch
git branch -d <branch>      # Delete branch
```

---

## Merge vs Rebase

Both integrate changes from one branch to another, but they work differently.

### Merge

**Preserves the entire commit history** and creates a merge commit.

```
Before:
main: A
sm:   A ─── B

After merge:
main: A ─── B ─── M (merge commit)
```

```bash
git checkout main
git merge sm
```

### Rebase

**Rewrites commit history** to create a linear timeline.

```
Before:
main: A ─── B
sm:   A ─── C

After rebase:
main: A ─── B ─── C
```

```bash
git checkout sm
git rebase main
```

### When to Use Each

| Scenario | Recommended |
|----------|-------------|
| Public/shared branches | **Merge** (preserves history) |
| Local feature branches | **Rebase** (cleaner history) |
| Collaborating with others | **Merge** (safer) |
| Personal cleanup before PR | **Rebase** |

> ⚠️ **Warning**: Never rebase commits that have been pushed to a shared repository.

---

## Undoing Changes

### Git Reset

Reset moves the HEAD pointer and optionally modifies staging area and working directory.

```bash
# Soft Reset: Undo commit, keep changes staged
git reset --soft HEAD~1

# Hard Reset: Undo commit, discard all changes
git reset --hard HEAD~1
```

| Mode | HEAD | Staging | Working Dir |
|------|------|---------|-------------|
| `--soft` | ✅ Moves | ❌ Keeps | ❌ Keeps |
| `--mixed` (default) | ✅ Moves | ✅ Resets | ❌ Keeps |
| `--hard` | ✅ Moves | ✅ Resets | ✅ Resets |

**Use Cases:**
- `--soft`: Fix a wrong commit message
- `--hard`: Completely discard recent commits

### Git Revert

Creates a **new commit** that undoes changes (safer for shared branches).

```bash
git revert HEAD        # Revert the last commit
git revert <commit-id> # Revert a specific commit
```

---

## Git Stashing

Temporarily save changes without committing when you need to switch branches.

### Stash Workflow

```bash
# Save changes to stash
git stash

# List all stashes
git stash list

# Apply and remove the latest stash
git stash pop

# Apply stash without removing it
git stash apply

# Apply a specific stash
git stash apply stash@{2}

# Clear all stashes
git stash clear
```

### Use Case Example

```bash
# Working on feature, need to fix urgent bug
git stash                    # Save current work
git checkout main            # Switch to main
git checkout -b hotfix       # Create hotfix branch
# ... fix the bug ...
git commit -m "fix: urgent bug"
git checkout feature-branch  # Return to feature
git stash pop                # Restore saved work
```

---

## Quick Reference Card

| Action | Command |
|--------|---------|
| Initialize repo | `git init` |
| Clone repo | `git clone <url>` |
| Check status | `git status` |
| Stage files | `git add .` |
| Commit | `git commit -m "message"` |
| Push | `git push origin <branch>` |
| Pull | `git pull origin <branch>` |
| Create branch | `git checkout -b <name>` |
| Merge branch | `git merge <branch>` |
| View history | `git log --oneline` |
| Undo last commit | `git reset --soft HEAD~1` |
| Stash changes | `git stash` |

---

## Additional Resources

- [Official Git Documentation](https://git-scm.com/doc)
- [GitHub Docs](https://docs.github.com)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)

---

*Happy Coding! 🚀*
