# Instructor Notes: Lab 2

## Purpose

Lab 2 is designed to be a gentle transition from environment setup into real programming work.

The programming task is intentionally modest. The main goals are to reinforce:

- synchronizing a GitHub fork
- pulling updates into PyCharm
- running code locally
- using the terminal
- making incremental commits
- explaining code in person

## Suggested In-Class Flow

1. Briefly review Lab 1 workflow.
2. Demonstrate GitHub Sync Fork.
3. Demonstrate Git -> Pull in PyCharm.
4. Have students locate the Lab 2 files.
5. Have students run the incomplete starter program.
6. Students complete the program in stages.
7. Require commits after each major stage.
8. Check off each student before they leave.

## Suggested Timing

- 10 minutes: fork sync and pull demonstration
- 10 minutes: review starter code and data file
- 45--60 minutes: student coding
- 20--30 minutes: checkoffs
- Remaining time: debugging and catch-up

## Expected Final Results

For the provided data file:

- Number of readings: 20
- Minimum temperature: 61.2
- Maximum temperature: 88.1
- Average temperature: 75.865

Rounded to two decimal places, the average is 75.86 or 75.87 depending on formatting conventions.

Python's standard formatting with `{average:.2f}` will display 75.86.

## Good Live Modification Requests

The easiest live modifications are:

- add temperature range: maximum - minimum
- round average to two decimal places
- ignore blank lines
- print whether the average is above or below 75

## Red Flags

A student may need extra help if they cannot explain:

- where the data file is located
- why `Path(__file__)` is being used
- the difference between commit and push
- how the list gets populated
- what their average function is doing

Do not over-penalize syntax confusion at this stage. The major objective is to establish workflow and basic comprehension.
