# Versioning, Branching, and Pull‑Request Workflow  
**Project Maintenance Guide**

This document defines the standard workflow for maintaining the repository, introducing new features, and managing concurrent development tasks.

---

## 1. Tagging a Repository Version

**Purpose:**  
Tags identify stable, meaningful points in the project’s history (e.g., initial baseline, releases, major refactors).

**Usage:**
- Create a lightweight or annotated tag at the current commit:
  ```
  git tag v0.1.0
  git tag -a v0.1.0 -m "Initial maintenance baseline"
  ```
- Push tags to the remote:
  ```
  git push --tags
  ```

**When to Tag:**
- Establishing a new baseline for long‑term maintenance.
- Completing a major refactor or API change.
- Publishing a release or milestone.

---

## 2. Branching Model

**Purpose:**  
Branches isolate work so multiple tasks can proceed independently without interfering with the main development line.

**Standard Branch Types:**

| Branch Type | Purpose |
|-------------|---------|
| `main`      | Stable, reviewed, production‑ready code. |
| `dev` (optional) | Integration branch for ongoing work before merging to `main`. |
| `feature/<name>` | New features, experiments, or refactors. |
| `fix/<name>` | Bug fixes or targeted corrections. |
| `wip/<name>` | Short‑lived exploratory work not yet ready for review. |

**Creating a Branch:**
```
git checkout -b feature/kernel-api-cleanup
```

**Updating a Branch:**
```
git pull origin main
git merge main
```

---

## 3. Working Trees (Optional but Recommended)

**Purpose:**  
Multiple working trees allow simultaneous checkouts of different branches without cloning the repository again.

**Usage:**
- Create a new working tree:
  ```
  git worktree add ../pfc-kernel-api feature/kernel-api-cleanup
  ```
- Remove a working tree:
  ```
  git worktree remove ../pfc-kernel-api
  ```

**When to Use:**
- Working on several features in parallel.
- Running long simulations or tests on one branch while editing another.
- Keeping experimental and stable work physically separated.

---

## 4. Commit Discipline

**Purpose:**  
Commits should be small, isolated, and meaningful.

**Guidelines:**
- One logical change per commit.
- Write descriptive commit messages summarizing the change and its motivation.
- Avoid mixing refactors with functional changes.

---

## 5. Pull Requests (PRs)

**Purpose:**  
Pull requests provide a controlled mechanism for merging changes into `main` or `dev`.

**Workflow:**
1. Push your branch:
   ```
   git push -u origin feature/kernel-api-cleanup
   ```
2. Open a pull request on the hosting platform (GitHub, GitLab, etc.).
3. Provide:
   - Summary of changes  
   - Motivation  
   - Testing performed  
   - Any breaking changes  
4. Address review comments and update the branch as needed.
5. Merge only when:
   - CI/tests pass  
   - Review is complete  
   - Conflicts are resolved  

**PR Merge Options:**
- **Squash merge:** condenses all commits into one (recommended for feature branches).
- **Rebase + merge:** preserves linear history.
- **Merge commit:** preserves branch structure (use sparingly).

---

## 6. Release Workflow

**Purpose:**  
Formalize stable versions for distribution or long‑term support.

**Steps:**
1. Ensure `main` is stable and tested.
2. Tag the release:
   ```
   git tag -a v0.2.0 -m "Kernel API cleanup and model-parameter decoupling"
   ```
3. Push the tag:
   ```
   git push origin v0.2.0
   ```
4. Optionally create a release entry on the hosting platform.

---

## 7. Recommended Practices

- Keep branches short‑lived; merge early and often.
- Rebase feature branches onto `main` to reduce merge conflicts.
- Use working trees to avoid context switching overhead.
- Tag meaningful milestones to simplify future debugging and bisecting.
- Avoid committing generated files or large binary outputs.
