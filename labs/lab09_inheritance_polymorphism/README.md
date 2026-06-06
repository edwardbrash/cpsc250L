# Lab 9: Inheritance and Polymorphism

## Overview

This lab continues the CPSC 250L emphasis on hands-on programming, iterative development, GitHub, and live checkoff.

Use the feature-branch workflow:

```text
sync fork -> pull -> create branch -> develop -> commit -> test -> merge -> push
```

Create a branch for this lab:

```bash
git checkout -b lab09-inheritance
```

After completing and testing the lab, merge back into `main`:

```bash
git checkout main
git merge lab09-inheritance
```

Then push using PyCharm:

```text
Git -> Push...
```

Do not use terminal `git push` unless you have terminal GitHub authentication configured.


# Learning Objectives

By the end of this lab, you should be able to:

- Define a base class
- Define derived classes using inheritance
- Override methods in derived classes
- Use polymorphism with a list of related objects
- Explain why inheritance can reduce repeated code

# Assignment

You will complete a simple plant inventory system.

The starter code includes:

```text
starter_code/plant.py
starter_code/garden_inventory.py
```

You will create a base class `Plant`, plus derived classes `Flower` and `Vegetable`.

# Program Requirements

Your program should:

1. Create a list containing `Plant`, `Flower`, and `Vegetable` objects.
2. Loop over the list and print each object.
3. Call the same method on different object types.
4. Demonstrate polymorphism.
5. Include at least one overridden method.

# Required Commits

```text
Commit 1: Add Plant base class
Commit 2: Add Flower derived class
Commit 3: Add Vegetable derived class
Commit 4: Add inventory program and testing
```

# Instructor Checkoff

Possible live requests:

- Add a new derived class.
- Add a method `needs_watering()`.
- Modify the output of one subclass.
- Explain method overriding.
- Explain polymorphism using your program.
