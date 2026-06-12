"""
CPSC 250L
Lab 2: Python Review and Git Fundamentals

This program reads temperature data from a text file and computes
basic statistics.

Complete the TODO sections below.
"""

import statistics

from pathlib import Path

def read_temperatures(filename):
    """
    Read temperature values from a text file.

    Each line of the file should contain one number.

    Parameters
    ----------
    filename : str or Path
        Path to the input data file.

    Returns
    -------
    list of float
        Temperature values read from the file.
    """
    temperatures = []

    with open(filename, "r") as f:
        for line in f:
            temperatures.append(float(line))
    return temperatures


def compute_average(values):
    """
    Compute the average of a list of numbers.
    """
    return statistics.mean(values)


def compute_minimum(values):
    """
    Compute the minimum value in a list of numbers.
    """
    return min(values)


def compute_maximum(values):
    """
    Compute the maximum value in a list of numbers.
    """
    return max(values)


def print_summary(values):
    """
    Print a formatted summary of the temperature data.
    """
    count = len(values)
    minimum = compute_minimum(values)
    maximum = compute_maximum(values)
    average = compute_average(values)

    # TODO: Improve this output formatting.
    print("Temperature Summary")
    print("Number of readings:", count)
    print(f"Minimum temperature: {minimum:.2f}")
    print(f"Maximum temperature: {maximum:.2f}")
    print(f"Average temperature: {average:.2f}")


def main():
    """
    Main program function.
    """
    data_file = Path(__file__).resolve().parent.parent / "data" / "temperatures.txt"
    temperatures = read_temperatures(data_file)
    print_summary(temperatures)


if __name__ == "__main__":
    main()
