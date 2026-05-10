# Lab 7: Operator Overloading and Object Comparisons

## Overview


In this lab, you will learn how objects can define their own behavior for common operations such as printing, comparing, and sorting.

You will create a `TimeDuration` class that represents a length of time in hours, minutes, and seconds.


---

# Learning Objectives

By the end of this lab, you should be able to:

- Create and use Python classes
- Create objects
- Store objects in lists
- Write and call object methods
- Use clean object-oriented design
- Continue using a feature-branch workflow
- Merge tested work back into `main`
- Push merged work using PyCharm

---

# Part 1: Sync, Pull, and Create a Branch

Sync your fork on GitHub, then pull in PyCharm.

Create a new branch:

```bash
git checkout -b lab07-comparisons
```

You may also create the branch using PyCharm's Git branch menu.

Stay on this branch while completing the lab.

---

# Part 2: Complete the Starter Code

Open the files in:

```text
starter_code/
```

Read the comments carefully and complete the required functions and methods.

---

# Part 3: Run and Test Your Program

Run the main program for this lab in PyCharm.

Fix any errors before merging your branch back into `main`.

---

# Part 4: Required Incremental Commits

Make several meaningful commits while working.

Do not wait until the end to make one giant commit.

Use commit messages that describe what you changed.

Examples:

```text
Add constructor
Add object methods
Add report output
Final cleanup and testing
```

---

# Part 5: Merge Back Into Main

After your code is working, merge your feature branch back into `main`.

You may use the PyCharm terminal for the local merge steps:

```bash
git checkout main
git merge lab07-comparisons
```

These commands do not communicate with GitHub. They only modify your local repository.

After the merge succeeds, push using PyCharm:

```text
Git -> Push...
```


## Important Note About Pushing to GitHub

You may use the PyCharm terminal for local Git commands such as:

```bash
git status
git checkout main
git merge <branch-name>
```

These commands only affect your local repository.

However, when pushing to GitHub, you should normally use PyCharm's built-in Git interface:

```text
Git -> Push...
```

PyCharm may already be authenticated with GitHub even when terminal Git is not.

If `git push` in the terminal asks for a GitHub username and password, do not worry. That means terminal Git authentication has not been configured separately. For this course, use PyCharm's **Git -> Push...** interface unless your instructor tells you otherwise.


---

# Instructor Checkoff

Be prepared to:

- run your program
- explain your class design
- explain your feature branch workflow
- show your commit history
- make a small live modification

Your instructor may ask you to add a method, modify output, create a new object, or explain how your objects interact.
