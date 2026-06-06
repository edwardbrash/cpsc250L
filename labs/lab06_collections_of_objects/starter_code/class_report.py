# Lab 6: Collections of Objects

from student_record import StudentRecord
import csv

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
    """
    Calculate the average of a list of numeric scores.

    If the list is empty, return None.
    """
    if scores is None:
        return None
    valid_scores = [score for score in scores if score is not None]
    if not valid_scores:
        return None
    return sum(valid_scores) / len(valid_scores)

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
            id = row[0]
            name = row[1]
            score_texts = row[2:]
            scores = [clean_score(score) for score in score_texts]
            record = StudentRecord(name, id)
            record.add_score(scores)
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
    highest_student = None
    for student in students:
        if student.calculate_average() is not None:
            if highest_student is None or student.calculate_average() > highest_student.calculate_average():
                highest_student = student
    return highest_student


def find_lowest_average_student(students):
    """
    Return the StudentRecord object with the lowest average.
    """
    lowest_student = None
    for student in students:
        if student.calculate_average() is not None:
            if lowest_student is None or student.calculate_average() < lowest_student.calculate_average():
                lowest_student = student
    return lowest_student


def print_class_report(students):
    """
    Print all student records and a class summary.
    """
    for student in students:
        print(student)
    print(f"Class average: {class_average(students):.2f}")
    highest_student = find_highest_average_student(students)
    if highest_student is not None:
        print(f"Highest average: {highest_student.name} with {highest_student.calculate_average():.2f}")
    lowest_student = find_lowest_average_student(students)
    if lowest_student is not None:
        print(f"Lowest average: {lowest_student.name} with {lowest_student.calculate_average():.2f}")

def main():
    students = read_student_records("../data/student_scores.csv")
    print_class_report(students)

main()
