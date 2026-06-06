# Lab 1: Professional Development Environment Setup

## Overview

Welcome to CPSC 250L.

In this course, all lab work will be completed using:

- Python
- PyCharm
- GitHub
- git
- the command line / terminal

You will use professional software development tools throughout the semester.

This first lab is designed to ensure that your development environment is fully operational before we begin more advanced programming exercises.

By the end of this lab, you should have:

- Python installed
- PyCharm installed
- a GitHub account
- a fork of the course repository
- a cloned local repository
- a functioning Python interpreter
- required Python packages installed
- a successful git commit and push to GitHub

This lab is extremely important. Problems with setup and configuration can make future labs much more difficult, so take your time and ask questions whenever needed.

---

# Objectives

By the end of this lab, you should be able to:

- Install Python
- Install PyCharm Community Edition
- Create or access a GitHub account
- Fork a GitHub repository
- Clone a repository using PyCharm
- Configure a Python interpreter
- Install required Python packages
- Use the terminal / command line
- Edit and run a Python program
- Commit changes using git
- Push changes to GitHub using PyCharm

---

# Important Concepts

Before beginning, it is important to understand the difference between Python and PyCharm.

| Tool | Purpose |
|---|---|
| Python | The programming language that executes programs |
| PyCharm | The development environment used to write and manage programs |

PyCharm helps you write code, but Python is what actually runs the code.

---

# Part 0: Install Python

## Windows Instructions

1. Go to:

```text
https://www.python.org/downloads/
```

2. Download the latest stable Python 3 release.

3. Run the installer.

IMPORTANT:

Before clicking Install, make sure you CHECK the box:

```text
Add Python to PATH
```

4. Complete the installation.

## Verify Python Installation on Windows

Open:

```text
Command Prompt
```

Run:

```bash
python --version
```

You should see output similar to:

```text
Python 3.12.2
```

---

## macOS Instructions

1. Go to:

```text
https://www.python.org/downloads/
```

2. Download the latest macOS installer.

3. Run the installer.

4. Complete the installation.

## Verify Python Installation on macOS

Open:

```text
Terminal
```

Run:

```bash
python3 --version
```

You should see output similar to:

```text
Python 3.12.2
```

---

# Part 1: Install PyCharm Community Edition

1. Go to:

```text
https://www.jetbrains.com/pycharm/download/
```

2. Download:

```text
PyCharm Community Edition
```

Do NOT download the Professional version.

3. Install PyCharm.

4. Launch PyCharm.

---

# Part 2: Create a GitHub Account

If you do not already have a GitHub account:

1. Go to:

```text
https://github.com
```

2. Create a free account.

3. Verify your email address if required.

Please choose a professional and identifiable username if possible.

---

# Part 3: Fork the CPSC250L Repository

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

# Part 4: Clone Your Fork into PyCharm

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

## Step 2: Log Into GitHub

If PyCharm asks you to authenticate with GitHub:

1. Log into your GitHub account.
2. Authorize PyCharm if requested.

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

# Part 5: Configure Python in PyCharm

You must configure a Python interpreter for your project.

## Windows

In PyCharm:

```text
File -> Settings -> Project -> Python Interpreter
```

## macOS

In PyCharm:

```text
PyCharm -> Settings -> Project -> Python Interpreter
```

A Python interpreter should already appear.

If not:

1. Click **Add Interpreter**
2. Choose a local Python installation
3. Select Python 3.9 or newer

---

# Part 6: Use the Terminal / Command Line

Professional programmers frequently use the terminal.

PyCharm includes a built-in terminal window.

Open the terminal in PyCharm.

## Windows Terminal Commands

Try:

```bash
dir
python --version
pip list
```

## macOS Terminal Commands

Try:

```bash
ls
python3 --version
pip3 list
```

---

# Part 7: Install Required Packages

This course uses several external Python libraries.

The required packages are listed in:

```text
requirements.txt
```

Install them using the PyCharm terminal.

## Windows

```bash
pip install -r requirements.txt
```

## macOS

```bash
pip3 install -r requirements.txt
```

This process may take several minutes.

---

# Part 8: Edit and Run the Program

Open:

```text
labs/lab01_environment_setup/helloworld.py
```

Replace the placeholder information with your own information.

Example:

```python
print("Hello CPSC 250L!")

print("Name: Jane Smith")
print("GitHub username: janesmith")
```

---

# Part 9: Run the Program

Run the program inside PyCharm.

Your output should look similar to:

```text
Hello CPSC 250L!
Name: Jane Smith
GitHub username: janesmith
```

---

# Part 10: Commit Your Changes

Now save your work using git.

Using the PyCharm interface:

```text
Git -> Commit...
```

Select the modified file.

Use a commit message such as:

```text
Complete Lab 1 environment setup
```

Click **Commit**.

---

# Part 11: Push Your Changes to GitHub

Push using PyCharm:

```text
Git -> Push...
```

After pushing, your changes should appear in your GitHub repository online.


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

# Part 12: Verify Your Push

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

# Part 13: Instructor Checkoff

Before leaving lab, demonstrate:

- Python installed successfully
- PyCharm installed successfully
- GitHub account exists
- Fork of the repository exists
- Repository cloned locally
- Python interpreter configured
- Terminal commands executed successfully
- Required packages installed
- Modified `helloworld.py`
- Successful program execution
- git commit history
- Successful push to GitHub

You may also be asked:

- What is Python?
- What is PyCharm?
- What is the purpose of a fork?
- What does git commit do?
- What does git push do?
- What is the difference between local and remote repositories?

---

# Troubleshooting

## Problem: `python` command not found

Try:

```bash
python3 --version
```

## Problem: `pip` command not found

Try:

```bash
python -m pip install numpy
```

or on macOS:

```bash
python3 -m pip install numpy
```

## Problem: PyCharm says no interpreter configured

Go to:

```text
Settings -> Python Interpreter
```

and select your installed Python version.

---

# Congratulations

You now have a fully functioning development environment for CPSC 250L.
