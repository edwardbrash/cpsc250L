# Lab 8: OOP Review Challenge


class Book:
    def __init__(self, title, author, year, genre, pages, rating):
        """
        Store information about a book.

        You may assume the input values are of the correct type.
        """
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre
        self.pages = pages
        self.rating = rating
        self.amount = 0 # set default stock to zero

    def add_stock(self, amount):
        """
        Increase quantity by amount.
        """
        self.amount += amount


    def sell_copies(self, amount):
        """
        Decrease quantity by amount if enough copies are available.

        Return True if the sale succeeds.
        Return False otherwise.
        """
        if self.amount >= amount:
            self.amount -= amount
            return True
        else:
            return False

    def __str__(self):
        return f"{self.title} by {self.author} ({self.year}) - {self.genre}, {self.pages} pages, rating: {self.rating}/5, stock: {self.amount}"


    def __lt__(self, other):
        """
        Compare books alphabetically by author name, then by title.

        Algorithm:
        Split the author name into fields
        Alphabetize according to the LAST field in the title
        """
        self_author_fields = self.author.split()
        other_author_fields = other.author.split()

        # Compare the last field of the author name
        if self_author_fields[-1] < other_author_fields[-1]:
            return True
        elif self_author_fields[-1] > other_author_fields[-1]:
            return False
        else:
            # If the last field is the same, compare the title
            return self.title < other.title
