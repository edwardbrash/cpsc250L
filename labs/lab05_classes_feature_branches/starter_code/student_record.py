# Lab 5: Classes, Objects, and Feature Branches
#
# Complete the StudentRecord class.


class StudentRecord:
    # class constructor
    def __init__(self, name, student_id):
        """
        Create a new student record.

        Parameters:
            name: student name as a string
            student_id: student ID as a string
            scores[]: scores as a list (empty by default)
        """
        self.name = name
        self.student_id = student_id
        self.scores = []

    def add_score(self, score):
        """
        Add one quiz score to this student's list of scores.

        Only add scores between 0 and 100.
        """
        if 0 <= score <= 100:
            self.scores.append(score)


    def calculate_average(self):
        """
        Return the average quiz score.

        If the student has no scores, return None.
        """
        if self.scores:
            return sum(self.scores) / len(self.scores)
        else:
            return None

    def highest_score(self):
        """
        Return the highest quiz score.

        If the student has no scores, return None.
        """
        if self.scores:
            return max(self.scores)
        else:
            return None

    def lowest_score(self):
        """
        Return the lowest quiz score.

        If the student has no scores, return None.
        """
        if self.scores:
            return min(self.scores)
        else:
            return None

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
        average = self.calculate_average()
        if average is None:
            return "N/A"
        elif average >= 87:
            return "A"
        elif average >= 77:
            return "B"
        elif average >= 67:
            return "C"
        elif average >= 57:
            return "D"
        else:
            return "F"

    def __str__(self):
        """
        Return a readable string representation of the student record.
        """
        # maybe this could be fancied up later!
        return f"StudentRecord(name={self.name}, student_id={self.student_id}, scores={getattr(self, 'scores', [])})"
