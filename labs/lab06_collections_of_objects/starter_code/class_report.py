# Lab 6: Collections of Objects

from student_record import StudentRecord


def clean_score(score_text):
    """
    Convert score text to an integer.

    Return None if the score is missing or invalid.
    """
    pass


def read_student_records(filename):
    """
    Read the CSV file and return a list of StudentRecord objects.
    """
    pass


def class_average(students):
    """
    Return the average of all student averages.

    Ignore students with no valid scores.
    """
    pass


def find_highest_average_student(students):
    """
    Return the StudentRecord object with the highest average.
    """
    pass


def find_lowest_average_student(students):
    """
    Return the StudentRecord object with the lowest average.
    """
    pass


def print_class_report(students):
    """
    Print all student records and a class summary.
    """
    pass


def main():
    students = read_student_records("../data/student_scores.csv")
    print_class_report(students)


main()
