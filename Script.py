#!/usr/bin/env python3.8

from __future__ import annotations

from typing import List, NamedTuple, Set, Tuple, Dict

BookID = int
LibraryID = int

class Library:
    bookqtt: int
    signup: int
    shipping: int
    books: Set[BookID]
    library_id: LibraryID

    def __init__(self, f, id):
        self.library_id = id
        
        line = f.readline().split()
        self.bookqtt = int(line[0]) # the number of books in this library
        self.signup = int(line[1]) # the number of days it takes to sign up this library
        self.shipping = int(line[2]) # the number of books that can be shipped per day
        
        self.books = set()
        line = f.readline().split()
        for i in line:
            self.books.add(int(i))

    def __repr__(self):
        return f"id: {self.library_id} books: {self.bookqtt} signup: {self.signup} shipping: {self.shipping} books: {self.books}"


class Problem(NamedTuple):
    book_scores: List[int]
    days: int
    libraries: List[Library]


def loadfile(filename) -> Tuple[List[int], int, List[Library]]:
    """Determines:
    - the scores of each book (and therefore implicitly how many books there are)
    - the number of days available
    - the libraries that exist
    """
    with open(filename, "r") as f:
        line = f.readline()
        line = line.split()
        books = int(line[0]) # the number of different books that exist
        libqtt = int(line[1]) # the number of different libraries that exist
        days = int(line[2]) # the number of days available

        bookscores: List[int] = [] # map of book ID to book score
        line = f.readline()
        line = line.split()
        for i in line:
            bookscores.append(int(i))

        librarys: List[Library] = []
        for i in range(libqtt):
            librarys.append(Library(f,i))

    return Problem(bookscores, days, librarys)

def savefile(filename: str, books_by_library: List[Tuple[LibraryID, List[BookID]]]):
    """Takes a list of tuples in the form (library ID, list of books sent by that
    library), in the order in which the libraries are signed up. Writes a
    submission file using this data to the given file path.

    For example, [(1, [4, 2, 0]), (0, [6, 9])] indicates that:
      - library ID 1 signs up first and sends 3 books: 4, 2, and 0
      - library ID 0 signs up second and sends 2 books: 6 and 9
    (nice)
    """
    with open(filename, "w") as f:
        f.write(f"{len(books_by_library)}\n")
        for library, books in books_by_library:
            f.write(f"{library} {len(books)}\n")
            f.write(f"{' '.join(str(x) for x in books)}\n")

def bookoccurances(book: BookID, librarys: List[Library]) -> int:
    """Counts the number of libraries which have a particular book."""
    # iow: inversely proportional to book rarity
    # (note that rarity != score)
    val = 0
    for i in librarys:
        if book in i.books:
            val += 1
    return val

def library_value(library, )

if __name__ == "__main__":
    f = loadfile("b_read_on.txt")
    books = f.book_scores
    days = f.days
    librarys = f.libraries
 
    bookmod = []    # number of times the book occurs in total
    for i in range(len(books)):
        bookmod.append(bookoccurances(i,librarys))
    modified_book_value = [] # number of total occurances/number of occurences
    for i in range(len(books)):
        modified_book_value.append(books[i]/bookmod[i]) # calculate modified book value
    
    print(f)
    
    print(bookmod)
    print(books)
    print(modified_book_value)
    
