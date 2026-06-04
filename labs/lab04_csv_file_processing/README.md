# Lab 4: File I/O and CSV Data Processing

## Overview

In this lab, you will work with structured data stored in a CSV file.

CSV stands for "comma-separated values." CSV files are commonly used to store tables of data in a plain-text format. Many real-world datasets are stored as CSV files.

Your task is to read a CSV file containing student quiz scores, clean the data, compute averages, and print a useful report.

This lab builds directly on Lab 3. You should organize your program using functions.

---

# Learning Objectives

By the end of this lab, you should be able to:

- Open and read a text file
- Process a CSV file line by line
- Skip a header row
- Split strings into fields
- Convert strings to numbers
- Handle missing or invalid data
- Store structured data in lists and dictionaries
- Compute averages from cleaned data
- Write modular code using functions
- Use Git and GitHub in an iterative workflow

---

# Part 1: Sync Your Fork

Before beginning:

1. Go to your fork of the repository on GitHub.
2. Click **Sync fork**.
3. In PyCharm, pull the newest changes using **Git -> Pull**.

Verify that the following folder now exists:

```text
labs/lab04_csv_file_processing
```

---

# Part 2: Examine the Data File

Open:

```text
data/quiz_scores.csv
```

The file contains student names and quiz scores.

Some entries are intentionally messy. You may see:

- missing scores
- non-numeric scores
- extra whitespace
- scores marked as `absent`

Real data is often messy. Your program should handle these cases gracefully.

---

# Part 3: Complete the Starter Program

Open:

```text
starter_code/student_scores.py
```

Complete the required functions:

```python
def clean_score(score_text):
    ...

def calculate_average(scores):
    ...

def read_scores(filename):
    ...

def letter_grade(average):
    ...

def print_student_report(records):
    ...

def print_class_summary(records):
    ...
```

---

# Part 4: Program Requirements

Your completed program should:

1. Read the CSV file.
2. Skip the header row.
3. Store each student's name and valid quiz scores.
4. Ignore missing or invalid quiz scores.
5. Compute each student's quiz average.
6. Assign a simple letter grade.
7. Print a student-by-student report.
8. Print a class summary.

---

# Part 5: Required Incremental Commits

Make at least FOUR commits.

Suggested commit structure:

```text
Commit 1: Add CSV reading function
Commit 2: Add score cleaning and averaging
Commit 3: Add student report output
Commit 4: Add class summary and cleanup
```

---

# Part 6: Push Your Changes

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
- explain how your CSV reading works
- explain how your code handles bad data
- show your Git commit history
- make a small live modification

Possible live requests include:

- Add a fourth quiz column to the CSV file and make sure the program still works.
- Change the letter-grade scale.
- Print the name of the student with the highest average.
- Count how many students have an average above 80.
- Explain what happens if a score is missing.
