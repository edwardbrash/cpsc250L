# Instructor Notes: Lab 4

## Primary Goals

This lab reinforces:

- file I/O
- CSV-style data processing
- string splitting
- type conversion
- data cleaning
- functions
- lists and dictionaries
- incremental Git workflow

## Why This Lab Matters

Students often assume that data arrives cleanly formatted. This lab introduces the more realistic idea that data may contain missing, invalid, or inconsistent entries.

This is also a good point to reinforce that writing code means anticipating possible problems, not just handling the perfect case.

## Suggested Live Modification Requests

Easy:

- Print the number of valid quiz scores for each student.
- Round averages to one decimal place.
- Count students with averages above 80.

Medium:

- Add a fourth quiz column to the CSV file.
- Print the name of the student with the highest average.
- Change the letter-grade scale.

Harder:

- Treat missing scores as zero instead of ignoring them.
- Print a warning message for each invalid score.
- Sort students by average before printing.

## Suggested Discussion Questions

- Why do we skip the first row?
- Why does `split(",")` work for this file?
- Why might `split(",")` not be enough for every CSV file?
- What is the difference between `None`, `0`, and an empty string?
- Why use a list of dictionaries instead of separate lists?

## Git Workflow Reminder

Students should make multiple commits.

During checkoff, consider asking them to show `git log` or the commit history in PyCharm/GitHub.
