---
layout: default
title: 'Set Up Work In Progress for GIT'
base-url: home/procedures/git-procedures/set-up-wip-for-git.md
breadcrumbs:
- title: 'Home'
  url: home.html
- title: 'Procedures'
  url: home/procedures.html
- title: 'GIT Procedures'
  url: home/procedures/git-procedures.html
---

# Set Up Work In Progress for GIT

## Overview

Since I am in the middle of a [project](https://github.com/users/dfhawthorne/projects/5/views/1) to convert my [Wiki](https://dfhawthorne.github.io/home) to the [Jekyll](https://jekyllrb.com/) format, I need to set up a way to apply changes to my Wiki without interfering with the project work. A case in point was the addition of several PostgreSQL procedures. I had set up a specific branch for that work, and deleted that branch after a successful merge into the main branch. Since then, I realised that this functionality should be retained. I will create a new branch called `work-in-progress`. This blog post shows the steps I took to achieve this.

## Table of Contents

* [Summary](home/procedures/git-procedures/set-up-wip-for-git.html#summary)
* [Created WIP Branch](home/procedures/git-procedures/set-up-wip-for-git.html#created-wip-branch)
  * [Ensured Main Branch was Up-to-Date](home/procedures/git-procedures/set-up-wip-for-git.html#ensured-main-branch-was-up-to-date)
  * [Confirmed WIP Branch Does Not Exists](home/procedures/git-procedures/set-up-wip-for-git.html#confirmed-wip-branch-does-not-exists)
  * [Created New Branch](home/procedures/git-procedures/set-up-wip-for-git.html#created-new-branch)
  * [Created Dummy Commit](home/procedures/git-procedures/set-up-wip-for-git.html#created-dummy-commit)
  * [Created Upstream Branch](home/procedures/git-procedures/set-up-wip-for-git.html#created-upstream-branch)
* [Created Extra Changes in WIP Branch](home/procedures/git-procedures/set-up-wip-for-git.html#created-extra-changes-in-wip-branch)
  * [Squashed New Commits](home/procedures/git-procedures/set-up-wip-for-git.html#squashed-new-commits)
  * [Pushed Latest Changes from WIP to GitHub](home/procedures/git-procedures/set-up-wip-for-git.html#pushed-latest-changes-from-wip-to-github)
* [Merged WIP into Main Using a Pull Request (PR)](home/procedures/git-procedures/set-up-wip-for-git.html#merged-wip-into-main-using-a-pull-request-pr)
  * [Checked GitHub CLI Status](home/procedures/git-procedures/set-up-wip-for-git.html#checked-github-cli-status)
  * [Created Pull Request](home/procedures/git-procedures/set-up-wip-for-git.html#created-pull-request)
  * [Checked PR Status](home/procedures/git-procedures/set-up-wip-for-git.html#checked-pr-status)
  * [Merged PR onto Main Branch](home/procedures/git-procedures/set-up-wip-for-git.html#merged-pr-onto-main-branch)
  * [Updated the Main Branch Locally](home/procedures/git-procedures/set-up-wip-for-git.html#updated-the-main-branch-locally)
* [Cherry Pick a Commit from Main into Project Branch](home/procedures/git-procedures/set-up-wip-for-git.html#cherry-pick-a-commit-from-main-into-project-branch)
* [Conclusion](home/procedures/git-procedures/set-up-wip-for-git.html#conclusion)

## Summary

The general steps were:

1. Created `work-in-progress` branch from the `main` branch.
1. Do Required Work in WIP
1. Used Pull Request (PR) to Merge WIP into Main
1. Cherry Pick a Commit from Main into Project Branch

Step 1 is done only once, with the other three (3) being done as needed.

__Note:__ This procedure is not definitive, but is the best I can do with my level of GIT knowledge. The procedure may be more cautious than is needed.

## Created WIP Branch

The general steps were:

1. Ensured `main` branch was up-to-date.
1. Determined if `work-in-progress` branch existed.
1. Created new branch
1. Created dummy commit
1. Created upstream branch

__Note:__ The dummy commit is needed to establish the upstream branch (`work-in-progress` on GitHub) during the push from the local branch.

__Note:__ These steps are done once only.

### Ensured Main Branch was Up-to-Date

__Note:__ It is important that there is no outstanding work on either the local or remote versions of the `main` branch. Although it is possible to proceed past this point without ensuring that the local and remote versions of the `main` are synchronised, it reduces difficulties further on by ensuring that this is so.

I used the following command to ensure that I am on the `main` branch and that the local version of the branch is not ahead of the remote version:

```bash
git status
```

The expected output was:

```text
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

If I was on another branch, I would have used the `git checkout main` command to switch to the `main` branch.

I used the following command to ensure that the remote version of the `main` branch was not ahead of the local version:

```bash
git pull
```

The expected output was:

```text
Already up to date.
```

### Confirmed WIP Branch Does Not Exists

__Note:__ Although it is possible to bypass this step by using GIT features, I think it is important to be aware of whether a branch existed before proceeding.

The following command was used to list all current branches:

```bash
git branch
```

The output was:

```text
  V2R4
  jekyll_collapse
  jekyll_redirect
* main
```

__Note__ that the `work-in-progress` branch is __not__ listed, and the `main` branch is still the default branch as indicated by the asterisk ('`*`').

### Created New Branch

I created a new branch, `work-in-progress`, as follows:

```bash
git checkout -b work-in-progress
git status
```

The output was:

```text
Switched to a new branch 'work-in-progress'
On branch work-in-progress
nothing to commit, working tree clean
```

### Created Dummy Commit

I created a small commit in order to establish the upstream branch:

```bash
touch home/procedures/postgresql/move-tablespace.html
mkdir home/procedures/postgresql/move-tablespace
git status
```

The output was:

```text
On branch work-in-progress
Untracked files:
  (use "git add <file>..." to include in what will be committed)
  home/procedures/postgresql/move-tablespace.html

nothing added to commit but untracked files present (use "git add" to track)
```

I added this file to GIT and committed the change as follows:

```bash
git add home/procedures/postgresql/move-tablespace.html
git -m "Started writing Move Tablespace procedure for PostgreSQL"
```

```text
[work-in-progress 4ce1115] Started writing Move Tablespace procedure for PostgreSQL
 1 file changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 docs/home/procedures/postgresql/move-tablespace.html
```

### Created Upstream Branch

I created an upstream branch (`work-in-progress`) on GitHub (`origin`) by pushing the dummy commit as follows:

```bash
git push --set-upstream origin work-in-progress
git status
```

The output was:

```text
Enumerating objects: 12, done.
Counting objects: 100% (12/12), done.
Delta compression using up to 6 threads
Compressing objects: 100% (6/6), done.
Writing objects: 100% (7/7), 586 bytes | 586.00 KiB/s, done.
Total 7 (delta 5), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (5/5), completed with 5 local objects.
remote: 
remote: Create a pull request for 'work-in-progress' on GitHub by visiting:
remote:      https://github.com/dfhawthorne/dfhawthorne.github.io/pull/new/work-in-progress
remote: 
To github.com:dfhawthorne/dfhawthorne.github.io.git
 * [new branch]      work-in-progress -> work-in-progress
Branch 'work-in-progress' set up to track remote branch 'work-in-progress' from 'origin'.
On branch work-in-progress
Your branch is up to date with 'origin/work-in-progress'.

nothing to commit, working tree clean
```

## Created Extra Changes in WIP Branch

The general steps were:

1. Squashed multiple commits into a single commit.
1. Pushed latest changes from WIP to GitHub.

### Squashed New Commits

I made extra changes and rebased those commits by using the following command:

```bash
git rebase -i
```

The default editor popped with the commits to be squashed into a single commit, and the commit message was adjusted. After saving and closing the editor, the following output was:

```text
[detached HEAD b72001e] Added PostgreSQL procedures: - Upgrade PostgreSQL 14 to 16 - Moving tablespaces (default and non-default) Other conversions to Jekyll format - Knowledge anchor page - Procedures anchor page   - Added PostgreSQL Procedures anchor page - Issues anchor page   - Added PostgreSQL Issues anchor page Added issue for Move Default Tablespace is Different from Normal Tablespace Updated build_toc.py script not to prettify HTML
 Date: Wed Apr 3 11:56:58 2024 +1100
 11 files changed, 404 insertions(+), 973 deletions(-)
 create mode 100644 docs/home/issues/postgresql-issues.html
 create mode 100644 docs/home/issues/postgresql-issues/move-default-tablespace-is-different-from-normal-tablespace.html
 rewrite docs/home/knowledge.html (99%)
 create mode 100644 docs/home/procedures/postgresql/move-default-tablespace.html
 create mode 100644 docs/home/procedures/postgresql/move-non-default-tablespace.html
 delete mode 100644 docs/home/procedures/postgresql/move-tablespace.html
Successfully rebased and updated refs/heads/work-in-progress.
```

### Pushed Latest Changes from WIP to GitHub

I used the following command to push the consolidated changes from the `work-in-progress` branch to the remote repository on GitHub:

```bash
git push
```

The output was:

```text
Enumerating objects: 32, done.
Counting objects: 100% (32/32), done.
Delta compression using up to 6 threads
Compressing objects: 100% (19/19), done.
Writing objects: 100% (19/19), 7.41 KiB | 3.71 MiB/s, done.
Total 19 (delta 13), reused 0 (delta 0), pack-reused 0
remote: Resolving deltas: 100% (13/13), completed with 11 local objects.
To github.com:dfhawthorne/dfhawthorne.github.io.git
   4ce1115..b72001e  work-in-progress -> work-in-progress
```

## Merged WIP into Main Using a Pull Request (PR)

The commits on the `work-in-progress` branch were merged into the `main` both on remote and on local using the steps:

1. Checked GitHub CLI Status
1. Created pull request (PR)
1. Checked PR status
1. Merged PR onto `main` remote branch
1. Updated the `main` loacl branch

### Checked GitHub CLI Status

I have installed `gh` (GitHub CLI) and authenticated my connection to my GitHub account.

I used the following command to validate my connection to the GitHub account:

```bash
gh auth status
```

The status is active as shown by:

```text
github.com
  ✓ Logged in to github.com account dfhawthorne (keyring)
  - Active account: true
  - Git operations protocol: ssh
  - Token: gho_************************************
  - Token scopes: 'admin:public_key', 'gist', 'project', 'read:org', 'repo'
```

### Created Pull Request

I ran the following command, using the GitHub CLI (`gh`), to create a pull request (PR) from the current branch (`work-in-progress`) to the `main` branch:

```bash
gh pr create \
    --assignee @me \
    --base main \
    --fill-verbose \
    --label documentation \
    --title "Added PostgreSQL procedures for upgrading server 14 to 16, and moving tablespaces" 
```

The creation of the PR was successful as shown below:

```text
Creating pull request for work-in-progress into main in dfhawthorne/dfhawthorne.github.io

https://github.com/dfhawthorne/dfhawthorne.github.io/pull/70
```

### Checked PR Status

I run the following command to check the status of PR on the current branch (`work-in-progress`):

```bash
gh pr status
```

The output was:

```text
Relevant pull requests in dfhawthorne/dfhawthorne.github.io

Current branch
  #70  Added PostgreSQL procedures for upgrading serve... [work-in-progress]

Created by you
  #70  Added PostgreSQL procedures for upgrading serve... [work-in-progress]

Requesting a code review from you
  You have no pull requests to review
```

### Merged PR onto Main Branch

I used the following command to merge the PR in the current branch (`work-in-progress`) into the `main` branch:

```bash
gh pr merge --merge
```

The merge of the PR was successful as shown by the following messages:

```text
✓ Merged pull request dfhawthorne/dfhawthorne.github.io#70 (Added PostgreSQL procedures for upgrading server 14 to 16, and moving tablespaces)
```

### Updated the Main Branch Locally

I updated the `main` branch locally as follows:

```bash
git checkout main
git pull
git status
```

```text
Switched to branch 'main'
Your branch is up to date with 'origin/main'.
remote: Enumerating objects: 1, done.
remote: Counting objects: 100% (1/1), done.
remote: Total 1 (delta 0), reused 0 (delta 0), pack-reused 0
Unpacking objects: 100% (1/1), 954 bytes | 954.00 KiB/s, done.
From github.com:dfhawthorne/dfhawthorne.github.io
   0ce8f2b..bda6093  main       -> origin/main
Updating 0ce8f2b..bda6093
Fast-forward
 docs/home/issues.html                                                                               |    2 +
 docs/home/issues/postgresql-issues.html                                                             |   14 ++
 docs/home/issues/postgresql-issues/move-default-tablespace-is-different-from-normal-tablespace.html |  180 ++++++++++++++
 docs/home/knowledge.html                                                                            | 1004 +++-----------------------------------------------------------------------
 docs/home/procedures.html                                                                           |    4 +
 docs/home/procedures/postgresql.html                                                                |    4 +
 docs/home/procedures/postgresql/move-default-tablespace.html                                        |  123 +++++++++
 docs/home/procedures/postgresql/move-non-default-tablespace.html                                    |   29 +++
 docs/home/procedures/postgresql/upgrade-postgresql-14-to-16.html                                    |   13 +-
 scripts/build_toc.py                                                                                |    4 +-
 10 files changed, 404 insertions(+), 973 deletions(-)
 create mode 100644 docs/home/issues/postgresql-issues.html
 create mode 100644 docs/home/issues/postgresql-issues/move-default-tablespace-is-different-from-normal-tablespace.html
 create mode 100644 docs/home/procedures/postgresql/move-default-tablespace.html
 create mode 100644 docs/home/procedures/postgresql/move-non-default-tablespace.html
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

## Cherry Pick a Commit from Main into Project Branch

I used the following commands to apply the latest PR from the `main` branch onto my current project branch, `V2R4`:

```bash
git checkout V2R4
git cherry-pick main -m 1
git status
```

The changes were successfully applied as shown below:

```text
Switched to branch 'V2R4'
Your branch is up to date with 'origin/V2R4'.
[V2R4 4a705c8] Merge pull request #70 from dfhawthorne/work-in-progress
 Date: Wed Apr 3 22:15:36 2024 +1100
 10 files changed, 404 insertions(+), 973 deletions(-)
 create mode 100644 docs/home/issues/postgresql-issues.html
 create mode 100644 docs/home/issues/postgresql-issues/move-default-tablespace-is-different-from-normal-tablespace.html
 rewrite docs/home/knowledge.html (99%)
 create mode 100644 docs/home/procedures/postgresql/move-default-tablespace.html
 create mode 100644 docs/home/procedures/postgresql/move-non-default-tablespace.html
On branch V2R4
Your branch is ahead of 'origin/V2R4' by 1 commit.
  (use "git push" to publish your local commits)

nothing to commit, working tree clean
```

The important option here is `-m 1`. The explanation from the `git-cherry-pick` manual page is:

> `-m parent-number`, `--mainline parent-number` \
>   Usually you cannot cherry-pick a merge because you do not know which side of the merge should be considered the mainline. This option specifies the parent number (starting from 1) of the mainline and allows cherry-pick to replay the change relative to the specified parent.

__Note:__ This option has to be specified because the head of the `main` branch is the result of a merge request.

## Conclusion

This procedure is somewhat convoluted but it is reproducible. With the success of this procedure, I will consider creating a `project` branch starting with V2R5. This will allow me to maintain a three (3) branch structure going forward:

1. `main` for deployment onto GitHub Pages
1. `work-in-progress` for out of project work
1. `project` for the main project work
