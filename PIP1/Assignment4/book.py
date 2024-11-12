class Book:
    def __init__(self, name, author, book_id, release_year):
        self._name = name
        self.author = author
        self.availability = True
        self.book_id = book_id
        self.release_year = release_year


    def borrowBook(self):
        if self.availability:
            self.availability = False
        else:
            print("The book " +  self._name + " is not available.")


    def returnBook(self):
        self.availability = True


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name


    def __eq__(self, other):
        if isinstance(other, Book):
            # compare e.g. only names
            # return self.name == other.name
            # compare all properties (2 ways)
            # return self.__dict__ == other.__dict__
            return vars(self) == vars(other)
        return False

    def __ne__(self, other):
        if isinstance(other, Book):
            # Compare only names
            # return self.name != other.name
            # Compare all properties (2 ways)
            # return self.__dict__ != other.__dict__
            return vars(self) != vars(other)
        return False


    def __str__(self):
        return self.name + ", written by " + self.author + " in the year " + str(self.release_year) + "."


book = Book("Process", "Franz Kafka", 1, 1925)
print(book)

book.borrowBook()
book.borrowBook()

book2 = Book("Process", "Franz Kafka", 1, 1925)
book3 = Book("Process", "Franz Kafka", 1, 1925)
book4 = Book("The Origin", "Dan Brown", 1, 2017)

print("\nComparisons")
print(book2 == book3)
print(book2 != book3)
print(book3 == book4)
print(book3 != book4)
