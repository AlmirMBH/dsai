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
            print(f'The book "{self._name}" is not available.')


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
            return self.name == other.name
        return False


    def __ne__(self, other):
        if isinstance(other, Book):
            return self.name != other.name
        return False


    def __str__(self):
        return f'{self.name}, written by {self.author} in the year {self.release_year}.'

# Example usage
book = Book("Process", "Franz Kafka", 1, 1925)
print(book)

book.borrowBook()
book.borrowBook()
