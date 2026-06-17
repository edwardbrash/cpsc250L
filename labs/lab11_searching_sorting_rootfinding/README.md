# Lab 11: Searching, Sorting, and Root Finding

## Overview

This lab continues the CPSC 250L emphasis on hands-on programming, iterative development, GitHub, and live checkoff.

Use the feature-branch workflow:

```text
sync fork -> pull -> create branch -> develop -> commit -> test -> merge -> push
```

Create a branch for this lab:

```bash
git checkout -b lab11-algorithms
```

After completing and testing the lab, merge back into `main`:

```bash
git checkout main
git merge lab11-algorithms
```

Then push using PyCharm:

```text
Git -> Push...
```

Do not use terminal `git push` unless you have terminal GitHub authentication configured.


# Learning Objectives

By the end of this lab, you should be able to:

- Implement linear search
- Implement binary search
- Explain why binary search requires sorted data
- Use loops for algorithmic problem solving
- Implement a simple bisection root-finding method

# Assignment

This lab connects two ideas:

1. Searching sorted data
2. Searching for a root of a mathematical function

Both are examples of algorithmic thinking.

# Program Requirements

Your program should:

1. Implement linear search.
2. Implement binary search.
3. Test both searches on sample data.
4. Implement bisection root finding.
5. Use bisection to find a root of a simple function.

# Required Commits

```text
Commit 1: Add linear search
Commit 2: Add binary search
Commit 3: Add bisection method
Commit 4: Add tests and cleanup
```

# Instructor Checkoff

Possible live requests:

- Search for a new value.
- Explain why binary search requires sorted data.
- Change the function used for root finding.
- Change the tolerance.
- Explain how bisection narrows the interval.
