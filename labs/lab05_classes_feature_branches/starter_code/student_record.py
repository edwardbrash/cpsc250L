# Lab 5: Classes, Objects, and Feature Branches
#
# Complete the StudentRecord class.


class StudentRecord:
    def __init__(self, name, student_id):
        """
        Create a new student record.

        Parameters:
            name: student name as a string
            student_id: student ID as a string
        """
        pass

    def add_score(self, score):
        """
        Add one quiz score to this student's list of scores.

        Only add scores between 0 and 100.
        """
        pass

    def calculate_average(self):
        """
        Return the average quiz score.

        If the student has no scores, return None.
        """
        pass

    def highest_score(self):
        """
        Return the highest quiz score.

        If the student has no scores, return None.
        """
        pass

    def lowest_score(self):
        """
        Return the lowest quiz score.

        If the student has no scores, return None.
        """
        pass

    def letter_grade(self):
        """
        Return a letter grade based on the student's average.

        Suggested scale:
            A: average >= 87
            B: average >= 77
            C: average >= 67
            D: average >= 57
            F: otherwise
        """
        pass

    def __str__(self):
        """
        Return a readable string representation of the student record.
        """
        return "dummy string"
