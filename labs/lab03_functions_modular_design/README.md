# Lab 3: Functions and Modular Program Design

## Overview

In this lab, you will practice breaking a larger Python program into smaller, well-organized functions.

Professional programmers rarely write large programs entirely in one block of code. Instead, programs are divided into reusable functions that each perform a specific task.

You will refactor a messy temperature analysis program into a cleaner and more modular design using functions.

This lab builds directly on the programming concepts from Labs 1 and 2.

---

# Learning Objectives

By the end of this lab, you should be able to:

- Define and use Python functions
- Pass parameters to functions
- Return values from functions
- Organize a program into reusable components
- Read data from a file
- Compute simple statistics
- Improve readability through modular design
- Use Git and GitHub in an iterative workflow
- Create meaningful incremental commits

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
labs/lab03_functions_modular_design
```

---

# Part 2: Examine the Messy Program

Open:

```text
starter_code/messy_temperature_report.py
```

This program works correctly, but it is poorly organized.

Notice:

- repeated code
- no reusable functions
- poor readability
- everything placed in one large block of code
- difficult to modify or extend

Your task is to reorganize this program into a cleaner and more modular design.

---

# Part 3: Complete the Modular Program

Open:

```text
starter_code/temperature_report.py
```

Complete the required functions:

```python
def read_temperatures(filename):
    ...

def calculate_average(values):
    ...

def find_maximum(values):
    ...

def find_minimum(values):
    ...

def count_above_threshold(values, threshold):
    ...

def print_report(values):
    ...
```

---

# Part 4: Program Requirements

Your completed program should:

1. Read temperatures from the data file.
2. Store temperatures in a list.
3. Compute:
   - average temperature
   - minimum temperature
   - maximum temperature
   - number of temperatures above 80
4. Print a clean report.

Example output:

```text
Temperature Report
------------------
Average temperature: 80.6
Maximum temperature: 95
Minimum temperature: 61
Temperatures above 80: 10
```

---

# Part 5: Run the Program

Run your completed program in PyCharm.

You should also test your program from the terminal.

## Windows

```bash
python temperature_report.py
```

## macOS

```bash
python3 temperature_report.py
```

---

# Part 6: Required Incremental Commits

You must make at least FOUR commits.

Suggested commit structure:

```text
Commit 1: Add file-reading function
Commit 2: Add statistics functions
Commit 3: Add report output function
Commit 4: Final cleanup and testing
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

- run your completed program
- explain how your functions work
- describe parameters and return values
- explain why modular code is useful
- show your Git commit history
- make a small live modification

Possible live requests include:

- Count temperatures below 70.
- Print the number of temperatures.
- Round the average to two decimal places.
- Add a temperature range calculation.
- Explain the difference between printing and returning.
