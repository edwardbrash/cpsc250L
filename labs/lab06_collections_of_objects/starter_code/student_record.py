# Lab 6: Collections of Objects
#
# Complete this class. You may reuse ideas from Lab 5.
import csv

class StudentRecord:
    def __init__(self, name, student_id, scores):

        self.name = name
        self.student_id = student_id
        self.scores = scores

    def add_score(self, score):

        if 0 <= score <= 100:
            self.scores.append(score)

    def calculate_average(self):

        a = len(self.scores)
        sum = 0.0
        for score in self.scores:
            sum = sum + score
        average = sum / a
        return average

    def highest_score(self):

        return max(self.scores)

    def lowest_score(self):

        return min(self.scores)

    def letter_grade(self):

        average = self.calculate_average()
        if average >= 87:
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

        StudentRecord = (f'StudentRecord(name = {self.name}, student_id = {self.student_id}, scores = {self.scores})')
        return StudentRecord

    def add_score(self, score):
        if 0 <= score <= 100:
            self.scores.append(score)

    def calculate_average(self):
        a = len(self.scores)
        sum = 0.0
        for score in self.scores:
            sum = sum + score
        average = sum / a
        return average

    def highest_score(self):
        return max(self.scores)

    def lowest_score(self):
        return min(self.scores)

    def letter_grade(self):
        average = self.calculate_average()
        if average >= 87:
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
        StudentRecord = (f'StudentRecord(name = {self.name}, student_id = {self.student_id}, scores = {self.scores})')
        return StudentRecord
