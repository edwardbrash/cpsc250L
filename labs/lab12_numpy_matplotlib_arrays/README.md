# Lab 12: NumPy Arrays and Matplotlib Plotting

## Overview

This lab continues the CPSC 250L emphasis on hands-on programming, iterative development, GitHub, and live checkoff.

Use the feature-branch workflow:

```text
sync fork -> pull -> create branch -> develop -> commit -> test -> merge -> push
```

Create a branch for this lab:

```bash
git checkout -b lab12-numpy-plotting
```

After completing and testing the lab, merge back into `main`:

```bash
git checkout main
git merge lab12-numpy-plotting
```

Then push using PyCharm:

```text
Git -> Push...
```

Do not use terminal `git push` unless you have terminal GitHub authentication configured.


# Learning Objectives

By the end of this lab, you should be able to:

- Create NumPy arrays
- Perform array calculations
- Generate data for a function
- Make a matplotlib plot
- Save a plot as an image file

# Assignment

You will model the motion of an object under constant acceleration.

You will use NumPy arrays to compute position and velocity values and matplotlib to plot the results.

# Program Requirements

Your program should:

1. Create a time array.
2. Compute position and velocity arrays.
3. Print selected values.
4. Plot position versus time.
5. Plot velocity versus time.
6. Save the plots as PNG files.

# Required Commits

```text
Commit 1: Add NumPy array calculations
Commit 2: Add position plot
Commit 3: Add velocity plot
Commit 4: Save plots and cleanup
```

# Instructor Checkoff

Possible live requests:

- Change the acceleration.
- Change the time interval.
- Add a title or axis label.
- Save a new plot.
- Explain why array operations are useful.
