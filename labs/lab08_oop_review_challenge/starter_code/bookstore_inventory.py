# Lab 8: Object-Oriented Programming Review Challenge

from book import Book
import csv

def create_inventory():
    """
    Read books from csv file, create and return a list of Book objects.
    """
    books = []

    with open("../data/booklist.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        csv_header = next(csv_reader) # skip header
        for row in csv_reader:
            title = row[0]
            author = row[1]
            year = row[2]
            genre = row[3]
            pages = row[4]
            rating = row[5]
            new_book = Book(title, author, year, genre, pages, rating)
            books.append(new_book)

    return books


def print_inventory(books):
    """
    Print every book in the inventory.
    """
    for book in books:
        print(book)


def total_inventory(books):
    """
    Return the total number of all books in inventory.
    """
    total = 0
    for book in books:
        total += book.amount
    return total


def find_by_author(books, author):
    """
    Return a list of books written by the specified author.
    """
    author_books = []
    for book in books:
        if book.author == author:
            author_books.append(book)
    return author_books


def find_low_stock(books, threshold):
    """
    Return a list of books whose quantity is less than or equal to threshold.
    """
    low_stock_books = []
    for book in books:
        if book.amount <= threshold:
            low_stock_books.append(book)
    return low_stock_books


def print_books(books):
    """
    Print a list of books.
    """
    for book in books:
        print(book)


def main():
    inventory = create_inventory()

    print("Full Inventory")
    print("--------------")
    print_inventory(inventory)

    print()
    print("Total inventory:", total_inventory(inventory))

    print()
    print("Books by Octavia Butler")
    print("-----------------------")
    print_books(find_by_author(inventory, "Octavia Butler"))

    print()
    print("Low Stock Books")
    print("---------------")
    print_books(find_low_stock(inventory, 3))

    print()
    print("Sorted by Title")
    print("---------------")
    sorted_books = sorted(inventory)
    print_books(sorted_books)


main()
