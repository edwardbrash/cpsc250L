# Lab 2: Python Review and Git Fundamentals

## Overview

In Lab 1, you set up your development environment and pushed your first change to GitHub.

In this lab, you will begin using that environment as a programmer. You will practice basic Python programming while also learning a professional Git/GitHub workflow.

This lab emphasizes three important habits:

1. Write and test code incrementally.
2. Commit your work in meaningful stages.
3. Push your completed work to GitHub.

---

# Objectives

By the end of this lab, you should be able to:

- Sync your GitHub fork with the instructor repository.
- Pull updated files into PyCharm.
- Run a Python program in PyCharm.
- Run a Python program from the terminal.
- Read numeric data from a text file.
- Store values in a Python list.
- Write and use simple functions.
- Compute basic statistics.
- Make multiple meaningful Git commits.
- Push your work to GitHub.
- Explain and modify your code during an instructor checkoff.

---

# Part 1: Sync Your Fork

The instructor repository may have changed since Lab 1.

Before starting today's work, you need to update your fork.

## Step 1: Go to Your Fork on GitHub

Open your web browser and go to your fork of the lab repository:

```text
https://github.com/YOUR-USERNAME/cpsc250L
```

## Step 2: Sync Your Fork

Near the top of the repository page, look for the **Sync fork** button.

Click:

```text
Sync fork
```

Then click:

```text
Update branch
```

If GitHub says your branch is already up to date, that is fine.

---

# Part 2: Pull the Updates into PyCharm

After syncing your fork on GitHub, open your local `cpsc250L` project in PyCharm.

Choose:

```text
Git -> Pull...
```

Accept the default options and pull the changes.

You should now see the folder for Lab 2:

```text
labs/lab02_python_review_git/
```

---

# Part 3: Inspect the Lab Files

This lab contains the following files:

```text
labs/lab02_python_review_git/
  README.md
  starter_code/
    statistics_program.py
  data/
    temperatures.txt
  checkoff.md
```

Open the starter program:

```text
starter_code/statistics_program.py
```

Also open the data file:

```text
data/temperatures.txt
```

The data file contains one temperature value per line.

---

# Part 4: Run the Starter Program

Run `statistics_program.py` before making any changes.

The starter program will not be complete. That is expected.

Your job is to replace the `TODO` sections with working code.

---

# Part 5: Complete the Program

The program should:

1. Read all temperatures from `data/temperatures.txt`.
2. Store the temperatures in a list.
3. Compute the number of temperatures.
4. Compute the minimum temperature.
5. Compute the maximum temperature.
6. Compute the average temperature.
7. Print the results in a clear format.

You should complete the program by filling in the provided functions.

Do not solve the entire lab by writing all code inside `main()`.

Use functions.

---

# Part 6: First Required Commit

After you have successfully read the data file and stored the values in a list, make your first commit.

Suggested commit message:

```text
Read temperature data from file
```

You may commit using PyCharm:

```text
Git -> Commit...
```

---

# Part 7: Compute the Statistics

Next, complete the functions that compute:

- minimum value
- maximum value
- average value

You may use loops, built-in functions, or a combination of both, but you must understand your solution.

After this part works, make your second commit.

Suggested commit message:

```text
Compute temperature statistics
```

---

# Part 8: Format the Output

Update the program so that the output is easy to read.

Your output should look similar to this:

```text
Temperature Summary
-------------------
Number of readings: 20
Minimum temperature: 61.2
Maximum temperature: 88.1
Average temperature: 74.53
```

The exact values will depend on the data file.

After this part works, make your third commit.

Suggested commit message:

```text
Format program output
```

---

# Part 9: Run the Program from the Terminal

You must run the program from both PyCharm and the terminal.

Open the PyCharm terminal.

Navigate to the Lab 2 starter code folder if needed.

## Windows

```bash
cd labs\lab02_python_review_git\starter_code
python statistics_program.py
```

## macOS

```bash
cd labs/lab02_python_review_git/starter_code
python3 statistics_program.py
```

If the program cannot find the data file, look carefully at the relative path used in the starter code.

---

# Part 10: Push Your Work to GitHub

After completing the lab and making the required commits, push your work to GitHub.

In PyCharm:

```text
Git -> Push...
```

Then verify your updated files on GitHub in your web browser.

---

# Part 11: Instructor Checkoff

Before leaving lab, demonstrate the following to the instructor:

- Your fork is synced with the instructor repository.
- Your Lab 2 files are present in PyCharm.
- Your program runs successfully in PyCharm.
- Your program runs successfully from the terminal.
- Your code uses functions.
- Your code reads data from the file.
- Your code computes the required statistics.
- Your Git history shows at least three meaningful commits.
- Your work has been pushed to GitHub.

You may also be asked to make a small live change to your program.

Possible live changes include:

- Round the average to two decimal places.
- Print the number of readings.
- Add a line showing the temperature range.
- Change the title of the output.
- Ignore blank lines in the input file.

---

# Submission

Your submission is your pushed GitHub repository.

You do not need to upload a separate file unless instructed otherwise.

---

# Reminder

The goal is not just to make the program work.

The goal is to understand your code well enough to explain, modify, and debug it.
