# DVC (Data Version Control) - Complete Learning Guide for beginner

> **Official Documentation**: [https://doc.dvc.org/start](https://doc.dvc.org/start)

---

## Table of Contents

1. [What is DVC?](#what-is-dvc)
2. [Installation](#installation)
3. [Initializing DVC in a Project](#initializing-dvc-in-a-project)
4. [Tracking Data with DVC](#tracking-data-with-dvc)
5. [Understanding .dvc Files](#understanding-dvc-files)
6. [Version Control Workflow](#version-control-workflow)
7. [Switching Between Data Versions](#switching-between-data-versions)
8. [Remote Storage (Optional)](#remote-storage-optional)
9. [Practical Session Summary](#practical-session-summary)
10. [Common Commands Reference](#common-commands-reference)

---

## What is DVC?

**DVC (Data Version Control)** is an open-source tool that brings Git-like version control to data and machine learning models. It allows you to:

- **Track large datasets** and ML models alongside your code
- **Version your data** without storing it in Git (avoids bloating your repository)
- **Switch between data versions** as easily as switching Git branches
- **Share data** across team members using remote storage
- **Reproduce experiments** by linking code versions to data versions

### Key Concept

> *"DVC is your Git for data!"*

DVC doesn't actually store your data in Git. Instead, it stores small `.dvc` metadata files that point to your actual data. The data itself is stored in a cache (`.dvc/cache`) and optionally in remote storage.

```
┌─────────────────────────────────────────────────────────────┐
│                     Your Repository                         │
├─────────────────────────────────────────────────────────────┤
│  Git tracks:           │  DVC tracks:                       │
│  - Source code         │  - Large datasets                  │
│  - .dvc files          │  - ML models                       │
│  - dvc.yaml            │  - Any large binary files          │
│  - Configuration       │                                    │
└─────────────────────────────────────────────────────────────┘
```

---

## Installation

### Using uv (Recommended)
```bash
uv tool install dvc
# OR add to your project
uv add dvc
```

### Using pipx
```bash
pipx install dvc
```

### Using pip
```bash
pip install dvc
```

### Verify Installation
```bash
dvc --help
```

### What I Did:
```bash
$ uv add dvc
# This installed dvc v3.66.1 along with 70+ dependencies
```

---

## Initializing DVC in a Project

### Prerequisites
- Your project must be inside a **Git repository** (DVC works alongside Git)

### Steps

1. **Initialize Git (if not already done)**
   ```bash
   git init
   ```

2. **Initialize DVC**
   ```bash
   dvc init
   ```

3. **Commit DVC initialization files**
   ```bash
   git add .dvc .dvcignore
   git commit -m "Initialize DVC"
   ```

### Files Created by `dvc init`

| File/Folder | Purpose |
|-------------|---------|
| `.dvc/config` | DVC configuration (remotes, settings) |
| `.dvc/.gitignore` | Ensures cache and temp files aren't tracked by Git |
| `.dvc/cache/` | Local cache for your data (auto-created) |
| `.dvcignore` | Similar to .gitignore, patterns for DVC to ignore |

### Important Note

If you try to run `dvc init` in a subdirectory that's not tracked by Git, you'll get an error:

```bash
$ cd DVC/
$ dvc init
ERROR: failed to initiate DVC - C:\Learning\MLOPS\DVC is not tracked by any supported SCM tool (e.g. Git)
```

**Solution**: Run `dvc init` in the root of your Git repository (where `.git` folder exists).

### What I Did:
```bash
$ cd /c/Learning/MLOPS
$ git init   # Repository already existed
$ dvc init   # Initialized DVC repository
$ git commit -m "feat:dvc init"
$ git push origin main
```

---

## Tracking Data with DVC

### Adding Data to DVC Tracking

Use `dvc add` to start tracking a file or directory:

```bash
dvc add <path-to-data>
```

### Example:
```bash
dvc add DVC/data/data.txt
```

### What Happens Behind the Scenes

1. **DVC calculates MD5 hash** of your data file
2. **Moves data to cache** (`.dvc/cache/files/md5/...`)
3. **Creates a link** from original location to cache
4. **Creates `.dvc` file** with metadata
5. **Creates `.gitignore`** to prevent Git from tracking the actual data

```
Before dvc add:
  DVC/data/
    └── data.txt (your actual data)

After dvc add:
  DVC/data/
    ├── data.txt        (link to cache)
    ├── data.txt.dvc    (metadata - tracked by Git)
    └── .gitignore      (ignores data.txt from Git)
  
  .dvc/cache/files/md5/
    └── xx/
        └── xxxxxxxxx... (actual data stored here)
```

### Commit to Git

After running `dvc add`, you need to track the `.dvc` file with Git:

```bash
git add DVC/data/data.txt.dvc DVC/data/.gitignore
git commit -m "Add raw data"
```

### What I Did:
```bash
$ dvc add DVC/data/data.txt
# Output: To track the changes with git, run: git add 'DVC\data\data.txt.dvc'

$ git add DVC/data/
$ git commit -m "feat:added .dvc data file"
$ git push origin main
```

---

## Understanding .dvc Files

A `.dvc` file is a small YAML metadata file that describes your tracked data:

### Example: `data.txt.dvc`
```yaml
outs:
- md5: f16864777cc7c4301aa3a6445517b33a
  size: 125
  hash: md5
  path: data.txt
```

### Fields Explained

| Field | Description |
|-------|-------------|
| `md5` | Hash of the file content (unique identifier) |
| `size` | File size in bytes |
| `hash` | Hashing algorithm used (default: md5) |
| `path` | Relative path to the data file |

### Key Insight

> When you modify `data.txt` and run `dvc add` again, the `md5` hash changes. This is how DVC tracks different versions of your data!

---

## Version Control Workflow

### The DVC + Git Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    Data Change Workflow                      │
├─────────────────────────────────────────────────────────────┤
│  1. Modify your data file                                   │
│  2. dvc add <file>         → Updates .dvc file              │
│  3. git add <file>.dvc     → Stage metadata changes         │
│  4. git commit             → Commit version                 │
│  5. dvc push (optional)    → Upload to remote storage       │
│  6. git push               → Push to Git remote             │
└─────────────────────────────────────────────────────────────┘
```

### Updating Tracked Data

When you modify a DVC-tracked file:

```bash
# 1. Make changes to data.txt
echo "new content" >> DVC/data/data.txt

# 2. Update DVC tracking
dvc add DVC/data/data.txt

# 3. Commit the updated .dvc file
git add DVC/data/data.txt.dvc
git commit -m "Update dataset"
git push origin main
```

### What I Did:

I tracked multiple versions of `data.txt`:

**Version 1 (Initial):**
```
This is the first version of my data
```

**Version 2 (Updated):**
```
This is the first version of my data
again i switch to the second version of my data
```

**Version 3 (Current):**
```
This is the first version of my data
again i switch to the second version of my data

this is the third version of my data
```

Each update followed this pattern:
```bash
$ dvc add DVC/data/data.txt
$ git add 'DVC\data\data.txt.dvc'
$ git commit -m "Updated the data.txt.dvc file"
```

---

## Switching Between Data Versions

This is the **most powerful feature** of DVC - time travel for your data!

### The Two-Step Process

```bash
# Step 1: Checkout the .dvc file version with Git
git checkout <commit-hash> <path-to-dvc-file>

# Step 2: Sync the actual data with DVC
dvc checkout
```

### Example: Going Back to Previous Version

```bash
# See commit history
git log

# Go back one version
git checkout HEAD~1 DVC/data/data.txt.dvc
dvc checkout

# Commit the reversion
git commit DVC/data/data.txt.dvc -m "Revert dataset updates"
```

### Switching to a Specific Commit

```bash
# Checkout entire repo at a specific commit
git checkout <commit-hash>
dvc checkout

# Return to main branch
git switch main
dvc checkout
```

### What I Did:

I practiced switching between versions:

```bash
# Reverted to previous version
$ git checkout HEAD~1 DVC/data/data.txt.dvc
$ dvc checkout
# Output: M DVC\data\data.txt (Modified)

$ git commit DVC/data/data.txt.dvc -m "Revert dataset updates"

# Switched to specific commit
$ git checkout f93e08027b31f80131b1e0aaad226e69eb8df91a
$ dvc checkout
# Data synced to that version

# Returned to main
$ git switch main
```

### Understanding the Output

When `dvc checkout` shows:
```
M       DVC\data\data.txt
```
The `M` means the file was **M**odified (synced to match the .dvc metadata).

---

## Remote Storage (Optional)

### What is Remote Storage?

Remote storage allows you to:
- **Share data** with team members
- **Backup data** to cloud storage
- **Access data** from different machines

### Supported Storage Types

- Amazon S3
- Azure Blob Storage
- Google Cloud Storage
- Google Drive
- SSH/SFTP
- HDFS
- Local/Network storage

### Setting Up a Local Remote (For Practice)

**Windows:**
```bash
mkdir %TEMP%\dvcstore
dvc remote add -d myremote %TEMP%\dvcstore
```

**Mac/Linux:**
```bash
mkdir /tmp/dvcstore
dvc remote add -d myremote /tmp/dvcstore
```

### Setting Up Cloud Remote (S3 Example)

```bash
dvc remote add -d storage s3://mybucket/dvcstore
```

### Push Data to Remote

```bash
dvc push
```

### Pull Data from Remote

```bash
dvc pull
```

### Workflow with Remote

```
┌─────────────────────────────────────────────────────────────┐
│              Team Collaboration Workflow                     │
├─────────────────────────────────────────────────────────────┤
│  Developer A:                                               │
│    1. dvc add data.csv                                      │
│    2. git add data.csv.dvc && git commit                    │
│    3. dvc push        → Uploads to remote storage           │
│    4. git push        → Pushes .dvc file                    │
│                                                             │
│  Developer B:                                               │
│    1. git pull        → Gets .dvc file                      │
│    2. dvc pull        → Downloads data from remote          │
└─────────────────────────────────────────────────────────────┘
```

---

## Practical Session Summary

### What I Learned and Practiced

| Step | Command | Purpose |
|------|---------|---------|
| 1 | `uv add dvc` | Installed DVC v3.66.1 |
| 2 | `git init` | Initialized Git repository |
| 3 | `dvc init` | Initialized DVC in project root |
| 4 | `git commit -m "feat:dvc init"` | Committed DVC config files |
| 5 | `dvc add DVC/data/data.txt` | Started tracking data file |
| 6 | `git add` + `git commit` | Versioned the .dvc metadata |
| 7 | Modified `data.txt` | Created new data versions |
| 8 | `dvc add` + `git commit` | Tracked new versions |
| 9 | `git checkout HEAD~1 <file>.dvc` | Reverted .dvc to previous version |
| 10 | `dvc checkout` | Synced data to match .dvc |
| 11 | `git checkout <commit-hash>` | Switched to specific commit |
| 12 | `git switch main` | Returned to main branch |

### My Git Commit History

```
commit 359f564 - Updated the data.txt.dvc file
commit f93e080 - Revert dataset updates  
commit 13ea688 - Revert dataset updates
commit 1a5df71 - update:added the content in data.txt
commit c003f85 - feat:added .dvc data file
commit 389fada - feat:dvc init
```

### My Data Evolution

```
Version 1: "This is the first version of my data"
     ↓
Version 2: + "again i switch to the second version of my data"
     ↓
Version 3: + "this is the third version of my data"
```

---

## Common Commands Reference

### Initialization & Configuration

| Command | Description |
|---------|-------------|
| `dvc init` | Initialize DVC in a Git repo |
| `dvc remote add -d <name> <url>` | Add a default remote storage |
| `dvc config core.autostage true` | Auto-stage .dvc files with git |

### Tracking Data

| Command | Description |
|---------|-------------|
| `dvc add <file>` | Start tracking a file/directory |
| `dvc remove <file>.dvc` | Stop tracking a file |
| `dvc status` | Show changed tracked files |

### Version Control

| Command | Description |
|---------|-------------|
| `dvc checkout` | Sync data to match .dvc files |
| `dvc diff` | Show diff between data versions |
| `dvc fetch` | Download data to cache (no checkout) |

### Remote Storage

| Command | Description |
|---------|-------------|
| `dvc push` | Upload tracked data to remote |
| `dvc pull` | Download tracked data from remote |
| `dvc remote list` | List configured remotes |

### Utilities

| Command | Description |
|---------|-------------|
| `dvc --help` | Show help |
| `dvc <command> --help` | Show help for specific command |
| `dvc doctor` | Diagnose DVC installation issues |
| `dvc gc` | Garbage collect unused cache files |

---

## Pro Tips

### 1. Enable Auto-Staging
```bash
dvc config core.autostage true
```
This automatically runs `git add <file>.dvc` after `dvc add`.

### 2. Check What Changed
```bash
dvc diff
```
Shows differences between current data and last committed version.

### 3. View Tracked Files
```bash
dvc data status
```

### 4. Clean Up Cache
```bash
dvc gc --workspace  # Remove unused files from cache
```

---

## Key Takeaways

1. **DVC + Git = Complete Version Control**
   - Git handles code and .dvc metadata
   - DVC handles actual data files

2. **The Magic Workflow**
   ```bash
   dvc add <data>    # Track/update data
   git add <>.dvc    # Stage metadata
   git commit        # Version it
   ```

3. **Time Travel**
   ```bash
   git checkout <commit> <file>.dvc
   dvc checkout
   ```

4. **Data Never Bloats Git**
   - Only small .dvc files go in Git
   - Actual data stays in cache/remote

5. **Team Collaboration**
   - `dvc push` / `dvc pull` for sharing data
   - Works like `git push` / `git pull`

---

## Next Steps

1. **Set up remote storage** for backup and sharing
2. **Explore DVC Pipelines** (`dvc.yaml`) for reproducible ML workflows
3. **Try Experiment Tracking** with `dvc exp`
4. **Integrate with MLflow** for complete MLOps workflow

---

## Resources

- **Official Documentation**: [https://doc.dvc.org](https://doc.dvc.org)
- **Getting Started Guide**: [https://doc.dvc.org/start](https://doc.dvc.org/start)
- **GitHub Repository**: [https://github.com/treeverse/dvc](https://github.com/treeverse/dvc)
- **Discord Community**: [https://dvc.org/chat](https://dvc.org/chat)
- **Video Tutorials**: Available on DVC official YouTube

---

*Documentation created: March 13, 2026*
*DVC Version: 3.66.1*
