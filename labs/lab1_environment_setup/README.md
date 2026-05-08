# Lab 1: Environment Setup and GitHub Workflow

## Overview

In this course, all lab work will be completed using GitHub, git, and PyCharm.

You will:

1. Fork the instructor's repository.
2. Clone your fork to your laptop.
3. Edit and run Python programs locally.
4. Commit your work using git.
5. Push your work to GitHub.
6. Demonstrate your work in person during lab.

This first lab is designed to ensure that your development environment is working correctly before we begin more advanced programming exercises.

---

# Objectives

By the end of this lab, you should be able to:

- Create or access a GitHub account.
- Fork a GitHub repository.
- Clone a repository using PyCharm.
- Configure a Python interpreter.
- Install required Python packages.
- Edit and run a Python file.
- Commit changes using git.
- Push changes to GitHub.
- Demonstrate your work to the instructor.

---

# Part 1: Create a GitHub Account

If you do not already have a GitHub account:

1. Go to:

```text
https://github.com
```

2. Create a free account.

3. Verify your email address if required.

Please choose a professional and identifiable username if possible.

---

# Part 2: Fork the CPSC250L Repository

Go to the instructor repository:

```text
https://github.com/brash99/cpsc250L
```

Click the **Fork** button near the upper-right corner of the page.

Accept the default options.

After forking, you should now have your own copy of the repository located at something like:

```text
https://github.com/YOUR-USERNAME/cpsc250L
```

This copy belongs to you.

---

# Part 3: Clone Your Fork into PyCharm

## Step 1: Open PyCharm

Launch PyCharm.

If prompted, choose:

```text
Get from VCS
```

If you already have a project open, you can instead choose:

```text
Git -> Clone...
```

---

## Step 2: Log Into GitHub

If PyCharm asks you to authenticate with GitHub:

1. Log into your GitHub account.
2. Authorize PyCharm if requested.

---

## Step 3: Clone Your Fork

IMPORTANT:

You should clone YOUR OWN fork, not the instructor repository.

Correct:

```text
https://github.com/YOUR-USERNAME/cpsc250L
```

Incorrect:

```text
https://github.com/brash99/cpsc250L
```

Choose a reasonable local directory location.

Click **Clone**.

PyCharm should now download the repository to your computer.

---

# Part 4: Configure Python

You must have a working Python interpreter configured in PyCharm.

## Check the Interpreter

In PyCharm:

```text
PyCharm -> Settings -> Project -> Python Interpreter
```

or on Windows:

```text
File -> Settings -> Project -> Python Interpreter
```

A Python interpreter should already appear.

If not:

1. Click **Add Interpreter**
2. Choose a local Python installation
3. Select Python 3.9 or newer

---

# Part 5: Install Required Packages

This course uses several external Python libraries.

The required packages are listed in:

```text
requirements.txt
```

You may install them either:

- through the PyCharm package manager

OR

- through the PyCharm terminal

## Terminal Installation Method

Open the PyCharm terminal and run:

```bash
pip install -r requirements.txt
```

This may take a few minutes.

---

# Part 6: Edit and Run the Program

Open the file:

```text
labs/lab01_environment_setup/helloworld.py
```

You should see something similar to:

```python
print("Hello CPSC 250L!")

print("Name: Your Name Here")
print("GitHub username: your-github-username-here")
```

Replace the placeholder information with your own information.

Example:

```python
print("Hello CPSC 250L!")

print("Name: Jane Smith")
print("GitHub username: janesmith")
```

---

# Part 7: Run the Program

Run the program inside PyCharm.

Your output should look similar to:

```text
Hello CPSC 250L!
Name: Jane Smith
GitHub username: janesmith
```

If your program runs successfully, your Python environment is working correctly.

---

# Part 8: Commit Your Changes

Now you will save your changes using git.

## Using the PyCharm Interface

1. Choose:

```text
Git -> Commit...
```

2. Select the modified file.

3. Enter a commit message such as:

```text
Complete Lab 1 environment setup
```

4. Click **Commit** or **Commit and Push**.

---

# Part 9: Push Your Changes to GitHub

If you did not already choose **Commit and Push**, then:

1. Choose:

```text
Git -> Push...
```

2. Push your changes to GitHub.

After pushing, your changes should now appear in your GitHub repository online.

---

# Part 10: Verify Your Push

Go to your GitHub repository in your web browser.

Example:

```text
https://github.com/YOUR-USERNAME/cpsc250L
```

Navigate to:

```text
labs/lab01_environment_setup/helloworld.py
```

Verify that your edited file appears online.

---

# Part 11: Instructor Checkoff

Before leaving lab, demonstrate the following to the instructor:

- Your GitHub account
- Your fork of the repository
- Your cloned repository in PyCharm
- Your configured Python interpreter
- Your installed packages
- Your modified `helloworld.py`
- Your running program
- Your git commit history
- Your pushed changes on GitHub

You may also be asked simple questions such as:

- What is the purpose of a fork?
- What does git commit do?
- What does git push do?
- What is the difference between local and remote repositories?

---

# Congratulations

You now have a fully working development environment for CPSC 250L.

You are ready to begin future labs involving:

- Python programming
- data manipulation
- plotting
- object-oriented programming
- git workflows
- collaborative software development
