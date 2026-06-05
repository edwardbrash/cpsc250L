# Lab 5: Classes, Objects, and Feature Branches

## Overview

This lab begins the main object-oriented programming portion of the course.

In previous labs, you wrote programs using functions, lists, files, and dictionaries. In this lab, you will begin organizing data and behavior together using a Python class.

You will also learn a new Git workflow: creating a feature branch, doing your work on that branch, testing your code, and then merging the completed work back into `main`.

---

# Learning Objectives

By the end of this lab, you should be able to:

- Define a Python class
- Write an `__init__` constructor
- Store data in instance variables
- Write methods that operate on object data
- Use `self`
- Create multiple objects from the same class
- Write a `__str__` method
- Create and work on a Git feature branch
- Merge a feature branch back into `main`
- Push merged work to GitHub using PyCharm

---

# Part 1: Sync Your Fork and Pull

Before beginning:

1. Go to your fork of the repository on GitHub.
2. Click **Sync fork**.
3. In PyCharm, pull the newest changes using **Git -> Pull**.

Verify that the following folder now exists:

```text
labs/lab05_classes_feature_branches
```

---

# Part 2: Create a Feature Branch

For this lab, do not work directly on `main`.

Create a new branch called:

```text
lab05-classes
```

You may do this in PyCharm using the Git branch menu, or from the terminal:

```bash
git checkout -b lab05-classes
```

The idea is:

```text
main = stable working code
feature branch = where new development happens
```

Stay on this branch while completing the lab.

---

# Part 3: Examine the Starter Files

Open:

```text
starter_code/student_record.py
```

and:

```text
starter_code/main.py
```

The file `student_record.py` contains the class you will complete.

The file `main.py` creates objects and tests your class.

---

# Part 4: Complete the StudentRecord Class

Each `StudentRecord` object should store:

- student name
- student ID
- list of quiz scores

The class should include methods to:

- add a quiz score
- calculate the average
- find the highest score
- find the lowest score
- return a letter grade
- produce a readable string using `__str__`

---

# Part 5: Required Incremental Commits

Make at least FOUR commits on your feature branch.

Suggested commit structure:

```text
Commit 1: Add StudentRecord constructor
Commit 2: Add score-management methods
Commit 3: Add average and grade methods
Commit 4: Add __str__ and final testing
```

---

# Part 6: Test Your Code

Run:

```text
starter_code/main.py
```

Make sure your program works before merging back into `main`.

---

# Part 7: Merge Back Into Main

After your code is working, merge your feature branch back into `main`.

You may use the PyCharm terminal for the local merge steps:

```bash
git checkout main
git merge lab05-classes
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

- show your feature branch
- show your commit history
- run your program
- explain what `self` means
- explain the purpose of `__init__`
- explain why objects combine data and behavior
- make a small live modification

Possible live requests include:

- Add a new quiz score to one student.
- Add a method that counts the number of scores.
- Modify the letter-grade scale.
- Change the `__str__` output.
- Add a new student object.
