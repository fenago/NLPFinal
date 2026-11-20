# Git Workflow: Branches, Fast-Forward Merge, Pull Requests

Sources:
- https://git-scm.com/docs/git-branch
- https://git-scm.com/docs/git-merge
- https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests (redirects to https://docs.github.com/en/pull-requests/reference/pull-requests)
- https://code.claude.com/docs/en/common-workflows (PR creation section)

Fetched: 2026-11-20

## git branch (git-scm.com/docs/git-branch)
- Purpose: "List, create, or delete branches."
- Create: `git branch <branch-name> [<start-point>]`. Switch with `git switch <branch>`; `checkout -b` combines both (the page's example note).
- List: `git branch` (current branch starred), `-r` remote-tracking, `-a` both. `--merged [<commit>]` / `--no-merged` filter.
- Delete: `-d` deletes only if "fully merged in its upstream branch, or in HEAD if no upstream was set"; `-D` is shortcut for `--delete --force`.
- Rename: `-m` / `-M`. Set upstream: `-u <upstream>` / `--set-upstream-to`.

## git merge (git-scm.com/docs/git-merge)
- "Incorporates changes from the named commits (since the time their histories diverged from the current branch) into the current branch."
- Fast-forward: when HEAD is an ancestor of the merged commit, Git just moves the branch pointer; **no merge commit**.
- Options:
  - `--ff` (default): fast-forward when possible, else create a merge commit.
  - `--no-ff`: always create a merge commit.
  - `--ff-only`: "resolve the merge as a fast-forward when possible. When not possible, refuse to merge and exit with a non-zero status."
- Example from the docs: `git merge --ff-only v1.2.3` when you have no work of your own.
- Pre-merge checks: commit or stash local work first; merge aborts if the index differs from HEAD, and stops if uncommitted changes overlap files it must update.
- "Already up to date." when all named commits are already ancestors of HEAD.
- Conflicts: HEAD stays put, conflicting files are marked; `git merge --abort` returns to the pre-merge state; `--continue` after resolving.
- Config: `merge.ff` can be `false` (like `--no-ff`) or `only` (like `--ff-only`).

## Pull requests (GitHub Docs)
- A pull request is "a proposal to merge code changes into a project": the place to discuss and review before merge.
- Tabs: Conversation (description, timeline, reviews), Commits, Checks (automated tests/builds), Files changed (diff), Findings (code scanning). A **merge status** box shows blockers and missing approvals.
- **Draft PRs** cannot be merged and do not auto-request code owners; mark ready for review to request reviews.
- Models: **shared repository** (collaborators push topic branches to one repo; common for small teams) and **fork and pull** (open source).
- GitHub makes temporary refs for the PR head and a simulated merge result; relevant to CI (see GitHub Actions merge branch).

## Claude Code and PRs
- Ask `create a pr`; Claude links the session to the PR when it runs `gh pr create`. `claude --from-pr <n>` reopens the session.
- Review Claude's generated PR before submitting.

## Project application (suggested workflow, derived from the above)
1. `main` is protected (S06); every agent works on a topic branch: `git switch -c <agent>/<task>`.
2. Small commits with clear messages; one owner per file (roster table).
3. Before opening a PR, update from `main` and make sure the branch can fast-forward: `git fetch` then `git merge --ff-only origin/main` fails loudly if histories diverged (rebase or merge `main` into the branch first).
4. Open a PR (draft while in progress); ORC reviews against the data contract; QA checks pass in the Checks tab; Netlify deploy preview is the visual check.
5. After merge, delete the topic branch: `git branch -d <branch>` (safe, refuses if unmerged).
6. Never force-push `main`; do not use `-D` unless ORC confirms the branch is disposable.
