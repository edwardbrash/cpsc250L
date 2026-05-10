# Lab 2: Python Review and Git Fundamentals

## Overview

In this lab, you will begin using your development environment for real programming work.

This lab reviews core CPSC 150/150L skills that you will need throughout CPSC 250 and CPSC 250L:

- variables
- lists
- loops
- functions
- file input
- simple statistics

You will also continue practicing the basic Git workflow:

```text
sync fork -> pull -> edit -> run -> commit -> push
```

---

# Learning Objectives

By the end of this lab, you should be able to:

- Sync your GitHub fork
- Pull new files into PyCharm
- Read numeric data from a file
- Store values in a list
- Use loops to process data
- Write simple functions
- Compute basic statistics
- Commit changes incrementally
- Push completed work to GitHub using PyCharm

---

# Part 1: Sync Your Fork

Before beginning:

1. Go to your fork of the repository on GitHub.
2. Click **Sync fork**.
3. In PyCharm, pull the newest changes:

```text
Git -> Pull
```

Verify that the following folder now exists:

```text
labs/lab02_python_review_git
```

---

# Part 2: Examine the Data File

Open:

```text
data/temperatures.txt
```

This file contains one temperature value per line.

---

# Part 3: Complete the Starter Program

Open:

```text
starter_code/statistics_program.py
```

Complete the program so that it:

1. Reads all temperatures from the file.
2. Stores them in a list.
3. Computes:
   - average
   - minimum
   - maximum
   - number of values
4. Prints a clean report.

---

# Part 4: Use Functions

Your program should use functions such as:

```python
def read_values(filename):
    ...

def calculate_average(values):
    ...

def print_report(values):
    ...
```

You may create additional helper functions.

---

# Part 5: Run the Program

Run the program in PyCharm.

Also test from the PyCharm terminal.

## Windows

```bash
python statistics_program.py
```

## macOS

```bash
python3 statistics_program.py
```

---

# Part 6: Required Incremental Commits

Make at least THREE commits.

Suggested commit structure:

```text
Commit 1: Add file reading
Commit 2: Add statistics calculations
Commit 3: Add final report output
```

---

# Part 7: Push Your Changes

Push using PyCharm:

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
- explain your functions
- show your commit history
- explain the difference between commit and push
- make a small live modification

Possible live requests include:

- Round the average to two decimal places.
- Print the number of temperatures.
- Count values above a threshold.
- Add a new value to the data file and rerun the program.
