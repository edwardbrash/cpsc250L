# Lab 6: Collections of Objects
from time import struct_time

from student_record import StudentRecord


def clean_score(score_text):
    """
    Convert score text to an integer.

    Return None if the score is missing or invalid.
    """
    if score_text is None:
        return None
    score_text = score_text.strip()
    if score_text == "":
        return None
    try:
        return int(score_text)
    except ValueError:
        return None

def calculate_average(scores):
    sum = 0.0
    count = 0
    for score in scores:
        if score is not None:
            sum += score
            count += 1
    if count > 0:
        return sum / count
    else:
        return None

import csv

def read_student_records(filename):
    """
    Read the CSV file and return a list of StudentRecord objects.
    """
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        records = []
        # skip header
        csv_header = next(csv_reader)
        for row in csv_reader:
            student_id = row[0]
            name = row[1]
            score_list = row[2:]
            scores = [clean_score(score) for score in score_list]
            record = StudentRecord(name, student_id, scores)
            records.append(record)
    return records



def class_average(students):
    """
    Return the average of all student averages.

    Ignore students with no valid scores.
    """
    sum = 0.0
    count = 0
    for student in students:
        average_this_student = calculate_average(student.scores)
        if average_this_student is not None:
            sum += average_this_student
            count += 1
    if count > 0:
        return sum / count
    else:
        return None


def find_highest_average_student(students):
    """
    Return the StudentRecord object with the highest average.
    """
    max_average = 0
    highest_student = None
    for student in students:
        average_this_student = calculate_average(student.scores)
        if average_this_student > max_average:
            highest_student = student
            max_average = average_this_student
    return highest_student

def find_lowest_average_student(students):
    """
    Return the StudentRecord object with the lowest average.
    """
    min_average = 100
    lowest_student = None
    for student in students:
        average_this_student = calculate_average(student.scores)
        if average_this_student < min_average:
            lowest_student = student
            min_average = average_this_student
    return lowest_student


def print_class_report(students):
    """
    Print all student records and a class summary.
    """
    for student in students:
        print(student)
    print(f'Class average: {class_average(students):.2f}')
    high_student = find_highest_average_student(students)
    low_student = find_lowest_average_student(students)
    print(f'Highest average: {high_student.name} with {calculate_average(high_student.scores):.2f}')
    print(f'Lowest average: {low_student.name} with {calculate_average(low_student.scores):.2f}')



def main():
    students = read_student_records("../data/student_scores.csv")
    print_class_report(students)


main()
